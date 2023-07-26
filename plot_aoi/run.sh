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

code_dir=/data/duongdb/tobii-eye-track-syndromic-faces/plot_aoi
cd $code_dir

# ! 
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023/AOI-default03232023

tobii_metrics="Total_duration_of_whole_fixations,Time_to_first_whole_fixation,Number_of_whole_fixations,Duration_of_first_whole_fixation,Number_of_Visits"

# slides="Slide 2,Slide 11"
# group1="BAF60a,BRD4,CREBBP,EP300,KMT2,LIMK1,PDGFRa,POLR1C,SMAD1,TCOF1,WHSC1,PTPN11,RIT1,TBX"
# group2="BAF60a,BRD4,CREBBP,EP300,KMT2,LIMK1,PDGFRa,POLR1C,SMAD1,TCOF1,WHSC1,PTPN11,RIT1,TBX"

# slides="Slide 11,Slide11"
# group1="BAF60a,BRD4,CREBBP,EP300,KMT2,LIMK1,PDGFRa,SMAD1,TCOF1,WHSC1"
# group2="Berny,Friederike,Hannah,Manuel,Meghna"

slides="Slide 12,Slide 12"
group1="BAF60a,BRD4,CREBBP,EP300,KMT2,LIMK1,PDGFRa,SMAD1,TCOF1,WHSC1,PTPN11,RIT1,TBX"
group2="Berny,Friederike,Hannah,Manuel,Meghna"

# --nan_to_0 makes sense if we do "total_number_of_fixation"

python3 $code_dir/aoi_compare.py --csv $main_data_dir/Peter20-24+Nih.csv --outname $main_data_dir/aoi_pval_slide_12.csv --boot_num 1000 --tobii_metrics $tobii_metrics --slides "Slide 12,Slide 12" --group1 $group1 --group2 $group2

# slides = ['Slide 11,Slide 11']

# people_names = [  ['BAF60a,BRD4,CREBBP,EP300,KMT2,LIMK1,PDGFRa,SMAD1,TCOF1,WHSC1'], 
#                   ['PTPN11,RIT1,TBX'] ]

['BAF60a', 'BRD4', 'CREBBP', 'EP300', 'GTF2I', 'KMT2', 'LIMK1', 'PDGFRa', 'PTPN11', 'RAD21', 'SMAD1', 'TBX1', 'TCOF1', 'WHSC1']

# {'BAF60a',
#  'BRD4',
#  'Berny',
#  'CREBBP',
#  'EP300',
#  'Friederike',
#  'Hannah',
#  'KMT2',
#  'LIMK1',
#  'Manuel',
#  'Meghna',
#  'PDGFRa',
#  'POLR1C',
#  'PTPN11',
#  'RIT1',
#  'SMAD1',
#  'TBX',
#  'TCOF1',
#  'WHSC1'}

