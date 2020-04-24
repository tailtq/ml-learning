import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
cv2.imshow('Original', image)

image_shape = image.shape

mask = np.zeros(image_shape[:2], dtype='uint8')
(cX, cY) = (200, 0)
cv2.rectangle(mask, (cX, cY), (cX + 280, image_shape[0]), 255, -1)
cv2.imshow('Mask', mask)

masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow('Mask applied to image', masked)
cv2.waitKey(0)
