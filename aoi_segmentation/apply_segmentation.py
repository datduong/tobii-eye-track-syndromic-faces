import cv2
import json
import numpy as np
import pandas as pd
import os, re
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys

from argparse import ArgumentParser

import matplotlib.pyplot as plt

import aoi_to_segmentation 

# ---------------------------------------------------------------------------- #

def apply_segmentation(img_dir, threshold, transparent_to_white, args): 
  """_summary_

  Args:
      img_dir (_type_): _description_
      threshold (_type_): _description_
      transparent_to_white (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  images = os.listdir(img_dir)
  if args.filter_by_word is not None: 
    images = [ i for i in images if re.match(args.filter_by_word,i) ]
  
  images = [i for i in images if ('otsu' not in i)] # ! only ourput images will have "otsu" name attached to it
  images = [i for i in images if ('thresh' not in i)]
  
  seg_dict = {} # save all segmentations in dict
  for img in images: 
    x, y = aoi_to_segmentation.cam_to_segmentation(   cam_mask = img, 
                                                      threshold = threshold,
                                                      smoothing = args.if_smoothing,
                                                      k = args.k,
                                                      img_dir = img_dir,
                                                      prefix = '',
                                                      transparent_to_white = transparent_to_white,
                                                      resize = args.resize,
                                                      plot_segmentation = args.plot_segmentation,
                                                      cut_off_pixel = args.cut_off_pixel
                                                      )

    seg_dict [ img ] = {'segmentation':x, 'image':y} # save both
  #
  return seg_dict


def average_segmentation (dict_segment,round_to_int=False,args=None): 
  """_summary_

  Args:
      dict_segment (dict): {image1:[h,w], image2:[h,w]}
      round_to_int (bool, optional): _description_. Defaults to False.

  Returns:
      _type_: _description_
  """
  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  arr=np.zeros(dict_segment[imlist[0]]['segmentation'].shape,float)
  for im in imlist:
    arr=arr+dict_segment[im]['segmentation']

  # average 
  arr = arr/N # ! @arr is matrix 720x720 (or so), has values 0-1. 1=white pixel
  ave =np.array(np.round(arr),dtype=int)
  
  # ! SMOOTH? 
  if args.if_smoothing: 
    arr = cv2.boxFilter(arr, -1, (1, 1))
    arr = np.array(arr)

  if args.scale_ave_pixel:
    arr = scale_by_ave_pixel_one_image (arr) # ! put on same scale, so easier to compare between 2 groups
    ave = scale_by_ave_pixel_one_image (ave)
  
  if round_to_int: # Round values in array and cast as 8-bit integer
    arr=np.array(np.round(arr),dtype=int)
    
  return arr, ave


def average_image (dict_segment,size=(720,720),args=None): 

  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  arr=np.zeros((size),float) # make empty array of 0
  for im in imlist:  
    arr=arr+np.array(dict_segment[im]['image'],dtype=float) # may not need np.array if img is already in np.

  # average 
  arr = arr/N

  if args.scale_ave_pixel: 
    arr = scale_by_ave_pixel_one_image (arr,target=125,maxval=255,criteria_pixel=0,flip_01=True) # ! DOES NOT WORK WELL? 

  # Round values 
  arr=np.array(np.round(arr),dtype=np.uint8)
  return arr 


def scale_by_ave_pixel_one_image(arr,target=0.5,maxval=1,criteria_pixel=0,flip_01=False): 
  """_summary_

  Args:
      arr (_type_): H x W matrix, should have value 0 to 1? 1=white 0=black pixel. 
                      not need to be 0-1 though can be any other value?
      target (int, optional): _description_. Defaults to 125.

  Returns:
      _type_: _description_
  """
  arr = np.array(arr,dtype=float)
  if flip_01: 
    arr = maxval-arr
  new_arr_no_0 = arr[np.where(arr!=criteria_pixel)] 
  new_arr_no_0 = np.mean(new_arr_no_0)
  arr = np.where( arr!=criteria_pixel, arr*target/new_arr_no_0, criteria_pixel ) # ! scale so new mean without @criteria matches @target
  arr = np.where( arr>maxval, maxval, arr)
  if flip_01:
    arr = maxval-arr
  return arr


def segementation_ave_image (dict_segment,size,args): 
  """_summary_

  Args:
      dict_segment (_type_): _description_
      size (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  ave_im = average_image (dict_segment, size=size, args=args)
  seg_im, _ = aoi_to_segmentation.cam_to_segmentation(  cam_mask = ave_im, 
                                                        threshold = args.threshold_group_1, # ! should use same setting for both set? 
                                                        smoothing = args.if_smoothing,
                                                        k = args.k,
                                                        img_dir = '',
                                                        prefix = '', 
                                                        transparent_to_white = False,
                                                        resize = args.resize,
                                                        plot_segmentation = False,
                                                        cut_off_pixel = None # ! don't need this if we already filter low pixel in individual img?
                                                        )

  return seg_im, ave_im
  
def diff_two_sets(dict1,dict2,args): 
  """_summary_

  Args:
      dict1 (_type_): _description_
      dict2 (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  # average images in @dict1, compute @cam_to_segmentation of this average? 
  # average segmentation in @dict1, compute @cam_to_segmentation of this average? 
  # aoi_to_segmentation.calculate_iou
  if args.boot_ave_segmentation: 
    seg_im1, _ = average_segmentation(dict1, round_to_int=True,args=args)
    seg_im2, _ = average_segmentation(dict2, round_to_int=True,args=args)
  else: 
    seg_im1, _ = segementation_ave_image (dict1,size=(720,720),args=args)  
    seg_im2, _ = segementation_ave_image (dict2,size=(720,720),args=args)

  #
  mIOU = aoi_to_segmentation.calculate_iou(seg_im1, seg_im2, true_pos_only=False) 
  return mIOU


def one_bootstrap_sample (dict1, dict2, args):
  """_summary_

  Args:
      dict1 (_type_): _description_
      dict2 (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  N1 = len(dict1)
  N2 = len(dict2)
  dict_arr = [dict1,dict2]
  prob_1_2 = np.array ([N1,N2]) / (N1+N2)
  # create a bootstrap sample
  boot_sample = []
  for index, N in enumerate([N1,N2]): 
    boot_dict = {}
    for n in range(N): 
      this_dict = dict_arr[np.random.choice(2,size=1,p=prob_1_2)[0]] # pick dictionary 0 or 1 with equal chance, or scale? 
      pick_this_person = np.random.choice(list(this_dict.keys()),size=1)[0]
      pick_this_data_point = this_dict[pick_this_person]
      if pick_this_person in boot_dict: 
        pick_this_person = pick_this_person + str(n)
      #
      boot_dict[pick_this_person] = pick_this_data_point
    #
    boot_sample.append( boot_dict )

  # 
  boot_statistics = diff_two_sets(boot_sample[0],boot_sample[1],args)

  return boot_statistics



def load_data (group_name, segmentation_of_group, args): 
  """_summary_

  Args:
      group_name (_type_): _description_
      segmentation_of_group (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  
  # ! process data of 1 group, create output name
  prefix = 'smoothk'+str(args.k) if args.if_smoothing else 'nosmooth'
  prefix = prefix + '-thresh'+str(args.threshold_group_1) if args.threshold_group_1 is not None else prefix+'-otsu'
  prefix = prefix + '-scale_ave_pix' if args.scale_ave_pixel else prefix
  prefix = prefix + '-boot_seg' if args.boot_ave_segmentation else prefix

  # ! take average of segmentation 
  if args.boot_ave_segmentation: 
    ave, img = average_segmentation(segmentation_of_group, round_to_int=True, args=args)
    out=Image.fromarray(np.uint8(img*255),mode="L")
    out.save(os.path.join(args.output_dir,prefix+"_seg_raw_ave"+group_name+".png"))

  # ! average image, then take segmentation of average 
  else: 
    ave, img = segementation_ave_image (segmentation_of_group, size=(720,720), args=args)
    img = np.array(img,dtype=np.uint8)
    out=Image.fromarray(img,mode="L")  # ! if use np.array(img*255,dtype=np.unit8) then get a black background. 
    out.save(os.path.join(args.output_dir,prefix+"_img_ave"+group_name+".png"))
    
  out=Image.fromarray(np.uint8(ave*255),mode="L") 
  out.save(os.path.join(args.output_dir,prefix+"_seg_ave"+group_name+".png"))

  return ave, img, prefix


# ---------------------------------------------------------------------------- #

# ! main 

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--img_dir', type=str,
                        help='path to images')

  parser.add_argument('--if_smoothing', action='store_true',
                        help='If true, smooth the pixelated heatmaps using box \
                              filtering.')
   
  parser.add_argument('--k', type=int, default=0,
                        help='size of kernel used for box filter smoothing (int); \
                              k must be >= 0; if k is > 0, make sure to set \
                              if_smoothing to True, otherwise no smoothing would \
                              be performed.')

  parser.add_argument('--threshold_group_1', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--threshold_group_2', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--resize', type=int, default=None, 
                        help='resize images, before doing this, make sure faces are properly aligned')

  parser.add_argument('--img_dir_group_1', type=str,
                        help='')

  parser.add_argument('--filter_by_word', type=str, default=None, 
                        help='')

  parser.add_argument('--img_dir_group_2', type=str,
                        help='')

  parser.add_argument('--output_dir', type=str,
                        help='')

  parser.add_argument('--plot_segmentation', action='store_true', default=False,
                        help='')

  parser.add_argument('--boot_num', type=int, default=None, 
                        help='')

  parser.add_argument('--boot_ave_segmentation', action='store_true', default= False,
                        help='')

  parser.add_argument('--cut_off_pixel', type=float, default=None, 
                        help='')

  parser.add_argument('--scale_ave_pixel', action='store_true', default=False,
                        help='')

  # ---------------------------------------------------------------------------- #
  
  parser.add_argument('--metric', type=str,
                      help='options are: iou or hitmiss')
  parser.add_argument('--gt_path', type=str,
                      help='directory where ground-truth segmentations are \
                            saved (encoded)')
  parser.add_argument('--pred_path', type=str,
                      help='json path where predicted segmentations are saved \
                            (if metric = iou) or directory with pickle files \
              containing heat maps (if metric = hitmiss and \
                            if_human_benchmark = false) or json path with \
                            human annotations for most representative points \
                            (if metric = hitmiss and if_human_benchmark = \
                            true)')
  parser.add_argument('--true_pos_only', type=str, default='True',
                      help='if true, run evaluation only on the true positive \
                      slice of the dataset (CXRs that contain predicted and \
                      ground-truth segmentations); if false, also include cxrs \
                      with a predicted segmentation but without a ground-truth \
                      segmentation, and include cxrs with a ground-truth\
                      segmentation but without a predicted segmentation.')
  parser.add_argument('--save_dir', default='.',
                      help='where to save evaluation results')
  parser.add_argument('--if_human_benchmark', type=str, default='False',
                      help='if true, scripts expects human benchmark inputs')
  parser.add_argument('--seed', type=int, default=0,
                      help='random seed to fix')
  args = parser.parse_args()


  # ---------------------------------------------------------------------------- #
  if args.resize is not None: 
    args.resize = (args.resize, args.resize)

  # ---------------------------------------------------------------------------- #
  slide_number = args.img_dir_group_1.split('/')[-2] # @slide_number expects input /path/SlideXYZ/GroupABC
  group_name1 = args.img_dir_group_1.split('/')[-1]
  group_name2 = args.img_dir_group_2.split('/')[-1]
  
  # ---------------------------------------------------------------------------- #
  
  # ! get segmentation of Tobii, group 1
  segmentation_group_1 = apply_segmentation(args.img_dir_group_1, threshold=args.threshold_group_1, transparent_to_white=True, args=args)

  # ! get segmentation of Tobii, group 2, or, we get deep learning heatmap as segmentation 
  segmentation_group_2 = apply_segmentation(args.img_dir_group_2, threshold=args.threshold_group_2, transparent_to_white=True, args=args)

  if args.boot_num is None: 
    # get name 
    prefix = 'smoothk'+str(args.k) if args.if_smoothing else 'nosmooth'
    # prefix = '-cut'+str(args.cut_off_pixel) if args.cut_off_pixel is not None else '-nocut'
    prefix = prefix + '-' + 'thresh'+str(args.threshold_group_1) if args.threshold_group_1 is not None else prefix+'otsu'
    prefix = prefix + '-scale_ave_pixel' if args.scale_ave_pixel else prefix

    # ! run simple mean/std of the differences 
    for model_name in segmentation_group_2: 
      mIoU = []
      for person in segmentation_group_1: 
        temp = aoi_to_segmentation.calculate_iou(segmentation_group_1[person], segmentation_group_2[model_name], true_pos_only=False) 
        mIoU.append(temp)
      #
      ave = np.mean ( np.array(mIoU) ) 
      std = np.std (np.array(mIoU))
      mIoU = mIoU + [ave,std]
      
      # save as csv 
      fout = open(os.path.join(args.output_dir,'many_vs_1_'+group_name1+'_'+group_name2+'_'+prefix+'.csv'),'w')
      fout.write ( model_name + ',' + ','.join ( [str(item) for item in mIoU] ) + '\n')
      fout.close()

  else:

    # ---------------------------------------------------------------------------- #

    # ! process data group 1  
    ave1, _, prefix = load_data (group_name1, segmentation_group_1, args)
    
    # ! process data group 2
    ave2, _, prefix = load_data (group_name1, segmentation_group_1, args)

    # ---------------------------------------------------------------------------- #

    # ! observe statistics 
    obs_stat = diff_two_sets(segmentation_group_1,segmentation_group_2, args=args) 

    # ! do bootstrap 
    boot_stat = []
    for n in range (args.boot_num):
      boot_stat.append (one_bootstrap_sample (segmentation_group_1, segmentation_group_2, args=args))
      
    # ! output
    boot_stat = np.array(boot_stat)
    boot_stat = boot_stat[~np.isnan(boot_stat)]
    
    if len(boot_stat) != args.boot_num:
      args.boot_num = len(boot_stat)

    # 
    ave = np.nanmean ( np.array(boot_stat) ) 
    std = np.nanstd (np.array(boot_stat))
    boot_rank = np.sum( boot_stat > obs_stat)/args.boot_num # ! very high rank --> high pval --> signif (same apply for very low rank)
    
    #
    fout = open(os.path.join(args.output_dir,'many_vs_many_'+group_name1+'_'+group_name2+'_'+prefix+'.csv'),'w')
    fout.write ('image_number,type,group_name1,group_name2,obs_stat,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2\n')
    fout.write ( slide_number+','+prefix+','+group_name1+','+group_name2 + ',' + ','.join ( [str(item) for item in [obs_stat,ave,std,boot_rank,args.boot_num,len(segmentation_group_1),len(segmentation_group_2)]] ) + '\n')
    fout.close()


