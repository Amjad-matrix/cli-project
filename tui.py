from models import Task
from storage import StorageHandler


def display_menu():
  print("\n==============================")
  print("      TASK MANAGER MENU       ")
  print("==============================")
  print("1. View All Tasks")
  print("2. View Active Tasks")
  print("3. View Completed Tasks")
  print("4. Add a Task")
  print("5. Toggle Task Completion")
  print("6. Delete a Task")
  print("7. Exit")
  print("==============================")


def run_interactive_menu():
  storage = StorageHandler()

  while True:
    display_menu()
    choice = input("\nSelect an option (1-7): ").strip()

    tasks = storage.load_tasks()

    if choice == "1":
      print("\n--- ALL TASKS ---")
      if not tasks:
        print("No tasks found.")
      for task in tasks:
        status = "✓" if task.completed else " "
        print(f"[{status}] #{task.id}: {task.title} (Priority: {task.priority})")

    elif choice == "2":
      print("\n--- ACTIVE TASKS ---")
      active_tasks = [t for t in tasks if not t.completed]
      if not active_tasks:
        print("No active tasks.")
      for task in active_tasks:
        print(f"[ ] #{task.id}: {task.title} (Priority: {task.priority})")

    elif choice == "3":
      print("\n--- COMPLETED TASKS ---")
      completed_tasks = [t for t in tasks if t.completed]
      if not completed_tasks:
        print("No completed tasks.")
      for task in completed_tasks:
        print(f"[✓] #{task.id}: {task.title} (Priority: {task.priority})")

    elif choice == "4":
      print("\n--- ADD TASK ---")
      title = input("Enter task title: ").strip()
      if not title:
        print("Error: Title cannot be empty!")
        continue

      priority = (
          input("Enter priority (low, medium, high) [default: medium]: ")
          .strip()
          .lower()
      )
      if priority not in ["low", "medium", "high"]:
        priority = "medium"

      new_id = max([t.id for t in tasks], default=0) + 1
      new_task = Task(
          task_id=new_id, title=title, priority=priority, completed=False
      )
      tasks.append(new_task)
      storage.save_tasks(tasks)
      print(f"Success: Task #{new_id} added!")

    elif choice == "5":
      print("\n--- TOGGLE COMPLETION ---")
      try:
        task_id = int(input("Enter Task ID to toggle: "))
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
          task.completed = not task.completed
          storage.save_tasks(tasks)
          status_str = "completed" if task.completed else "active"
          print(f"Success: Task #{task_id} marked as {status_str}!")
        else:
          print("Error: Task ID not found.")
      except ValueError:
        print("Error: Please enter a valid numerical ID.")

    elif choice == "6":
      print("\n--- DELETE TASK ---")
      try:
        task_id = int(input("Enter Task ID to delete: "))
        task_exists = any(t.id == task_id for t in tasks)
        if task_exists:
          tasks = [t for t in tasks if t.id != task_id]
          storage.save_tasks(tasks)
          print(f"Success: Task #{task_id} deleted!")
        else:
          print("Error: Task ID not found.")
      except ValueError:
        print("Error: Please enter a valid numerical ID.")

    elif choice == "7":
      print("\nGoodbye!")
      break

    else:
      print("Invalid choice! Please select a number from 1 to 7.")


if __name__ == "__main__":
  run_interactive_menu()