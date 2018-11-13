from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class Form(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Cognome', validators=[DataRequired()])
    password = PasswordField('Password')

class UpdateForm(FlaskForm):
    photo = FileField("Carica un file", validators=[FileRequired()])