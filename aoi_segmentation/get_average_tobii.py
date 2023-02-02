

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

# ! take average of all heatmaps (everyone)
# ! remove the average from each heatmap to see "what's not standard"


outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023'

imdir = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-has-mismatch-name-to-csv/"


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
arr=np.array(np.round(arr),dtype=np.uint8)
average_image_array = np.array(arr) # ! 4 dimension not 3. 

out=Image.fromarray(np.array(arr)).convert('L')


out.save(os.path.join(outdir,"total_average_25radius.jpg"))


outdir = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-has-mismatch-name-csv-no-ave/"
# os.makedirs(outdir)

for im in imlist:
  imarr=np.array(Image.open(os.path.join(imdir,im)),dtype=float)
  imarr = imarr - average_image_array
  imarr = np.where(imarr<0,0,imarr)
  out=Image.fromarray(np.array(imarr,dtype=np.uint8),mode='RGBA')
  out.save(os.path.join(outdir,im))

  
# ---------------------------------------------------------------------------- #



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
# imdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-has-mismatch-name-csv-no-ave/'

imdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/all'
imlist = os.listdir(imdir)

# imlist = [i for i in imlist if '_BAD.png' not in i]
# imlist = [i for i in imlist if '_Bad.png' not in i]
# imlist = [i for i in imlist if '_bad.png' not in i]
# imlist = [i for i in imlist if 'rBAD.png' not in i]
# imlist = [i for i in imlist if 'POLR1C' not in i]

# imlist = [i for i in imlist if re.match(r'^5_',i) ]
N = len(imlist)
print ('total img count', N)
z=Image.open(os.path.join(imdir,imlist[0])).size
    
# Create a np array of floats to store the average (assume RGB images)
# arr=np.zeros((h,w,4),float)

arr=np.zeros(z,float)


# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
  imarr=np.array(Image.open(os.path.join(imdir,im)),dtype=float)
  arr=arr+imarr/N

# Round values in array and cast as 8-bit integer
arr=np.array(np.round(arr),dtype=np.uint8)
average_image_array = np.array(arr) # ! 4 dimension not 3. 

out=Image.fromarray(np.array(arr)).convert('L')
# out.save(os.path.join('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023',"total_average_no_totave_25radius_slide_5.jpg"))

out.show()

out = np.array(out)
out = cv2.boxFilter(out, -1, (5, 5))
out = np.array(out)
out = np.where(out>10,0,255)

out = Image.fromarray(out).convert('L')
out.show()

