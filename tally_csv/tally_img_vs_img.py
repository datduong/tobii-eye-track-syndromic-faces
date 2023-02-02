import os,sys,re,pickle
import numpy as np
import pandas as pd 

import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, balanced_accuracy_score


# ! can make a heatmap of pvalue here. 

# this_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images'
# df = [pd.read_csv(os.path.join(this_path,i)) for i in os.listdir(this_path) if i.endswith('csv')]
# df = pd.concat(df)
# temp = df['boot_rank'].to_numpy()
# temp = np.where(temp > .5, 1-temp, temp)
# df['boot_pval'] = list(temp)

# df.to_csv(os.path.join(this_path,'all_results.csv'))


# ---------------------------------------------------------------------------- #

this_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Diseases'
df = 'all_results.csv'
df = pd.read_csv(os.path.join(this_path,df))

slide_count = 17
all_pval = np.ones((slide_count,slide_count))
criteria = 'smoothk10-thresh0.5-scaleave-bootseg-round0.7'

# {'smoothk20-otsu',
#  'smoothk20-thresh0.3',
#  'smoothk20-thresh0.4',
#  'smoothk20-thresh0.5',
#  'smoothk20-thresh0.6',
#  'smoothk20-thresh0.7'}

df = df[df['type']==criteria ]
df = df[df['group_name1'].str.contains('Group1') ]

for index,row in df.iterrows(): 
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
plt.savefig(os.path.join(this_path,criteria+'.png'))
# pickle.dump(normalized_array,open(title+'.np','wb')) # later we will average over many folds

# /data/duongdb/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/Compare2Images/smoothk10-thresh0.5-scaleave-bootseg-round0.7_seg_ave

