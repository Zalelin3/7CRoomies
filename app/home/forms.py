from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, FieldList, IntegerField, SelectField,BooleanField
from wtforms.validators import DataRequired, EqualTo
# from wtforms.ext.sqlachemy.fields import QuerySelectField
from ..models import Post, Pet, User, On_campus, Off_campus

class FilterForm(FlaskForm):
    #not done yet
    """
    Form for usrs to input the condition to filter post
    """
    school = IntegerField('school')
    pet = SelectField(BooleanField('pet'))
    capacity = IntegerField('capacity')
    nSingles= IntegerField('nSingles')
    nDoubles= IntegerField('nDoubles')
    nTriples= IntegerField('nTriples')
    nQuads= IntegerField('nQuads')
    partyFreq= IntegerField('partyFreq')
    visitorFreq= IntegerField('visitorFreq')
    bedtime= IntegerField('bedtime')
    noiseSen= IntegerField('noiseSen')
    allowed_gender= IntegerField('allowed_gender')
    submit = SubmitField('Filter')