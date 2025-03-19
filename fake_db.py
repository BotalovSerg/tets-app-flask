import re
from typing import TypedDict, List
from datetime import datetime

# Список задач в памяти. Каждая задача — словарь с уникальным ID.
# ID генерируется как длина списка + 1 для простоты.
# Это позволяет быстро находить, добавлять и удалять задачи.


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

    # Валидация формата дедлайна (DD-MM-YYYY)
    @staticmethod
    def validate_deadline(deadline: str) -> bool:
        return re.match(r"\d{2}-\d{2}-\d{4}", deadline) is None

    def add_task(self, title: str, description: str, deadline: str) -> Task | None:
        if self.validate_deadline(deadline):
            return None
        task: Task = {
            "id": self.generate_unique_id(),
            "title": title,
            "description": description,
            "deadline": deadline,
            "deadline_date": datetime.strptime(deadline, "%d-%m-%Y"),
        }
        self.tasks.append(task)
        return task


task_manager = TaskManager()
