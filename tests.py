import os
import unittest

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from util import Playlist, Track, get_bpms_from_tracks, get_tracks_in_bpm_range


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
        self.playlist = Playlist(self.raw_playlist, with_bpm=True)
        self.tracks = self.playlist.tracks
        self.track = Track(self.raw_track, with_bpm=True)

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
        self.assertIsInstance(playlist.tracks[0].bpm, float)

    def test_track_attributes(self):
        track = self.track
        self.assertEqual(track.name, self.raw_track['name'])
        self.assertEqual(track.id, self.raw_track['id'])
        self.assertEqual(track.uri, self.raw_track['uri'])
        self.assertIsInstance(track.bpm, float)

    def test_get_bpms(self):
        bpms = get_bpms_from_tracks(self.tracks)
        self.assertIsInstance(bpms, list)
        self.assertIsInstance(bpms[0], float)

    def test_get_tracks_in_bpm_range(self):
        min_bpm = 100
        max_bpm = 110
        new_tracks = get_tracks_in_bpm_range(self.tracks, min_bpm, max_bpm)
        for nt in new_tracks:
            self.assertGreaterEqual(nt.bpm, min_bpm)
            self.assertLessEqual(nt.bpm, max_bpm)
