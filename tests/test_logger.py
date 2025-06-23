from src.core.logger import Logger

def test_logger_get_logger():
    logger = Logger("test").get_logger()
    assert logger.name == "test"
    logger.info("Logger test info")
    logger.debug("Logger test debug")