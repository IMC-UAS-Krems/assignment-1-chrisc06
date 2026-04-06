from datetime import date

class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0.0
        for session in self.sessions:
            total += session.duration_listened_seconds
        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self):
        unique_ids = set()
        for session in self.sessions:
            unique_ids.add(session.track.track_id)
        return unique_ids

class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)

class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = [] 

    def add_sub_user(self, member):
        self.sub_users.append(member)

    def all_members(self):
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent
