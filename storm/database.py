from pymongo import MongoClient
from storm.objects import StormConfig, Playlist, Track, PlaylistTrack, Artist, Album, ArtistBlacklist

from .utils.logging import database_logger
from mongoengine import connect
from mongoengine.queryset.visitor import Q

from datetime import datetime


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

    def update_playlist_tracks(self, playlist_id, tracks, flag_deleted=False):
        """Updates the playlist tracks in the database."""
        for track in tracks:
            track.update({"playlist_id": playlist_id})
            PlaylistTrack.from_json(track).save()

        if flag_deleted:
            for track in PlaylistTrack.objects(playlist_id=playlist_id):
                if track not in tracks:
                    track.soft_delete()
                    track.save()

        database_logger.info(f"Updated playlist tracks: {len(tracks)}")

    def update_artists_from_tracks(self):
        """
        Creates artists from tracks in the database.

        if the artist already exists it will not update.
        """

        Track.objects()
        for track in Track.objects():
            artists = track["artists"]
            for artist in artists:
                artist_id = artist["id"] if "id" in artist else None
                if artist_id:
                    if not Artist.objects(_id=artist_id).first():
                        database_logger.info(
                            f"New artist found in tracks: {artist_id}, {artist['name'] if 'name' in artist else 'No Artist Name'}"
                        )
                        Artist.from_json(artist).save()

        database_logger.info("Updated artists from tracks.")

    def update_artists_from_playlist_tracks(self, playlist_id):
        """Updates the artists from the playlist tracks in the database."""
        tracks = PlaylistTrack.objects(playlist_id=playlist_id)
        for track in tracks:
            for artist in track.get_artists(id_only=False):
                if not Artist.objects(_id=artist["id"]).first():
                    Artist.from_json(artist).save()

        database_logger.info(f"Updated artists from playlist tracks: {len(tracks)}")

    def update_albums_from_artist_albums(self, artist, albums):
        """Updates the artist albums in the database."""
        for album in albums:
            if not Album.objects(_id=album["id"]).first():
                Album.from_json(album).save()

        Artist.objects(_id=artist["_id"]).first().update_album_date()

    def get_artists_for_album_collection(self, start_date, return_missing=True):
        """Returns all artists for the album collection.

        If an end date is provided, only artists with albums updated between
        the start and end date will be returned.

        If an artist has no last_album_update, they will be returned if return_missing is True.
        """
        query = Q()

        if start_date:
            query &= Q(last_album_update__lte=start_date)

        if return_missing:
            query |= Q(last_album_update__exists=False)

        return Artist.objects(query)

    def get_albums_for_track_collection(
        self, start_date=None, only_return_missing=True
    ):
        """Returns all albums for the track collection.

        If an end date is provided, only albums with tracks collected between
        the start and end date will be returned.

        If an album has no tracks_collected_date, they will be returned if return_missing is True.
        """
        query = Q()

        if start_date:
            query &= Q(tracks_collected_date__lte=start_date)

        if only_return_missing:
            query &= Q(tracks_collected_date__exists=False)

        return Album.objects(query)

    def update_tracks_from_album_tracks(self, album_id, tracks):
        """Updates the album tracks in the database."""
        for track in tracks:
            track.update({"album": {"id": album_id}})
            Track.from_json(track).save()

        Album.objects(_id=album_id).first().update_tracks_collected_date()
        database_logger.info(f"Updated album tracks: {len(tracks)}")

    def update_album_track_collection_fail(self, album_id):
        """Updates the album track collection fail count in the database."""
        album = Album.objects(_id=album_id).first()
        album.increment_track_collection_fail_count()
        album.save()

        database_logger.warning(
            f"Album fail count at: {album.track_collection_fail_count} for album: {album_id}"
        )

    def blacklist_artists_from_playlist(self, playlist_id, storm_name):
        """Blacklists artists from the playlist in the database."""
        playlist = Playlist.objects(_id=playlist_id).first()
        artists = playlist.get_artists()
        
        for artist in artists:
            if not ArtistBlacklist.objects(_id=artist["_id"]).first():
                ArtistBlacklist(_id=artist["_id"], storm_name=storm_name).save()

    def get_blacklisted_artists(self, storm_name):
        """Returns all blacklisted artists for the specified storm."""
        return ArtistBlacklist.objects(storm_name=storm_name)
    
    def get_playlist_tracks(self, playlist_id, include_deleted=False):
        """Returns all tracks for the specified playlist."""
        if include_deleted:
            return PlaylistTrack.objects(playlist_id=playlist_id)
        return PlaylistTrack.objects(playlist_id=playlist_id)
    
    def get_playlist_artists(self, playlist_id):
        """Returns all artists for the specified playlist."""
        tracks = self.get_playlist_tracks(playlist_id)
        artists = []
        for track in tracks:
            artists.extend(track.get_artists())
        return list(set(artists))
    
    def get_artist_albums(self, artist_id):
        """Returns all albums for the specified artist."""
        albums = Album.objects.all()
        return [album for album in albums if any(artist['id'] == artist_id for artist in album.artists)]

    def get_artist_albums_by_date(self, artist_id, start_date, end_date):
        """Returns all albums for the specified artist between the specified dates."""
        
        query = Q()
        if start_date:
            query &= Q(release_date__gte=start_date)
        if end_date:
            query &= Q(release_date__lte=end_date)
        
        albums = Album.objects(query)
        return [album for album in albums if any(artist['id'] == artist_id for artist in album.artists)]

    def get_artist_tracks(self, artist_id):
        """Returns all tracks where artist_id is in the "artist" list on the track."""
        tracks = Track.objects.all()
        return [track for track in tracks if any(artist['id'] == artist_id for artist in track.artists)]

    def get_artist_tracks_by_date(self, artist_id, start_date, end_date):
        """Returns all tracks for the specified artist between the specified dates"""
        albums = self.get_artist_albums_by_date(artist_id, start_date, end_date)
        tracks = []
        for album in albums:
            album_tracks = Track.objects.filter(album__id=album['_id'])
            tracks.extend(album_tracks)
        
        return tracks

