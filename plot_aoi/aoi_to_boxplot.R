

# ! make simple boxplot showing "range" of time spent at an aoi. 


library('ggplot2')
library('ggpubr')
library('coin')
library('EnvStats')

# ---------------------------------------------------------------------------- #

get_user_list = function(expert_level_path, which_group) {
  this_path = paste0( expert_level_path, 
                      gsub(' ','',slide_number) ,
                      '/', which_group) 
  if (! dir.exists(this_path)) {
    return (NULL)
  }
  this_path = list.files ( this_path )

  user = NULL
  for (i in this_path) {
    this_i = unlist ( strsplit( i, '_') ) [2]
    if (is.null (user)){
      user = this_i
    } else {
      user = c(user,this_i)
    }
  }

  return ( user )
}

# get_user_list ('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/','Group1')


# ---------------------------------------------------------------------------- #

data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-manual05012023/'
df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-manual05012023/Peter+Nih05012023.csv')

# ---------------------------------------------------------------------------- #


for (this_slide_number in (c(2,4,6,8,9,11,12,14,15,17))) {

  slide_number = paste ('Slide',this_slide_number)  

  # ---------------------------------------------------------------------------- #

  expert_correct = get_user_list ('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/','Group1')
  nonexpert_correct = get_user_list ('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/','Group1')

  expert_incorrect = get_user_list ('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/','Group2')
  nonexpert_incorrect = get_user_list ('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rNonExpertNoAveByAcc04172023/','Group2')

  # ---------------------------------------------------------------------------- #

  df_wrt_slide = subset (df, df$Media==slide_number)
  print (nrow(df_wrt_slide))

  df_wrt_slide_expert = subset (df_wrt_slide, df_wrt_slide$Participant %in% expert_correct )
  if (nrow(df_wrt_slide_expert) > 0) {
    df_wrt_slide_expert$ParticipantType = 'successful clinicians'
  }

  df_wrt_slide_nonexpert = subset (df_wrt_slide, df_wrt_slide$Participant %in% nonexpert_correct )
  if (nrow(df_wrt_slide_nonexpert) > 0){
    df_wrt_slide_nonexpert$ParticipantType = 'successful non-clinicians'
  }

  df_wrt_slide_expert_incorrect = subset (df_wrt_slide, df_wrt_slide$Participant %in% expert_incorrect )
  if (nrow(df_wrt_slide_expert_incorrect) > 0){
    df_wrt_slide_expert_incorrect$ParticipantType = 'underperforming clinicians'
  }

  df_wrt_slide_nonexpert_incorrect = subset (df_wrt_slide, df_wrt_slide$Participant %in% nonexpert_incorrect )
  if (nrow(df_wrt_slide_nonexpert_incorrect) > 0){
    df_wrt_slide_nonexpert_incorrect$ParticipantType = 'underperforming non-clinicians'
  }

  df_wrt_slide = rbind (df_wrt_slide_expert, df_wrt_slide_nonexpert, df_wrt_slide_expert_incorrect, df_wrt_slide_nonexpert_incorrect)


  # ---------------------------------------------------------------------------- #

  # Time_to_first_whole_fixation Total_duration_of_fixations

  thisplot <-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Total_duration_of_fixations, fill=as.factor(ParticipantType))) +
    geom_boxplot(position=position_dodge2(padding = 0.3, preserve='single')) +
    geom_point(position = position_jitterdodge()) +
    theme_bw(base_size = 16) +
    theme(legend.title = element_blank(), legend.text=element_text(size=14), legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
    labs(title = paste ('Total_duration_of_fixations')) +
    ylab('Millisecond') 

  png(file=paste0(data_path,gsub(' ','',slide_number),'TotDuration-Expert-NonExpert.png'),width = 720, height = 400,
      units = "px")
  print (thisplot)
  dev.off()

  # ---------------------------------------------------------------------------- #

  thisplot <-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Time_to_first_whole_fixation, fill=as.factor(ParticipantType))) +
    geom_boxplot(position=position_dodge2(padding = 0.3, preserve='single')) +
    geom_point(position = position_jitterdodge()) +
    theme_bw(base_size = 16) +
    theme(legend.title = element_blank(), legend.text=element_text(size=14), legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
    labs(title = paste ('Time_to_first_whole_fixation')) +
    ylab('Millisecond') 

  png(file=paste0(data_path,gsub(' ','',slide_number),'FirstWholeFix-Expert-NonExpert.png'),width = 720, height = 400,
      units = "px")
  print (thisplot)
  dev.off()

}

