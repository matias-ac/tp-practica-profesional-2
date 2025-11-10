"""
Utilidades y decoradores para la aplicación
"""
from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            from flask import request
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.es_administrador():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def planificador_required(f):
    """Decorador para requerir rol de planificador o administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            from flask import request
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.es_planificador():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

