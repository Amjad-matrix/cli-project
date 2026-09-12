# Imports Python's built-in module for parsing terminal arguments
import argparse

# Imports Task model to create new task objects from command inputs
from models import Task

# Imports StorageHandler to manage disk read/write actions
from storage import StorageHandler


# Controller function responsible for setting up CLI and processing inputs
def run_cli():
  # Instantiates the main argument parser with a top-level program description
  parser = argparse.ArgumentParser(description="Terminal Task Manager")
  # Creates sub-command handlers and tracks chosen command in 'command' attribute
  subparsers = parser.add_subparsers(dest="command")

  # Adds sub-parser configuration for the 'add' sub-command
  add_parser = subparsers.add_parser("add", help="Add a new task")
  # Configures positional string argument for entering the task title
  add_parser.add_argument("title", type=str, help="Title of the task")
  # Configures optional priority flag restricted to low/medium/high values
  add_parser.add_argument(
      "-p",
      "--priority",
      choices=["low", "medium", "high"],
      default="medium",
  )

  # Adds sub-parser configuration for the 'list' sub-command
  subparsers.add_parser("list", help="List all tasks")

  # Adds sub-parser configuration for the 'complete' sub-command
  complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
  # Configures required integer positional argument for target task ID
  complete_parser.add_argument("id", type=int, help="Task ID to mark complete")

  # Parses command-line inputs entered by user into an args namespace object
  args = parser.parse_args()
  # Instantiates the storage handler to access tasks.json
  storage = StorageHandler()
  # Loads all persistent tasks into memory from the JSON file
  tasks = storage.load_tasks()

  # Checks if the user ran the 'add' sub-command
  if args.command == "add":
    # Calculates auto-incrementing ID by finding max current ID and adding 1
    new_id = max([t.id for t in tasks], default=0) + 1
    # Constructs a new Task object instance from user inputs
    new_task = Task(new_id, args.title, args.priority)
    # Appends the new task instance to the loaded task array
    tasks.append(new_task)
    # Persists the updated task array to the storage file
    storage.save_tasks(tasks)
    # Prints success confirmation output to terminal
    print(f"Task '{args.title}' added with ID {new_id}.")

  # Checks if the user ran the 'list' sub-command
  elif args.command == "list":
    # Checks if storage contains zero tasks
    if not tasks:
      # Outputs message indicating no records exist
      print("No tasks found.")
      # Exits function execution early
      return
    # Iterates over every Task object contained in the stored list
    for t in tasks:
      # Sets status icon to a checkmark if finished, or blank space if pending
      status = "✓" if t.completed else " "
      # Prints formatted line showing status, ID, title, and priority level
      print(f"[{status}] {t.id}: {t.title} (Priority: {t.priority})")

  # Checks if the user ran the 'complete' sub-command
  elif args.command == "complete":
    # Loops through current task objects searching for matching ID
    for t in tasks:
      # Compares current loop item's ID with target ID from command argument
      if t.id == args.id:
        # Sets completed status flag of task object to True
        t.mark_complete()
        # Writes updated list back to the disk file
        storage.save_tasks(tasks)
        # Outputs completion confirmation to terminal
        print(f"Task {args.id} marked as complete.")
        # Exits function execution after updating target item
        return
    # Executes if loop finishes without finding matching task ID argument
    print(f"Task with ID {args.id} not found.")