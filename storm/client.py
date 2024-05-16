from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .utils.logging import client_logger


class StormClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Initialize Spotipy client
        client_credentials_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_playlist_tracks(self, playlist_id):
        """Get all tracks from a playlist."""
        items = []
        results = self.sp.playlist_tracks(playlist_id)
        while results:
            items.extend(results["items"])
            results = self.sp.next(results)
        return items

    def get_playlist_metadata(self, playlist_id):
        """Get data about a playlist."""
        # Get all data on playlist
        fields = "collaborative, description, followers, id, name, owner, public, snapshot_id, type"
        playlist = self.sp.playlist(playlist_id, fields=fields)
        return playlist
