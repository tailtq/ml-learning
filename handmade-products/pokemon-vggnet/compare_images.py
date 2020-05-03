from skimage.measure import _structural_similarity as ssim
import numpy as np
import glob
import cv2
import os


def mse(image1, image2):
    err = np.sum((image1.astype('float') - image2.astype('float')) ** 2)
    err /= float(image1.shape[0])

    return err


labels = os.listdir('dataset')

print(labels)

for label in labels:
    path = 'dataset/{}/*'.format(label)
    image_paths = sorted(glob.glob(path))
    image_paths_len = len(image_paths)

    for (i, cur_path) in enumerate(image_paths):
        for j in range(i + 1, image_paths_len):
            next_path = image_paths[j]
            image1 = cv2.imread(cur_path)
            image2 = cv2.imread(next_path)

            if image1.shape[0] == image2.shape[0] and image1.shape[1] == image2.shape[1] and image1.shape[2] == image2.shape[2]:
                print(mse(image1, image2), cur_path, next_path)
# image1 = cv2.imread('dataset/charizard/00000033.png')
# image2 = cv2.imread('dataset/charizard/00000049.png')
#
# print(mse(image1, image2))
