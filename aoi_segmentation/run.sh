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
img_dir_tobii=$main_data_dir/Prelim/KS_123022/IndividualFirst # Second
img_dir_model=$main_data_dir/Prelim/KS_123022/EfficientNetOcclusion

this_k=20
threshold_tobii=.5 # lower --> more "high" signal (strong focus)
threshold_model=.5

# output_dir=$main_data_dir/Prelim/KS_123022/ # mean_vs_model.csv

# python3 apply_segmentation.py --img_dir_tobii $img_dir_tobii --img_dir_model $img_dir_model --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing 

# --threshold_tobii $threshold_tobii --threshold_model $threshold_model

# if_smoothing

# threshold

# k

img_dir_model=$main_data_dir/Prelim/KS_123022/IndividualThird

output_dir=$main_data_dir/Prelim/KS_123022/ # mean_vs_model.csv

# python3 apply_segmentation.py --img_dir_tobii $img_dir_tobii --img_dir_model $img_dir_model --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing --boot_num 100 
# # --threshold_tobii $threshold_tobii --threshold_model $threshold_model

python3 apply_segmentation.py --img_dir_tobii $img_dir_tobii --img_dir_model $img_dir_model --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --if_smoothing --boot_num 100 --threshold_tobii $threshold_tobii --threshold_model $threshold_model

