import logging as log
import json
import os
import cv2
import time

from InputDevice import InputDevice
from InputDevice import InputDevices
from NodeDetection import NodeDetection
from OSCCommunication import OSCCommunication
from Calibration import Calibration
from Parameters import Parameters
class App:
    def __init__(self):
        filePath = os.path.join(
            os.path.dirname(__file__),
            '..',
            'assets',
            'image.png'
        )

        self.inputDevice = InputDevice(InputDevices.FileInputDevice, filePath)

        self.currentFrame = self.inputDevice.device.getFrame()
        self.nodeDetection = NodeDetection()
        self.osc = OSCCommunication()
        self.parameters = Parameters()
        
        self.setCallbacks()

        # This must be the last instruction all the time
        self.osc.init()

    def setCallbacks(self):
        self.osc.dispatcher.map('/getNodesCoords', self.handleGetNodesCoords)
        self.osc.dispatcher.map('/runCalibration', self.handleGetCalibrationRequest)
    
    def handleGetCalibrationRequest(self, channelName, value):
        if value > 0:
            log.debug('Received calibration request')
            calibration = Calibration()
            
            self.osc.client.send_message('/showCalibrationPattern', 1)
            time.sleep(1)

            calibrationFrame = self.inputDevice.device.getFrame(showCalibrationPattern = True)
            rectangle = calibration.getBoundingRectangle(calibrationFrame)

            self.parameters.set('boundingRect', rectangle)
            self.parameters.savePreset()
            
            time.sleep(1)
            self.osc.client.send_message('/showCalibrationPattern', 0)
    
    def handleGetNodesCoords(self, channelName, value):
        log.debug('Running node coords handler')

        if value > 0:
            self.nodeDetection.setImage(self.currentFrame)
            mainNode, secondaryNodes = self.nodeDetection.runPipeline()

            mainNodeData = {
                'position': mainNode.pt,
                'size': mainNode.size
            }

            secondaryNodesData = []

            for node in secondaryNodes:
                secondaryNodesData.append({
                    'position': node.pt,
                    'size': node.size
                })

            message = {
                "mainNode": mainNodeData,
                "secondaryNodes": secondaryNodesData,
                "originalSize": self.nodeDetection.image.shape
            }

            log.debug('Sending nodes coords')
            log.debug(json.dumps(message))
            self.osc.client.send_message('/nodesCoords', json.dumps(message))
