from collections import UserDict
from flask import Flask
from flask.ext.cors import CORS
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
CORS(app)
#app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Todo API',
    description='A simple TODO API',
)

ns = api.namespace('todos', description='TODO operations')

class TodoDict(UserDict):
    def __getitem__(self, key):
        return {'todo_id': key, **UserDict.__getitem__(self, key)}

TODOS = TodoDict({
    1 : {'title': 'build an API', 'order': 1, 'completed': False},
    2 : {'title': '?????', 'order': 2, 'completed': False},
    3 : {'title': 'profit!', 'order': 3, 'completed': False},
})

todo = api.model('Todo', {
    'title': fields.String(required=True, description='The task details'),
    'completed': fields.Boolean(default=False, decription='Task completed flag'),
    'order': fields.Integer(description='Task order'),
    'url': fields.Url('todo', absolute=True)
})


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

parser = api.parser()
parser.add_argument('title', type=str, help='The task details')
parser.add_argument('order', type=int, help='Task order')
parser.add_argument('completed', type=bool, help='Task completed flag')


@ns.route('/<int:todo_id>', endpoint='todo')
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    #@api.doc(description='todo_id should be in {0}'.format(', '.join(TODOS.keys())))
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
    def patch(self, todo_id):
        '''Update a given resource'''
        task = TODOS[todo_id]
        print(parser.parse_args())
        for k, v in parser.parse_args().items():
            if v is not None:
                task[k] = v
        TODOS[todo_id] = task
        return task


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.marshal_list_with(todo)
    def get(self):
        '''List all todos'''
        return list(TODOS.values())

    @api.doc(parser=parser)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a todo'''
        args = parser.parse_args()
        todo_id = len(TODOS) + 1
        TODOS[todo_id] = {
            'title': args['title'],
            'order': args['order'],
            'completed': args['completed'],
        }
        return TODOS[todo_id], 201


if __name__ == '__main__':
    app.run(debug=True)
