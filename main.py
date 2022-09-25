import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

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
playlist = sp.playlist(playlist_id)
tracks = playlist["tracks"]["items"]


track_ids = [track["track"]["id"] for track in tracks]

audio_features = sp.audio_features(track_ids)
bpms = [af["tempo"] for af in audio_features]
assert len(track_ids) == len(bpms)


min_bpm = 100
max_bpm = 110

filtered_songs = []
for track_id, bpm in zip(track_ids, bpms):
    if (bpm >= min_bpm) and (bpm <= max_bpm):
        filtered_songs.append(track_id)

# TODO: create a new playlist with just these filtered songs
# user_playlist_create(user, name, public=True, collaborative=False, description='')


# add items to playlist
# playlist_add_items(playlist_id, items, position=None)


breakpoint()
