

library('metafor')

dat = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/all_img_nonexpgroup_heatmap_vs_heatmap_long.csv')

expert_or_not = 'Nonclinicians' # ! Clinicians OR Nonclinicians CHANGE THIS IF NEEDED

fout_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/'


mod = c(  'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave70.0-round0.3',
          'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave90.0-round0.3', 
          'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave110.0-round0.3'
          # 'k0-thresh0.0-cutbfscale10.0-avepix0.3-smoothave-pixcutave130.0-round0.3' 
          )


threshold_used = c(70,90,110) # ! 

mod_list = list() # put everything into a list (this is like a dictionary in python)
threshold_list = list() 
for (i in c(1:length(mod))){
  mod_list [[as.character(i)]] = mod[i] 
  threshold_list [[as.character(i)]] = threshold_used[i]
}

# ---------------------------------------------------------------------------- #

for (group in c("1,2") ) { # , "2,3", "2,4", "3,4"


  for (i in names(mod_list)) {

    this_df = subset(dat, dat$type==mod_list[[i]])
    this_df = this_df [this_df$group==group, ]

    this_df = this_df[this_df$group_size1>0,] # ! AVOID CASES WHERE WE HAVE JUST 1 PARTICIPANT ANSWERING CORRECTLY. HIGHLY UNSTABLE ???
    this_df = this_df[this_df$group_size2>0,]
    # print (mod[i])
    # print (this_df)

    # ---------------------------------------------------------------------------- #
    
    res <- rma(obs_stat, sei=boot_std, data=this_df, test="knha")

    # ---------------------------------------------------------------------------- #

    threshold = threshold_list[[i]]

    if (threshold > 100) {
      threshold_name = 'high'
    } else{
      threshold_name = 'low'
    }

    this_title = paste0 ( 'Successful vs underperforming\n', expert_or_not, ' IoU threshold ', threshold_name )

    # ---------------------------------------------------------------------------- #

    # ! PLOT
    png(file=paste0(fout_path,'Group1-Group2-IoU-thr',threshold,'.png'), width = 4.5, height = 6, units="in", res=300)

    forest(res, slab=paste(gsub('Group1','', this_df$condition ) , sep = ","), main=this_title, xlim=c(-.5,1.5)) # alim=c(-0.05,0.45), xlim=c(-.25,.75)

    dev.off()

  }

}

