from src.data.commands import init_replies
from src.core.recognizer import Recognizer
from src.core.logger import Logger

logger = Logger(__name__).get_logger()

if __name__ == "__main__":
    try:
        logger.info("Initializing commands and replies")
        init_replies()

        logger.info("Starting the recognizer")
        recognizer = Recognizer()
        recognizer.start()
    except Exception as e:
        logger.exception("An error occurred in the main application: %s", e)