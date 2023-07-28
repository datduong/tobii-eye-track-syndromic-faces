

import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys, re

import matplotlib.pyplot as plt


# ! average of a few images after remove the "common consensus"
# imdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-fix-mismatch-name-csv-no-ave/'


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



for group in ['Group1','Group2','Group3','Group4']: 
    
  imdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Slide11/' + group
  imlist = os.listdir(imdir)

  # imlist = [i for i in imlist if re.match(r'^5_',i) ]
  N = len(imlist)
  print ('total img count', N)
  z=np.array(Image.open(os.path.join(imdir,imlist[0])),dtype=float).shape
      
  # Create a np array of floats to store the average (assume RGB images)
  # arr=np.zeros((h,w,4),float)
  arr=np.zeros(z,float)

  # Build up average pixel intensities, casting each image as an array of floats
  for im in imlist:
    imarr=np.array(Image.open(os.path.join(imdir,im)),dtype=float)
    arr=arr+imarr/N

  # Round values in array and cast as 8-bit integer
  arr=np.array(np.round(arr),dtype=np.uint8)

  out=Image.fromarray(np.array(arr)).convert('L')
  out.save(os.path.join('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/CheckColorIntensityScale',"total_average_no_totave_25radius_slide_11_"+group+".jpg"))

  arr = np.array(out) # ! bring back to np.array to scale
  # arr = 255-arr # flip to black?
  arr = scale_shift_ave_pixel_one_image (arr/255,target=.2) * 255 # do scaling in 0/1 then bring back to 255 
  out=Image.fromarray(np.array(arr,dtype=np.uint8)).convert('L')
  out.save(os.path.join('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/CheckColorIntensityScale',"total_average_no_totave_25radius_slide_11_"+group+"scale.jpg"))
