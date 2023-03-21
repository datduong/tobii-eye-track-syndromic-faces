
# ! average of a few images after remove the "common consensus"


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

# save grid 
def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols

  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size
  
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid


# ! average of a few images after remove the "common consensus"

slidename_arr = [ str(i)+'_' for i in [2,3,11,14,17] ] # ['17_']

imdir_arr = ['C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-fix-mismatch-name-csv-no-ave-whtbg-3sec',
             'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-fix-mismatch-name-csv-no-ave-whtbg'
             ]

out_arr = []

foutname = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radiusAve3vs7s.jpg'

for imdir in imdir_arr : 

  for slidename in slidename_arr: 

    imlist = os.listdir(imdir)
    imlist = [i for i in imlist if re.match(r'^'+slidename, i)]

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
    out_arr.append(out)
    
#

grid = image_grid(out_arr, rows=len(imdir_arr), cols=len(slidename_arr))
grid.save(os.path.join(foutname))


