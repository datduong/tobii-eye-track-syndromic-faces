import os,sys,re,pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# from segmentation_mask_overlay import overlay_masks

from matplotlib import cm

# ---------------------------------------------------------------------------- #

# ! we need to remap image numbering, during the experiments, we had multiple powerpoint slides 

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


# ! overlap the saliency map with segmented images.
# ! cannot use original images, because of copyright problem? 

face_seg_dir = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/SurveyPicsFacerSegment'
all_model_face_seg = os.listdir(face_seg_dir)
all_model_face_seg = [i for i in all_model_face_seg if i.endswith('.PNG')]

# ---------------------------------------------------------------------------- #

datadir_path = 'C:/Users/duongdb/Downloads/SaveOverlay_NEW/SaveOverlay'

outdir_path = 'C:/Users/duongdb/Downloads/SaveOverlay_NEW/SaveOverlay/OnTopSegmentFace'

os.makedirs(outdir_path,exist_ok=True)

coverage_threshold = 'HIGH'

img_array = os.listdir(datadir_path)
img_array = [img for img in img_array if coverage_threshold+'-' in img]


for img in img_array: 
  
  this_mask = Image.open(os.path.join(datadir_path,img)).convert("L") # ! "mask" = "saliency map", this is just a naming convention
  this_mask = np.array(this_mask)
  this_mask = cm.magma((255-this_mask)/255)
  this_mask = Image.fromarray(np.uint8(this_mask*255)).convert("RGBA")

  # read in the segmented images
  # ! cannot use original images, because of copyright problem? 

  this_face_segment = img.split('-')[-1]
  this_face_segment = match_model_heatmap_to_face_seg[this_face_segment]
  
  original_image = Image.open(os.path.join(face_seg_dir,this_face_segment)).convert("L")
  original_image = np.array(original_image)
  original_image = Image.fromarray(original_image).convert('RGBA')

  # overlay
  blend_image = Image.blend (original_image, this_mask, alpha=0.4)

  # convert face_segment number ordering in powerpoint into the ordering used in Tobii
  img_index_in_tobii = re.sub('Slide','',this_face_segment)
  img_index_in_tobii = match_powerpoint_to_tobii [ int ( re.sub(r'\.PNG','',img_index_in_tobii) ) ] 

  foutname = os.path.join( outdir_path, coverage_threshold + '-' + id_to_english[ img_index_in_tobii ] + '-SaliencyOnSegmentFace.png' )
  blend_image.save(foutname)

  