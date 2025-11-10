"""
Rutas para autenticación (login, logout)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Usuario

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



