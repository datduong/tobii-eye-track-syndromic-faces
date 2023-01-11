#!/bin/bash

# ---------------------------------------------------------------------------- #

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=12g
# sbatch --partition=gpu --time=1-00:00:00 --gres=gpu:v100x:2 --mem=20g --cpus-per-task=20 

# ---------------------------------------------------------------------------- #

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37

module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

code_dir=/data/duongdb/Tobii-AOI-FaceSyndromes/aoi_segmentation
cd $code_dir

# ! 
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01032023
img_dir_group_1=$main_data_dir/Prelim/KS_25rad_01072023/IndividualFirstSecond_OnSlide1 # Second
img_dir_group_2=$main_data_dir/Prelim/KS_25rad_01072023/EfficientNetOcclusion

this_k=20
threshold_group_1=.7 # lower --> more "high" signal (strong focus)
threshold_group_2=.7

# output_dir=$main_data_dir/Prelim/KS_25rad_01072023/ # mean_vs_model.csv

# python3 apply_segmentation.py --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing 

# --threshold_group_1 $threshold_group_1 --threshold_group_2 $threshold_group_2

# if_smoothing

# threshold

# k

img_dir_group_2=$main_data_dir/Prelim/KS_25rad_01072023/IndividualThird_OnSlide1

output_dir=$main_data_dir/Prelim/KS_25rad_01072023/OnSlide1 # mean_vs_model.csv
mkdir $output_dir

python3 apply_segmentation.py --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing --boot_num 100 

# --threshold_group_1 $threshold_group_1 --threshold_group_2 $threshold_group_2

python3 apply_segmentation.py --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing --boot_num 100 --threshold_group_1 $threshold_group_1 --threshold_group_2 $threshold_group_2

