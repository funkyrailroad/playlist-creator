import argparse

from util import (
    Playlist,
    get_bpms_from_tracks,
    get_spotipy_client,
    get_tracks_in_bpm_range,
)

parser = argparse.ArgumentParser(
    prog="The Musical Metronome Playlist Creator",
    description="Create a new playlist with songs in a given BPM range",
)

parser.add_argument("playlist_id")
parser.add_argument("min_bpm")
parser.add_argument("max_bpm")

args = parser.parse_args()


sp = get_spotipy_client()
user_info = sp.current_user()
user_id = user_info["id"]

playlist_id = args.playlist_id
raw_playlist = sp.playlist(playlist_id)

playlist = Playlist(raw_playlist, with_bpm=True)
playlist_id = playlist.id
raw_tracks = raw_playlist["tracks"]["items"]
tracks = playlist.tracks
bpms = get_bpms_from_tracks(tracks)

min_bpm = args.min_bpm
max_bpm = args.max_bpm

tracks_in_bpm_range = get_tracks_in_bpm_range(tracks, min_bpm, max_bpm)


# create a new raw_playlist with just these filtered songs
new_playlist_name = f"{playlist.name}: {min_bpm}-{max_bpm} BPM"
new_pl = sp.user_playlist_create(
    user_id, new_playlist_name, public=False, collaborative=False
)
new_pl_id = new_pl["id"]

# add items to raw_playlist
sp.playlist_add_items(new_pl_id, [track.id for track in tracks_in_bpm_range])
