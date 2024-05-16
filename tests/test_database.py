import pytest
from pymongo import MongoClient
from pymongo.collection import Collection
from storm.database import StormDB
from storm.objects.storm_config import StormConfig

# Define MongoDB test database settings
TEST_HOST = 'localhost'
TEST_PORT = 27017
TEST_DB_NAME = 'test_storm_database'

@pytest.fixture
def storm_db():
    # Initialize StormDB with the test MongoDB collection
    storm_db = StormDB(host=TEST_HOST, port=TEST_PORT, db_name=TEST_DB_NAME)
    yield storm_db
    storm_db.client.drop_database(TEST_DB_NAME)

def test_create_new_storm_config(storm_db):
    # Call the method to create a new storm configuration
    input_playlist = "input_playlist_id"
    target_playlist = "target_playlist_id"
    storm_name = "test_storm"
    config = storm_db.create_new_storm_config(storm_name, input_playlist, target_playlist)

    # Verify that the method returns a StormConfig object
    assert isinstance(config, StormConfig)

    # Verify that the document was inserted into the test MongoDB collection
    assert storm_db.db.get_collection('storm_config').count_documents({}) == 1

def test_get_all_configs(storm_db):
    storm_db.create_new_storm_config("test_storm1", "input1", "target1")
    storm_db.create_new_storm_config("test_storm2", "input2", "target2")

    # Call the method to get all storm configurations
    configs = storm_db.get_all_configs()

    # Verify that the method returns a list of StormConfig objects
    assert len(configs) == 2
    assert all(isinstance(config, StormConfig) for config in configs)

def test_get_config_by_name(storm_db):

    storm_db.create_new_storm_config("test_storm1", "input1", "target1")
    storm_db.create_new_storm_config("test_storm2", "input2", "target2")

    # Call the method to get a storm configuration by name
    config = storm_db.get_config_by_name("test_storm2")

    # Verify that the method returns a StormConfig object
    assert isinstance(config, StormConfig)
    assert config.storm_name == "test_storm2"
    assert config.input_playlist == "input2"
    assert config.target_playlist == "target2"

def test_get_config_by_name_not_found(storm_db):
    storm_db.create_new_storm_config("test_storm1", "input1", "target1")
    storm_db.create_new_storm_config("test_storm2", "input2", "target2")

    # Call the method to get a storm configuration by name
    config = storm_db.get_config_by_name("test_storm3")

    # Verify that the method returns None when the configuration is not found
    assert config.storm_name == None

def test_update_playlist(storm_db):
    # Create a playlist object
    playlist = {
        "id": "test_playlist_id",
        "name": "test_playlist",
        "owner": {"id": "test_owner_id", "display_name": "test_owner_name"},
        "public": True,
        "collaborative": False,
        "description": "test_description",
        "followers": {'total': 100},
        "snapshot_id": "test_snapshot_id",
        "type": "test_type",
    }

    # Call the method to update the playlist
    storm_db.update_playlist(playlist)

    # Verify that the document was inserted into the test MongoDB collection
    assert storm_db.db.get_collection('playlist').count_documents({}) == 1
