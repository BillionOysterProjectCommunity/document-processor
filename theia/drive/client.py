from google.oauth2.credentials import Credentials
from theia.settings.config import Config

from googleapiclient.discovery import build

"""
Google drive client functions
"""

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

class Client:
    def __init__(self, credentials: Credentials, config: Config):
        self.config = config
        self.service = build("drive", "v3", credentials=credentials)
        
    def show_initial_files(self):

        results = (
            self.service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )

        return results
    
    def upload_file_to_folder(self, file):
        pass
    