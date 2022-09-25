import os
import unittest

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from util import Playlist, Track


class Tests(unittest.TestCase):
    def setUp(self):
        oauth_manager = SpotifyOAuth(
            client_id=os.environ["SPOTIPY_CLIENT_ID"],
            client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
            redirect_uri="https://example.com/callback",
            scope="user-library-read",
        )
        self.sp = spotipy.Spotify(auth_manager=oauth_manager)
        self.raw_playlist = self.get_example_raw_playlist()
        self.raw_track = self.get_example_raw_track()
        self.playlist = Playlist(self.raw_playlist)
        self.tracks = self.playlist.tracks
        self.track = self.tracks[0]

    def get_example_raw_track(self):
        raw_tracks = self.raw_playlist["tracks"]["items"]
        return raw_tracks[0]['track']

    def get_example_raw_playlist(self):
        playlists = self.sp.current_user_playlists()["items"]
        playlist_id = playlists[0]["id"]
        return self.sp.playlist(playlist_id)

    def test_playlist_attributes(self):
        playlist = self.playlist
        self.assertEqual(playlist.name, self.raw_playlist['name'])
        self.assertEqual(playlist.id, self.raw_playlist['id'])
        self.assertEqual(playlist.uri, self.raw_playlist['uri'])
        self.assertIsInstance(playlist.tracks, list)
        self.assertIsInstance(playlist.tracks[0], Track)

    def test_track_attributes(self):
        track = self.track
        self.assertEqual(track.name, self.raw_track['name'])
        self.assertEqual(track.id, self.raw_track['id'])
        self.assertEqual(track.uri, self.raw_track['uri'])
