from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineResult

class CagePipeline(Job):
    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:
        pass