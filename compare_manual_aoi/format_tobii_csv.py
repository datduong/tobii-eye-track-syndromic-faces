
import os,sys,re,pickle
import numpy as np 
import pandas as pd 

df = pd.read_csv('C:/Users/duongdb/Documents/TOBII_DATA_PATH/AOI-data.csv')
name = df['Recording'].values
name = [n.split('-')[0] for n in name]
name = [n.split('_')[0] for n in name]


df['Participant'] = name

df.to_csv('C:/Users/duongdb/Documents/TOBII_DATA_PATH/AOI-data-format.csv',index=None)


