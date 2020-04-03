import numpy as np
import shutil
import os
import cv2

from pathlib import Path

path = Path('../../../../datasets/camvid/train')
combination_path = path/'combination'
resize_combination_path = path/'combination_320'

(resize_combination_path).mkdir(exist_ok=True)
filenames = os.listdir(str(combination_path))

for filename in filenames:
    file_path = str(combination_path/filename)
    if '_P' in filename:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (320, 240))
    cv2.imwrite(str(resize_combination_path/filename), image)