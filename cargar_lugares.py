"""
Script para cargar lugares de interés desde archivos CSV a la base de datos
"""
import pandas as pd
import os
from app import create_app, db
from app.models import Provincia, Ciudad, LugarInteres

def cargar_lugares_desde_csv():
    """Carga lugares de interés desde archivos CSV en la carpeta data/"""
    app = create_app()
    
    with app.app_context():
        # Ruta a la carpeta de datos
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        # Verificar que existe la carpeta
        if not os.path.exists(data_dir):
            print(f"Creando carpeta {data_dir}...")
            os.makedirs(data_dir)
            print("Carpeta creada. Por favor, coloca tus archivos CSV allí.")
            return
        
        # Contador de lugares cargados
        lugares_cargados = 0
        
        # 1. Cargar Parques Nacionales
        parques_file = os.path.join(data_dir, 'parques_nacionales.csv')
        if os.path.exists(parques_file):
            print(f"Cargando {parques_file}...")
            try:
                df = pd.read_csv(parques_file)
                print(f"  Columnas encontradas: {list(df.columns)}")
                
                for _, row in df.iterrows():
                    nombre = str(row.get('nombre', '')).strip()
                    provincia_nombre = str(row.get('provincia', '')).strip()
                    
                    if not nombre or nombre == 'nan':
                        continue
                    
                    # Buscar o crear provincia
                    provincia = Provincia.query.filter_by(nombre=provincia_nombre).first()
                    if not provincia and provincia_nombre:
                        provincia = Provincia(nombre=provincia_nombre)
                        db.session.add(provincia)
                        db.session.flush()
                    
                    # Verificar si ya existe
                    lugar_existente = LugarInteres.query.filter_by(
                        nombre=nombre,
                        categoria='Parque Nacional'
                    ).first()
                    
                    if not lugar_existente:
                        lugar = LugarInteres(
                            nombre=nombre,
                            categoria='Parque Nacional',
                            idProvincia=provincia.idProvincia if provincia else None,
                            fuente=row.get('fuente', 'datos.gob.ar'),
                            identificadorExterno=str(row.get('id', '')),
                            enlaceFicha=row.get('enlace', '')
                        )
                        db.session.add(lugar)
                        lugares_cargados += 1
                
                db.session.commit()
                print(f"  ✓ Parques Nacionales cargados: {lugares_cargados}")
            except Exception as e:
                db.session.rollback()
                print(f"  ✗ Error al cargar parques nacionales: {e}")
        else:
            print(f"  ⚠ Archivo no encontrado: {parques_file}")
        
        # 2. Cargar Alojamientos
        alojamientos_file = os.path.join(data_dir, 'alojamientos.csv')
        if os.path.exists(alojamientos_file):
            print(f"\nCargando {alojamientos_file}...")
            try:
                df = pd.read_csv(alojamientos_file)
                print(f"  Columnas encontradas: {list(df.columns)}")
                
                lugares_aloj = 0
                for _, row in df.iterrows():
                    nombre = str(row.get('nombre', '')).strip()
                    provincia_nombre = str(row.get('provincia', '')).strip()
                    ciudad_nombre = str(row.get('ciudad', '')).strip()
                    
                    if not nombre or nombre == 'nan':
                        continue
                    
                    # Buscar o crear provincia
                    provincia = None
                    if provincia_nombre:
                        provincia = Provincia.query.filter_by(nombre=provincia_nombre).first()
                        if not provincia:
                            provincia = Provincia(nombre=provincia_nombre)
                            db.session.add(provincia)
                            db.session.flush()
                    
                    # Buscar o crear ciudad
                    ciudad = None
                    if ciudad_nombre and provincia:
                        ciudad = Ciudad.query.filter_by(
                            nombre=ciudad_nombre,
                            idProvincia=provincia.idProvincia
                        ).first()
                        if not ciudad:
                            ciudad = Ciudad(nombre=ciudad_nombre, idProvincia=provincia.idProvincia)
                            db.session.add(ciudad)
                            db.session.flush()
                    
                    # Verificar si ya existe
                    lugar_existente = LugarInteres.query.filter_by(
                        nombre=nombre,
                        categoria='Alojamiento'
                    ).first()
                    
                    if not lugar_existente:
                        lugar = LugarInteres(
                            nombre=nombre,
                            categoria='Alojamiento',
                            idProvincia=provincia.idProvincia if provincia else None,
                            idCiudad=ciudad.idCiudad if ciudad else None,
                            fuente=row.get('fuente', 'datos.gob.ar'),
                            identificadorExterno=str(row.get('id', '')),
                            enlaceFicha=row.get('enlace', '')
                        )
                        db.session.add(lugar)
                        lugares_aloj += 1
                
                db.session.commit()
                print(f"  ✓ Alojamientos cargados: {lugares_aloj}")
                lugares_cargados += lugares_aloj
            except Exception as e:
                db.session.rollback()
                print(f"  ✗ Error al cargar alojamientos: {e}")
        else:
            print(f"  ⚠ Archivo no encontrado: {alojamientos_file}")
        
        # 3. Cargar Fiestas/Eventos
        fiestas_file = os.path.join(data_dir, 'fiestas_eventos.csv')
        if os.path.exists(fiestas_file):
            print(f"\nCargando {fiestas_file}...")
            try:
                df = pd.read_csv(fiestas_file)
                print(f"  Columnas encontradas: {list(df.columns)}")
                
                lugares_fiestas = 0
                for _, row in df.iterrows():
                    nombre = str(row.get('nombre', '')).strip()
                    provincia_nombre = str(row.get('provincia', '')).strip()
                    ciudad_nombre = str(row.get('ciudad', '')).strip()
                    
                    if not nombre or nombre == 'nan':
                        continue
                    
                    # Buscar o crear provincia
                    provincia = None
                    if provincia_nombre:
                        provincia = Provincia.query.filter_by(nombre=provincia_nombre).first()
                        if not provincia:
                            provincia = Provincia(nombre=provincia_nombre)
                            db.session.add(provincia)
                            db.session.flush()
                    
                    # Buscar o crear ciudad
                    ciudad = None
                    if ciudad_nombre and provincia:
                        ciudad = Ciudad.query.filter_by(
                            nombre=ciudad_nombre,
                            idProvincia=provincia.idProvincia
                        ).first()
                        if not ciudad:
                            ciudad = Ciudad(nombre=ciudad_nombre, idProvincia=provincia.idProvincia)
                            db.session.add(ciudad)
                            db.session.flush()
                    
                    # Verificar si ya existe
                    lugar_existente = LugarInteres.query.filter_by(
                        nombre=nombre,
                        categoria='Fiesta/Evento'
                    ).first()
                    
                    if not lugar_existente:
                        lugar = LugarInteres(
                            nombre=nombre,
                            categoria='Fiesta/Evento',
                            idProvincia=provincia.idProvincia if provincia else None,
                            idCiudad=ciudad.idCiudad if ciudad else None,
                            fuente=row.get('fuente', 'datos.gob.ar'),
                            identificadorExterno=str(row.get('id', '')),
                            enlaceFicha=row.get('enlace', '')
                        )
                        db.session.add(lugar)
                        lugares_fiestas += 1
                
                db.session.commit()
                print(f"  ✓ Fiestas/Eventos cargados: {lugares_fiestas}")
                lugares_cargados += lugares_fiestas
            except Exception as e:
                db.session.rollback()
                print(f"  ✗ Error al cargar fiestas/eventos: {e}")
        else:
            print(f"  ⚠ Archivo no encontrado: {fiestas_file}")
        
        print("\n" + "="*50)
        print(f"Total de lugares de interés cargados: {lugares_cargados}")
        print("="*50)

if __name__ == '__main__':
    cargar_lugares_desde_csv()



