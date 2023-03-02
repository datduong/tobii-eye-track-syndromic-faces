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

from copy import deepcopy

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
                                                      cut_pixel_per_img = args.cut_pixel_per_img, 
                                                      hi_threshold = args.hi_threshold_group_1
                                                      )

    seg_dict [ img ] = {'segmentation':x, 'image':y} # save both
  #
  return seg_dict


def ave_of_segmentation (dict_segment,args=None): 
  """_summary_

  Args:
      dict_segment (_type_): _description_
      args (_type_, optional): _description_. Defaults to None.

  Returns:
      _type_: _description_
  """
  
  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  arr=np.zeros(dict_segment[imlist[0]]['segmentation'].shape,float)
  for im in imlist:
    arr=arr+dict_segment[im]['segmentation']

  arr = arr/N # ! @arr is matrix 720x720 (or so), has values 0-1. 1=white pixel

  if args.scale_or_shift_ave_pixel is not None:
    arr = scale_shift_ave_pixel_one_image (arr, target=args.scale_or_shift_ave_pixel) # ! put on same scale, so easier to compare between 2 groups

  threshold_to_binary = args.cut_ave_img_to_binary if args.scale_or_shift_ave_pixel is not None else args.cut_seg_to_binary_1
  seg_im, _ = aoi_to_segmentation.cam_to_segmentation(  cam_mask = arr, 
                                                        threshold = threshold_to_binary, # ! should use same setting for both set? 
                                                        smoothing = True,
                                                        k = args.k,
                                                        img_dir = '',
                                                        prefix = '', 
                                                        transparent_to_white = False,
                                                        resize = args.resize,
                                                        plot_segmentation = False,
                                                        cut_pixel_per_img = None, 
                                                        hi_threshold = args.hi_threshold_group_1
                                                        )
    
  return seg_im, np.array(arr,dtype=float)


def average_image (dict_segment,size=(720,720),args=None): 

  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  arr=np.zeros((size),float) # make empty array of 0
  for im in imlist:  
    arr=arr+np.array(dict_segment[im]['image'],dtype=float) # may not need np.array if img is already in np.

  arr = arr/N # average 

  if args.remove_low_before_scale is not None: 
    arr = np.where(arr>args.remove_low_before_scale, arr, 0) # remove very faint low signal, too many low faint signal will make "visible signals" very bright 
    
  if args.scale_or_shift_ave_pixel is not None: 
    arr = 255 * scale_shift_ave_pixel_one_image (arr/255, target=args.scale_or_shift_ave_pixel) # ! DOES NOT WORK WELL? # put everything in 0/1 scale # bring back to 0/255

  arr=np.array(np.round(arr),dtype=np.uint8) # Round values into proper 0-255
  return arr 


def scale_shift_ave_pixel_one_image(arr,target=0.5,maxval=1,criteria_pixel=0,flip_01=False,scale=True): 
  """_summary_

  Args:
      arr (_type_): _description_
      target (float, optional): _description_. Defaults to 0.5.
      maxval (int, optional): _description_. Defaults to 1.
      criteria_pixel (int, optional): _description_. Defaults to 0.
      flip_01 (bool, optional): _description_. Defaults to False.
      scale (bool, optional): _description_. Defaults to True.

  Returns:
      _type_: _description_
  """
  arr = np.array(arr,dtype=float)
  if flip_01: 
    arr = maxval-arr
  
  new_arr_no_0 = arr[np.where(arr!=criteria_pixel)] 
  new_arr_no_0 = np.mean(new_arr_no_0)
  
  if scale: # ! works a lot better with tobii
    arr = np.where( arr!=criteria_pixel, arr*target/new_arr_no_0, criteria_pixel ) # ! scale so new mean without @criteria matches @target
  else: 
    amount = target - new_arr_no_0 
    arr = np.where( arr!=criteria_pixel, arr+amount, criteria_pixel )
  
  arr = np.where( arr>maxval, maxval, arr) # bound so nothing goes over 255
  arr = np.where( arr<0, 0, arr) # bound at 0 from below
  
  if flip_01:
    arr = maxval-arr
  
  return arr


