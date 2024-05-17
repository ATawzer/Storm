from invoke import task
from storm.jobs import ETLPlaylistOperation, ETLArtistAlbums, ETLAlbumTracks
from storm import StormClient, StormDB
from storm.jobs.base import StormContext

from datetime import datetime, timedelta

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
    