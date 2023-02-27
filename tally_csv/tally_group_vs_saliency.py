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


path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Saliency/k20-thresh0.1-pixcut70-seg'
foutpath = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Saliency'
criteria_arr = ['k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3', 
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3', 
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3'
                ]

slide = ['Slide' + str(i) for i in np.arange(1,18)]

for criteria in criteria_arr: 
  csv = [i for i in os.listdir(path) if i.endswith('csv')]
  csv = [i for i in csv if criteria in i]
  csv = [ pd.read_csv(os.path.join(path,c) ) for c in csv ] 
  df_long = pd.concat (csv)
  df_long.to_csv(os.path.join(foutpath,'Eb4Occ-'+criteria+'.csv'), index=False)



for s in slide: 
  this_path = os.path.join(path,'saliency-vs-'+s+'')
  if not os.path.exists(this_path): 
    continue
  csv = [i for i in os.listdir(this_path) if i.endswith('csv')]
  if len(csv)==0:
    print ('empty',s)
    continue
  this_df = [ pd.read_csv(os.path.join(this_path,c) ) for c in csv ] 
  this_df = pd.concat(this_df)
  temp = this_df['boot_rank'].to_numpy()
  temp = np.where(temp > .5, 1-temp, temp)
  this_df['boot_pval'] = list(temp)
  # this_df = this_df[this_df['type']==criteria]
  # 
  # ! how to view this? https://stackoverflow.com/questions/22798934/pandas-long-to-wide-reshape-by-two-variables
  # ! filter some other stuffs? this will make viewing easier
  # this_df = this_df[ ~((this_df['group_name1']=='Group1') & (this_df['group_name2']=='Group3')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group1') & (this_df['group_name2']=='Group4')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group2') & (this_df['group_name2']=='Group3')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group2') & (this_df['group_name2']=='Group4')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group1OnSlide1') & (this_df['group_name2']=='Group3OnSlide1')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group1OnSlide1') & (this_df['group_name2']=='Group4OnSlide1')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group2OnSlide1') & (this_df['group_name2']=='Group3OnSlide1')) ]
  # this_df = this_df[ ~((this_df['group_name1']=='Group2OnSlide1') & (this_df['group_name2']=='Group4OnSlide1')) ]
  this_df = this_df[ this_df['group_size1'] > 0]
  this_df = this_df[ this_df['group_size2'] > 0]
  #  values = 'obs_stat,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2'.split(',')
  # ! long format
  all_df_long.append(this_df) # add 2 list 
  # ! wide format
  this_df = pd.pivot(this_df, index=['image_number','group_name1','group_name2'], columns = ['type'], values = 'obs_stat,boot_pval,boot_ave,boot_std,boot_rank,boot_num,group_size1,group_size2'.split(',')) #Reshape from long to wide
  all_df_wide.append(this_df) # append single item


# 
all_df_wide = pd.concat(all_df_wide)
all_df_wide.to_csv(os.path.join(path,'all_heatmap_vs_heatmap_wide.csv'))

all_df_long = pd.concat(all_df_long)

# format to be plotted in R
slide_num = [i.split('+')[0] for i in all_df_long['image_number'].values]
slide_disease = [ id_to_english[int(re.sub('Slide','',i))] for i in slide_num ]
all_df_long['condition'] = slide_disease

pair1 = [i.split('Group')[-1] for i in all_df_long['group_name1'].values]
pair2 = [i.split('Group')[-1] for i in all_df_long['group_name2'].values]
pair = [str(i)+','+str(j) for i,j in zip(pair1,pair2)]
all_df_long['group'] = pair


all_df_long.to_csv(os.path.join(path,'all_heatmap_vs_heatmap_long.csv'),index=None)

all_df_long
