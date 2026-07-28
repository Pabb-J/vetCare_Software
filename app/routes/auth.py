from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario
import logging

logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        telefono = request.form['telefono']
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']

        if Usuario.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('auth.registro'))

        if Usuario.query.filter_by(dni=dni).first():
            flash('El DNI ya está registrado.')
            return redirect(url_for('auth.registro'))

        nuevo = Usuario(nombre=nombre, apellido=apellido, dni=dni, telefono=telefono, correo=correo, rol=rol)
        nuevo.set_password(password)
        db.session.add(nuevo)
        db.session.commit()
        flash('Cuenta creada exitosamente.')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and not usuario.activo:
            flash('Esta cuenta fue dada de baja. Contactá al administrador.')
            return render_template('login.html')

        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for('auth.dashboard'))
        flash('Credenciales incorrectas.')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/perfil')
@login_required
def perfil_dueno():
    from app.models.turno import Turno
    from app.models.mascota import Mascota
    turnos = Turno.query.filter_by(dueno_id=current_user.id).order_by(Turno.fecha, Turno.hora).all()
    mascotas = Mascota.query.filter_by(dueno_id=current_user.id).all()
    logger.info(f"User {current_user.id} ({current_user.correo}) has {len(mascotas)} mascotas")
    for mascota in mascotas:
        logger.info(f"  - Mascota: {mascota.nombre} (ID: {mascota.id})")
    return render_template('perfil_dueno.html', turnos=turnos, mascotas=mascotas)



@auth.route('/olvide-contrasena', methods=['GET', 'POST'])
def olvide_contrasena():
    if request.method == 'POST':
        correo = request.form.get('correo')
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario:
            return redirect(url_for('auth.nueva_contrasena', usuario_id=usuario.id))
        flash('No existe una cuenta con ese correo.')
    return render_template('olvide_contrasena.html')

@auth.route('/nueva-contrasena/<int:usuario_id>', methods=['GET', 'POST'])
def nueva_contrasena(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        nueva = request.form.get('password')
        confirmar = request.form.get('confirmar')
        if nueva != confirmar:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('auth.nueva_contrasena', usuario_id=usuario_id))
        if len(nueva) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('auth.nueva_contrasena', usuario_id=usuario_id))
        usuario.set_password(nueva)
        db.session.commit()
        flash('Contraseña actualizada correctamente.')
        return redirect(url_for('auth.login'))
    return render_template('nueva_contrasena.html', usuario=usuario)