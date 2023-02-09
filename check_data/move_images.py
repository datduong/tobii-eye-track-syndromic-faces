import os,sys,re,pickle
import pandas as pd
import numpy as np 

# probably not every important 
# move images around 

df = pd.read_csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/TableEyeTrackingSimple.csv').fillna('')

columns = [ 'Syn vs Non Syn Correct',
            'Syn vs Non Syn Incorrect', 	 
            'Syn vs NonSyn Correct Syndrome Name Correct',
            'Syn vs NonSyn Correct Syndrome name Incorrect']

main_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'
source='C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-fix-mismatch-name-csv-no-ave'

for slide_name in [17]: # np.arange(1,18)

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
    print (key_name,im)
    
    final_dir = os.path.join(main_dir,'RemoveAveEyeTrack','Slide'+slide_name,'Group'+str(index+1))
    if not os.path.exists(final_dir): 
      os.makedirs(final_dir)

    # if not os.path.exists(os.path.join(final_dir+'OnSlide1')): 
    #   os.makedirs(os.path.join(final_dir+'OnSlide1'))
      
    for i in im: 
      for k in key_name: 
        if k in i : 
          os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))
          # ! move their results from slide 1 --> can later use as baseline 
          # user = i.split('_')[1] # user name 
          # i = '1_'+user+'_25r.png'
          # if os.path.exists(os.path.join(source,i)): 
          #   os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir+'OnSlide1'))



# ---------------------------------------------------------------------------- #

# ! all images 
main_dir = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'
source='C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/25radius-fix-mismatch-name-csv-no-ave'

for image_id in np.arange(1,18): 
  slide_name = str(image_id)
  im = os.listdir(source)
  im = [i for i in im if re.match(r'^'+slide_name+'_',i) ]
  
  final_dir = os.path.join(main_dir,'RemoveAveEyeTrack','Slide'+slide_name,'all')
  if not os.path.exists(final_dir): 
    os.makedirs(final_dir)
    
  #
  for i in im: 
    os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))




slide 17
['CREBBP', 'GTF2I', 'LIMK1', 'PDGFRa', 'TCOF1', 'WHSC1'] ['17_BAF60a_25r.png', '17_BRD4_25r.png', '17_CREBBP_25r.png', '17_EP300_25r.png', '17_GTF21_25r.png', '17_KMT2_25r.png', '17_PDGFRa_25r.png', '17_PTPN11_25r.png', '17_RAD21_25r.png', '17_RITI_25r.png', '17_SMAD1_25r.png', '17_TBX1_25r.png', '17_TCOF1_25.png', '17_WHSC1_25r.png']
slide 17
['BAF60a', 'BRD4', 'EP300', 'KMT2', 'POLR1C', 'PTPN11', 'RAD21', 'RIT1', 'SMAD1', 'TBX1'] ['17_BAF60a_25r.png', '17_BRD4_25r.png', '17_CREBBP_25r.png', '17_EP300_25r.png', '17_GTF21_25r.png', '17_KMT2_25r.png', '17_PDGFRa_25r.png', '17_PTPN11_25r.png', '17_RAD21_25r.png', '17_RITI_25r.png', '17_SMAD1_25r.png', '17_TBX1_25r.png', '17_TCOF1_25.png', '17_WHSC1_25r.png']
slide 17
['PDGFRa'] ['17_BAF60a_25r.png', '17_BRD4_25r.png', '17_CREBBP_25r.png', '17_EP300_25r.png', '17_GTF21_25r.png', '17_KMT2_25r.png', '17_PDGFRa_25r.png', '17_PTPN11_25r.png', '17_RAD21_25r.png', '17_RITI_25r.png', '17_SMAD1_25r.png', '17_TBX1_25r.png', '17_TCOF1_25.png', '17_WHSC1_25r.png']
slide 17
['CREBBP', 'GTF2I', 'LIMK1', 'TCOF1', 'WHSC1'] ['17_BAF60a_25r.png', '17_BRD4_25r.png', '17_CREBBP_25r.png', '17_EP300_25r.png', '17_GTF21_25r.png', '17_KMT2_25r.png', '17_PDGFRa_25r.png', '17_PTPN11_25r.png', '17_RAD21_25r.png', '17_RITI_25r.png', '17_SMAD1_25r.png', '17_TBX1_25r.png', '17_TCOF1_25.png', '17_WHSC1_25r.png']