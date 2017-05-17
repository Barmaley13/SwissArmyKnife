"""
Database Classes
Classes that save/load python content to/from the hard drive(or other means of non-volatile memory).
Make sure to provide pickle-able data, no objects, classes or anything that might be hard to convert to a string
Please do not use DatabaseEntry directly, nor DatabaseDictBase. Those are exposed for overloading purposes.
Use DatabaseList, DatabaseDict or DatabaseOrderedDict!
"""


### INCLUDES ###
import os
import copy
import logging

from . import file_system
from . import pickle
from .ordered_dict import OrderedDict


### CONSTANTS ###
## Logger ##
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)
# LOGGER.setLevel(logging.DEBUG)


### CLASSES ###
## Base Database Class ##
class DatabaseEntry(object):
    """ DatabaseEntry class """
    def __init__(self, entry_data_type, db_file=None, defaults=None):
        super(DatabaseEntry, self).__init__()
        self._main = entry_data_type()
        self._db_file = db_file
        self._defaults = defaults
        self.load()

    ## Load Methods ##
    def load(self):
        """ External Load """
        db_main = self._load()
        if db_main is not None:
            self._main = db_main

    def _load(self):
        """ Internal Load - loads main from a file if it exists """
        db_main = None
        if self._db_file is not None:
            # LOGGER.debug('Loading db_file: ' + str(self._db_file))
            database_data = pickle.unpickle_file(self._db_file)

            if database_data is not False:
                db_main = database_data

        if self._defaults is not None and db_main is None:
            db_main = self._load_default()

        return db_main

    def _load_default(self):
        """ Loads main with defaults """
        # LOGGER.debug("type(defaults) = " + str(type(self._defaults)))

        if type(self._defaults) is type(self._main):
            # LOGGER.debug("Deep Copy")
            defaults = copy.deepcopy(self._defaults)
        else:
            # LOGGER.error("Defaults type: " + str(type(self._defaults)) + " is not supported!")
            defaults = None

        return defaults

    ## Save Methods ##
    def save(self, db_content=None):
        """ Saves main to a file """
        if db_content is None:
            db_content = self._main

        if self._db_file is not None:
            if os.sep in self._db_file:
                sub_folders_path = os.path.dirname(self._db_file)
                file_system.make_dir(sub_folders_path)

            # LOGGER.debug('Saving db_file: ' + str(self._db_file))
            pickle.pickle_file(self._db_file, db_content)

    ## Delete Methods ##
    def delete(self):
        """ Deletes database file """
        if self._db_file is not None:
            file_system.remove_file(self._db_file)

    ## Generic Macros ##
    def __iter__(self):
        return iter(self._main)

    def __getitem__(self, key):
        """ Allows using self[key] method """
        return self._main[key]

    def __setitem__(self, key, value):
        """ Allows using self[key] = value method """
        self._main[key] = value

    def __delitem__(self, key):
        """ Allows using del self[key] method """
        del self._main[key]

    def __len__(self):
        """ Allows using len(self) method """
        return len(self._main)

    def __repr__(self):
        """ Allows using self method. Returns list of dictionaries """
        return repr(self._main)

    def __str__(self):
        """ Allows using print self method """
        return str(self.__repr__())

    def pop(self, index):
        """ Allows using pop method """
        return self._main.pop(index)


## List, Dict and OrderedDict Database Classes ##
class DatabaseList(DatabaseEntry):
    """ DatabaseList class """
    def __init__(self, **kwargs):
        """ Load database entry """
        super(DatabaseList, self).__init__(list, **kwargs)

    ## Some List Specific Methods ##
    def append(self, value):
        """ Allows using append method """
        self._main.append(value)

    def extend(self, value):
        """ Allows using extend method """
        self._main.extend(value)

    def insert(self, index, value):
        """ Allows using insert method """
        self._main.insert(index, value)


class DatabaseDictBase(DatabaseEntry):
    """ Some Dictionary Specific Methods """
    def __init__(self, *args, **kwargs):
        super(DatabaseDictBase, self).__init__(*args, **kwargs)
        self._default_value = None
        self.auto_key_creation = True

    def update(self, value):
        """ Allows using update method """
        self._main.update(value)

    def items(self):
        """ Allows using items method """
        return self._main.items()
    
    def values(self):
        """ Allows using values method """
        return self._main.values()
    
    def keys(self):
        """ Allows using keys method """
        return self._main.keys()

    def clear(self):
        """ Allows using clear method """
        return self._main.clear()

    ## Overloading Generic Macros ##
    def __getitem__(self, key):
        """ Overloading to allow automatic key creation feature """
        if key not in self._main:
            if self._default_value is not None:
                LOGGER.warning("Warning key '" + str(key) + "' does not exists! Providing default value!")
                return self._default_value

            if self.auto_key_creation:
                LOGGER.warning("Warning key '" + str(key) + "' does not exists! Creating one!")

                default_value = None
                if key in self._defaults:
                    default_value = self._defaults[key]

                self.__setitem__(key, default_value)

        return super(DatabaseDictBase, self).__getitem__(key)


class DatabaseDict(DatabaseDictBase):
    """ DatabaseDict class """
    def __init__(self, **kwargs):
        """ Load database entry """
        super(DatabaseDict, self).__init__(dict, **kwargs)


class DatabaseOrderedDict(DatabaseDictBase):
    """ DatabaseOrderedDict class """
    def __init__(self, **kwargs):
        """ Load database entry """
        super(DatabaseOrderedDict, self).__init__(OrderedDict, **kwargs)

    def insert_after(self, existing_key, key_value):
        """ Allows using insert_after method """
        self._main.insert_after(existing_key, key_value)

    def insert_before(self, existing_key, key_value):
        """ Allows using insert_before method """
        self._main.insert_before(existing_key, key_value)
