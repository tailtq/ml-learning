import numpy as np
import math

padding = 1
stride = 1

img = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
img_w_padding = np.pad(img, padding)

filter = np.array([[0, 1, 2], [0, 1, 1], [0, 1, 1]])

filter_shape = filter.shape
img_shape = img.shape

# new shape with
# new_width = ceil((width + padding * 2 - filter_width_size) / stride) + 1
# new_height = ceil((height + padding * 2 - filter_height_size) / stride) + 1
new_shape = (
    math.ceil((img_shape[0] + padding * 2 - filter_shape[0]) / stride) + 1, # new height
    math.ceil((img_shape[1] + padding * 2 - filter_shape[1]) / stride) + 1, # new width
)
feature_map = np.zeros(new_shape)

print("Image with padding")
print(img_w_padding)
print("---")

print("Filter")
print(filter)
print("---")

for h_i in range(new_shape[0]):
    for w_i in range(new_shape[1]):
        stride_h_i = h_i * stride
        stride_w_i = w_i * stride
        receptive_field = img_w_padding[stride_h_i:stride_h_i + filter_shape[0], stride_w_i:stride_w_i + filter_shape[1]]

        feature_map[h_i, w_i] = np.multiply(receptive_field, filter).sum()

print("Feature map")
print(feature_map)
