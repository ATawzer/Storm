from storm import StormClient, StormDB  # noqa: F401


class StormJob:
    """
    Chains operations together to form a single job.
    """

    def __init__(self, *operations):
        self.operations = operations

    def execute(self, context):
        """
        Execute the job.
        """
        for operation in self.operations:
            operation.execute(context)


class StormContext:
    """
    Contains the necessary objects for a job to execute.
    """

    def __init__(self, storm_client, storm_db):
        self.storm_client = storm_client
        self.storm_db = storm_db


class StormOperation:
    """
    Base class for operations.
    """

    def execute(self, context):
        """
        Execute the operation.
        """
        raise NotImplementedError
