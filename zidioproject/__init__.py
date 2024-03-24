from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_mail import Mail,Message
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()



mail = Mail()
def create_app():
    from zidioproject.models import db
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile("config.py", silent=True)
    db.init_app(app)
    migrate = Migrate(app,db)
    socketio = SocketIO(app)
    csrf.init_app(app)
    return app, socketio
app, socketio = create_app()


from zidioproject import user_routes
from zidioproject.forms import *

