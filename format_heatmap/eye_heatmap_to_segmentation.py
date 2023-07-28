import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys

import matplotlib.pyplot as plt
from matplotlib import cm

# ---------------------------------------------------------------------------- #

# ! follow https://github.com/rajpurkarlab/cheXlocalize

# ---------------------------------------------------------------------------- #

def calculate_iou(pred_mask, gt_mask, true_pos_only=False): 
    # ! follow https://github.com/rajpurkarlab/cheXlocalize
    """
    Calculate IoU score between two segmentation masks.

    Args:
        pred_mask (np.array 720x720): binary segmentation mask (should only use np.array with 0/1 entires)
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
            iou_score = 0 # np.nan
        else:
            iou_score = np.sum(intersection) / (np.sum(union))

    return iou_score


def calculate_simple_diff(pred_mask, gt_mask): # ! doing subtraction between 2 images. 

    if int ( np.max (pred_mask) ) > 1: # not on 0/1 scale, so we divide 255
        pred_mask = pred_mask/255.0
        gt_mask = gt_mask/255.0
        
    union = np.logical_or(pred_mask, gt_mask)

    simple_diff = abs(pred_mask - gt_mask)
    keep_non_zero = simple_diff * union # only count differences where there are signals. 
    
    score = np.sum(keep_non_zero) / np.sum(union)

    return score



def img_to_segment(cam_mask, threshold=None, smoothing=False, k=0, img_dir=None, prefix=None, transparent_to_white=False, plot_grayscale_map=False, plot_segmentation=False, plot_default_otsu=False, resize=None, cut_pixel_per_img=None, hi_threshold=None, face_parse_mask=None, outdir=None, matplotlib_cm=False):
    """
    Threshold a saliency heatmap to binary segmentation mask.
    Args:
        cam_mask (torch.Tensor): heat map in the original image size (H x W).
            Will squeeze the tensor if there are more than two dimensions.
        threshold (np.float64): threshold to use
        smoothing (bool): if true, smooth the pixelated heatmaps using box filtering
        k (int): size of kernel used for box filter smoothing (int); k must be
                 >= 0; if k is > 0, make sure to set if_smoothing to True,
                 otherwise no smoothing would be performed.

    Returns:
        segmentation (np.ndarray): binary segmentation output
    """

    if outdir is None: 
        outdir = img_dir
        
    # ! original code reads in pickle https://github.com/rajpurkarlab/cheXlocalize
    # if (len(cam_mask.size()) > 2):
    #     cam_mask = cam_mask.squeeze()

    # assert len(cam_mask.size()) == 2

    # # normalize heatmap
    # mask = cam_mask - cam_mask.min()
    # mask = mask.div(mask.max()).data
    # mask = mask.cpu().detach().numpy()

    # ! read saliency image, or a numpy
    # ! if input is numpy, then it should be 2D matrix on grayscale 0-255
    if type(cam_mask) == str: 
        if transparent_to_white: 
            mask = Image.open(os.path.join(img_dir,cam_mask)) 
            # https://stackoverflow.com/questions/50898034/how-replace-transparent-with-a-color-in-pillow/50898375#50898375
            temp = Image.new("RGBA", (mask.size), "WHITE")  # Create a white rgba background
            temp.paste(mask, (0, 0), mask)                  # Paste the image on the background. Go to the links given below for details.
            mask = np.array(temp)
            # ! convert grayscale
            # ! @mask will have white background, and black spots for eye tracks
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) # https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
            mask = 255 - mask # flip, white-->eye focus, black-->nothing
        else: 
            # ! NOTE: THERE'S A PROBLEM, DARKEST RED WILL LOOK BLACK. DO NOT USE IF BACKGROUND IS TRANSPARENT
            mask = np.array(Image.open(os.path.join(img_dir,cam_mask)).convert('L')) # red-->white, transparent-->black 
            mask = 255 - mask # flip, white-->eye focus, black-->nothing
            
    # ! read in numpy, so we set mask=cam_mask, set to uint8 for @cv2
    else: 
        mask = cam_mask # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap

    # ---------------------------------------------------------------------------- #

    if resize is not None: 
        mask = cv2.resize(mask, resize, interpolation = cv2.INTER_AREA)

    if face_parse_mask is not None: 
        mask = np.array(mask) * face_parse_mask # ! apply face parser to remove random noise

    if cut_pixel_per_img is not None: 
        if (0 < cut_pixel_per_img) and (cut_pixel_per_img < 1): 
            sys.exit('cut off pix is on raw scale 0-255')
        #
        mask = np.array(mask)
        mask = np.where (mask > cut_pixel_per_img, mask, 0) # keep pixel higher than this threshold.

    if matplotlib_cm: # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
        mask = cm.gray(mask/255) * 255 # ! scale 0=true_black and 1=white, what about in the middle? 

    if smoothing:
        # ! smoothing on original grayscale image. 
        # ! smooth will add in non-zero, so @cut_pixel_per_img is not a true cutoff anymore 
        mask = cv2.boxFilter(mask, -1, (k, k)) 
        
    # ---------------------------------------------------------------------------- #
    
    formated_input_img_as_np = np.copy(np.array(mask)) # ! may need this later for bootstrap, this is the input image after resize and smoothing and a bunch of other stuffs (if used)

    # ---------------------------------------------------------------------------- #
    
    # use Otsu's method to find threshold if no threshold is passed in
    # if (threshold is None) :
        
    #     maxval = 255 # ! grayscale uses 0 to 255
    #     thresh = cv2.threshold(mask, 0, maxval, cv2.THRESH_OTSU)[1] # ! this should not differ from @segmentation_output ?? @thres looks same as @segmentation

    #     if plot_default_otsu: # ! plot
    #         img = Image.fromarray(np.uint8(thresh), 'L')
    #         img.show()

    #     # draw out contours
    #     cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #     polygons = []
    #     for cnt in cnts:
    #         if len(cnt) > 1:
    #             polygons.append([list(pt[0]) for pt in cnt])

    #     # create segmentation based on contour
    #     img_dims = (mask.shape[1], mask.shape[0])
    #     segmentation_output = Image.new("L", img_dims, "#000000") # ! using "Image.new('1', img_dims)" creates a black image. # https://pillow.readthedocs.io/en/stable/reference/Image.html
    #     for polygon in polygons:
    #         coords = [(point[0], point[1]) for point in polygon]
    #         ImageDraw.Draw(segmentation_output).polygon(coords,
    #                                                     outline=255,
    #                                                     fill=255) # ! fill=1 fills in white spots, color image 0=black, 255=white
            
    #     segmentation = np.array(segmentation_output, dtype="int")//255 # mod 255 to bring back to 0/1 scale

    # else:

    segmentation = None
    if threshold is not None: 
        mask = np.array(mask)
        if int(np.max(mask)) > 1: # need to scale down to 0/1 
            mask = mask/255.0 # @mask will have black background, and white spots, see "mask = 255 - mask"
        # ! NOTE: use mask>threshold if white is eye-signal, and use < if black (low value pixel) is eye-signal
        segmentation = np.array(mask > threshold, dtype="int") 

        
    if face_parse_mask is not None: 
        segmentation = segmentation * face_parse_mask # ! apply face parser to remove random noise


    if segmentation is not None: 
        # ! segmentation must be strict 0/1
        assert np.count_nonzero((segmentation!=0) & (segmentation!=1))==0 # https://stackoverflow.com/questions/40595967/fast-way-to-check-if-a-numpy-array-is-binary-contains-only-0-and-1


    if plot_segmentation and (segmentation is not None): # ! plot ? why not
        segmentation_as_png = Image.fromarray(np.uint8(segmentation*255), 'L') 
        prefix = 'k'+str(k) if smoothing else 'nosmooth'
        prefix = prefix + '-' + 'thresh'+str(threshold) if threshold is not None else 'otsu'
        temp = prefix + '-' + cam_mask.split('/')[-1]
        segmentation_as_png.save(os.path.join(outdir,temp))

    return segmentation, formated_input_img_as_np

