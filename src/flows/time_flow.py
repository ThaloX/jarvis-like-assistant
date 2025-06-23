import datetime
from src.core.logger import Logger

logger = Logger(__name__).get_logger()

class TimeService:
    def __init__(self):
        logger.info("Initializing TimeService")
        self.local_tz = datetime.datetime.now().astimezone().tzinfo

    def get_time(self) -> str:
        now = datetime.datetime.now(self.local_tz)
        logger.debug(f"Fetched current time: {now.strftime('%H:%M:%S')}")
        return f"The current time is {now.strftime('%H:%M:%S')}."

    def get_date(self) -> str:
        today = datetime.date.today()
        day_of_week = today.strftime('%A')
        logger.debug(f"Fetched current date: {today.strftime('%A, %d %B %Y')}")
        return f"Today's date is {day_of_week}, {today.strftime('%A, %d %B %Y')}."

    def get_week_info(self) -> str:
        today = datetime.date.today()
        week_number = today.isocalendar()[1]
        logger.debug(f"Fetched week info: {today.strftime('%A, %d %B %Y')}, week {week_number}")
        return f"Today is {today.strftime('%A, %d %B %Y')}, week {week_number} of the year."

    def get_time_info(self, data: list[str]) -> str:
        """
        Returns time/date/week info based on tokens.
        Always includes the current time.
        """
        logger.info(f"Received tokens for time info: {data}")
        if "week" in data:
            result = f"{self.get_week_info()} {self.get_time()}"
        elif "date" in data:
            result = f"{self.get_date()} {self.get_time()}"
        else:
            result = self.get_time()
        logger.info(f"Returning time info result: {result}")
        return result