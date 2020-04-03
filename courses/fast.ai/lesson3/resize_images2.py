import numpy as np
import shutil
import os
import cv2
import glob

from pathlib import Path

image_size = (240, 160)
path = Path('../../../../datasets/camvid/train')

images = glob.glob(str(path/'images/*.png'))
images_resize_path = path/('images_' + str(image_size[0]))
images_resize_path.mkdir(exist_ok=True)

labels = glob.glob(str(path/'labels/*.png'))
labels_resize_path = path/('labels_' + str(image_size[0]))
labels_resize_path.mkdir(exist_ok=True)

for image_path in images:
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, image_size)

    filename = os.path.basename(image_path)
    cv2.imwrite(str(images_resize_path/filename), image)


for image_path in labels:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, image_size)

    filename = os.path.basename(image_path).replace('_P', '')
    cv2.imwrite(str(labels_resize_path/filename), image)
