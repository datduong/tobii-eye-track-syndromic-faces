import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys, re


# ---------------------------------------------------------------------------- #

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols

  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size
  
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid

# ---------------------------------------------------------------------------- #

# ! see user behavior, average over all images for same person. 

# ---------------------------------------------------------------------------- #

main_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'

# ---------------------------------------------------------------------------- #

# imdir = '25radius-fix-mismatch-name-csv-no-ave-whtbg' 
# outputname = "ave_over_image_same_person.png"

imdir = '25radius-no-ave-whtbg-peter'
outputname = "peter_ave_over_image_same_person.png"

# ---------------------------------------------------------------------------- #

img_arr = os.listdir(os.path.join(main_dir,imdir))
                     
user_name_arr = [i.split('_')[1] for i in img_arr] 
user_name_arr = [i.split('-')[0] for i in user_name_arr] 
user_name_arr = sorted ( list ( set (user_name_arr) ) )

len(user_name_arr)

all_img_as_pil = []
for user in user_name_arr: 
  these_img = [i for i in img_arr if ('_'+user) in i]
  these_img = [np.array(Image.open(os.path.join(main_dir,imdir,im)),dtype=float) for im in these_img]
  these_img = np.mean(these_img, axis=0)
  these_img = Image.fromarray( np.uint8 (np.array(these_img)) , mode='L')
  all_img_as_pil.append(these_img)

# ---------------------------------------------------------------------------- #

grid = image_grid(all_img_as_pil, rows=5, cols=5)
grid.save(os.path.join(main_dir,outputname))

