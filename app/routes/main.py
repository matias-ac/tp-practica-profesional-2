"""
Rutas principales de la aplicación
"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Página de inicio"""
    return render_template('index.html')



