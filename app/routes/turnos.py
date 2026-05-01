from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.turno import Turno

turnos = Blueprint('turnos', __name__)

@turnos.route('/turnos', methods=['GET'])
@login_required
def listar_turnos():
    # Si es dueño, ve sus turnos
    if current_user.rol == 'dueno':
        mis_turnos = Turno.query.filter_by(dueno_id=current_user.id).all()
    # Si es veterinario, ve los turnos que le asignaron
    elif current_user.rol == 'veterinario':
        mis_turnos = Turno.query.filter_by(veterinario_id=current_user.id).all()
    else:
        mis_turnos = []
    return render_template('turnos.html', turnos=mis_turnos)

@turnos.route('/turnos/agendar', methods=['GET','POST'])
@login_required
def agendar_turno():
    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        veterinario_id = request.form['veterinario_id']
        mascota_id = request.form['mascota_id']

        nuevo_turno = Turno(
            fecha=fecha,
            hora=hora,
            veterinario_id=veterinario_id,
            mascota_id=mascota_id,
            dueno_id=current_user.id,
            estado='ocupado'
        )
        db.session.add(nuevo_turno)
        db.session.commit()
        flash('Turno agendado exitosamente.')
        return redirect(url_for('turnos.listar_turnos'))

    return render_template('agendar_turno.html')
