import asyncio

from abc import (
    ABCMeta,
    abstractmethod
)

from typing import (
    List
)

import pandas as pd

from theia.web.forms import MetadataForm

class PipelineResult:
    def __init__(self, name, df: pd.DataFrame):
        self.name = name
        self.df = df

class Job:

    async def run() -> PipelineResult:
        raise NotImplementedError(".run() must be overrided for the instructions required to run a job")

class PipelineJob(Job):

    def __init__(self, form: MetadataForm):
        self.form = form

class JobRunner:

    def __init__(self): pass

    async def _runtasks(self,*tasks: Job):

        jobs = []

        for t in tasks:
            jobs.append(t.run())

        result = await asyncio.gather(*jobs)

        return result

    def run(self, tasks: List[Job]):

        t = asyncio.run(self._runtasks(*tasks))

        return t
    
    def run_with_pipeline(self, tasks: List[Job]):
        t = asyncio.run(self._runtasks(*tasks))

        table = {}

        result: PipelineResult
        for result in t:
            table[result.name] = result.df

        return table

            

        

        
