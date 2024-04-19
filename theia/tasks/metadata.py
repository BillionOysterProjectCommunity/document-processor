import pandas as pd

from theia.tasks.fields import (
    BROODSTOCK,
    SET_DATE,
    DISTRIBUTION_DATE,
    TAG_NUMBER,
    MONITORING_DATE,
    ORGANIZATION,
    LOCATION,
    STEWARD_EMAIL,
    STEWARD_NAME,
)

from theia.web.forms import MetadataForm
from theia.tasks.job import PipelineJob, PipelineResult
from theia.settings.config import pkg_dir


class MetadataPipeline(PipelineJob):

    NAME = "metadata"

    def __init__(self, form: MetadataForm):
        super().__init__(form)

    async def run(self) -> PipelineResult:
        b = broodstock(str(self.form.tag_number.data))

        df = pd.DataFrame(
            {
                BROODSTOCK: b.broodstock,
                DISTRIBUTION_DATE: b.distribution,
                SET_DATE: b.distribution,
                TAG_NUMBER: self.form.tag_number.data,
                MONITORING_DATE: self.form.monitoring_date.data,
                ORGANIZATION: self.form.organization.data,
                LOCATION: self.form.location.data,
                STEWARD_NAME: self.form.steward_name.data,
                STEWARD_EMAIL: self.form.steward_email.data,
            },
            index=[0],
        )

        return PipelineResult(self.NAME, df)

class Broodstock:
    def __init__(self, broodstock, distribution):
        self.broodstock = broodstock
        self.distribution = distribution

def broodstock(tag_number):
    p = pkg_dir() + "/" + "tasks" "/" + "broodstock.csv"
    df = pd.read_csv(p)

    bd = Broodstock("None", "None")

    # attempt to extract cage id

    df = df[df["tag_number"] == tag_number]

    installation = ["d", "c", "b", "a"]
    for i in range(len(installation)):
        try: 
            b = df[f"broodstock_{installation[i]}"].values[0]
            d = df[f"distribution_{installation[i]}"].values[0]
            if type(b) == str and not "None":  # return the most recent broostock install (not NaN)
                bd.broodstock = b
                bd.distribution = d
                return bd
        except IndexError:
            pass
    return bd

