from flaskapp import db, app


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(30), unique=True, nullable=False)
    year = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"({self.title}, {self.year}, {self.description})"


def get_all_movies():
    with app.app_context():
        return Movie.query.all()


if __name__ == "__main__":
    pass
