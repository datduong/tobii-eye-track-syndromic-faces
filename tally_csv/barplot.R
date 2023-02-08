library('ggplot2')
library('magrittr') # needs to be run every time you start R and want to use %>%
library('dplyr')    # alternatively, this also loads %>%
library('tidyr')
library('tibble')

df = read.csv('C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/RemoveAveEyeTrack/all_heatmap_vs_heatmap_long.csv')

criteria = 'smoothk10-thresh0.1-avepix0.2-round0.35'

df = df[df['type'] == criteria, ]

# https://stackoverflow.com/questions/38101512/the-same-width-of-the-bars-in-geom-barposition-dodge

g = df %>% 
  as.tibble() %>% 
  mutate_at(c("group", "condition"), as.factor) %>% 
  complete(group,condition)


p = ggplot(data=g, aes(x=condition, y=boot_pval, fill=group)) +
  geom_col(position = position_dodge2(width = 0.9, preserve = "single")) +
  facet_grid(~condition, scales = "free_x", space = "free_x", switch = "x") +  
  theme_bw(base_size = 16) +
  theme(axis.title.x=element_blank(), axis.title.y = element_text(size = 16), plot.title = element_text(hjust = 0.5, size=14),axis.text.x = element_blank(),
        axis.ticks.x=element_blank() ) +
  labs(title = 'Compare groups on same image') +
  ylab('pvalue') 

p

