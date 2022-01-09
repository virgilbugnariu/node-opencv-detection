import logging as log
import json

from NodeDetection import NodeDetection
from OSCCommunication import OSCCommunication

class App:
    def __init__(self):
        self.nodeDetection = NodeDetection()
        self.osc = OSCCommunication()
        
        self.setCallbacks()
        self.osc.init()

    def setCallbacks(self):
        self.osc.dispatcher.map('/getNodesCoords', self.handleGetNodesCoords)
    
    def handleGetNodesCoords(self, channelName, value):
        log.debug('Running node coords handler')

        if value > 0:
            self.nodeDetection.loadImage()
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
