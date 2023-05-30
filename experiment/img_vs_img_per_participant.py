
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

# ! same participant, but look at their heatmap on affected 
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023
img_dir_group_1=$main_data_dir/FOLDER_1/GROUP1 

# ! same participant, but look at their heatmap on unaffected 
img_dir_group_2=$main_data_dir/FOLDER_2/GROUP2

# ! output
output_dir=$main_data_dir/FOLDER_1/SameParticipantAffUnaff # mean_vs_model.csv
mkdir $output_dir

output_dir=$main_data_dir/FOLDER_1/SameParticipantAffUnaff/GROUP1 # mean_vs_model.csv
mkdir $output_dir

# ! add suffix to output average images? 
name_suffix_1=aff
name_suffix_2=unaff

# ! may as well do this at tons of threshold to see what happens

remove_low_before_scale=10 # ! remove very low noisy signal before scaling up the color intensity

for this_k in 10        
do
  for this_thres in 0 
  do

    # ! @this_k control smoothing parameter to smooth out the dots in the heatmap 
    # ! @this_thres remove pixel values in the indidivual person (0=not doing anything). we may need this if there are super noisy dots in the corners of the image. 

    # ! compare simple average images of 2 groups NIH vs Peter, using simple subtraction
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --simple_diff

    # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes) hence @remove_low_before_scale argument, use using simple subtraction
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --remove_low_before_scale $remove_low_before_scale

    # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use intersection-over-union hence @cut_ave_img_to_binary argument 
    python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

    # ! START REMOVING VERY LOW SIGNAL (HENCE, USE ONLY HIGH SIGNAL TO COMPARE 2 SETS OF PARTICIPANTS). at very high values like 150, only the brightest spots will be kept, everything else will be removed. 
    for cut_pixel_ave_img in 50 70 90 110 130 150  
    do

      # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use using simple subtraction
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --simple_diff --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --remove_low_before_scale $remove_low_before_scale

      # ! compare simple average images of 2 groups, scale up the color intensity to match well between 2 groups (due to low sample sizes), use intersection-over-union hence @cut_ave_img_to_binary argument 
      python3 apply_segmentation.py --cut_seg_to_binary_1 $this_thres --cut_seg_to_binary_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --boot_num 1000 --name_suffix_1 $name_suffix_1 --name_suffix_2 $name_suffix_2 --scale_or_shift_ave_pixel 0.3 --smooth_ave --cut_pixel_ave_img $cut_pixel_ave_img --cut_ave_img_to_binary 0.3 --remove_low_before_scale $remove_low_before_scale

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

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023' # @main_folder is where we save all the output data

#
folder_array = ['HeatmapAffPerParticipant', 'HeatmapUnAffPerParticipant']

# user_array = [  'BAF60a',
#                 'BRD4',
#                 'CREBBP',
#                 'EP300',
#                 'G10',
#                 'G11',
#                 'G17',
#                 'G19',
#                 'G27',
#                 'G29',
#                 'G8',
#                 'GTF2I',
#                 'KMT2',
#                 'LIMK1',
#                 'PDGFRa',
#                 'PTPN11',
#                 'RAD21',
#                 'RIT1',
#                 'SMAD1',
#                 'TBX1',
#                 'TCOF1',
#                 'WHSC1']


user_array = ['G1',
              'G12',
              'G13',
              'G14',
              'G15',
              'G16',
              'G18',
              'G2',
              'G20',
              'G21',
              'G22',
              'G23',
              'G24',
              'G25',
              'G26',
              'G28',
              'G3',
              'G4',
              'G5',
              'G6',
              'G7',
              'G9']


# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for this_user in user_array: # Group1
  #
  if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023',folder_array[0],this_user)):
    continue
  if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023',folder_array[1],this_user)): # ! compare how same participant looks at aff vs unaff. 
    continue
  script = re.sub('THIS_K',str(this_k),script_base)
  script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script) # ! note @THRESHOLD_GROUP_1 is NIH
  script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script) # ! note @THRESHOLD_GROUP_2 is Peter's participants 
  #
  script = re.sub('FOLDER_1',folder_array[0],script)
  script = re.sub('FOLDER_2',folder_array[1],script)
  script = re.sub('GROUP1',this_user,script)
  script = re.sub('GROUP2',this_user,script)
  #
  time.sleep( 1 )
  now = datetime.now() # current date and time
  # ! make a bunch of bash script
  script_name = os.path.join(script_path,'script4'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
  fout = open(script_name,'w')
  fout.write(script)
  fout.close()
  # ! @sbatch is used to submit jobs
  os.system('sbatch --time=00:55:00 --mem=4g --cpus-per-task=4 ' + script_name ) 

      
# end





