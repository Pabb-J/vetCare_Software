from app import db

class Mascota (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    especie = db.Column(db.String(50), nullable = False)
    raza = db.Column(db.String(50), nullable = False)
    edad = db.Column(db.Integer, nullable = False)
    peso = db.Column(db.Float, nullable = False)
    dueno_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)

