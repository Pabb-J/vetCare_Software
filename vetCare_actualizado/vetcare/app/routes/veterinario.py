from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.turno import Turno
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.historia_clinica import Diagnostico, Tratamiento, Medicamento
from datetime import date, timedelta
from functools import wraps

veterinario = Blueprint('veterinario', __name__)

# Decorador para restringir acceso solo a veterinarios
def solo_veterinario(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.rol != 'veterinario':
            flash('Acceso no autorizado.', 'error')
            return redirect(url_for('auth.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ─── HU-11: Agenda de turnos del veterinario ───────────────────────────────────

@veterinario.route('/veterinario/agenda')
@login_required
@solo_veterinario
def agenda():
    vista = request.args.get('vista', 'dia')  # dia | semana | mes
    hoy = date.today()

    if vista == 'semana':
        inicio = hoy - timedelta(days=hoy.weekday())
        fin = inicio + timedelta(days=6)
    elif vista == 'mes':
        inicio = hoy.replace(day=1)
        if hoy.month == 12:
            fin = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)
    else:  # dia
        inicio = hoy
        fin = hoy

    turnos = Turno.query.filter(
        Turno.veterinario_id == current_user.id,
        Turno.fecha >= inicio,
        Turno.fecha <= fin
    ).order_by(Turno.fecha, Turno.hora).all()

    return render_template('veterinario/agenda.html', turnos=turnos, vista=vista, hoy=hoy)


# ─── HU-12: Reprogramar turno ──────────────────────────────────────────────────

@veterinario.route('/veterinario/turnos/<int:id>/reprogramar', methods=['POST'])
@login_required
@solo_veterinario
def reprogramar_turno(id):
    turno = Turno.query.get_or_404(id)

    if turno.veterinario_id != current_user.id:
        flash('No podés reprogramar un turno que no es tuyo.', 'error')
        return redirect(url_for('veterinario.agenda'))

    # Notificamos al admin marcando estado como 'reprogramar'
    turno.estado = 'reprogramar'
    db.session.commit()
    flash('Se envió la solicitud de reprogramación al administrador.', 'success')
    return redirect(url_for('veterinario.agenda'))


# ─── HU-13: Perfil del veterinario ────────────────────────────────────────────

@veterinario.route('/veterinario/perfil')
@login_required
@solo_veterinario
def perfil():
    turnos = Turno.query.filter_by(
        veterinario_id=current_user.id, estado='ocupado'
    ).order_by(Turno.fecha, Turno.hora).all()

    # IDs de mascotas únicas atendidas por este veterinario
    mascota_ids = {t.mascota_id for t in turnos if t.mascota_id}
    mascotas = Mascota.query.filter(Mascota.id.in_(mascota_ids)).all()

    return render_template('veterinario/perfil.html',
                           turnos=turnos,
                           mascotas=mascotas)


# ─── HU-14: Registrar mascota (veterinario) ───────────────────────────────────

@veterinario.route('/veterinario/mascotas/registrar', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def registrar_mascota():
    if request.method == 'POST':
        dueno_dni = request.form.get('dueno_dni', '').strip()
        dueno = None
        if dueno_dni:
            dueno = Usuario.query.filter_by(dni=dueno_dni).first()
            if not dueno:
                flash('No se encontró un dueño con ese DNI. La mascota se registrará sin dueño.', 'error')

        mascota = Mascota(
            nombre=request.form['nombre'],
            especie=request.form['especie'],
            raza=request.form['raza'],
            edad=int(request.form['edad']),
            peso=float(request.form['peso']),
            dueno_id=dueno.id if dueno else None
        )
        db.session.add(mascota)
        db.session.commit()
        flash(f'Mascota "{mascota.nombre}" registrada correctamente.', 'success')
        return redirect(url_for('veterinario.agenda'))

    duenos = Usuario.query.filter_by(rol='dueno').all()
    return render_template('veterinario/registrar_mascota.html', duenos=duenos)


# ─── HU-15: Registrar diagnóstico ─────────────────────────────────────────────

@veterinario.route('/veterinario/diagnostico/nuevo', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def nuevo_diagnostico():
    if request.method == 'POST':
        mascota_id = request.form['mascota_id']
        mascota = Mascota.query.get_or_404(mascota_id)

        diagnostico = Diagnostico(
            mascota_id=mascota.id,
            veterinario_id=current_user.id,
            descripcion=request.form['descripcion'],
            observaciones=request.form.get('observaciones', '')
        )
        db.session.add(diagnostico)
        db.session.commit()
        flash('Diagnóstico registrado en la historia clínica.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=mascota.id))

    mascotas = Mascota.query.all()
    return render_template('veterinario/nuevo_diagnostico.html', mascotas=mascotas)


# ─── HU-16: Registrar tratamiento ─────────────────────────────────────────────

@veterinario.route('/veterinario/tratamiento/nuevo/<int:diagnostico_id>', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def nuevo_tratamiento(diagnostico_id):
    diagnostico = Diagnostico.query.get_or_404(diagnostico_id)

    if request.method == 'POST':
        tratamiento = Tratamiento(
            diagnostico_id=diagnostico.id,
            descripcion=request.form['descripcion'],
            duracion=request.form.get('duracion', ''),
            indicaciones=request.form.get('indicaciones', '')
        )
        db.session.add(tratamiento)
        db.session.commit()
        flash('Tratamiento registrado correctamente.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=diagnostico.mascota_id))

    return render_template('veterinario/nuevo_tratamiento.html', diagnostico=diagnostico)


# ─── HU-17: Registrar medicamento ─────────────────────────────────────────────

@veterinario.route('/veterinario/medicamento/nuevo/<int:diagnostico_id>', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def nuevo_medicamento(diagnostico_id):
    diagnostico = Diagnostico.query.get_or_404(diagnostico_id)

    if request.method == 'POST':
        medicamento = Medicamento(
            diagnostico_id=diagnostico.id,
            nombre=request.form['nombre'],
            dosis=request.form['dosis'],
            frecuencia=request.form['frecuencia'],
            duracion=request.form.get('duracion', '')
        )
        db.session.add(medicamento)
        db.session.commit()
        flash('Medicamento registrado en la historia clínica.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=diagnostico.mascota_id))

    return render_template('veterinario/nuevo_medicamento.html', diagnostico=diagnostico)


# ─── Historia clínica completa de una mascota ─────────────────────────────────

@veterinario.route('/veterinario/historia-clinica/<int:mascota_id>')
@login_required
@solo_veterinario
def historia_clinica(mascota_id):
    mascota = Mascota.query.get_or_404(mascota_id)
    diagnosticos = Diagnostico.query.filter_by(mascota_id=mascota_id)\
        .order_by(Diagnostico.fecha.desc()).all()
    return render_template('veterinario/historia_clinica.html',
                           mascota=mascota,
                           diagnosticos=diagnosticos)

# ─── Editar diagnóstico ────────────────────────────────────────────────────────
@veterinario.route('/veterinario/diagnostico/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def editar_diagnostico(id):
    diagnostico = Diagnostico.query.get_or_404(id)
    if request.method == 'POST':
        diagnostico.descripcion = request.form['descripcion']
        diagnostico.observaciones = request.form.get('observaciones', '')
        db.session.commit()
        flash('Diagnóstico actualizado.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=diagnostico.mascota_id))
    return render_template('veterinario/editar_diagnostico.html', diagnostico=diagnostico)

# ─── Editar tratamiento ────────────────────────────────────────────────────────
@veterinario.route('/veterinario/tratamiento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def editar_tratamiento(id):
    tratamiento = Tratamiento.query.get_or_404(id)
    if request.method == 'POST':
        tratamiento.descripcion = request.form['descripcion']
        tratamiento.duracion = request.form.get('duracion', '')
        tratamiento.indicaciones = request.form.get('indicaciones', '')
        db.session.commit()
        flash('Tratamiento actualizado.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=tratamiento.diagnostico.mascota_id))
    return render_template('veterinario/editar_tratamiento.html', tratamiento=tratamiento)

# ─── Editar medicamento ────────────────────────────────────────────────────────
@veterinario.route('/veterinario/medicamento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@solo_veterinario
def editar_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    if request.method == 'POST':
        medicamento.nombre = request.form['nombre']
        medicamento.dosis = request.form['dosis']
        medicamento.frecuencia = request.form['frecuencia']
        medicamento.duracion = request.form.get('duracion', '')
        db.session.commit()
        flash('Medicamento actualizado.', 'success')
        return redirect(url_for('veterinario.historia_clinica', mascota_id=medicamento.diagnostico.mascota_id))
    return render_template('veterinario/editar_medicamento.html', medicamento=medicamento)
