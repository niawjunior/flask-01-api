#!flask/bin/python
from flask import Flask, jsonify, make_response,abort, request, render_template

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/', methods=['GET'])
def index(name='Pasupol'):
    return render_template('index.html', name = name)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return abort(404)
    return jsonify({'tasks': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_all_task():
    return jsonify(tasks)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
    'id': tasks[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json.get('description', ""),
    'done': False
    }   
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def validate(error):
    return make_response(jsonify({'error': 'Field Title Can not Empty'}), 400)

if __name__ == '__main__':
    app.run(debug=True)