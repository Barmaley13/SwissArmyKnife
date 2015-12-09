# !/usr/bin/env python
"""
Script for generating package distribution

Used quite a few recipes from here:
https://wiki.python.org/moin/Distutils/Cookbook

"""


### INCLUDES ###
import os
import sys
import imp
import shutil
import glob

from distutils.core import setup

from py_knife import __version__
from py_knife import file_system


### CONSTANTS ###
## Meta Data ##
__author__ = 'Kirill V. Belyayev'
__license__ = 'GPL'


### FUNCTIONS ###
## Setup Functions ##
def is_package(path):
    return os.path.isfile(os.path.join(path, '__init__.py'))


def find_packages(path, base=""):
    """ Find all packages in path """
    py_packages = {}
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


def non_python_files(path):
    """ Return all non-python-file file names in path """
    result = []
    all_results = []
    module_suffixes = [info[0] for info in imp.get_suffixes()]
    ignore_dirs = ['cvs']
    if os.path.isdir(path):
        for item in os.listdir(path):
            name = os.path.join(path, item)
            if os.path.isfile(name) and os.path.splitext(item)[1] not in module_suffixes:
                result.append(name)
            elif os.path.isdir(name) and item.lower() not in ignore_dirs:
                all_results.extend(non_python_files(name))
        if result:
            all_results.append((path, result))

    return all_results


def package_data_files(path):
    """ Returns all file names in path in package data format """
    result = []
    for item in non_python_files(path):
        result += item[1]

    return result


## Dist Functions ##
def _generate_docs(doc_packages):
    """
    Generates documentation. Performed before generating distribution on host (Windows) system.
    """
    print "*** Generating Documentation ***"
    # Set current working directory
    cwd = sys.path[0]
    print "CWD = ", str(cwd)
    os.chdir(cwd)

    # Rebuilding package module interconnections and package classes images.
    for package_name, package_path in doc_packages.items():
        package_path = package_path.split('py_knife')
        package_path[0] = ''
        package_path = 'py_knife'.join(package_path)
        pyreverse_command = 'pyreverse -o png -p ' + package_name + ' ' + package_path
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
    print 'sphinx-apidoc -f -o _docs py_knife'
    os.system('sphinx-apidoc -f -o _docs py_knife')
    # Rebuilding documentation in html format
    file_system.remove_dir('docs')
    print 'sphinx-build -b html _docs docs'
    os.system('sphinx-build -b html _docs docs')


### SETUP PROCEDURES ###
packages = find_packages(".", "")
# print "packages = ", str(packages), "\n"

if len(sys.argv):
    if 'sdist' in sys.argv:
        _generate_docs(packages)
        print "*** Generation Distribution ***"
    elif 'install' in sys.argv:
        # Enable force to overwrite existing files and create folders
        if '--force' not in sys.argv:
            sys.argv.append('--force')

# Probably none, kept for future reference
data_files = (non_python_files('py_knife'))
# print "data_files = ", str(data_files), "\n"

package_data_content = package_data_files('docs')
package_data = {'': package_data_content}
# print "package_data = ", str(package_data), "\n"

setup(
    name='py_knife',
    version=__version__,
    description='Swiss Army Knife',
    long_description='Swiss Army Knife of Python',
    author='Kirill V. Belyayev',
    author_email='kbelyayev@gmail.com',
    url='https://github.com/Barmaley13/SwissArmyKnife',
    # download_url='https://github.com/Barmaley13/SwissArmyKnife/tarball/' + __version__,
    packages=packages.keys(),
    package_dir=packages,
    package_data=package_data,
    data_files=data_files,
    requires=[
        'pyserial',
        'pycrypto'
    ]
)
