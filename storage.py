# Imports Python's built-in module for reading and writing JSON files
import json
# Imports the OS module for interacting with system file paths
import os
# Imports typing support to annotate expected return types
from typing import List
# Imports the Task model class from the local models module
from models import Task
# Defines the storage handler class to manage reading and writing to disk
class StorageHandler:
    # Constructor that sets the JSON target path and ensures file existence
    def __init__(self, filepath: str = "tasks.json"):
        # Stores the target filepath to an instance variable
        self.filepath = filepath
        # Checks if the designated JSON storage file already exists on disk
        if not os.path.exists(self.filepath):
            # Creates an initial empty JSON file if it does not exist
            self.save_tasks([])

    # Reads stored task data from disk and converts it into Task objects
    def load_tasks(self) -> List[Task]:
        # Begins a try block to handle potential missing file or parsing errors
            try:
                # Opens the JSON file in read mode and ensures safe closure
                with open(self.filepath, "r") as file:
                    # Parses raw JSON text from the file into a Python list of dicts
                    data = json.load(file)
                    # Converts each dictionary into a Task object using list comprehension
                    return [Task.from_dict(item) for item in data]
                # Catches file missing or invalid JSON syntax errors safely
            except (json.JSONDecodeError, FileNotFoundError):
                # Returns an empty list if data loading fails to prevent crashing
                return []

    # Writes a list of Task objects back to the JSON file on disk
    def save_tasks(self, tasks: List[Task]) -> None:
        # Opens the target JSON file in write mode to overwrite current contents
        with open(self.filepath, "w") as file:
            # Serializes task objects to dicts and writes formatted JSON with 4-space indent
            json.dump([task.to_dict() for task in tasks], file, indent=4)