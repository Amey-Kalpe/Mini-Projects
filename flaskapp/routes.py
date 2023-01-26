import os
from flaskapp import app
from flaskapp import db
from flaskapp.forms import EditRatingAndReview, AddMovieForm
from flask import render_template, redirect, url_for, request
from models import Movie, get_ranked_movies
from dotenv import load_dotenv
import requests

load_dotenv()


@app.route("/")
def home():
    return render_template("index.html", movies=get_ranked_movies())


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


@app.route("/select", methods=["POST"])
def select():
    params = {
        "api_key": os.getenv("MOVIE_API_KEY"),
        "query": request.form.get("title")
    }
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_response = requests.get(search_url, params=params)
    results = search_response.json().get("results")
    return render_template("select.html", results=results)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()

    movie_id = request.args.get("movie_id")
    if movie_id:
        params = {
            "api_key": os.getenv("MOVIE_API_KEY")
        }
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        resp_json = requests.get(
            details_url, params={"api_key": params["api_key"]}).json()

        poster_img = resp_json.get('poster_path')
        image_url = f"https://image.tmdb.org/t/p/w500{poster_img}"

        new_movie = Movie(
            id=movie_id,
            title=resp_json.get("original_title"),
            year=resp_json.get("release_date"),
            description=resp_json.get("overview"),
            img_url=image_url
        )
        with app.app_context():
            db.session.add(new_movie)
            db.session.commit()

        return redirect(url_for('edit', movie_id=movie_id))

    return render_template("add.html", form=form)


@app.route("/clear")
def clear():
    with app.app_context():
        Movie.__table__.drop(db.engine)
