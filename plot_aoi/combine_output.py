
import sys,re,pickle,os
import numpy as np 
import pandas as pd 

main_data_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/img_img_aoi_result'
os.chdir(main_data_path)
df = [i for i in os.listdir(main_data_path) if i.endswith('pval.csv') ]
df = [pd.read_csv(i) for i in df]
df = pd.concat(df)

df2 = [i for i in os.listdir(main_data_path) if i.endswith('observed_stat.csv')]
df2 = [pd.read_csv(i) for i in df2]
df2 = pd.concat(df2)

# df['observed_stat'] = df2['value'].values
df.shape

df2.shape

 
df3 = pd.merge(df,df2,on=['index','variable','slide1','slide2'])

df3.to_csv('/data/duongdb/Face11CondTobiiEyeTrack01112023/img_img_aoi_pval.csv', index=None)


# ---------------------------------------------------------------------------- #


