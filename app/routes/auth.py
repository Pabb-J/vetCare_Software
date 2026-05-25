from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from app import db, mail
from app.models.usuario import Usuario

auth = Blueprint('auth', __name__)

# Registro de usuario
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

        nuevo = Usuario(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            correo=correo,
            rol=rol
        )
        nuevo.set_password(password)
        db.session.add(nuevo)
        db.session.commit()
        flash('Cuenta creada exitosamente.')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for('auth.dashboard'))
        flash('Credenciales incorrectas.')

    return render_template('login.html')

# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Dashboard
@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Solicitud de recuperación de contraseña
@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        correo = request.form['correo']
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario:
            token = usuario.get_reset_token()
            link = url_for('auth.reset_password', token=token, _external=True)
            msg = Message("Recuperar contraseña", recipients=[correo])
            msg.body = f"Usa este enlace para restablecer tu contraseña: {link}"
            mail.send(msg)
            flash("Se envió un correo con instrucciones.")
            return redirect(url_for('auth.login'))
        else:
            flash("Si el correo existe, se enviará un enlace.")
    return render_template('reset_password_request.html')

# Restablecer contraseña
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    usuario = Usuario.verify_reset_token(token)
    if not usuario:
        flash("El enlace es inválido o ha expirado.")
        return redirect(url_for('auth.reset_password_request'))

    if request.method == 'POST':
        new_password = request.form['password']
        usuario.set_password(new_password)
        db.session.commit()
        flash("Contraseña actualizada correctamente.")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')
