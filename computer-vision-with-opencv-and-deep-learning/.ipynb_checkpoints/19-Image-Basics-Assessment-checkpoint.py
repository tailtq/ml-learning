import numpy as np
import cv2

image = cv2.imread('course/DATA/dog_backpack.jpg')

fix_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(fix_image, (x, y), 50, color=(0, 0, 255), thickness=10)
    
cv2.namedWindow('my_drawing')

cv2.setMouseCallback('my_drawing', draw_circle)

while True:
    cv2.imshow('my_drawing', fix_image)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
        
cv2.destroyAllWindows()