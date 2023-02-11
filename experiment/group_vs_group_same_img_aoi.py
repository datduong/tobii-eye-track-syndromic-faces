import os,sys,re,pickle,time
from datetime import datetime
import numpy as np
import pandas as pd 


# ---------------------------------------------------------------------------- #
script_base="""#!/bin/bash

# ---------------------------------------------------------------------------- #

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=12g
# sbatch --partition=gpu --time=1-00:00:00 --gres=gpu:v100x:2 --mem=20g --cpus-per-task=20 

# ---------------------------------------------------------------------------- #

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37

module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

code_dir=/data/duongdb/Tobii-AOI-FaceSyndromes/plot_aoi
cd $code_dir

# ! 
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023

tobii_metrics="Total_duration_of_whole_fixations,Time_to_first_whole_fixation,Number_of_whole_fixations,Duration_of_first_whole_fixation"

group1=GROUP1
group2=GROUP2

python3 $code_dir/aoi_compare.py --csv $main_data_dir/AOI-data.csv --outname $main_data_dir/aoi_pval.csv --boot_num 1000 --nan_to_0 --tobii_metrics $tobii_metrics --slides "SLIDEPAIR" --group1 $group1 --group2 $group2


"""

# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023' # @main_folder is where we save all the data

slide_folders = os.listdir(main_folder) # @slide_folders should be "Slide1", "Slide2" ...

slide_folders = [s for s in slide_folders if 'Slide' in s]

# slide_folders = ['Slide2','Slide11'] # , 'Slide3']

# ---------------------------------------------------------------------------- #
os.chdir(main_folder)

for folder in slide_folders: 
  #
  for SUFFIX in ['']: # ,'OnSlide1']: 
    if len(SUFFIX)>0: 
      group_folder = [f for f in os.listdir(folder) if SUFFIX in f]
    else: 
      group_folder = [f for f in os.listdir(folder) if 'OnSlide1' not in f] # kinda dumb... whatever
    #
    #
    group_folder = [g for g in group_folder if 'Result' not in g]
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
        # ! get people id in group. 
        g1_name = [i.split('_')[1] for i in os.listdir(os.path.join(main_folder,folder,g1))]
        g2_name = [i.split('_')[1] for i in os.listdir(os.path.join(main_folder,folder,g2))]
        g1_name = ','.join(g1_name)
        g2_name = ','.join(g2_name)
        #
        script = re.sub('SLIDEPAIR',str(this_k),script_base)
        script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script)
        script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script)
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
        os.system('sbatch --time=00:20:00 --mem=4g --cpus-per-task=4 ' + script_name )
