import os,sys,re,pickle
import numpy as np
import pandas as pd 


# ! combine all heatmap result
# ! filter rows/cols for nice visual


match_powerpoint_to_tobii = {
  1:3, 
  2:5, 
  3:7, 
  4:10, 
  5:13, 
  6:16, 
  7:12, 
  8:15, 
  9:8, 
  10:11, 
  11:6, 
  12:4, 
  13:14, 
  16:17, 
  17:9, 
  23:2
}

match_tobii_to_powerpoint = { v:k for k,v in match_powerpoint_to_tobii.items() }

id_to_english = {
  1:'TCS',
  2:'WS', 
  4:'RSTS1', 
  6:'WHS',
  8:'CdLS', 
  9:'Down',
  11:'KS', 
  12:'NS', 
  14:'22q11DS', 
  15:'PWS',
  17:'BWS',
  3: 'Unaff3',
  5: 'Unaff5',
  7: 'Unaff7',
  10: 'Unaff10',
  13: 'Unaff13',
  16: 'Unaff16',
}


path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023'

slide = ['Slide' + str(i) for i in np.arange(2,18)]
# slide = ['Slide2','Slide11','Slide14','Slide12','Slide8']

all_df_long = []

for s in slide: 
  #
  this_path = os.path.join(path,'CompareGroupSameImg'+s)
  if not os.path.exists(this_path): 
    continue
  #
  csv = [i for i in os.listdir(this_path) if i.endswith('csv')]
  if len(csv)==0:
    print ('empty',s)
    continue
  #
  this_df = [ pd.read_csv(os.path.join(this_path,c) ) for c in csv ] 
  this_df = pd.concat(this_df)
  temp = this_df['boot_rank'].to_numpy()
  temp = np.where(temp > .5, 1-temp, temp)
  this_df['boot_pval'] = list(temp)
  #
  # this_df = this_df[this_df['type']==criteria]
  # ! how to view this? https://stackoverflow.com/questions/22798934/pandas-long-to-wide-reshape-by-two-variables
  # ! filter some other stuffs? this will make viewing easier ?
  # this_df = this_df[ this_df['group_size1'] > 1] # ! PROBABLY SHOULD NOT USE PARTITION WITH JUST 1 PERSON. 
  # this_df = this_df[ this_df['group_size2'] > 1]
  # ! long format
  all_df_long.append(this_df) # add 2 list 
  
# 

all_df_long = pd.concat(all_df_long)

# format to be plotted in R
slide_num = [i.split('+')[0] for i in all_df_long['image_number'].values]
slide_disease = [ id_to_english[int(re.sub('Slide','',i))] for i in slide_num ]
all_df_long['condition'] = slide_disease

pair1 = [i.split('Group')[-1] for i in all_df_long['group_name1'].values]
pair2 = [i.split('Group')[-1] for i in all_df_long['group_name2'].values]
pair = [str(i)+','+str(j) for i,j in zip(pair1,pair2)]
all_df_long['group'] = pair

all_df_long.to_csv(os.path.join(path,'all_img_nonexpgroup_heatmap_vs_heatmap_long.csv'),index=None)

all_df_long
