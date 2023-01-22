from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddMovieForm(FlaskForm):
    title = StringField(label="Title", name="title",
                        validators=[DataRequired()])
    submit = SubmitField(label="Add")


class EditRatingAndReview(FlaskForm):
    rating = StringField(label="Your Rating Out of 10", name="rating",
                         validators=[DataRequired()])
    review = StringField(label="Your Review", name="review",
                         validators=[DataRequired()])
    submit = SubmitField(label="Update")
