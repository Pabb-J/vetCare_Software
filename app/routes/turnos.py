from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.turno import Turno
from app.models.usuario import Usuario
from datetime import datetime, timedelta, date
from app.models.mascota import Mascota
from collections import defaultdict

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
    
    # Build calendar data: for each vet, which dates have turnos
    turnos_all = Turno.query.filter(Turno.fecha >= date.today()).all()
    cal_data = defaultdict(lambda: {'disponible': 0, 'ocupado': 0, 'cancelado': 0, 'total': 0})
    for t in turnos_all:
        key = f"{t.fecha.isoformat()}_{t.veterinario_id}"
        cal_data[key][t.estado] = cal_data[key].get(t.estado, 0) + 1
        cal_data[key]['total'] += 1

    veterinarios = Usuario.query.filter_by(rol='veterinario').all()
    return render_template('turnos/generar.html', veterinarios=veterinarios, turnos_data=dict(cal_data))


@turnos.route('/turnos', methods=['GET'])
@login_required
def listar_turnos():
    if current_user.rol == 'dueno':
        mis_turnos = Turno.query.filter_by(dueno_id=current_user.id).all()
        return render_template('turnos/listar_turnos.html', turnos=mis_turnos)
    elif current_user.rol == 'veterinario':
        mis_turnos = Turno.query.filter_by(veterinario_id=current_user.id, estado='ocupado').all()
        return render_template('turnos/listar_turnos.html', turnos=mis_turnos)
    # Admin: redirect to admin panel
    return redirect(url_for('turnos.admin_turnos'))

@turnos.route('/turnos/admin', methods=['GET', 'POST'])
@login_required
def admin_turnos():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))

    filtro_estado = request.args.get('estado', 'todos')
    filtro_vet = request.args.get('veterinario', 'todos')
    filtro_fecha_desde = request.args.get('fecha_desde', '')
    filtro_fecha_hasta = request.args.get('fecha_hasta', '')
    busqueda = request.args.get('busqueda', '')

    query = Turno.query

    if filtro_estado != 'todos':
        query = query.filter(Turno.estado == filtro_estado)
    if filtro_vet != 'todos':
        query = query.filter(Turno.veterinario_id == int(filtro_vet))
    if filtro_fecha_desde:
        query = query.filter(Turno.fecha >= datetime.strptime(filtro_fecha_desde, '%Y-%m-%d').date())
    if filtro_fecha_hasta:
        query = query.filter(Turno.fecha <= datetime.strptime(filtro_fecha_hasta, '%Y-%m-%d').date())

    turnos = query.order_by(Turno.fecha.desc(), Turno.hora.desc()).all()

    # Stats
    total = len(turnos)
    disponibles = sum(1 for t in turnos if t.estado == 'disponible')
    ocupados = sum(1 for t in turnos if t.estado == 'ocupado')
    cancelados = sum(1 for t in turnos if t.estado == 'cancelado')
    reprogramar = sum(1 for t in turnos if t.estado == 'reprogramar')

    veterinarios = Usuario.query.filter_by(rol='veterinario').all()

    return render_template('turnos/admin_turnos.html',
                           turnos=turnos,
                           veterinarios=veterinarios,
                           filtro_estado=filtro_estado,
                           filtro_vet=filtro_vet,
                           filtro_fecha_desde=filtro_fecha_desde,
                           filtro_fecha_hasta=filtro_fecha_hasta,
                           total=total, disponibles=disponibles,
                           ocupados=ocupados, cancelados=cancelados,
                           reprogramar=reprogramar)

