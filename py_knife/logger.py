"""
Logger Class

To use logger simply::

    import sys
    sys.stdout = Logger(log_file_path)

"""


### INCLUDES ###
import sys


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
