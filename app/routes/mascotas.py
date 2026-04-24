from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.mascota import Mascota

mascotas = Blueprint('mascotas', __name__)

@mascotas.route('/mis-mascotas')
@login_required
def listar():
    mis_mascotas = Mascota.query.filter_by(dueno_id=current_user.id).all()
    return render_template('mascotas/listar.html', mascotas=mis_mascotas)

@mascotas.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregarMascota():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        peso = request.form['peso']

        nuevaMascota = Mascota(nombre= nombre, especie=especie, raza=raza, edad=edad, peso=peso, dueno_id = current_user.id)
        db.session.add(nuevaMascota)
        db.session.commit()
        flash('Mascota agregada exitosamente!')
        return redirect(url_for('mascotas.listar'))
    return render_template('mascotas/agregar.html')
    
@mascotas.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editarMascota(id):
    mascotaBuscada = Mascota.query.get_or_404(id)
    if request.method == 'POST':
        mascotaBuscada.nombre = request.form['nombre']
        mascotaBuscada.especie = request.form['especie']
        mascotaBuscada.raza = request.form['raza']
        mascotaBuscada.edad = request.form['edad']
        mascotaBuscada.peso = request.form['peso']
        db.session.commit()
        flash('Mascota actualizada!')
        return redirect(url_for('mascotas.listar'))
    return render_template('mascotas/editar.html', mascotaBuscada=mascotaBuscada)
