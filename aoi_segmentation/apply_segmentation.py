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
  #
  images = [i for i in images if ('otsu' not in i)] # ! only ourput images will have "otsu" name attached to it
  images = [i for i in images if ('thresh' not in i)]
  print (images)
  seg_dict = {} # save all segmentations in dict
  for img in images: 
    # cam_mask, threshold=np.nan, smoothing=False, k=0, workdir=None, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=None
    seg_dict [ img ]  = aoi_to_segmentation.cam_to_segmentation(  cam_mask = img, 
                                                                  threshold = threshold,
                                                                  smoothing = args.if_smoothing,
                                                                  k = args.k,
                                                                  img_dir = img_dir,
                                                                  prefix = '', 
                                                                  transparent_to_white = transparent_to_white,
                                                                  resize = args.resize,
                                                                  plot_segmentation = args.plot_segmentation
                                                                  )
  #
  return seg_dict


def average_segmentation (dict_segment,round_to_int=False): 
  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  arr=np.zeros(dict_segment[imlist[0]].shape,float)
  for im in imlist:
    arr=arr+dict_segment[im] # ['segmentation']

  # average 
  arr = arr/N

  if round_to_int: # Round values in array and cast as 8-bit integer
    arr=np.array(np.round(arr),dtype=int)
  
  return arr

def average_image (dict_segment): 
  imlist = list ( dict_segment.keys() ) 
  N = len(imlist)*1.0 # float
  w,h=Image.open(imlist[0]).size
  arr=np.zeros((h,w,1),float)
  for im in imlist:  
    arr=arr+np.array(dict_segment[im]['image'],dtype=float) # may not need np.array if img is already in np.

  # average 
  arr = arr/N
  # Round values in array and cast as 8-bit integer # this is needed for image
  arr=np.array(np.round(arr),dtype=np.uint8)
  return arr 
  
def diff_two_sets(dict1,dict2): 
  # average images in @dict1, compute @cam_to_segmentation of this average? 
  # average segmentation in @dict1, compute @cam_to_segmentation of this average? 
  # aoi_to_segmentation.calculate_iou
  ave1 = average_segmentation(dict1, round_to_int=True)
  ave2 = average_segmentation(dict2, round_to_int=True)
  mIOU = aoi_to_segmentation.calculate_iou(ave1, ave2, true_pos_only=False) 
  return mIOU


def one_bootstrap_sample (dict1, dict2):
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
  boot_statistics = diff_two_sets(boot_sample[0],boot_sample[1])

  return boot_statistics


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

  parser.add_argument('--threshold_tobii', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--threshold_model', type=float, default= None,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--resize', type=int, default=None, 
                        help='resize images, before doing this, make sure faces are properly aligned')

  parser.add_argument('--img_dir_tobii', type=str,
                        help='')

  parser.add_argument('--filter_by_word', type=str, default=None, 
                        help='')

  parser.add_argument('--img_dir_model', type=str,
                        help='')

  parser.add_argument('--output_dir', type=str,
                        help='')

  parser.add_argument('--plot_segmentation', action='store_true',
                        help='')

  parser.add_argument('--boot_num', type=int, default=None, 
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
  
  # ! get segmentation of Tobii
  tobii_segmentation = apply_segmentation(args.img_dir_tobii, threshold=args.threshold_tobii, transparent_to_white=True, args=args)

  # ! get deep learning heatmap as segmentation 
  # if args.if_smoothing is False: 
  #   args.if_smoothing = True
  
  model_segmentation = apply_segmentation(args.img_dir_model, threshold=args.threshold_model, transparent_to_white=True, args=args)

  if args.boot_num is None: 
    # ! run simple mean/std of the differences 
    for model_name in model_segmentation: 
      mIoU = []
      for person in tobii_segmentation: 
        temp = aoi_to_segmentation.calculate_iou(tobii_segmentation[person], model_segmentation[model_name], true_pos_only=False) 
        mIoU.append(temp)
      #
      ave = np.mean ( np.array(mIoU) ) 
      std = np.std (np.array(mIoU))
      mIoU = mIoU + [ave,std]
      
      # save as csv 
      fout = open(os.path.join(args.output_dir,'output_simple_mean.csv'),'w')
      print (mIoU)
      fout.write ( model_name + ',' + ','.join ( [str(item) for item in mIoU] ) + '\n')
      # end write out
      fout.close()

  else:
    ave1 = average_segmentation(tobii_segmentation, round_to_int=True)
    out=Image.fromarray(np.uint8(ave1*255),mode="L") # Image.fromarray(np.uint8(segmentation*255), 'L')
    out.save(os.path.join(args.output_dir,"SegAverage1.png"))
    
    ave2 = average_segmentation(model_segmentation, round_to_int=True)
    out=Image.fromarray(np.uint8(ave2*255),mode="L")
    out.save(os.path.join(args.output_dir,"SegAverage2.png"))

    obs_stat = diff_two_sets(tobii_segmentation,model_segmentation) 
    boot_stat = []
    for n in range (args.boot_num):
      boot_stat.append (one_bootstrap_sample (tobii_segmentation, model_segmentation))
      
    #
    boot_stat = np.array(boot_stat)
    ave = np.mean ( np.array(boot_stat) ) 
    std = np.std (np.array(boot_stat))
    print (obs_stat)
    print (ave)
    print (std)
    print ('rank', np.sum( boot_stat > obs_stat))
    

  


