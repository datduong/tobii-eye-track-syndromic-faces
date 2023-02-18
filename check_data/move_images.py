import os,sys,re,pickle
import pandas as pd
import numpy as np 

# ---------------------------------------------------------------------------- #

main_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'

source = '25radius-no-ave-whtbg-peter' # '25radius-fix-mismatch-name-csv-no-ave-whtbg'

final_output_dir = 'RemoveAveEyeTrackPeter' # RemoveAveEyeTrack

df = 'TableEyeTrackingSimplePeter.csv'

# ---------------------------------------------------------------------------- #

source = os.path.join(main_dir,source)

# ---------------------------------------------------------------------------- #

df = pd.read_csv(os.path.join(main_dir,df)).fillna('')
columns = [ 'Syn vs Non Syn Correct',
            'Syn vs Non Syn Incorrect', 	 
            'Syn vs NonSyn Correct Syndrome Name Correct',
            'Syn vs NonSyn Correct Syndrome name Incorrect']

# ---------------------------------------------------------------------------- #
# # remove white spaces
# for col in columns: 
#   temp = df[col].values 
#   temp = [str(i).strip() for i in temp]
#   df[col] = temp 

# ---------------------------------------------------------------------------- #

for slide_name in np.arange(1,18) : # np.arange(1,18) [17]

  temp_df = df [ df['Image']==slide_name ]
  
  for index, col in enumerate(columns): 
    
    key_name = [i for i in temp_df[col].tolist() if len(i) > 0 ] 
    
    if len(key_name) == 0: 
      continue

    slide_name = str(slide_name)
    
    im = [i for i in os.listdir(source)] # ! copy images
    im = [i for i in im if '_BAD.png' not in i]
    im = [i for i in im if '_Bad.png' not in i]
    im = [i for i in im if '_bad.png' not in i]
    im = [i for i in im if 'rBAD.png' not in i]
    im = [i for i in im if 'POLR1C' not in i]
  
    im = [i for i in im if re.match(r'^'+slide_name+'_',i) ]

    if len(im) == 0: 
      continue

    print ('slide', slide_name)
    print (key_name,'\n',im)
    
    final_dir = os.path.join(main_dir,final_output_dir,'Slide'+slide_name,'Group'+str(index+1))
    if not os.path.exists(final_dir): 
      os.makedirs(final_dir)

    # if not os.path.exists(os.path.join(final_dir+'OnSlide1')): 
    #   os.makedirs(os.path.join(final_dir+'OnSlide1'))
      
    for i in im: 
      for k in key_name: 
        if ('_'+k+'.png') in i : # ! CHECK NAMING CONVENTION 
          os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))
          # ! move their results from slide 1 --> can later use as baseline 
          # user = i.split('_')[1] # user name 
          # i = '1_'+user+'_25r.png'
          # if os.path.exists(os.path.join(source,i)): 
          #   os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir+'OnSlide1'))



# ---------------------------------------------------------------------------- #

# ! all images 

for image_id in np.arange(1,18): 
  slide_name = str(image_id)
  im = os.listdir(source)
  im = [i for i in im if re.match(r'^'+slide_name+'_',i) ]
  
  final_dir = os.path.join(main_dir,final_output_dir,'Slide'+slide_name,'all')
  if not os.path.exists(final_dir): 
    os.makedirs(final_dir)
    
  #
  for i in im: 
    os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))


