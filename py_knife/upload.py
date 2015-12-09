"""
Web Upload Functions
"""

### INCLUDES ###
import os
import codecs
import logging


### CONSTANTS ###
## Meta Data ##
__author__ = 'Kirill V. Belyayev'
__license__ = 'GPL'

## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
## Upload related Functions with recursion ##
def save_upload(upload_folder_path, upload_data):
    """ Tries to open Upload File """
    output = False

    upload_path = os.path.join(upload_folder_path, upload_data.filename)
    try:
        upload_file = codecs.open(upload_path, 'w+')
    except:
        pass
    else:
        try:
            # This is dangerous for big files (using RAM)
            # TODO: Figure out RAM-less alternative upload
            upload_file.write(upload_data.file.read())
        except:
            pass
        else:
            output = upload_path

    return output
