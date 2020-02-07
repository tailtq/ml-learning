import cv2
import numpy as np


def convert_image_for_mnist(gray_image):
    start, end, size = detect_number(gray_image)
    if start is not None:
        gray_image = convert_image(gray_image, start, end, size)
    else:
        gray_image = gray_image.copy()

    return cv2.resize(gray_image, dsize=(28, 28))


def detect_number(image):
    gray_image, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None, None, None

    largest_index = 0
    converted_contours = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        converted_contours.append([(x, y), (x + w, y + h), (w, h)])
        
    for i in range(len(converted_contours)):
        contour = converted_contours[i]
        
        if sum(contour[2]) > sum(converted_contours[largest_index][2]):
            largest_index = i
    
    return converted_contours[largest_index]


def convert_image(image, start, end, size):
    if size[0] > size[1]:
        max_size = size[0]
    else:
        max_size = size[1]
    number = image[start[1]:end[1], start[0]:end[0]]
    
    new_image = np.zeros((max_size + 50, max_size + 50))
    w_position = np.int((new_image.shape[1] - size[0]) / 2)
    h_position = np.int((new_image.shape[0] - size[1]) / 2)
    
    new_image[h_position:h_position + size[1], w_position:w_position + size[0]] = number
    
    return new_image
