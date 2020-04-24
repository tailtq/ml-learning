import numpy as np
import argparse
import imutils
import cv2


def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image = cv2.resize(image, (int(image.shape[1] / 2), int(image.shape[0] / 2)))
cv2.imshow('Original', image)

cv2.imshow('Rotated by 45 Degrees', rotate(image, 45))
cv2.imshow('Rotated by 90 Degrees', rotate(image, 90))
cv2.waitKey(0)
