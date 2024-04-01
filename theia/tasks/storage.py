import pandas as pd

from theia.web.forms import MetadataForm
from theia.web.utils import upload_dir
from theia.tasks.job import PipelineJob, PipelineResult

from google.cloud import storage

class StoragePipeline(PipelineJob):

    GCP_BUCKET_NAME = "billion-oyster-project-data-sheet-media"
    GCP_BUCKET_URI = "https://storage.googleapis.com/billion-oyster-project-data-sheet-media/"

    def __init__(self, form: MetadataForm):
        self.client = storage.Client()
        super().__init__(form)

    async def run(self) -> PipelineResult:

        bucket = self.client.bucket(self.GCP_BUCKET_NAME)
        filename = self.form.image.data.filename
        blob = bucket.blob(filename)

        blob.upload_from_filename(upload_dir(filename))

        df = pd.DataFrame({
            "url": self.GCP_BUCKET_URI + filename,
        }, index=[0])

        return PipelineResult("storage", df)
