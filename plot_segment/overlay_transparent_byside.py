
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
# tobii_num = [2,3,4,6,11,14]

image_type = 'img_ave'


output_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareWithPeter'
os.makedirs(output_dir,exist_ok=True)

# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3 
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3  
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3  
# k0-thresh0.0-diff                                                       
# k0-thresh0.0-cutbfscale10.0-diff                                        
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff                    
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave50.0-diff      
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-diff      
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-diff      
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-diff     
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-diff     
# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-diff     

TOBII_CHOICE = ['k0-thresh0.0-diff',
                'k0-thresh0.0-cutbfscale10.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-diff',    
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-diff',      
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-diff',     
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-diff', 
                ]


# ---------------------------------------------------------------------------- #

for this_group in ['all','Group1', 'Group2', 'Group3', 'Group4']: # 'all','Group1', 'Group2', 'Group3', 'Group4'
    
  for tobii_index, this_tobii in enumerate(tobii_num) : # ! for each image 
    
    our_img = []
    peter_img = []
      
    for tobii_choice in TOBII_CHOICE: 
      
      tobii_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/'+tobii_choice
      peter_tobii_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter/Compare2Images/'+tobii_choice

      all_tobii_mask = [i for i in os.listdir(tobii_dir) if i.endswith('.png')]
      all_tobii_mask = [i for i in all_tobii_mask if tobii_choice in i]
      all_tobii_mask = [i for i in all_tobii_mask if this_group in i]
      all_tobii_mask = [i for i in all_tobii_mask if image_type in i]

      # ---------------------------------------------------------------------------- #

      image = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG'
      image = Image.open(image).convert("RGBA")

      this_tobii_mask = [i for i in all_tobii_mask if 'Slide'+str(this_tobii)+this_group in i]
      if len(this_tobii_mask) == 0: 
        continue
      this_tobii_mask = this_tobii_mask[0]

      if not os.path.exists ( os.path.join(peter_tobii_dir,this_tobii_mask) ): # ! compare side by side, need images from both cohorts
        continue

      mask_as_img = [
                    os.path.join(tobii_dir,this_tobii_mask),
                    os.path.join(peter_tobii_dir,this_tobii_mask)
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
        # 
        # convert mask into an image 
        # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
        this_mask = cm.magma(this_mask/255)
        this_mask = Image.fromarray(np.uint8(this_mask*255)).convert("RGBA")
        masks.append(this_mask)
        

      for i,foreground in enumerate(masks) : 
        blend_image = Image.blend (image, foreground, alpha=0.4)
        if i == 0: 
          our_img.append(blend_image)
        if i ==1: 
          peter_img.append(blend_image)


    #
    all_img_as_pil = our_img + peter_img
    if len(all_img_as_pil)==0: 
      continue
    grid = image_grid(all_img_as_pil, rows=2, cols=len(our_img))
    grid.save(os.path.join(output_dir,this_group+'_'+str(this_tobii)+"tobii_overlay.png"))

