"""
Python Distribution Install Functions
"""

### INCLUDES ###
import os
import subprocess
import logging

from .file_system import remove_dir


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
def install_package(package_name, package_path=None):
    """ Runs install inside of install """
    cwd = os.getcwd()

    clean_up = False
    if package_path is None:
        package_path = os.path.join(cwd, package_name)
        clean_up = True
    os.chdir(package_path)

    print 'Installing ' + package_name + '...'
    if os.name == 'nt':
        # This failed on E10 as part of web interface install
        install_process = subprocess.Popen(['python', 'setup.py', 'install'], shell=True)
    else:
        # Proven to work robust on E10 (but fails on Windows)
        install_process = subprocess.Popen(['python setup.py install'], shell=True)

    install_process.wait()
    os.chdir(cwd)

    if clean_up:
        print 'Cleaning ' + package_name + ' up...'
        remove_dir(package_path)
