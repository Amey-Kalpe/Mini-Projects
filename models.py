from flaskapp import db, app


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(30), unique=True, nullable=False)
    year = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"({self.title}, {self.year}, {self.description})"


def get_ranked_movies():
    """Fetch all movies from the database and update the rank 
    by rating in ascending order.

    Returns:
        list: ranked movies 
    """
    with app.app_context():
        ranked_movies = Movie.query.order_by(Movie.rating)
        for index, movie in enumerate(ranked_movies):
            movie.ranking = 10 - index
            db.session.commit()

        return ranked_movies


if __name__ == "__main__":
    with app.app_context():
        Movie.__table__.drop()
        db.create_all()
