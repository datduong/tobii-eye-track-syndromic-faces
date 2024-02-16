
rm(list = ls())

library('metafor')
library('data.table')

# ! KL divergence within the same participant, when we compare affected vs unaffected heatmap for this person


data_path = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/'
folder_path = 'KL-symmetric/NonExpSameParticipant'
expert_or_not = 'Nonclinicians' # ! Clinicians OR Nonclinicians CHANGE THIS IF NEEDED

data_path = paste0(data_path,folder_path)

threshold_used = c('low','high')
file_name = c('NonExpert_participant-70.0-kl-name.csv',
              'NonExpert_participant-110.0-kl-name.csv')

file_name_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(file_name))){
  file_name_list [[i]] = file_name[i] 
  threshold_list [[i]] = threshold_used[i]
}



xlim=c(-7,24) # ! define width of plot
alim=c(0,12)
height = 6 # ! when look at all slides


for (index in c(1:length(file_name))){

  dat = read.csv(paste0(data_path,'/',file_name_list[[index]]))
  dat = dat[dat$group_size1>0,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE ???
  dat = dat[dat$group_size2>0,]

  dat = dat[dat$boot_std>0,]
  if (nrow(dat) == 0) {
    next
  }

  res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

  # ! CHANGE TITLE ACCORDING TO INPUT GROUPS AND SETTING
  this_title = paste0 ( expert_or_not, ', affected vs unaffected\nKL threshold ', threshold_list[[index]] )

  # ! PLOT
  png(file=paste0(data_path,'/',expert_or_not,'-Aff-Unaff-KL-thr',threshold_list[[index]],'.png'), width = 4.5, height = height, units="in", res=300)

  # @slab removes group name on y-axis, so we see "slide" as y-axis name
  # @xlim sets x-axis width of plot, may need to change depending on how nice we want plot to look visually
  forest(res, order="obs", slab=dat$user_id, main=this_title, xlim=xlim, alim=alim, header=c('Participant','KL [95% CI]')) 

  dev.off()

}

