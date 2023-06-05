

# ! make simple boxplot showing "range" of time spent at an aoi. 


library('ggplot2')
library('ggpubr')
library('coin')
library('EnvStats')

data_path = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-manual05012023/'
df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-manual05012023/Peter+Nih05012023.csv')

# ---------------------------------------------------------------------------- #

slide_number = 'Slide 2' 

expert_correct = 'BRD4,CREBBP,EP300,G10,G17,G19,G27,G29,G8,KMT2,LIMK1,PTPN11,RAD21,RIT1,TCOF1,WHSC1'

expert_incorrect = 'BAF60a,G11,GTF2I,SMAD1,TBX1'

nonexpert_correct = 'G13,G15,G21,G22,G23,G24,G26,G28,G4,G9'

nonexpert_incorrect = 'G12,G14,G16,G18,G1,G20,G25,G2,G3,G5,G6,G7'

# ---------------------------------------------------------------------------- #

expert_correct = unlist(strsplit(expert_correct,","))
nonexpert_correct = unlist(strsplit(nonexpert_correct,","))

expert_incorrect = unlist(strsplit(expert_incorrect,","))
nonexpert_incorrect = unlist(strsplit(nonexpert_incorrect,","))

# ---------------------------------------------------------------------------- #

df_wrt_slide = subset (df, df$Media==slide_number)

df_wrt_slide_expert = subset (df_wrt_slide, df_wrt_slide$Participant %in% expert_correct )
df_wrt_slide_expert$ParticipantType = 'expert_correct'

df_wrt_slide_nonexpert = subset (df_wrt_slide, df_wrt_slide$Participant %in% nonexpert_correct )
df_wrt_slide_nonexpert$ParticipantType = 'nonexpert_correct'

df_wrt_slide_expert_incorrect = subset (df_wrt_slide, df_wrt_slide$Participant %in% expert_incorrect )
df_wrt_slide_expert_incorrect$ParticipantType = 'expert_incorrect'

df_wrt_slide_nonexpert_incorrect = subset (df_wrt_slide, df_wrt_slide$Participant %in% nonexpert_incorrect )
df_wrt_slide_nonexpert_incorrect$ParticipantType = 'nonexpert_incorrect'

df_wrt_slide = rbind (df_wrt_slide_expert, df_wrt_slide_nonexpert, df_wrt_slide_expert_incorrect, df_wrt_slide_nonexpert_incorrect)


# ---------------------------------------------------------------------------- #

# Time_to_first_whole_fixation Total_duration_of_fixations

thisplot <-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Total_duration_of_fixations, fill=as.factor(ParticipantType))) +
  geom_boxplot(position=position_dodge2(padding = 0.3, preserve='single')) +
  geom_point(position = position_jitterdodge()) +
  theme_bw(base_size = 16) +
  theme(legend.title = element_blank(), legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
  labs(title = paste ('Total_duration_of_fixations')) +
  ylab('Millisecond') 

png(file=paste0(data_path,gsub(' ','',slide_number),'TotDuration-Expert-NonExpert.png'),width = 720, height = 400,
    units = "px")
thisplot
dev.off()


thisplot <-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Time_to_first_whole_fixation, fill=as.factor(ParticipantType))) +
  geom_boxplot(position=position_dodge2(padding = 0.3, preserve='single')) +
  geom_point(position = position_jitterdodge()) +
  theme_bw(base_size = 16) +
  theme(legend.title = element_blank(), legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
  labs(title = paste ('Time_to_first_whole_fixation')) +
  ylab('Millisecond') 

png(file=paste0(data_path,gsub(' ','',slide_number),'FirstWholeFix-Expert-NonExpert.png'),width = 720, height = 400,
    units = "px")
thisplot
dev.off()


