# Imports the main execution function from the taskmanager package CLI module
from taskmanger.cli  import run_cli

# Checks if script is being run directly from terminal rather than imported
if __name__ == "__main__":
  # Executes the primary CLI handler function
  run_cli()