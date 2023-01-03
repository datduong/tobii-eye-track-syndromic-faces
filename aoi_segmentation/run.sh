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

code_dir=
cd $code_dir

# ! 
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01032023
img_dir_tobii=$main_data_dir/Prelim/KS_123022/IndividualFirstSecond
img_dir_model=$main_data_dir/Prelim/KS_123022/EfficientNetOcclusion
output_csv=$main_data_dir/Prelim/KS_123022

python3 apply_segmentation.py --img_dir_tobii $img_dir_tobii --img_dir_model $img_dir_model --output_csv $output_csv --resize 720 --plot_segmentation

if_smoothing

threshold

k
