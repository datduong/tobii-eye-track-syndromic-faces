
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

image1 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff_img_aveSlide11Group1.png'
img =  Image.open(os.path.join(image1)).convert('L') 
img_as_np = np.array(img) #/ 255 # make 0/1
# ! remove random noise
img_as_np = np.where(img_as_np>70,img_as_np,0) # ! if value over 70, keep the same, else set 0. 
# ! compute some coverage
# some code
im = Image.fromarray(np.uint8(img_as_np))

# ! face_mask... if needed. 
face_mask = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment/Slide6.PNG'    
img_mask =  Image.open(os.path.join(face_mask)).convert('L') 
img_as_np_mask = np.array(img_mask) 
img_as_np_mask = np.where(img_as_np_mask>0,1,0) 

img_as_np = img_as_np * img_as_np_mask
im = Image.fromarray(np.uint8(img_as_np))

