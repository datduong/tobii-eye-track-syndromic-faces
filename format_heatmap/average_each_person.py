import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys, re
from matplotlib import cm

import shutil

# ---------------------------------------------------------------------------- #

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols
  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h), color=(255, 255, 255))
  # grid_w, grid_h = grid.size
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid

# ---------------------------------------------------------------------------- #

# ! see user behavior, average over all images for same person. 

# ---------------------------------------------------------------------------- #

main_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'

fout_dir = os.path.join(main_dir,'Heatmap25rExpertNoAveByAcc04172023')
imdir = 'Heatmap25rExpertNoAve04172023' 

for choice in ['HeatmapAffPerParticipant','HeatmapUnAffPerParticipant']: 
    
  fout_dir_per_participant = os.path.join(fout_dir,choice)
  os.makedirs (fout_dir_per_participant,exist_ok=True)

  # ---------------------------------------------------------------------------- #

  if 'HeatmapAffPerParticipant' in fout_dir_per_participant: 
    outputname = "affected_ave_over_image_same_participant.png"
  else: 
    outputname = "unaffected_ave_over_image_same_participant.png"

  # ---------------------------------------------------------------------------- #

  # ! filter by image type? 
  slide_array = '2,4,6,8,9,11,12,14,15,17'.split(',')

  # ---------------------------------------------------------------------------- #

  img_arr = os.listdir(os.path.join(main_dir,imdir))

  img_arr = [i for i in img_arr if not re.match('^1_',i)]

  if slide_array is not None: 
    if 'HeatmapAffPerParticipant' in fout_dir_per_participant: 
      img_arr = [i for i in img_arr if any (re.match('^'+s+'_',i) for s in slide_array ) ] # ! 
    else: 
      img_arr = [i for i in img_arr if not any (re.match('^'+s+'_',i) for s in slide_array ) ] 
    # check 
    temp = set ( [i.split('_')[0] for i in img_arr] )
    print (temp)
    print (len(temp))
    
                      
  user_name_arr = [i.split('_')[1] for i in img_arr] 
  user_name_arr = [i.split('-')[0] for i in user_name_arr] 
  user_name_arr = sorted ( list ( set (user_name_arr) ) )

  len(user_name_arr)

  all_img_as_pil = []
  for user in user_name_arr: 

    these_img = [i for i in img_arr if re.findall('_'+user+'_',i) ]

    #
    folder_this_participant = os.path.join( fout_dir_per_participant, user)
    os.makedirs(folder_this_participant,exist_ok=True)

    # 
    for im in these_img: 
      shutil.copy2(os.path.join(main_dir,imdir,im), folder_this_participant) 
    
    these_img = [np.array(Image.open(os.path.join(main_dir,imdir,im)).convert('L'),dtype=float) for im in these_img]
    print (user, len(these_img))
    these_img = np.mean(these_img, axis=0)
    # these_img = 255 - these_img # flip, so white is main focus, later apply color map ?
    these_img = 255 * cm.magma(these_img/255) 
    these_img = Image.fromarray( np.uint8 (np.array(these_img)) ) #  , mode='L'
    all_img_as_pil.append(these_img)

  # ---------------------------------------------------------------------------- #

  user_name_arr
  grid = image_grid(all_img_as_pil, rows=5, cols=5) # row=3 or 5? 
  grid.save(os.path.join(fout_dir,outputname))

