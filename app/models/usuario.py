from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< HEAD
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
=======
>>>>>>> Brian

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
<<<<<<< HEAD
    reset_token = db.Column(db.String(100), nullable=True) #  permite guardar un token temporal cuando el usuario pide recuperar su contraseña.
    
=======

>>>>>>> Brian
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

<<<<<<< HEAD
    def get_reset_token(self, expires_sec=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.correo, salt='password-reset')

    @staticmethod
    def verify_reset_token(token, expires_sec=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            correo = s.loads(token, salt='password-reset', max_age=expires_sec)
        except:
            return None
        return Usuario.query.filter_by(correo=correo).first()
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
=======
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
>>>>>>> Brian
