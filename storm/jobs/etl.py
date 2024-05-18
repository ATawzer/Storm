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
        tracks = context.storm_client.get_playlist_tracks(playlist_id)

        etl_logger.info(f"Extracted {len(tracks)} tracks from Spotify")
        etl_logger.info(f"Synchronizing data with database...")

        context.storm_db.update_playlist(playlist)
        context.storm_db.update_playlist_tracks(playlist_id, tracks, flag_deleted=True)

        etl_logger.info(
            f"Data synchronized with database for playlist: {playlist_id}, {playlist['name']}"
        )


class ETLArtistAlbums(StormOperation):
    """
    Extracts all of an artists albums from Spotify and loads them into the database.

    Currently filters on the update date for the artists.
    """

    def __init__(self, album_start_date):
        self.album_start_date = album_start_date

    def execute(self, context):
        """
        Execute the operation.
        """

        etl_logger.info(
            f"Extracting data from Spotify for artist albums updated between: {self.album_start_date}"
        )

        artists = context.storm_db.get_artists_for_album_collection(
            self.album_start_date
        )
        for artist in artists:
            albums = context.storm_client.get_artist_albums(artist["_id"])
            context.storm_db.update_albums_from_artist_albums(artist, albums)

            etl_logger.info(
                f"Extracted {len(albums)} albums for artist: {artist['_id']}, {artist['name']}"
            )

        etl_logger.info(
            f"Data synchronized with database for artist albums updated prior to: {self.album_start_date}"
        )


class ETLAlbumTracks(StormOperation):
    """
    Extracts all of an albums tracks from Spotify and loads them into the database.
    """

    def __init__(self, album_last_collected_date=None):
        self.album_last_collected_date = album_last_collected_date

    def execute(self, context):
        """
        Execute the operation.
        """

        etl_logger.info(
            f"Extracting data from Spotify for album tracks not updated since prior to: {self.album_last_collected_date}"
        )

        albums = context.storm_db.get_albums_for_track_collection(
            self.album_last_collected_date, only_return_missing=True
        )
        for album in albums:
            tracks = context.storm_client.get_album_tracks(album["_id"])

            if len(tracks) > 0:
                context.storm_db.update_tracks_from_album_tracks(album["_id"], tracks)
                etl_logger.info(
                    f"Extracted {len(tracks)} tracks for album: {album['_id']}, {album['name']}"
                )

            else:
                context.storm_db.update_album_track_collection_fail(album["_id"])

        etl_logger.info(
            f"Data synchronized with database for album tracks updated prior to: {self.album_last_collected_date}"
        )