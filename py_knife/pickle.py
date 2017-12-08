"""
Pickle/Unpickle Functions
"""

### INCLUDES ###
import os
import sys
import logging

try:
    import cPickle as pickle
except:
    import pickle

from .file_system import open_file, write_file


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
## Pickle/Unpickle File ##
def pickle_file(file_path, data_to_pickle):
    """ Pickle file """
    output = False          # Not sure why False, because data can be '' or None?

    file_instance = open_file(file_path, 'w+')
    if file_instance is not None:
        file_name = os.path.basename(file_path)
        try:
            pickled_data = pickle.dumps(data_to_pickle)
        except KeyboardInterrupt:
            # Retry
            # TODO: Might want to have several retries, not just single retry
            pickle_file(file_path, data_to_pickle)
        except TypeError as error:
            LOGGER.error("Could not pickle '{}'!".format(file_name))
            LOGGER.error('Type Error Details: {}'.format(error))
        except:
            LOGGER.error("Could not pickle '{}'!".format(file_name))
            LOGGER.error('Pickler error: {}'.format(sys.exc_info()[0]))
        else:
            output = write_file(file_instance, pickled_data)

        file_instance.close()

    return output


def unpickle_file(file_path):
    """ Unpickle file """
    output = False          # Not sure why False, because data can be '' or None?

    file_instance = open_file(file_path, 'r')
    if file_instance is not None:
        pickled_data = file_instance.read()
        try:
            unpickled_data = pickle.loads(pickled_data)
        except:
            file_name = os.path.basename(file_path)
            LOGGER.error("Could not unpickle '{}'!".format(file_name))
            LOGGER.error('Unpickler error: {}'.format(sys.exc_info()[0]))
        else:
            output = unpickled_data

        file_instance.close()

    return output
