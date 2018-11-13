from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class SearchForm(FlaskForm):
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    name_song = StringField(u'Song', validators=[DataRequired()])


