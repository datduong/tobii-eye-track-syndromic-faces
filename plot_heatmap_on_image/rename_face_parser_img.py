import os,sys,re,pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# from segmentation_mask_overlay import overlay_masks

import shutil

from matplotlib import cm

# ---------------------------------------------------------------------------- #

# ! we need to remap image numbering, during the experiments, we had multiple powerpoint slides 

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

id_to_english = {
  2:'WS', 
  4:'RSTS1', 
  6:'WHS',
  8:'CdLS', 
  9:'Down',
  11:'KS', 
  12:'NS', 
  14:'22q11DS', 
  15:'PWS',
  17:'BWS',
  3: 'Unaff',
  5: 'Unaff',
  7: 'Unaff',
  10: 'Unaff',
  13: 'Unaff',
  16: 'Unaff',
}

# ---------------------------------------------------------------------------- #
outdir_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment/Rename'

os.makedirs(outdir_path,exist_ok=True)


datadir_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment'
file_array = os.listdir (datadir_path)
file_array = [f for f in file_array if f.endswith('.PNG')]

for fin in file_array: 
  source = os.path.join(datadir_path,fin)
  slide_index = re.sub('Slide','',fin)
  slide_index = int (re.sub(r'\.PNG','',slide_index))
  try: 
    disease_name = id_to_english [ match_powerpoint_to_tobii [ slide_index ] ] 
    tobii_slide = 'tobii'+str(match_powerpoint_to_tobii [ slide_index ])
  except: 
    continue
  dst_dir = os.path.join(outdir_path,re.sub('.PNG','-'+tobii_slide+'-'+disease_name+'.PNG',fin))
  shutil.copy(source,dst_dir)

