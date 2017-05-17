# !/usr/bin/env python
"""
Python Distribution Package Utilities

Used quite a few recipes from here:
https://wiki.python.org/moin/Distutils/Cookbook
Some hints on how to extend commands
http://stackoverflow.com/questions/1321270/how-to-extend-distutils-with-a-simple-post-install-script/1321345#1321345
"""


### INCLUDES ###
import os
import imp
import glob
import shutil
import logging

from .ordered_dict import OrderedDict
from . import file_system


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)


### FUNCTIONS ###
def is_package(path):
    return os.path.isfile(os.path.join(path, '__init__.py'))


def find_packages(path, base=""):
    """ Find all packages in path """
    py_packages = OrderedDict()

    for item in os.listdir(path):
        py_dir = os.path.join(path, item)
        if os.path.isdir(py_dir) and is_package(py_dir):
            # print "item = ", item
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            py_packages[module_name] = py_dir
            py_packages.update(find_packages(py_dir, module_name))

    return py_packages


def non_python_files(path, ignore_dirs=None):
    """ Return all non-python-file file names in path """
    result = []
    all_results = []
    module_suffixes = [info[0] for info in imp.get_suffixes()]

    if ignore_dirs is None:
        ignore_dirs = []

    if os.path.isdir(path):
        for item in os.listdir(path):
            name = os.path.join(path, item)
            if os.path.isfile(name) and os.path.splitext(item)[1] not in module_suffixes:
                result.append(name)
            elif os.path.isdir(name) and item.lower() not in ignore_dirs:
                all_results.extend(non_python_files(name, ignore_dirs))
        if result:
            all_results.append((path, result))

    return all_results


def package_data_files(path, ignore_dirs=None):
    """ Returns all file names in path in package data format """
    result = []
    for item in non_python_files(path, ignore_dirs):
        result += item[1]

    return result


def generate_docs(doc_packages):
    """ Generates documentation. Performed before generating distribution on host (Windows) system """
    if len(doc_packages):
        _base_package_names = list()

        # Rebuilding package module interconnections and package classes images
        for _package_name, _package_path in doc_packages.items():
            # Figuring out base package name
            _base_package_name = _package_name.split('.')[0]
            if _base_package_name not in _base_package_names:
                _base_package_names.append(_base_package_name)

            # Rebuild images
            _package_path = _package_path.split(_base_package_name)
            _package_path[0] = ''
            _package_path = _base_package_name.join(_package_path)
            pyreverse_command = 'pyreverse -o png -p ' + _package_name + ' ' + _package_path
            print pyreverse_command
            os.system(pyreverse_command)

        # Moving images to appropriate folder
        images = glob.glob('*.png')
        destination_path = os.path.join('_docs', 'images')
        file_system.make_dir(destination_path)
        for image_path in images:
            image_name = os.path.basename(image_path)
            shutil.move(image_path, os.path.join(destination_path, image_name))

        # Updating automatically generated rst files
        for _base_package_name in _base_package_names:
            apidoc_str = 'sphinx-apidoc -f -o _docs ' + _base_package_name
            print apidoc_str
            os.system(apidoc_str)

        # Rebuilding documentation in html format
        file_system.remove_dir('docs')
        build_str = 'sphinx-build -b html _docs docs'
        print build_str
        os.system(build_str)
