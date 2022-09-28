import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_spotipy_client():
    auth_manager = SpotifyOAuth(
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        redirect_uri="https://example.com/callback",
        scope="user-library-read",
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


sp = get_spotipy_client()


class Playlist:
    # NOTE: may want to change this to just take the playlist id
    def __init__(self, js, with_bpm=False):
        self.js = js
        self.name = js["name"]
        self.id = js["id"]
        self.uri = js["uri"]
        self.tracks = self.get_tracks(with_bpm)

    def get_tracks(self, with_bpm=False):
        raw_tracks = self.js["tracks"]["items"]
        tracks = [Track(rt["track"]) for rt in raw_tracks]
        bpms = get_bpms_from_tracks(tracks)
        if with_bpm:
            for track, bpm in zip(tracks, bpms):
                track.bpm = bpm
        return tracks

    def __str__(self):
        return self.name

    def get_tracks_in_bpm_range(self, min_bpm, max_bpm):
        return get_tracks_in_bpm_range(self.tracks, min_bpm, max_bpm)


class Track:
    def __init__(self, js, with_bpm=False):
        self.js = js
        self.name = js["name"]
        self.id = js["id"]
        self.uri = js["uri"]
        if with_bpm:
            self.bpm = self.get_bpm()

    def get_bpm(self):
        afs = sp.audio_features([self.id])
        assert len(afs) == 1
        return afs[0]["tempo"]

    def __str__(self):
        return self.name


def get_bpms_from_tracks(tracks: list[Track]):
    track_ids = [track.id for track in tracks]
    audio_features = sp.audio_features(track_ids)
    bpms = [float(af["tempo"]) for af in audio_features]
    assert len(track_ids) == len(bpms)
    return bpms


def get_tracks_in_bpm_range(tracks, min_bpm, max_bpm):
    """Return only the tracks within the bpm range (inclusive)."""

    # filter function
    def track_is_in_bpm_range(track):
        return min_bpm <= track.bpm <= max_bpm

    tracks_in_bpm_range = filter(track_is_in_bpm_range, tracks)
    return list(tracks_in_bpm_range)


def add_bpm_subset_to_new_playlist(
    source_playlist_id, target_playlist_id, min_bpm, max_bpm
):
    # take a playlist
    # extract all the songs within a bpm range
    # add those songs to another playlist
    pass


def list_my_playlist_names_and_ids():
    """Return a list of playlists, their name and id."""
    items = sp.current_user_playlists()["items"]
    return [{k: item[k] for k in ["name", "id"]} for item in items]


def delete_all_tracks_in_playlist(playlist_id):
    js = sp.playlist(playlist_id)
    target_playlist = Playlist(js)
    target_playlist_track_ids = [t.id for t in target_playlist.tracks]
    sp.playlist_remove_all_occurrences_of_items(playlist_id, target_playlist_track_ids)
