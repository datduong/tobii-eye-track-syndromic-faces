
import os,sys,re,pickle, time
from datetime import datetime
import numpy as np 

# ! make script to compare 2 groups on the same image. 
# ! may have 1 to 3 groups 

script_base = """#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37

module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

code_dir=/data/duongdb/Tobii-AOI-FaceSyndromes/aoi_segmentation
cd $code_dir

# ! NIH data
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack
img_dir_group_1=$main_data_dir/SLIDE_NUM/GROUP1 

# ! Peter data
main_data_dir_2=/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter
img_dir_group_2=$main_data_dir_2/SLIDE_NUM/GROUP2

# ! output
output_dir=$main_data_dir/CompareGroupSameImgVsPeter # mean_vs_model.csv
mkdir $output_dir

output_dir=$main_data_dir/CompareGroupSameImgVsPeter/SLIDE_NUM # mean_vs_model.csv
mkdir $output_dir


# ! may as well do this at tons of threshold to see what happens

remove_low_before_scale=10 # ! remove very low noisy signal before scaling up the color intensity

for this_k in 10        
do
  for this_thres in 0 
  do

    # ! @this_k control smoothing parameter to smooth out the dots in the heatmap 
    # ! @this_thres remove pixel values in the indidivual person (0=not doing anything). we may need this if there are super noisy dots in the corners of the image. 

    # ! compare simple average images of 2 groups NIH vs Peter, using simple subtraction
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 nih --name_suffix_2 peter --simple_diff

    # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes) hence @remove_low_before_scale argument, use using simple subtraction
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 nih --name_suffix_2 peter --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --remove_low_before_scale $remove_low_before_scale

    # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use intersection-over-union hence @cut_ave_img_to_binary argument 
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 nih --name_suffix_2 peter --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

    # ! START REMOVING VERY LOW SIGNAL (HENCE, USE ONLY HIGH SIGNAL TO COMPARE 2 SETS OF PARTICIPANTS). at very high values like 150, only the brightest spots will be kept, everything else will be removed. 
    for cut_pixel_ave_img in 50 70 90 110 130 150  
    do

      # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use using simple subtraction
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 nih --name_suffix_2 peter --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --remove_low_before_scale $remove_low_before_scale

      # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use intersection-over-union hence @cut_ave_img_to_binary argument 
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 nih --name_suffix_2 peter --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

    done 
    
  done
done 


"""

# ---------------------------------------------------------------------------- #

this_k = 10 # 20 # ! lower-->rough shape, higher-->more smooth
cut_seg_to_binary_1 = .5 # ! higher-->more white spot. lower-->less white spot
cut_seg_to_binary_2 = .5 

# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack' # @main_folder is where we save all the output data

# 
slide_folders = ['Slide'+str(s) for s in np.arange(1,18)]

# slide_folders = ['Slide2', 'Slide11', 'Slide6']

# slide_folders = ['Slide1']

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for folder in slide_folders:
  for group in ['Group1']: 
    # @group: 
    # Group1 = NIH vs Peter, participant who answer "correct affected vs not" 
    # Group2 = NIH vs Peter, participant who answer "incorrect affected vs not" 
    # Group3 = NIH vs Peter, participant who answer "correct affected vs not" AND say correct disease name  
    # Group2 = NIH vs Peter, participant who answer "correct affected vs not" BUT say wrong disease name 
    if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack',folder,group)):
      continue
    if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter',folder,group)):
      continue
    script = re.sub('THIS_K',str(this_k),script_base)
    script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script) # ! note @THRESHOLD_GROUP_1 is NIH
    script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script) # ! note @THRESHOLD_GROUP_2 is Peter's participants 
    script = re.sub('SLIDE_NUM',str(folder),script)
    script = re.sub('GROUP1',group,script)
    script = re.sub('GROUP2',group,script)
    #
    time.sleep( 1.5 )
    now = datetime.now() # current date and time
    # ! make a bunch of bash script
    script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
    fout = open(script_name,'w')
    fout.write(script)
    fout.close()
    # ! @sbatch is used to submit jobs
    os.system('sbatch --time=00:35:00 --mem=4g --cpus-per-task=4 ' + script_name ) 

        
# end





