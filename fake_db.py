import re
from typing import TypedDict, List
from datetime import datetime


class Task(TypedDict):
    _id: int
    title: str
    description: str
    deadline: str
    deadline_date: datetime


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.current_id = 0

    def generate_unique_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def get_tasks(self) -> List[Task]:
        return sorted(self.tasks, key=lambda task: task.get("deadline_date"))

    @staticmethod
    def validate_deadline(deadline: str) -> bool:
        return re.match(r"\d{2}-\d{2}-\d{4}", deadline) is not None

    def add_task(self, title: str, description: str, deadline: str) -> Task:
        task: Task = {
            "_id": self.generate_unique_id(),
            "title": title,
            "description": description,
            "deadline": deadline,
            "deadline_date": datetime.strptime(deadline, "%d-%m-%Y"),
        }
        self.tasks.append(task)
        return task

    def delete_task(self, task_id: int) -> bool | None:
        current_len = len(self.tasks)
        if current_len:
            self.tasks = [task for task in self.tasks if task.get("_id") != task_id]
            return current_len != len(self.tasks)


task_manager = TaskManager()
