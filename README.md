## Flask-RESTPlus
Create a `todo.py` file containing the following code (from [Flask-RESTPlus documentation](https://flask-restplus.readthedocs.io/en/stable/example.html)) and run it with `python3 todo.py`.
```
from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Todo API',
    description='A simple TODO API',
)

ns = api.namespace('todos', description='TODO operations')

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

todo = api.model('Todo', {
    'task': fields.String(required=True, description='The task details')
})

listed_todo = api.model('ListedTodo', {
    'id': fields.String(required=True, description='The todo ID'),
    'todo': fields.Nested(todo, description='The Todo')
})


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

parser = api.parser()
parser.add_argument('task', type=str, required=True, help='The task details', location='form')


@ns.route('/<string:todo_id>')
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='todo_id should be in {0}'.format(', '.join(TODOS.keys())))
    @api.marshal_with(todo)
    def get(self, todo_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @api.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        '''Delete a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @api.doc(parser=parser)
    @api.marshal_with(todo)
    def put(self, todo_id):
        '''Update a given resource'''
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.marshal_list_with(listed_todo)
    def get(self):
        '''List all todos'''
        return [{'id': id, 'todo': todo} for id, todo in TODOS.items()]

    @api.doc(parser=parser)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a todo'''
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


if __name__ == '__main__':
    app.run(debug=True)

```

You can test your *todo* API with:

| description | verb | path | command |
|---|---|---|---|
| List all todos | GET | /todos/ | curl -X GET --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/' |
| Create a todo | POST | /todos/ | curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'task=read%20documentation' 'http://127.0.0.1:5000/todos/' |
| Fetch a todo | GET | /todos/{todo_id} | curl -X GET --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/todo1'
| Update a todo | PUT | /todos/{todo_id} | curl -X PUT --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'task=update%20documentation' 'http://127.0.0.1:5000/todos/todo2'
| Delete a todo | DELETE | /todos/{todo_id} | curl -X DELETE --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/todo3' |


The API class from *Flask-RESTPlus* automatically generates API documentation from annotations. You can browse the documentation at [http://localhost:5000/#](http://127.0.0.1:5000/#). The [Swagger](http://swagger.io/) documentation UI is generated from a [swagger.json](http://127.0.0.1:5000/swagger.json) file using javascript.

Note that this is a minimal example. Real applications split their codebase into [modules](https://docs.python.org/3/tutorial/modules.html).
 The *Todo* model uses a simple dictionnary structure (*TODOS*) and does not persist objects into database (these are destroyed upon restart).
