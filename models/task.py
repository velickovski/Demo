import datetime
import pandas as pd
import logging.config
from persistence.task_persistence import FILE_PATH

# Configure logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("task_manager")

class Task:
    def __init__(self, taskName: str, priority: str, deadline: str, task_id=None, visible=True, completed=False, date_created=None, dateCompleted=None):
        self.id = task_id if task_id is not None else self.get_next_id()
        self.taskName = taskName
        self.priority = priority
        self.deadline = deadline
        self.date_created = date_created if date_created else datetime.datetime.now().isoformat()
        self.visible = visible
        self.completed = completed
        self.dateCompleted = dateCompleted

    def __repr__(self):
        return (f"Task(ID: {self.id}, Name: {self.taskName}, Priority: {self.priority}, "
                f"Deadline: {self.deadline}, Created: {self.date_created}, "
                f"Completed: {self.completed}, DateCompleted: {self.dateCompleted})")

    @staticmethod
    def get_next_id():
        """Retrieve the next available task ID from the CSV."""
        try:
            df = pd.read_csv(FILE_PATH())
            if df.empty:
                return 1
            return df['id'].max() + 1
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return 1

    def save(self):
        """Save the current task to the CSV file."""
        try:
            df = pd.read_csv(FILE_PATH())
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['id', 'taskName', 'priority', 'deadline', 'date_created', 'visible', 'completed', 'dateCompleted'])

        new_task_data = pd.DataFrame([self.__dict__])
        df = pd.concat([df, new_task_data], ignore_index=True)
        df.to_csv(FILE_PATH(), index=False)
        logger.info(f"Task '{self.taskName}' (ID: {self.id}) saved successfully.")

    @staticmethod
    def get_task_by_id(task_id: int):
        """Retrieve a task by its ID."""
        try:
            df = pd.read_csv(FILE_PATH())
            task_data = df[df['id'] == task_id].to_dict(orient="records")
            if not task_data:
                logger.warning(f"Task ID {task_id} not found.")
                return None
            return Task(**task_data[0])
        except Exception as e:
            logger.error(f"Error retrieving task ID {task_id}: {e}")
            return None

    def update(self, new_taskName=None, new_priority=None, new_deadline=None):
        """Update the task with new values."""
        try:
            df = pd.read_csv(FILE_PATH())
            if self.id not in df['id'].values:
                logger.warning(f"Task ID {self.id} not found for update.")
                return False

            task_index = df[df['id'] == self.id].index[0]

            if new_taskName:
                df.at[task_index, 'taskName'] = new_taskName
                self.taskName = new_taskName
            if new_priority:
                df.at[task_index, 'priority'] = new_priority
                self.priority = new_priority
            if new_deadline:
                df.at[task_index, 'deadline'] = new_deadline
                self.deadline = new_deadline

            df.to_csv(FILE_PATH(), index=False)
            logger.info(f"Task ID {self.id} updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error updating task ID {self.id}: {e}")
            return False

    def delete(self):
        """Mark the task as deleted (sets visibility to False)."""
        try:
            df = pd.read_csv(FILE_PATH())
            if self.id not in df['id'].values:
                logger.warning(f"Task ID {self.id} not found for deletion.")
                return False

            df.loc[df['id'] == self.id, 'visible'] = False
            df.to_csv(FILE_PATH(), index=False)
            logger.info(f"Task ID {self.id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting task ID {self.id}: {e}")
            return False

    def complete(self):
        """Mark the task as completed."""
        try:
            df = pd.read_csv(FILE_PATH())
            if self.id not in df['id'].values:
                logger.warning(f"Task ID {self.id} not found for completion.")
                return False

            df.loc[df['id'] == self.id, ['completed', 'visible']] = [True, False]
            df.loc[df['id'] == self.id, 'dateCompleted'] = datetime.date.today().isoformat()
            df.to_csv(FILE_PATH(), index=False)
            logger.info(f"Task ID {self.id} marked as completed.")
            return True
        except Exception as e:
            logger.error(f"Error completing task ID {self.id}: {e}")
            return False
