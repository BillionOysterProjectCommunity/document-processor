import pandas as pd

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult
from theia.tasks.fields import (
    TOTAL_CUMULATIVE_LIVE_OYSTER
)

class MeasurementPipeline(PipelineJob):

    NAME = "cumulative_measurements"

    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:
        df = pd.DataFrame({
            TOTAL_CUMULATIVE_LIVE_OYSTER: self.form.total_live_oysters.data
        }, index=[0])
        return PipelineResult(self.NAME, df)
