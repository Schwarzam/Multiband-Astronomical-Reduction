import argparse

import os
import sys
import subprocess
import mar



version__ = 0.1



from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


## functions to deal with YAML
class AttributeDict(dict):
    def __init__(self, d):
        super().__init__(d)
        
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def dumpconfig(_config, outfile):
    f = open(outfile, "w")
    f.write(dump(_config, Dumper=Dumper))
    f.close()

def loadconfig(file):
    fil = load(open(file), Loader=Loader)
    return fil
## -- ##


ABS_PATH = mar.__path__[0] + '/'


class Enviroment:
    """
    A class that represents the configuration of the MAR package.

    Attributes:
        marPath (str): The absolute path to the default configuration file.
        marConf (AttributeDict): A dictionary-like object that holds the configuration values
            loaded from the configuration file.

    Methods:
        welcome(): Prints a welcome message to the console if this is the first time the
            package is being used.
        getConf(): Returns the configuration values stored in `marConf`.
        setItemConf(section: str, item: str, value: Any): Sets the value of a specific configuration
            item in the specified section.
        saveConf(): Saves the current configuration values to the configuration file.

    """
    def __init__(self):
        self.marPath = os.path.join(mar.__path__[0], 'config', 'defaultconfig.yaml')
        #self.marPath = 'defaultconfig.yaml'
        self.marConf = AttributeDict(loadconfig(self.marPath))
        self.welcome()

    def load_config(self, path):
        try:
            self.marConf = AttributeDict(loadconfig(path))
            self.marPath = path
        except:
            return "Could not load config file."
        
    def welcome(self):
        if self.marConf.get('FIRST_TIME'):
            print("""
-------------------------------------------
Multiband Astronomical Reduction
MAR Package

Provided by Gustavo Schwarz and Fábio Herpich
S-PLUS - 2022

gustavo.b.schwarz@gmail.com
-------------------------------------------            
            """)
        
            del self.marConf['FIRST_TIME']
            self.saveConf()
        
    def getConf(self):
        return self.marConf
    
    def setItemConf(self, section, item, value):
        if value is None or value == '':
            del self.marConf.get(section)[item]
        else:
            self.marConf.get(section)[item] = value
        
        self.saveConf()
        
    def saveConf(self):
        dumpconfig(dict(self.getConf()), self.marPath)


env = Enviroment()