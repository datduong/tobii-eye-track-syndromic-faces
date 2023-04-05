
import os,sys,pickle,re
import numpy as np 

# ! some images don't have dash, we should add them? 

# img_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Peter25RadiusTobiiHeatmap04042023_original_name'
img_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Peter25RadiusTobiiHeatmap04042023'

os.makedirs(img_dir,exist_ok=True)

img = os.listdir(img_dir)

for i in img:
  if '_G28' in i: 
    continue # ! problem with G28??
  if '_' in i: 
    os.rename(os.path.join(img_dir,i), os.path.join(img_dir,i)) 
    continue
  #
  new_name = re.sub(' ','_',i)
  os.rename(os.path.join(img_dir,i), os.path.join(img_dir,new_name)) 


for i in os.listdir(img_dir) : # check again 
  if '_' not in i: 
    print (i)

    