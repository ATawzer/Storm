from mongoengine import Document, StringField, ObjectIdField, ListField


class StormConfig(Document):
    """
    A class used to represent a storm configuration in the database.

    Attributes
    ----------
    storm_name : StringField
        The name of the storm configuration, is a unique identifier.
    input_playlist : StringField
        The name of the input playlist. This will be used to get a list of
        artists to get tracks for.
    target_playlist : StringField
        The name of the target playlist. This where storm runs will be
        written to.
    """

    storm_name = StringField(required=True, primary_key=True)
    input_playlists = ListField()
    artist_blacklist_playlist = StringField()

    meta = {"collection": "storm_config"}
