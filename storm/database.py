from .objects.storm_config import StormConfig


class StormDB:
    """
    A class used to interact with the storm database.
    """

    def __init__(self):
        pass

    def create_new_storm_config(self, input_playlist, target_playlist):
        """Creates a new storm configuration in the database."""
        config = StormConfig(
            input_playlist=input_playlist, target_playlist=target_playlist
        )
        config.save()
        return config
