import datetime
import os
from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constants
TODAY = "today"
TOMORROW = "tomorrow"
NEXT = "next"
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarService:
    def __init__(self):
        """
        Initialize the CalendarService by authenticating with Google Calendar API.
        """
        # Path to the credentials file 
        user_specific_folder = Path(__file__).parent.parent / "user-specific"
        self.creds = None
        # Check if token.json file exists for storing user credentials
        if os.path.exists(Path(f'{user_specific_folder}/token.json').resolve()):
            self.creds = Credentials.from_authorized_user_file(Path(f'{user_specific_folder}/token.json').resolve(), SCOPES)

        # If there are no valid credentials, request the user to log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(Path(f'{user_specific_folder}/credentials.json').resolve(), SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(Path(f'{user_specific_folder}/token.json').resolve(), 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")
            self.service = None
            raise
        

    def get_date_from_keyword(self, keyword: str) -> datetime.date:
        """
        Get the date based on a keyword like 'today', 'tomorrow', or 'yesterday'.

        Args:
            keyword (str): The keyword specifying the date.

        Returns:
            datetime.date: The corresponding date.
        """
        today = datetime.date.today()
        if keyword == TOMORROW:
            return today + datetime.timedelta(days=1)
        else:
            raise ValueError("Invalid keyword for date.")

    def parse_date_from_string(self, date_str: str) -> datetime.date:
        """
        Parse a date from a string in the format 'day month' (e.g., '20 May').

        Args:
            date_str (str): The date string.

        Returns:
            datetime.date: The parsed date.
        """
        try:
            return datetime.datetime.strptime(date_str, "%d %B").replace(year=datetime.date.today().year).date()
        except ValueError:
            raise ValueError("Invalid date format. Use 'day month' (e.g., '20 May').")

    def get_events_for_date(self, target_date: datetime.date) -> str:
        """
        Retrieve events for a specific date from Google Calendar.

        Args:
            target_date (datetime.date): The target date.

        Returns:
            str: A string containing the events for the specified date.
        """
        start_of_day = datetime.datetime.combine(target_date, datetime.time.min).isoformat() + 'Z'
        end_of_day = datetime.datetime.combine(target_date, datetime.time.max).isoformat() + 'Z'

        events_result = self.service.events().list( # type: ignore
            calendarId='primary',  # Use 'primary' for the main calendar
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        if not events:
            return f"No events found for {target_date.strftime('%d %B %Y')}."

        event_list = [f"{event['start'].get('dateTime', event['start'].get('date'))}: {event['summary']}" for event in events]
        return f"Events for {target_date.strftime('%d %B %Y')}:\n" + "\n".join(event_list)

    def get_calendar_events(self, data: List[str]) -> str:
        """
        Get the calendar events for today, tomorrow, yesterday, or a specific date.

        Args:
            data (list): List of strings containing the date information.

        Returns:
            str: The calendar events for the specified date.
        """
        try:
            if NEXT in data:
                now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
                event_results = self.service.events().list( # type: ignore
                    calendarId='primary', 
                    timeMin=now, 
                    maxResults=3, 
                    singleEvents=True, 
                    orderBy="startTime"
                ).execute() 
                events = event_results.get('items', [])
                if not events:
                    return "No upcoming events found."
                event_list = [f"{event['start'].get('dateTime', event['start'].get('date'))}: {event['summary']}" for event in events]
                return "Upcoming events:\n" + "\n".join(event_list)
            elif TODAY in data:
                target_date = self.get_date_from_keyword(TODAY)
            elif TOMORROW in data:
                target_date = self.get_date_from_keyword(TOMORROW)
            else:
                # Assume the date is in 'day month' format
                date = data[-2:]
                if len(date[0]) > 2:
                    date[0] = date[0][:2]
                date_str = " ".join(date)
                target_date = self.parse_date_from_string(date_str)

            return self.get_events_for_date(target_date)
        except Exception as e:
            return f"An error occurred: {e}"