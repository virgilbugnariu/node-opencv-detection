from enum import Enum
import logging as log

from InputDevice import FileInputDevice
from InputDevice import WebcamInputDevice

class InputDevices(Enum):
    FileInputDevice = 1
    WebcamInputDevice = 2

class InputDevice:
    def __init__(self, inputDeviceType, args):
        self.initInputDevice(inputDeviceType, args)
    
    def initInputDevice(self,inputDeviceType, args):
        if inputDeviceType == InputDevices.FileInputDevice:
            self.device = FileInputDevice.FileInputDevice(args)
        elif inputDeviceType == InputDevices.WebcamInputDevice:
            self.device = WebcamInputDevice.WebcamInputDevice(args)
        else:
            log.error('Unknown input device specified')

    def getFrame(self, *args, **kwargs):
        return self.device.getFrame(*args, **kwargs) 