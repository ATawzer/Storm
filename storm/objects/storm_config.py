from mongoengine import Document, StringField


class StormConfig(Document):
    """
    A class used to represent a storm configuration in the database.

    Attributes
    ----------
    input_playlist : StringField
        The name of the input playlist. This will be used to get a list of
        artists to get tracks for.
    target_playlist : StringField
        The name of the target playlist. This where storm runs will be
        written to.
    """

    input_playlist = StringField(required=True)
    target_playlist = StringField(required=True)

    meta = {"collection": "storm_config"}
