
import sys,re,pickle,os
import numpy as np 
import pandas as pd 

main_data_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023/img_img_aoi_result'
os.chdir(main_data_path)
df = [i for i in os.listdir(main_data_path) if i.endswith('pval.csv')]
df = [pd.read_csv(i) for i in df]

df = pd.concat(df)
df.to_csv('/data/duongdb/Face11CondTobiiEyeTrack01112023/img_img_aoi_pval.csv', index=None)


# ---------------------------------------------------------------------------- #


