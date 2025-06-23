import csv
import time


def sort_by_categories() -> None:
    """
    Sort the given CSV file by the category.
    """
    with open("jarvis-like-assistant/unsorted.csv", newline="") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        sortedlist = sorted(
            spamreader,
            key=lambda row: (row["category"], row["command"], row["reply"]),
            reverse=False,
        )

    with open("jarvis-like-assistant/input.csv", "w") as f:
        fieldnames = ["category", "command", "reply"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)
            time.sleep(0.1)


def remove_duplicate_lines(file_path: str) -> None:
    """
    Remove duplicate lines from the given file.

    Args:
        file_path (str): The path to the file.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        unique_lines = set(lines)

    with open(file_path, "w") as file:
        file.writelines(unique_lines)


# # Test
# sort_by_categories()
# remove_duplicate_lines("jarvis-like-assistant/input.csv")
