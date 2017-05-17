"""
This module functionality consist of:

    * File Manipulation Functions
    * Directory Manipulation Functions
    * File/Folder Memory Space/Size Functions
    * Open/Write/Read File Functions
    * Time Stamp Functions

"""

### INCLUDES ###
import os
import sys
import shutil
import glob
import ctypes
import codecs
import time
import logging

from distutils.spawn import find_executable


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
## File Functions ##
def make_file(file_path):
    """ Creating empty file """
    if not os.path.isfile(file_path):
        LOGGER.debug('Creating file: ' + str(file_path))
        new_file = open(file_path, 'a')
        # Clear content of the file (just in case)
        # new_file.seek(0)
        # new_file.truncate()
        new_file.close()


def remove_file(file_path):
    if os.path.isfile(file_path):
        LOGGER.debug('Removing file: ' + str(file_path))
        os.remove(file_path)


def remove_files(files_path, exclude_paths=None):
    """ Removes files, specified by path/filter """
    if exclude_paths is None:
        exclude_paths = list()

    files = glob.glob(files_path)
    # Remove files first
    for item in files:
        if item not in exclude_paths:
            remove_file(item)

    # Remove directories second
    for item in files:
        if item not in exclude_paths:
            remove_dir(item)


def copy_file(source_file, destination_file, permissions=None, dos2unix=True):
    """
    Copying File
    :param source_file: Source File Path
    :param destination_file: Destination File Path
    :param permissions: Permissions string (for unix only)
    :param dos2unix: Conversion to unix format (for unix only)
    :return: True if copying is successful, False otherwise
    """
    output = os.path.isfile(source_file)
    if output:
        # Remove destination file (if exists)
        if os.path.isfile(destination_file):
            os.remove(destination_file)

        # Copy file
        shutil.copy(source_file, destination_file)

        if os.name == 'posix':
            # Convert to unix format
            if dos2unix:
                if find_executable('dos2unix'):
                    os.system('dos2unix ' + destination_file)

            # Add permissions
            if permissions is not None:
                os.system('chmod ' + str(permissions) + ' ' + destination_file)

    return output


def fetch_file(file_path):
    """ Fetches files, specified by path/filter """
    output = None

    files = glob.glob(file_path)
    if len(files):
        csv_path = files[0]
        # Provide with csv name as an output
        output = os.path.basename(csv_path)

    return output


## Directory Functions ##
def make_dir(dir_path):
    """
    Creating directory
    :param dir_path: Path of the new directory
    :return: True if folder has been created, False if folder exists already
    """
    output = not os.path.isdir(dir_path)
    if output:
        LOGGER.debug('Creating folder: ' + str(dir_path))
        os.makedirs(dir_path)

    return output


def remove_dir(dir_path):
    """
    Removing directory
    :param dir_path: Path of the directory
    :return: True if remove successful (such directory existed in the first place), False otherwise
    """
    output = os.path.isdir(dir_path)
    if output:
        LOGGER.debug('Removing folder: ' + str(dir_path))
        shutil.rmtree(dir_path)

    return output


def empty_dir(dir_path):
    """
    Empty directory
    :param dir_path: Path of the directory
    :return: True if empty successful (such directory existed in the first place), False otherwise
    """
    output = remove_dir(dir_path)
    if output:
        os.makedirs(dir_path)

    return output


def copy_dir(source_path, destination_path):
    # LOGGER.debug('source: ' + str(source_path))
    # LOGGER.debug('destination: ' + str(destination_path))
    if os.path.isdir(source_path):
        make_dir(destination_path)
        sub_items = glob.glob(os.path.join(source_path, '*'))
        for sub_item_path in sub_items:
            sub_item_name = os.path.basename(sub_item_path)
            copy_dir(sub_item_path, os.path.join(destination_path, sub_item_name))

    elif os.path.isfile(source_path):
        copy_file(source_path, destination_path)


## File/Folder Memory Space/Size Functions ##
def get_size(path):
    """
    Taken from here
    http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
    """
    total_size = 0

    if os.path.isfile(path):
        try:
            stat = os.stat(path)
        except OSError:
            pass
        else:
            total_size += stat.st_size

    elif os.path.isdir(path):
        seen = set()
        for directory_path, directory_names, file_names in os.walk(path):
            for f in file_names:
                fp = os.path.join(directory_path, f)

                try:
                    stat = os.stat(fp)
                except OSError:
                    continue

                if stat.st_ino in seen:
                    continue

                seen.add(stat.st_ino)

                total_size += stat.st_size

    return total_size  # size in bytes


def get_free_space(path):
    """
    Return free space in bytes
    Taken from here, slightly modified:
    http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python
    """
    if os.name == 'nt':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        # TODO: Works on Linux, double check this works on MAC, consider following link:
        # http://ilostmynotes.blogspot.com/2014/05/cross-platform-python-method-for.html
        st = os.statvfs(path)
        return st.f_bavail * st.f_frsize


def print_memory_size(size):
    """
    Taken from here
    http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
    """
    _bytes = 'B'
    _kilo_bytes = 'KB'
    _mega_bytes = 'MB'
    _giga_bytes = 'GB'
    _tera_bytes = 'TB'
    memory_units = [_bytes, _kilo_bytes, _mega_bytes, _giga_bytes, _tera_bytes]
    memory_format = '%f %s'
    memory_radix = 1024.

    for u in memory_units[:-1]:
        if size < memory_radix:
            return memory_format % (size, u)
        size /= memory_radix

    return memory_format % (size, memory_units[-1])


## Open/Write/Read File Functions ##
def open_file(file_path, mode, encoding=None):
    """ Tries reading file. Returns false if failed """
    output = None
    try:
        file_instance = codecs.open(file_path, mode, encoding)
    except:
        pass
    else:
        output = file_instance

    return output


def save_file(file_path, file_content, encoding=None, permissions=None):
    """ Tries to open file for writing """
    output = False

    file_instance = open_file(file_path, 'w+', encoding)
    if file_instance is not None:
        if write_file(file_instance, file_content):
            output = os.path.basename(file_path)
        file_instance.close()

        if os.name == 'posix':
            # Add permissions
            if permissions is not None:
                os.system('chmod ' + str(permissions) + ' ' + file_path)

    return output


def write_file(file_instance, file_content):
    """ Tries writing file """
    output = False
    try:
        file_instance.write(file_content)
    except:
        LOGGER.error("write_file unexpected error:" + str(sys.exc_info()[0]))
    else:
        output = True

    return output


## Time Stamp Functions ##
def create_time_stamp(time_stamp_format):
    return time.strftime(time_stamp_format, time.localtime(time.time()))
