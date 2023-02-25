import cv2
import json
import numpy as np
import pandas as pd
import os, re
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys

from argparse import ArgumentParser

import matplotlib.pyplot as plt
from matplotlib import cm

import aoi_to_segmentation 
from apply_segmentation import scale_shift_ave_pixel_one_image

match_model_heatmap_to_face_seg = {
  '22q11DSSlide150v2_heatmappositiveAverage.png': 'Slide13.PNG', 
  'BWSSlide17v2_heatmappositiveAverage.png': 'Slide16.PNG',
  'DownSlide60v2_heatmappositiveAverage.png': 'Slide17.PNG',
  'WHSSlide13v2_heatmappositiveAverage.png': 'Slide11.PNG', 
  'WSSlide316v2_heatmappositiveAverage.png': 'Slide23.PNG', 
  'CdLSSlide124v2_heatmappositiveAverage.png': 'Slide9.PNG', 
  'KSSlide133v2_heatmappositiveAverage.png': 'Slide10.PNG', 
  'NSSlide7v2_heatmappositiveAverage.png': 'Slide7.PNG',
  'PWSSlide44v2_heatmappositiveAverage.png': 'Slide8.PNG',
  'RSTS1Slide57v2_heatmappositiveAverage.png': 'Slide12.PNG',
  # 'UnaffectedSlide217_heatmappositiveAverage.png': 'Slide4.PNG',
  # 'UnaffectedSlide225_heatmappositiveAverage.png': 'Slide1.PNG',
  # 'UnaffectedSlide234_heatmappositiveAverage.png': 'Slide3.PNG',
  # 'UnaffectedSlide235_heatmappositiveAverage.png': 'Slide2.PNG',
}

match_face_seg_to_model = {v:k for k,v in match_model_heatmap_to_face_seg.items()}

match_powerpoint_to_tobii = {
  1:3, 
  2:5, 
  3:7, 
  4:10, 
  5:13, 
  6:16, 
  7:12, 
  8:15, 
  9:8, 
  10:11, 
  11:6, 
  12:4, 
  13:14, 
  16:17, 
  17:9, 
  23:2
}

match_tobii_to_powerpoint = { v:k for k,v in match_powerpoint_to_tobii.items() }


# ---------------------------------------------------------------------------- #

face_seg_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment'

this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/EfficientNetOccSegment'

this_img = [i for i in os.listdir(this_path)]
this_img = [i for i in this_img if 'smooth' not in i]
this_img = [i for i in this_img if 'thres' not in i]
this_img = [i for i in this_img if 'mask' not in i]
print (this_img)

# ---------------------------------------------------------------------------- #

original_image_dir = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/'


# ---------------------------------------------------------------------------- #

for th in [.1, .15, 0.2,0.3,0.35, 0.4]: # 0.1,0.2,0.3,0.4,0.5
  
  for cam_mask in this_img:

    face_mask = os.path.join(face_seg_dir, match_model_heatmap_to_face_seg[cam_mask.split('/')[-1]])
    
    face_mask = np.array(Image.open(face_mask).convert('L'))
    face_mask = np.where (face_mask==0,0,1) # ! remove background, keep everything else. 
    
    seg, img = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=th, smoothing=True, k=20, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=True, plot_default_otsu=False, resize=(720,720), cut_pixel_per_img=None, face_parse_mask=face_mask)

# ---------------------------------------------------------------------------- #

for cut_pixel_per_img in [10, 50,25,75]: 
    
  for cam_mask in this_img:

    face_mask = os.path.join(face_seg_dir, match_model_heatmap_to_face_seg[cam_mask.split('/')[-1]])
    
    face_mask = np.array(Image.open(face_mask).convert('L'))
    face_mask = np.where (face_mask==0,0,1) # ! remove background, keep everything else. 
    
    seg, img = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=0, smoothing=True, k=20, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=(720,720), cut_pixel_per_img=cut_pixel_per_img, face_parse_mask=face_mask)

    img = Image.fromarray(np.uint8(img), 'L') 
    prefix = 'k20-thresh0-pixcut'+str(cut_pixel_per_img)
    temp = prefix + '-' + cam_mask.split('/')[-1]
    img.save(os.path.join(this_path,temp))

    # overlay 
    if cut_pixel_per_img == 10: 
      original_image = os.path.join(original_image_dir, match_model_heatmap_to_face_seg[cam_mask.split('/')[-1]])
      image = os.path.join(this_path,original_image)
      image = Image.open(image).convert("RGBA")
      this_mask = np.array(img)
      # ! scale pixel value up down? 
      
      this_mask = cm.magma((255-this_mask)/255)
      this_mask = Image.fromarray(np.uint8(this_mask*255)).convert("RGBA")
      blend_image = Image.blend (image, this_mask, alpha=0.5)
      temp = 'overlay-' + prefix + '-' + cam_mask.split('/')[-1]
      blend_image.save(os.path.join(this_path,temp))


