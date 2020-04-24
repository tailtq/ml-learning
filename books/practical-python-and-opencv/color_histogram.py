from matplotlib import pyplot as plt
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# fig, ax = plt.subplots(1, 2, figsize=(15, 5))
channels = cv2.split(image)
# colors = ('b', 'g', 'r')
#
# ax[0].imshow(image)
# ax[0].axis('off')
#
# for (channel, color) in zip(channels, colors):
#     hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
#     ax[1].plot(hist, color=color)
#     ax[1].set_xlim([0, 256])
#
# ax[1].set_title('Color Histogram')
# ax[1].set_xlabel('Bins')
# ax[1].set_ylabel('# of Pixels')
# plt.show()

fig, ax = plt.subplots(1, 3, figsize=(15, 5))
hist = cv2.calcHist([channels[1], channels[0]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax[0].imshow(hist, interpolation='nearest')
ax[0].set_title('2D Color Histogram for G and B')
plt.colorbar(p)

hist = cv2.calcHist([channels[1], channels[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax[1].imshow(hist, interpolation='nearest')
ax[1].set_title('2D Color Histogram for G and R')
plt.colorbar(p)

hist = cv2.calcHist([channels[0], channels[2]], [0, 1], None, [32, 32], [0, 256, 0, 256])
p = ax[2].imshow(hist, interpolation='nearest')
ax[2].set_title('2D Color Histogram for B and R')
plt.colorbar(p)

plt.show()

print('2D histogram shape: {}, with {} values'.format(hist.shape, hist.flatten().shape[0]))
