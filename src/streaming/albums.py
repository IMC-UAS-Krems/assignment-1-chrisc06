from streaming.tracks import AlbumTrack
from streaming.artists import Artist

class Album:
    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    # Adds a track to the album. It also sets the track's album property, sorted by track number.
    def add_track(self, track):
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self):
        return {t.track_id for t in self.tracks}

    def duration_seconds(self):
        total_duration = 0.0
        for track in self.tracks:
            total_duration += track.duration
        return total_duration
