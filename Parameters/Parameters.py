import os
import sys
import logging as log
import time
import json

from Parameters.Singleton import Singleton

def getTimestampFromFilename(filename):
    name = os.path.splitext(filename)[0]
    timestamp = name[-12:]
    return float(timestamp)

class Parameters(metaclass = Singleton):
    def __init__(self):
        log.debug('Init parameters')
        baseFolder = os.path.dirname(__file__)
        self.presetsFolderName = 'presets'
        
        self.presetsFolderPath = os.path.join(
            baseFolder, 
            self.presetsFolderName
        )
        
        presetFolderExists = self.checkPresetsFolderPresence()
        
        if not presetFolderExists:
            self.initializeStorage()
            self.preset = {}
            log.info('No presets available. Run calibration first!')
        else:
            self.preset = self.getLatestPreset()

    def initializeStorage(self):
        log.debug('Presets folder missing. Creating')
        os.mkdir(self.presetsFolderPath)
    
    def checkPresetsFolderPresence(self):
        return os.path.exists(self.presetsFolderPath)

    def getAvailablePresets(self):
        pass

    def getLatestPreset(self):
        dir = os.listdir(self.presetsFolderPath)
        if len(dir) == 0:
            return {}
        else:
            latestPreset = max(dir, key = lambda filename: getTimestampFromFilename(filename))
            log.debug('Loading preset with filename %s', latestPreset)

            file = open(os.path.join(self.presetsFolderPath, latestPreset), 'r')
            data = file.read()
            return json.loads(data)
        pass
    
    """
    Creates a new preset file with the current timestamp
    """
    def savePreset(self):
        timestamp = round(time.time(), 0)
        presetFilePath = 'preset-' + str(timestamp) + '.json'
        data = json.dumps(self.preset)

        file = open(os.path.join(self.presetsFolderPath, presetFilePath), 'a')
        file.write(data)
        file.close()
    
    def set(self, name, value):
        log.debug('Setting %s with value %s', name, value)
        self.preset.update({name: value})

    def get(self, name):
        return self.preset[name]

    


