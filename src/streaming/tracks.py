from abc import ABC, abstractmethod # I don't really understand the purpose, studied from https://www.datacamp.com/tutorial/python-abstract-classes
from datetime import date

class Track(ABC):
    def __init__(self, track_id, title, duration, genre):
        self.track_id = track_id
        self.title = title
        self.duration = duration
        self.genre = genre

    def play(self):
        pass

    def duration_minutes(self):
        return self.duration / 60.0

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __hash__(self):
        return hash(self.track_id)

class Song(Track):
    def __init__(self, track_id, title, duration, genre, artist):
        super().__init__(track_id, title, duration, genre)
        self.artist = artist

class SingleRelease(Song):
    def __init__(self, track_id, title, duration, genre, artist, release_date=None):
        super().__init__(track_id, title, duration, genre, artist)
        self.release_date = release_date

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration, genre, artist, track_number):
        super().__init__(track_id, title, duration, genre, artist)
        self.track_number = track_number
        self.album = None

class Podcast(Track):
    def __init__(self, track_id, title, duration, genre, host, description=""):
        super().__init__(track_id, title, duration, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration, genre, host, guest, description=""):
        super().__init__(track_id, title, duration, genre, host, description)
        self.guest = guest

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration, genre, host, season, episode_number, description=""):
        super().__init__(track_id, title, duration, genre, host, description)
        self.season = season
        self.episode_number = episode_number

class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration, genre, author, narrator):
        super().__init__(track_id, title, duration, genre)
        self.author = author
        self.narrator = narrator
