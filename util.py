class Playlist:
    def __init__(self, js):
        self.js = js
        self.name = js['name']
        self.id = js['id']
        self.uri = js['uri']
