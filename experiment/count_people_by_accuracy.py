
import os,sys,re,pickle
import numpy as np 

# ! count by accuracy 

# Heatmap25rExpertNoAveByAcc04172023

main_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/'

slides = ['Slide' + str(i) for i in np.arange(2,18)]

groups = ['Group' + str(i) for i in np.arange(1,4)]

for s in slides: 
  print ('\n')
  for g in groups: 
    try: 
      print ( s, g, len ( os.listdir(os.path.join(main_path,s,g))) ) 
    except: 
      pass 
