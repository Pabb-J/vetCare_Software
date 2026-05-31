from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.mascota import Mascota

mascota_bp = Blueprint('mascota', __name__)

@mascota_bp.route('/mascotas', methods=['GET'])
@login_required
def listar_mascotas():
    mascotas = Mascota.query.filter_by(dueno_id=current_user.id).all()
    return render_template('mascotas.html', mascotas=mascotas)

@mascota_bp.route('/mascotas/agregar', methods=['GET', 'POST'])
@login_required
def agregar_mascota():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        edad = request.form['edad']

        nueva_mascota = Mascota(nombre=nombre, especie=especie, edad=edad, dueno_id=current_user.id)
        db.session.add(nueva_mascota)
        db.session.commit()
        flash('Mascota agregada exitosamente.')
        return redirect(url_for('mascota.listar_mascotas'))

    return render_template('agregar_mascota.html')