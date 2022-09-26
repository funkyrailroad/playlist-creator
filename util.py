import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

auth_manager = SpotifyOAuth(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
    redirect_uri="https://example.com/callback",
    scope="user-library-read",
)

sp = spotipy.Spotify(auth_manager=auth_manager)


class Playlist:
    def __init__(self, js, with_bpm=False):
        self.js = js
        self.name = js['name']
        self.id = js['id']
        self.uri = js['uri']
        self.tracks = self.get_tracks(with_bpm)

    def get_tracks(self, with_bpm=False):
        raw_tracks = self.js["tracks"]["items"]
        tracks = [Track(rt["track"]) for rt in raw_tracks]
        return tracks

    def __str__(self):
        return self.name


class Track:
    def __init__(self, js, with_bpm=False):
        self.js = js
        self.name = js['name']
        self.id = js['id']
        self.uri = js['uri']
        if with_bpm:
            self.bpm = sp.audio_features([self.id])

    def __str__(self):
        return self.name


def get_bpms_from_tracks(tracks: list[Track]):
    track_ids = [track.id for track in tracks]
    audio_features = sp.audio_features(track_ids)
    bpms = [float(af["tempo"]) for af in audio_features]
    assert len(track_ids) == len(bpms)
    return bpms
