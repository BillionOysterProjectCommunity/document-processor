import asyncio
from typing import (
    List,
    Dict
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
    
    def run_with_pipeline(self, tasks: List[Job]) -> Dict[str, PipelineResult]:
        t = asyncio.run(self._runtasks(*tasks))

        table = {}

        result: PipelineResult
        for result in t:
            table[result.name] = result.df

        return table

    def marshal_results(self, data: Dict[str, PipelineResult]) -> pd.DataFrame:
        """
        marshals a compiled table of PipeLineResults and converges the
        DataFrames into a regular 2D DataFrame consistent of all the columns
        from all the tables
        """
        flat = {}

        for table in data.keys():
            for col in data[table].columns.values.tolist():
                d = data[table][col].values.tolist()
                flat[col] = d

        df = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in flat.items()]))

        categorical = []

        for k in flat.keys():
            if len(flat[k]) == 1:
                categorical.append(k)

        for col in categorical:
            first = df[col].iloc[0]
            df[col].fillna(first, inplace=True)

        return df