@turnos.route('/turnos/admin/reprogramar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_reprogramar(id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))

    turno = Turno.query.get_or_404(id)

    if request.method == 'POST':
        nueva_fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        nueva_hora = datetime.strptime(request.form['hora'], '%H:%M').time()

        # Check if slot is already occupied
        conflicto = Turno.query.filter(
            Turno.veterinario_id == turno.veterinario_id,
            Turno.fecha == nueva_fecha,
            Turno.hora == nueva_hora,
            Turno.estado.in_(['ocupado', 'reprogramar']),
            Turno.id != id
        ).first()
        if conflicto:
            flash('Ese horario ya está ocupado por otro turno.', 'error')
            return render_template('turnos/admin_reprogramar.html', turno=turno)

        turno.fecha = nueva_fecha
        turno.hora = nueva_hora
        turno.estado = 'ocupado'
        db.session.commit()
        flash('Turno reprogramado exitosamente.', 'success')
        return redirect(url_for('turnos.admin_turnos'))

    return render_template('turnos/admin_reprogramar.html', turno=turno)

# ─── Admin: list/delete dueños ───
@turnos.route('/admin/duenos')
@login_required
def admin_duenos():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    duenos = Usuario.query.filter_by(rol='dueno').order_by(Usuario.apellido).all()
    return render_template('turnos/admin_duenos.html', duenos=duenos)

@turnos.route('/admin/duenos/<int:id>/eliminar', methods=['POST'])
@login_required
def admin_eliminar_dueno(id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    dueno = Usuario.query.get_or_404(id)
    if dueno.rol != 'dueno':
        flash('El usuario no es un dueño.', 'error')
        return redirect(url_for('turnos.admin_duenos'))
    dueno.activo = False
    db.session.commit()
    flash(f'Dueño {dueno.nombre} {dueno.apellido} dado de baja.', 'success')
    return redirect(url_for('turnos.admin_duenos'))

@turnos.route('/admin/duenos/<int:id>/reactivar', methods=['POST'])
@login_required
def admin_reactivar_dueno(id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    dueno = Usuario.query.get_or_404(id)
    if dueno.rol != 'dueno':
        flash('El usuario no es un dueño.', 'error')
        return redirect(url_for('turnos.admin_duenos'))
    dueno.activo = True
    db.session.commit()
    flash(f'Dueño {dueno.nombre} {dueno.apellido} reactivado.', 'success')
    return redirect(url_for('turnos.admin_duenos'))

# ─── Admin: list/delete veterinarios ───
@turnos.route('/admin/veterinarios')
@login_required
def admin_veterinarios():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    veterinarios = Usuario.query.filter_by(rol='veterinario').order_by(Usuario.apellido).all()
    return render_template('turnos/admin_veterinarios.html', veterinarios=veterinarios)

@turnos.route('/admin/veterinarios/<int:id>/eliminar', methods=['POST'])
@login_required
def admin_eliminar_veterinario(id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    vet = Usuario.query.get_or_404(id)
    if vet.rol != 'veterinario':
        flash('El usuario no es un veterinario.', 'error')
        return redirect(url_for('turnos.admin_veterinarios'))
    # Liberar turnos futuros de este veterinario
    Turno.query.filter(
        Turno.veterinario_id == id,
        Turno.fecha >= date.today(),
        Turno.estado == 'disponible'
    ).delete()
    vet.activo = False
    db.session.commit()
    flash(f'Veterinario {vet.nombre} {vet.apellido} eliminado.', 'success')
    return redirect(url_for('turnos.admin_veterinarios'))

@turnos.route('/admin/veterinarios/<int:id>/reactivar', methods=['POST'])
@login_required
def admin_reactivar_veterinario(id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))
    vet = Usuario.query.get_or_404(id)
    if vet.rol != 'veterinario':
        flash('El usuario no es un veterinario.', 'error')
        return redirect(url_for('turnos.admin_veterinarios'))
    vet.activo = True
    db.session.commit()
    flash(f'Veterinario {vet.nombre} {vet.apellido} reactivado.', 'success')
    return redirect(url_for('turnos.admin_veterinarios'))

# ─── Admin: crear turno específico ───
@turnos.route('/admin/turnos/crear', methods=['GET', 'POST'])
@login_required
def admin_crear_turno():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        veterinario_id = int(request.form['veterinario_id'])
        dueno_id = int(request.form['dueno_id'])
        mascota_id = request.form.get('mascota_id')
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        hora = datetime.strptime(request.form['hora'], '%H:%M').time()

        # Check slot not occupied
        conflicto = Turno.query.filter(
            Turno.veterinario_id == veterinario_id,
            Turno.fecha == fecha,
            Turno.hora == hora,
            Turno.estado == 'ocupado'
        ).first()
        if conflicto:
            flash('Ese horario ya está ocupado.', 'error')
            return redirect(url_for('turnos.admin_crear_turno'))

        turno = Turno(
            fecha=fecha, hora=hora,
            veterinario_id=veterinario_id,
            dueno_id=dueno_id if dueno_id else None,
            mascota_id=int(mascota_id) if mascota_id else None,
            estado='ocupado'
        )
        db.session.add(turno)
        db.session.commit()
        flash('Turno creado exitosamente.', 'success')
        return redirect(url_for('turnos.admin_turnos'))

    veterinarios = Usuario.query.filter_by(rol='veterinario', activo=True).all()
    duenos = Usuario.query.filter_by(rol='dueno', activo=True).all()
    mascotas = Mascota.query.all()
    return render_template('turnos/admin_crear_turno.html',
                           veterinarios=veterinarios,
                           duenos=duenos,
                           mascotas=mascotas)

@turnos.route('/turnos/agendar', methods=['GET','POST'])
@login_required
def agendar_turno():

    if request.method == 'POST':
        turno_id = request.form['turno_id']
        turno = Turno.query.get_or_404(turno_id)

        if turno.estado != 'disponible':
            flash('Ese turno ya fue reservado por otro usuario.', 'error')
            return redirect(url_for('turnos.agendar_turno'))

        turno.estado = 'ocupado'
        turno.dueno_id = current_user.id
        turno.mascota_id = None
        db.session.commit()
        flash('Turno agendado exitosamente!', 'success')
        return redirect(url_for('turnos.listar_turnos'))

    turnos_disponibles = Turno.query.filter(
        Turno.estado == 'disponible',
        Turno.fecha >= date.today()
    ).all()

    # Build calendar availability data (per date+veterinario)
    tres_meses = date.today() + timedelta(days=90)
    turnos_todos = Turno.query.filter(
        Turno.fecha >= date.today(),
        Turno.fecha <= tres_meses
    ).all()

    cal_data = {}
    for t in turnos_todos:
        key = f"{t.fecha.isoformat()}_{t.veterinario_id}"
        if key not in cal_data:
            cal_data[key] = {'disponible': 0, 'ocupado': 0, 'cancelado': 0}
        if t.estado in cal_data[key]:
            cal_data[key][t.estado] += 1

    calendar_data = {}
    for key, stats in cal_data.items():
        if stats['disponible'] > 0:
            calendar_data[key] = 'available'
        elif stats['ocupado'] > 0 or stats['cancelado'] > 0:
            calendar_data[key] = 'full'

    return render_template('turnos/agendar_turno.html',
                           turnos_disponibles=turnos_disponibles,
                           calendar_data=calendar_data)
  
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
            if fecha_hora_turno - fecha_hora_actual < timedelta(hours=24):
                flash('Solo podés cancelar turnos con al menos 24 horas de anticipación. Contactá a la clínica si necesitás cancelarlo antes.', 'error')
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
        
        redirect_url = 'turnos.listar_turnos'
        if current_user.rol == 'admin':
            redirect_url = 'turnos.admin_turnos'
        flash('Turno cancelado exitosamente!', 'success')
        return redirect(url_for(redirect_url))
        
    except Exception as e:
        db.session.rollback()
        flash(f' Error: {str(e)}', 'error')
        redirect_url = 'turnos.listar_turnos'
        if current_user.rol == 'admin':
            redirect_url = 'turnos.admin_turnos'
        return redirect(url_for(redirect_url))