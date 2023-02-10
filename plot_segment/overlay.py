
import os,sys,re,pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from segmentation_mask_overlay import overlay_masks

# ! overlay tobii segmentation on the image 

# ! https://github.com/lobantseff/segmentation-mask-overlay


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
  17:'BWS'
}


model_choice = 'smoothk20-thresh0.5-'
model_dir = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment/'
all_model_mask = os.listdir(model_dir)
all_model_mask = [i for i in all_model_mask if model_choice in i]

# ! mask? cheat a bit? 
face_seg_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/SurveyPicsFacerSegment'
all_model_face_seg = os.listdir(face_seg_dir)
all_model_face_seg = [i for i in all_model_mask if i.endswith('.PNG')]
use_face_seg_removal = True

# slide_folders = ['Slide2','Slide11','Slide14','Slide12','Slide8'
tobii_num = [2,11,14,12,8]
tobii_choice = 'smoothk10-thresh0.1-avepix0.2-round0.3_seg_ave' 
tobii_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/thresh0.1-avepix0.2-round0.3_seg_ave'
all_tobii_mask = os.listdir(tobii_dir)
all_tobii_mask = [i for i in all_tobii_mask if tobii_choice in i]


all_img_as_pil = []

for tobii_index, this_tobii in enumerate(tobii_num) : 

  image = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG'

  disease_english_name = id_to_english[this_tobii]
  output_name = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/'+model_choice+disease_english_name+'_overlay.png'

  image = Image.open(image).convert("L")
  image = np.array(image)

  this_tobii_mask = [i for i in all_tobii_mask if 'Slide'+str(this_tobii)+'G' in i]
  if len(this_tobii_mask) == 0: 
    continue
  #
  this_tobii_mask = this_tobii_mask[0]

  this_model_mask = [i for i in all_model_mask if disease_english_name+'Slide' in i][0]
  
  mask_as_img = [
                os.path.join(model_dir,this_model_mask), 
                os.path.join(tobii_dir,this_tobii_mask)
                ]

  mask_labels = [
                'Model', 
                'Human'
                ]

  masks = []
  for this_mask in mask_as_img: 
    this_mask = Image.open(this_mask).convert("L")
    
    if use_face_seg_removal: 
      face_remove = Image.open(os.path.join(face_seg_dir,'Slide'+str(match_tobii_to_powerpoint[this_tobii])+'.PNG')).convert("L")
      face_remove = np.array (face_remove)
      face_remove = np.where (face_remove==0,0,1)
      this_mask = np.array(this_mask)
      this_mask = this_mask * face_remove 
      
    this_mask = np.array(this_mask,dtype="bool") # should be pure black/white style ??
    masks.append(this_mask)
    
  # [Optional] prepare labels
  # mask_labels = [f"Mask_{i}" for i in range(len(masks))]

  # [Optional] prepare colors
  # https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html
  cmap = plt.cm.tab10(np.arange(6)) # np.arange(len(mask_labels))
  cmap = cmap[[3,2],:]
  # Laminate your image!
  # fig = overlay_masks(image, masks, labels=mask_labels, colors=cmap, mask_alpha=0.5) # matplotlib.figure.Figure
  # Do with that image whatever you want to do.
  # fig.savefig(output_name, bbox_inches="tight", dpi=300)
  
  pil_img = overlay_masks(image, masks, labels=mask_labels, colors=cmap, mask_alpha=0.4, return_pil_image=True) # matplotlib.figure.Figure
  all_img_as_pil.append(pil_img)


#

def image_grid(imgs, rows, cols):
  # assert len(imgs) == rows*cols

  w, h = imgs[0].size
  grid = Image.new('RGB', size=(cols*w, rows*h))
  grid_w, grid_h = grid.size
  
  for i, img in enumerate(imgs):
      grid.paste(img, box=(i%cols*w, i//cols*h))
  return grid
  
grid = image_grid(all_img_as_pil, rows=3, cols=3)
