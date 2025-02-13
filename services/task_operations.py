import pandas as pd
import logging.config
from models.task import Task
from persistence.task_persistence import FILE_PATH

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("task_manager")

class TaskManager:
    @staticmethod
    def add_task(self, task: Task):
        task.save()

    @staticmethod
    def edit_task(self, task_id: int, new_taskName=None, new_priority=None, new_deadline=None):
        task = Task.get_task_by_id(task_id)
        if task:
            return task.update(new_taskName, new_priority, new_deadline)
        return False

    @staticmethod
    def delete_task(self, task_id: int):
        task = Task.get_task_by_id(task_id)
        if task:
            return task.delete()
        return False

    @staticmethod
    def complete_task(self, task_id: int):
        task = Task.get_task_by_id(task_id)
        if task:
            return task.complete()
        return False

    @staticmethod
    def view_tasks(self):
        try:
            df = pd.read_csv(FILE_PATH())
            visible_tasks = df[df['visible'] == True]
            print(visible_tasks)
        except Exception as e:
            logger.error(f"Error displaying tasks: {e}")
