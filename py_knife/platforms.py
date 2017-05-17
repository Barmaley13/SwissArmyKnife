"""
Determine current platform
Uses python platform module to determine if run this script on Windows, MAC, Ubuntu or Debian Linux
Or 'Raspberry Pi' or 'Synapse E10' system
"""


### INCLUDES ###
import platform
import logging


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)

## Platform Types ##
LINUX = 'linux'
UBUNTU = 'ubuntu'
DEBIAN = 'debian'
MAC = 'darwin'
WINDOWS = 'windows'
RASPBERRY_PI = 'raspberry-pi'
SYNAPSE_E10 = 'synapse-e10'

## Platform Groups ##
LINUX_PLATFORMS = LINUX, UBUNTU, DEBIAN
PC_PLATFORMS = LINUX_PLATFORMS + (MAC, WINDOWS)
EMBEDDED_PLATFORMS = RASPBERRY_PI, SYNAPSE_E10
PLATFORMS = PC_PLATFORMS + EMBEDDED_PLATFORMS           # all possible options

## Embedded Platform Identifiers ##
PI_HARDWARE = ('BCM2708', 'BCM2709')
E10_PLATFORM = 'Linux-2.6.33-armv5tejl-with-glibc2.0'

## Determine Platform ##
PLATFORM = platform.system().lower()
if PLATFORM == 'linux':
    if platform.platform() == E10_PLATFORM:
        PLATFORM = SYNAPSE_E10

    else:
        linux_distribution = platform.linux_distribution()[0].lower()
        if len(linux_distribution):
            PLATFORM = linux_distribution

        if PLATFORM == DEBIAN:
            try:
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('Hardware') and line.endswith(PI_HARDWARE):
                            PLATFORM = RASPBERRY_PI
                            break
            except:
                pass
