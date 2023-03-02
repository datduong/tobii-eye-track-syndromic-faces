
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

cut_pixel_per_img=20 # ! if use, should be pixel value at 80 (about bottom 10%)

remove_low_before_scale=10

for this_k in 10 
do
  for this_thres in 0 
  do

    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff
    
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --remove_low_before_scale $remove_low_before_scale

    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

    for cut_pixel_ave_img in 50 70 90 110 130 150  
    do
    
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --remove_low_before_scale $remove_low_before_scale

      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

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

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack' # @main_folder is where we save all the data

# 
slide_folders = ['Slide'+str(s) for s in np.arange(1,18)]

# slide_folders = ['Slide2', 'Slide11', 'Slide6']

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for folder in slide_folders:
  for group in ['all']: 
    script = re.sub('THIS_K',str(this_k),script_base)
    script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script)
    script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script)
    script = re.sub('SLIDE_NUM',str(folder),script)
    script = re.sub('GROUP1',group,script)
    script = re.sub('GROUP2',group,script)
    #
    time.sleep( 1.5 )
    now = datetime.now() # current date and time
    script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
    fout = open(script_name,'w')
    fout.write(script)
    fout.close()
    os.system('sbatch --time=00:35:00 --mem=4g --cpus-per-task=4 ' + script_name )
    # exit()
        
  #



