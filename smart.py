import smartsheet
from config import Config

# TODO API Access requires "upgraded" plan for smartsheet

class Smart:
    def __init__(self, config):
        self.config = config
        self.client = smartsheet.Smartsheet(access_token=self.config.read('smartsheet-access-token'))