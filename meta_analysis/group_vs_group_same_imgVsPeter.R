

library('metafor')

# mod = c(  
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-diff.csv',                   
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-diff.csv',   
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv',
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-diff.csv',    
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3.csv',
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-diff.csv',    
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3.csv',
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-diff.csv',     
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv', 
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-diff.csv',     
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3.csv', 
#   'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3.csv',               
#   'VsPeter-k0-thresh0.0-diff.csv',                                                      
# )

mod = c(  
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv',  
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3.csv', 
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave150.0-round0.3.csv',  
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv',  
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3.csv', 
  'VsPeter-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3.csv'                                                     
)

for (i in c(1:length((mod)))) {

  dat = read.csv(paste0('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/CompareGroupSameImgVsPeter/',mod[i]))

  # res <- rma(observed_stat, sei=std, data=dat, test="knha", weights=group_size)
  res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

  if (i==1) { threshold = 110 }
  if (i==2) { threshold = 130 }
  if (i==3) { threshold = 150 }
  if (i==4) { threshold = 70 }
  if (i==5) { threshold = 90 }
  if (i==6) { threshold = 0 }

  this_title = paste ( 'NIH vs. Peter Participants correctly identify\nimage as affected, IoU, threshold', threshold )
  windows() 
  forest(res, slab=paste(gsub('Group1','', dat$group_name1 ) , sep = ","), main=this_title, xlim=c(-.4,1.25))

}


# forest(dat$observed_stat, sei=dat$std, slab=paste(dat$tobii, sep = ","), refline=0) alim=c(-0.05,0.55)



# forest(x, vi, sei, ci.lb, ci.ub)
#        annotate=TRUE, showweights=FALSE, header=FALSE,
#        xlim, alim, olim, ylim, at, steps=5,
#        level=95, refline=0, digits=2L, width,
#        xlab, slab, ilab, ilab.xpos, ilab.pos,
#        order, subset, transf, atransf, targs, rows,
#        efac=1, pch, psize, plim=c(0.5,1.5), col,
#        lty, fonts, cex, cex.lab, cex.axis, ...)

