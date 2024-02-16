import os,sys,re,pickle
import numpy as np
import shutil

# put all expert into same folder? 
peter_clinician_id_number = [8,10,11,19,17,27,29]
# G8
# G10
# G11
# G17
# G19
# G27
# G29


peter_clinician_id_number = ['_G'+str(p)+'_25r' for p in peter_clinician_id_number]

main_dir = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH'
source_folder = os.path.join(main_dir,'Peter25RadiusTobiiHeatmap04172023_fix_name')
destination_folder = os.path.join(main_dir,'Heatmap25rNonExpert04172023')

expert_images = [i for i in os.listdir(source_folder) if not any (j in i for j in peter_clinician_id_number)] # use "not any" if move non-expert

for p in expert_images: 
  src = os.path.join(source_folder, p)
  dst = os.path.join(destination_folder, p)
  shutil.copy2(src, dst)

  