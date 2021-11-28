# Module in charge of creating the forms needed to be rendered in the html files

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    rating = StringField(label='Your rating out of 10', name='rating', validators=[DataRequired()])
    review = StringField(label='Your review', name='review', validators=[DataRequired()])
    submit = SubmitField('Submit', name='submit')


class AddForm(FlaskForm):
    title = StringField(label='Movie Title', name='title', validators=[DataRequired()])
    submit = SubmitField('Submit', name='submit')