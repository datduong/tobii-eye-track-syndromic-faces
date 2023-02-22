
import os,sys,re,pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from segmentation_mask_overlay import overlay_masks

from matplotlib import cm


# ! overlay tobii segmentation on the image 

# ! https://github.com/lobantseff/segmentation-mask-overlay

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols

  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size
  
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid

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

model_choice = 'smoothk20-thresh0.5-'
model_dir = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment/'
all_model_mask = os.listdir(model_dir)
all_model_mask = [i for i in all_model_mask if model_choice in i]

# ---------------------------------------------------------------------------- #

# ! mask? cheat a bit? 
face_seg_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment'
all_model_face_seg = os.listdir(face_seg_dir)
all_model_face_seg = [i for i in all_model_mask if i.endswith('.PNG')]
use_face_seg_removal = True

# ---------------------------------------------------------------------------- #

tobii_num = np.arange(2,18)

this_group = 'all'
image_type = 'img_ave'

tobii_choice = 'k0-thresh0.0-cutbfscale10.0-avepix0.2-smoothave-pixcutave70.0-diff'

tobii_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/'+tobii_choice
peter_data_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images/'+tobii_choice

all_tobii_mask = os.listdir(tobii_dir)
all_tobii_mask = [i for i in all_tobii_mask if tobii_choice in i]
all_tobii_mask = [i for i in all_tobii_mask if this_group in i]
all_tobii_mask = [i for i in all_tobii_mask if image_type in i]


# ---------------------------------------------------------------------------- #

for tobii_index, this_tobii in enumerate(tobii_num) : 
  
  all_img_as_pil = []

  image = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG'
  image = Image.open(image).convert("RGBA")

  this_tobii_mask = [i for i in all_tobii_mask if 'Slide'+str(this_tobii)+this_group in i]
  if len(this_tobii_mask) == 0: 
    continue
  #
  this_tobii_mask = this_tobii_mask[0]

  mask_as_img = [
                os.path.join(tobii_dir,this_tobii_mask),
                os.path.join(peter_data_dir,this_tobii_mask)
                ]


  masks = []
  for index, this_mask in enumerate(mask_as_img): 
    this_mask = Image.open(this_mask).convert("L")
    if use_face_seg_removal: # ! mask out region not of interest? 
      face_remove = Image.open(os.path.join(face_seg_dir,'Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG')).convert("L")
      face_remove = np.array (face_remove)
      face_remove = np.where (face_remove==0,0,1)
      this_mask = np.array(this_mask)
      this_mask = this_mask * face_remove 
      
    # this_mask = np.array(this_mask,dtype="bool") # should be pure black/white style ??

    this_mask = cm.magma(this_mask/255)
    this_mask = Image.fromarray(np.uint8(this_mask*255)).convert("RGBA")
    masks.append(this_mask)
    
  # plot 
  cmap = plt.cm.tab10(np.arange(6)) # https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html
  cmap = cmap[[2],:]

  for foreground in masks : 
    blend_image = Image.blend (image, foreground, alpha=0.7)
    all_img_as_pil.append(blend_image)

  #
  grid = image_grid(all_img_as_pil, rows=1, cols=2)
  grid.save(os.path.join(tobii_dir,this_group+str(this_tobii)+"tobii_overlay.png"))

