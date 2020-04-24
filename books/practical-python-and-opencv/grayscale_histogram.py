from matplotlib import pyplot as plt
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

fig, ax = plt.subplots(1, 2, figsize=(15, 8))
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

ax[0].imshow(image, cmap='gray')
ax[1].plot(hist)
ax[1].set_title('Grayscale Histogram')
ax[1].set_xlabel('Bins')
ax[1].set_ylabel('# of Pixels')
ax[1].set_xlim([0, 256])

plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
