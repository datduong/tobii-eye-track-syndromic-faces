
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


# ! simple test case, compute iou score 

def read_img_convert_np_array (imgpath): 
  img =  Image.open(os.path.join(imgpath)).convert('L') 
  img_as_np = np.array(img) #/ 255 # make 0/1
  # img_as_np = np.where(img_as_np>0,1,0) 
  return img, img_as_np


# ---------------------------------------------------------------------------- #
# image1 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023/Slide11/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3_seg_aveSlide11Group1exp.png'
# image2 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/EfficientNetOccSegment/k20-thresh0.1-pixcut0-seg-KSSlide133v2_heatmappositiveAverage.png'

image1 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023/Slide11/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3_seg_aveSlide11Group1exp.png'
image2 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/EfficientNetOccSegment/k20-thresh0.1-pixcut70-seg-KSSlide133v2_heatmappositiveAverage.png'

img1, image1 = read_img_convert_np_array(image1)
img2, image2 = read_img_convert_np_array(image2)

iou_score = aoi_to_segmentation.calculate_iou(image1,image2,true_pos_only=False)
print (iou_score)

0.0958543833580

0.08807485733467607
