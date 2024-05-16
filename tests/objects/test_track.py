from storm.objects.track import Track

def test_track():
    # Retrieve the saved Track object
    track = Track(name="test_track", artists="test_artist", album="test_album", duration_ms="test_duration", _id="test_id")
    assert isinstance(track, Track)
    assert track.name == "test_track"
    assert track.artists == "test_artist"
    assert track.album == "test_album"
    assert track.duration_ms == "test_duration"
    assert track._id is not None

def test_track_from_json():
    # Create a Track object from a JSON object
    track = Track.from_json({"id": "test_id", "name": "test_track", "artists": "test_artist", "album": "test_album", "duration_ms": "test_duration"})
    assert isinstance(track, Track)
    assert track._id == "test_id"
    assert track.artists == "test_artist"
    assert track.album == "test_album"
    assert track.duration_ms == "test_duration"
    assert track.explicit is None

def test_track_from_json_missing_name():
    # Create a Track object from a JSON object with a missing name
    try:
        Track.from_json({"id": "test_id", "artists": "test_artist", "album": "test_album", "duration_ms": "test_duration"})
        assert False
    except ValueError as e:
        assert str(e) == "Track name is required."

def test_track_from_json_missing_artists():
    # Create a Track object from a JSON object with missing artists
    try:
        Track.from_json({"id": "test_id", "name": "test_track", "album": "test_album", "duration_ms": "test_duration"})
        assert False
    except ValueError as e:
        assert str(e) == "Track artists are required."

def test_track_from_json_missing_album():
    # Create a Track object from a JSON object with missing album
    try:
        Track.from_json({"id": "test_id", "name": "test_track", "artists": "test_artist", "duration_ms": "test_duration"})
        assert False
    except ValueError as e:
        assert str(e) == "Track album is required."

def test_track_from_json_missing_id():
    # Create a Track object from a JSON object with missing ID
    try:
        Track.from_json({"name": "test_track", "artists": "test_artist", "album": "test_album", "duration_ms": "test_duration"})
        assert False
    except ValueError as e:
        assert str(e) == "Track ID is required."
