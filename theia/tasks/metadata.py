import pandas as pd

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult
from theia.settings.config import pkg_dir

class MetadataPipeline(PipelineJob):

    NAME = "metadata"

    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:
        # TOTAL_CUMULATIVE_LIVE_OYSTER = "total_number_live_oysters"
        # df = pd.DataFrame({
        #     TOTAL_CUMULATIVE_LIVE_OYSTER: self.form.total_live_oysters.data
        # }, index=[0])

        BROODSTOCK = "broodstock"

        df = pd.DataFrame({
            BROODSTOCK: broodstock(str(self.form.tag_number.data))
        }, index=[0])

        return PipelineResult(self.NAME, df)

def broodstock(tag_number):
  p = pkg_dir() + "/" + "tasks" "/" + "broodstock.csv"
  df = pd.read_csv(p)

  # attempt to extract cage id
  try:
    df = df[df['tag_number'] == tag_number]

    # TODO: column based time-series data forces the user to iterate
    # in a list-like manner. Fix all install dates categories by using a time-series datastore
    installation = ['d', 'c', 'b', 'a']
    for i in range(len(installation)):
      v = df[f'broodstock_{installation[i]}'].values[0]
      print(v)
      if type(v) == str: # return the most recent broostock install (not NaN)
        return v
    # No broodstock identifiers found, return None
    return None

  # cage id not present in database
  except (KeyError):
    return None

