from .etl import ETLPlaylistOperation, ETLArtistAlbums, ETLAlbumTracks  # noqa: F401
from .base import StormContext, StormOperation  # noqa: F401

from storm.utils.logging import etl_logger

class ArtistTrackBuilder(StormOperation):
    """
    Generates a list of tracks based on artists.
    """

    def __init__(self, artists, start_date=None, end_date=None, target_playlist=None):
        self.artists = artists
        self.start_date = start_date
        self.end_date = end_date
        self.target_playlist = target_playlist

    def execute(self, context):
        """
        Execute the operation.
        """

        etl_logger.info(f"Building tracks for {len(self.artists)} artists, releases between {self.start_date} and {self.end_date}.")
        tracks = []

        for artist in self.artists:
            artist_tracks = context.storm_db.get_artist_tracks_by_date(artist, self.start_date, self.end_date)
            tracks.extend(artist_tracks)

        etl_logger.info(f"{len(tracks)} tracks found")
        return tracks

