rm(list = ls())

library('metafor')

saliency_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Compare2Saliency/k20-thresh0.05-pixcut70-seg/'

output_base_name = paste0('sal-','k20-thresh0.05-pixcut70-seg')

# xlim=c(-.4,.8) # works for 'k20-thresh0.05-pixcut70-seg'? 
# alim=c(0,.4)

xlim=c(-.2,.5) # 
alim=c(0,.2)

mod = c(  'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv', 
          # 'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3.csv', 
          'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv'
          # 'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3.csv' 
          )

threshold_used = c(70,110)

# ---------------------------------------------------------------------------- #

mod_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(mod))){
  mod_list [[as.character(i)]] = mod[i] 
  threshold_list [[as.character(i)]] = threshold_used[i]
}

# ---------------------------------------------------------------------------- #

for (i in names(mod_list)) {

  dat = read.csv(paste0(saliency_path,mod_list[i]))

  dat = dat[order(dat$condition),]

  # res <- rma(observed_stat, sei=std, data=dat, test="knha", weights=group_size)
  res <- rma(observed_stat, sei=std, data=dat, test="knha")

  # ---------------------------------------------------------------------------- #

  threshold = threshold_list[[i]]
  if (threshold > 100) {
    threshold_name = 'high'
  } else{
    threshold_name = 'low'
  }
  
  this_title = paste ( 'Successful clinicians vs model\nIoU threshold', threshold_name )
 
  # ! PLOT
  png(file=paste0(saliency_path,output_base_name,threshold,'.png'), width = 4, height = 5, units="in", res=300)

  forest(res, slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','IoU [95% CI]'))

  dev.off()

}

