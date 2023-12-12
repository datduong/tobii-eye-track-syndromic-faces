
rm(list = ls())

library('metafor')
library('data.table')


data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'
folder_path = 'KL-symmetric/ExpvModelResult'

# ---------------------------------------------------------------------------- #
# # ! KL divergence within the same participant, when we compare affected vs unaffected heatmap for this person

file_name = c('Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-kl-name.csv',
              'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-kl-name.csv')

xlim=c(-6,40) # ! define width of plot
alim=c(5,20)
# height = 5 # ! when look at all slides
height= 4.5 # ! if remove RSTS1? 



# ---------------------------------------------------------------------------- #

# ! read in IoU 
# file_name = c('Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv',
#               'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv')

# xlim=c(-.4,1) # ! adjusting the size of the plot
# alim=c(0,.4) # ! change for KL divergence?
# height = 5 # ! when look at all slides
# height= 4.5 # ! if remove RSTS1? 


# ---------------------------------------------------------------------------- #

data_path = paste0(data_path,folder_path)

threshold_used = c('low','high')


file_name_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(file_name))){
  file_name_list [[i]] = file_name[i] 
  threshold_list [[i]] = threshold_used[i]
}




for (index in c(1:length(file_name))){

  dat = read.csv(paste0(data_path,'/',file_name_list[[index]]))

  dat = dat[dat$group_size>0,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE ???

  dat = subset (dat, dat$condition != 'RSTS1') # ! remove because of low prediction accuracy by deep learning classifier 

  dat = dat[order(dat$condition),] # ! rank in alphabet

  # dat = dat[dat$boot_std>0,]
  # if (nrow(dat) == 0) {
  #   next
  # }

  # res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

  res <- rma(new_stat, sei=std, data=dat, test="knha")

  # ! CHANGE TITLE ACCORDING TO INPUT GROUPS AND SETTING
  this_title = paste ( 'Successful clinicians vs model\nKL threshold', threshold_list[[index]] ) # ! change if needed. 

  # this_title = paste ( 'Successful clinicians vs model\nIoU threshold', threshold_list[[index]] ) # ! change if needed. 

  # ! PLOT
  # ! RemoveRSTS1

  png(file=paste0(data_path,'/SuccClinic-KL-thr',threshold_list[[index]],'RemoveRSTS1.png'), width = 4, height = height, units="in", res=300)

  # png(file=paste0(data_path,'/SuccClinic-IoU-thr',threshold_list[[index]],'RemoveRSTS1.png'), width = 4, height = height, units="in", res=300)


  # @slab removes group name on y-axis, so we see "slide" as y-axis name
  # @xlim sets x-axis width of plot, may need to change depending on how nice we want plot to look visually

  forest(res, slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','KL [95% CI]'), refline=NA) 

  # forest(res, slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','IoU [95% CI]')) 

  dev.off()

}

