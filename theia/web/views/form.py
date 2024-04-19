from flask import (
    Blueprint,
    render_template,
    session,
)

import pandas as pd

from theia.web.middleware import login_required
from theia.web.forms import MetadataForm
from theia.web.utils import upload_dir, package_dir

from theia.tasks.document import DocumentPipeline
from theia.tasks.storage import StoragePipeline
from theia.tasks.cage import CagePipeline
from theia.tasks.drive import DrivePipeline
from theia.tasks.measurements import MeasurementPipeline
from theia.tasks.metadata import MetadataPipeline
from theia.tasks.job import JobRunner

entry = Blueprint("entry", __name__, url_prefix="/f", template_folder="templates")


@entry.route("/form", methods=("GET", "POST"))
@login_required
def form():

    form = MetadataForm()
    location_csv = package_dir() + "web/" + "views/" + "location.csv"
    locations = pd.read_csv(location_csv)
    form.location.choices = list(locations["Site"])

    if form.validate_on_submit():

        file = form.image.data
        path = upload_dir(file.filename)
        file.save(path)
        dp = DocumentPipeline(path)
        cage = CagePipeline(form)
        measurements = MeasurementPipeline(form)
        metadata = MetadataPipeline(form)
        st = StoragePipeline(form)

        runner = JobRunner()
        table = runner.run_with_pipeline([dp, cage, measurements, metadata, st])

        df = runner.marshal_results(table)

        print(df)

        # Convert to a csv-like string form downloading on the client side as a csv file
        df = df.to_csv()

        return render_template("result.html", df=df)

    return render_template("form.html", form=form)
