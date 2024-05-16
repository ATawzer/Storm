from storm.client import StormClient

def test_get_playlist_tracks():
    # Initialize the StormClient
    storm_client = StormClient()

    # Call the method to get all tracks from a playlist
    playlist_id = "1Jhuw695S6WhcQIJNEVWdc"
    tracks = storm_client.get_playlist_tracks(playlist_id)

    # Verify that the method returns a list of tracks
    assert len(tracks) == 1
    assert all('track' in track for track in tracks)

def test_get_playlist_metadata():
    # Initialize the StormClient
    storm_client = StormClient()

    # Call the method to get metadata about a playlist
    playlist_id = "1Jhuw695S6WhcQIJNEVWdc"
    playlist = storm_client.get_playlist_metadata(playlist_id)

    # Verify that the method returns a dictionary with playlist data
    assert 'id' in playlist
    assert 'name' in playlist
    assert 'owner' in playlist
    assert 'public' in playlist
    assert 'collaborative' in playlist
    assert 'description' in playlist
    assert playlist['description'] == 'Testing Storm ETLs'
    assert 'followers' in playlist
    assert 'snapshot_id' in playlist
    assert 'type' in playlist