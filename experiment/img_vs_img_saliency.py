
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

code_dir=/data/duongdb/tobii-eye-track-syndromic-faces/format_heatmap
cd $code_dir

# ! 

main_data_dir=/data/duongdb/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023

img_dir_group_1=$main_data_dir/SLIDE_NUM1/GROUP1 
img_dir_group_2=$main_data_dir/SLIDE_NUM2/GROUP2

output_dir=$main_data_dir/Compare2Saliency # mean_vs_model.csv
mkdir $output_dir

output_dir=$main_data_dir/Compare2Saliency/SALIENCYCRITERIA
mkdir $output_dir


compare_vs_this=/data/duongdb/TOBII_DATA_PATH/EfficientNetOccSegment/COMPARE_VS_THIS


# ! add suffix to output average images? 
name_suffix_1=human
name_suffix_2=EfnetOcc


# ---------------------------------------------------------------------------- #

remove_low_before_scale=10 # ! remove very low noisy signal before scaling up the color intensity

for this_k in 10 
do
  for this_thres in 0 
  do

    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 100 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale --compare_vs_this $compare_vs_this

    for cut_pixel_ave_img in 70 90 110 130  
    do

      # ! USE SIMPLE DIFFERENCE, SO CHECK @SALIENCYCRITERIA
      # python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 100 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --remove_low_before_scale $remove_low_before_scale --compare_vs_this $compare_vs_this

      # ! USE SIMPLE OVERLAP AREA, SO CHECK @SALIENCYCRITERIA
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 100 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale --compare_vs_this $compare_vs_this

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

script_path = '/data/duongdb/TOBII_DATA_PATH'

main_folder = '/data/duongdb/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023' # @main_folder is where we save all the data

# k20-thresh0.1-pixcut0-seg-KSSlide133v2_heatmappositiveAverage

compare_vs_this = {
  'Slide14': '22q11DSSlide150v2_heatmappositiveAverage.png',
  'Slide17': 'BWSSlide17v2_heatmappositiveAverage.png',
  'Slide9': 'DownSlide60v2_heatmappositiveAverage.png',
  'Slide6': 'WHSSlide13v2_heatmappositiveAverage.png',
  'Slide2' : 'WSSlide316v2_heatmappositiveAverage.png',
  'Slide8' : 'CdLSSlide124v2_heatmappositiveAverage.png',
  'Slide11' : 'KSSlide133v2_heatmappositiveAverage.png',
  'Slide12' : 'NSSlide7v2_heatmappositiveAverage.png',
  'Slide15' : 'PWSSlide44v2_heatmappositiveAverage.png',
  'Slide4' : 'RSTS1Slide57v2_heatmappositiveAverage.png',
}

criteria = 'k20-thresh0.05-pixcut20-seg' # 'k20-thresh0.1-pixcut70' # 'k20-thresh0.1-pixcut70-seg'

for k,v in compare_vs_this.items(): 
  compare_vs_this[k] = criteria+'-'+v
  

# slide_folders = ['Slide2','Slide11'] # , 'Slide3']

slide_folders = list ( compare_vs_this.keys() ) 

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for i1, folder1 in enumerate(slide_folders): 
  print (folder1)
  for SUFFIX in ['Group1']:  # Group1
    group_folder1 = os.path.join(folder1,SUFFIX)
    #
    script = re.sub('THIS_K',str(this_k),script_base)
    script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script)
    script = re.sub('SLIDE_NUM1',str(folder1),script)
    script = re.sub('GROUP1',SUFFIX,script)
    #
    script = re.sub('COMPARE_VS_THIS',compare_vs_this[str(folder1)],script)
    script = re.sub('SALIENCYCRITERIA',criteria,script)
    #
    time.sleep( 1.5 )
    now = datetime.now() # current date and time
    script_name = os.path.join(script_path,'script1'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
    fout = open(script_name,'w')
    fout.write(script)
    fout.close()
    os.system('sbatch --time=00:20:00 --mem=4g --cpus-per-task=4 ' + script_name )

      
#


