import os, sys, re, pickle
import numpy as np
import pandas as pd 

from argparse import ArgumentParser

from scipy.stats import mannwhitneyu
import pingouin as pg

from tqdm import tqdm

# ---------------------------------------------------------------------------- #


def get_statistic (df, image_name, participants, tobii_metrics, average_option='median', print_participants=False): 
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
    df = df[ df['Media'].isin([image_name]) ] # get @participants who saw @image_name
  if len(participants)!=0 : 
    df = df[ df['Participant'].isin(participants) ]

  # for each face region, take mean. 
  if df.shape[0] == 0: 
    print ('empty?', image_name, participants)
    exit() 

  if print_participants: 
    print ('participant list', sorted(list(set(df['Participant'].values.tolist()))))

  if average_option == 'mean': 
    obs_stat_df = df.groupby('AOI')[tobii_metrics].mean() # ! https://www.statology.org/pandas-mean-by-group/

  if average_option == 'median': 
    obs_stat_df = df.groupby('AOI')[tobii_metrics].median() 
    
  AOI = obs_stat_df.index.tolist() # ! need this to access the row of each AOI, these are just names like "eye,nose,mouth..."
  obs_stat = obs_stat_df.to_numpy() # array, num of AOI x tobii_metrics 

  # also return @obs_stat_df  @df of the user and image. 
  return AOI, obs_stat, df, obs_stat_df


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

  df = [df1,df2] # ! sample obs from both slides at once
  num_of_slide = len(df)

  # 
  prob_1_2 = np.array ([N1,N2]) / (N1+N2)
  boot_sample = []
  for index, N in enumerate ([N1,N2]): 
    new_df = []
    for n in range (N): 
      pick_this_slide = np.random.choice(num_of_slide,size=1,p=prob_1_2)[0] # ! pick random slide
      # print ('pick_this_slide',pick_this_slide)
      temp = list ( set ( df[pick_this_slide]['Participant'].tolist() ) )
      pick_this_person = np.random.choice(temp,size=1) # ! pick a random person in this slide 
      temp = df[pick_this_slide]
      this_random_point = temp[ temp['Participant'].isin(pick_this_person) & temp['Media'].isin([image_name[pick_this_slide]]) ] 
      new_df.append(this_random_point) # ! make a random dataset
    #
    boot_sample.append ( pd.concat(new_df) )
    
  return boot_sample[0], boot_sample[1]


def do_bootstrap (df, image_name, participants, tobii_metrics, args, boot_num=100): 
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
    group_statistic[index] = get_statistic (df, g, participants[index], tobii_metrics, average_option=args.test_statistic, print_participants=True) 

  # 
  assert np.array_equal(group_statistic[0][0], group_statistic[1][0]) # equal @AOI
  observed_stat = group_statistic[0][1] - group_statistic[1][1] # matrix

  # ! compute percent change? 
  observed_stat_percent_change = np.around ( observed_stat/group_statistic[0][1], 2 ) 

  # ! bootstrap 
  boot = []

  for i in range(boot_num):
    # make random df
    boot_df1, boot_df2 = random_sample_df ( group_statistic[0][2], group_statistic[1][2], image_name, participants)
    boot_group_statistic1 = get_statistic (boot_df1, image_name=None, participants=[], tobii_metrics=tobii_metrics, average_option=args.test_statistic) 
    boot_group_statistic2 = get_statistic (boot_df2, image_name=None, participants=[], tobii_metrics=tobii_metrics, average_option=args.test_statistic) 
    #
    boot_stat = boot_group_statistic1[1] - boot_group_statistic2[1]
    boot.append(boot_stat)
  
  # finish bootstrap
  boot = np.array(boot)
  mean = np.nanmean(boot,axis=0)
  std = np.nanstd(boot,axis=0)

  pval = np.sum( boot >= np.abs(observed_stat ), axis=0) / boot_num # how often boot sample is more extreme than observed

  AOI = group_statistic[0][0]

  # ! format output 

  # ---------------------------------------------------------------------------- #
  # make a nice table
  pval_copy = np.where (pval < 0.05, '*', '') 
  nice_view_output = np.char.add(observed_stat_percent_change.astype(str), pval_copy)

  nice_view_nih = np.char.add( np.around(group_statistic[0][1],2).astype(str),')')
  nice_view_nih = np.char.add(' (',nice_view_nih)
  
  nice_view_output = np.char.add(nice_view_output , nice_view_nih)

  nice_view_output = pd.DataFrame(nice_view_output, columns=tobii_metrics, index=AOI) 
  
  # ---------------------------------------------------------------------------- #
  
  observed_stat = pd.DataFrame(observed_stat, columns=tobii_metrics, index=AOI) # ! matrix size: num_aoi x num_tobii_metric
  observed_stat_percent_change = pd.DataFrame(observed_stat_percent_change, columns=tobii_metrics, index=AOI)
  pval = pd.DataFrame(pval, columns=tobii_metrics, index=AOI)
  mean = pd.DataFrame(mean, columns=tobii_metrics, index=AOI)
  std = pd.DataFrame(std, columns=tobii_metrics, index=AOI)
  
  return nice_view_output, observed_stat, pval, group_statistic, boot, mean, std, AOI, observed_stat_percent_change


