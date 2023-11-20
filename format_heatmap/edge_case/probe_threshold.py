
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

import eye_heatmap_to_segmentation 
from apply_segmentation import scale_shift_ave_pixel_one_image

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols
  w, h = imgs[0].size
  grid = Image.new('L', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size
  for i, img in enumerate(imgs):
    grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid


# ---------------------------------------------------------------------------- #

# SLIDE = 'Slide4'
# this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/'+SLIDE+'/Group1'
# outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023//RemoveAveEyeTrack/'+SLIDE+'/probe'

# name_add = this_path.split('/')[-1]

this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-no-ave-whtbg-peter'
outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/probe_threshold_our'
name_add = 'all'

# ---------------------------------------------------------------------------- #

os.makedirs(outdir,exist_ok=True)

imlist = [i for i in os.listdir(this_path)]
imlist = [i for i in imlist if 'otsu' not in i]
imlist = [i for i in imlist if 'thres' not in i]
imlist = [i for i in imlist if '_BAD.png' not in i]
imlist = [i for i in imlist if '_Bad.png' not in i]
imlist = [i for i in imlist if '_bad.png' not in i]
imlist = [i for i in imlist if 'rBAD.png' not in i]
imlist = [i for i in imlist if 'POLR1C' not in i]

# print (this_img)

SINGLE_SEG_THRESHOLD = 0
SINGLE_IMG_THRESHOLD = 0 # int(.5*255)
try_these = [0.4,0.5,0.6,0.7,0.8]

img_arr = []
seg_arr = []
img_ave_pixel = []

for img_input in imlist:
  segment, img = eye_heatmap_to_segmentation.img_to_segment(img_input, threshold=SINGLE_SEG_THRESHOLD, smoothing=False, k=10, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_pixel_per_img=SINGLE_IMG_THRESHOLD, outdir=outdir)
  img_arr.append ( img )
  seg_arr.append ( segment )
  img_ave_pixel.append ( np.mean(img[img>0]) ) 

#

# take average 

ave_img = np.mean (img_arr,axis=0)
print ('ave pix', np.mean(img_ave_pixel)) # ave pix 94.02328958247313 for all images, when use no threshold 
print ('std', np.std(img_ave_pixel)) # ave pix 94.02328958247313 for all images, when use no threshold 
print ('std', np.quantile(img_ave_pixel, [.1,.25,.5,.75,.9])) # ave pix 94.02328958247313 for all images, when use no threshold 

ave_img_show=Image.fromarray(np.array(ave_img,dtype=np.uint8)).convert('L')

seg_arr = np.mean (seg_arr, axis=0)
ave_seg_arr_show=Image.fromarray(np.array(seg_arr*255,dtype=np.uint8)).convert('L') # ! raw segmentation average

# ---------------------------------------------------------------------------- #

# peter data
# ave pix 103.34141253298583
# std 10.67015229954374
# std [ 88.24093877  97.24918663 105.58500716 110.42567875 114.90847804]

thisimg = Image.open('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images/k0-thresh0.0-diff/k0-thresh0.0-diff_img_aveSlide6all.png') 
thisimg = np.array(thisimg)
np.quantile(thisimg[thisimg>0].flatten(),[.1,.25,.5,.75,.9]) 
# array([ 2.,  5.,  8., 20., 38.])

thisimg = Image.open('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/k0-thresh0.0-diff/k0-thresh0.0-diff_img_aveSlide6all.png') 
thisimg = np.array(thisimg)
np.quantile(thisimg[thisimg>0].flatten(),[.1,.25,.5,.75,.9]) 
# array([ 2.,  6., 15., 31., 47.])

# ---------------------------------------------------------------------------- #

# ! take average of many segmentations
# out = scale_shift_ave_pixel_one_image(seg_arr,target=0.5,maxval=1,criteria_pixel=0,flip_01=False,scale=True) 
# brighter = Image.fromarray(np.array(out* 255,dtype=np.uint8)).convert('L')

plot_arr = []
for th in try_these: 
  segment, temp = eye_heatmap_to_segmentation.img_to_segment(seg_arr, threshold=th, smoothing=True, k=10, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_pixel_per_img=None, outdir=outdir)
  out_show=Image.fromarray(np.array(segment* 255,dtype=np.uint8)).convert('L')
  plot_arr.append(out_show)


all_img_as_pil = [ave_img_show, ave_seg_arr_show] + plot_arr
grid = image_grid(all_img_as_pil, rows=1, cols=len(all_img_as_pil))
grid.save(os.path.join(outdir,name_add+"probe_ave_of_seg"+str(SINGLE_IMG_THRESHOLD)+"cut"+str(SINGLE_SEG_THRESHOLD)+".png"))

# ---------------------------------------------------------------------------- #

# ! take segmentation of average
ave_img = scale_shift_ave_pixel_one_image(ave_img/255.0,target=0.2,maxval=1,criteria_pixel=0,flip_01=False,scale=True) * 255
brighter = Image.fromarray(np.array(ave_img,dtype=np.uint8)).convert('L')

plot_arr = []
for th in try_these: 
  segment, temp = eye_heatmap_to_segmentation.img_to_segment(ave_img, threshold=th, smoothing=True, k=10, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_pixel_per_img=None, outdir=outdir)
  out_show=Image.fromarray(np.array(segment* 255,dtype=np.uint8)).convert('L')
  plot_arr.append(out_show)


all_img_as_pil = [ave_img_show,brighter] + plot_arr
grid = image_grid(all_img_as_pil, rows=1, cols=len(all_img_as_pil))
grid.save(os.path.join(outdir,name_add+"probe_seg_of_ave_rawpix"+str(SINGLE_IMG_THRESHOLD)+"cut"+str(SINGLE_SEG_THRESHOLD)+".png"))


