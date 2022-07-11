from flask import Flask, render_template
from post import Post

app = Flask(__name__)
posts = Post()


@app.route("/")
def home():
    all_posts = posts.posts
    return render_template("index.html", posts=all_posts)


@app.route("/blog/<int:id_>")
def get_blog(id_):
    post = posts.get_post(id_)
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
