from flaskapp import app
from flask import render_template, redirect, url_for, request
from models import Movie, get_all_movies
from flaskapp import db
from flaskapp.forms import AddMovieForm, EditRatingAndReview


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


@app.route("/add")
def add():
    form = AddMovieForm()
    return render_template("add.html", form=form)

    black_adam = Movie(
        title="Black Adam",
        year=2022,
        description="After being bestowed with godly powers and imprisoned for it, Black Adam is liberated from his earthly binds to unleash his fury on the modern world.",
        rating=4.5,
        ranking=1,
        review="Above average. One-time watch.",
        img_url="https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.dc.com%2F2022-11%2FBlack_Adam_S_DD_KA_TT_3000x3000_300dpi_EN.jpeg%3Fw%3D1200&imgrefurl=https%3A%2F%2Fwww.dc.com%2FBlackAdam&tbnid=IVQEWnXYl4HGVM&vet=12ahUKEwjN-Ma8vtj8AhWrjNgFHRrtBRYQMygNegUIARD5AQ..i&docid=T2CdjCllNsHMSM&w=1200&h=1200&itg=1&q=Black%20Adam&ved=2ahUKEwjN-Ma8vtj8AhWrjNgFHRrtBRYQMygNegUIARD5AQ"
    )
    with app.app_context():
        db.session.add(black_adam)
        db.session.commit()
