from app import db

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)
    dueno_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    estado = db.Column(db.String(20), default='disponible')  # disponible, ocupado, cancelado
    tipo_consulta = db.Column(db.String(50), nullable=True)

    veterinario = db.relationship('Usuario', foreign_keys=[veterinario_id])
    dueno = db.relationship('Usuario', foreign_keys=[dueno_id])
    mascota = db.relationship('Mascota', foreign_keys=[mascota_id])




