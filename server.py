from flask_socketio import SocketIO
from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='./templates/static')
socketio = SocketIO(app)
