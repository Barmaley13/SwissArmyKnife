"""
Zip Archive Functions
"""

### INCLUDES ###
import os
import zipfile
import logging


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
def create_zip(zip_path, files_path):
    """ Creates Zip Archive """
    zip_status = True

    try:
        zip_archive = zipfile.ZipFile(zip_path, 'w')

        for root, dirs, files in os.walk(files_path):
            for _file in files:
                zip_archive.write(os.path.join(root, _file))

        zip_archive.close()

    except:
        zip_status = False

    return zip_status


def extract_zip(zip_path, extract_path=None, password=None):
    """ Opens Zip Archive in order to extract files """
    zip_status = True

    try:
        zip_archive = zipfile.ZipFile(zip_path, 'r')
        if password is not None:
            zip_archive.setpassword(password)

        if extract_path is None:
            extract_path = os.path.dirname(zip_path)

        zip_archive.extractall(extract_path)
        zip_archive.close()

    except:
        zip_status = False

    return zip_status
