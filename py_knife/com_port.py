"""
Serial(COM) Port Functions
"""

### INCLUDES ###
import logging

from serial.tools.list_ports import comports


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
def available_ports():
    """ Returns list of available serial ports """
    output = list()
    for serial_port, port_description, hardware_id in sorted(comports()):
        LOGGER.debug('Port Name: ' + str(serial_port))
        # LOGGER.debug('Port: {:>10} Desc: {:>10} HW ID: {:>10}'.format(serial_port, port_description, hardware_id))
        output.append(serial_port)

    return output
