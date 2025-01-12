from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token
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
        results = self.sp.artist_albums(artist_id, album_type="album,single")
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
        auth_manager = spotipy.oauth2.SpotifyOAuth(scope="playlist-modify-private playlist-modify-public", cache_path=".cache", show_dialog=True, open_browser=True, username=user_id, redirect_uri="http://localhost/")
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

        self.user_id = user_id

    def add_tracks_to_playlist(self, playlist_id, track_ids, overwrite=False):
        """Write tracks to a playlist in batches."""
        batch_size = 100  # Spotify's limit for adding tracks in a single request
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]

            if overwrite and i == 0:
                self.sp.user_playlist_replace_tracks(self.user_id, playlist_id, batch)
                client_logger.info(f"Replaced tracks in playlist: {playlist_id}")
                continue

            self.sp.user_playlist_add_tracks(self.user_id, playlist_id, batch)

        client_logger.info(f"Added a total of {len(track_ids)} tracks to playlist: {playlist_id}")

    def add_tracks_to_playlist_by_name(self, playlist_name, track_ids, make_new=False, overwrite=False):
        """Add tracks to a playlist by name."""
        playlist_id = self.get_playlist_id_by_name(playlist_name)
        if not playlist_id and make_new:
            playlist_id = self.create_playlist(playlist_name)
        self.add_tracks_to_playlist(playlist_id, track_ids, overwrite=overwrite)

    def get_playlist_id_by_name(self, playlist_name):
        """Get the ID of a playlist by name."""
        playlists = self.sp.current_user_playlists()
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                return playlist["id"]

        client_logger.error(f"Playlist not found: {playlist_name}")
        return None

    def create_playlist(self, playlist_name):
        """Create a new playlist."""
        playlist = self.sp.user_playlist_create(self.user_id, playlist_name)
        playlist_id = playlist["id"]

        client_logger.info(f"Created new playlist: {playlist_id}")
        return playlist_id

    def add_tracks_to_new_playlist(self, track_ids, playlist_name):
        """Create a new playlist and add tracks to it."""
        playlist_id = self.create_playlist(playlist_name)
        self.add_tracks_to_playlist(playlist_id, track_ids)

        return playlist_id
