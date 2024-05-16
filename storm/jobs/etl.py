from .base import StormOperation, StormContext
from storm.utils.logging import etl_logger


class ETLPlaylistOperation(StormOperation):
    """
    Extracts data from Spotify and loads it into the database.
    """

    def __init__(self, playlist_ids):
        self.playlist_ids = playlist_ids

    def execute(self, context):
        """
        Execute the operation.
        """

        for playlist_id in self.playlist_ids:
            self.extract_load_playlist(context, playlist_id)

    def extract_load_playlist(self, context, playlist_id):
        # Extract data from Spotify

        etl_logger.info(f"Extracting data from Spotify: {playlist_id}")
        playlist = context.storm_client.get_playlist_metadata(playlist_id)

        etl_logger.info(f"Extracted {len(tracks)} tracks from Spotify")
        etl_logger.info(f"Synchronizing data with database...")
        context.storm_db.update_playlist(playlist)
        context.storm_db.update_playlist_tracks(playlist_id, tracks)
        etl_logger.info(f"Data synchronized with database for playlist: {playlist_id}, {playlist['name']}")
