import pandas as pd

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult

class CagePipeline(PipelineJob):
    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:

        df = pd.DataFrame({
            "tag_type": self._tag_type(),
        }, index=[0])

        return PipelineResult("cage", df)

    def _tag_type(self):
        CIRCLE = "Circle"
        RECTANGLE = "Rectangle"

        if self.form.tag_type.data == CIRCLE:
            return CIRCLE
        else:
            return RECTANGLE