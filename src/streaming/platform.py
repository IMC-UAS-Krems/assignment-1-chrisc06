from datetime import datetime, date, timedelta

from streaming.tracks import Track, Song, AlbumTrack, Podcast, AudiobookTrack
from streaming.users import User, FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.artists import Artist
from streaming.albums import Album
from streaming.playlists import Playlist, CollaborativePlaylist
from streaming.sessions import ListeningSession

# This class manages mostly everything about the streaming platform, I've done something similar with an online game im working on aswell, a class that stores all the playerdata.
class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self._catalogue = {}
        self._users = {} 
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track):
        self._catalogue[track.track_id] = track

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id):
        return self._catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())

    # Q1: Calculate the total listening time across all users for a given period.
    def total_listening_time_minutes(self, start, end):
        total_time_seconds = 0.0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_time_seconds += session.duration_listened_seconds
        return total_time_seconds / 60.0

    # Q2: Compute the average number of unique tracks listened to by premium users.
    def avg_unique_tracks_per_premium_user(self, days=30):
        premium_users = []
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)

        if not premium_users:
            return 0.0

        total_unique_tracks = 0
        now = datetime.now()

        for user in premium_users:
            unique_tracks_for_user = set()
            for session in user.sessions:
                if (now - session.timestamp).days <= days:
                    unique_tracks_for_user.add(session.track.track_id)
            total_unique_tracks += len(unique_tracks_for_user)

        return total_unique_tracks / len(premium_users)

    # Q3: Find the track that has been listened to by the most different users.
    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None

        track_listeners_count = {}
        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            if track_id not in track_listeners_count:
                track_listeners_count[track_id] = set()
            track_listeners_count[track_id].add(user_id)

        if not track_listeners_count:
            return None

        most_distinct_track_id = None
        max_distinct_listeners = -1

        for track_id, listeners_set in track_listeners_count.items():
            if len(listeners_set) > max_distinct_listeners:
                max_distinct_listeners = len(listeners_set)
                most_distinct_track_id = track_id

        return self._catalogue.get(most_distinct_track_id)

    # Q4: Calculate the average session duration for each type of user.
    def avg_session_duration_by_user_type(self):
        user_type_durations = {}
        for session in self._sessions:
            user_type_name = type(session.user).__name__
            if user_type_name not in user_type_durations:
                user_type_durations[user_type_name] = []
            user_type_durations[user_type_name].append(session.duration_listened_seconds)

        avg_durations_list = []
        for user_type, durations in user_type_durations.items():
            if durations:
                average = sum(durations) / len(durations)
                avg_durations_list.append((user_type, average))


        avg_durations_list.sort(key=lambda x: x[1], reverse=True)
        return avg_durations_list

    # Q5: Calculate the total listening time for sub-users who are under a certain age.
    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total_seconds = 0.0
        for session in self._sessions:
            if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

    # Q6: Find the top N artists based on their total listening time.
    def top_artists_by_listening_time(self, n=5):
        artist_total_time = {}
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist_id = session.track.artist.artist_id
                artist_total_time[artist_id] = artist_total_time.get(artist_id, 0.0) + session.duration_listened_seconds

        sorted_artists_by_time = sorted(artist_total_time.items(), key=lambda item: item[1], reverse=True)

        result = []
        for artist_id, total_seconds in sorted_artists_by_time[:n]:
            artist = self._artists.get(artist_id)
            if artist:
                result.append((artist, total_seconds / 60.0))
        return result

    # Q7: Determine a user's most listened-to genre and what percentage of their total listening time it represents.
    def user_top_genre(self, user_id):
        user = self.get_user(user_id)
        if not user or not user.sessions:
            return None

        genre_listening_time = {}
        total_listening_time_user = 0.0

        for session in user.sessions:
            genre = session.track.genre
            duration = session.duration_listened_seconds
            genre_listening_time[genre] = genre_listening_time.get(genre, 0.0) + duration
            total_listening_time_user += duration

        if total_listening_time_user == 0:
            return None

        top_genre = max(genre_listening_time.items(), key=lambda item: item[1])[0]
        top_genre_time = genre_listening_time[top_genre]
        percentage = (top_genre_time / total_listening_time_user) * 100.0

        return (top_genre, percentage)

    # Q8: Find collaborative playlists that contain songs from more than a specified number of distinct artists.
    def collaborative_playlists_with_many_artists(self, threshold=3):
        matching_playlists = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                distinct_artists_in_playlist = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        distinct_artists_in_playlist.add(track.artist.artist_id)
                
                if len(distinct_artists_in_playlist) > threshold:
                    matching_playlists.append(playlist)
        return matching_playlists

    # Q9: Calculate the average number of tracks per playlist, separated by playlist type.
    def avg_tracks_per_playlist_type(self):
        playlist_counts = {"Playlist": 0, "CollaborativePlaylist": 0}
        playlist_track_sums = {"Playlist": 0, "CollaborativePlaylist": 0}

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                playlist_type_name = "CollaborativePlaylist"
            else:
                playlist_type_name = "Playlist"
            
            playlist_counts[playlist_type_name] += 1
            playlist_track_sums[playlist_type_name] += len(playlist.tracks)

        averages = {}
        for p_type in playlist_counts:
            if playlist_counts[p_type] > 0:
                averages[p_type] = playlist_track_sums[p_type] / playlist_counts[p_type]
            else:
                averages[p_type] = 0.0
        return averages

    # Q10: Identify users who have listened to every track on at least one complete album.
    def users_who_completed_albums(self):
        results = []
        for user in self._users.values():
            user_listened_track_ids = {session.track.track_id for session in user.sessions}
            
            completed_album_titles = []
            for album in self._albums.values():
                if album.tracks: 
                    album_track_ids = album.track_ids()
                    if album_track_ids.issubset(user_listened_track_ids):
                        completed_album_titles.append(album.title)

            if completed_album_titles:
                results.append((user, completed_album_titles))
        return results
