
import os,sys,re,pickle
import numpy as np
import pandas as pd 


image_source = 'C:/Users/duongdb/Documents/TOBII_DATA_PATH/Peter25radiusTobiiHeatmap'
img = [i.split(' ')[-1] for i in os.listdir(image_source)]

