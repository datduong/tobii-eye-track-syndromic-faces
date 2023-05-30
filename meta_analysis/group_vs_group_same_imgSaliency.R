

library('metafor')


# k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3
# Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-round0.3

mod = c(  'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3.csv', 
          # 'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3.csv', 
          'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3.csv'
          # 'Eb4Occ-k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3.csv' 
          )


for (i in c(1:2)) {

  dat = read.csv(paste0('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/Compare2Saliency/k20-thresh0.05-pixcut20-seg/',mod[i]))

  # res <- rma(observed_stat, sei=std, data=dat, test="knha", weights=group_size)
  res <- rma(observed_stat, sei=std, data=dat, test="knha")

  if (i==1) { threshold = 'low' } # 70
  if (i==2) { threshold = 'high' }
  # if (i==3) { threshold = 'high' }
  # if (i==4) { threshold = 'high' }

  this_title = paste ( 'Successful clincians, threshold', threshold )
  windows() 
  forest(res, slab=paste(gsub('Group1','', dat$tobii ) , sep = ","), main=this_title, alim=c(-0.05,0.35), xlim=c(-.25,.75))

}


# forest(dat$observed_stat, sei=dat$std, slab=paste(dat$tobii, sep = ","), refline=0)



# forest(x, vi, sei, ci.lb, ci.ub)
#        annotate=TRUE, showweights=FALSE, header=FALSE,
#        xlim, alim, olim, ylim, at, steps=5,
#        level=95, refline=0, digits=2L, width,
#        xlab, slab, ilab, ilab.xpos, ilab.pos,
#        order, subset, transf, atransf, targs, rows,
#        efac=1, pch, psize, plim=c(0.5,1.5), col,
#        lty, fonts, cex, cex.lab, cex.axis, ...)

