"""
Web Upload Functions
"""

### INCLUDES ###
import os
import codecs
import logging


### CONSTANTS ###
## Read Chunk Size ##
CHUNK_SIZE = 512 * 1024         # 0.5 MB


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
        while True:
            data_chunk = upload_data.file.read(CHUNK_SIZE)

            if not data_chunk:
                break
            else:
                upload_file.write(data_chunk)

        upload_file.close()
        output = upload_path

    return output
