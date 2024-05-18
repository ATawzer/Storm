from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DictField,
    DateTimeField,
)
from .track import Track

from datetime import datetime


class Playlist(Document):
    """
    A class used to represent a playlist in the database.

    Attributes
    ----------
    playlist_name : StringField
        The name of the playlist, is a unique identifier.
    tracks : ListField
        A list of tracks in the playlist.
    """

    name = StringField(required=True)
    tracks = ListField()
    owner = DictField()
    _id = StringField(required=True, primary_key=True)
    public = BooleanField()
    collaborative = BooleanField()
    description = StringField()
    followers = DictField()
    snapshot_id = StringField()
    type = StringField()
    sys_last_updated = DateTimeField()

    meta = {"collection": "playlist"}

    def from_json(json):
        """Creates a Playlist object from a JSON object."""
        return Playlist(
            _id=json["id"],
            name=json["name"],
            tracks=json["tracks"] if "tracks" in json else [],
            owner=json["owner"] if "owner" in json else None,
            public=json["public"] if "public" in json else None,
            collaborative=json["collaborative"] if "collaborative" in json else None,
            description=json["description"] if "description" in json else None,
            followers=json["followers"] if "followers" in json else {},
            snapshot_id=json["snapshot_id"] if "snapshot_id" in json else None,
            type=json["type"] if "type" in json else None,
            sys_last_updated=datetime.now(),
        )


class PlaylistTrack(Document):
    """
    Class used to represent a playlist item in the database, these are returned
    from the playlist endpoint in the Spotify API, contain tracks.

    Attributes
    ----------
    playlist_id : StringField
        The ID of the playlist
    track: DictField
        The track object
    track_id: StringField
        The ID of the track
    added_at: StringField
        The date the track was added to the playlist
    added_by: DictField
        The user who added the track
    is_local: BooleanField
        Whether the track is local or not
    """

    playlist_id = StringField(required=True)
    track = DictField(required=True)
    track_id = StringField(required=True)
    added_at = StringField()
    added_by = DictField()
    is_local = BooleanField()
    _id = StringField(required=True, primary_key=True)
    sys_last_updated = DateTimeField()
    sys_is_deleted = BooleanField(default=False)

    meta = {"collection": "playlist_track"}

    def from_json(json):
        """Creates a PlaylistTrack object from a JSON object."""
        return PlaylistTrack(
            _id=json["track"]["id"] + json["playlist_id"],
            playlist_id=json["playlist_id"],
            track=json["track"],
            track_id=json["track"]["id"],
            added_at=json["added_at"],
            added_by=json["added_by"],
            is_local=json["is_local"],
            sys_last_updated=datetime.now(),
        )

    def save(self):
        """Saves the playlist item to the database."""
        super().save()
        self.save_track()

    def save_track(self):
        """Saves the nested track from the playlist item."""
        track = Track.from_json(self.track)
        track.save()

    def get_artists(self):
        """Returns a list of artists for the track."""
        return [x["id"] for x in self.track["artists"]]
    
    def soft_delete(self):
        """Soft deletes the playlist track."""
        self.sys_last_updated = datetime.now()
        self.sys_is_deleted = True
        self.save()
