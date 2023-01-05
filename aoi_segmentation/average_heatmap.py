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
imlist = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01032023/Prelim/KS_123022/Individual"
os.chdir(imlist)
imlist = os.listdir(imlist)
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

# Generate, save and preview final image
out=Image.fromarray(arr,mode="RGBA")
out.save(os.path.join(outdir,"ManualAverage.png"))
# out.show()
