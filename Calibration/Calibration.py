import logging as log
import numpy as np
import cv2

# Test
class Calibration:
    def __init__(self):
        pass

    def getBoundingRectangle(self, image):
        COLUMNS = 10
        ROWS = 7

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
            iterations = 1
        )

        retval, corners = cv2.findChessboardCorners(
            clean.astype('uint8'),
            (COLUMNS, ROWS)
        )

        if not retval:
            log.debug('No checkerboard pattern found')
            return
        
        mainCorners = (
            corners[0][0].tolist(),
            corners[COLUMNS - 1][0].tolist(),
            corners[-1][0].tolist(),
            corners[-COLUMNS][0].tolist()
        )

        return mainCorners
