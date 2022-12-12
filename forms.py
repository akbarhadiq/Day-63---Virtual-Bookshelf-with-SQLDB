from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired(), Length(min=1, max=250, message="You either does not fill the form, or your book title is greater than 250 characters")])
    author = StringField("Author", validators=[DataRequired(), Length(min=1, max=250, message="You either does not fill the form, or your book title is greater than 250 characters")])
    rating = FloatField("Rating", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditRating(FlaskForm):
    hidden_id = HiddenField()
    rating = FloatField("Change Rating", validators=[DataRequired()])
    submit = SubmitField("Edit Rating")