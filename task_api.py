from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mohammed%409360@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Task Manager API with PostgreSQL!"

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status
    }), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status
    } for t in tasks])

if __name__ == '__main__':
    app.run(debug=True)
