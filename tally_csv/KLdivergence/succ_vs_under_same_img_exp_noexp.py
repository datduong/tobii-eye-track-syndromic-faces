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

path = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/KL-symmetric/Underperforming_clin_vs_nonclin'
foutpath = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/KL-symmetric/Underperforming_clin_vs_nonclin'


file_name_array = [ 'G2vG2-70.0-kl.csv',
                    'G2vG2-110.0-kl.csv'
                  ]

# ! map slide into disease names. 

for fin in file_name_array: 
  df = pd.read_csv(os.path.join(path,fin))
  temp = df['group_name1'].tolist() # ['SlideXGroupY']
  temp = [i.split('Group')[0] for i in temp]
  temp = [int ( re.sub('Slide','',i) ) for i in temp]
  df ['label_index'] = temp
  temp = [id_to_english_name_out[i] for i in temp ]
  df ['condition'] = temp 
  # ! sort by label index
  df = df.sort_values(by=['label_index'],ignore_index=True)
  new_name = re.sub (r'\.csv','-name.csv',fin)
  df.to_csv ( os.path.join(foutpath,new_name), index=None)

  

