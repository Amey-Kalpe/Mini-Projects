from sqlalchemy import func
import random
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# util functions


def row_to_dict(rows):
    return list(map(lambda row: {
        "name": row.name,
        "map_url": row.map_url,
        "img_url": row.img_url,
        "location": row.location,
        "seats": row.seats,
        "has_toilet": row.has_toilet,
        "has_wifi": row.has_wifi,
        "has_sockets": row.has_sockets,
        "can_take_calls": row.can_take_calls,
        "coffee_price": row.coffee_price
    }, rows))

# Cafe TABLE Configuration


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random_cafe():
    max_id = db.session.query(func.max(Cafe.id)).scalar()
    random_id = random.randint(1, max_id)
    cafe = Cafe.query.get(random_id)
    return jsonify(row_to_dict([cafe]))


@app.route("/all", methods=["GET"])
def get_all_cafes():
    all_cafes = Cafe.query.all()
    return jsonify(row_to_dict(all_cafes))


@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("loc")
    cafes = Cafe.query.filter(Cafe.location.like(f"%{location}%")).all()

    return jsonify(row_to_dict(cafes)) if cafes else {
        "Not Found": "Sorry, we do not have a cafe at that location."
    }


# HTTP POST - Create Record
# HTTP PUT/PATCH - Update Record
# HTTP DELETE - Delete Record
if __name__ == '__main__':
    app.run(debug=True)
