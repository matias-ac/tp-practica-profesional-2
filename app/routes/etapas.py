""" Rutas para la gestión de etapas dentro de un itinerario """
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Itinerario, Etapa, Ciudad, Provincia, LugarInteres
from app.utils import planificador_required
from datetime import datetime

bp = Blueprint('etapas', __name__, url_prefix='/itinerarios/<int:itinerario_id>/etapas')

def verificar_permiso_itinerario(itinerario_id):
    """Verifica que el usuario tenga permiso para modificar el itinerario"""
    itinerario = Itinerario.query.get_or_404(itinerario_id)
    puede_modificar = (itinerario.idUsuario == current_user.idUsuario) or current_user.es_administrador()
    return itinerario, puede_modificar

def _parse_date(value):
    """Convierte str/date/datetime a date; devuelve None si inválido."""
    if value is None:
        return None
    # Si ya es objeto date/datetime (no str)
    if hasattr(value, "isoformat") and not isinstance(value, str):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except Exception:
        return None

def validate_etapa_dates(itinerario, fecha_inicio_s, fecha_fin_s):
    """Valida formato, orden y rango (con itinerario). Devuelve lista de errores."""
    errores = []
    fi = _parse_date(fecha_inicio_s) if fecha_inicio_s else None
    ff = _parse_date(fecha_fin_s) if fecha_fin_s else None

    if fecha_inicio_s and fi is None:
        errores.append("Fecha de inicio inválida. Use formato AAAA-MM-DD.")
    if fecha_fin_s and ff is None:
        errores.append("Fecha de fin inválida. Use formato AAAA-MM-DD.")
    if fi and ff and fi > ff:
        errores.append("La fecha de inicio debe ser anterior o igual a la fecha de fin.")

    if itinerario is not None:
        itin_fi = _parse_date(getattr(itinerario, "fechaInicio", None))
        itin_ff = _parse_date(getattr(itinerario, "fechaFin", None))
        if itin_fi and fi and fi < itin_fi:
            errores.append(f"La fecha de inicio ({fi.isoformat()}) es anterior al inicio del itinerario ({itin_fi.isoformat()}).")
        if itin_ff and ff and ff > itin_ff:
            errores.append(f"La fecha de fin ({ff.isoformat()}) es posterior al fin del itinerario ({itin_ff.isoformat()}).")

    return errores

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
@planificador_required
def crear(itinerario_id):
    """Crea una nueva etapa en un itinerario"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)

    if not puede_modificar:
        # Responder JSON para AJAX o flash+redirect para formulario tradicional
        is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return jsonify({'success': False, 'message': 'No tienes permiso'}), 403
        flash('No tienes permiso para agregar etapas a este itinerario', 'error')
        return redirect(url_for('itinerarios.detalle', id=itinerario_id))

    provincias = Provincia.query.order_by(Provincia.nombre).all()

    if request.method == 'POST':
        actividad_dia = request.form.get('actividadDelDia', '').strip()
        id_ciudad = request.form.get('idCiudad', '').strip()
        id_lugar_interes = request.form.get('idLugarInteres', '').strip()
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        nota_personal = request.form.get('notaPersonal', '').strip()

        if not actividad_dia:
            flash('La actividad del día es obligatoria', 'error')
            return render_template('etapas/formulario.html',
                                   modo='crear',
                                   itinerario=itinerario,
                                   etapa=None,
                                   provincias=provincias,
                                   form=request.form)

        errores_fe = validate_etapa_dates(itinerario, fecha_inicio, fecha_fin)
        if errores_fe:
            for e in errores_fe:
                flash(e, 'error')
            return render_template('etapas/formulario.html',
                                   modo='crear',
                                   itinerario=itinerario,
                                   etapa=None,
                                   provincias=provincias,
                                   form=request.form)

        nueva_etapa = Etapa(
            idItinerario=itinerario_id,
            actividadDelDia=actividad_dia,
            idCiudad=int(id_ciudad) if id_ciudad and id_ciudad != '' else None,
            idLugarInteres=int(id_lugar_interes) if id_lugar_interes and id_lugar_interes != '' else None,
            fechaInicio=fecha_inicio if fecha_inicio else None,
            fechaFin=fecha_fin if fecha_fin else None,
            notaPersonal=nota_personal if nota_personal else None
        )

        # Asignar nuevo orden al final de la lista
        max_orden = db.session.query(db.func.max(Etapa.orden)).filter_by(idItinerario=itinerario_id).scalar()
        if max_orden is None:
            nueva_etapa.orden = 1
        else:
            nueva_etapa.orden = max_orden + 1

        try:
            db.session.add(nueva_etapa)
            db.session.commit()
            flash('Etapa creada exitosamente', 'success')
            return redirect(url_for('itinerarios.detalle', id=itinerario_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la etapa: {str(e)}', 'error')
            return render_template('etapas/formulario.html',
                                   modo='crear',
                                   itinerario=itinerario,
                                   etapa=None,
                                   provincias=provincias,
                                   form=request.form)

    # GET: mostrar formulario vacío
    return render_template('etapas/formulario.html',
                           modo='crear',
                           itinerario=itinerario,
                           etapa=None,
                           provincias=provincias)

@bp.route('/<int:etapa_id>/editar', methods=['GET', 'POST'])
@login_required
@planificador_required
def editar(itinerario_id, etapa_id):
    """Edita una etapa existente"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)

    if not puede_modificar:
        is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return jsonify({'success': False, 'message': 'No tienes permiso'}), 403
        flash('No tienes permiso para editar etapas de este itinerario', 'error')
        return redirect(url_for('itinerarios.detalle', id=itinerario_id))

    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()
    provincias = Provincia.query.order_by(Provincia.nombre).all()

    if request.method == 'POST':
        actividad_dia = request.form.get('actividadDelDia', '').strip()
        id_ciudad = request.form.get('idCiudad', '').strip()
        id_lugar_interes = request.form.get('idLugarInteres', '').strip()
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        nota_personal = request.form.get('notaPersonal', '').strip()

        if not actividad_dia:
            flash('La actividad del día es obligatoria', 'error')
            return render_template('etapas/formulario.html',
                                   modo='editar',
                                   itinerario=itinerario,
                                   etapa=etapa,
                                   provincias=provincias,
                                   form=request.form)

        errores_fe = validate_etapa_dates(itinerario, fecha_inicio, fecha_fin)
        if errores_fe:
            for e in errores_fe:
                flash(e, 'error')
            return render_template('etapas/formulario.html',
                                   modo='editar',
                                   itinerario=itinerario,
                                   etapa=etapa,
                                   provincias=provincias,
                                   form=request.form)

        etapa.actividadDelDia = actividad_dia
        etapa.idCiudad = int(id_ciudad) if id_ciudad and id_ciudad != '' else None
        etapa.idLugarInteres = int(id_lugar_interes) if id_lugar_interes and id_lugar_interes != '' else None
        etapa.fechaInicio = fecha_inicio if fecha_inicio else None
        etapa.fechaFin = fecha_fin if fecha_fin else None
        etapa.notaPersonal = nota_personal if nota_personal else None

        try:
            db.session.commit()
            flash('Etapa actualizada exitosamente', 'success')
            return redirect(url_for('itinerarios.detalle', id=itinerario_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la etapa: {str(e)}', 'error')
            return render_template('etapas/formulario.html',
                                   modo='editar',
                                   itinerario=itinerario,
                                   etapa=etapa,
                                   provincias=provincias,
                                   form=request.form)

    # GET: mostrar formulario con datos de la etapa
    return render_template('etapas/formulario.html',
                           modo='editar',
                           itinerario=itinerario,
                           etapa=etapa,
                           provincias=provincias)

@bp.route('/<int:etapa_id>/eliminar', methods=['POST'])
@login_required
@planificador_required
def eliminar(itinerario_id, etapa_id):
    """Elimina una etapa"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)

    if not puede_modificar:
        is_ajax = request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return jsonify({'success': False, 'message': 'No tienes permiso'}), 403
        flash('No tienes permiso para eliminar etapas de este itinerario', 'error')
        return redirect(url_for('itinerarios.detalle', id=itinerario_id))

    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()

    try:
        db.session.delete(etapa)
        db.session.commit()
        flash('Etapa eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la etapa: {str(e)}', 'error')

    return redirect(url_for('itinerarios.detalle', id=itinerario_id))

@bp.route('/<int:etapa_id>/subir', methods=['POST'])
@login_required
@planificador_required
def subir(itinerario_id, etapa_id):
    """Mueve una etapa hacia arriba (cambia su fecha para que aparezca antes)"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)

    if not puede_modificar:
        return jsonify({'success': False, 'message': 'No tienes permiso'}), 403

    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()

    # Encontrar la etapa anterior basada en el campo 'orden'
    etapa_anterior = Etapa.query.filter(
        Etapa.idItinerario == itinerario_id,
        Etapa.orden < etapa.orden
    ).order_by(Etapa.orden.desc()).first()

    if not etapa_anterior:
        return jsonify({'success': False, 'message': 'Ya es la primera etapa'}), 400

    try:
        # Intercambiar valores de orden
        orden_temp = etapa.orden
        etapa.orden = etapa_anterior.orden
        etapa_anterior.orden = orden_temp

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error del servidor: {str(e)}'}), 500

@bp.route('/<int:etapa_id>/bajar', methods=['POST'])
@login_required
@planificador_required
def bajar(itinerario_id, etapa_id):
    """Mueve una etapa hacia abajo (cambia su fecha para que aparezca después)"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)

    if not puede_modificar:
        return jsonify({'success': False, 'message': 'No tienes permiso'}), 403

    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()

    # Encontrar la etapa siguiente basada en el campo 'orden'
    etapa_siguiente = Etapa.query.filter(
        Etapa.idItinerario == itinerario_id,
        Etapa.orden > etapa.orden
    ).order_by(Etapa.orden.asc()).first()

    if not etapa_siguiente:
        return jsonify({'success': False, 'message': 'Ya es la última etapa'}), 400

    try:
        # Intercambiar valores de orden
        orden_temp = etapa.orden
        etapa.orden = etapa_siguiente.orden
        etapa_siguiente.orden = orden_temp

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error del servidor: {str(e)}'}), 500
    