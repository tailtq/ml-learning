from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
from imutils import contours as cnts

import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path of the image to be scanned')
args = vars(ap.parse_args())

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

img = cv2.imread(args['image'])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*peri, True)

    if len(approx) == 4:
        screenContour = approx
        break

# cv2.drawContours(img, [screenContour], -1, (0, 255, 0), 2)

warped_img = four_point_transform(img, screenContour.reshape(4, 2))
warped = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method='gaussian')
warped = (warped > T).astype('uint8') * 255

# cv2.imshow('Image', warped_img)
# cv2.imshow('Grayscale image', warped)
# cv2.waitKey(0)

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
questionContours = []

for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    ar = w / float(h)

    if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
        questionContours.append(contour)
        # cv2.drawContours(warped_img, [contour], -1, (0, 0, 255), 2)

questionContours = cnts.sort_contours(questionContours, method='top-to-bottom')[0]
correct = 0

for (q, i) in enumerate(np.arange(0, len(questionContours), 5)):
    contours = cnts.sort_contours(questionContours[i:i + 5])[0]
    bubbled = None

    for (j, contour) in enumerate(contours):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [contour], -1, 255, -1)

        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)

        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)

    color = (0, 0, 255)
    k = ANSWER_KEY[q]

    if k == bubbled[1]:
        color = (0, 255, 0)
        correct += 1

    cv2.drawContours(warped_img, [contours[k]], -1, color, 3)

cv2.imshow('Image', warped_img)
cv2.waitKey(0)
