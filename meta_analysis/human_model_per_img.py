
import os,sys,re,pickle 

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# ! make csv for meta-analysis in R


def calculate_iou(pred_mask, gt_mask, true_pos_only):
    """
    Calculate IoU score between two segmentation masks.

    Args:
        pred_mask (np.array): binary segmentation mask
        gt_mask (np.array): binary segmentation mask
    Returns:
        iou_score (np.float64)
    """
    intersection = np.logical_and(pred_mask, gt_mask)
    union = np.logical_or(pred_mask, gt_mask)

    if true_pos_only:
        if np.sum(pred_mask) == 0 or np.sum(gt_mask) == 0:
            iou_score = np.nan
        else:
            iou_score = np.sum(intersection) / (np.sum(union))
    else:
        if np.sum(union) == 0: 
            # ! union has no overlapping, so return 0 intead of nan ??
            # ! at extreme threshold, this happens if we put in all black images (so 0 or 0 = 0)
            iou_score = np.nan
        else:
            iou_score = np.sum(intersection) / (np.sum(union))

    return iou_score



select_criteria_1 = ''
select_criteria_2 = ''


mask_dir_1 = ''
mask_dir_2 = ''


mask_set_1 = [os.path.join(mask_dir_1,i) for i in os.listdir(mask_dir_1) if select_criteria_1 in i ]
# print (mask_set_1)

mask_set_2 = [os.path.join(mask_dir_2,i) for i in os.listdir(mask_dir_2) if select_criteria_2 in i ]
# print (mask_set_2)

this_model = np.array(Image.open(mask_set_2[0]).convert("L"))

all_iou = []
for this_human in mask_set_1: 
  this_human = np.array(Image.open(this_human).convert("L"))
  iou = calculate_iou (this_human,this_model)
  all_iou.append(iou)

# 
all_iou = np.array(all_iou)
mean_iou = np.mean(all_iou)
std = np.std(all_iou)



