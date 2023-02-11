
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

# ! 

main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack

img_dir_group_1=$main_data_dir/SLIDE_NUM1/GROUP1 
img_dir_group_2=$main_data_dir/SLIDE_NUM2/GROUP2

output_dir=$main_data_dir/Compare2Images # mean_vs_model.csv
mkdir $output_dir

# ! may as well do this at tons of threshold to see what happens

cut_pixel_per_img=90

for this_k in 10 
do
  for this_thres in 0 
  do

    # 0.4 0.5 0.6 0.7 0.8 0.9
    # 0.2 0.3 0.4 0.5 0.6 0.7 0.8

    # python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff 

    # python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --smooth_ave

    # python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.2

    # python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.2 --smooth_ave 
    
    # for round_to_int in 0.2 0.3 0.4 0.5 0.6 0.7
    # do
    
    #   python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.2 --smooth_ave --round_to_int $round_to_int
      
    # done 

    # 45 90 135 150 170
    
    for cut_pixel_ave_img in 45 90 120 135 150 170 185
    do
    
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --simple_diff --scale_or_shift_ave_pixel 0.2 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img 

      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --scale_or_shift_ave_pixel 0.2 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --round_to_int 0.1

      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --scale_or_shift_ave_pixel 0.2 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --round_to_int 0.05
      
    done 

  done
done 

"""

# ---------------------------------------------------------------------------- #

# threshold=.5, smoothing=True, k=3

this_k = 10 # 20 # ! lower-->rough shape, higher-->more smooth
cut_seg_to_binary_1 = .5 # ! higher-->more white spot. lower-->less white spot
cut_seg_to_binary_2 = .5 

# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack' # @main_folder is where we save all the data

slide_folders = os.listdir(main_folder) # @slide_folders should be "Slide1", "Slide2" ...

# slide_folders = [s for s in slide_folders if ('Slide' in s) and ('CompareGroup' not in s)]

slide_folders = ['Slide2','Slide3','Slide11','Slide14', 'Slide4'] # , 'Slide3']

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for i1, folder1 in enumerate(slide_folders): 
  for i2, folder2 in enumerate(slide_folders): 
    if i1>=i2: 
      continue
    #
    print (folder1,folder2)
    for SUFFIX in ['Group1','Group3']:  # Group1 'Group1','Group2'
      group_folder1 = os.path.join(folder1,SUFFIX)
      group_folder2 = os.path.join(folder2,SUFFIX)
      #
      if (not os.path.exists(group_folder1)) or (not os.path.exists(group_folder2)): 
        continue
      #
      #
      script = re.sub('THIS_K',str(this_k),script_base)
      script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script)
      script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script)
      script = re.sub('SLIDE_NUM1',str(folder1),script)
      script = re.sub('SLIDE_NUM2',str(folder2),script)
      script = re.sub('GROUP1',SUFFIX,script)
      script = re.sub('GROUP2',SUFFIX,script)
      #
      time.sleep( 1.5 )
      now = datetime.now() # current date and time
      script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
      fout = open(script_name,'w')
      fout.write(script)
      fout.close()
      os.system('sbatch --time=00:35:00 --mem=4g --cpus-per-task=4 ' + script_name )

        
#


