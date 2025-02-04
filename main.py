from services.task_operations import TaskManager
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def main():
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
            manager.add_task()
            logger.info("Task Added")
        elif choice == "2":
            manager.view_tasks()
            logger.info("View Tasks")
        elif choice == "3":
            manager.edit_task()
            logger.info("Edit Task was successful")
        elif choice == "4":
            manager.delete_task()
            logger.info("Task has been deleted")
        elif choice == "5":
            manager.complete_task()
            logger.info("Task Completed")
        elif choice == "6":
            print("Thank you for using the Smart Task Organizer!")
            logger.info("Exiting Smart Task Organizer")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    manager = TaskManager()
    main()
