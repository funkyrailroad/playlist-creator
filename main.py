from util import (
    Playlist,
    get_bpms_from_tracks,
    get_spotipy_client,
    get_tracks_in_bpm_range,
)

sp = get_spotipy_client()

playlists = sp.current_user_playlists()["items"]
playlist_id = playlists[0]["id"]
raw_playlist = sp.playlist(playlist_id)

playlist = Playlist(raw_playlist, with_bpm=True)
raw_tracks = raw_playlist["tracks"]["items"]
tracks = playlist.tracks
bpms = get_bpms_from_tracks(tracks)

min_bpm = 100
max_bpm = 110

tracks_in_bpm_range = get_tracks_in_bpm_range(tracks, min_bpm, max_bpm)


# TODO: create a new raw_playlist with just these filtered songs
# user_playlist_create(user, name, public=True, collaborative=False, description='')

# add items to raw_playlist
# playlist_add_items(playlist_id, items, position=None)
