import cv2
import numpy as np

windowTitle = 'Playground'
filename = 'image.png'
file = None
output = None
kernel = np.ones((5,5),np.uint8)
grayscale = None

def main():
    global file
    file = cv2.imread(filename)

    cv2.namedWindow(windowTitle)
    cv2.createTrackbar(
        'Erosion',
        windowTitle,
        0, 10,
        onChange
    )
    prepareImage()
    onChange(0)

def prepareImage():
    global output
    global grayscale

    height, width, channels = file.shape
    output = np.zeros((height, width))

    grayscale = cv2.cvtColor(file, cv2.COLOR_RGB2GRAY)
    
    output = cv2.dilate(grayscale, kernel, iterations = 2)


def onChange(val):
    global output
    global file
    global grayscale
    global kernel

    final = file.copy()

    dilated = cv2.dilate(grayscale, kernel, iterations = 2)
    contours, hierarchy = cv2.findContours(
        dilated, 
        cv2.RETR_TREE, 
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        final, 
        [max(contours, key = cv2.contourArea)], 
        -1, 
        (255, 255, 255),
        thickness = cv2.FILLED
    )

    output = cv2.dilate(
        output,
        kernel,
        iterations = val
    )

    cv2.imshow(windowTitle, output)
    
if __name__ == '__main__':
    main()
    cv2.waitKey()