import logging
import colorlog
import datetime
import pytz
import tzlocal

class Logger:
    def __init__(self, name: str):
        """
        Initialize the Logger class with the specified name.

        Args:
            name (str): The name of the logger.
        """
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)

            # Create handlers
            console_handler = logging.StreamHandler()
            file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

            # Set levels for handlers
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.DEBUG)

            # Create formatter with colors for console
            color_formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
                datefmt=None  # Removed datefmt to use custom formatter
            )

            file_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                datefmt=None  # Removed datefmt to use custom formatter
            )

            # Add custom time converter for local timezone
            def custom_time(*args):
                utc_dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                local_tz = tzlocal.get_localzone()  # Dynamically get the local timezone
                return utc_dt.astimezone(local_tz).timetuple()

            logging.Formatter.converter = custom_time

            console_handler.setFormatter(color_formatter)
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: Configured logger instance.
        """
        return self.logger