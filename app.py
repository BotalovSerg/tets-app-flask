from flask import Flask, request, jsonify

from fake_db import task_manager

app = Flask(__name__)


@app.get("/tasks")
def get_tasks():
    tasks = task_manager.get_tasks()
    result = [
        {
            "id": task["_id"],
            "title": task["title"],
            "description": task["description"],
            "deadline": task["deadline"],
        }
        for task in tasks
    ]
    return jsonify(result)


@app.post("/tasks")
def add_task():
    data: dict = request.get_json()
    if (
        not data
        or "title" not in data
        or "description" not in data
        or "deadline" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    if not task_manager.validate_deadline(data["deadline"]):
        return jsonify({"error": "Invalid deadline format. Use DD-MM-YYYY"}), 400

    task = task_manager.add_task(
        data.get("title"),
        data.get("description"),
        data.get("deadline"),
    )
    return jsonify({"message": "Task added", "task": task}), 201


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    success = task_manager.delete_task(task_id)
    if success:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
