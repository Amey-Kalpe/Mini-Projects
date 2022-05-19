import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

titles = soup.find_all("h3", class_="title")

titles = [title.getText() for title in titles[::-1]]

with open("Empire's 100 Greatest Movies of all time.txt", "w") as movies:
    for title in titles:
        movies.write(title + "\n")
