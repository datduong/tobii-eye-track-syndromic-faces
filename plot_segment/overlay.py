

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from segmentation_mask_overlay import overlay_masks

# ! overlay tobii segmentation on the image 

# ! https://github.com/lobantseff/segmentation-mask-overlay


# [Example] Load image. If you are sure of you masks
image = 'C:/Users/duongdb/Documents/ManyFaceConditions12012022/survey_pics_eyetrack_tobii/Slide7.PNG'
output_name = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/NS_overlay.png'
image = Image.open(image).convert("L")
image = np.array(image)

# [Example] Mimic list of masks
# masks = []
# for i in np.linspace(0, image.shape[1], 10, dtype="int"):
#     mask = np.zeros(image.shape, dtype="bool")
#     mask[i : i + 100, i : i + 200] = 1
#     masks.append(mask)

# C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Diseases/smoothk10-thresh0.5-scaleave-bootseg-round0.5/smoothk10-thresh0.5-scaleave-bootseg-round0.5_seg_aveSlide14Group1.png'
# smoothk10-thresh0.5-scaleave-bootseg-round0.5_seg_raw_aveSlide14Group1
# C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Diseases/smoothk10-thresh0.5-scaleave-bootseg-round0.5/smoothk10-thresh0.5-scaleave-bootseg-round0.5_seg_raw_aveSlide14Group1.png
# smoothk20-thresh0.8-22q11DSSlide150v2_heatmappositiveAverage.png
# smoothk20-thresh0.8-KSSlide133_heatmappositiveAverage.png
# smoothk20-thresh0.8-NSSlide7_heatmappositiveAverage.png

mask_as_img = ['C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Diseases/smoothk10-thresh0.5-scaleave-bootseg-round0.5/smoothk10-thresh0.5-scaleave-bootseg-round0.5_seg_raw_aveSlide12Group1.png',
               'C:/Users/duongdb/Documents/ManyFaceConditions12012022/Classify/b4ns448wlEqualss10lr3e-05dp0.2b64ntest1NormalNotAsUnaff/EfficientNetOccSegment/smoothk20-thresh0.7-NSSlide7_heatmappositiveAverage.png']
mask_labels = ['Human',
               'Model']
masks = []
for this_mask in mask_as_img: 
  this_mask = Image.open(this_mask).convert("L")
  this_mask = np.array(this_mask,dtype="bool") # should be pure black/white style ??
  masks.append(this_mask)
  
# [Optional] prepare labels
# mask_labels = [f"Mask_{i}" for i in range(len(masks))]

# [Optional] prepare colors
# https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html
cmap = plt.cm.Set1(np.arange(len(mask_labels)))

# Laminate your image!
fig = overlay_masks(image, masks, labels=mask_labels, colors=cmap, mask_alpha=0.5)

# Do with that image whatever you want to do.
fig.savefig(output_name, bbox_inches="tight", dpi=300)

fig
