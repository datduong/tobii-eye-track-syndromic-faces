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
imlist = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide2/Group1"
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

# ---------------------------------------------------------------------------- #

mask = Image.open(im)
new_image = Image.new("RGBA", (mask.size), "WHITE") # Create a white rgba background
new_image.paste(mask, (0, 0), mask)              # Paste the image on the background. Go to the links given below for details.
mask = np.array(new_image)

imarr = cv2.cvtColor(np.array(mask), cv2.COLOR_BGR2GRAY)
cv2.imshow('image',imarr)
cv2.waitKey(0)

imarr = np.array(imarr)
imarr = np.where (imarr>70, 255, imarr)
imarr=Image.fromarray(imarr,mode='L')
imarr.show()

# ---------------------------------------------------------------------------- #
imarr=Image.open(im).convert('L') 
imarr.show()
imarr = np.array(imarr,dtype=float)
new_arr_no_0 = imarr[np.where(imarr>0)]
np.min(new_arr_no_0)
np.mean(new_arr_no_0)


imarr = np.where (imarr>0,-1*imarr + 255, imarr)
imarr = np.where (imarr>255,255,imarr)

imarr=Image.fromarray(imarr)
imarr.show()


for i in range(4):
  print (np.sum(imarr[:,:,i]) )


new_image = Image.new("RGBA", (imarr.size), "BLACK") # Create a white rgba background
new_image.paste(imarr, (0, 0), imarr)              # Paste the image on the background. Go to the links given below for details.
# imarr.show()
new_image.show()

imarr = cv2.cvtColor(np.array(new_image), cv2.COLOR_BGR2GRAY)
cv2.imshow('image',imarr)
cv2.waitKey(0)



imarr=np.array(Image.open(im),dtype=np.uint8)
imarr = cv2.cvtColor(imarr, cv2.COLOR_BGR2GRAY)
cv2.imshow('image',imarr)
cv2.waitKey(0)

# ---------------------------------------------------------------------------- #


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

# ! different color intensity to otsu 
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

outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5'
imlist = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5/Group1"
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
out=Image.fromarray(np.array(arr)).convert('RGB')
out.save("C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5red.jpg")


########

outdir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5'
imlist = "C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5/Group1"
os.chdir(imlist)
imlist = os.listdir(imlist)
imlist = [i for i in imlist if 'otsu' not in i]
imlist = [i for i in imlist if 'thres' not in i]
N = len(imlist)
print ('total img count', N)

w,h=Image.open(imlist[0]).size
    
# Create a np array of floats to store the average (assume RGB images)
arr=np.zeros((h,w),float)

# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
  mask = Image.open(im)
  temp = Image.new("RGBA", (mask.size), "WHITE") # Create a white rgba background
  temp.paste(mask, (0, 0), mask)              # Paste the image on the background. Go to the links given below for details.
  temp = temp.convert('L')
  mask = np.array(temp)
  arr = arr+mask/N


# Round values in array and cast as 8-bit integer
arr=np.array(np.round(arr),dtype=np.uint8)
out=Image.fromarray(np.array(arr)).convert('L')

out=np.array(out)
out=np.where(out<255,out-20,out)
out=np.where(out>255,255,out)
out=np.array(np.round(out),dtype=np.uint8)
out=Image.fromarray(out,mode='L')

out.save("C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5red2.jpg")

img = np.array(out,dtype=np.uint8)
# img = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
k = 10
img = cv2.boxFilter(img, -1, (k, k))
img = (255 - img)
ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)   
cv2.imwrite("C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide5red2otsu.jpg", thresh1)

# ! make color more dark or light
mask = Image.open(im)
new_image = Image.new("RGBA", (mask.size), "WHITE") # Create a white rgba background
new_image.paste(mask, (0, 0), mask)              # Paste the image on the background. Go to the links given below for details.

mask = np.array(new_image)
img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
k = 20
img = cv2.boxFilter(img, -1, (k, k))
mask = 255 - img
ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)   


