"""
Rutas para la gestión de etapas dentro de un itinerario
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Itinerario, Etapa, Ciudad, Provincia, LugarInteres
from app.utils import planificador_required

bp = Blueprint('etapas', __name__, url_prefix='/itinerarios/<int:itinerario_id>/etapas')

def verificar_permiso_itinerario(itinerario_id):
    """Verifica que el usuario tenga permiso para modificar el itinerario"""
    itinerario = Itinerario.query.get_or_404(itinerario_id)
    puede_modificar = (itinerario.idUsuario == current_user.idUsuario) or current_user.es_administrador()
    return itinerario, puede_modificar

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
@planificador_required
def crear(itinerario_id):
    """Crea una nueva etapa en un itinerario"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)
    
    if not puede_modificar:
        flash('No tienes permiso para agregar etapas a este itinerario', 'error')
        return redirect(url_for('itinerarios.detalle', id=itinerario_id))
    
    # Obtener provincias y ciudades para el formulario
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    
    if request.method == 'POST':
        actividad_dia = request.form.get('actividadDelDia', '').strip()
        id_ciudad = request.form.get('idCiudad', '').strip()
        id_lugar_interes = request.form.get('idLugarInteres', '').strip()
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        nota_personal = request.form.get('notaPersonal', '').strip()
        
        # Validación básica
        if not actividad_dia:
            flash('La actividad del día es obligatoria', 'error')
            return render_template('etapas/formulario.html', 
                                 modo='crear',
                                 itinerario=itinerario,
                                 etapa=None,
                                 provincias=provincias)
        
        # Crear la etapa
        nueva_etapa = Etapa(
            idItinerario=itinerario_id,
            actividadDelDia=actividad_dia,
            idCiudad=int(id_ciudad) if id_ciudad and id_ciudad != '' else None,
            idLugarInteres=int(id_lugar_interes) if id_lugar_interes and id_lugar_interes != '' else None,
            fechaInicio=fecha_inicio if fecha_inicio else None,
            fechaFin=fecha_fin if fecha_fin else None,
            notaPersonal=nota_personal if nota_personal else None
        )
        
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
                                 provincias=provincias)
    
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
        flash('No tienes permiso para editar etapas de este itinerario', 'error')
        return redirect(url_for('itinerarios.detalle', id=itinerario_id))
    
    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    
    if request.method == 'POST':
        actividad_dia = request.form.get('actividadDelDia', '').strip()
        id_ciudad = request.form.get('idCiudad', '').strip()
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        nota_personal = request.form.get('notaPersonal', '').strip()
        
        # Validación básica
        if not actividad_dia:
            flash('La actividad del día es obligatoria', 'error')
            return render_template('etapas/formulario.html',
                                 modo='editar',
                                 itinerario=itinerario,
                                 etapa=etapa,
                                 provincias=provincias)
        
        # Actualizar la etapa
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
                                 provincias=provincias)
    
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
    
    # Obtener todas las etapas ordenadas por fecha (las None al final)
    todas_etapas = Etapa.query.filter_by(idItinerario=itinerario_id).all()
    etapas_ordenadas = sorted(todas_etapas, key=lambda e: (e.fechaInicio is None, e.fechaInicio or ''))
    
    try:
        indice_actual = etapas_ordenadas.index(etapa)
        if indice_actual > 0:
            # Intercambiar fechas con la etapa anterior
            etapa_anterior = etapas_ordenadas[indice_actual - 1]
            fecha_temp = etapa.fechaInicio
            etapa.fechaInicio = etapa_anterior.fechaInicio
            etapa_anterior.fechaInicio = fecha_temp
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Ya es la primera etapa'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/<int:etapa_id>/bajar', methods=['POST'])
@login_required
@planificador_required
def bajar(itinerario_id, etapa_id):
    """Mueve una etapa hacia abajo (cambia su fecha para que aparezca después)"""
    itinerario, puede_modificar = verificar_permiso_itinerario(itinerario_id)
    
    if not puede_modificar:
        return jsonify({'success': False, 'message': 'No tienes permiso'}), 403
    
    etapa = Etapa.query.filter_by(idEtapa=etapa_id, idItinerario=itinerario_id).first_or_404()
    
    # Obtener todas las etapas ordenadas por fecha (las None al final)
    todas_etapas = Etapa.query.filter_by(idItinerario=itinerario_id).all()
    etapas_ordenadas = sorted(todas_etapas, key=lambda e: (e.fechaInicio is None, e.fechaInicio or ''))
    
    try:
        indice_actual = etapas_ordenadas.index(etapa)
        if indice_actual < len(etapas_ordenadas) - 1:
            # Intercambiar fechas con la etapa siguiente
            etapa_siguiente = etapas_ordenadas[indice_actual + 1]
            fecha_temp = etapa.fechaInicio
            etapa.fechaInicio = etapa_siguiente.fechaInicio
            etapa_siguiente.fechaInicio = fecha_temp
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Ya es la última etapa'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

