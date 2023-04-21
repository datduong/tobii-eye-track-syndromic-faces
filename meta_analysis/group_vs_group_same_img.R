

library('metafor')



dat = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/all_img_group_heatmap_vs_heatmap_long.csv')
expert_or_not = 'Expert'

fout_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/'

# unique(this_df$type)
# unique(this_df$group)
# [1] "1,2" "2,3" "2,4" "3,4"


mod = c(  'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3',
          'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3', 
          'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3'
          # 'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3' 
          )

# , "2,3", "2,4", "3,4"

for (group in c("1,2") ) {

  for (i in c(1:3)) {

    this_df = subset(dat, dat$type==mod[i])
    this_df = this_df [this_df$group==group, ]

    this_df = this_df[this_df$group_size1>1,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE.  
    this_df = this_df[this_df$group_size2>1,]
    print (mod[i])
    print (this_df)
    res <- rma(obs_stat, sei=boot_std, data=this_df, test="knha")

    if (i==1) { threshold = 70 }
    if (i==2) { threshold = 90 }
    if (i==3) { threshold = 110 }
    # if (i==2) { threshold = 130 }
    this_title = paste ( 'Expert participants', group , 'threshold', threshold )

    # ! PLOT
    png(file=paste0(fout_path,'Group1-Group2-IoU-thr',threshold,'.png'))

    forest(res, slab=paste(gsub('Group1','', this_df$condition ) , sep = ","), main=this_title, xlim=c(-.4,1.25)) # alim=c(-0.05,0.45), xlim=c(-.25,.75)
    dev.off()

  }

}


# forest(this_df$observed_stat, sei=this_df$std, slab=paste(this_df$tobii, sep = ","), refline=0)



# forest(x, vi, sei, ci.lb, ci.ub)
#        annotate=TRUE, showweights=FALSE, header=FALSE,
#        xlim, alim, olim, ylim, at, steps=5,
#        level=95, refline=0, digits=2L, width,
#        xlab, slab, ilab, ilab.xpos, ilab.pos,
#        order, subset, transf, atransf, targs, rows,
#        efac=1, pch, psize, plim=c(0.5,1.5), col,
#        lty, fonts, cex, cex.lab, cex.axis, ...)

