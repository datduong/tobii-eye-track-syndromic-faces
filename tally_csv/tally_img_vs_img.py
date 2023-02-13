import os,sys,re,pickle
import numpy as np
import pandas as pd 

import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, balanced_accuracy_score


# ! can make a heatmap of pvalue here. 

this_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images'
if os.path.exists(this_path): 
  os.system('rm -f ' + os.path.join(this_path,'all_results.csv'))
  df = [pd.read_csv(os.path.join(this_path,i)) for i in os.listdir(this_path) if i.endswith('csv')]
  df = pd.concat(df)
  temp = df['boot_rank'].to_numpy()
  temp = np.where(temp > .5, 1-temp, temp)
  df['boot_pval'] = list(temp)
  df.to_csv(os.path.join(this_path,'all_results.csv'))


# ---------------------------------------------------------------------------- #

this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images'
df = 'all_results.csv'
df = pd.read_csv(os.path.join(this_path,df))

# nosmooth-thresh0.0-avepix0.3-round
# nosmooth-rawpixcut90.0-thresh0.0-avepix0.3-round

# criteria_array = [ 'nosmooth-thresh0.0-avepix0.3-round' + str(i) for i in [0.2, 0.3, 0.4 ,0.5 ,0.6 ,0.7, 0.8]]

criteria_array = ['k0-thresh0.0-avepix0.2-smoothave-pixcutave'+s+'-round0.3' for s in '45.0 70.0 90.0 110.0 135.0 170.0 190.0'.split() ]

group_array = ['Group1','Group3','Group2','Group4','all']

group_array = ['Group1','all']


slide_count = 17

for group in group_array: 
  for criteria in criteria_array: 

    all_pval = np.ones((slide_count,slide_count))
    
    df2 = df[df['type']==criteria ]
    df2 = df2[df2['group_name1'].str.contains(group) ]

    for index,row in df2.iterrows(): 
      slides = [s.strip() for s in row['image_number'].split('+')]
      i = int(re.sub('Slide','',slides[0]))-1
      j = int(re.sub('Slide','',slides[1]))-1
      if row['boot_pval'] == 0: 
        row['boot_pval'] = 0.001
      all_pval[i,j] = row['boot_pval']
      all_pval[j,i] = row['boot_pval']


    maskout = np.triu(all_pval)

    df_cm = pd.DataFrame( all_pval, 
                          index = [str(i+1) for i in range(slide_count)],
                          columns = [str(i+1) for i in range(slide_count)]
                        ).astype(float).round(3)

    
    plt.figure(figsize=(15,15))
    sn.set_context("talk", font_scale=1)
    sn.set(font_scale=1.2) # for label size
    ax = plt.axes()
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 20}, fmt=".2f", cbar=False, ax=ax, mask=maskout) # font size mask=maskout

    ax.set_title('Img vs Img, Correct Affected vs. Unaffected, '+criteria)
    plt.xticks(rotation=20)
    plt.yticks(rotation=0)
    plt.rc('ytick', labelsize=18)
    plt.savefig(os.path.join(this_path,group+'-'+criteria+'.png'))
