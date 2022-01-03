import cv2
import numpy as np

image = cv2.imread('image.png')
height, width, channels = image.shape
output = np.zeros((height, width))

grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

kernel = np.ones((5,5),np.uint8)
dilated = cv2.dilate(grayscale, kernel, iterations = 2)

cv2.imshow('caca', dilated)
cv2.waitKey()

contours, hierarchy = cv2.findContours(
    dilated, 
    cv2.RETR_TREE, 
    cv2.CHAIN_APPROX_SIMPLE
)

cv2.drawContours(
    output, 
    [max(contours, key = cv2.contourArea)], 
    -1, 
    (255, 255, 255),
    thickness = cv2.FILLED
)


cv2.imshow('A', output)
cv2.waitKey()