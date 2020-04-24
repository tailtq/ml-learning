from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2


def show_image(image, screen_name='Test'):
    cv2.imshow(screen_name, image)
    cv2.waitKey(0)


ap = argparse.ArgumentParser()
ap.add_argument('-p', '--shape-predictor', required=True, help='path to facial landmark predictor')
ap.add_argument('-i', '--image', required=True, help='path to input image')
args = vars(ap.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args['shape_predictor'])

image = cv2.imread(args['image'])
orig = image.copy()
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rects = detector(gray, 1)

# rects = face_utils.rect_to_bb(list(rects)[0])
# cv2.rectangle(image, (rects[0], rects[1]), (rects[0] + rects[2], rects[1] + rects[3]), (0, 255, 0), 2)
# show_image(image)

for (i, rect) in enumerate(rects):
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(image, 'Face #{}'.format(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

show_image(image, 'Output')
