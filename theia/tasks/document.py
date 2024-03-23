import os

from typing import Any

from theia.tasks.job import PipelineJob, PipelineResult
from theia.document.processor import DocumentProcessor

from theia.web.utils import upload_dir

import pandas as pd

class DocumentPipeline(PipelineJob):

    PIPELINE_NAME = "document"

    def __init__(self, filepath: Any | None):
                self.filepath = filepath
          
    async def run(self) -> PipelineResult:

        SHELL_HEIGHT_MM = "measurements"
        LIVE_DEAD_COUNT = "live/dead"

        document_processor = DocumentProcessor()
        df = document_processor.process_document(self.filepath)
        df = df.dropna() # Drop corrupted values

        df1 = pd.DataFrame({
                "shell_height_mm": df[SHELL_HEIGHT_MM],
                "average_shell_height": df[SHELL_HEIGHT_MM].mean(),
                "live_dead_count": df[LIVE_DEAD_COUNT]
        })

        return PipelineResult(self.PIPELINE_NAME, df1)
    
def test_document_pipeline():
        
        from theia.tasks.job import JobRunner

        path = upload_dir("bbp_607_7_29_23_front.jpg")

        dp = DocumentPipeline(path)

        runner = JobRunner()
        table = runner.run_with_pipeline([dp])

        print(table)