from invoke import task
from storm.jobs import ETLPlaylistOperation, ETLArtistAlbums, ETLAlbumTracks, ArtistTrackBuilder
from storm import StormClient, StormDB, StormUserClient
from storm.jobs.base import StormContext

from datetime import datetime, timedelta
import os
import pandas as pd

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
    lyrical_safety = "2zngrEiplX6Z1aAaIWgZ4m"
    ETLPlaylistOperation([instrumental_safety, lyrical_safety]).execute(context)

@task
def extract_artists_from_tracks(c, playlist_id):
    """ Extracts artists from tracks in the database"""
    db = StormDB()
    db.update_artists_from_playlist_tracks(playlist_id)

    return db.get_playlist_artists(playlist_id)

@task
def extract_weekly_artist_albums(c, artists):
    """ Extracts artist albums from Spotify"""
    context = StormContext(StormClient(), StormDB())
    start_date = datetime.now() - timedelta(days=7)
    ETLArtistAlbums(artists, start_date).execute(context)

@task
def extract_missing_album_tracks(c):
    """ Extracts missing album tracks from Spotify"""
    context = StormContext(StormClient(), StormDB())
    ETLAlbumTracks().execute(context)

@task
def run_full_etl(c):
    """ Runs the full ETL job"""

    instrumental_safety = "0R1gw1JbcOFD0r8IzrbtYP"
    lyrical_safety = "2zngrEiplX6Z1aAaIWgZ4m"

    run_playlist_etl(c)
    inst_artists = extract_artists_from_tracks(c, instrumental_safety)
    lyr_artists = extract_artists_from_tracks(c, lyrical_safety)

    extract_weekly_artist_albums(c, inst_artists)
    extract_weekly_artist_albums(c, lyr_artists)

    extract_missing_album_tracks(c)

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
    artists = context.storm_db.get_playlist_artists("0R1gw1JbcOFD0r8IzrbtYP") + context.storm_db.get_playlist_artists("2zngrEiplX6Z1aAaIWgZ4m")
    tracks = ArtistTrackBuilder(artists, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")).execute(context)

    context.storm_user_client.add_tracks_to_playlist_by_name(f"Storm Weekly {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", [track["_id"] for track in tracks], make_new=True, overwrite=True)

@task
def run_many_storms_weekly(c, start_date=None, end_date=datetime.now()):
    """ Runs the storm ETL job weekly"""
    
    dates = pd.date_range(start_date, end_date, freq="W-SUN")
    for i in range(len(dates) - 1):
        run_storm_in_range(c, dates[i].strftime("%Y-%m-%d"), dates[i+1].strftime("%Y-%m-%d"))