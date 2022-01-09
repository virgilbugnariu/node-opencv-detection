import cv2
import os
import numpy as np

image = None
iterations = 1

def main():
    global image
    
    image = cv2.imread(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'assets',
            'image_angle1_calib.png'
        )
    )
    render()
    

def render():
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    thresholdPassOne = cv2.adaptiveThreshold(
        gray, 
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    cleanKernel = np.ones((1, 1), np.uint8)

    clean = cv2.morphologyEx(
        thresholdPassOne,
        cv2.MORPH_OPEN,
        cleanKernel,
        iterations = iterations
    )
    
    retval, corners = cv2.findChessboardCorners(
        clean.astype('uint8'),
        (10, 7)
    )

    if retval:
        result = cv2.cvtColor(gray.copy(), cv2.COLOR_GRAY2BGR)

        cornerA = corners[0]
        cornerB = corners[9]
        cornerC = corners[-1]
        cornerD = corners[-10]

        points = np.array([
            cornerA[0],
            cornerB[0],
            cornerC[0],
            cornerD[0],
        ], np.int32)

        cv2.polylines(
            result,
            [points],
            True,
            (0, 0, 255)
        )
    else:
        result = gray
        print("No checkerboard found")

    
    cv2.imshow('Pass two', result)
    return

if __name__ == '__main__':
    main()
    while True:
        key = cv2.waitKey()
        if key == 27:
            break
        else:
            iterations += 1
            render()

            continue