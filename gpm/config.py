"""
Provides ability to read a JSON based configuration file

The configuration file must reside in a folder called "cfg" in the directory 
where Python script is and the name of the file should match the name of the 
Python Script

Python script:
folderX/ScriptY.py

configuration file:
folderX/cfg/ScriptY.json

"""
import os.path
import json


# Read the configuration file. Just need to provide __file__ as parameter
class Config(object):
    # create: set True if the file needs to be created if doesn't exist
    def __init__(self, script, create=False, cfg_file=None, cfg_dir=None):
        # Define config file name
        if cfg_file is None:
            cfg_file = os.path.splitext(os.path.basename(script))[0] + '.json'

        # Define config dir
        if cfg_dir is None:
            cfg_dir = os.path.join(os.path.dirname(os.path.abspath(script)), 'cfg')

        # Define full path
        cfg_file_path = os.path.join(cfg_dir, cfg_file)

        self._file = cfg_file
        self._dir = cfg_dir
        self._file_path = cfg_file_path

        if create:
            self._create()

    def read(self):
        # Read config file
        with open(self._file_path, 'r') as f:
            config = json.load(f)

        # Define instance variables from dict
        for key, val in config.items():
            setattr(self, key, val)

    def _create(self):
        if not os.path.exists(self._dir):
            os.mkdir(self._dir)

        if not os.path.exists(self._file_path):
            cfg_data = {}
            with open(self._file_path, 'w') as outfile:
                json.dump(cfg_data, outfile)
