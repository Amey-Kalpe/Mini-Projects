import spotipy
from bs4 import BeautifulSoup
import requests
from spotipy import SpotifyOAuth

import add_tracks_to_playlist as add_tracks

scope = "playlist-modify-public"

date = input(
    "Which year do you want to travel to? Enter date in this format: YYYY-MM-DD\n"
)

year = date.split("-")[0]

url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url)

content = response.text

soup = BeautifulSoup(content, "html.parser")

all_songs = soup.select(selector="div li h3#title-of-a-story")

song_titles = [song.getText().strip() for song in all_songs]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

song_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} not found. Skipping.")

# TODO: -------Assign any playlist name here--------
playlist = "Billboard Top 100"

# TODO: ------- Use this code block to generate playlist id with a specific owner id -------
# result = sp.search(q=f"playlist:{playlist}", type="playlist")
# for item in result["playlists"]["items"]:
#     if item["owner"]["id"] == "ameydude":
#         playlist_id = item["id"]
#         break

add_tracks.main(playlist_id, song_uris)
