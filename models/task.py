from datetime import datetime


class Task:
    def __init__(self, taskName: str, priority: str, deadline: str):
        self.taskName = taskName
        self.priority = priority
        self.deadline = deadline
        self.date_created = datetime.now()
        self.visible = True
        self.completed = False
        self.dateCompleted = "N/A"

    def __repr__(self):
        return f"{self.taskName},{self.priority},{self.deadline}"
