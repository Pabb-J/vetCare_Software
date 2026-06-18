    from flask import Flask, redirect, url_for
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

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    from app.models.mascota import Mascota
    from app.models.historia_clinica import Diagnostico, Tratamiento, Medicamento
    from app.models.tienda import Producto, CarritoItem, Compra, CompraItem

    @app.template_filter('strftime')
    def strftime_filter(date_obj, format_str='%d/%m/%Y'):
        if date_obj:
            return date_obj.strftime(format_str)
        return ''

    from app.models.turno import Turno

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.mascotas import mascotas
    app.register_blueprint(mascotas)

    from app.routes.turnos import turnos
    app.register_blueprint(turnos)

    from app.routes.veterinario import veterinario
    app.register_blueprint(veterinario)

    from app.routes.tienda import tienda
    app.register_blueprint(tienda)

    return app

