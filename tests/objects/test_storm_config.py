import pytest
from mongoengine import connect
from storm.objects.storm_config import StormConfig
import mongomock

# Connect to a test database
connect("test_storm_database", mongo_client_class=mongomock.MongoClient)

@pytest.fixture
def setup_database():
    # Create some test data
    config_data = {
        "input_playlist": "input_playlist_id",
        "target_playlist": "target_playlist_id"
    }
    StormConfig(**config_data).save()

def test_storm_config(setup_database):
    # Retrieve the saved StormConfig object
    config = StormConfig.objects.first()

    # Check that the object was saved correctly
    assert config.input_playlist == "input_playlist_id"
    assert config.target_playlist == "target_playlist_id"
