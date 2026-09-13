# Imports Python's built-in datetime class to handle timestamps for task creation
from datetime import datetime


# Defines the main Task class to encapsulate task data and behaviors
class Task:

    # Constructor method executed when a new Task instance is initialized
    def __init__(self,
                 task_id:int,
                 title:str,
                 priority: str = "medium",
                 completed: bool = False,
                 ):
        # Assigns the unique integer identifier to the instance
        self.id = task_id
        # Assigns the title or description text to the instance
        self.title = title
        # Converts the priority string to lowercase for standard formatting
        self.priority = priority.lower()
        # Stores the completion status as a boolean (True or False)
        self.completed = completed
        # Captures the current date/time and stores it in ISO format string
        self.created_at = datetime.now().isoformat()

    # Instance method to update the task status to finished
    def mark_completed(self):
        # Sets the completion status flag to True
        self.completed = True
        # Helper method to serialize task attributes for JSON output
    def to_dict(self):
        # Returns the instance attribute dictionary mapping keys to values
        return self.__dict__

    # Class method acting as a factory to build Task instances from dictionaries
    @classmethod
    def from_dict(cls, data: dict):
        # Instantiates a new Task object using the dictionary values
        task = cls(data["id"], data["title"], data["priority"], data["completed"])
        # Restores original creation timestamp if present, or creates a new one
        task.created_at = data.get("created_at", datetime.now().isoformat())
        # Returns the newly created Task object instance
        return task
