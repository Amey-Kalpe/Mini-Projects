import os
from flaskapp import app
from flaskapp import db
from flaskapp.forms import EditRatingAndReview, AddMovieForm
from flask import render_template, redirect, url_for, request
from models import Movie, get_all_movies
from dotenv import load_dotenv
import requests

load_dotenv()


@app.route("/")
def home():
    return render_template("index.html", movies=get_all_movies())


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    edit_form = EditRatingAndReview()

    if request.method == "POST":
        if edit_form.validate_on_submit():
            form = request.form
            movie = Movie.query.get(movie_id)
            movie.rating = form.get("rating")
            movie.review = form.get("review")
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("edit.html", form=edit_form, movie_id=movie_id)


@app.route("/delete/<int:movie_id>", methods=["GET"])
def delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()

    if request.method == "POST":
        params = {
            "api_key": os.getenv("MOVIE_API_KEY"),
            "query": request.form.get("title")
        }
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_response = requests.get(search_url, params=params)
        movie_id = search_response.json().get("results")[0].get("id")
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        details_response = requests.get(
            details_url, params={"api_key": params["api_key"]})

    # TODO:
    # Add button redirects to '/select'
    # After a movie is selected, that movie's id from api response should be passed to '/add'
    # Redirect to '/edit' after movie is added successfully

    return render_template("add.html", form=form)

    with app.app_context():
        # db.session.add(new_movie)
        db.session.commit()
