from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.turno import Turno
from app.models.usuario import Usuario
from datetime import datetime, timedelta, date
from app.models.mascota import Mascota

turnos = Blueprint('turnos', __name__)

@turnos.route('/generar-turnos', methods=['GET', 'POST'])
@login_required
def generarTurnos():

    if request.method == 'POST':
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d') 
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d') 
        hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()
        duracion = int(request.form['duracion'])
        veterinario_id = int(request.form['veterinario_id'])
    

        hora_actual = hora_inicio
        fecha_actual = fecha_inicio
        
        while fecha_actual <=fecha_fin:
            hora_actual = hora_inicio

            while hora_actual <= hora_fin:

                nuevo_turno = Turno(fecha = fecha_actual, hora = hora_actual, veterinario_id = veterinario_id, estado = 'disponible', mascota_id = None, dueno_id = None, tipo_consulta = None)
                db.session.add(nuevo_turno)

                hora_datetime = datetime.combine(fecha_actual.date(), hora_actual)
                hora_datetime += timedelta(minutes=duracion)
                hora_actual = hora_datetime.time()

            fecha_actual += timedelta(days=1)
        
        db.session.commit()
        flash('Turno generado exitoxamente!')
        return redirect(url_for('turnos.listar_turnos'))
    

    veterinarios = Usuario.query.filter_by(rol='veterinario').all()
    return render_template('turnos/generar.html', veterinarios=veterinarios)


@turnos.route('/turnos', methods=['GET'])
@login_required
def listar_turnos():
    # Si es dueño, ve sus turnos
    if current_user.rol == 'dueno':
        mis_turnos = Turno.query.filter_by(dueno_id=current_user.id).all()
    # Si es veterinario, ve los turnos que le asignaron
    elif current_user.rol == 'veterinario':
        mis_turnos = Turno.query.filter_by(veterinario_id=current_user.id, estado = 'ocupado').all()
    else:
        mis_turnos = []
    return render_template('turnos/listar_turnos.html', turnos=mis_turnos)

@turnos.route('/turnos/agendar', methods=['GET','POST'])
@login_required
def agendar_turno():

    if request.method == 'POST':
        turno_id = request.form['turno_id']
        turno = Turno.query.get_or_404(turno_id)
        turno.estado = 'ocupado'
        turno.dueno_id = current_user.id
        turno.mascota_id = request.form['mascota_id']
        db.session.commit()
        flash('Turno agendado exitosamente!')
        return redirect(url_for('turnos.listar_turnos'))

    mascotas = Mascota.query.filter_by(dueno_id= current_user.id).all()

    turnos_disponibles = Turno.query.filter(
        Turno.estado == 'disponible',
        Turno.fecha >= date.today()
    ).all()
    return render_template('turnos/agendar_turno.html', turnos_disponibles=turnos_disponibles, mascotas=mascotas)
  
@turnos.route('/turnos/<int:id>/cancelar', methods=['POST'])
@login_required
def cancelar_turno(id):
    
    try:
        turno = Turno.query.get_or_404(id)
        
        fecha_hora_turno = datetime.combine(turno.fecha, turno.hora)
        fecha_hora_actual = datetime.now()
        
        if fecha_hora_turno <= fecha_hora_actual:
            flash('No se puede cancelar un turno pasado!', 'error')
            return redirect(url_for('turnos.listar_turnos')) 
        
        if current_user.rol == 'dueno':
            if turno.dueno_id != current_user.id: 
                flash('No puedes cancelar un turno que no es tuyo!', 'error')
                return redirect(url_for('turnos.listar_turnos'))
        
        elif current_user.rol == 'admin':
            pass  
        
        else:
            flash('No tienes permiso para cancelar turnos.', 'error')
            return redirect(url_for('turnos.listar_turnos'))
        
        turno.estado = 'disponible'
        turno.mascota_id = None
        turno.dueno_id = None
        
        db.session.commit()
        
      
        flash('Turno cancelado exitosamente!', 'success')
        return redirect(url_for('turnos.listar_turnos'))
        
    except Exception as e:
        db.session.rollback()
        flash(f' Error: {str(e)}', 'error')
        return redirect(url_for('turnos.listar_turnos'))