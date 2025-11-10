"""
Rutas para el panel de datos (dashboard) con gráficos
"""
import pandas as pd
import os
from flask import Blueprint, jsonify, request, render_template
from app import create_app

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def get_data_dir():
    """Obtiene la ruta del directorio de datos"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

@bp.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('dashboard/index.html')

@bp.route('/api/turismo-receptivo', methods=['GET'])
def turismo_receptivo():
    """Devuelve datos de turismo receptivo por mes para un año"""
    año = request.args.get('año', '2024', type=str)
    
    try:
        data_dir = get_data_dir()
        csv_path = os.path.join(data_dir, 'turismo_receptivo.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'Archivo de datos no encontrado'}), 404
        
        df = pd.read_csv(csv_path)
        
        # Filtrar por año
        df_año = df[df['año'] == int(año)]
        
        # Ordenar por mes
        df_año = df_año.sort_values('mes')
        
        # Formatear datos
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        datos = {
            'labels': [meses[int(m)-1] for m in df_año['mes']],
            'data': df_año['turistas'].tolist(),
            'año': año
        }
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/motivos-viaje', methods=['GET'])
def motivos_viaje():
    """Devuelve datos de motivos de viaje por categoría para un año"""
    año = request.args.get('año', '2024', type=str)
    
    try:
        data_dir = get_data_dir()
        csv_path = os.path.join(data_dir, 'motivos_viaje.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'Archivo de datos no encontrado'}), 404
        
        df = pd.read_csv(csv_path)
        
        # Filtrar por año
        df_año = df[df['año'] == int(año)]
        
        # Formatear datos
        datos = {
            'labels': df_año['categoria'].tolist(),
            'data': df_año['cantidad'].tolist(),
            'año': año
        }
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/rangos-edad', methods=['GET'])
def rangos_edad():
    """Devuelve datos de distribución por rangos de edad"""
    try:
        data_dir = get_data_dir()
        csv_path = os.path.join(data_dir, 'rangos_edad.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'Archivo de datos no encontrado'}), 404
        
        df = pd.read_csv(csv_path)
        
        # Formatear datos
        datos = {
            'labels': df['rango_edad'].tolist(),
            'data': df['cantidad'].tolist()
        }
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/años-disponibles', methods=['GET'])
def años_disponibles():
    """Devuelve lista de años disponibles en los datos"""
    try:
        data_dir = get_data_dir()
        csv_path = os.path.join(data_dir, 'turismo_receptivo.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'años': ['2024']})
        
        df = pd.read_csv(csv_path)
        años = sorted(df['año'].unique().tolist(), reverse=True)
        
        return jsonify({'años': años})
    except Exception as e:
        return jsonify({'años': ['2024']})



