import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from util import Playlist, Track, get_bpms_from_tracks

auth_manager = SpotifyClientCredentials(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
)

auth_manager = SpotifyOAuth(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
    redirect_uri="https://example.com/callback",
    scope="user-library-read",
)

sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.current_user_playlists()["items"]

playlist_id = playlists[0]["id"]
raw_playlist = sp.playlist(playlist_id)
playlist = Playlist(raw_playlist)
raw_tracks = raw_playlist["tracks"]["items"]
tracks = [Track(rt["track"]) for rt in raw_tracks]
bpms = get_bpms_from_tracks(tracks)

min_bpm = 100
max_bpm = 110

filtered_songs = []
for track, bpm in zip(tracks, bpms):
    if min_bpm <= bpm <= max_bpm:
        filtered_songs.append(track)

# TODO: create a new raw_playlist with just these filtered songs
# user_playlist_create(user, name, public=True, collaborative=False, description='')

# add items to raw_playlist
# playlist_add_items(playlist_id, items, position=None)
