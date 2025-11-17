"""
Rutas para la gestión de itinerarios
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Itinerario, Usuario, Rol
from app.utils import planificador_required

bp = Blueprint('itinerarios', __name__, url_prefix='/itinerarios')

@bp.route('/')
def listar():
    """Lista todos los itinerarios públicos y los del usuario actual"""
    # Si el usuario está autenticado, mostrar sus itinerarios y los públicos
    if current_user.is_authenticated:
        # Itinerarios del usuario actual
        mis_itinerarios = Itinerario.query.filter_by(idUsuario=current_user.idUsuario).all()
        
        # Si es administrador, puede ver todos los itinerarios (públicos y privados)
        if current_user.es_administrador():
            # Todos los itinerarios de otros usuarios (públicos y privados)
            itinerarios_publicos = Itinerario.query.filter(
                Itinerario.idUsuario != current_user.idUsuario
            ).all()
        else:
            # Solo itinerarios públicos de otros usuarios
            itinerarios_publicos = Itinerario.query.filter(
                Itinerario.esPrivado == 0,
                Itinerario.idUsuario != current_user.idUsuario
            ).all()
        
        return render_template('itinerarios/listar.html', 
                             mis_itinerarios=mis_itinerarios,
                             itinerarios_publicos=itinerarios_publicos)
    else:
        # Solo mostrar itinerarios públicos
        itinerarios_publicos = Itinerario.query.filter_by(esPrivado=0).all()
        return render_template('itinerarios/listar.html',
                             mis_itinerarios=[],
                             itinerarios_publicos=itinerarios_publicos)

@bp.route('/mis-itinerarios')
@login_required
@planificador_required
def mis_itinerarios():
    """Lista solo los itinerarios del usuario actual"""
    itinerarios = Itinerario.query.filter_by(idUsuario=current_user.idUsuario).order_by(Itinerario.fechaInicio.desc()).all()
    return render_template('itinerarios/mis_itinerarios.html', itinerarios=itinerarios)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
@planificador_required
def crear():
    """Crea un nuevo itinerario"""
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        es_privado = request.form.get('esPrivado', '0')
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        
        # Validación de campos
        errores = []
        if not titulo:
            errores.append('El título es obligatorio.')
        elif len(titulo) < 3 or len(titulo) > 100:
            errores.append('El título debe tener entre 3 y 100 caracteres.')

        if not descripcion:
            errores.append('La descripción es obligatoria.')
        elif len(descripcion) < 10 or len(descripcion) > 500:
            errores.append('La descripción debe tener entre 10 y 500 caracteres.')

        if not fecha_inicio:
            errores.append('La fecha de inicio es obligatoria.')
        
        if not fecha_fin:
            errores.append('La fecha de fin es obligatoria.')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            errores.append('La fecha de inicio no puede ser posterior a la fecha de fin.')

        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('itinerarios/formulario.html', modo='crear', form=request.form)
        
        # Crear el itinerario
        nuevo_itinerario = Itinerario(
            idUsuario=current_user.idUsuario,
            titulo=titulo,
            descripcion=descripcion if descripcion else None,
            esPrivado=1 if es_privado == '1' else 0,
            fechaInicio=fecha_inicio if fecha_inicio else None,
            fechaFin=fecha_fin if fecha_fin else None
        )
        
        try:
            db.session.add(nuevo_itinerario)
            db.session.commit()
            flash('Itinerario creado exitosamente', 'success')
            return redirect(url_for('itinerarios.mis_itinerarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el itinerario: {str(e)}', 'error')
            return render_template('itinerarios/formulario.html', modo='crear')
    
    return render_template('itinerarios/formulario.html', modo='crear', itinerario=None)

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita un itinerario existente"""
    itinerario = Itinerario.query.get_or_404(id)
    
    # Verificar permisos: solo el dueño o administrador puede editar
    if itinerario.idUsuario != current_user.idUsuario and not current_user.es_administrador():
        flash('No tienes permiso para editar este itinerario', 'error')
        return redirect(url_for('itinerarios.listar'))
    
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        es_privado = request.form.get('esPrivado', '0')
        fecha_inicio = request.form.get('fechaInicio', '').strip()
        fecha_fin = request.form.get('fechaFin', '').strip()
        
        # Validación básica
        if not titulo:
            flash('El título es obligatorio', 'error')
            return render_template('itinerarios/formulario.html', modo='editar', itinerario=itinerario)
        
        # Actualizar el itinerario
        itinerario.titulo = titulo
        itinerario.descripcion = descripcion if descripcion else None
        itinerario.esPrivado = 1 if es_privado == '1' else 0
        itinerario.fechaInicio = fecha_inicio if fecha_inicio else None
        itinerario.fechaFin = fecha_fin if fecha_fin else None
        
        try:
            db.session.commit()
            flash('Itinerario actualizado exitosamente', 'success')
            return redirect(url_for('itinerarios.mis_itinerarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el itinerario: {str(e)}', 'error')
            return render_template('itinerarios/formulario.html', modo='editar', itinerario=itinerario)
    
    return render_template('itinerarios/formulario.html', modo='editar', itinerario=itinerario)

@bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Elimina un itinerario"""
    itinerario = Itinerario.query.get_or_404(id)
    
    # Verificar permisos: solo el dueño o administrador puede eliminar
    if itinerario.idUsuario != current_user.idUsuario and not current_user.es_administrador():
        flash('No tienes permiso para eliminar este itinerario', 'error')
        return redirect(url_for('itinerarios.listar'))
    
    try:
        titulo = itinerario.titulo
        db.session.delete(itinerario)
        db.session.commit()
        flash(f'Itinerario "{titulo}" eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el itinerario: {str(e)}', 'error')
    
    return redirect(url_for('itinerarios.mis_itinerarios'))

@bp.route('/<int:id>')
def detalle(id):
    """Muestra el detalle de un itinerario"""
    itinerario = Itinerario.query.get_or_404(id)
    
    # Verificar permisos: si es privado, solo el dueño o admin puede verlo
    if itinerario.esPrivado == 1:
        if not current_user.is_authenticated or (itinerario.idUsuario != current_user.idUsuario and not current_user.es_administrador()):
            flash('Este itinerario es privado', 'error')
            return redirect(url_for('itinerarios.listar'))
    
    # Obtener el usuario creador
    usuario_creador = Usuario.query.get(itinerario.idUsuario)
    
    # Ordenar etapas por fecha (las que no tienen fecha al final)
    etapas_ordenadas = sorted(itinerario.etapas, 
                               key=lambda e: (e.fechaInicio is None, e.fechaInicio or ''))
    
    return render_template('itinerarios/detalle.html', 
                         itinerario=itinerario,
                         usuario_creador=usuario_creador,
                         etapas_ordenadas=etapas_ordenadas)

