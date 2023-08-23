import bcrypt
from flask import Flask
# Importing custom form classes from a 'forms' module
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    # Creating an instance of the Flask class
    app = Flask(__name__)
# Configuring the app's secret key
    app.config['SECRET_KEY'] = '4c3099db0ecb9b7001591977431185fa'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    from flaskblog.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
