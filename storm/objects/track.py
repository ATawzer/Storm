from mongoengine import (
    Document,
    StringField,
    DictField,
    ListField,
    IntField,
    BooleanField,
    DateTimeField,
)

from datetime import datetime


class Track(Document):
    """
    A class used to represent a track in the database.

    Attributes
    ----------
    track_name : StringField
        The name of the track.
    artists : ListField
        The artists of the track.
    album : StringField
        The album of the track.
    duration : StringField
        The duration of the track.
    """

    artists = ListField(required=True)
    album = DictField(required=True)
    available_markets = ListField()
    disc_number = IntField()
    duration_ms = IntField()
    explicit = BooleanField()
    href = StringField()
    name = StringField(required=True)
    popularity = IntField()
    preview_url = StringField()
    track_number = IntField()
    type = StringField()
    uri = StringField()
    _id = StringField(required=True, primary_key=True)
    last_updated = DateTimeField()

    meta = {"collection": "track"}

    def from_json(json):
        """Creates a Track object from a JSON object."""

        if "name" not in json:
            raise ValueError("Track name is required.")
        if "artists" not in json:
            raise ValueError("Track artists are required.")
        if "album" not in json:
            raise ValueError("Track album is required.")
        if "id" not in json:
            raise ValueError("Track ID is required.")

        return Track(
            _id=json["id"],
            artists=json["artists"],
            album=json["album"],
            available_markets=(
                json["available_markets"] if "available_markets" in json else None
            ),
            disc_number=json["disc_number"] if "disc_number" in json else None,
            duration_ms=json["duration_ms"] if "duration_ms" in json else None,
            explicit=json["explicit"] if "explicit" in json else None,
            href=json["href"] if "href" in json else None,
            name=json["name"],
            popularity=json["popularity"] if "popularity" in json else None,
            preview_url=json["preview_url"] if "preview_url" in json else None,
            track_number=json["track_number"] if "track_number" in json else None,
            type=json["type"] if "type" in json else None,
            uri=json["uri"] if "uri" in json else None,
            last_updated=datetime.now(),
        )
