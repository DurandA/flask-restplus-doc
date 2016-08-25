# Flask-RESTPlus example
## TodoMVC
The [Flask-RESTPlus documentation](https://flask-restplus.readthedocs.io/en/stable) includes an [example](https://flask-restplus.readthedocs.io/en/stable/example.html)) of a [TodoMVC](https://todomvc.com/TodoMVC) API. TodoMVC is "a project which offers the same Todo application implemented using MV* concepts in most of the popular JavaScript MV* frameworks of today.".

While exploring RESTful APIs, we will use a simple "todo" application as an example. This example is compatible with [TodoMVC](https://todomvc.com/TodoMVC). TodoMVC is "a project which offers the same Todo application implemented using MV* concepts in most of the popular JavaScript MV* frameworks of today." You can try your API using any of the TodoMVC clients (e.g. [Todo-Backend's client](http://www.todobackend.com/client/)). You can also compare different frameworks with the [Todo-Backend](http://www.todobackend.com/) project as they offer "a shared example to showcase backend tech stacks" as they provides a similar RESTful API.

## Running the example
Let's grab the todo example from [Flask-RESTPlus documentation](https://flask-restplus.readthedocs.io/en/stable/example.html) or copy the following code to a `todo.py` file and run it with `python3 todo.py`.
```
from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
```

Test your API on your browser with the TodoMVC client http://www.todobackend.com/client/. Point to `127.0.0.1:5000` (5000 is the default port on the debug server). Use you browser built-in network debugger to see how the application client and backend are interacting. Alternatively, use an HTTP debugger like (Fiddler)[http://www.telerik.com/fiddler] or any network analyzer that can parse HTTP requests. Mastering one of these tools is necessary to complete your project without headaches.

You can also query the *todo* API directly with curl:

| description | verb | path | command |
|---|---|---|---|
| List all todos | GET | /todos/ | curl -X GET --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/' |
| Create a todo | POST | /todos/ | curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'task=read%20documentation' 'http://127.0.0.1:5000/todos/' |
| Fetch a todo | GET | /todos/{todo_id} | curl -X GET --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/todo1'
| Update a todo | PUT | /todos/{todo_id} | curl -X PUT --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'task=update%20documentation' 'http://127.0.0.1:5000/todos/todo2'
| Delete a todo | DELETE | /todos/{todo_id} | curl -X DELETE --header 'Accept: application/json' 'http://127.0.0.1:5000/todos/todo3' |

## Dissecting the example
The code starts by importing the `Flask` class from `flask` library as well as `Api` and `Resource` classes and `fields` object from `flask_restplus` library.
```
from flask import Flask
from flask_restplus import Api, Resource, fields
```
The Flask object represents your webserver application.
```
app = Flask(__name__)
```
The webserver is initialized with import_name=[__main__](https://docs.python.org/3/library/__main__.html) https://docs.python.org/3/library/__main__.html

The Api object is useful to describe your ressources and methods and can generate documentation from your code.
```
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)
```
We will check the generated API documentation later in this document.

```
ns = api.namespace('todos', description='TODO operations')
```
Here we declare a namespace so that each function of this namespace will be accessible through the `todos` root path or subpath (i.e. `http://example.com/todos`).

The Todo API enables *todo* objects CRUD (create, read, update and delete) through JSON representation. In order for your *todo* resources to be serialized and deserialized properly as well as to define the data model in the documentation, the `Model` object is used.
```
todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})
```
This example use a simple [data access object](https://en.wikipedia.org/wiki/Data_access_object) to store and retrieve the todos. The TodoDAO stores the todos an arry structure (`todos` array stored in `TodoDAO` instance) and does not persist objects into database (these are destroyed upon restart).

```
class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

            if todo['id'] == id:
    def get(self, id):
        for todo in self.todos:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)
```
The DAO is initialized and we create three example todos.
```
DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})
```

```
@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201
```

```
@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
```

```
if __name__ == '__main__':
    app.run(debug=True)
```
The `if __name__ == '__main__'` ensures that the script is executed directly (i.e. it is not imported). The application is started in debug mode. Debug mode provides

## Common mistakes
same-origin policy
```
from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
```



The API class from *Flask-RESTPlus* automatically generates API documentation from annotations. You can browse the documentation at [http://localhost:5000/#](http://127.0.0.1:5000/#). The [Swagger](http://swagger.io/) documentation UI is generated from a [swagger.json](http://127.0.0.1:5000/swagger.json) file using javascript.




Note that this is a minimal example. Real applications split their codebase into [modules](https://docs.python.org/3/tutorial/modules.html).
