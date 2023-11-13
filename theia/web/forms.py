from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileField,
    FileRequired
)  
from wtforms.fields import (
    SelectField,
    DateField,
    IntegerField
)

from wtforms.validators import DataRequired

# NOTE: field data is accessed through form.field.data

class MetadataForm(FlaskForm):
    tag_type = SelectField('Tag Type', choices=['Rectangle', 'Circle'])
    monitoring_date = DateField('Monitoring Date', validators=[DataRequired()])
    total_live_oysters = IntegerField('Total Live Oysters', validators=[DataRequired()])
    image = FileField('Measurement Image',validators=[FileRequired()])
    # NOTE: enctype="multipart/form-data" on <form></form> for the .data property to be present on
    #       the file.

