import os

from typing import Any

from theia.tasks.job import PipelineJob, PipelineResult
from theia.document.processor import DocumentProcessor

from theia.web.utils import upload_dir

import pandas as pd

class DocumentPipeline(PipelineJob):

    PIPELINE_NAME = "document"
    SHELL_HEIGHT_MM = "measurements"
    LIVE_DEAD_COUNT = "live/dead"
    LIVE_GEQ_15MM = "total # of live oysters greater than or equal to 15mm:"
    LIVE_LE_15MM = "Total LIVE oysters LESS than 15 mm"
    DEAD_GEQ_15MM = "Total DEAD oysters greater than or equal to 15mm:"
    DEAD_LE_15MM = "Total DEAD oysters LESS than 15 mm"


    def __init__(self, filepath: Any | None):
                self.filepath = filepath
          
    async def run(self) -> PipelineResult:

        document_processor = DocumentProcessor()
        df = document_processor.process_document(self.filepath)
        df = df.dropna() # Drop corrupted values

        df1 = pd.DataFrame({
                "shell_height_mm": df[self.SHELL_HEIGHT_MM],
                "average_shell_height": df[self.SHELL_HEIGHT_MM].mean(),
                "live_dead_count": df[self.LIVE_DEAD_COUNT],
        })

        df2 = pd.DataFrame({
                "shell_height_mm": df1["shell_height_mm"],
                "average_shell_height": df1["average_shell_height"],
                "live_dead_count": df1["live_dead_count"],
                self.LIVE_GEQ_15MM: total_live_geq_15mm(df1),
                self.LIVE_LE_15MM: total_live_le_15mm(df1),
                self.DEAD_GEQ_15MM: total_dead_geq_15mm(df1),
                self.DEAD_LE_15MM: total_dead_le_15mm(df1)
        })      

        # df1.to_csv('measurements.csv')

        return PipelineResult(self.PIPELINE_NAME, df2)

def total_live_geq_15mm(df):
        df = df[df["shell_height_mm"] >= 15]
        df = df[df["live_dead_count"] == "L"]

        return df["live_dead_count"].count()

def total_live_le_15mm(df):
        df = df[df["shell_height_mm"] < 15]
        df = df[df["live_dead_count"] == "L"]

        return df["live_dead_count"].count()

def total_dead_geq_15mm(df):
        df = df[df["shell_height_mm"] >= 15]
        df = df[df["live_dead_count"] == "D"]

        return df["live_dead_count"].count()

def total_dead_le_15mm(df):
        df = df[df["shell_height_mm"] < 15]
        df = df[df["live_dead_count"] == "D"]

        return df["live_dead_count"].count()