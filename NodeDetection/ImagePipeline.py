import logging as log
import cv2
import numpy as np

class ImagePipeline:
    def __init__(self, image):
        self.image = image
        self.rows = image.shape[0]
        self.columns = image.shape[1]

    def run(self):
        contours = self.findContours(self.image)
        morphed = self.morph(contours)
        nodes = self.blobDetection(morphed)

        result = nodes
        return result

    def findContours(self, inputImage):
        log.debug('Pipeline - Find contours running')
        dilated = cv2.dilate(
            inputImage,
            np.ones((5,5), np.uint8),
            iterations = 2
        )

        contours, hierarchy = cv2.findContours(
            dilated,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        shape = np.zeros((self.rows, self.columns))

        cv2.drawContours(
            shape,
            [max(contours, key = cv2.contourArea)],
            -1,
            (255, 255, 255),
            thickness = cv2.FILLED
        )

        return shape

    def morph(self, inputImage):
        log.debug('Pipeline - Morph running')
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (20, 20)
        )

        morphed = cv2.morphologyEx(
            inputImage,
            cv2.MORPH_ELLIPSE,
            kernel,
            iterations = 3
        )

        return morphed

    def blobDetection(self, inputImage):
        params = cv2.SimpleBlobDetector_Params()

        params.filterByColor = False
        params.filterByCircularity = True
        params.filterByConvexity = False
        params.filterByInertia = False

        params.minCircularity = 0.001

        params.filterByArea = True
        params.minArea = 0.001
        params.maxArea = 99999
        params.minDistBetweenBlobs = 0.1

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(inputImage.astype('uint8'))

        log.debug('Found %i nodes.', len(keypoints))

        mainNode = max(keypoints, key = lambda item: item.size)

        secondaryNodes = tuple(
            filter(
                lambda node: node is not mainNode,
                keypoints
            )
        )

        return (
            mainNode,
            secondaryNodes
        )
