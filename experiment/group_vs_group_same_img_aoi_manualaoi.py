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
main_data_dir=/data/duongdb/Face11CondTobiiEyeTrack01112023/AOI-default03232023

# Number_of_Visits Total_duration_of_whole_fixations

tobii_metrics="Total_duration_of_fixations,Number_of_whole_fixations,Time_to_first_whole_fixation,Duration_of_first_whole_fixation,Number_of_Glances,Time_to_first_Glance,Duration_of_first_Glance,Number_of_Visits,Time_to_first_Visit,Duration_of_first_Visit,Total_duration_of_Visit,Minimum_duration_of_Visit,Maximum_duration_of_Visit,Number_of_saccades_in_AOI"

group1=GROUP1
group2=GROUP2

# ---------------------------------------------------------------------------- #

# --nan_to_0 
# --zero_to_nan 

# ---------------------------------------------------------------------------- #


output_dir=$main_data_dir/CompareWithinNihManualAoi
mkdir $output_dir

output_dir=$output_dir/SLIDENUM
mkdir $output_dir

# Peter+Nih04072023PeterClinic.csv
# Peter+Nih04072023.csv
# Peter+Nih04072023NihClinic.csv  
 
for csv_input in NihMetricsManualUniqueDysmorphicAOIs.csv             
do 

python3 $code_dir/aoi_compare.py --csv $main_data_dir/$csv_input --outname $output_dir'/aoi_THISGROUP_SLIDENUM_'$csv_input --boot_num 500 --tobii_metrics $tobii_metrics --slides "SLIDEPAIR" --group1 $group1 --group2 $group2 --test_statistic mean --aoi_to_use AOI_TO_USE

# python3 $code_dir/aoi_compare.py --csv $main_data_dir/$csv_input --outname $output_dir'/aoi_THISGROUP_SLIDENUM_'$csv_input --boot_num 500 --tobii_metrics $tobii_metrics --slides "SLIDEPAIR" --group1 $group1 --group2 $group2 --test_statistic mean --col_zero_to_nan Total_duration_of_whole_fixations


done



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

dir_set_1 = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023' 
dir_set_2 = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023' 

# slide_folders = ['Slide'+str(s) for s in np.arange(2,18)]

slide_folders = ['Slide2','Slide11'] # ['Slide2','Slide11','Slide12','Slide6'] # , 'Slide3'] ,'Slide11','Slide12','Slide6'

AOI_to_use = {  'Slide 11': '11_D1,11_D2,11_D3,11_D4,11_D5,11_D6,11_D7', 
                'Slide 2': '2_D1,2_D2,2_D3'}

# ---------------------------------------------------------------------------- #
# ! don't need to worry about physicians vs not. the input csv will already be divided into groups. 
# german_physicians = ['G8', 'G10', 'G11', 'G17', 'G19' ] 

# ---------------------------------------------------------------------------- #

os.chdir(script_path)

for slide_i in slide_folders: # go over each slide
  for group1 in ['Group1']: 
    for group2 in ['Group2']: # use group 1, 2, 3, 4 or "all" between nih vs peter ,'Group1'
      set1 = [get_user_from_image_name(s) for s in os.listdir(os.path.join(dir_set_1,slide_i,group1))]
      set2 = [get_user_from_image_name(s) for s in os.listdir(os.path.join(dir_set_2,slide_i,group2))]
      # 
      set1 = ','.join(set1)
      set2 = ','.join(set2) 
      #
      script = re.sub('THISGROUP',str(group1+group2),script_base)
      script = re.sub('SLIDENUM',str(slide_i),script)
      this_slide = re.sub('Slide','Slide ',slide_i)
      script = re.sub('SLIDEPAIR',this_slide+','+this_slide,script)
      script = re.sub('GROUP1',set1,script)
      script = re.sub('GROUP2',set2,script)
      script = re.sub('AOI_TO_USE',AOI_to_use[this_slide],script)
      #
      time.sleep( 1 )
      now = datetime.now() # current date and time
      script_name = os.path.join(script_path,'script0'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
      fout = open(script_name,'w')
      fout.write(script)
      fout.close()
      # os.system('sbatch --time=00:30:00 --mem=2g --cpus-per-task=4 ' + script_name )


#
# 
exit() 

