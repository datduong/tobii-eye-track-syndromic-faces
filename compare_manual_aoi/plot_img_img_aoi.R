
library('ggplot2')
library('plotly')

df = read.csv('C:/Users/duongdb/Documents/TOBII_DATA_PATH/img_img_aoi_pval.csv')
slide_number=11
df_wrt_slide = subset (df, df$slide1==slide_number)
df_wrt_slide = df_wrt_slide[df_wrt_slide$value>0,]
df_wrt_slide = df_wrt_slide[df_wrt_slide$value<1,]

df_wrt_slide = df_wrt_slide[df_wrt_slide$variable=='Time_to_first_whole_fixation',]

df_wrt_slide$value = -1*log(df_wrt_slide$value)

p_Total_duration_of_fixations<-ggplot(df_wrt_slide, aes(x=as.factor(slide2), y=value, color=as.factor(index))) +
  # geom_point(size=4) +
  geom_jitter(width=0.25, size=4) +
  theme_bw(base_size = 16) +
  theme(legend.position = 'left', legend.direction = "vertical", axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14) ) +
  labs(title = paste (slide_number, '')) +
  ylab('pval') 

# p_Total_duration_of_fixations
# shape=as.factor(variable)
# position=position_dodge(1)

ggplotly(p_Total_duration_of_fixations)
