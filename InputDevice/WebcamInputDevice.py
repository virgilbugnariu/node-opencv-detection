import logging as log

class WebcamInputDevice:
    def __init__(self, deviceName):
        self.deviceName = deviceName
        self.frame = None

    def getFrame(self):
        log.info("Not yet implemented")