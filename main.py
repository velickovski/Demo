from services.task_operations import TaskManager
from models.task import Task
import logging
import logging.config
import datetime

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def main():
    manager = TaskManager()

    logger.info('Starting Smart Task Organizer')
    print("Welcome to the Smart Task Organizer!")
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Finish Task")
    print("6. Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            task_name = input("Enter task name: ").strip()
            priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

            try:
                deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
                if deadline_date < datetime.date.today():
                    print("Deadline cannot be in the past.")
                    continue
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            task = Task(task_name, priority, deadline)
            manager.add_task(task)
            logger.info(f"Task '{task_name}' added.")

        elif choice == "2":
            manager.view_tasks()
            logger.info("View Tasks")

        elif choice == "3":
            task_id = input("Enter the ID of the task to edit: ").strip()
            updated_name = input("Enter new task name: ").strip()
            updated_priority = input("Enter new priority (Low, Medium, High): ").strip().capitalize()
            updated_deadline = input("Enter new deadline (YYYY-MM-DD): ").strip()

            updated_task = Task(updated_name, updated_priority, updated_deadline)
            success = manager.edit_task(int(task_id), updated_task)
            if success:
                print(f"Task {task_id} updated successfully.")
            else:
                print(f"Task {task_id} not found or could not be updated.")

        elif choice == "4":
            task_id = input("Enter the ID of the task to delete: ").strip()
            success = manager.delete_task(int(task_id))
            if success:
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Task {task_id} not found.")

        elif choice == "5":
            task_id = input("Enter the ID of the task to mark as completed: ").strip()
            success = manager.complete_task(int(task_id))
            if success:
                print(f"Task {task_id} marked as completed.")
            else:
                print(f"Task {task_id} not found.")

        elif choice == "6":
            print("Thank you for using the Smart Task Organizer!")
            logger.info("Exiting Smart Task Organizer")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
