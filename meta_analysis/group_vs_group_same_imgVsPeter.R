

library('metafor')

data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023/'

what_group = 'all' # ! 4 possible groups. 

threshold_used = c(110,130,150,70,90,0) # ! threshold used can be changed, but has to match variable @mod

mod = c(  
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv',  
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3.csv', 
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3.csv',  
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv',  
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3.csv', 
  '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3.csv'                                                     
)

mod = paste0 (what_group,mod) # add the name @what_group to @mod

# ---------------------------------------------------------------------------- #

mod_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(mod))){
  mod_list [[as.character(i)]] = mod[i] 
  threshold_list [[as.character(i)]] = threshold_used[i]
}

# ---------------------------------------------------------------------------- #

for (i in names(mod_list)) {

  dat = read.csv(paste0(data_path,mod_list[[i]]))

  # dat = dat[dat$group_size1>1,]
  # dat = dat[dat$group_size2>1,]

  # res <- rma(observed_stat, sei=std, data=dat, test="knha", weights=group_size)
  res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

  threshold = threshold_list[[i]]

  # ! CHANGE TITLE ACCORDING TO INPUT GROUPS AND SETTING
  # this_title = paste ( 'NIH vs. Peter Participants correctly identify\nimage as affected, IoU, threshold', threshold )
  this_title = paste ( what_group, 'Expert vs. Non Expert Participants\nIoU, threshold', threshold )

  # ! PLOT
  png(file=paste0(data_path,what_group,'-Expert-NonExpert-IoU-thr',threshold,'.png'))

  # @slab removes group name on y-axis, so we see "slide" as y-axis name
  # @xlim sets x-axis width of plot, may need to change depending on how nice we want plot to look visually
  forest(res, slab=paste(gsub(what_group,'', dat$group_name1 ) , sep = ","), main=this_title, xlim=c(-.4,1.25)) 

  dev.off()
}


# ---------------------------------------------------------------------------- #

# forest(dat$observed_stat, sei=dat$std, slab=paste(dat$tobii, sep = ","), refline=0) alim=c(-0.05,0.55)
# forest(x, vi, sei, ci.lb, ci.ub)
#        annotate=TRUE, showweights=FALSE, header=FALSE,
#        xlim, alim, olim, ylim, at, steps=5,
#        level=95, refline=0, digits=2L, width,
#        xlab, slab, ilab, ilab.xpos, ilab.pos,
#        order, subset, transf, atransf, targs, rows,
#        efac=1, pch, psize, plim=c(0.5,1.5), col,
#        lty, fonts, cex, cex.lab, cex.axis, ...)

