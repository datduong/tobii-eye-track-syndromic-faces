import os,sys,re,pickle
import pandas as pd
import numpy as np 

from argparse import ArgumentParser
import shutil

# ---------------------------------------------------------------------------- #


parser = ArgumentParser()

parser.add_argument('--main_dir', type=str, default='C:/Users/duongdb/Documents/TOBII_DATA_PATH',
                      help='')

parser.add_argument('--source', type=str,
                      help='name of input image folder')

parser.add_argument('--final_output_dir', type=str,
                      help='name of new image folder')

parser.add_argument('--df', type=str, default=None,
                      help='csv where we keep info on the 4 groups based on their accuracy')

parser.add_argument('--add_file_name_pattern', type=str, default=None, 
                      help='add .png to file name when looking at files to move') # 

parser.add_argument('--clinician_list', type=str, default=None, 
                      help='a list of names like a,b,c,d,e...')

parser.add_argument('--move_only_clinician', action='store_true', default= False, 
                      help='use only clinicians')

parser.add_argument('--move_only_non_clinician', action='store_true', default= False, 
                      help='use only none-clinicians')


# ---------------------------------------------------------------------------- #
args = parser.parse_args()

# ---------------------------------------------------------------------------- #

if args.add_file_name_pattern is None: 
  args.add_file_name_pattern = ''

if args.clinician_list is not None: 
  args.clinician_list = [i.strip() for i in args.clinician_list.split(',')]

if args.move_only_clinician: 
  args.final_output_dir = args.final_output_dir + 'Clinician'

if args.move_only_non_clinician: 
  args.final_output_dir = args.final_output_dir + 'NotClinician'

# ---------------------------------------------------------------------------- #

# main_dir = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/'

# ---------------------------------------------------------------------------- #

# source = '25radius-fix-mismatch-name-csv-no-ave-whtbg' # '25radius-fix-mismatch-name-csv-no-ave-whtbg'
# final_output_dir = 'eye_track_data_without_ave_signal' # eye_track_data_without_ave_signal
# df = 'eye_track_record_accuracy_per_person.csv.csv'
# add_file_name_pattern = '.png'

# ---------------------------------------------------------------------------- #

# source = '25radius-keep-ave-whtbg-nonclinicians' # '25radius-fix-mismatch-name-csv-no-ave-whtbg'
# final_output_dir = 'KeepAveEyeTrackPeter' # eye_track_data_without_ave_signal
# df = 'eye_track_record_accuracy_per_person.csv'

# ---------------------------------------------------------------------------- #

source = os.path.join(args.main_dir,args.source)


if args.df is not None: # ! because data is coming in at different time points, we may not have a final @args.df

  # ---------------------------------------------------------------------------- #

  df = pd.read_csv(os.path.join(args.main_dir,args.df)).fillna('')
  columns = [ 'Syn vs Non Syn Correct',
              'Syn vs Non Syn Incorrect', 	 
              'Syn vs NonSyn Correct Syndrome Name Correct',
              'Syn vs NonSyn Correct Syndrome name Incorrect']

  # ---------------------------------------------------------------------------- #


  # ---------------------------------------------------------------------------- #

  for slide_name in np.arange(1,18) : # np.arange(1,18) : # np.arange(1,18) [17]

    temp_df = df [ df['Image']==slide_name ]
    
    for index, col in enumerate(columns): 
      
      key_name = [i for i in temp_df[col].tolist() if len(i) > 0 ] # ! get all the people codename (like abc, def, ...)
      
      if len(key_name) == 0: 
        continue

      # ! we may want to partition data only with respect to clinician vs not. 
      if args.move_only_clinician: 
        key_name = [i for i in key_name if any ( [ c==i for c in args.clinician_list ] ) ] # match whole word because we can see name G1, and G11.  

      if args.move_only_non_clinician: 
        key_name = [i for i in key_name if not any ( [ c==i for c in args.clinician_list ] ) ] 

      # ! now we check slide name, and also remove images considered "BAD"
      slide_name = str(slide_name)
      
      im = [i for i in os.listdir(source)] # ! copy images
      im = [i for i in im if '_BAD.png' not in i]
      im = [i for i in im if '_Bad.png' not in i]
      im = [i for i in im if '_bad.png' not in i]
      im = [i for i in im if 'BAD.png' not in i]
      im = [i for i in im if 'POLR1C' not in i] # this person data fails. 
    
      im = [i for i in im if re.match(r'^'+slide_name+'_',i) ]

      if len(im) == 0: 
        continue

      # print ('slide', slide_name)
      # print (key_name,'\n',im)
      
      final_dir = os.path.join(args.main_dir,args.final_output_dir,'Slide'+slide_name,'Group'+str(index+1))
      if not os.path.exists(final_dir): 
        os.makedirs(final_dir)

      # if not os.path.exists(os.path.join(final_dir+'OnSlide1')): 
      #   os.makedirs(os.path.join(final_dir+'OnSlide1'))
        
      for i in im: # go over each image... kind of slow... whatever
        for k in key_name: 
          
          # ! peter naming is using 1_G[number].png, we're using "1_[alphabet]_25r"
          # if ('_'+k+'.png') in i : # ! CHECK NAMING CONVENTION... 
          if ('_'+k+args.add_file_name_pattern) in i : # ! CHECK NAMING CONVENTION... 
            
            if os.path.exists ( os.path.join(source,i) ) : 
          
              shutil.copy2 ( os.path.join(source,i), os.path.join(final_dir,i))
              
              # os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))
              # ! move their results from slide 1 --> can later use as baseline 
              # user = i.split('_')[1] # user name 
              # i = '1_'+user+'_25r.png'
              # if os.path.exists(os.path.join(source,i)): 
              #   os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir+'OnSlide1'))



# ---------------------------------------------------------------------------- #

# ! put everyone image in the same folder, because why not ?

for image_id in np.arange(1,18): 
  slide_name = str(image_id)
  im = os.listdir(source)
  im = [i for i in im if re.match(r'^'+slide_name+'_',i) ]

  # ! we may want to partition data only with respect to clinician vs not. 
  if args.move_only_clinician: 
    im = [i for i in im if any ( [ ('_'+c+args.add_file_name_pattern) in i  for c in args.clinician_list ] ) ] 
    
  if args.move_only_non_clinician: 
    im = [i for i in im if not any ( [ ('_'+c+args.add_file_name_pattern) in i  for c in args.clinician_list ] ) ]  

  final_dir = os.path.join(args.main_dir,args.final_output_dir,'Slide'+slide_name,'all')
  if not os.path.exists(final_dir): 
    os.makedirs(final_dir)
    
  #
  for i in im: 
    os.system ('scp ' + os.path.join(source,i) + ' ' + os.path.join(final_dir))


