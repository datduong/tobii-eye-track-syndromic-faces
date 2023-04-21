
library('ggplot2')


# slide_number = 3
# group_option = 'NihClinicPeterNotClinic' # 'NihClinicPeterNotClinic' # 'NihClinicPeterClinic'
# main_dir = paste0('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/CompareNihPeter/Slide',slide_number,'/')
# csv_input = paste0('meanaoi_metric_all_Slide',slide_number,'_Peter+Nih04072023',group_option,'long-form.csv')


# ---------------------------------------------------------------------------- #

slide_number = 2
group_option = 'NihMetricsManualUniqueDysmorphicAOIs' # 'NihClinicPeterNotClinic' # 'NihClinicPeterClinic'
main_dir = paste0('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/CompareWithinNihManualAoi/Slide',slide_number,'/')
csv_input = paste0('meanaoi_Group1Group2_Slide',slide_number,'_',group_option,'long-form.csv')

# ---------------------------------------------------------------------------- #

df = read.csv(paste0(main_dir,csv_input))
names(df) = c ("aoi","variable","pval","slide1","slide2","observe_diff","percent_diff","value1","value2")    
# output_to_combine = [pval,
#                        observed_stat,
#                        observed_stat_percent_change, 
#                        group_statistic[0][3], 
#                        group_statistic[1][3]]
# "value_x"   "value_y"   "value_x.1" "value_y.1" "value"  


# df = subset( df, df$aoi %in% c('Forehead','L_Eye','R_Eye','Mouth','Nose'))

# ---------------------------------------------------------------------------- #

df = subset( df, df$aoi != 'R_Cheek')
df = subset( df, df$aoi != 'L_Cheek')
df = subset( df, df$aoi != 'Chin')

# ---------------------------------------------------------------------------- #

# df = subset( df, df$variable %in% c('Number_of_whole_fixations','Number_of_Glances','Number_of_Visits','Number_of_saccades_in_AOI','Time_to_first_whole_fixation','Time_to_first_Glance','Time_to_first_Visit'))

df = subset( df, df$variable %in% c('Total_duration_of_fixations','Number_of_whole_fixations','Time_to_first_whole_fixation'))

# ! flip, so it's easy to view ?
# df$percent_diff[ df$variable == 'Time_to_first_whole_fixation' ] = df$percent_diff[ df$variable == 'Time_to_first_whole_fixation' ]  * -1
# df$percent_diff[ df$variable == 'Time_to_first_Glance' ] = df$percent_diff[ df$variable == 'Time_to_first_Glance' ]  * -1

# ! use only "whole fixation" ?
# "Number_of_whole_fixations,Time_to_first_whole_fixation,Duration_of_first_whole_fixation,Number_of_Glances,Time_to_first_Glance,Duration_of_first_Glance"
# df = subset( df, df$variable != 'Number_of_Glances')
# df = subset( df, df$variable != 'Time_to_first_Glance')
# df = subset( df, df$variable != 'Duration_of_first_Glance')

# ---------------------------------------------------------------------------- #

# https://r-graphics.org/recipe-bar-graph-adjust-width
# https://stackoverflow.com/questions/69936965/how-to-add-an-asterix-significance-above-specific-bars-in-faceted-bar-graph-g

p = ggplot(df, aes(x=aoi, y=percent_diff, fill=as.factor(variable) )) + 
  geom_col(width = 0.7, position=position_dodge2(preserve = "single")) +
  geom_text(aes(label = ifelse(pval<0.05, "*", ""), group = variable), 
            position = position_dodge(width = .7), vjust=.3, size = 20 / .pt) + 
  scale_fill_discrete(name="Metric" ) +
  theme_bw(base_size = 14) +
  theme(legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 14), plot.title = element_text(hjust = 0.5, size=14), axis.text.x = element_text(angle = 30, vjust = 0.5, hjust=0.25) ) +
  labs(title = paste('Slide',slide_number,group_option)) +
  ylab('(Acc-NotAcc) / Acc') 

png(file=paste0(main_dir,slide_number,'_',group_option,'.png'), width=9.5, height=4, units="in", res=720)
p
dev.off()

# breaks=c('Number_of_whole_fixations','Time_to_first_whole_fixation','Duration_of_first_whole_fixation','Total_duration_of_whole_fixations' )

# ---------------------------------------------------------------------------- #

# df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/Peter+Nih04072023NihClinicPeterClinic.csv')
# df = subset(df, df$AOI != 'Aggregated AOI 1')
# df = subset (df, df$Media != 'Slide 1')

# # ---------------------------------------------------------------------------- #

# # slide_number = 'Slide 11' # 'Slide 11' 2
# # df = subset (df, df$Media==slide_number)
# slide_number = ''

# Time_to_first_whole_fixation<-ggplot(df, aes(x=as.factor(AOI), y=Time_to_first_whole_fixation, fill=as.factor(where_from))) +
#   geom_boxplot(position=position_dodge2(preserve = "single")) +
#   theme_bw(base_size = 16) +
#   theme(legend.position = 'bottom', legend.direction = "horizontal", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) , legend.title = element_blank(), axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1) ) +
#   labs(title = paste (slide_number, 'Time_to_first_whole_fixation')) +
#   ylab('Milisec') + facet_wrap(~Media, ncol = 4)


# Time_to_first_whole_fixation




