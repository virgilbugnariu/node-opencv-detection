import cv2
import logging as log
import os

class FileInputDevice:
    def __init__(self, filePath):
        log.debug('FileInputDevice initialized.')
        log.debug('Filepath %s', filePath)
        self.frame = cv2.imread(filePath)
    """
        Since this is used for debugging purposes, this method has an additional showCalibrationPattern flag
    """
    def getFrame(self, showCalibrationPattern = False):
        if showCalibrationPattern:
            log.debug('Showing test pattern')
            return cv2.imread(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'assets',
                    'image_angle3_calib.png'
                )
            )
        return self.frame