from zidioproject import app
from flask_socketio import SocketIO

if __name__ == '__main__':
    app.config.from_pyfile("config.py")
    socketio = SocketIO(app)
    socketio.run(app, debug=True, port=7444, use_reloader=True)






