import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class WatchUser(models.Model):
    ROLE_CHOICES = (
        ('viewer', 'Viewer'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    password_hash = models.CharField(max_length=255)
    display_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    subtitle_locale = models.CharField(max_length=20, default='en-US')
    avatar_initials = models.CharField(max_length=10, default='PR')
    avatar_color = models.CharField(max_length=30, default='#E50914')
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.display_name} ({self.role})"


class Title(models.Model):
    id = models.CharField(primary_key=True, max_length=50)  # e.g., 't_1001' or 'the-salt-road'
    name = models.CharField(max_length=200)
    episode_info = models.CharField(max_length=200, default='S1 · E4 "The Crossing"')
    duration_seconds = models.IntegerField(default=2730)  # 45m 30s
    video_asset_url = models.CharField(max_length=500, blank=True)
    synopsis = models.TextField()
    genres = models.JSONField(default=list)
    match_percentage = models.IntegerField(default=97)
    rating_tag = models.CharField(max_length=50, default='TV-MA')
    year = models.IntegerField(default=2026)
    episodes_count = models.IntegerField(default=6)
    resolution_badge = models.CharField(max_length=20, default='4K')
    poster_url = models.CharField(max_length=500, blank=True)
    backdrop_url = models.CharField(max_length=500, blank=True)
    is_published = models.BooleanField(default=True)
    schema_version = models.CharField(max_length=20, default='v1.2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.episode_info}"


class TimelineEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('trivia', 'Trivia'),
        ('character', 'Character'),
        ('variation_point', 'Variation Point'),
        ('glossary', 'Glossary'),
    )

    id = models.CharField(primary_key=True, max_length=50)  # e.g., 'evt_3118'
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='timeline_events')
    ts_seconds = models.IntegerField(db_index=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    content = models.TextField()
    source_id = models.CharField(max_length=50, blank=True)
    character_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ts_seconds']
        indexes = [
            models.Index(fields=['title', 'ts_seconds']),
            models.Index(fields=['title', 'event_type']),
        ]

    def __str__(self):
        return f"[{self.ts_seconds}s] {self.event_type}: {self.content[:40]}"


class VariationOption(models.Model):
    timeline_event = models.ForeignKey(TimelineEvent, on_delete=models.CASCADE, related_name='variation_options')
    variation_id = models.CharField(max_length=50)  # e.g., 'v_01'
    option_key = models.CharField(max_length=10)   # 'a', 'b'
    label = models.CharField(max_length=300)
    asset_ref = models.CharField(max_length=200, blank=True)
    vote_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('timeline_event', 'option_key')

    def __str__(self):
        return f"{self.variation_id} [{self.option_key}]: {self.label}"


class WatchSpace(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('ended', 'Ended'),
    )
    VERBOSITY_CHOICES = (
        ('minimal', 'Minimal'),
        ('normal', 'Normal'),
        ('chatty', 'Chatty'),
    )
    PRIVACY_CHOICES = (
        ('invite_only', 'Invite Only'),
        ('public', 'Public Link'),
    )

    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4)  # e.g. 'ws_88231'
    invite_code = models.CharField(max_length=20, unique=True, db_index=True)   # e.g. 'NX-4Q7K'
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='watch_spaces')
    host = models.ForeignKey(WatchUser, on_delete=models.CASCADE, related_name='hosted_spaces')
    room_name = models.CharField(max_length=200, default='Friday Noir Club')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    max_participants = models.IntegerField(default=15)
    ai_verbosity = models.CharField(max_length=20, choices=VERBOSITY_CHOICES, default='normal')
    voting_enabled = models.BooleanField(default=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='invite_only')
    current_playback_ts = models.FloatField(default=812.0)  # default 13:32
    is_playing = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    active_variation = models.JSONField(default=dict, blank=True)
    active_vote = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.room_name} ({self.invite_code}) - {self.status}"


class WatchSpaceParticipant(models.Model):
    ROLE_CHOICES = (
        ('host', 'Host'),
        ('participant', 'Participant'),
    )
    watch_space = models.ForeignKey(WatchSpace, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(WatchUser, on_delete=models.CASCADE, related_name='participant_sessions')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    is_muted = models.BooleanField(default=False)
    connection_quality = models.CharField(max_length=20, default='Excellent')
    drift_ms = models.IntegerField(default=37)
    last_heartbeat = models.DateTimeField(auto_now=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('watch_space', 'user')

    def __str__(self):
        return f"{self.user.display_name} in {self.watch_space.room_name} ({self.role})"


class ChatMessage(models.Model):
    MSG_TYPE_CHOICES = (
        ('chat', 'User Chat'),
        ('ai_answer', 'AI Co-Pilot Answer'),
        ('system', 'System Notification'),
    )

    watch_space = models.ForeignKey(WatchSpace, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(WatchUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    msg_type = models.CharField(max_length=20, choices=MSG_TYPE_CHOICES, default='chat')
    body = models.TextField()
    ts_seconds = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    source_events = models.JSONField(default=list, blank=True)
    is_grounded = models.BooleanField(default=False)
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = self.user.display_name if self.user else self.msg_type.upper()
        return f"[{self.msg_type}] {sender}: {self.body[:30]}"


class Interaction(models.Model):
    user = models.ForeignKey(WatchUser, on_delete=models.CASCADE, related_name='interactions')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='interactions')
    watched_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(default=5)  # 1 to 5
    co_watched_with = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.display_name} -> {self.title.name} ({self.rating} stars)"


class SessionAnalytics(models.Model):
    watch_space = models.OneToOneField(WatchSpace, on_delete=models.CASCADE, related_name='analytics')
    watch_time_seconds = models.IntegerField(default=6120)  # 1h 42m
    peak_viewers = models.IntegerField(default=8)
    ai_questions_count = models.IntegerField(default=23)
    trivia_cards_count = models.IntegerField(default=14)
    chat_messages_count = models.IntegerField(default=186)
    sync_drift_avg_ms = models.IntegerField(default=31)
    sync_drift_peak_ms = models.IntegerField(default=68)
    variations_applied = models.JSONField(default=list, blank=True)
    top_ai_moments = models.JSONField(default=list, blank=True)
    chat_activity_distribution = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.watch_space.room_name} ({self.watch_space.invite_code})"


class UserVideo(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4)
    user = models.ForeignKey(WatchUser, on_delete=models.CASCADE, related_name='uploaded_videos')
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField(default=0)
    duration_seconds = models.IntegerField(default=0)
    content_type = models.CharField(max_length=100, default='video/mp4')
    thumbnail_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.display_name})"

