from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.usuario import Usuario

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