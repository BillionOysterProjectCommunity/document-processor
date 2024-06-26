import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from theia.drive.client import Client as Drive
from theia.models.metadata import MetaData
from theia.settings.config import Config

"""
To authorized with Google OAuth use the OAuth Client ID for desktop and download the credentials
into the /drive directory as credentials.json
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        config = Config()
        service = Drive(credentials=creds, config=config)

        print(service.show_initial_files())
    except HttpError as error:
        print(f"An error occurred: {error}")

    print("------------------------------\n")

    path = os.path.abspath(os.path.join("training_data", "training_7.jpg"))
    meta = MetaData()
    meta.monitoring_date = datetime.fromisoformat("2023-11-12")

    print("------------------------------\n")

    print(service.directory_id(2023, 1))

    service.process_ors_document(path, meta)


if __name__ == "__main__":
    main()
