from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.mascota import Mascota

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.mascotas import mascotas
    app.register_blueprint(mascotas)

    from app.routes.turnos import turnos
    app.register_blueprint(turnos)

    return app