def many_df_to_csv (args,df_list,header): 
  fout = open(args.outname,'w')
  for index,d in enumerate(df_list):
    fout.write('\n'+header[index])
    fout.write(d.to_string())
    fout.write('\n')
  fout.close()


def df_to_long_csv (args,df_list,header): 
  # https://stackoverflow.com/questions/36537945/reshape-wide-to-long-in-pandas
  for index,d in enumerate(df_list):
    d['index'] = d.index
    d = d.reset_index()
    df = pd.melt(d, id_vars='index', value_vars=args.tobii_metrics)
    df['stat_type'] = header[index]
    df['slide1'] = args.slides[0].split()[-1]
    df['slide2'] = args.slides[1].split()[-1]
    df.to_csv(re.sub(r'.csv',header[index]+'.csv',args.outname) , index=None) 


def combine_df_to_csv_to_plot_later (args,df_list,outputname): 
  out = None
  for index,d in enumerate(df_list): 
    d['index'] = d.index
    d = d.reset_index()
    df = pd.melt(d, id_vars='index', value_vars=args.tobii_metrics) # "index,variable,value,slide1,slide2"
    df['slide1'] = args.slides[0].split()[-1]
    df['slide2'] = args.slides[1].split()[-1] # ! should be the same as Slide2 unless we compare 2 different images
    # df['stat_type'] = header[index]
    if out is None: 
      out = df
    else: 
      out = out.merge( df, on="index,variable,slide1,slide2".split(',') )
  # ! jointly append (wide format)
  out.to_csv(re.sub(r'.csv',outputname+'.csv',args.outname) , index=None) 
  
def string_comma_to_list (this_str): 
  if this_str is None: 
    return None
  return [s.strip() for s in this_str.split(',')]

# ---------------------------------------------------------------------------- #


