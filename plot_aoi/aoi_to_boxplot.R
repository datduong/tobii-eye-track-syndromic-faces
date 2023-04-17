

# ! make simple boxplot showing "range" of time spent at an aoi. 


library('ggplot2')
library('ggpubr')
library('coin')
library('EnvStats')

df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter+Nih04072023NihClinicPeterClinic.csv')


# ---------------------------------------------------------------------------- #

slide_number = 'Slide 11' # 'Slide 11' 2

df_wrt_slide = subset (df, df$Media==slide_number)
Time_to_first_whole_fixation<-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Time_to_first_whole_fixation, fill=as.factor(where_from))) +
  geom_boxplot(position=position_dodge(1)) +
  theme_bw(base_size = 16) +
  theme(legend.position = 'bottom', legend.direction = "horizontal", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
  labs(title = paste (slide_number, 'Time_to_first_whole_fixation')) +
  ylab('Milisec') 

Time_to_first_whole_fixation


# # ---------------------------------------------------------------------------- #

# df_wrt_slide = subset (df, df$TOI==slide_number)
# p_Time_to_first_fixation<-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Time_to_first_fixation)) +
#   geom_boxplot(position=position_dodge(1)) +
#   theme_bw(base_size = 16) +
#   theme(legend.position = 'bottom', legend.direction = "horizontal", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
#   labs(title = paste (slide_number, 'Time_to_first_fixation')) +
#   ylab('Milisec') 

# p_Time_to_first_fixation

# ggarrange(p_Time_to_first_fixation, p_Total_duration_of_fixations,  common.legend = TRUE, nrow = 2, ncol=1)

# # ---------------------------------------------------------------------------- #


# df_wrt_slide = subset (df, df$TOI==slide_number)
# p_Number_of_fixations<-ggplot(df_wrt_slide, aes(x=as.factor(AOI), y=Number_of_fixations)) +
#   geom_boxplot(position=position_dodge(1)) +
#   theme_bw(base_size = 16) +
#   theme(legend.position = 'bottom', legend.direction = "horizontal", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
#   labs(title = paste (slide_number, 'Number_of_fixations')) +
#   ylab('Milisec') 

# p_Number_of_fixations

# # ---------------------------------------------------------------------------- #

# ggarrange(p_Time_to_first_fixation, p_Total_duration_of_fixations,  common.legend = TRUE, nrow = 2, ncol=1)


# ---------------------------------------------------------------------------- #

do_test_2_samples = function(df1,df2,colname1,colname2,test_type,remove_0=FALSE) {

  x1 = df1[colname1]
  x2 = df2[colname2]

  if(remove_0){
    x1 = x1[x1>0]
    x2 = x2[x2>0]
  }

  x1 = x1[!is.na(x1)]
  x2 = x2[!is.na(x2)]

  if (test_type=='ttest_mean'){
    test1 = t.test(x1, x2, var.equal = FALSE)
  }

  if (test_type=='permu_median'){
    test1 = twoSamplePermutationTestLocation (x1,x2, fcn = "median", n.permutations = 1000)
  }

  if (test_type=='permu_mean'){
    test1 = twoSamplePermutationTestLocation (x1,x2, fcn = "mean", n.permutations = 1000)
  }

  test1 = t(data.frame(c(test1$p.value,test1$estimate)))
  return (test1)
}

slide_number_x = 'Slide 2'
slide_number_y = 'Slide 11'
what_stat = 'mean'
# this_aoi = 'R_Eye'
# 'Chin',
list_aoi = c('Chin','Forehead','L_Cheek','L_Ear','L_Eye','Mouth','Nose','R_Cheek','R_Ear','R_Eye') # L_Ear
list_output = list()
for (this_aoi in list_aoi) {
  print (this_aoi)
  df_wrt_slide_x = subset (df, df$TOI==slide_number_x & df$AOI==this_aoi)
  df_wrt_slide_y = subset (df, df$TOI==slide_number_y & df$AOI==this_aoi)

  if( sum ( ! is.na(df_wrt_slide_x$Time_to_first_fixation) ) < 2 ) {
    next
  }
  if( sum ( ! is.na(df_wrt_slide_y$Time_to_first_fixation) ) < 2 ) {
    next
  }

  if( sum ( ! is.na(df_wrt_slide_x$Time_to_first_whole_fixation) ) < 2 ) {
    next
  }
  if( sum ( ! is.na(df_wrt_slide_y$Time_to_first_whole_fixation) ) < 2 ) {
    next
  }

  temp1 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Time_to_first_fixation','Time_to_first_fixation',paste0('permu_',what_stat),remove_0=TRUE)

  temp2 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Total_duration_of_fixations','Total_duration_of_fixations',paste0('permu_',what_stat),remove_0=TRUE)

  temp3 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Number_of_fixations','Number_of_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  temp4 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Total_duration_of_whole_fixations','Total_duration_of_whole_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  temp5 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Time_to_first_whole_fixation','Time_to_first_whole_fixation',paste0('permu_',what_stat))

  temp6 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Number_of_whole_fixations','Number_of_whole_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  tempfinal = data.frame(rbind(temp1,temp2,temp3,temp4,temp5,temp6))
  tempfinal$AOI = this_aoi

  colnames(tempfinal) = c('pvalue',paste0(what_stat,'_',gsub(' ','',slide_number_x)), paste0(what_stat,'_',gsub(' ','',slide_number_y)), 'AOI')

  rownames(tempfinal) = c('Time_to_first_fixation','Total_duration_of_fixations','Number_of_fixations','Total_duration_of_whole_fixations','Time_to_first_whole_fixation','Number_of_whole_fixations')
  list_output[[this_aoi]] = tempfinal

}
do.call(rbind,list_output)

# ---------------------------------------------------------------------------- #


# ! compare 2 groups 

slide_number_x = 'Slide 11'
slide_number_y = 'Slide 11'
group1 = c('BAF60a','BRD4','CREBBP','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','TCOF1','WHSC1')
# group1 = c('BAF60a','BRD4','EP300','KMT2','LIMK1','PDGFRa','POLR1C','SMAD1','WHSC1')
group2 = c('PTPN11','RIT1','TBX')
what_stat = 'median'
# this_aoi = 'R_Eye'
# 'Chin',
list_aoi = c('Chin','Forehead','L_Cheek','L_Ear','L_Eye','Mouth','Nose','R_Cheek','R_Ear','R_Eye') # L_Ear
list_output = list()
for (this_aoi in list_aoi) {
  print (this_aoi)
  df_wrt_slide_x = subset (df, df$TOI==slide_number_x & df$AOI==this_aoi & df$Participant %in% group1)
  df_wrt_slide_y = subset (df, df$TOI==slide_number_y & df$AOI==this_aoi & df$Participant %in% group2)

  if( sum ( ! is.na(df_wrt_slide_x$Time_to_first_fixation) ) < 2 ) {
    next
  }
  if( sum ( ! is.na(df_wrt_slide_y$Time_to_first_fixation) ) < 2 ) {
    next
  }

  if( sum ( ! is.na(df_wrt_slide_x$Time_to_first_whole_fixation) ) < 2 ) {
    next
  }
  if( sum ( ! is.na(df_wrt_slide_y$Time_to_first_whole_fixation) ) < 2 ) {
    next
  }

  temp1 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Time_to_first_fixation','Time_to_first_fixation',paste0('permu_',what_stat),remove_0=TRUE)

  temp2 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Total_duration_of_fixations','Total_duration_of_fixations',paste0('permu_',what_stat),remove_0=TRUE)

  temp3 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Number_of_fixations','Number_of_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  temp4 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Total_duration_of_whole_fixations','Total_duration_of_whole_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  temp5 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Time_to_first_whole_fixation','Time_to_first_whole_fixation',paste0('permu_',what_stat))

  temp6 = do_test_2_samples(df_wrt_slide_x,df_wrt_slide_y,'Number_of_whole_fixations','Number_of_whole_fixations',paste0('permu_',what_stat),remove_0=FALSE)

  tempfinal = data.frame(rbind(temp1,temp2,temp3,temp4,temp5,temp6))
  tempfinal$AOI = this_aoi

  colnames(tempfinal) = c('pvalue',paste0(what_stat,'_',gsub(' ','',slide_number_x)), paste0(what_stat,'_',gsub(' ','',slide_number_y)), 'AOI')

  rownames(tempfinal) = c('Time_to_first_fixation','Total_duration_of_fixations','Number_of_fixations','Total_duration_of_whole_fixations','Time_to_first_whole_fixation','Number_of_whole_fixations')
  list_output[[this_aoi]] = tempfinal

}
do.call(rbind,list_output)




# ---------------------------------------------------------------------------- #

person_number = 'BAF60a'
df_wrt_person = subset (df, df$Participant==person_number)
df_wrt_person = subset (df_wrt_person, df_wrt_person$TOI!='Entire Recording')
# df_wrt_person = subset (df_wrt_person, df_wrt_person$TOI %in% c('Slide 2','Slide 3', 'Slide 4'))
p<-ggplot(df_wrt_person, aes(x=as.factor(AOI), y=Time_to_first_fixation,fill)) +
  geom_boxplot(position=position_dodge(1)) +
  theme_bw(base_size = 18) +
  theme(legend.position = 'bottom', legend.direction = "horizontal", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5) ) +
  labs(title = person_number) +
  ylab('Milisec') 

p
