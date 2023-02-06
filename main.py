from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "some secret key"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Flask Login functions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req_form = request.form
        user = User(
            email=req_form.get("email"),
            password=generate_password_hash(
                req_form.get("password"), method="pbkdf2:sha256", salt_length=8),
            name=req_form.get("name")
        )
        db.session.add(user)
        db.session.commit()
        return render_template("secrets.html", name=req_form.get("name"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        req_form = request.form
        user = User.query.filter_by(email=req_form.get("email")).scalar()
        user = User(email=user.email, password=user.password, name=user.name)
        
        valid = check_password_hash(
            User.query.filter_by(email=req_form.get("email")).scalar().password,
            req_form.get("password")
            )
        
        if valid:
            login_user(user)
        
            next_ = request.args.get("next")
            
            if not is_safe_url(next_):
                return abort(400)
            
            return redirect(next_ or url_for("secrets"))
        
        flash("Bad Credentials! Please login again.")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("./static/files", "cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
