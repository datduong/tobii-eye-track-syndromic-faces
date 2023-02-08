
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

def scale_shift_ave_pixel_one_image(arr,target=0.5,maxval=1,criteria_pixel=0,flip_01=False,scale=True): 
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
  if scale: # ! works a lot better with tobii
    arr = np.where( arr!=criteria_pixel, arr*target/new_arr_no_0, criteria_pixel ) # ! scale so new mean without @criteria matches @target
  else: 
    amount = target - new_arr_no_0 
    arr = np.where( arr!=criteria_pixel, arr+amount, criteria_pixel )
  #
  arr = np.where( arr>maxval, maxval, arr) # bound so nothing goes over 255
  arr = np.where( arr<0, 0, arr) # bound at 0 from below
  if flip_01:
    arr = maxval-arr
  return arr


this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Slide2/Group3'
outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023//RemoveAveEyeTrack/Slide2/probe'

os.makedirs(outdir,exist_ok=True)

this_img = [i for i in os.listdir(this_path)]
this_img = [i for i in this_img if 'smooth' not in i]
this_img = [i for i in this_img if 'thres' not in i]
print (this_img)

ave_img = []
for cam_mask in this_img:
  segment, img = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=0.1, smoothing=True, k=10, img_dir=this_path, prefix=None, transparent_to_white=True, plot_grayscale_map=False, plot_segmentation=True, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None, outdir=outdir)

  ave_img.append ( np.array(img) )
#

# take average 

ave_img = np.mean (ave_img,axis=0)
ave_img_show=Image.fromarray(np.array(ave_img,dtype=np.uint8)).convert('L').resize((720,720))

out = scale_shift_ave_pixel_one_image(ave_img/255,target=0.2,maxval=1,criteria_pixel=0,flip_01=False,scale=True) * 255
out_show=Image.fromarray(np.array(out,dtype=np.uint8)).convert('L').resize((720,720))

segment, img = aoi_to_segmentation.cam_to_segmentation(out, threshold=0.2, smoothing=True, k=10, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None, outdir=outdir)

ave_seg=Image.fromarray(np.array(segment*255,dtype=np.uint8)).convert('L').resize((720,720))
ave_img_new=Image.fromarray(np.array(img,dtype=np.uint8)).convert('L').resize((720,720))

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols

  w, h = imgs[0].size
  grid = Image.new('L', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size

  for i, img in enumerate(imgs):
    grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid


all_img_as_pil = [ave_img_show,out_show, ave_seg, ave_img_new]
grid = image_grid(all_img_as_pil, rows=1, cols=4)
grid.save(os.path.join(outdir,"check_step.png"))

