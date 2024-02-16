import os,sys,re,pickle
import numpy as np
import pandas as pd 


# ! combine all heatmap result
# ! filter rows/cols for nice visual


match_powerpoint_to_tobii = {
  1:3, 
  2:5, 
  3:7, 
  4:10, 
  5:13, 
  6:16, 
  7:12, 
  8:15, 
  9:8, 
  10:11, 
  11:6, 
  12:4, 
  13:14, 
  16:17, 
  17:9, 
  23:2
}

match_tobii_to_powerpoint = { v:k for k,v in match_powerpoint_to_tobii.items() }

id_to_english = {
  1:'TCS',
  2:'WS', 
  4:'RSTS1', 
  6:'WHS',
  8:'CdLS', 
  9:'Down',
  11:'KS', 
  12:'NS', 
  14:'22q11DS', 
  15:'PWS',
  17:'BWS',
  3: 'Unaff3',
  5: 'Unaff5',
  7: 'Unaff7',
  10: 'Unaff10',
  13: 'Unaff13',
  16: 'Unaff16',
}

id_to_english_name_out = {
  1:'TCS',
  2:'WS', 
  4:'RSTS1', 
  6:'WHS',
  8:'CdLS', 
  9:'Down',
  11:'KS', 
  12:'NS', 
  14:'22q11DS', 
  15:'PWS',
  17:'BWS',
  3: 'Unaff1',
  5: 'Unaff2',
  7: 'Unaff3',
  10: 'Unaff4',
  13: 'Unaff5',
  16: 'Unaff6',
}


path = '/data/duongdb/TOBII_DATA_PATH/Heatmap25rNonExpertNoAveByAcc04172023/HeatmapAffPerParticipant/SameParticipantAffUnaff' # ! individual output of each participant 

foutname = 'same_participant_aff_vs_unaff_heatmap_long.csv' # ! we put all participants into same csv

# user_array = [  'BAF60a',
#                 'BRD4',
#                 'CREBBP',
#                 'EP300',
#                 'G10',
#                 'G11',
#                 'G17',
#                 'G19',
#                 'G27',
#                 'G29',
#                 'G8',
#                 'GTF2I',
#                 'KMT2',
#                 'LIMK1',
#                 'PDGFRa',
#                 'PTPN11',
#                 'RAD21',
#                 'RIT1',
#                 'SMAD1',
#                 'TBX1',
#                 'TCOF1',
#                 'WHSC1']

user_array = ['G1',
              'G12',
              'G13',
              'G14',
              'G15',
              'G16',
              'G18',
              'G2',
              'G20',
              'G21',
              'G22',
              'G23',
              'G24',
              'G25',
              'G26',
              'G28',
              'G3',
              'G4',
              'G5',
              'G6',
              'G7',
              'G9']

user_array = sorted (user_array)

all_df_long = []

for s in user_array: # ! for each person, look at how this person perform between unaff and affected
  #
  this_path = os.path.join(path,s) # ! look into this user
  if not os.path.exists(this_path): 
    continue
  #
  csv = [i for i in os.listdir(this_path) if i.endswith('csv')]
  if len(csv)==0:
    print ('empty',s)
    continue
  #
  this_df = [ pd.read_csv(os.path.join(this_path,c) ) for c in csv ] 
  this_df = pd.concat(this_df)
  temp = this_df['boot_rank'].to_numpy()
  temp = np.where(temp > .5, 1-temp, temp)
  this_df['boot_pval'] = list(temp)
  # ! long format
  all_df_long.append(this_df) # add 2 list 
  
# 

all_df_long = pd.concat(all_df_long)

# # format to be plotted in R
# slide_num = [i.split('+')[0] for i in all_df_long['image_number'].values]
# slide_disease = [ id_to_english_name_out[int(re.sub('Slide','',i))] for i in slide_num ]
# all_df_long['condition'] = slide_disease

# pair1 = [i.split('Group')[-1] for i in all_df_long['group_name1'].values]
# pair2 = [i.split('Group')[-1] for i in all_df_long['group_name2'].values]
# pair = [str(i)+','+str(j) for i,j in zip(pair1,pair2)]
# all_df_long['group'] = pair

all_df_long.to_csv(os.path.join(path,foutname),index=None)

all_df_long


# ---------------------------------------------------------------------------- #

# cd /cygdrive/c/Users/duongdb/Documents/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/HeatmapAffPerParticipant
# scp $biowulf:/data/duongdb/TOBII_DATA_PATH/Heatmap25rExpertNoAveByAcc04172023/HeatmapAffPerParticipant/SameParticipantAffUnaff/*csv .


