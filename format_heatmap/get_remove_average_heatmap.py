

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
from argparse import ArgumentParser

# ---------------------------------------------------------------------------- #

# ! take average of all heatmaps (everyone)
# ! remove the average from each heatmap to see "what's not standard"

# ---------------------------------------------------------------------------- #

def string_comma_to_np (this_str): 
  if this_str is None: 
    return None
  return tuple ( [int(s.strip()) for s in this_str.split(',')] ) 

# ---------------------------------------------------------------------------- #

parser = ArgumentParser()

parser.add_argument('--main_datadir', type=str, default='C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023',
                      help='')

parser.add_argument('--imdir', type=str,
                      help='name of input image folder')

parser.add_argument('--outputname', type=str, default=None,
                      help='name of average image output')

parser.add_argument('--where_to_save_formated_individual', type=str,
                      help='name of new image folder')

parser.add_argument('--imsize', type=str, default='720,720', 
                      help='image size input and output') # 

parser.add_argument('--cropsize', type=str, default=None, 
                      help='crop image to center') # left, top, right, bottom --> 600,180,1320,900 

parser.add_argument('--resize_output', type=string_comma_to_np, default=None, 
                      help='resize output') # 720,720

parser.add_argument('--keep_average', action='store_true', default=False, 
                      help='keep average, not remove it') # 720,720

# ---------------------------------------------------------------------------- #
args = parser.parse_args()
  
args.imsize = string_comma_to_np(args.imsize)
args.cropsize = string_comma_to_np(args.cropsize)

imdir = os.path.join(args.main_datadir,args.imdir)
imlist = os.listdir(imdir)
imlist = [i for i in imlist if 'otsu' not in i]
imlist = [i for i in imlist if 'thres' not in i]
imlist = [i for i in imlist if '_BAD.png' not in i]
imlist = [i for i in imlist if '_Bad.png' not in i]
imlist = [i for i in imlist if '_bad.png' not in i]
imlist = [i for i in imlist if 'rBAD.png' not in i]
imlist = [i for i in imlist if 'POLR1C' not in i]
    
N = len(imlist)

print ('total img count', N)

w,h=Image.open(os.path.join(imdir,imlist[0])).size
    
# Create a np array of floats to store the average (assume RGB images)
arr=np.zeros((h,w,4),float)

# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
  imarr=np.array(Image.open(os.path.join(imdir,im)),dtype=float)
  arr=arr+imarr/N

# Round values in array and cast as 8-bit integer
average_image_array = np.array(arr) # ! 4 dimension not 3. 
arr= Image.fromarray (np.array(np.round(arr),dtype=np.uint8))


# ! save the average image. 
if args.outputname is not None: 
  # https://stackoverflow.com/questions/50898034/how-replace-transparent-with-a-color-in-pillow/50898375#50898375
  out = Image.new("RGBA", (args.imsize), "WHITE")  
  out.paste(arr, (0, 0), arr)                  
  out = cv2.cvtColor(np.array(out), cv2.COLOR_BGR2GRAY) 
  cv2.imwrite(os.path.join(args.main_datadir,args.outputname), 255-out)


# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

# ! take out average 
outdir = os.path.join(args.main_datadir,args.where_to_save_formated_individual) # save output dir
os.makedirs(outdir,exist_ok=True)

for im in imlist:
  imarr=np.array(Image.open(os.path.join(imdir,im)),dtype=float)

  # ---------------------------------------------------------------------------- #

  if not args.keep_average: 
    imarr = imarr - average_image_array # ! take out average 

  # ---------------------------------------------------------------------------- #
  
  imarr = np.where(imarr<0,0,imarr)
  this_img=Image.fromarray(np.array(imarr,dtype=np.uint8),mode='RGBA')
  
  # ! convert into true black/white
  temp = Image.new("RGBA", (args.imsize), "WHITE")  
  temp.paste(this_img, (0, 0), this_img)                 
  temp = cv2.cvtColor(np.array(temp), cv2.COLOR_BGR2GRAY) 

  temp = Image.fromarray(np.array(temp), mode='L')

  if args.cropsize is not None: 
    temp = temp.crop( args.cropsize )

  if args.resize_output is not None: 
    temp = temp.resize( args.resize_output )
  
  im = re.sub(' ', '_',im) # don't want space in name, it's annoying 
  temp.save(os.path.join(outdir,im))
  # if 'GTF2I' in im: 
  #   print (os.path.join(outdir,im))

  
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

