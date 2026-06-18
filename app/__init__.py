from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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
    from app.models.usuario import Usuario

    class AdminView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated and current_user.rol == 'admin'
        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('auth.login'))

    admin = Admin(app, name='VetCare Admin')
    admin.add_view(AdminView(Usuario, db.session))
    admin.add_view(AdminView(Mascota, db.session))
    admin.add_view(AdminView(Turno, db.session))
    admin.add_view(AdminView(Diagnostico, db.session))
    admin.add_view(AdminView(Tratamiento, db.session))
    admin.add_view(AdminView(Medicamento, db.session))
    admin.add_view(AdminView(Producto, db.session))
    admin.add_view(AdminView(CarritoItem, db.session))
    admin.add_view(AdminView(Compra, db.session))
    admin.add_view(AdminView(CompraItem, db.session))

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

