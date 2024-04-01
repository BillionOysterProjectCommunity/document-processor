from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileField,
    FileRequired
)  
from wtforms.fields import (
    SelectField,
    SelectMultipleField,
    DateField,
    IntegerField,
    StringField
)

from wtforms.widgets.core import DateInput

from wtforms.validators import DataRequired

# NOTE: field data is accessed through form.field.data

class MetadataForm(FlaskForm):
    organization = StringField('Organization', validators=[DataRequired()])
    steward_name = StringField('Steward Name', validators=[DataRequired()])
    steward_email = StringField('Steward Email', validators=[DataRequired()])
    location = SelectField('Location')
    tag_type = SelectField('Tag Type', choices=['Rectangle', 'Circle'])
    tag_number = IntegerField('Tag Number')
    monitoring_date = DateField('Monitoring Date', validators=[DataRequired()], widget=DateInput())
    total_live_oysters = IntegerField('Total Live Oysters', validators=[DataRequired()])
    image = FileField('Measurement Image',validators=[FileRequired()])
    # NOTE: enctype="multipart/form-data" on <form></form> for the .data property to be present on
    #       the file.

class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    roles = SelectMultipleField('Roles', choices=['admin', 'user'])

class DeleteUserForm(FlaskForm):
    email = StringField('Email')