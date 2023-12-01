
import os,sys,re,pickle, time
from datetime import datetime
import numpy as np 

# ! make script to compare 2 groups on the same image. 
# ! may have 1 to 3 groups 

script_base = """

"""

# ---------------------------------------------------------------------------- #

this_k = 10 # 20 # ! lower-->rough shape, higher-->more smooth
cut_seg_to_binary_1 = .5 # ! higher-->more white spot. lower-->less white spot
cut_seg_to_binary_2 = .5 

# ---------------------------------------------------------------------------- #

script_path = '/data/duongdb/Face11CondTobiiEyeTrack01112023'

main_folder = '/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023' # @main_folder is where we save all the output data

# 
slide_folders = ['Slide'+str(s) for s in np.arange(1,18)]

# slide_folders = ['Slide2', 'Slide11', 'Slide6']

# slide_folders = ['Slide1']

# ---------------------------------------------------------------------------- #

# ! for each slide1, slide2 (as a folder)
# ! for each group1, group2 ...

os.chdir(main_folder)

for folder in slide_folders:
  for group in ['all','Group1','Group2','Group3','Group4']: # Group1
    # @group: 
    # Group1 = expert vs nonexpert, participant who answer "correct affected vs not" 
    # Group2 = expert vs nonexpert, participant who answer "incorrect affected vs not" 
    # Group3 = expert vs nonexpert, participant who answer "correct affected vs not" AND say correct disease name  
    # Group2 = expert vs nonexpert, participant who answer "correct affected vs not" BUT say wrong disease name 
    if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023',folder,group)):
      continue
    if not os.path.isdir(os.path.join('/data/duongdb/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023',folder,group)):
      continue
    script = re.sub('THIS_K',str(this_k),script_base)
    script = re.sub('THRESHOLD_GROUP_1',str(cut_seg_to_binary_1),script) # ! note @THRESHOLD_GROUP_1 is NIH
    script = re.sub('THRESHOLD_GROUP_2',str(cut_seg_to_binary_2),script) # ! note @THRESHOLD_GROUP_2 is Peter's participants 
    script = re.sub('SLIDE_NUM',str(folder),script)
    script = re.sub('GROUP1',group,script)
    script = re.sub('GROUP2',group,script)
    #
    time.sleep( 1 )
    now = datetime.now() # current date and time
    # ! make a bunch of bash script
    script_name = os.path.join(script_path,'script4'+'-'+now.strftime("%m-%d-%H-%M-%S")+'.sh')
    fout = open(script_name,'w')
    fout.write(script)
    fout.close()
    # ! @sbatch is used to submit jobs
    os.system('sbatch --time=00:55:00 --mem=4g --cpus-per-task=4 ' + script_name ) 

        
# end
exit() 





