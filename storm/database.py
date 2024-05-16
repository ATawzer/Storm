from pymongo import MongoClient
from storm.objects import StormConfig, Playlist, Track, PlaylistTrack, Artist

from .utils.logging import database_logger
from mongoengine import connect


class StormDB:
    """
    A class used to interact with the storm database. Serves as a high-level
    interface API for interacting with the MongoDB database.
    """

    def __init__(self, host="localhost", port=27017, db_name="storm_database"):
        """Initialize the MongoDB client."""
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        connect(db_name, host=host, port=port)

        database_logger.info(f"Connected to MongoDB at {host}:{port}")

    def create_new_storm_config(self, storm_name, input_playlist, target_playlist):
        """Creates a new storm configuration in the database."""
        config = StormConfig(
            storm_name=storm_name,
            input_playlist=input_playlist,
            target_playlist=target_playlist,
        )
        config.save()

        database_logger.info(f"Created new storm configuration: {storm_name}")
        return config

    def get_all_configs(self):
        """Returns all storm configurations as a QuerySet iterator."""
        return StormConfig.objects

    def get_config_by_name(self, storm_name):
        """Returns the storm configuration with the specified name."""
        result = StormConfig.objects(storm_name=storm_name).first()
        if result is None:
            database_logger.warning(
                f"Storm configuration not found, returning empty record: {storm_name}"
            )
            return StormConfig()
        return result

    def update_playlist(self, playlist):
        """Updates the playlist in the database."""
        Playlist.from_json(playlist).save()

        database_logger.info(f"Updated playlist: {playlist['id']}")

    def update_playlist_tracks(self, playlist_id, tracks):
        """Updates the playlist tracks in the database."""
        for track in tracks:
            track.update({"playlist_id": playlist_id})
            PlaylistTrack.from_json(track).save()

        database_logger.info(f"Updated playlist tracks: {len(tracks)}")

    def update_artists_from_tracks(self):
        """
        Creates artists from tracks in the database.

        if the artist already exists it will not update.
        """
        
        Track.objects()
        for track in Track.objects():
            artist = track["artists"]
            if not Artist.objects(artist=artist['id']).first():
                Artist.from_json(artist).save()
