import pandas as pd
import os
import logging.config
from dotenv import load_dotenv
from models.task import Task  # Ensure Task is imported

# Configure logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("task_manager")

def ensure_csv_file():
    """
    Checks if the configured folder and file exist.
    If not, throws an error and advises the user to create them manually.
    """
    if not os.path.isdir(FOLDER_PATH()):
        logger.error(f"Folder '{FOLDER_PATH()}' does not exist.")
        raise FileNotFoundError(f"Folder '{FOLDER_PATH()}' does not exist. Please create it manually.")

    if not os.path.isfile(FILE_PATH()):
        logger.error(f"File '{FILE_PATH()}' does not exist.")
        raise FileNotFoundError(f"File '{FILE_PATH()}' does not exist. Please create it manually.")

def get_next_id() -> int:
    """
    Retrieves the next unique ID for a new task.

    Returns:
    - int: The next unique ID.
    """
    try:
        if os.path.exists(FILE_PATH()):
            df = pd.read_csv(FILE_PATH())
            next_id = df['id'].max() + 1 if not df.empty else 1
            logger.debug(f"Next task ID: {next_id}")
            return next_id
        else:
            logger.debug("CSV file does not exist, starting ID from 1.")
            return 1
    except Exception as e:
        logger.error(f"Error retrieving next task ID: {e}")
        return 1

def save_task_to_csv(task: Task):
    """
    Saves a given Task object to the CSV file.

    Parameters:
    - task (Task): The Task object to save.
    """
    try:
        task_id = get_next_id()
        task_data = {
            'id': [task_id],
            'taskName': [task.taskName],
            'priority': [task.priority],
            'deadline': [task.deadline],
            'date_created': [task.date_created],
            'visible': [task.visible],
            'completed': [task.completed],
            'dateCompleted': [task.dateCompleted],
        }
        df = pd.DataFrame(task_data)
        df.to_csv(FILE_PATH(), mode='a', index=False, header=not os.path.exists(FILE_PATH()))
        logger.info(f"Task '{task.taskName}' (ID: {task_id}) saved to CSV.")
    except Exception as e:
        logger.error(f"Error saving task '{task.taskName}' to CSV: {e}")

def load_tasks_from_csv() -> pd.DataFrame:
    """
    Loads all tasks from the CSV file into a DataFrame.

    Returns:
    - pd.DataFrame: A DataFrame of all tasks.
    """
    try:
        df = pd.read_csv(FILE_PATH())
        logger.info("Tasks loaded from CSV.")
        return df
    except Exception as e:
        logger.error(f"Error loading tasks from CSV: {e}")
        return pd.DataFrame()

def FOLDER_PATH():
    load_dotenv()
    folder_path = os.getenv("FOLDER_PATH", "data")
    logger.debug(f"Using folder path: {folder_path}")
    return folder_path

def FILE_PATH():
    load_dotenv()
    file_path = os.getenv("FOLDER_PATH", "data") + "/" + os.getenv("FILE_PATH", "data.csv")
    logger.debug(f"Using file path: {file_path}")
    return file_path