def segementation_of_ave (dict_segment,size,args): 
  """_summary_

  Args:
      dict_segment (_type_): _description_
      size (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  ave_im = average_image (dict_segment, size=size, args=args) 

  threshold_to_binary = None # ! if we do simple diff, then we don't need @seg_im because @threshold_to_binary acts on @seg_img
  if not args.simple_diff: 
    threshold_to_binary = args.cut_ave_img_to_binary if args.cut_ave_img_to_binary is not None else None # ! scale ave pixel up to brighter value, need to use @cut_ave_img_to_binary

  seg_im, ave_im = aoi_to_segmentation.cam_to_segmentation(   cam_mask = ave_im, 
                                                              threshold = threshold_to_binary, # ! should use same setting for both set? 
                                                              smoothing = args.smooth_ave,
                                                              k = args.k,
                                                              img_dir = '',
                                                              prefix = '', 
                                                              transparent_to_white = False,
                                                              resize = args.resize,
                                                              plot_segmentation = False,
                                                              cut_pixel_per_img = args.cut_pixel_ave_img, 
                                                              hi_threshold = args.hi_threshold_group_1
                                                              )

  return seg_im, ave_im # @ave_im will not be original average if we use "smoothing" and so forth. 

  
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
    seg_im1, ave_im1 = ave_of_segmentation(dict1, args=args)
    if args.compare_vs_this is None: 
      seg_im2, ave_im2 = ave_of_segmentation(dict2, args=args)
  else: 
    seg_im1, ave_im1 = segementation_of_ave (dict1,size=(720,720),args=args)  
    if args.compare_vs_this is None: 
      seg_im2, ave_im2 = segementation_of_ave (dict2,size=(720,720),args=args)

  #
  if args.compare_vs_this is None: 
    if args.simple_diff: 
      score = aoi_to_segmentation.calculate_simple_diff(ave_im1, ave_im2) # ! simple diff on 2 averages of 2 sets of images
    else:
      score = aoi_to_segmentation.calculate_iou(seg_im1, seg_im2, true_pos_only=False) 
  else: 
    if args.simple_diff: 
      score = aoi_to_segmentation.calculate_simple_diff(ave_im1, dict2['image']) 
    else:
      score = aoi_to_segmentation.calculate_iou(seg_im1, dict2['segmentation'], true_pos_only=False) 
  return score


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


def save_img (image,outname,mode="L"): 
  if np.max(np.array(image)) <= 1: 
    image = image*255
  #
  out=Image.fromarray(np.array(image,dtype=np.uint8),mode=mode)
  out.save(outname)
  
  
def average_over_data (group_name, segmentation_of_group, args): 
  """_summary_

  Args:
      group_name (_type_): _description_
      segmentation_of_group (_type_): _description_
      args (_type_): _description_

  Returns:
      _type_: _description_
  """
  
  # ! process data of 1 group, create output name
  prefix = 'k'+str(args.k) if args.if_smoothing else 'k0'
  prefix = prefix + '-pixcut'+str(args.cut_pixel_per_img) if args.cut_pixel_per_img is not None else prefix
  prefix = prefix + '-thresh'+str(args.cut_seg_to_binary_1) if args.cut_seg_to_binary_1 is not None else prefix+'-otsu'
  prefix = prefix + '-cutbfscale'+str(args.remove_low_before_scale) if args.remove_low_before_scale is not None else prefix
  prefix = prefix + '-avepix'+str(args.scale_or_shift_ave_pixel) if args.scale_or_shift_ave_pixel is not None else prefix
  prefix = prefix + '-bootseg' if args.boot_ave_segmentation else prefix
  prefix = prefix + '-smoothave' if args.smooth_ave else prefix
  prefix = prefix + '-pixcutave'+str(args.cut_pixel_ave_img) if args.cut_pixel_ave_img is not None else prefix # smoothing introduce extra "signal" where there wasn't signal, so we need this.
  prefix = prefix + '-round'+str(args.cut_ave_img_to_binary) if args.cut_ave_img_to_binary is not None else prefix
  prefix = prefix + '-diff' if args.simple_diff else prefix

  # ! take average of segmentation 
  if args.boot_ave_segmentation: 
    ave, img = ave_of_segmentation(segmentation_of_group,  args=args)
    save_img ( img, os.path.join(args.output_dir,prefix+"_seg_raw_ave"+group_name+".png") )

  # ! average image, then take segmentation of average 
  else: 
    ave, img = segementation_of_ave (segmentation_of_group, size=(720,720), args=args)
    save_img (img, os.path.join(args.output_dir,prefix+"_img_ave"+group_name+".png") ) # ! if use np.array(img*255,dtype=np.unit8) then get a black background. 

  # 
  if args.simple_diff is False: 
    save_img (ave, os.path.join(args.output_dir,prefix+"_seg_ave"+group_name+".png"))

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

  parser.add_argument('--cut_seg_to_binary_1', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--cut_seg_to_binary_2', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--hi_threshold_group_1', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--hi_threshold_group_2', type=float, default= None,
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

  parser.add_argument('--cut_pixel_per_img', type=float, default=None, 
                        help='')

  parser.add_argument('--scale_or_shift_ave_pixel', type=float, default=None,
                        help='')

  parser.add_argument('--cut_ave_img_to_binary', type=float, default=None, 
                        help='')

  parser.add_argument('--compare_vs_this', type=str, default=None, 
                        help='')

  parser.add_argument('--transparent_to_white', action='store_true', default= False,
                        help='')

  parser.add_argument('--simple_diff', action='store_true', default= False,
                        help='')

  parser.add_argument('--smooth_ave', action='store_true', default= False,
                        help='')

  parser.add_argument('--cut_pixel_ave_img', type=float, default=None, 
                        help='')

  parser.add_argument('--remove_low_before_scale', type=float, default=None, 
                        help='before scale color intensity up, we remove random noise signals (e.g. very low pixel values)') 
  
  
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

  if args.cut_pixel_ave_img is not None: 
    if args.cut_pixel_ave_img < 1: 
      sys.exit("raw pixel cut off from 0-255")   

  if args.cut_pixel_per_img is not None: 
    if args.cut_pixel_per_img < 1: 
      sys.exit("raw pixel cut off from 0-255")  

  
  # ---------------------------------------------------------------------------- #
  
  slide_number1 = args.img_dir_group_1.split('/')[-2] # @slide_number expects input /path/SlideXYZ/GroupABC
  group_name1 = slide_number1 + args.img_dir_group_1.split('/')[-1]

  slide_number2 = args.img_dir_group_2.split('/')[-2]
  group_name2 = slide_number2 + args.img_dir_group_2.split('/')[-1]
  
  # ---------------------------------------------------------------------------- #
  
  # ! get segmentation of Tobii, group 1
  segmentation_group_1 = apply_segmentation(args.img_dir_group_1, threshold=args.cut_seg_to_binary_1, transparent_to_white=args.transparent_to_white, args=args)
  
  # ! process data group 1  
  ave1, _, prefix1 = average_over_data (group_name1, segmentation_group_1, args)

  if args.compare_vs_this is not None: 
    # get name 
    prefix = prefix1

    single_img = np.array (Image.open(args.compare_vs_this).convert("L"), dtype=int)
    segmentation_group_2 = {'segmentation': single_img, 
                            'image': single_img } # duplicate both

    observed_mIOU = diff_two_sets ( segmentation_group_1, segmentation_group_2 , args )

    num_people_to_sample = len(segmentation_group_1)
    mIoU = [] # ! bootstrap only on @segmentation_group_1
    for i in np.arange(args.boot_num): 
      boot_dict = dict() # empty: 
      pick_this_person = np.random.choice( list(segmentation_group_1.keys()), size=num_people_to_sample, replace=True )
      for ip,p in enumerate(pick_this_person): 
        pick_this_data_point = segmentation_group_1[p]
        if p not in boot_dict: 
          boot_dict[p] = deepcopy ( pick_this_data_point ) # need deepcopy? probably not. 
        else: 
          boot_dict[p+str(ip)] = deepcopy ( pick_this_data_point )
      # 
      boot_mIOU = diff_two_sets ( boot_dict, segmentation_group_2 , args )
      mIoU.append(boot_mIOU)
      
    # end boot
    ave = np.nanmean ( np.array(mIoU) ) 
    std = np.nanstd (np.array(mIoU))
    boot_output = [observed_mIOU,ave,std]
    
    # save as csv 
    model_name = args.compare_vs_this.split('/')[-1]
    fout = open(os.path.join(args.output_dir,'saliency-vs-'+group_name1+'_'+prefix+'.csv'),'w')
    fout.write ('saliency,tobii,observed_stat,mean,std,group_size\n')
    fout.write ( model_name + ',' + group_name1 + ',' + ','.join ( [str(item) for item in boot_output] ) + ',' + str(len(segmentation_group_1)) + '\n')
    fout.close()

  else:

    # ! get segmentation of Tobii, group 2, or, we get deep learning heatmap as segmentation 
    segmentation_group_2 = apply_segmentation(args.img_dir_group_2, threshold=args.cut_seg_to_binary_2, transparent_to_white=args.transparent_to_white, args=args)

    # ---------------------------------------------------------------------------- #
 
    # ! process data group 2
    ave2, _, prefix2 = average_over_data (group_name2, segmentation_group_2, args)

    # ---------------------------------------------------------------------------- #

    # ! observe statistics 
    obs_stat = diff_two_sets(segmentation_group_1,segmentation_group_2, args=args) 

    # ! do bootstrap 
    total_sample = len(segmentation_group_1) + len(segmentation_group_2) # ! edit boot number? 
    call_combo = total_sample**total_sample
    if call_combo < args.boot_num : # ! in some cases, sample size too small.
      args.boot_num = np.min ( [ int(call_combo * 1.5) , args.boot_num ] )# let's say we have 2 groups, size 1 and 3, then that's 4**4 = 256, now 256*2. 

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
    if prefix1==prefix2: 
      prefix = prefix1
    else:
      prefix = prefix1 + prefix2

    fout = open(os.path.join(args.output_dir,group_name1+'-vs-'+group_name2+'_'+prefix+'.csv'),'w')
    fout.write ('image_number,type,group_name1,group_name2,obs_stat,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2\n')
    fout.write ( slide_number1+'+'+slide_number2+','+prefix+','+group_name1+','+group_name2 + ',' + ','.join ( [str(item) for item in [obs_stat,ave,std,boot_rank,args.boot_num,len(segmentation_group_1),len(segmentation_group_2)]] ) + '\n')
    fout.close()


