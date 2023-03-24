import os,sys,re,pickle,time
from datetime import datetime
import numpy as np
import pandas as pd 


# ---------------------------------------------------------------------------- #
script_base="""#!/bin/bash

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
def get_user_from_image_name (x):
  # @x is image name like G1_something.png
  x = x.split('_')[1].strip()
  if x.endswith('.png'): 
    x = x.split('.')[0]
  return x
   
# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

dir_set_1 = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack' 
dir_set_2 = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrackPeter' 

slide_folders = os.listdir(dir_set_1) # @slide_folders should be "Slide1", "Slide2" ...

# slide_folders = [s for s in slide_folders if 'Slide' in s]

slide_folders = ['Slide2','Slide11'] # , 'Slide3']

# ---------------------------------------------------------------------------- #
# ! do something here later? 
# german_physicians = ['G8', 'G10', 'G11', 'G17', 'G19' ] 

# ---------------------------------------------------------------------------- #

os.chdir(script_path)

for folder in slide_folders: # go over each slide
  for group in ['Group1']: # use group 1, 2, 3, 4 or "all" between nih vs peter 
    set1 = [get_user_from_image_name(s) for s in os.listdir(os.path.join(dir_set_1,group))]
    set2 = [get_user_from_image_name(s) for s in os.listdir(os.path.join(dir_set_2,group))]
    # 
    set1 = ','.join(set1)
    set2 = ','.join(set2)
    #
    script = re.sub('SLIDE_NUM',str(folder),script)
    script = re.sub('GROUP1',set1,script)
    script = re.sub('GROUP2',set2,script)
    #
    time.sleep( 1.5 )
    now = datetime.now() # current date and time
    script_name = os.path.join(script_path,'script'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
    fout = open(script_name,'w')
    fout.write(script)
    fout.close()
    os.system('sbatch --time=00:20:00 --mem=4g --cpus-per-task=4 ' + script_name )

      