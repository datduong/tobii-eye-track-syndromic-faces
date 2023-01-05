import os, sys, re, pickle
import numpy as np
import pandas as pd 

def get_statistic (df, image_name, participants, col_name): 
  if image_name is not None: 
    df = df[ df['TOI'].isin([image_name]) ] # get @participants who saw @image_name
  if len(participants)!=0 : 
    df = df[ df['Participant'].isin(participants) ]
  # for each face region, take mean. 
  if df.shape[0] == 0: 
    print ('empty?')
  obs_stat = df.groupby('AOI')[col_name].mean() # ! https://www.statology.org/pandas-mean-by-group/
  AOI = obs_stat.index.tolist() # ! need this to access the row of each AOI
  obs_stat = obs_stat.to_numpy() # array, num of AOI x col_name 
  return AOI, obs_stat, df 

def random_shuffle_get_statistic (df, image_name, participants, col_name, seed): 
  df = df.sample(frac=1,replace=True,seed=seed).reset_index(drop=True)
  return get_statistic (df, image_name, participants, col_name)

def random_sample_df (df1,df2,image_name,participants):
  N1 = len(participants[0])
  N2 = len(participants[1])
  # randomly make df1 
  participants = sorted ( list(set ( participants[0] + participants[1] ) ) ) # combine everyone into a single list

  df = pd.concat([df1,df2])
  # 
  new_df1 = []
  for n in range(N1): 
    pick_this_person = np.random.choice(participants,size=1)
    pick_this_slide = np.random.choice(image_name,size=1)
    this_random_point = df[ df['Participant'].isin(pick_this_person) & df['TOI'].isin(pick_this_slide) ]
    new_df1.append(this_random_point)
  
  #
  new_df2 = []
  for n in range(N2): 
    pick_this_person = np.random.choice(participants,size=1)
    pick_this_slide = np.random.choice(image_name,size=1)
    this_random_point = df[ df['Participant'].isin(pick_this_person) & df['TOI'].isin(pick_this_slide) ]
    new_df2.append(this_random_point)

  return pd.concat(new_df1), pd.concat(new_df2)
  
def do_bootstrap (df, image_name, participants, col_name, boot_num=100): 
  """
  Bootstrap.
  Args:
    df: pd.dataframe
    image_name (array): [slide1,slide2]
    participants (array): 

  Returns:
      
  """
  group_statistic = {}
  for index,g in enumerate(image_name): 
    group_statistic[g] = get_statistic (df, g, participants[index], col_name) 

  # 
  assert np.array_equal(group_statistic[image_name[0]][0], group_statistic[image_name[1]][0]) # equal @AOI
  observed_stat = group_statistic[image_name[0]][1] - group_statistic[image_name[1]][1] # matrix

  boot = []

  for i in range(boot_num):
    # make random df
    boot_df1, boot_df2 = random_sample_df ( group_statistic[image_name[0]][2], group_statistic[image_name[1]][2], image_name, participants)
    boot_group_statistic1 = get_statistic (boot_df1, image_name=None, participants=[], col_name=col_name) 
    boot_group_statistic2 = get_statistic (boot_df2, image_name=None, participants=[], col_name=col_name) 
    #
    boot_stat = boot_group_statistic1[1] - boot_group_statistic2[1]
    boot.append(boot_stat)
  # 

  boot = np.array(boot)
  mean = np.nanmean(boot,axis=0)
  std = np.nanstd(boot,axis=0)

  pval = np.sum( boot >= np.abs(observed_stat ), axis=0) / 100 # how often boot sample is more extreme than observed

  AOI = group_statistic[image_name[0]][0]
  
  return observed_stat, pval, group_statistic, boot, mean, std, AOI

# ---------------------------------------------------------------------------- #

# ! permute entire row to get statistic significant test. 
df = 'C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/data/Trial_data_export_121522.csv'
df = pd.read_csv(df)
df = df.sort_values(['AOI','Participant']).reset_index(drop=True)

slides = ['Slide 2','Slide 11']

people_names = [  ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','TCOF1','WHSC1','PTPN11','RIT1','TBX'], 
                  ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','TCOF1','WHSC1','PTPN11','RIT1','TBX'] ]

col_names = ['Total_duration_of_whole_fixations','Time_to_first_whole_fixation','Number_of_whole_fixations']

observed_stat, pval, group_statistic, boot, mean, std, AOI = do_bootstrap (   df, 
                                                                              image_name=slides, 
                                                                              participants=people_names,   
                                                                              col_name=col_names)
group_statistic['Slide 2'][0]

print (observed_stat[4])
print (mean[4])
print (std[4])


