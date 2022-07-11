import requests


class Post:
    def __init__(self) -> None:
        self.posts = []
        self.blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
        self.load_posts()

    def load_posts(self):
        response = requests.get(self.blog_url)
        self.posts = response.json()

    def get_post(self, id_):
        for post in self.posts:
            if post["id"] == id_:
                return post
