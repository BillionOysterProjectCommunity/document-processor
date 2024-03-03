import pandas as pd

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult

class DrivePipeline(PipelineJob):

    NAME = "web"

    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:
        """
        Uploads a drive document to the ORS Drive folder and returns
        the URI
        """
        df = pd.DataFrame({
            "url": "drive.google.com"
        }, index=[0])
        return PipelineResult(self.NAME, df)