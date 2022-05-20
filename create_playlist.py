# Creates a playlist for a user

import argparse
import logging
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger("examples.create_playlist")
logging.basicConfig(level="DEBUG")


def get_args():
    parser = argparse.ArgumentParser(description="Creates a playlist for user")
    parser.add_argument("-p", "--playlist", required=True, help="BillBoard Top 100")
    parser.add_argument(
        "-d",
        "--description",
        required=False,
        default="",
        help="Top 100 Billboard tracks.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope,
        )
    )
    user_id = sp.me()["id"]
    sp.user_playlist_create(user_id, args.playlist)


if __name__ == "__main__":
    main()
