import numpy as np
import shutil
import os
import cv2
import glob

from pathlib import Path

files = glob.glob('../../../../datasets/camvid/train/images/*.png')

for file in files:
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image[:704, :, :]
    cv2.imwrite(file, image)
    
    
files = glob.glob('../../../../datasets/camvid/train/labels/*.png')

for file in files:
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    image = image[:704, :]
    cv2.imwrite(file, image)