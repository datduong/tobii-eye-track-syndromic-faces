
import os,sys,re,pickle
import numpy as np
import pandas as pd 

df = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/AOI-default03232023/Nih/Simple AOIs_NIH_032923.csv'
df = pd.read_csv(df)
user_in_df = set(df['Participant'].values)

image_source = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/25radius-fix-mismatch-name-to-csv-04172023'

img = os.listdir(image_source)

dash_in_name = [i for i in img if '-' in i]
dash_in_name


img = [i.split('_')[1] for i in os.listdir(image_source)]
img = [i.split('-')[0] if '-' in i else i for i in img  ]

img = set(img)

print ('in user in df but not img')
print ( user_in_df-img )

print ('reverse')
print ( img-user_in_df ) 
# {'GTF21', 'GTF@1', 'CEBBP', 'KIMT2', 'RTI', 'TOCF1', 'RITI', 'PTPN'}

# ---------------------------------------------------------------------------- #
# ! check with simple excel that saves the accuracy scores
acc = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/eye_track_record_accuracy_per_person.csvNih04172023.csv'
acc = pd.read_csv(acc)
user_acc = []
for i in np.arange(0,4): 
  user_acc = user_acc + acc.iloc[:, i].values.tolist()
#

user_acc = set (user_acc)
print ('in user in acc but not img')
print ( user_acc-img )
print ('reverse')
print ( img-user_acc ) 

# ---------------------------------------------------------------------------- #

rename = {'GTF21':'GTF2I', 'GTF@1':'GTF2I', 
          'CEBBP':'CREBBP', 
          'KIMT2':'KMT2', 
          'RTI':'RIT1', 
          'TOCF1':'TCOF1', 
          'RITI':'RIT1', 
          'PTPN':'PTPN11'}

# ! need to rename the images. 
image_source = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/25radius'
cygwin_source = '/cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius'
for i in os.listdir(image_source): 
  userid = i.split('_')[1] 
  userid = userid.split('-')[0] if '-' in userid else userid
  for k,val in rename.items(): 
    if k == userid: 
      newname = re.sub(k,val,i)
      print ('mv '+ os.path.join(cygwin_source,i) + ' ' + os.path.join(cygwin_source,newname))
      # os.system('mv '+ os.path.join(image_source,i) + ' ' + os.path.join(image_source,newname))
  
#


# user_in_df
# {'BAF60a',
#  'BRD4',
#  'CREBBP',
#  'EP300',
#  'GTF2I',
#  'KMT2',
#  'LIMK1',
#  'PDGFRa',
#  'POLR1C',
#  'PTPN11',
#  'RAD21',
#  'RIT1',
#  'SMAD1',
#  'TBX1',
#  'TCOF1',
#  'WHSC1'}

# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/10_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/10_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/10_RITI-25r_BAD.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/10_RIT1-25r_BAD.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/12_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/12_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/13_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/13_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/13_RITI_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/13_RIT1_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/14_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/14_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/14_RITI_25r_BAD.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/14_RIT1_25r_BAD.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/15_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/15_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/15_RITI_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/15_RIT1_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_CEBBP_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_CREBBP_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_RITI_25r_bad.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_RIT1_25r_bad.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_TOCF1_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/16_TCOF1_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/17_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/17_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/17_RITI_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/17_RIT1_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_KIMT2_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_KMT2_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_PTPN_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/5_PTPN11_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_KIMT2_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_KMT2_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_RITI_25rBAD.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/6_RIT1_25rBAD.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/7_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/7_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/8_GTF21_25r.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/8_GTF2I_25r.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/9_GTF@1_25r_BAD.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/9_GTF2I_25r_BAD.png
# mv /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/9_RTI_25r_BAD.png /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/25radius/9_RIT1_25r_BAD.png