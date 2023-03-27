
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
'G25' :'Sebastian'
}

map_user_to_codename = { v.lower() :k for k,v in map_codename_to_user.items() }

# ! we have wrong spelling in names 
fix_name = {
 'nanditha':'G12',
 'behnam':'G6',
 'sheetal kumar':'G19',
 'astrid golla':'G4',
 'isabelle claus': 'G8',
 'friederike': 'G22'
 }

map_user_to_codename.update(fix_name)
 
# ---------------------------------------------------------------------------- #
add_name = ''
peter_clinician_list = None
nih_clinician_list = None

peter_nonclinician_list = None
nih_nonclinician_list = None

if nih_clinician_list is not None : 
  add_name = add_name + 'nihclinician'

if peter_clinician_list is not None : 
  add_name = add_name + 'peterclinician'

if nih_nonclinician_list is not None: 
  add_name = add_name + 'nihnotclinician'

if peter_nonclinician_list is not None: 
  add_name = add_name + 'peternotclinician'

  
# ---------------------------------------------------------------------------- #


fout = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter+Nih'+add_name+'.csv'
df_array = ['C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter/Simple AOIs_German_032423G1-20.csv',
            'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter/Simple AOIs_German_032423G20-24.csv',
            'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Nih/SimpleAOIs_NIH.csv']

df_array = [pd.read_csv(d) for d in df_array]

dfpeter = pd.concat(df_array[0:2])

dfpeter['where_from'] = 'peter'

dfpeter = dfpeter[dfpeter["TOI"].str.contains("Image") == False] # remove the 3s, why do we need this 3s ? 
dfpeter = dfpeter.reset_index(drop=True)


# ---------------------------------------------------------------------------- #

dfnih = df_array[2]
dfnih['where_from'] = 'nih' # [2] because we have 3 data input 
dfnih = dfnih[dfnih["TOI"].str.contains(" 3s") == False] # remove the 3s, why do we need this 3s ? 
dfnih = dfnih.reset_index(drop=True)

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
  dfpeter = dfpeter["Participant"].isin(peter_clinician_list)

if peter_nonclinician_list is not None:
  dfpeter = dfpeter["Participant"].isin(peter_nonclinician_list)


# ! filter participants? 
if nih_clinician_list is not None:
  dfnih = dfnih["Participant"].isin(nih_clinician_list)

if nih_nonclinician_list is not None:
  dfnih = dfnih["Participant"].isin(nih_nonclinician_list)
  
# ---------------------------------------------------------------------------- #

df = [dfpeter, dfnih]
df = pd.concat(df)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

# ! fix "slide 11" and "slide11" spacing between 2 csv
temp = list (df['Media'].values)
temp = [re.sub('Slide','',t.strip()).strip() for t in temp ]
temp = ['Slide ' + t for t in temp ]
df['Media'] = temp

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
df.to_csv(fout,index=False)

# may see this below, but they don't affect the computation. 
# sys:1: DtypeWarning: Columns (7,8,9,10,11,26) have mixed types.Specify dtype option on import or set low_memory=False.
