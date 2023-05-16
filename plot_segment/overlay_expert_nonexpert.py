
import os,sys,re,pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from segmentation_mask_overlay import overlay_masks

from matplotlib import cm


# ! overlay tobii segmentation on the original_image 

# ! follow https://github.com/lobantseff/segmentation-mask-overlay

# ---------------------------------------------------------------------------- #

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols
  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h))
  # grid_w, grid_h = grid.size
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid

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

# ! use saliency map ?
# model_choice = 'smoothk20-thresh0.5-'
# model_dir = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment/'
# all_model_mask = os.listdir(model_dir)
# all_model_mask = [i for i in all_model_mask if model_choice in i]

# ---------------------------------------------------------------------------- #

# ! use face parser map to remove eye movement outside of face ?

use_face_seg_removal = False

face_seg_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment'
all_model_face_seg = os.listdir(face_seg_dir)
all_model_face_seg = [i for i in all_model_face_seg if i.endswith('.PNG')]

# ---------------------------------------------------------------------------- #

tobii_num = np.arange(2,18) # tobii_num = [2,3,4,6,11,14] np.arange(2,18)

image_type = 'img_ave'

output_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/MetaAnalysisExpertNoExpert'

os.makedirs(output_dir,exist_ok=True)

TOBII_CHOICE = [
                # 'k0-thresh0.0-diff',
                # 'k0-thresh0.0-cutbfscale10.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-diff',    
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-diff',      
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-diff',     
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-diff', 
                ]


# ---------------------------------------------------------------------------- #

for this_group in ['Group1']: # 'all','Group1', 'Group2', 'Group3', 'Group4'
    
  for tobii_index, this_tobii in enumerate(tobii_num) : # ! for each original_image 
    
    img_dir_set1 = [] # ! can be expert or just nih group
    img_dir_set2 = [] # ! another group of participants 
      
    for tobii_choice in TOBII_CHOICE: 

      # ! get the average heatmaps of each participant set. @tobii_choice select low/medium/high attention in heatmap
      tobii_dir1 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023//Heatmap25rExpertNoAveByAcc04172023/'+tobii_choice
      tobii_dir2 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023//Heatmap25rNonExpertNoAveByAcc04172023/'+tobii_choice

      tobii_heatmap_arr = [i for i in os.listdir(tobii_dir1) if i.endswith('.png')]
      tobii_heatmap_arr = [i for i in tobii_heatmap_arr if tobii_choice in i]
      tobii_heatmap_arr = [i for i in tobii_heatmap_arr if this_group in i]
      tobii_heatmap_arr = [i for i in tobii_heatmap_arr if image_type in i]

      # ---------------------------------------------------------------------------- #

      original_image = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG'
      original_image = Image.open(original_image).convert("RGBA")

      this_tobii_heatmap = [i for i in tobii_heatmap_arr if 'Slide'+str(this_tobii)+this_group in i]
      if len(this_tobii_heatmap) == 0: 
        continue
      this_tobii_heatmap = this_tobii_heatmap[0]

      if not os.path.exists ( os.path.join(tobii_dir2,this_tobii_heatmap) ): # ! compare side by side, need images from both cohorts
        continue

      mask_as_img = [
                    os.path.join(tobii_dir1,this_tobii_heatmap),
                    os.path.join(tobii_dir2,this_tobii_heatmap)
                    ]


      masks = [] # ! @masks is naming convention of https://github.com/lobantseff/segmentation-mask-overlay
      
      for index, this_mask in enumerate(mask_as_img): 
        this_mask = Image.open(this_mask).convert("L")
        this_mask = np.array(this_mask)
        
        if use_face_seg_removal: # ! mask out region not of interest? 
          face_remove = Image.open(os.path.join(face_seg_dir,'Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG')).convert("L")
          face_remove = np.array (face_remove)
          face_remove = np.where (face_remove==0,0,1)
          this_mask = this_mask * face_remove 
         
        # convert mask into an original_image 
        # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-original_image-applying-matplotlib-colormap
        this_mask = cm.magma((255-this_mask)/255)
        this_mask = Image.fromarray(np.uint8(this_mask*255)).convert("RGBA")
        masks.append(this_mask)
        

      for i,foreground in enumerate(masks) : 
        blend_image = Image.blend (original_image, foreground, alpha=0.3)
        if i == 0: 
          img_dir_set1.append(blend_image)
        if i ==1: 
          img_dir_set2.append(blend_image)

    #
    all_img_as_pil = img_dir_set1 + img_dir_set2
    if len(all_img_as_pil)==0: 
      continue
    grid = image_grid(all_img_as_pil, rows=2, cols=len(img_dir_set1))
    grid.save(os.path.join(output_dir,this_group+'_'+str(this_tobii)+"tobii_overlay_short.png"))

