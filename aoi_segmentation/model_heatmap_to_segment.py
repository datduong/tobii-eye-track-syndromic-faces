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

import aoi_to_segmentation 
from apply_segmentation import scale_shift_ave_pixel_one_image

match_model_heatmap_to_face_seg = {
  '22q11DSSlide150v2_heatmappositiveAverage.png': 'Slide13.PNG', 
  'WHSSlide13_heatmappositiveAverage.png': 'Slide11.PNG', 
  'WSSlide316_heatmappositiveAverage.png': 'Slide23.PNG', 
  'CdLSSlide124_heatmappositiveAverage.png': 'Slide8.PNG', 
  'KSSlide133_heatmappositiveAverage.png': 'Slide10.PNG', 
  'NSSlide7_heatmappositiveAverage.png': 'Slide7.PNG',
  'UnaffectedSlide217_heatmappositiveAverage.png': 'Slide4.PNG',
  'UnaffectedSlide225_heatmappositiveAverage.png': 'Slide1.PNG',
  'UnaffectedSlide234_heatmappositiveAverage.png': 'Slide3.PNG',
  'UnaffectedSlide235_heatmappositiveAverage.png': 'Slide2.PNG',
}

match_face_seg_to_model = {v:k for k,v in match_model_heatmap_to_face_seg.items()}

# ---------------------------------------------------------------------------- #

this_path = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment'

this_img = [i for i in os.listdir(this_path)]
this_img = [i for i in this_img if 'smooth' not in i]
this_img = [i for i in this_img if 'thres' not in i]
this_img = [i for i in this_img if 'mask' not in i]
print (this_img)


for th in [0.1,0.2,0.3,0.4,0.5]: 
  
  for cam_mask in this_img:

    face_mask = os.path.join('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment', match_model_heatmap_to_face_seg[cam_mask.split('/')[-1]])
    
    face_mask = np.array(Image.open(face_mask).convert('L'))
    face_mask = np.where (face_mask==0,0,1)
    
    seg, img = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=th, smoothing=True, k=20, img_dir=this_path, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=True, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None, face_parse_mask=face_mask)

