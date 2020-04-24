import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
cv2.imshow('Original', image)

cropped = image[:, 200:480]
cropped[0:20, 0:20] += 255
cv2.imshow('Taylor Swift face', cropped)
cv2.waitKey(0)
