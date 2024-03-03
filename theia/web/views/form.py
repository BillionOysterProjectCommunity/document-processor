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
from theia.document.processor import DocumentProcessor
from theia.web.forms import MetadataForm
from theia.web.models.metadata import MetaData

from theia.tasks.document import DocumentPipeline
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
    metadata = MetaData()


    if form.validate_on_submit():
        # TODO Add columns O-X from Ambassador Data Entry Google Sheet 

        # TODO Completley refactor the form logic
        # In -> form | out -> csv

        """
        utils.marshal(form) -> 
        # utils.py
        def marshal(form: FlaskForm, obj: any):
            
        """       

        rectangle_tag = form.tag_type.data
        round_tag = form.tag_type.data
        monitoring_date = form.monitoring_date.data
        total_live_oysters = form.total_live_oysters.data
        file = form.image.data
        path = os.path.abspath(os.path.join("web/uploads", file.filename))
        file.save(path)

        document_processor = DocumentProcessor()
        df = document_processor.process_document(path)
        df = df.dropna() # Drop corrupted values

        # Drive.process_ors_document(path)

        broodstock = metadata.get_broodstock()
        set_date = metadata.get_setDate()
        distribution_date = metadata.get_distributionDate()

        df = pd.DataFrame({
            "Round Tag": round_tag,
            "Rectangle Tag": rectangle_tag,
            "Invalid": False,
            "Data_Quality": False,
            "Data_Sheet": "https://drive.google.com",
            "Data_Decisions": False,
            "Monitoring_Date": monitoring_date,
            "Broodstock": broodstock,
            "Set_Date": set_date,
            "Distribution_Date": distribution_date,
            "Clump": False,
            "Live_Oysters_Clump": False,
            "Total_Number_Live_Oysters": total_live_oysters,
            # TODO Continue to add fields
            "shell_height_mm":  df['measurements'],
            "live/dead": df['live/dead']
        })

        df = df.to_csv()

        return render_template("result.html", df=df)
    
    return render_template("form.html", form=form)