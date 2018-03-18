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
    def __init__(self, script_name=None):
        # Process filename to get only filename without extension
        filename = os.path.splitext(os.path.basename(script_name))[0]

        # Import config file
        config_file = os.path.join(os.path.dirname(os.path.dirname(\
            os.path.abspath(__file__))), 'cfg/' + filename + '.json')
        config_file = os.path.normpath(config_file)

        # Read config file
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except IOError as e:
            print('cannot access config file %s' % config_file)
            print(e)
            exit(1)
        else:
            # Define instance variables from dict
            for key, val in config.items():
                setattr(self, key, val)