from flask import Flask, request, jsonify
from datetime import datetime

from .fake_db import tasks
from .utils import validate_deadline

app = Flask(__name__)


@app.get("/tasks")
def get_tasks():
    # Сортируем задачи по дедлайну (ближайшие сверху)
    sorted_tasks = sorted(tasks, key=lambda x: x["deadline_date"])
    result = [
        {
            "id": t["id"],
            "title": t["title"],
            "description": t["description"],
            "deadline": t["deadline"],
        }
        for t in sorted_tasks
    ]
    return jsonify(result)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if (
        not data
        or "title" not in data
        or "description" not in data
        or "deadline" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    if not validate_deadline(data["deadline"]):
        return jsonify({"error": "Invalid deadline format. Use DD-MM-YYYY"}), 400

    try:
        # Преобразуем дедлайн в объект datetime для удобства сортировки
        deadline_date = datetime.strptime(data["deadline"], "%d-%m-%Y")
    except ValueError:
        return jsonify({"error": "Invalid date. Use DD-MM-YYYY format"}), 400

    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "title": data["title"],
        "description": data["description"],
        "deadline": data["deadline"],
        "deadline_date": deadline_date,  # Для внутренней сортировки
    }
    tasks.append(task)
    return jsonify({"message": "Task added", "task": task}), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    initial_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == initial_length:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
