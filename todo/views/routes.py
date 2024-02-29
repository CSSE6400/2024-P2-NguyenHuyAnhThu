from flask import Blueprint, jsonify, request 
from todo.models import db 
from todo.models.todo import Todo 
from datetime import datetime
from flask import Blueprint, jsonify
 
api = Blueprint('api', __name__, url_prefix='/api/v1') 

TEST_ITEM = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2023-02-27T00:00:00",
    "created_at": "2023-02-20T00:00:00",
    "updated_at": "2023-02-20T00:00:00"
}
 
@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


# @api.route('/todos', methods=['GET'])
# def get_todos():
#     """Return the list of todo items"""
#     return jsonify([TEST_ITEM])

#This will query the database for all the todos and return them as JSON
@api.route('/todos', methods=['GET']) 
def get_todos(): 
   query = request.args.to_dict(flat=False) #=>>> Get parameters from URL 
   todos = Todo.query.all() 
   result = [] 
   if len(query) == 0:
      for todo in todos: 
         result.append(todo.to_dict()) 
   else:
      for todo in todos:
         for i in list(query.keys()):
            if len(query[i]) > 1: return jsonify({'error': 'Parameter not valid'}), 400 
            todo_dict = todo.to_dict()[i]
            print("tdo_dict:", str(todo_dict).lower())
            print("query:", ''.join(query[i]))
            if str(todo_dict).lower() == ''.join(query[i]): result.append(todo.to_dict()) 
   return jsonify(result)

# @api.route('/todos/<int:todo_id>', methods=['GET'])
# def get_todo(todo_id):
#     """Return the details of a todo item"""
#     return jsonify(TEST_ITEM)

#This will query the database for the todos based on todo_id and return them as JSON
@api.route('/todos/<int:todo_id>', methods=['GET']) 
def get_todo(todo_id): 
   todo = Todo.query.get(todo_id) 
   if todo is None: 
      return jsonify({'error': 'Todo not found'}), 404 
   return jsonify(todo.to_dict())

# @api.route('/todos', methods=['POST'])
# def create_todo():
#     """Create a new todo item and return the created item"""
#     return jsonify(TEST_ITEM), 201

#Add todo
@api.route('/todos', methods=['POST']) 
def create_todo(): 
   todo = Todo( 
      title=request.json.get('title'), 
      description=request.json.get('description'), 
      completed=request.json.get('completed', False), 
   ) 
   
   if not set(list(request.get_json().keys())).issubset(list(todo.to_dict().keys())): return jsonify({'error':'Undefined fields'}), 400

   if 'deadline_at' in request.json: 
      todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at')) 
 
   # Adds a new record to the database or will update an existing record 
   db.session.add(todo) 
   # Commits the changes to the database, this must be called for the changes to be saved 
   db.session.commit() 
   return jsonify(todo.to_dict()), 201

# @api.route('/todos/<int:todo_id>', methods=['PUT'])
# def update_todo(todo_id):
#     """Update a todo item and return the updated item"""
#     return jsonify(TEST_ITEM)

#update todo
@api.route('/todos/<int:todo_id>', methods=['PUT']) 
def update_todo(todo_id): 
   todo = Todo.query.get(todo_id) 
   if todo is None: 
      return jsonify({'error': 'Todo not found'}), 404 
   #request.get_json(): get body request's json
   #Can;t add extra fields
   if not set(list(request.get_json().keys())).issubset(list(todo.to_dict().keys())): return jsonify({'error':'Undefined fields'}), 400
   # print(list(todo.to_dict().keys())) ==> have to convert object to dictionary (to_dict is defined in class Todo)
   #Can't change id
   if request.json.get("id"): return jsonify({'error':"Cant change id"}), 400
 
   todo.title = request.json.get('title', todo.title) 
   todo.description = request.json.get('description', todo.description) 
   todo.completed = request.json.get('completed', todo.completed) 
   todo.deadline_at = request.json.get('deadline_at', todo.deadline_at) 
   db.session.commit() 
 
   return jsonify(todo.to_dict())

# @api.route('/todos/<int:todo_id>', methods=['DELETE'])
# def delete_todo(todo_id):
#     """Delete a todo item and return the deleted item"""
#     return jsonify(TEST_ITEM)

#delete todo
@api.route('/todos/<int:todo_id>', methods=['DELETE']) 
def delete_todo(todo_id): 
   todo = Todo.query.get(todo_id) 
   if todo is None: 
      return jsonify({}), 200 
 
   db.session.delete(todo) 
   db.session.commit() 
   return jsonify(todo.to_dict()), 200
 
