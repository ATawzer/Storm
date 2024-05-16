from storm.jobs.etl import ETLPlaylistOperation
from storm.jobs.base import StormContext
from storm import StormClient, StormDB

import pytest

# Define MongoDB test database settings
TEST_HOST = 'localhost'
TEST_PORT = 27017
TEST_DB_NAME = 'test_storm_database'

@pytest.fixture
def storm_context():

    # Initialize StormClient and StormDB
    storm_client = StormClient()
    storm_db = StormDB(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB_NAME)

    # Initialize StormContext with the StormClient and StormDB
    context = StormContext(storm_client, storm_db)
    yield context


def test_etl_playlist_operation(storm_context):
    test_playlists = ["1Jhuw695S6WhcQIJNEVWdc", "2N9YXYN64MhO0Pz5jok6WM"]

    ETLPlaylistOperation(test_playlists).execute(storm_context)