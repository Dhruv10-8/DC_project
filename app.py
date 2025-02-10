from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/tasks/*": {"origins": "*"}})  # Allow CORS for task routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

# Add Task (POST)
@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid request format, JSON expected"}), 400

        data = request.get_json()
        description = data.get('description')
        due_date = data.get('due_date')

        if not description or not due_date:
            return jsonify({"error": "Both description and due_date are required"}), 400

        task = Task(description=description, due_date=due_date)
        db.session.add(task)
        db.session.commit()

        return jsonify({"message": "Task added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Display All Tasks (GET)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{"id": task.id, "description": task.description, "due_date": str(task.due_date)} for task in tasks]
    return jsonify(task_list)

# Delete Task by ID (DELETE)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
