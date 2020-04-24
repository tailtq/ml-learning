from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(pt_a, pt_b):
    return (pt_a[0] + pt_b[0]) / 2, (pt_a[1] + pt_b[1]) / 2


def show_image(win_name, image):
    cv2.imshow(win_name, image)
    cv2.waitKey(0)


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to the input image')
ap.add_argument('-w', '--width', type=float, required=True,
                help='width of the left-most object in the image (in inches)')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

for c in cnts:
    if cv2.contourArea(c) < 100:
        continue

    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype=int)

    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype(int)], -1, (0, 255, 0), 2)

    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    (tl, tr, br, bl) = box
    (tltr_x, tltr_y) = midpoint(tl, tr)
    (blbr_x, blbr_y) = midpoint(bl, br)

    (tlbl_x, tlbl_y) = midpoint(tl, bl)
    (trbr_x, trbr_y) = midpoint(tr, br)

    cv2.circle(orig, (int(tltr_x), int(tltr_y)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbr_x), int(blbr_y)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlbl_x), int(tlbl_y)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbr_x), int(trbr_y)), 5, (255, 0, 0), -1)

    cv2.line(orig, (int(tltr_x), int(tltr_y)), (int(blbr_x), int(blbr_y)), (255, 0, 255), 2)
    cv2.line(orig, (int(tlbl_x), int(tlbl_y)), (int(trbr_x), int(trbr_y)), (255, 0, 255), 2)

    dA = dist.euclidean((tltr_x, tltr_y), (blbr_x, blbr_y))
    dB = dist.euclidean((tlbl_x, tlbl_y), (trbr_x, trbr_y))

    if pixelsPerMetric is None:
        pixelsPerMetric = dB / args['width']

    # compute the size of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric
    # draw the object sizes on the image
    cv2.putText(orig, '{:.1f}cm'.format(dimA),
                (int(tltr_x - 15), int(tltr_y - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
    cv2.putText(orig, '{:.1f}cm'.format(dimB),
                (int(trbr_x + 10), int(trbr_y)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)

    show_image('Test', orig)
