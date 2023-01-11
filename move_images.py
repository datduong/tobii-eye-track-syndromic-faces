import os,sys,re,pickle

# probably not every important 
# move images around 

source='C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01032023/Prelim/25radius'

final_dir='C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01032023/Prelim/KS_25rad_01072023/IndividualThird_OnSlide1'

if not os.path.exists(final_dir): 
  os.makedirs(final_dir)

  
slide_name = '1_'

# key_name = ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','SMAD1','TCOF1','WHSC1']

key_name = ['PTPN11','RIT1','TBX']

im = [i for i in os.listdir(source)]

im = [i for i in im if '_BAD.png' not in i]

im = [i for i in im if re.match(r'^'+slide_name,i) ]

for i in im: 
  for k in key_name: 
    if k in i : 
      os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))


    

