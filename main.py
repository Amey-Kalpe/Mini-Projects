from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from forms import CreatePostForm, RegistrationForm, LoginForm, CommentForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap(app)

# Gravatar
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)

##CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

##FLASK lOGIN
login_manager = LoginManager()
login_manager.init_app(app)


def admin_only(func):
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            func()

        return abort(403)

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


##CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comments", back_populates="posts")
    author = relationship("User", back_populates="posts")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    comments = relationship("Comments", back_populates="author")
    posts = relationship("BlogPost", back_populates="author")


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    posts = relationship("BlogPost", back_populates="comments")
    author = relationship("User", back_populates="comments")
    # One-to-Many relationship between User and Comments


# db.create_all()


@app.route("/")
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template(
        "index.html", all_posts=posts, logged_in=current_user.is_authenticated
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()
    if request.method == "POST":
        if registration_form.validate_on_submit():
            req_form = request.form
            user = User.query.filter_by(email=req_form.get("email")).first()
            if user:
                flash("User already exists. Please login instead.")
                return redirect(url_for("login"))
            name = req_form.get("name")
            email = req_form.get("email")
            password = req_form.get("password")
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(password, salt_length=8),
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=registration_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            req_form = request.form
            user = User.query.filter_by(email=req_form.get("email")).first()
            if not user:
                flash(
                    "This user doesn't exist. Please register first.", category="error"
                )
                return redirect(url_for("register"))
            valid = check_password_hash(user.password, req_form.get("password"))

            if valid:
                login_user(user)

                next_ = request.args.get("next")

                if not is_safe_url(next_):
                    return abort(400)

                return redirect(next_ or url_for("get_all_posts"))

        flash("Invalid Credentials. Please try to login again.", category="error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login to proceed.")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comment_form = CommentForm()
    comments = Comments.query.filter_by(post_id=post_id).all()
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Please login to comment.")
            return redirect(url_for("login"))

        if comment_form.validate_on_submit():
            comment_text = request.form.get("comment")
            comment = Comments(
                text=comment_text, author_id=current_user.id, post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post_id))
    return render_template(
        "post.html",
        post=requested_post,
        comment_form=comment_form,
        logged_in=current_user.is_authenticated,
        comments=comments,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@admin_only
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img_url=form.img_url.data,
                author=current_user,
                date=date.today().strftime("%B %d, %Y"),
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@admin_only
@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@admin_only
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
