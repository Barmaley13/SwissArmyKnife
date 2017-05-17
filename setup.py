# !/usr/bin/env python
"""
Swiss Army Knife Setup Scripts
"""


### INCLUDES ###
import sys

from distutils.core import setup

from py_knife import __version__
from py_knife.py_setup import find_packages, non_python_files, package_data_files, generate_docs


### SETUP PROCEDURES ###
packages = find_packages(".", "")
# print "packages = ", str(packages), "\n"

if len(sys.argv):
    if 'sdist' in sys.argv:
        print "*** Generating Documentation ***"
        generate_docs(packages)

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
