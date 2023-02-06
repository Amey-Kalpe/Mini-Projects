from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()


app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config["CKEDITOR_PKG_TYPE"] = "basic"
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


## util functions
def row_to_dict(rows):
    return [
        {
            "id": row.id,
            "title": row.title,
            "subtitle": row.subtitle,
            "date": row.date,
            "body": row.body,
            "author": row.author,
            "img_url": row.img_url,
        }
        for row in rows
    ]


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


def fetch_posts():
    return row_to_dict(BlogPost.query.all())


@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=fetch_posts())


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in fetch_posts():
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        author=post.author,
        img_url=post.img_url,
    )
    if form.validate_on_submit():
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        post.author = form.author.data
        db.session.commit()
        return redirect(url_for("show_post", index=post.id))

    return render_template("make-post.html", form=form, header="Edit Post")


@app.route("/new-post", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            req_form = request.form
            post = BlogPost(
                title=req_form.get("title"),
                subtitle=req_form.get("subtitle"),
                date=datetime.now().strftime("%B %d, %Y"),
                author=req_form.get("author"),
                body=req_form.get("body"),
                img_url=req_form.get("img_url"),
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, header="New Post")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    BlogPost.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
