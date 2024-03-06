from datetime import datetime

from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

from theia.settings.config import Config

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pdfkit
import json

"""
Google drive client functions
"""

class Client:
    def __init__(self, credentials: Credentials):
        self.config = Config()
        self.service = build("drive", "v3", credentials=credentials)
        
    def show_initial_files(self):

        results = (
            self.service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )

        return results
    
    def directory_id(self, year, month):
        # https://drive.google.com/drive/u/1/folders/14TnRzd3Zs7MJQ2XGyMwi0J-n59fpvyo1
        # Records are delimited into years and months for use with the datetime.fromisoformat()
        year = str(year)
        month = str(month)

        with open('directory.json') as f:
            content = f.read()

        d = json.loads(content)

        return d[year][month]
    
    def process_ors_document(self, path, metadata):
        date: datetime = metadata.monitoring_date

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('submission.html')
        raw = template.render(image=path)

        with open("uploads/compiled.html", "w") as f:
            f.write(raw)

        filename = f'{date.year}'

        pdfkit.from_file('uploads/compiled.html', 
                         output_path=f'uploads/{filename}.pdf',
                         options={"enable-local-file-access": None})
        
        # TODO: Automatically upload to google drive master sheet folder using year + month



        
        
    