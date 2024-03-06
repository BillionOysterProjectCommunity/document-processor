import pandas as pd

from theia.drive.client import Client as Drive

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult

from google.oauth2.credentials import Credentials
from theia.web.views.auth import client_id

class DrivePipeline(PipelineJob):

    NAME = "web"

    def __init__(self, form: MetadataForm, token):
        self.client = self._init_credentials(token)
        super().__init__(form)

    def _init_credentials(self, token):
        c = Credentials(client_id=client_id, token=token)
        return Drive(c)

    async def run(self) -> PipelineResult:
        """
        Uploads a drive document to the ORS Drive folder and returns
        the URI
        """

        df = pd.DataFrame({
            "url": "drive.google.com"
        }, index=[0])
        return PipelineResult(self.NAME, df)