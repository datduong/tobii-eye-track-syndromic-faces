import cv2
import json
import numpy as np
import pandas as pd
import os
from pathlib import Path
import pickle
from PIL import Image, ImageDraw
import sys

import matplotlib.pyplot as plt

img = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide 2 7s BAF60a CTOI.png'
foutname = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Slide 2 7s BAF60a CTOI_trim1080.png'
img = Image.open(img)
img = img.crop((420,0,1500,1080))
img = img.resize((720,720))
img.save(os.path.join(foutname))
