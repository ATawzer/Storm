from mongoengine import (
    Document,
    StringField,
    DictField,
    ListField,
    IntField,
    DateTimeField,
)

from datetime import datetime

class Album(Document):
    """
    A class used to represent an album in the database.

    Attributes
    ----------
    album_name : StringField
        The name of the album.
    artists : ListField
        The artists of the album.
    release_date : StringField
        The release date of the album.
    """

    album_type = StringField()
    total_tracks = IntField()
    artists = ListField()
    available_markets = ListField()
    external_urls = DictField()
    href = StringField()
    images = ListField()
    name = StringField(required=True)
    release_date = StringField()
    release_date_precision = StringField()
    restrictions = DictField()
    type = StringField()
    uri = StringField()
    _id = StringField(required=True, primary_key=True)
    album_group = StringField()
    last_updated = DateTimeField()
    tracks_collected_date = DateTimeField()
    track_collection_fail_count = IntField()

    meta = {"collection": "album"}

    def from_json(json):
        """Creates an Album object from a JSON object."""
        return Album(
            _id=json["id"],
            album_type=json["album_type"] if "album_type" in json else None,
            total_tracks=json["total_tracks"] if "total_tracks" in json else None,
            artists=json["artists"] if "artists" in json else [],
            available_markets=json["available_markets"] if "available_markets" in json else [],
            external_urls=json["external_urls"] if "external_urls" in json else {},
            href=json["href"] if "href" in json else None,
            images=json["images"] if "images" in json else [],
            name=json["name"],
            release_date=json["release_date"] if "release_date" in json else None,
            release_date_precision=json["release_date_precision"] if "release_date_precision" in json else None,
            restrictions=json["restrictions"] if "restrictions" in json else {},
            type=json["type"] if "type" in json else None,
            uri=json["uri"] if "uri" in json else None,
            last_updated=datetime.now()
        )
    
    def update_tracks_collected_date(self):
        """Updates the tracks collected date."""
        self.tracks_collected_date = datetime.now()
        self.save()

    def increment_track_collection_fail_count(self):
        """Increments the track collection fail count."""
        if not self.track_collection_fail_count:
            self.track_collection_fail_count = 0
        self.track_collection_fail_count += 1
        self.save()