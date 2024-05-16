import logging

# Project-level logger
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# Console handler for project-level logger
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
# logger.addHandler(handler)

# Database logger
database_logger = logging.getLogger("storm.database")
database_logger.setLevel(logging.INFO)
database_handler = logging.StreamHandler()
database_handler.setLevel(logging.INFO)
database_handler.setFormatter(formatter)
database_logger.addHandler(database_handler)

# client logger
client_logger = logging.getLogger("storm.client")
client_logger.setLevel(logging.INFO)
client_handler = logging.StreamHandler()
client_handler.setLevel(logging.INFO)
client_handler.setFormatter(formatter)
client_logger.addHandler(client_handler)

# ETL logger
etl_logger = logging.getLogger("storm.etl")
etl_logger.setLevel(logging.INFO)
etl_handler = logging.StreamHandler()
etl_handler.setLevel(logging.INFO)
etl_handler.setFormatter(formatter)
etl_logger.addHandler(etl_handler)
