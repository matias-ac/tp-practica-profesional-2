"""
Script para verificar que la instalación esté correcta
"""
import sys
import os

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 o superior es requerido")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    dependencias = [
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'pandas',
        'dotenv'
    ]
    
    faltantes = []
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            faltantes.append(dep)
    
    if faltantes:
        print(f"\n⚠️  Faltan dependencias. Ejecuta: pip install -r requirements.txt")
        return False
    return True

def verificar_estructura():
    """Verifica que la estructura de carpetas esté correcta"""
    carpetas_requeridas = [
        'app',
        'app/models',
        'app/routes',
        'templates',
        'static',
        'data',
        'instance'
    ]
    
    faltantes = []
    for carpeta in carpetas_requeridas:
        if os.path.exists(carpeta):
            print(f"✅ {carpeta}/")
        else:
            print(f"❌ {carpeta}/ - NO EXISTE")
            faltantes.append(carpeta)
    
    if faltantes:
        print(f"\n⚠️  Faltan carpetas. Revisa la estructura del proyecto.")
        return False
    return True

def verificar_archivos():
    """Verifica que los archivos principales existan"""
    archivos_requeridos = [
        'app.py',
        'init_db.py',
        'requirements.txt',
        'README.md',
        'app/__init__.py',
        'app/models/__init__.py',
        'app/models/usuario.py',
        'app/models/itinerario.py',
        'app/models/lugares.py'
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO EXISTE")
            faltantes.append(archivo)
    
    if faltantes:
        print(f"\n⚠️  Faltan archivos. Revisa la estructura del proyecto.")
        return False
    return True

def main():
    print("="*60)
    print("VERIFICACIÓN DE INSTALACIÓN - Mi Hoja de Ruta")
    print("="*60)
    print()
    
    print("1. Verificando Python...")
    ok_python = verificar_python()
    print()
    
    print("2. Verificando dependencias...")
    ok_deps = verificar_dependencias()
    print()
    
    print("3. Verificando estructura de carpetas...")
    ok_estructura = verificar_estructura()
    print()
    
    print("4. Verificando archivos principales...")
    ok_archivos = verificar_archivos()
    print()
    
    print("="*60)
    if ok_python and ok_deps and ok_estructura and ok_archivos:
        print("✅ ¡Todo está correcto! Puedes continuar con:")
        print("   1. python init_db.py  (inicializar base de datos)")
        print("   2. python app.py      (ejecutar la aplicación)")
    else:
        print("⚠️  Hay problemas que deben resolverse antes de continuar.")
    print("="*60)

if __name__ == '__main__':
    main()



