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

# ---------------------------------------------------------------------------- #

path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Compare2Saliency/k20-thresh0.05-pixcut20-seg'
foutpath = path
criteria_arr = ['k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3',
                # 'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3', 
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3',
                'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3', 
                # 'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3'
                ]

slide = ['Slide' + str(i) for i in np.arange(1,18)]

for criteria in criteria_arr: 
  csv = [i for i in os.listdir(path) if i.endswith('csv')]
  csv = [i for i in csv if criteria in i]
  csv = [ pd.read_csv(os.path.join(path,c) ) for c in csv ] 
  df_long = pd.concat (csv)
  df_long.to_csv(os.path.join(foutpath,'Eb4Occ-'+criteria+'.csv'), index=False)


# ---------------------------------------------------------------------------- #


