
import os,sys,re,pickle, time
from datetime import datetime
import numpy as np 

# ! make script to compare 2 groups on the same image. 
# ! may have 1 to 3 groups 

script_base = """#!/bin/bash

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

outfolder=$main_data_dir/img_img_aoi_result
mkdir $outfolder

tobii_metrics="Total_duration_of_whole_fixations,Time_to_first_whole_fixation,Number_of_whole_fixations,Duration_of_first_whole_fixation"

group1=GROUP1
group2=GROUP2

python3 $code_dir/aoi_compare.py --csv $main_data_dir/AOI-data-format.csv --outname $outfolder/OUTPUTNAME.csv --boot_num 1000 --nan_to_0 --tobii_metrics $tobii_metrics --slides "SLIDEPAIR" --group1 $group1 --group2 $group2


"""

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023' # @main_folder is where we save all the data

slide_folders = os.listdir(main_folder) # @slide_folders should be "Slide1", "Slide2" ...

slide_folders = [s for s in slide_folders if 'Slide' in s]
slide_folders = [s for s in slide_folders if os.path.isdir(os.path.join(main_folder,s)) ]

# slide_folders = ['Slide2','Slide11'] # , 'Slide3']
# slide_folders_base = ['Slide2']
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
    for SUFFIX in ['Group1']: 
      group_folder1 = os.path.join(folder1,SUFFIX)
      group_folder2 = os.path.join(folder2,SUFFIX)
      g1_name = list (set([i.split('_')[1] for i in os.listdir(os.path.join(main_folder,group_folder1))]))
      g2_name = list (set([i.split('_')[1] for i in os.listdir(os.path.join(main_folder,group_folder2))]))
      g1_name = ','.join(g1_name) # get name like ABC,DEF,HIJ...
      g2_name = ','.join(g2_name)
      #
      script = re.sub('SLIDEPAIR',re.sub('Slide','Slide ',folder1)+','+re.sub('Slide','Slide ',folder2),script_base)
      script = re.sub('GROUP1',g1_name,script)
      script = re.sub('GROUP2',g2_name,script)
      OUTPUTNAME = folder1+folder2+SUFFIX
      script = re.sub('OUTPUTNAME',OUTPUTNAME,script)
      if os.path.exists('/data/duongdb/Face11CondTobiiEyeTrack01112023/img_img_aoi_result/'+OUTPUTNAME+'.csv'):
        continue
      #
      time.sleep( 1.5 )
      now = datetime.now() # current date and time
      script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
      fout = open(script_name,'w')
      fout.write(script)
      fout.close()
      os.system('sbatch --time=00:20:00 --mem=4g --cpus-per-task=2 ' + script_name )
      # exit()
        
#


