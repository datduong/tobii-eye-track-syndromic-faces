import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys

import matplotlib.pyplot as plt

# ! test if average is similar to tobii's default 
outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01032023/Prelim/KS_123022'
imlist = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01032023/Prelim/KS_123022/Individual_all"
os.chdir(imlist)
imlist = os.listdir(imlist)
imlist = [i for i in imlist if 'otsu' not in i]
imlist = [i for i in imlist if 'thres' not in i]
N = len(imlist)
print ('total img count', N)

w,h=Image.open(imlist[0]).size
    
# Create a np array of floats to store the average (assume RGB images)
arr=np.zeros((h,w,4),float)

# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
  imarr=np.array(Image.open(im),dtype=float)
  arr=arr+imarr/N

# Round values in array and cast as 8-bit integer
arr=np.array(np.round(arr),dtype=np.uint8)

# arr=np.array(np.round(arr))

# # Generate, save and preview final image
# out=Image.fromarray(arr,mode="RGBA")
# out.save(os.path.join(outdir,"ManualAverageIndividual_all.png"))
# # out.show()

arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
# cv2.imshow('image',arr)
# cv2.waitKey(0)


def scale_by_ave_pixel_one_image(arr,target=125): 
  new_arr_no_0 = arr[np.where(arr!=0)]
  new_arr_no_0 = np.mean(new_arr_no_0)
  print (new_arr_no_0)
  # mask_black = np.where(arr==0,arr,1)
  arr = arr * target/new_arr_no_0 # scale mean to 125
  # arr = arr * 255/ np.max(arr)
  new_arr_no_0 = arr[np.where(arr!=0)]
  new_arr_no_0 = np.mean(new_arr_no_0)
  print (new_arr_no_0)
  # arr = arr * mask_black
  arr = np.where(arr>255,255,arr)
  return arr

arr = np.array(arr,dtype=float)
print ('ave')
print ('min', np.min(arr))
print ('max', np.max(arr) )
print ('mean', np.mean(arr) )
print ('size', arr.shape )
  
arr=scale_by_ave_pixel_one_image(arr)

print ('after scale')
print ('min', np.min(arr))
print ('max', np.max(arr) )
print ('mean', np.mean(arr) )
print ('size', arr.shape )

arr=np.array(np.round(arr),dtype=np.uint8)
out=Image.fromarray(np.array(arr),mode="L")
out.show()

# ---------------------------------------------------------------------------- #


