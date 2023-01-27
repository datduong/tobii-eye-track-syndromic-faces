import sys,os,re,pickle
import numpy as np 
import pandas as pd 

# ! just count how often AOI_x ranks high/low 
df = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/img_img_aoi_pval.csv'
df = pd.read_csv(df)

slides = np.arange(2,18)

aoi = sorted ( list ( set (df['index'].values ) ) )
# this_aoi = 'L_eye'
metric = sorted ( list ( set (df['variable'].values ) ) )
# metric = ['Number_of_whole_fixations']

all_count_matrix = {}

for index_metric, this_metric in enumerate(metric): 
  count_matrix = np.zeros((len(aoi),len(slides)))
  for index_aoi,this_aoi in enumerate(aoi): 
    df2 = df[(df['variable']==this_metric) & (df['index']==this_aoi)]
    for index,row in df2.iterrows(): 
      if (row['value_x'] == 0) or (row['value_x']==1):
        continue
      if (row['value_x'] < 0.05): # small pvalue 
        if this_metric == 'Time_to_first_whole_fixation': 
          if ( row['value_y'] < 0 ): # how often faster (so smaller number) people look at slide1
            x = row['slide1']-2 # shift 1 down because 1st slide is practice 
          else: 
            x = row['slide2']-2
        else: 
          if ( row['value_y'] > 0 ): # how often slide1 is higher than the other slide2 
            x = row['slide1']-2 # shift 1 down because 1st slide is practice 
          else: 
            x = row['slide2']-2
        #
        count_matrix [index_aoi,x] = count_matrix [index_aoi,x] + 1 
      #
  # 
  all_count_matrix[this_metric] = count_matrix
      
#

for m in metric: 
  arr = all_count_matrix[m]
  df = pd.DataFrame(data = arr, index = aoi, 
                                columns = slides)
  print(m)
  print(df.to_string())
  df.to_csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/img_img_'+m+'.csv')
  #

