from mongoengine import (
    Document,
    StringField,
    DictField,
    ListField,
    IntField,
    DateTimeField,
)

from datetime import datetime


class Artist(Document):
    """
    A class used to represent an artist in the database.

    Attributes
    ----------
    artist_name : StringField
        The name of the artist.
    genres : ListField
        The genres of the artist.
    popularity : IntField
        The popularity of the artist.
    """

    name = StringField(required=True)
    external_urls = DictField()
    followers = DictField()
    genres = ListField()
    href = StringField()
    popularity = IntField()
    _id = StringField(required=True, primary_key=True)
    images = ListField()
    type = StringField()
    last_updated = DateTimeField()
    last_album_update = DateTimeField()

    meta = {"collection": "artist"}

    def from_json(json):
        """Creates an Artist object from a JSON object."""
        return Artist(
            _id=json["id"],
            name=json["name"],
            external_urls=json["external_urls"] if "external_urls" in json else None,
            followers=json["followers"] if "followers" in json else {},
            genres=json["genres"] if "genres" in json else [],
            href=json["href"] if "href" in json else None,
            popularity=json["popularity"] if "popularity" in json else None,
            images=json["images"] if "images" in json else [],
            type=json["type"] if "type" in json else None,
            last_updated=datetime.now(),
        )

    def update_album_date(self):
        """Updates the last album update date."""
        self.last_album_update = datetime.now()
        self.save()

class ArtistBlacklist(Document):
    """
    A class used to represent an artist blacklist in the database.
    These are members that should not be included in the specified storm run.

    Attributes
    ----------
    artist_id : StringField
        The ID of the artist to blacklist.
    """

    artist_id = StringField(required=True, primary_key=True)
    storm_name = StringField(required=True)
    blacklist_type = StringField()

    meta = {"collection": "artist_blacklist"}