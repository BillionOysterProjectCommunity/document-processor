import pandas as pd

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult

class CagePipeline(PipelineJob):
    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:

        df = pd.DataFrame({
            "tag_type": self._tag_type(),
            "broodstock": self._broodstock(),
            "set_date": self._set_date(),
            "distribution_date": self._distribution_date(),
        }, index=[0])

        return PipelineResult("cage", df)

    def _tag_type(self):
        CIRCLE = "Circle"
        RECTANGLE = "Rectangle"

        if self.form.tag_type.data == CIRCLE:
            return CIRCLE
        else:
            return RECTANGLE

    def _broodstock(self):
        return 0

    def _set_date(self):
        return 0

    def _distribution_date(self):
        return 0
