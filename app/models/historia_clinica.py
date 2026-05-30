from app import db
from datetime import datetime

class Diagnostico(db.Model):
    __tablename__ = 'diagnostico'
    id = db.Column(db.Integer, primary_key=True)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    mascota = db.relationship('Mascota', backref='diagnosticos')
    veterinario = db.relationship('Usuario', foreign_keys=[veterinario_id])
    tratamientos = db.relationship('Tratamiento', backref='diagnostico', lazy=True)
    medicamentos = db.relationship('Medicamento', backref='diagnostico', lazy=True)


class Tratamiento(db.Model):
    __tablename__ = 'tratamiento'
    id = db.Column(db.Integer, primary_key=True)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnostico.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    duracion = db.Column(db.String(100), nullable=True)  # ej: "10 días"
    indicaciones = db.Column(db.Text, nullable=True)


class Medicamento(db.Model):
    __tablename__ = 'medicamento'
    id = db.Column(db.Integer, primary_key=True)
    diagnostico_id = db.Column(db.Integer, db.ForeignKey('diagnostico.id'), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    dosis = db.Column(db.String(100), nullable=False)      # ej: "5mg"
    frecuencia = db.Column(db.String(100), nullable=False) # ej: "cada 8 horas"
    duracion = db.Column(db.String(100), nullable=True)    # ej: "7 días"
