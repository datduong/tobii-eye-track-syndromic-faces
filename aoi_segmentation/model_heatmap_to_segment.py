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
from apply_segmentation import scale_shift_ave_pixel_one_image

this_path = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment'

this_img = [i for i in os.listdir(this_path)]
this_img = [i for i in this_img if 'smooth' not in i]
this_img = [i for i in this_img if 'thres' not in i]
this_img = [i for i in this_img if 'mask' not in i]
print (this_img)


def save_img (image,outname,mode="L"): 
  if np.max(np.array(image)) <= 1: 
    image = image*255
  #
  out=Image.fromarray(np.array(image,dtype=np.uint8),mode=mode)
  out.save(outname)


# new_arr_no_0 = arr[np.where(arr!=criteria_pixel)] 
# new_arr_no_0 = np.mean(new_arr_no_0)
# arr = np.where( arr!=criteria_pixel, arr*target/new_arr_no_0, criteria_pixel ) # ! scale so new mean without @criteria matches @target
# arr = np.where( arr>maxval, maxval, arr)

criteria_pixel = 255.0/2

target = 51.0

for cam_mask in this_img:

  arr = Image.open(os.path.join(this_path,cam_mask)).convert("L") # high signal --> green color --> black dot
  arr = 255-np.array(arr) # flip so white=high signal 
  new_arr_no_0 = arr[np.where(arr!=0)] 
  

  # img = scale_by_ave_pixel_one_image ( img/255, target=.1, maxval=1,criteria_pixel=0 ) * 255
  new_arr_no_0 = np.mean(new_arr_no_0)

  print (new_arr_no_0)
  print ( 'ratio', target/new_arr_no_0 )
  
  
  # out = Image.fromarray(np.array(img,dtype=np.uint8),mode='L')

  
  # img, seg = aoi_to_segmentation.cam_to_segmentation(img, threshold=0.7, smoothing=True, k=20, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None)

  # save_img (img, os.path.join(this_path,cam_mask.split('/')[-1]+"_mask.png"))


#  'smoothk20-thresh0.8-'

