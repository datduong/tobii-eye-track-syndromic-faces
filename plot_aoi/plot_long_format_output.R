
library('ggplot2')

df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/AOI-default03232023/aoi_trajectory_Slide11_Group1_peterclinicianlong-format.csv')

# output_to_combine = [pval,
#                        observed_stat,
#                        observed_stat_percent_change, 
#                        group_statistic[0][3], 
#                        group_statistic[1][3]]

# "value_x"   "value_y"   "value_x.1" "value_y.1" "value"  

names(df) = c ("aoi","variable","pval","slide1","slide2","observe_diff","percent_diff","value1","value2")    

# ---------------------------------------------------------------------------- #

df = subset( df, df$aoi != 'R_Cheek')
df = subset( df, df$aoi != 'L_Cheek')

# ---------------------------------------------------------------------------- #

# https://r-graphics.org/recipe-bar-graph-adjust-width
# https://stackoverflow.com/questions/69936965/how-to-add-an-asterix-significance-above-specific-bars-in-faceted-bar-graph-g

p = ggplot(df, aes(x=aoi, y=percent_diff, fill=as.factor(variable) )) + 
  geom_col(width = 0.7, position=position_dodge2(preserve = "single")) +
  geom_text(aes(label = ifelse(pval<0.05, "*", ""), group = variable), 
            position = position_dodge(width = .7), vjust=.3, size = 20 / .pt) + 
  scale_fill_discrete(name="Metric") +
  theme_bw(base_size = 16) +
  theme(legend.position = 'right', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
  labs(title = '') +
  ylab('(NIH-Peter) / NIH') 


