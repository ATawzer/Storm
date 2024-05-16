from storm.objects.storm_config import StormConfig

def test_storm_config():
    # Retrieve the saved StormConfig object
    config = StormConfig(storm_name="test_storm", input_playlist="input_playlist_id", target_playlist="target_playlist_id")
    assert isinstance(config, StormConfig)
    assert config.storm_name == "test_storm"
    assert config.input_playlist == "input_playlist_id"
    assert config.target_playlist == "target_playlist_id"

