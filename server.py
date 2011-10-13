import json
import pymongo
from bson.objectid import ObjectId
from bson import json_util

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/todos/', defaults={'todo_id': None}, methods=['GET','POST'])
@app.route('/todos/<todo_id>',  methods=['GET','POST','PUT','DELETE'])
def todos_api(todo_id):
    method = request.method.upper()
    body = None
    
    if method == 'GET':
        body = get_todos(todo_id)
    elif method == 'POST':
        body = save_todo(request.json)
    elif method == 'PUT':
        body = update_todo(todo_id, request.json)
    else:
        body = {'error': 'no method found'}
    
    resp = make_response(json.dumps(body, default=json_util.default))
    resp.mimetype = 'application/json'
    
    return resp

def get_todos(todo_id):
    todos = get_collection()
    todo = todos.find_one({'_id': ObjectId(todo_id)})
    
    todo['id'] = str(todo['_id'])
    del todo['_id']
    
    return todo

def save_todo(data):
    todos = get_collection()
    oid = todos.insert(data)
    return {'id': str(oid)}

def update_todo(todo_id, data):
    todos = get_collection()
    todos.update({'_id': ObjectId(todo_id)}, {'$set': data})
    return {'message': 'OK'}

def delete_todo(todo_id):
    return {}

def get_collection():
    conn = pymongo.Connection('localhost', 27017)
    return conn[app.db_name].todos

if __name__ == '__main__':
    app.db_name = 'todos_prod'
    app.run(host='0.0.0.0')
