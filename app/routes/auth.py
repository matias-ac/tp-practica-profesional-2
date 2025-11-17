"""
Rutas para autenticación (login, logout)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Rol

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicia sesión de un usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Por favor, completa todos los campos', 'error')
            return render_template('auth/login.html')
        
        # Buscar usuario por email
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario, remember=True)
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            
            # Redirigir según el rol
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif usuario.es_administrador():
                return redirect(url_for('itinerarios.listar'))
            elif usuario.es_planificador():
                return redirect(url_for('itinerarios.mis_itinerarios'))
            else:
                return redirect(url_for('itinerarios.listar'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario"""
    nombre_usuario = current_user.nombre
    logout_user()
    flash(f'Hasta luego, {nombre_usuario}!', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registra un nuevo usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validación de campos
        if not email or not password or not nombre or not confirm_password:
            flash('Por favor, completa todos los campos obligatorios.', 'warning')
            return render_template('auth/register.html', form=request.form)

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html', form=request.form)

        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado. Por favor, inicia sesión.', 'error')
            return redirect(url_for('auth.login'))

        # Asignar rol por defecto "Planificador"
        rol_planificador = Rol.query.filter_by(titulo='Planificador').first()
        if not rol_planificador:
            flash('Error interno: No se encontró el rol de planificador. Contacta al administrador.', 'danger')
            return render_template('auth/register.html', form=request.form)

        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            email=email,
            nombre=nombre,
            apellido=apellido,
            idRol=rol_planificador.idRol
        )
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """Muestra y actualiza el perfil del usuario."""
    if request.method == 'POST':
        form_name = request.form.get('form_name')

        if form_name == 'update_profile':
            # Lógica para actualizar datos personales
            nombre = request.form.get('nombre', '').strip()
            apellido = request.form.get('apellido', '').strip()
            email = request.form.get('email', '').strip().lower()

            if not nombre or not email:
                flash('Nombre y Email son campos obligatorios.', 'warning')
                return redirect(url_for('auth.perfil'))

            # Verificar si el email ha cambiado y si ya está en uso
            if email != current_user.email and Usuario.query.filter_by(email=email).first():
                flash('El nuevo email ya está registrado por otro usuario.', 'error')
                return redirect(url_for('auth.perfil'))

            current_user.nombre = nombre
            current_user.apellido = apellido
            current_user.email = email
            db.session.commit()
            flash('Tus datos han sido actualizados correctamente.', 'success')

        elif form_name == 'change_password':
            # Lógica para cambiar la contraseña
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')

            if not current_password or not new_password or not confirm_new_password:
                flash('Todos los campos de contraseña son obligatorios.', 'warning')
                return redirect(url_for('auth.perfil'))

            if not current_user.check_password(current_password):
                flash('La contraseña actual es incorrecta.', 'error')
                return redirect(url_for('auth.perfil'))

            if new_password != confirm_new_password:
                flash('Las nuevas contraseñas no coinciden.', 'error')
                return redirect(url_for('auth.perfil'))

            current_user.set_password(new_password)
            db.session.commit()
            flash('Contraseña actualizada correctamente.', 'success')
        
        return redirect(url_for('auth.perfil'))

    return render_template('auth/perfil.html')
