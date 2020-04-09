from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, FieldList, IntegerField
from wtforms.validators import DataRequired, EqualTo

from ..models import Post, Pet, User, On_campus, Off_campus

class FilterForm(FlaskForm):
    #not done yet
    """
    Form for usrs to input the condition to filter post
    """
    authors = FieldList(StringField('Name', [validators.required()]))

    submit = SubmitField('Filter')