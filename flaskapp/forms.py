from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddMovieForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    year = StringField(label="Year", validators=[DataRequired()])
    description = StringField(label="Description", validators=[DataRequired()])
    rating = StringField(label="Rating", validators=[DataRequired()])
    ranking = StringField(label="Ranking", validators=[DataRequired()])
    review = StringField(label="Review", validators=[DataRequired()])
    img_url = StringField(label="Image URL", validators=[DataRequired()])
    submit = SubmitField(label="Add")


class EditRatingAndReview(FlaskForm):
    rating = StringField(label="Your Rating Out of 10",
                         validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Update")
