import csv
from operator import __and__
from pathlib import Path
from typing import Dict, List
from src.core.logger import Logger

# Global dictionaries for csv data
commands: Dict[str, List[str]] = {}
replies: Dict[str, List[str]] = {}
q_and_a: Dict[str, str] = {}

logger = Logger(__name__).get_logger()

def load_csv(file_path: str) -> List[List[str]]:
    """
    Load data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        List[List[str]]: The data from the CSV file as a list of lists.
    """
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return [row for row in reader]

def init_replies() -> None:
    """
    Load user and reply data from a CSV file and store them in global dictionaries.
    """
    logger.info("Initializing replies from CSV files")
    data = load_csv(str(Path("user_data/input.csv")))
    q_a_data = load_csv(str(Path("user_data/q_and_a.csv")))

    global commands
    global replies
    global q_and_a

    for row in data:
        category = row[0]
        command = row[1]
        reply = row[2]

        if category not in commands:
            commands[category] = []
        if category not in replies:
            replies[category] = []

        commands[category].append(command)
        replies[category].append(reply)
    
    for row in q_a_data:
        question = row[0]
        answer = row[1]

        if question not in q_and_a:
            q_and_a[question] = ""

        q_and_a[question] = answer

    logger.info("Replies initialized successfully")
