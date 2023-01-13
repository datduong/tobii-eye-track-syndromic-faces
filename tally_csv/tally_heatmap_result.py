import os,sys,re,pickle
import numpy as np
import pandas as pd 


# ! combine all heatmap result
# ! filter rows/cols for nice visual

path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/'
slide = ['Slide' + str(i) for i in np.arange(2,18)]
# slide = ['Slide11','Slide10']
all_df_wide = []
all_df_long = []
for s in slide: 
  this_path = os.path.join(path,s)
  csv = [i for i in os.listdir(this_path) if i.endswith('csv')]
  if len(csv)==0:
    print ('empty',s)
    continue
  this_df = [ pd.read_csv(os.path.join(this_path,c) ) for c in csv ] 
  for d in this_df: 
    temp = d['boot_rank'].to_numpy()
    temp = np.where(temp > .5, 1-temp, temp)
    d['boot_pval'] = list(temp)
  # 
  all_df_long = all_df_long + this_df # add 2 list 
  # ! how to view this? https://stackoverflow.com/questions/22798934/pandas-long-to-wide-reshape-by-two-variables
  this_df = pd.concat (this_df)
  #  values = 'obs_stat,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2'.split(',')
  this_df = pd.pivot(this_df, index=['image_number','group_name1','group_name2'], columns = ['type'], values = 'obs_stat,boot_pval,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2'.split(',')) #Reshape from long to wide
  all_df_wide.append(this_df) # append single item

# 
all_df_wide = pd.concat(all_df_wide)
all_df_wide.to_csv(os.path.join(path,'all_heatmap_vs_heatmap_wide.csv'))

all_df_long = pd.concat(all_df_long)
all_df_long.to_csv(os.path.join(path,'all_heatmap_vs_heatmap_long.csv'),index=None)

