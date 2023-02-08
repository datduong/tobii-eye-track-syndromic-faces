

library('metafor')

dat = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/example_meta.csv')

res <- rma(obs_stat, sei=boot_std, data=dat, test="knha")

forest(res, slab=paste(dat$group_name1,dat$group_name2, sep = ","))


forest(dat$obs_stat, sei=dat$boot_std, slab=paste(dat$group_name1,dat$group_name2, sep = ","), refline=0)



# forest(x, vi, sei, ci.lb, ci.ub)
#        annotate=TRUE, showweights=FALSE, header=FALSE,
#        xlim, alim, olim, ylim, at, steps=5,
#        level=95, refline=0, digits=2L, width,
#        xlab, slab, ilab, ilab.xpos, ilab.pos,
#        order, subset, transf, atransf, targs, rows,
#        efac=1, pch, psize, plim=c(0.5,1.5), col,
#        lty, fonts, cex, cex.lab, cex.axis, ...)