import os
import tomllib

import theia

from flask import current_app


def config(key: str):
    return current_app.config["SETTINGS"].read(key)


def load_service_account():
    """
    TODO Load service account data
    Reads environment variable GOOGLE_APPLICATION_CREDENTIALS_DOCUMENT_AI_IAM
    MUST be in JSON format
    Writes ADC credentials to theia/service-account.json
    Sets GOOGLE_APPLICATION_CREDENTIALS = {absolute_path}/theia/service-account.json
    """
    pass


RELATIVE_CONFIG_PATH = "billionoysterproject/document.toml"


def pkg_dir():
    p = os.path.dirname(theia.__file__)

    return p


class Config:
    """
    Base configuration store.
    """

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self):
        """
        Returns a reader to the config file object.
        """

        p = pkg_dir() + "/" + "config.toml"

        if "BILLION_OYSTER_CONFIG" not in os.environ:
            with open(p, "rb") as f:
                return tomllib.load(f)
        else:
            # TODO Read BILLION_OYSTER_CONFIG as toml string and ingest all variables into config map
            pass

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
