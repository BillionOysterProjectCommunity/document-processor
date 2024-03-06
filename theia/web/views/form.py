import os

import pandas as pd

from flask import (
    Flask, 
    Blueprint,
    current_app,
    request, 
    redirect, 
    render_template,
    session, 
    url_for
)

from theia.web.middleware import login_required
from theia.web.forms import MetadataForm
from theia.web.utils import upload_dir

from theia.tasks.document import DocumentPipeline
from theia.tasks.cage import CagePipeline
from theia.tasks.drive import DrivePipeline
from theia.tasks.measurements import MeasurementPipeline
from theia.tasks.job import JobRunner

entry = Blueprint(
    'entry', 
    __name__, 
    url_prefix='/f',
    template_folder="templates"
    )

config = current_app

@entry.route("/form", methods=('GET', 'POST'))
@login_required
def form():

    form = MetadataForm()

    if form.validate_on_submit():
        # TODO Add columns O-X from Ambassador Data Entry Google Sheet 
        
        file = form.image.data
        path = upload_dir(file.filename)
        file.save(path)
        dp = DocumentPipeline(path)
        cage = CagePipeline(form)
        drive = DrivePipeline(form)
        measurements = MeasurementPipeline(form)

        runner = JobRunner()
        table = runner.run_with_pipeline([
            dp,
            cage,
            drive,
            measurements
        ])

        df = runner.marshal_results(table)

        df = df.to_csv()

        return render_template("result.html", df=df)
    
    return render_template("form.html", form=form)