
rm(list = ls())

library('metafor')
library('data.table')

data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Heatmap25rExpertVsNonExpert04172023/'



for (what_group in c('Group1')){ # ! 4 possible groups.  ,'Group3','Group4' 'all','Group1','Group2'

  threshold_used = c(110,130,150,70,90,0) # ! threshold used can be changed, but has to match variable @mod 130,150

  mod = c(  
    '-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv', # ! look at experiments ran with different hyperparameters.  
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

  split_img = '' # ! empty
  # split_img = 'Unaff' # ! split the set of images into 2 sets, and do comparision on each set 
  # alim = c(0,.8)
  # split_img = 'Aff' # ! split the set of images into 2 sets, and do comparision on each set 

  # ---------------------------------------------------------------------------- #


  for (i in names(mod_list)) {

    height = 6 # ! set image height to control line spacing
    alim=c(0,.8)

    if (what_group=='Group2'){
      alim=c(-.3,.7)
      height=4
    }

    
    dat = read.csv(paste0(data_path,mod_list[[i]]))

    if (split_img == 'Unaff'){
      dat = dat[dat$condition %like% 'Unaff', ]
      height = 4
    }
    if (split_img == 'Aff'){
      dat = dat[!(dat$condition %like% 'Unaff'), ]
      height = 5
    }


    dat = dat[dat$group_size1>1,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE ???
    dat = dat[dat$group_size2>1,]

    dat = dat[dat$boot_std>0,]
    if (nrow(dat) == 0) {
      next
    }
    # res <- rma(observed_stat, sei=std, data=dat, test="knha", weights=group_size)
    res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

    threshold = threshold_list[[i]]
    if (threshold > 100) {
      threshold_name = 'high'
    } else{
      threshold_name = 'low'
    }

    xlim=c(-.5,1.5) # ! define width of plot

    if (what_group == 'all'){
      what_group_name = 'All'
    }
    if (what_group == 'Group1'){
      what_group_name = 'Successful'
    }
    if (what_group == 'Group2'){
      what_group_name = 'Underperforming'
      xlim=c(-1,1.5)
    }
    # if (what_group = 'Group3'){
    #   what_group_name = 'All'
    # }
    # if (what_group = 'Group4'){
    #   what_group_name = 'All'
    # }

    # ! CHANGE TITLE ACCORDING TO INPUT GROUPS AND SETTING
    this_title = paste ( what_group_name, 'clinicians vs nonclinicians\nIoU threshold', threshold_name )
    # this_title = paste0 ( what_group_name, ' clinicians vs','\nnonclinicians IoU threshold ', threshold_name )

    # ! PLOT
    png(file=paste0(data_path,what_group,'-Expert-NonExpert-IoU-thr',threshold,split_img,'.png'), width = 4.5, height = height, units="in", res=300)

    # @slab removes group name on y-axis, so we see "slide" as y-axis name
    # @xlim sets x-axis width of plot, may need to change depending on how nice we want plot to look visually
    forest(res, slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','IoU [95% CI]')) 
    # forest(res, order="obs", slab=dat$condition, main=this_title, xlim=xlim, alim=alim, header=c('Image','IoU [95% CI]')) 
    dev.off()
  }

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

