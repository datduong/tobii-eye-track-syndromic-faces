
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

main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023

img_dir_group_1=$main_data_dir/SLIDE_NUM/GROUP1 
img_dir_group_2=$main_data_dir/SLIDE_NUM/GROUP2

this_k=THIS_K
# threshold_group_1=THRESHOLD_GROUP_1 
# threshold_group_2=THRESHOLD_GROUP_2

output_dir=$main_data_dir/SLIDE_NUM # mean_vs_model.csv
mkdir $output_dir

# --if_smoothing

python3 apply_segmentation.py --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --boot_num 100 

# --boot_ave_segmentation
# --scale_pixel 

# ! may as well do this at tons of threshold to see what happens
# for this_thres in 0.4 0.5 0.6 0.7 
# do

# --if_smoothing

  # python3 apply_segmentation.py --threshold_group_1 $this_thres --threshold_group_2 $this_thres --img_dir_group_1 $img_dir_group_1 --img_dir_group_2 $img_dir_group_2 --output_dir $output_dir --resize 720 --k $this_k --plot_segmentation --boot_num 100 --boot_ave_segmentation --if_smoothing

# --scale_pixel

# done

"""

# ---------------------------------------------------------------------------- #

this_k = 10 # 20 # ! lower-->rough shape, higher-->more smooth
threshold_group_1 = .7 # ! higher-->more white spot. lower-->less white spot
threshold_group_2 = .7 

# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023' # @main_folder is where we save all the data

slide_folders = os.listdir(main_folder) # @slide_folders should be "Slide1", "Slide2" ...

slide_folders = [s for s in slide_folders if 'Slide' in s]

slide_folders = ['Slide2','Slide11'] # , 'Slide3']

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for folder in slide_folders: 
  for SUFFIX in ['','OnSlide1']: 
    if len(SUFFIX)>0: 
      group_folder = [f for f in os.listdir(folder) if SUFFIX in f]
    else: 
      group_folder = [f for f in os.listdir(folder) if 'OnSlide1' not in f] # kinda dumb... whatever
    #
		#
    group_folder = [g for g in group_folder if os.path.isdir(os.path.join(main_folder,folder,g))]
    print (folder, group_folder)
		#
    for i,g1 in enumerate(group_folder):
      for j,g2 in enumerate(group_folder): 
        if j<=i: 
          continue
        print (g1,g2)
        if g1=='Group1' and g2=='Group3': 
          continue
        if g1=='Group1' and g2=='Group4': 
          continue
        # if g1=='Group2' and g2=='Group3': 
        #   continue
        # if g1=='Group2' and g2=='Group4': 
        #   continue
        if g1=='Group1OnSlide1' and g2=='Group3OnSlide1': 
          continue
        if g1=='Group1OnSlide1' and g2=='Group4OnSlide1': 
          continue
        # if g1=='Group2OnSlide1' and g2=='Group3OnSlide1': 
        #   continue
        # if g1=='Group2OnSlide1' and g2=='Group4OnSlide1': 
        #   continue
        #
        script = re.sub('THIS_K',str(this_k),script_base)
        script = re.sub('THRESHOLD_GROUP_1',str(threshold_group_1),script)
        script = re.sub('THRESHOLD_GROUP_2',str(threshold_group_2),script)
        script = re.sub('SLIDE_NUM',str(folder),script)
        script = re.sub('GROUP1',g1,script)
        script = re.sub('GROUP2',g2,script)
				#
        time.sleep( 1.5 )
        now = datetime.now() # current date and time
        script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
        fout = open(script_name,'w')
        fout.write(script)
        fout.close()
        # os.system('sbatch --time=00:20:00 --mem=4g --cpus-per-task=4 ' + script_name )
        exit()
				
#



