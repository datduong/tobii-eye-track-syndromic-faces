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
from matplotlib import cm


# ---------------------------------------------------------------------------- #

# ! cannot use original images in paper, we have to redo these for Down and 22q, cannot use KS 

output_dir = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/ProcessStepExample'

os.makedirs(output_dir,exist_ok=True)


image_array = [ 
                # 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rNonExpertNoAveByAcc04172023/SimpleAverageBeforeRemoveCommonSignal.png',
                # 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/SimpleAverageBeforeRemoveCommonSignal.png',
                'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertKeepAveByAcc04172023/k0-thresh0.0-diff/k0-thresh0.0-diff_img_aveSlide14Group1.png',
                'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/k0-thresh0.0-diff/k0-thresh0.0-diff_img_aveSlide14Group1.png',
                'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff/k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff_img_aveSlide14Group1.png'
              ]


for index,this_img in enumerate(image_array): 

  # arr = np.array(Image.open(this_img),dtype=float)
  # arr=np.array(np.round(arr),dtype=np.uint8)

  # arr = cm.magma(arr)
  # out = Image.fromarray(np.uint8(arr*255)).convert("RGB")

  # foutname = this_img.split('.png')[0] + 'Magma.png'
  # out.save( os.path.join(foutname ) )

  # ! if we read in black background, then convert it back into white
  arr = np.array(Image.open(this_img).convert("L"),dtype=float)
  arr=np.array(arr)

  arr = cm.magma((255-arr)/255)
  out = Image.fromarray(np.uint8(arr*255)).convert("RGB")

  foutname = this_img.split('.png')[0] + 'Magma.png'
  foutname = 'step'+str(index) + '_' + foutname.split('/')[-1]
  out.save( os.path.join(output_dir, foutname ) )


