from flask import Flask, request, jsonify
 
app = Flask(__name__)
 
# In-memory storage for tasks
tasks = []
 
# Home route
@app.route('/')
def home():
    return "Task Manager API is running!"
 
# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)
 
# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201
 
# Update a task (mark as completed or change title)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404
 
# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200
 
if __name__ == '__main__':
    app.run(debug=True)