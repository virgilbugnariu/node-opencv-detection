import logging
import getopt
import sys
from NodeDetection import NodeDetection
from OSCCommunication import OSCCommunication

# Init program
def main(args):

    # Defaults
    LOG_LEVEL = 'INFO'

    # Get logging level argument
    try:
        opts, args = getopt.getopt(args, 'l', ['log='])
    except:
        print('Invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--log'):
            LOG_LEVEL = arg

    logging.basicConfig(level=LOG_LEVEL)

    logging.info('Initialize NodeDetection')
    nodeDetection = NodeDetection()

    logging.info('Initialize OSC communication')
    osc = OSCCommunication()

    def handleGetNodesCoords(channelName, value):
        if value > 0:
            nodeDetection.loadImage()
            result = nodeDetection.runPipeline()

            osc.client.send_message('/nodesCoords', 12)
            print(result)

    osc.dispatcher.map('/getNodesCoords', handleGetNodesCoords)

    osc.init()

if __name__ == '__main__':
    main(sys.argv[1:])
