import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


image = cv2.imread(args['image'])
image = cv2.resize(image, (int(image.shape[1] / 2), int(image.shape[0] / 2)))
cv2.imshow('Original', image)

cv2.imshow('Resized (Width)', resize(image, width=200))
cv2.waitKey(0)
