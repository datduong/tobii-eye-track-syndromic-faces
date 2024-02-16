import os,sys,re,pickle
import numpy as np
import pandas as pd 


# ! combine all heatmap result
# ! filter rows/cols for nice visual


match_powerpoint_to_tobii = { # ! in Suzanna's original powerpoint, the images are not in the same order as Chris's ordering on Tobii. 
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

id_to_english_name_out = {
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
  3: 'Unaff1',
  5: 'Unaff2',
  7: 'Unaff3',
  10: 'Unaff4',
  13: 'Unaff5',
  16: 'Unaff6',
}


# ---------------------------------------------------------------------------- #

path = '/data/duongdb/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023'
foutpath = '/data/duongdb/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023'

criteria_arr = ['k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3', 
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3', 
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff',
                'k0-thresh0.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-diff',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3',
                ]

slide = ['Slide' + str(i) for i in np.arange(2,18)]

for this_group in ['all','Group1','Group2','Group3','Group4']:
  for criteria in criteria_arr: 
    df_arr = []
    for this_slide in slide: 
      csv = [i for i in os.listdir(os.path.join(path,this_slide)) if i.endswith('csv')]
      csv = [i for i in csv if criteria in i]
      csv = [i for i in csv if this_group in i]
      csv = [ pd.read_csv(os.path.join(path,this_slide,c) ) for c in csv ] 
      if len(csv) == 0: 
        continue
      csv = pd.concat (csv) # put all the slide together 
      csv['condition'] = id_to_english_name_out[ int (re.sub('Slide','',this_slide)) ] # ! use english labels, instead of using slide1 slide2...
      df_arr = df_arr + [csv] # append  over many slides
    #
    if len(df_arr) == 0: 
      continue
    #
    df_long = pd.concat (df_arr)
    df_long.to_csv(os.path.join(foutpath,this_group+'-'+criteria+'.csv'), index=False)


#

