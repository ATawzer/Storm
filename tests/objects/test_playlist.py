from storm.objects.playlist import Playlist

def test_playlist():
    # Retrieve the saved Playlist object
    playlist = Playlist(name="test_playlist", _id="test_id", owner={"test_owner":0}, tracks={"test_track_id":"test_track"})
    assert isinstance(playlist, Playlist)
    assert playlist.name == "test_playlist"
    assert playlist.owner == {"test_owner":0}
    assert len(playlist.tracks.keys()) == 1
    assert playlist._id is not None

def test_playlist_from_json():
    # Create a Playlist object from a JSON object
    playlist = Playlist.from_json({"id": "test_id", "name": "test_playlist", "owner": {"test_owner":0}, "tracks": {"test_track_id":"test_track"}})
    assert isinstance(playlist, Playlist)
    assert playlist._id == "test_id"
    assert playlist.name == "test_playlist"
    assert playlist.owner == {"test_owner":0}
    assert len(playlist.tracks.keys()) == 1
    assert playlist.public is None
    assert playlist.collaborative is None
    assert playlist.description is None
    assert playlist.followers == {}
    assert playlist.snapshot_id is None
    assert playlist.type is None
