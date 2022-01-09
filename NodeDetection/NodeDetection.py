import logging as log
import os
import cv2


from .ImagePipeline import ImagePipeline

class NodeDetection:
    def __init__(self):
        log.debug('NodeDetection class initialized')
        self.loadImage()
        nodePositions = self.runPipeline()

    def loadImage(self):
        log.debug('Loading image')
        originalImage = cv2.imread(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'assets',
                'image.png'
            )
        )

        log.debug('Converting image to grayscale')
        self.image = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

    def runPipeline(self):
        log.debug('Running pipeline')
        pipeline = ImagePipeline(self.image)
        mainNode, secondaryNodes = pipeline.run()

        return (
            mainNode,
            secondaryNodes
        )
