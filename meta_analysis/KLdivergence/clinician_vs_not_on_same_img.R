
rm(list = ls())

library('metafor')
library('data.table')

data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/'
folder_path = 'KL-symmetric/Underperforming_clin_vs_nonclin'


data_path = paste0(data_path,folder_path)

what_group_name = 'Underperforming' # Successful Underperforming

threshold_used = c('low','high')
file_name = c('G2vG2-70.0-kl-name.csv',
              'G2vG2-110.0-kl-name.csv')

file_name_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(file_name))){
  file_name_list [[i]] = file_name[i] 
  threshold_list [[i]] = threshold_used[i]
}



# xlim=c(-5,16) # ! define width of plot
# alim=c(0,8)
# height = 6 # ! when look at all slides

xlim=c(-10,36) # ! define width of plot
alim=c(0,18)
height=4 # ! if use underperforming 

split_img = ''

for (index in c(1:length(file_name))){

  dat = read.csv(paste0(data_path,'/',file_name_list[[index]]))

  # ! WE ONLY DO THIS >1 IF THE TOTAL SAMPLE SIZE IS EXTREMELY SMALL, IN 22Q, UNDERPERFORMING HAS 1 AND 3 PEOPLE  
  dat = dat[dat$group_size1>1,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE ???
  dat = dat[dat$group_size2>1,]

  dat = dat[dat$boot_std>0,]
  if (nrow(dat) == 0) {
    next
  }

  if (split_img == 'Unaff'){
      dat = dat[dat$condition %like% 'Unaff', ]
      height = 4
  }
  if (split_img == 'Aff'){
    dat = dat[!(dat$condition %like% 'Unaff'), ]
    height = 5
  }



  res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

  # ! CHANGE TITLE ACCORDING TO INPUT GROUPS AND SETTING
  # this_title = paste ( what_group_name, 'clinicians vs nonclinicians\nKL threshold', threshold_list[[index]] )
  this_title = paste ( what_group_name, 'clinicians vs\nnonclinicians KL threshold', threshold_list[[index]] )

  # ! PLOT
  png(file=paste0(data_path,'/',what_group_name,'-Expert-NonExpert-KL-noisethr',threshold_list[[index]],split_img,'.png'), width = 4.5, height = height, units="in", res=300)

  # @slab removes group name on y-axis, so we see "slide" as y-axis name
  # @xlim sets x-axis width of plot, may need to change depending on how nice we want plot to look visually
  forest(res, order="obs", slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','KL [95% CI]')) 

  dev.off()

}

# slab=dat$condition