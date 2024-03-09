import os
import tomllib

import theia

from flask import current_app

def config(key: str):
    return current_app.config["SETTINGS"].read(key)




RELATIVE_CONFIG_PATH = "billionoysterproject/document.toml"

class Config:
    """
    Base configuration store.
    """
    def __init__(self):
        self._config = self._load_config()

    def _config_path(self):
        p = os.path.dirname(theia.__file__)  + "/" + "config.toml"

        return p

    def _load_config(self):
        """
        Returns a reader to the config file object.
        """
        with open(self._config_path(), "rb") as f:
            return tomllib.load(f)

    def set(self, key, value):
        """
        Set a key value pair in the config

        Example:

        config = Config()

        config.set('smartsheet-id', 12345)

        config.read('smartsheet-id')
        """
        self._config[key] = value
    
    def read(self, key):
        """
        Returns a value based on the config key given.
        """
        return self._config[key]
    

