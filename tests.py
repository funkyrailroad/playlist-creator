from pprint import pprint
import unittest

from util import (
    Playlist,
    Track,
    add_bpm_subset_to_new_playlist,
    delete_all_tracks_in_playlist,
    get_bpms_from_tracks,
    get_spotipy_client,
    get_tracks_in_bpm_range,
    list_my_playlist_names_and_ids,
)


class Tests(unittest.TestCase):
    def setUp(self):
        self.sp = get_spotipy_client()
        self.raw_playlist = self.get_example_raw_playlist()
        self.raw_track = self.get_example_raw_track()
        self.playlist = Playlist(self.raw_playlist, with_bpm=True)
        self.tracks = self.playlist.tracks
        self.track = Track(self.raw_track, with_bpm=True)
        self.target_playlist_id = "7InKckkWA9HT6mF3BTcCiZ"

    def get_example_raw_track(self):
        raw_tracks = self.raw_playlist["tracks"]["items"]
        return raw_tracks[0]["track"]

    def get_example_raw_playlist(self):
        playlists = self.sp.current_user_playlists()["items"]
        playlist_id = playlists[0]["id"]
        return self.sp.playlist(playlist_id)

    def test_playlist_attributes(self):
        playlist = self.playlist
        self.assertEqual(playlist.name, self.raw_playlist["name"])
        self.assertEqual(playlist.id, self.raw_playlist["id"])
        self.assertEqual(playlist.uri, self.raw_playlist["uri"])
        self.assertIsInstance(playlist.tracks, list)
        self.assertIsInstance(playlist.tracks[0], Track)
        self.assertIsInstance(playlist.tracks[0].bpm, float)

    def test_track_attributes(self):
        track = self.track
        self.assertEqual(track.name, self.raw_track["name"])
        self.assertEqual(track.id, self.raw_track["id"])
        self.assertEqual(track.uri, self.raw_track["uri"])
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

    def test_add_bpm_subset_to_new_playlist(self):
        self.fluxfm_playlist_id = "7hTt6Urb1Nfaxdz0GjbX2A"
        # source_playlist_id =
        min_bpm = 100
        max_bpm = 110
        add_bpm_subset_to_new_playlist(
            self.fluxfm_playlist_id, self.target_playlist_id, min_bpm, max_bpm
        )

    def test_list_my_playlist_names_and_ids(self):
        playlists = list_my_playlist_names_and_ids()
        for playlist in playlists:
            self.assertIn("name", playlist)
            self.assertIn("id", playlist)


#     def test_delete_all_tracks_in_playlist(self):
#         delete_all_tracks_in_playlist(self.target_playlist_id)
#         js = self.sp.playlist(self.target_playlist_id)
#         target_playlist = Playlist(js)
#         self.assertEqual(len(target_playlist.tracks), 0)
