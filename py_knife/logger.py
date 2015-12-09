"""
Logger Class
"""


### INCLUDES ###
import sys


### CONSTANTS ###
## Meta Data ##
__author__ = 'Kirill V. Belyayev'
__license__ = 'GPL'


### CLASSES ###
class Logger(object):
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        self.filename = filename
        if self.filename is not None:
            self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        if self.filename is not None:
            self.log.write(message)
