import os

from typing import Any

from theia.tasks.job import PipelineJob, PipelineResult
from theia.document.processor import DocumentProcessor

from theia.tasks.fields import (
        SHELL_HEIGHT_MM,
        LIVE_DEAD_COUNT,
        LIVE_GEQ_15MM,
        LIVE_LE_15MM,
        DEAD_GEQ_15MM,
        DEAD_LE_15MM
)

import pandas as pd

class DocumentPipeline(PipelineJob):

    PIPELINE_NAME = "document"


    def __init__(self, filepath: Any | None):
                self.filepath = filepath
          
    async def run(self) -> PipelineResult:

        document_processor = DocumentProcessor()
        df = document_processor.process_document(self.filepath)
        df = df.dropna() # Drop corrupted values

        df1 = pd.DataFrame({
                "shell_height_mm": df[SHELL_HEIGHT_MM],
                "average_shell_height": df[SHELL_HEIGHT_MM].mean(),
                "live_dead_count": df[LIVE_DEAD_COUNT],
        })

        df2 = pd.DataFrame({
                "shell_height_mm": df1["shell_height_mm"],
                "average_shell_height": df1["average_shell_height"],
                "live_dead_count": df1["live_dead_count"],
                LIVE_GEQ_15MM: total_live_geq_15mm(df1),
                LIVE_LE_15MM: total_live_le_15mm(df1),
                DEAD_GEQ_15MM: total_dead_geq_15mm(df1),
                DEAD_LE_15MM: total_dead_le_15mm(df1)
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