class Playlist:
    def __init__(self, js):
        self.js = js
        self.name = js['name']
        self.id = js['id']
        self.uri = js['uri']
        self.tracks = self.get_tracks()

    def get_tracks(self):
        raw_tracks = self.js["tracks"]["items"]
        tracks = [Track(rt["track"]) for rt in raw_tracks]
        return tracks

    def __str__(self):
        return self.name


class Track:
    def __init__(self, js):
        self.js = js
        self.name = js['name']
        self.id = js['id']
        self.uri = js['uri']

    def __str__(self):
        return self.name
