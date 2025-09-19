DEPRECATED: This project relied on the audio features endpoint from the
Spotify API. That has been deprecated for applications not yet granted
extended mode Web API access. See [this notice](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api).

A somewhat related functionality can be achieved with [this website](http://sortyourmusic.playlistmachinery.com/index.html).

# Background

As a music listener, discovering new music and listening to new playlists is
an incredibly rewarding (although fairly boring and time-consuming) endeavor.
As a drummer, practicing new beats and fills at a consistent tempo set by a
metronome is an incredibly rewarding (although fairly boring and
time-consuming) endeavor.

The goal of this project was to create playlists that facilitate combining
these activities to allow for more musically-rich practice sessions and more
productive music discovery sessions.


# Usage

Prepare a virtual environment and install the requirements
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Get the id of a playlist of interest. In the case of this Spotify playlist URL:
```
https://open.spotify.com/playlist/1jGRJQrJkNSC9OKRxEjxoe?si=8c702edc41354ad0
```
The playlist id is `1jGRJQrJkNSC9OKRxEjxoe`.

Run the program and pass the playlist id, min_bpm and max_bpm as parameters:
```
python main.py <playlist_id> <min_bpm> <max_bpm>
```
