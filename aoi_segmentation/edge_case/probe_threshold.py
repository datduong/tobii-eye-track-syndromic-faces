
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

this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Slide14/Group1'

this_img = [i for i in os.listdir(this_path)]
this_img = [i for i in this_img if 'smooth' not in i]
this_img = [i for i in this_img if 'thres' not in i]
print (this_img)

for cam_mask in this_img:
  img, seg = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=.5, smoothing=True, k=3, img_dir=this_path, prefix=None, transparent_to_white=True, plot_grayscale_map=False, plot_segmentation=True, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None)


#

# looks okay
# img, seg = aoi_to_segmentation.cam_to_segmentation(cam_mask, threshold=.5, smoothing=True, k=3, img_dir=this_path, prefix=None, transparent_to_white=True, plot_grayscale_map=False, plot_segmentation=True, plot_default_otsu=False, resize=(720,720), cut_off_pixel=None)

