<<<<<<< HEAD
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()   # ← instancia global
=======
﻿from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
>>>>>>> Brian

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

<<<<<<< HEAD
    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    # Modelos
    from app.models.mascota import Mascota

    # Blueprints
=======
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.mascota import Mascota
    from app.models.historia_clinica import Diagnostico, Tratamiento, Medicamento
    from app.models.tienda import Producto, CarritoItem, Compra, CompraItem

    @app.template_filter('strftime')
    def strftime_filter(date_obj, format_str='%d/%m/%Y'):
        if date_obj:
            return date_obj.strftime(format_str)
        return ''

    from app.models.turno import Turno

>>>>>>> Brian
    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.mascotas import mascotas
    app.register_blueprint(mascotas)

    from app.routes.turnos import turnos
    app.register_blueprint(turnos)

<<<<<<< HEAD
    # Configuración de correo
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'
    app.config['MAIL_PASSWORD'] = 'tu_app_password'
    app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo@gmail.com'
=======
    from app.routes.veterinario import veterinario
    app.register_blueprint(veterinario)

    from app.routes.tienda import tienda
    app.register_blueprint(tienda)
>>>>>>> Brian

    return app

