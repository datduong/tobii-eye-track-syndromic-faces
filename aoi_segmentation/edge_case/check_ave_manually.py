

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

imdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Slide2/Group1'
# total_average_no_totave_25radius_slide_11_group1
outputname = 'PeterSlide2Group1'

imlist = os.listdir(imdir)

# imlist = [i for i in imlist if '_BAD.png' not in i]
# imlist = [i for i in imlist if '_Bad.png' not in i]
# imlist = [i for i in imlist if '_bad.png' not in i]
# imlist = [i for i in imlist if 'rBAD.png' not in i]
# imlist = [i for i in imlist if 'POLR1C' not in i]

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
out.save(os.path.join('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023',outputname+".jpg"))

