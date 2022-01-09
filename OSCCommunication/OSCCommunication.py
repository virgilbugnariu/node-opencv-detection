import logging as log
import socket

from pythonosc import osc_server
from pythonosc import dispatcher as OSCDispatcher
from pythonosc import udp_client

class OSCCommunication:
    def __init__(self):
        log.debug('OSCCommunication class initialized')
        self.dispatcher = OSCDispatcher.Dispatcher()

    def init(self):
        IP_ADDRESS = '192.168.0.104'
        PORT = 8000

        self.dispatcher.map('/test', print)

        self.server = osc_server.ThreadingOSCUDPServer(
            (IP_ADDRESS, PORT),
            self.dispatcher
        )

        self.client = udp_client.SimpleUDPClient(
            '192.168.0.107',
            8001
        )

        log.info('Starting OSC Server')
        self.server.serve_forever()
