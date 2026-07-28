from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.mascota import Mascota
from app.models.usuario import Usuario
from app.models.historia_clinica import Diagnostico

mascotas = Blueprint('mascotas', __name__)

@mascotas.route('/mis-mascotas')
@login_required
def listar():
    if current_user.rol == 'dueno':
        mis_mascotas = Mascota.query.filter_by(dueno_id=current_user.id).all()
    elif current_user.rol == 'veterinario':
        mis_mascotas = Mascota.query.all()
    else:
        mis_mascotas = Mascota.query.all()
    return render_template('mascotas/listar.html', mascotas=mis_mascotas)

@mascotas.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregarMascota():
    if current_user.rol not in ('veterinario', 'admin'):
        flash('Tu mascota la registra el veterinario con tu DNI, no podés agregarla vos mismo.', 'error')
        return redirect(url_for('mascotas.listar'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        peso = request.form['peso']
        dueno_dni = request.form['dueno_dni']
        
        print(f"DEBUG: Buscando dueño con DNI: {dueno_dni}")
        dueno = Usuario.query.filter_by(dni = dueno_dni).first()
        print(f"DEBUG: Dueño encontrado: {dueno}")

        if not dueno:
            print(f"DEBUG: No existe dueño con DNI: {dueno_dni}")
            flash('No existe ese dueño')
            return redirect(url_for('mascotas.agregarMascota')) 

        print(f"DEBUG: Agregando mascota para dueño: {dueno.nombre} {dueno.apellido} (ID: {dueno.id})")
        nuevaMascota = Mascota(nombre= nombre, especie=especie, raza=raza, edad=edad, peso=peso, dueno_id = dueno.id)
        db.session.add(nuevaMascota)
        
        try:
            db.session.commit()
            print(f"DEBUG: Mascota agregada exitosamente con ID: {nuevaMascota.id}")
            flash('Mascota agregada exitosamente!')
            return redirect(url_for('mascotas.listar'))
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: Error al agregar mascota: {e}")
            flash(f'Error al agregar mascota: {str(e)}')
            return redirect(url_for('mascotas.agregarMascota'))
    return render_template('mascotas/agregar.html')


@mascotas.route('/mascotas/detalle/<int:id>')
@login_required
def detalle(id):
    mascota = Mascota.query.get_or_404(id)

    # El dueño solo puede ver el detalle de SUS propias mascotas.
    # Veterinario y admin pueden ver el detalle de cualquier mascota.
    if current_user.rol == 'dueno' and mascota.dueno_id != current_user.id:
        flash('No tenés acceso a esa mascota.', 'error')
        return redirect(url_for('mascotas.listar'))

    diagnosticos = Diagnostico.query.filter_by(mascota_id=mascota.id)\
        .order_by(Diagnostico.fecha.desc()).all()

    return render_template('mascotas/detalle.html', mascota=mascota, diagnosticos=diagnosticos)


@mascotas.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editarMascota(id):
    if current_user.rol not in ('veterinario', 'admin'):
        flash('Solo el veterinario o el administrador pueden editar los datos de una mascota.', 'error')
        return redirect(url_for('mascotas.listar'))

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
