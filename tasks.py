from invoke import task
from storm.jobs import ETLPlaylistOperation, ETLArtistAlbums, ETLAlbumTracks, ArtistTrackBuilder
from storm import StormClient, StormDB, StormUserClient
from storm.jobs.base import StormContext

from datetime import datetime, timedelta
import os

@task
def test(c, format=True, lint=True):
    """ Runs a full test suite"""
    if format:
        c.run("invoke format")
    if lint:
        c.run("invoke lint")
    c.run("pytest ./tests --cov=storm --cov-report=term-missing")

@task
def lint(c):
    """ Runs flake8 on the project"""
    c.run("flake8 ./storm")

@task
def format(c):
    """ Runs black on the project"""
    c.run("black ./storm")

@task
def run_playlist_etl(c):
    """ Runs the playlist ETL job"""
    context = StormContext(StormClient(), StormDB())
    instrumental_safety = "0R1gw1JbcOFD0r8IzrbtYP"
    ETLPlaylistOperation([instrumental_safety]).execute(context)

@task
def extract_artists_from_tracks(c):
    """ Extracts artists from tracks in the database"""
    db = StormDB()
    db.update_artists_from_tracks()

@task
def extract_weekly_artist_albums(c):
    """ Extracts artist albums from Spotify"""
    context = StormContext(StormClient(), StormDB())
    start_date = datetime.now() - timedelta(days=7)
    ETLArtistAlbums(start_date).execute(context)

@task
def extract_missing_album_tracks(c):
    """ Extracts missing album tracks from Spotify"""
    context = StormContext(StormClient(), StormDB())
    ETLAlbumTracks().execute(context)

@task
def run_storm_in_range(c, start_date=None, end_date=None):
    """ Runs the storm ETL job in a date range"""
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if not end_date:
        end_date = datetime.now()
    else:    
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    context = StormContext(StormClient(), StormDB(), StormUserClient(os.getenv("SPOTIFY_USER_ID")))
    artists = context.storm_db.get_playlist_artists("0R1gw1JbcOFD0r8IzrbtYP")
    tracks = ArtistTrackBuilder(artists, start_date, end_date).execute(context)

    context.storm_user_client.add_tracks_to_new_playlist(tracks, f"Storm {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    