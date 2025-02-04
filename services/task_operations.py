import datetime
import time
import pandas as pd
import threading
import keyboard
import logging.config
from models.task import Task
from persistence.task_persistence import ensure_csv_file, save_task_to_csv, FILE_PATH

# Configure logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("task_manager")

class TaskManager:
    """
    A class to manage tasks. Handles operations like adding, editing, deleting, and displaying tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager by ensuring the CSV file exists and sets up the ESC key listener.
        """
        ensure_csv_file()
        self.abort_flag = False
        self.esc_thread = threading.Thread(target=self.detect_esc, daemon=True)
        self.esc_thread.start()
        logger.info("Task Manager initialized.")

    def detect_esc(self):
        """
        Listens for the ESC key press and sets the abort flag to True.
        """
        while True:
            if keyboard.is_pressed('esc'):
                self.abort_flag = True
                print("\nOperation aborted. Returning to the main menu...")
                logger.warning("Operation aborted by user.")
                break

    def reset_abort_flag(self):
        """ Resets the abort flag to False before starting a new operation. """
        self.abort_flag = False

    @staticmethod
    def get_filtered_tasks(visible=True, completed=False):
        """
        Filters tasks based on their visibility and completion status.

        :param visible: Whether to include only visible tasks.
        :param completed: Whether to include only completed tasks.
        :return: A pandas DataFrame of filtered tasks.
        """
        try:
            df = pd.read_csv(FILE_PATH())
            if 'visible' in df.columns and 'completed' in df.columns:
                df = df[(df['visible'] == visible) & (df['completed'] == completed)]
            return df
        except Exception as e:
            logger.error(f"Error reading tasks from CSV: {e}")
            return pd.DataFrame()

    @staticmethod
    def display_tasks(df: pd.DataFrame):
        """
        Displays tasks in a tabular format with an additional 'Time Remaining' column.
        """
        logger.info('Displaying tasks')

        if df.empty:
            print("No tasks found.")
            logger.info("No tasks found.")
            return

        today = datetime.date.today()
        priority_map = {"High": 1, "Medium": 2, "Low": 3}

        def parse_deadline(deadline):
            try:
                return datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                logger.warning(f"Invalid deadline format: {deadline}")
                return None

        sorted_tasks = sorted(
            df.to_dict('records'),
            key=lambda task: (
                priority_map.get(task.get('priority'), 4),
                parse_deadline(task.get('deadline')) or datetime.date.max
            )
        )

        print(f"\033[1m{'ID':<5}{'Task Name':<30}{'Priority':<15}{'Deadline':<20}{'Time Remaining':<20}\033[0m")
        print("-" * 90)

        for task in sorted_tasks:
            deadline = task.get('deadline', 'N/A')
            priority = task.get('priority', 'N/A')

            deadline_date = parse_deadline(deadline)
            time_remaining_display = (
                f"{(deadline_date - today).days} days"
                if deadline_date and deadline_date > today
                else "\033[31mOverdue\033[0m"
            ) if deadline_date else "\033[33mInvalid Date\033[0m"

            priority_display = f"\033[31m{priority:<15}\033[0m" if priority == 'High' else f"{priority:<15}"
            deadline_display = f"\033[31m{deadline:<20}\033[0m" if "Overdue" in time_remaining_display else f"{deadline:<20}"

            print(f"{task['id']:<5}{task['taskName']:<30}{priority_display}{deadline_display}{time_remaining_display:<20}")

        print("-" * 90)

    def add_task(self):
        """ Adds a new task to the CSV file. """
        self.reset_abort_flag()

        while True:
            task_name = input("Enter task name: ").strip()
            if self.abort_flag:
                return
            if task_name:
                break
            print("Task name cannot be empty.")

        while True:
            priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
            if self.abort_flag:
                return
            if priority in ["Low", "Medium", "High"]:
                break
            print("Invalid priority!")

        while True:
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
            if self.abort_flag:
                return
            try:
                deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
                if deadline_date >= datetime.date.today():
                    break
                print("Deadline cannot be in the past.")
            except ValueError:
                print("Invalid date format.")

        task = Task(task_name, priority, deadline)
        save_task_to_csv(task)
        print(f"Task '{task_name}' added successfully.")
        logger.info(f"Task added: {task_name}")

    def edit_task(self):
        """
        Edits an existing task in the CSV file.
        Overdue tasks cannot be edited.
        """
        self.reset_abort_flag()

        # Load and filter tasks
        df = self.get_filtered_tasks()
        if df.empty:
            print("No tasks found to edit.")
            logger.info("No tasks found to edit.")
            return

        self.display_tasks(df)

        # Validate task ID
        while True:
            task_id = input("Enter the ID of the task to edit: ").strip()
            if self.abort_flag:
                return
            if task_id.isdigit() and int(task_id) in df['id'].values:
                task_index = df[df['id'] == int(task_id)].index[0]
                break
            print("Invalid ID. Please enter a valid task ID.")

        # Check if the task is overdue
        deadline_str = df.at[task_index, 'deadline']
        try:
            deadline_date = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
            if deadline_date <= datetime.date.today():
                print(f"Task ID {task_id} is Overdue and cannot be edited.")
                logger.warning(f"Attempted to edit overdue task ID {task_id}. Editing not allowed.")
                return
        except (ValueError, TypeError):
            print(f"Task ID {task_id} has an invalid deadline format and cannot be edited.")
            logger.warning(f"Task ID {task_id} has an invalid deadline: {deadline_str}. Editing not allowed.")
            return

        print("Press Enter to keep the current value or press ESC to cancel.")

        # Update task name
        while True:
            new_task_name = input(f"Enter new task name (current: {df.at[task_index, 'taskName']}): ").strip()
            logger.debug(f"New task name input: {new_task_name}")
            if self.abort_flag:
                return
            if new_task_name or not new_task_name:
                if new_task_name:
                    df.at[task_index, 'taskName'] = new_task_name
                    logger.info(f"Task name updated to: {new_task_name}")
                break
            print("Task name cannot be empty. Please try again.")

        # Update priority
        while True:
            new_priority = input(
                f"Enter new priority (Low, Medium, High) (current: {df.at[task_index, 'priority']}): "
            ).strip().capitalize()
            logger.debug(f"New priority input: {new_priority}")
            if self.abort_flag:
                return
            if new_priority in ["Low", "Medium", "High"] or not new_priority:
                if new_priority:
                    df.at[task_index, 'priority'] = new_priority
                    logger.info(f"Task priority updated to: {new_priority}")
                break
            print("Invalid priority! Priority must be 'Low', 'Medium', or 'High'. Please try again.")

        # Update deadline
        while True:
            new_deadline = input(
                f"Enter new deadline (YYYY-MM-DD) (current: {df.at[task_index, 'deadline']}): "
            ).strip()
            logger.debug(f"New deadline input: {new_deadline}")
            if self.abort_flag:
                return
            if not new_deadline:
                break
            try:
                deadline_date = datetime.datetime.strptime(new_deadline, "%Y-%m-%d").date()
                today = datetime.date.today()
                if deadline_date >= today:
                    df.at[task_index, 'deadline'] = new_deadline
                    logger.info(f"Task deadline updated to: {new_deadline}")
                    break
                else:
                    print("Deadline cannot be in the past. Please enter a future date or today.")
            except ValueError:
                print("Invalid date format! Please use the format YYYY-MM-DD.")

        # Save updated tasks to CSV
        df.to_csv(FILE_PATH(), index=False)
        print("Task updated successfully.")
        logger.info(f"Task ID {task_id} updated successfully.")
        time.sleep(1)

    def delete_task(self):
        """ Marks a task as not visible in the CSV file. """
        self.reset_abort_flag()
        df = self.get_filtered_tasks()

        if df.empty:
            print("No tasks found to delete.")
            return

        self.display_tasks(df)

        while True:
            task_id = input("Enter the ID of the task to delete: ").strip()
            if self.abort_flag:
                return
            if task_id.isdigit() and int(task_id) in df['id'].values:
                df.loc[df['id'] == int(task_id), 'visible'] = False
                break
            print("Invalid ID.")

        df.to_csv(FILE_PATH(), index=False)
        print(f"Task with ID {task_id} deleted.")
        logger.info(f"Task deleted: {task_id}")

    def complete_task(self):
        """ Marks a task as completed in the CSV file. """
        self.reset_abort_flag()
        df = self.get_filtered_tasks(completed=False)

        if df.empty:
            print("No tasks found to complete.")
            return

        self.display_tasks(df)

        while True:
            task_id = input("Enter the ID of the task to mark as completed: ").strip()
            if self.abort_flag:
                return
            if task_id.isdigit() and int(task_id) in df['id'].values:
                df.loc[df['id'] == int(task_id), ['completed', 'visible']] = [True, False]
                df.loc[df['id'] == int(task_id), 'dateCompleted'] = datetime.date.today().isoformat()
                break
            print("Invalid ID.")

        df.to_csv(FILE_PATH(), index=False)
        print(f"Task with ID {task_id} marked as completed.")
        logger.info(f"Task completed: {task_id}")

    def view_tasks(self):
        """ Displays all visible tasks in the CSV file. """
        self.reset_abort_flag()
        df = self.get_filtered_tasks()
        self.display_tasks(df)
