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
    
    def get_artist_albums(self, artist_id):
        """Get all albums by an artist."""
        albums = []
        results = self.sp.artist_albums(artist_id)
        while results:
            albums.extend(results["items"])
            results = self.sp.next(results)
        return albums
    
    def get_album_tracks(self, album_id):
        """Get all tracks from an album."""
        tracks = []

        try:
            results = self.sp.album_tracks(album_id)
            while results:
                tracks.extend(results["items"])
                results = self.sp.next(results)
            return tracks
        except Exception as e:
            client_logger.error(f"Error getting album tracks for album: {album_id}")
            return tracks
    
class StormUserClient:
    """
    Storm Client with user permissions. Needed for writing to a user's account.
    """
    def __init__(self, user_id):
        # Initialize Spotipy client
        client_credentials_manager = SpotifyClientCredentials(user_id=user_id)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def write_tracks_to_playlist(self, playlist_id, track_ids):
        """Write tracks to a playlist."""
        self.sp.user_playlist_add_tracks(playlist_id, track_ids)

        client_logger.info(f"Added {len(track_ids)} tracks to playlist: {playlist_id}")