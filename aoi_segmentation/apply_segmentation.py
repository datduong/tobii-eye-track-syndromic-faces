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

def apply_segmentation(img_dir, transparent_to_white, args): 
  images = os.listdir(img_dir)
  if args.filter_by_word is not None: 
    images = [ i for i in images if re.match(args.filter_by_word,i) ]
  #
  seg_dict = {} # save all segmentations in dict
  for img in images: 
    # cam_mask, threshold=np.nan, smoothing=False, k=0, workdir=None, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=None
    seg_dict [ img ]  = aoi_to_segmentation.aoi_to_segmentation(  cam_mask = img, 
                                                                  threshold = args.threshold,
                                                                  smoothing = args.smoothing,
                                                                  k = args.k,
                                                                  workdir = img_dir,
                                                                  prefix = '', 
                                                                  transparent_to_white = transparent_to_white,
                                                                  resize = args.resize,
                                                                  plot_segmentation = args.plot_segmentation
                                                                  )
  #
  return seg_dict


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

  parser.add_argument('--threshold', type=float,
                        help="threshold heatmap, will not use otsu")

  parser.add_argument('--resize', type=int, default=None, 
                        help='resize images, before doing this, make sure faces are properly aligned')

  parser.add_argument('--img_dir_tobii', type=str,
                        help='')

  parser.add_argument('--img_dir_model', type=str,
                        help='')

  parser.add_argument('--output_csv', type=str,
                        help='')

  parser.add_argument('--plot_segmentation', action='store_true',
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
  tobii_segmentation = apply_segmentation(args.img_dir_tobii, transparent_to_white=True, args=args)

  # ! get deep learning heatmap as segmentation 
  if args.if_smoothing is False: 
    args.if_smoothing = True
  
  model_segmentation = apply_segmentation(args.img_dir_model, transparent_to_white=False, args=args)

  # ! run simple mean/std of the differences 
  for model_name in model_segmentation: 
    mIoU = []
    for person in tobii_segmentation: 
      temp = aoi_to_segmentation.calculate_iou(tobii_segmentation[person], model_segmentation[model_name], true_pos_only=False) 
      mIoU.append(temp)
    #
    ave = np.mean ( np.array(mIoU) ) 
    std = np.std (np.array(mIoU))
    mIoU.append([ave,std])

  # save as csv 
  fout = open(args.output_csv,'w')
  fout.write ( ','.join ( [f'{item:03d}' for item in mIoU] ) ) 

  