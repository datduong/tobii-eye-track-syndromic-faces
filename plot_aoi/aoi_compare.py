import os, sys, re, pickle
import numpy as np
import pandas as pd 

def get_statistic (df, image_name, participants, tobii_metrics, average_option='median'): 
  """_summary_

  Args:
      df (_type_): _description_
      image_name (_type_): _description_
      participants (_type_): _description_
      tobii_metrics (_type_): _description_
      average_option (str, optional): _description_. Defaults to 'median'.

  Returns:
      _type_: _description_
  """
  if image_name is not None: 
    df = df[ df['TOI'].isin([image_name]) ] # get @participants who saw @image_name
  if len(participants)!=0 : 
    df = df[ df['Participant'].isin(participants) ]
  # for each face region, take mean. 
  if df.shape[0] == 0: 
    print ('empty?', image_name, participants)

  #
  if average_option == 'mean': 
    obs_stat = df.groupby('AOI')[tobii_metrics].mean() # ! https://www.statology.org/pandas-mean-by-group/

  if average_option == 'median': 
    obs_stat = df.groupby('AOI')[tobii_metrics].median() # ! https://www.statology.org/pandas-mean-by-group/  
    
  AOI = obs_stat.index.tolist() # ! need this to access the row of each AOI
  obs_stat = obs_stat.to_numpy() # array, num of AOI x tobii_metrics 
  return AOI, obs_stat, df 


def random_sample_df (df1,df2,image_name,participants):
  """_summary_

  Args:
      df1 (_type_): _description_
      df2 (_type_): _description_
      image_name (_type_): _description_
      participants (_type_): _description_

  Returns:
      _type_: _description_
  """
  N1 = len(participants[0])
  N2 = len(participants[1])
  
  # randomly make df1 
  participants = sorted ( list(set ( participants[0] + participants[1] ) ) ) # combine everyone into a single list

  df = pd.concat([df1,df2]) # ! sample obs from both slides at once

  # 
  new_df1 = []
  for n in range(N1): 
    pick_this_person = np.random.choice(participants,size=1) # ! pick a random person 
    pick_this_slide = np.random.choice(image_name,size=1) # ! pick random slide
    this_random_point = df[ df['Participant'].isin(pick_this_person) & df['TOI'].isin(pick_this_slide) ] 
    new_df1.append(this_random_point) # ! make a random dataset
  
  #
  new_df2 = []
  for n in range(N2): 
    pick_this_person = np.random.choice(participants,size=1)
    pick_this_slide = np.random.choice(image_name,size=1)
    this_random_point = df[ df['Participant'].isin(pick_this_person) & df['TOI'].isin(pick_this_slide) ]
    new_df2.append(this_random_point)

  return pd.concat(new_df1), pd.concat(new_df2)


def do_bootstrap (df, image_name, participants, tobii_metrics, boot_num=100): 
  """Bootstrap

  Args:
      df (pd.dataframe): _description_
      image_name (array): [slide1,slide2]
      participants (array): _description_
      tobii_metrics (array): _description_
      boot_num (int, optional): _description_. Defaults to 100.

  Returns:
      _type_: _description_
  """
  group_statistic = {}
  for index,g in enumerate(image_name): 
    group_statistic[index] = get_statistic (df, g, participants[index], tobii_metrics) 

  # 
  assert np.array_equal(group_statistic[0][0], group_statistic[1][0]) # equal @AOI
  observed_stat = group_statistic[0][1] - group_statistic[1][1] # matrix

  boot = []

  for i in range(boot_num):
    # make random df
    boot_df1, boot_df2 = random_sample_df ( group_statistic[0][2], group_statistic[1][2], image_name, participants)
    boot_group_statistic1 = get_statistic (boot_df1, image_name=None, participants=[], tobii_metrics=tobii_metrics) 
    boot_group_statistic2 = get_statistic (boot_df2, image_name=None, participants=[], tobii_metrics=tobii_metrics) 
    #
    boot_stat = boot_group_statistic1[1] - boot_group_statistic2[1]
    boot.append(boot_stat)
  
  # finish bootstrap
  boot = np.array(boot)
  mean = np.nanmean(boot,axis=0)
  std = np.nanstd(boot,axis=0)

  pval = np.sum( boot >= np.abs(observed_stat ), axis=0) / boot_num # how often boot sample is more extreme than observed

  AOI = group_statistic[0][0]

  # format output 
  observed_stat = pd.DataFrame(observed_stat, columns=tobii_metrics, index=AOI)
  pval = pd.DataFrame(pval, columns=tobii_metrics, index=AOI)
  mean = pd.DataFrame(mean, columns=tobii_metrics, index=AOI)
  std = pd.DataFrame(std, columns=tobii_metrics, index=AOI)
  
  return observed_stat, pval, group_statistic, boot, mean, std, AOI

# ---------------------------------------------------------------------------- #

# ! permute entire row to get statistic significant test. 
df = 'C:/Users/duongdb/Documents/GitHub/Tobii-AOI-FaceSyndromes/data/Trial_data_export_121522.csv'
df = pd.read_csv(df)
df = df.sort_values(['AOI','Participant']).reset_index(drop=True)

# df["Time_to_first_whole_fixation"] = df["Time_to_first_whole_fixation"].replace(np.nan, 7000)

df["Duration_of_first_whole_fixation"] = df["Duration_of_first_whole_fixation"].replace(np.nan, 0)

# slides = ['Slide 2','Slide 11']

# people_names = [  ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','TCOF1','WHSC1','PTPN11','RIT1','TBX'], 
#                   ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','TCOF1','WHSC1','PTPN11','RIT1','TBX'] ]

slides = ['Slide 11','Slide 11']

people_names = [  ['BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','SMAD1','TCOF1','WHSC1'], 
                  ['PTPN11','RIT1','TBX'] ]

tobii_metrics = ['Total_duration_of_whole_fixations','Time_to_first_whole_fixation','Number_of_whole_fixations','Duration_of_first_whole_fixation']

observed_stat, pval, group_statistic, boot, mean, std, AOI = do_bootstrap (   df, 
                                                                              image_name=slides, 
                                                                              participants=people_names,   
                                                                              tobii_metrics=tobii_metrics,
                                                                              boot_num=200)


for d in [observed_stat, pval, mean, std]:
  print(d.to_string())