if __name__ == '__main__':
  parser = ArgumentParser()

  parser.add_argument('--csv', type=str,
                        help='')

  parser.add_argument('--outname', type=str,
                        help='')

  parser.add_argument('--test_statistic', type=str, default='mean', 
                        help='')

  parser.add_argument('--boot_num', type=int, default=200, 
                        help='')

  parser.add_argument('--nan_to_0',  action='store_true', default=False,
                        help='')

  parser.add_argument('--tobii_metrics', type=string_comma_to_list,
                        help='')

  parser.add_argument('--slides', type=string_comma_to_list,
                        help='')

  parser.add_argument('--group1', type=string_comma_to_list,
                        help='')

  parser.add_argument('--group2', type=string_comma_to_list,
                        help='')

  parser.add_argument('--col_nan_to_0', type=string_comma_to_list, default=None,
                        help='which col has nan convert to 0') # Duration_of_first_whole_fixation,something,something

  parser.add_argument('--col_zero_to_nan', type=string_comma_to_list, default=None,
                        help='which col has 0 convert to nan') # this will remove the row when computing mean/median

  parser.add_argument('--aoi_to_use', type=string_comma_to_list, default='Chin,Forehead,L_Cheek,L_Ear,L_Eye,Mouth,Nose,R_Cheek,R_Ear,R_Eye',
                        help='which aoi to use')
  
  # ---------------------------------------------------------------------------- #
  args = parser.parse_args()
  for arg in vars(args): # print ... why not
    print (arg, getattr(args, arg))

  # ---------------------------------------------------------------------------- #
  
  df = pd.read_csv ( args.csv )
  df = df.sort_values(['AOI','Participant']).reset_index(drop=True)

  if args.aoi_to_use is not None: 
    df = df [ df["AOI"].isin(args.aoi_to_use) ]
  
  if args.col_nan_to_0 is not None: 
    for col in args.col_nan_to_0: 
      df[col] = df[col].replace(np.nan, 0)

  if args.col_zero_to_nan is not None: # convert 0-->nan will remove the observation when we take mean or median 
    for col in args.col_zero_to_nan: 
      df[col] = df[col].replace(0,np.nan)

  # ---------------------------------------------------------------------------- #

  # change output name based on setting 
  add_to_name = args.test_statistic + 'nan2ze' if args.col_nan_to_0 is not None else args.test_statistic
  add_to_name = add_to_name + 'ze2nan' if args.col_zero_to_nan is not None else add_to_name
  outputname = add_to_name + args.outname.split('/')[-1]
  temp = args.outname.split('/')
  temp = temp[0:(len(temp)-1)]
  args.outname = '/'.join(temp+[outputname])
  print ('output name ', args.outname )
  
  # ---------------------------------------------------------------------------- #
  
  people_names = [args.group1, args.group2]
  nice_view_output, observed_stat, pval, group_statistic, boot, mean, std, AOI, observed_stat_percent_change = do_bootstrap (   df, 
                                                                                image_name=args.slides, 
                                                                                participants=people_names,   
                                                                                tobii_metrics=args.tobii_metrics,
                                                                                args=args,
                                                                                boot_num=args.boot_num)

  
  many_df_to_csv (args, [nice_view_output], ['(Nih-Peter)/Nih,pval<0.05,(Nih)'])
  
  # ! 
  # many_df_to_csv(args, [observed_stat_percent_change, group_statistic[0][3], group_statistic[1][3], observed_stat, pval, mean, std], ['PercentChangeWrtNIH','nih','peter','observed_stat', 'pval', 'boot_mean', 'boot_std'])

  # df_to_long_csv(args, [pval,observed_stat], ['pval','observed_stat'])

  output_to_combine = [pval,
                       observed_stat,
                       observed_stat_percent_change, 
                       group_statistic[0][3], 
                       group_statistic[1][3]]
  
  combine_df_to_csv_to_plot_later (args,output_to_combine,'long-form')
  
  # # ! 
  # df1 = df[ df['Media'].isin([args.slides[0]]) ] # get @participants who saw @image_name
  # df1 = df1[ df1['Participant'].isin(args.group1) ]
  # df2 = df[ df['Media'].isin([args.slides[1]]) ] # get @participants who saw @image_name
  # df2 = df2[ df2['Participant'].isin(args.group2) ]
  # fout = open(re.sub(r'.csv','',args.outname)+'mannwhitneyu.csv','w')
  # for aoi in AOI: 
  #   for met in args.tobii_metrics: 
  #     temp1 = df1[df1['AOI']==aoi][met]
  #     temp2 = df2[df2['AOI']==aoi][met]
  #     if len(temp1)==0 or len(temp2)==0: 
  #       continue
  #     try: 
  #       U1, p = mannwhitneyu (temp1,temp2)
  #       # res = pg.ttest(temp1, temp2)
  #       # print (aoi,met)
  #       # print (res)
  #     except: 
  #       continue
  #     fout.write(aoi+','+met+','+str(p)+'\n')
  # #
  # fout.close()

  


  