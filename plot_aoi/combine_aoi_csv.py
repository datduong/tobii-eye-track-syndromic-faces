
import os,sys,re,pickle
import numpy as np 
import pandas as pd 

# ! combine input from Ben and Anna
# ! do some filter here? 

# ---------------------------------------------------------------------------- #

map_codename_to_user = {
'G1'	:'Alexej',
'G2'	:'Andreas',
'G3'	:'Fabian',
'G4'	:'Astrid Gola',
'G5'	:'Aakash',
'G6'	:'Benham',
'G7'	:'Rana',
'G8'	:'Isabella',
'G9'	:'Grace',
'G10'	:'Axel',
'G11'	:'Annette',
'G12'	:'Nanitha',
'G13'	:'Leonie',
'G14'	:'Pietro',
'G15'	:'Schmida',
'G16'	:'Hustinx',
'G17'	:'Tim Bender',
'G18'	:'Farhad',
'G19'	:'Sheethal',
'G20'	:'Berny',
'G21'	:'Hannah',
'G22'	:'Fredreike',
'G23'	:'Manuel',
'G24'	:'Meghna',
'G25' :'Sebastian',
'G26' :'Matthias Weigl',
'G27' :'Elisabeth',
'G28' :'Tzung', 
'G29' :'Claudia',
}

map_user_to_codename = { v.lower() :k for k,v in map_codename_to_user.items() } # ! PUT EVERYTHING IN LOWER CASE, MAKE LIFE EASER

# ! we have wrong spelling in names, MUST USE LOWER CASE HERE, MAKE LIFE EASIER
fix_name = {
 'nanditha':'G12',
 'behnam':'G6',
 'sheetal kumar':'G19',
 'astrid golla':'G4',
 'isabelle claus': 'G8',
 'friederike': 'G22',
 'mattihias': 'G26',
 'elisabet': 'G27',
 }

map_user_to_codename.update(fix_name)
 
# ---------------------------------------------------------------------------- #
add_name = '04072023'

peter_clinician_id_number = [8,10,11,19,17,27,29]

peter_clinician_list = None # ['G'+str(i) for i in peter_clinician_id_number] # None

# nih_clinician_list = None
nih_clinician_list = ['BAF60a',
                      'BRD4',
                      'CREBBP',
                      'EP300',
                      # 'GTF2I',
                      'KMT2',
                      'LIMK1',
                      'PDGFRa',
                      'POLR1C',
                      'PTPN11',
                      # 'RAD21',
                      'RIT1',
                      'SMAD1',
                      'TBX1',
                      'TCOF1',
                      'WHSC1'] # GTF2I RAD21	are trainees

peter_nonclinician_list = ['G'+str(i) for i in range(1,30) if i not in peter_clinician_id_number ] # ['G'+str(i) for i in range(1,25) if i not in peter_clinician_id_number ]   #  None

nih_nonclinician_list = None # ['GTF2I','RAD21'] GTF2I RAD21

# ---------------------------------------------------------------------------- #

if nih_clinician_list is not None : 
  add_name = add_name + 'NihClinic'

if peter_clinician_list is not None : 
  add_name = add_name + 'PeterClinic'

if nih_nonclinician_list is not None: 
  add_name = add_name + 'NihNotClinic'

if peter_nonclinician_list is not None: 
  add_name = add_name + 'PeterNotClinic'

  
# ---------------------------------------------------------------------------- #

fout = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter+Nih'+add_name+'.csv'

df_array = ['C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter/AOI_peter_04072023.csv',
            'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Nih/Simple AOIs_NIH_032923.csv']

df_array = [pd.read_csv(d) for d in df_array]

# ---------------------------------------------------------------------------- #

# dfpeter = pd.concat(df_array[0:2])
dfpeter = df_array[0]
dfpeter['where_from'] = 'peter'

dfpeter = dfpeter[dfpeter["TOI"].str.contains("Image") == False] # remove the 3s, why do we need this 3s ? 
dfpeter = dfpeter.reset_index(drop=True)

# check user names 
user = set(dfpeter['Participant'].values.tolist()) 
user_define = set ( map_user_to_codename.keys() ) 
print ( user_define - user ) 
print ( user - user_define )


# ---------------------------------------------------------------------------- #

dfnih = df_array[1] # use at [1] or [2] because we have 2 or 3 data input 
dfnih['where_from'] = 'nih' 
dfnih = dfnih[dfnih["TOI"].str.contains(" 3s") == False] # remove the 3s, why do we need this 3s ? 
dfnih = dfnih.reset_index(drop=True)

# check user names 
user = set(dfnih['Participant'].values.tolist()) 
user_define = """BAF60a
BRD4
CREBBP
EP300
GTF2I
KMT2
LIMK1
PDGFRa
POLR1C
PTPN11
RAD21
RIT1
SMAD1
TBX1
TCOF1
WHSC1
""".split('\n')
user_define = set ( [i.strip() for i in user_define] ) 
print ( user_define - user ) 
print ( user - user_define )


# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #

# ! map user name into code name G_number 

user_name = [i.lower() for i in dfpeter['Participant'].values.tolist()] # lower case all user names in peter

print (set(user_name)) # see all user name

for index,user in enumerate(user_name) : 
  for key in map_user_to_codename: 
    if re.match(key,user): 
      user_name[index] = map_user_to_codename[key]

# see all user name again. 
print (set(user_name)) 
dfpeter['Participant'] = user_name

# ---------------------------------------------------------------------------- #

# ! filter participants? 
if peter_clinician_list is not None:
  dfpeter = dfpeter [ dfpeter["Participant"].isin(peter_clinician_list) ]

if peter_nonclinician_list is not None:
  dfpeter = dfpeter [ dfpeter["Participant"].isin(peter_nonclinician_list) ]


# ! filter participants? 
if nih_clinician_list is not None:
  dfnih = dfnih [ dfnih["Participant"].isin(nih_clinician_list) ]

if nih_nonclinician_list is not None:
  dfnih = dfnih [ dfnih["Participant"].isin(nih_nonclinician_list) ] 
  
# ---------------------------------------------------------------------------- #

df = [dfpeter, dfnih]
df = pd.concat(df)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

df = df [ df["Media"] != "Entire Recording" ] 
df = df [ df["TOI"] != "Entire Recording" ] 
# ! fix "slide 11" and "slide11" spacing between 2 csv
temp = list (df['Media'].values)
temp = [re.sub('Slide','',t.strip()).strip() for t in temp ]
temp = ['Slide ' + t for t in temp ]
df['Media'] = temp

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
df.to_csv(fout,index=False)

print ( 'check final user list', sorted( list (set (df['Participant'].values.tolist()) ) ))

# may see this below, but they don't affect the computation. 
# sys:1: DtypeWarning: Columns (7,8,9,10,11,26) have mixed types.Specify dtype option on import or set low_memory=False.
