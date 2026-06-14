from app import db
from datetime import datetime

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(80), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    imagen_url = db.Column(db.String(500), nullable=True)
    imagen_ancho = db.Column(db.Integer, default=300)
    imagen_alto  = db.Column(db.Integer, default=200)

    items_carrito = db.relationship('CarritoItem', backref='producto', lazy=True)

    def __repr__(self):
        return f'<Producto {self.nombre}>'


class CarritoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __repr__(self):
        return f'<CarritoItem usuario={self.usuario_id} producto={self.producto_id}>'


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    items = db.relationship('CompraItem', backref='compra', lazy=True)

    def __repr__(self):
        return f'<Compra {self.id} usuario={self.usuario_id}>'


class CompraItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto')

    def subtotal(self):
        return self.cantidad * self.precio_unitario
