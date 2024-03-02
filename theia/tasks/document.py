import os

from typing import Any

from theia.tasks.job import PipelineJob, PipelineResult
from theia.document.processor import DocumentProcessor

class DocumentPipeline(PipelineJob):

    PIPELINE_NAME = "document"

    def __init__(self, filepath: Any | None):
                self.filepath = filepath
          
    async def run(self) -> PipelineResult:
            document_processor = DocumentProcessor()
            df = document_processor.process_document(self.filepath)
            df = df.dropna() # Drop corrupted values

            return PipelineResult(self.PIPELINE_NAME, df)
    
def test_document_pipeline():
        
        from theia.tasks.job import JobRunner

        path = os.path.abspath(os.path.join("../web/uploads", "bbp_607_7_29_23_front.jpg"))

        dp = DocumentPipeline(path)

        runner = JobRunner()
        table = runner.run_with_pipeline([dp])

        print(table)