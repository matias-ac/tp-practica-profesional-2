"""
Rutas para buscar lugares de interés
"""
from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import LugarInteres, Provincia

bp = Blueprint('lugares', __name__, url_prefix='/lugares')

@bp.route('/')
def index():
    """Página principal de lugares de interés"""
    # Obtener todas las provincias para el filtro
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    
    # Obtener todas las categorías disponibles
    categorias = db.session.query(LugarInteres.categoria).distinct().all()
    categorias_list = [cat[0] for cat in categorias if cat[0]]
    
    # Obtener lugares (con paginación opcional)
    lugares = LugarInteres.query.order_by(LugarInteres.nombre).limit(50).all()
    
    return render_template('lugares/index.html',
                         lugares=lugares,
                         provincias=provincias,
                         categorias=categorias_list)

@bp.route('/api/buscar', methods=['GET'])
def buscar():
    """Busca lugares de interés por nombre y/o provincia"""
    nombre = request.args.get('nombre', '').strip()
    provincia_id = request.args.get('provincia_id', '').strip()
    categoria = request.args.get('categoria', '').strip()
    
    query = LugarInteres.query
    
    # Filtrar por nombre (búsqueda parcial, case-insensitive)
    if nombre:
        query = query.filter(LugarInteres.nombre.ilike(f'%{nombre}%'))
    
    # Filtrar por provincia
    if provincia_id:
        try:
            query = query.filter(LugarInteres.idProvincia == int(provincia_id))
        except ValueError:
            pass
    
    # Filtrar por categoría
    if categoria:
        query = query.filter(LugarInteres.categoria == categoria)
    
    # Limitar resultados a 50
    lugares = query.limit(50).all()
    
    # Formatear resultados
    resultados = []
    for lugar in lugares:
        resultados.append({
            'id': lugar.idLugarInteres,
            'nombre': lugar.nombre,
            'categoria': lugar.categoria,
            'provincia': lugar.provincia.nombre if lugar.provincia else None,
            'ciudad': lugar.ciudad.nombre if lugar.ciudad else None,
            'enlace': lugar.enlaceFicha
        })
    
    return jsonify({'lugares': resultados})

@bp.route('/api/por-provincia/<int:provincia_id>', methods=['GET'])
def por_provincia(provincia_id):
    """Obtiene todos los lugares de interés de una provincia"""
    categoria = request.args.get('categoria', '').strip()
    
    query = LugarInteres.query.filter_by(idProvincia=provincia_id)
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    lugares = query.all()
    
    resultados = []
    for lugar in lugares:
        resultados.append({
            'id': lugar.idLugarInteres,
            'nombre': lugar.nombre,
            'categoria': lugar.categoria,
            'ciudad': lugar.ciudad.nombre if lugar.ciudad else None,
            'enlace': lugar.enlaceFicha
        })
    
    return jsonify({'lugares': resultados})

@bp.route('/api/categorias', methods=['GET'])
def categorias():
    """Obtiene todas las categorías disponibles"""
    categorias = db.session.query(LugarInteres.categoria).distinct().all()
    categorias_list = [cat[0] for cat in categorias if cat[0]]
    return jsonify({'categorias': categorias_list})

