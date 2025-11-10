"""
Script para inicializar la base de datos y crear usuarios de prueba
"""
from app import create_app, db
from app.models import Usuario, Rol, Itinerario, Etapa, Ciudad, Provincia, Aeropuerto, ParqueNacional, LugarInteres

def init_database():
    """Inicializa la base de datos y crea datos de prueba"""
    app = create_app()
    
    with app.app_context():
        # Eliminar todas las tablas existentes (¡CUIDADO en producción!)
        print("Eliminando tablas existentes...")
        db.drop_all()
        
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        
        # Crear roles
        print("Creando roles...")
        roles = [
            Rol(titulo='Administrador'),
            Rol(titulo='Planificador'),
            Rol(titulo='Visitante')
        ]
        for rol in roles:
            db.session.add(rol)
        db.session.commit()
        
        # Obtener los roles creados
        rol_admin = Rol.query.filter_by(titulo='Administrador').first()
        rol_planificador = Rol.query.filter_by(titulo='Planificador').first()
        rol_visitante = Rol.query.filter_by(titulo='Visitante').first()
        
        # Crear usuarios de prueba
        print("Creando usuarios de prueba...")
        usuarios = [
            Usuario(
                idRol=rol_admin.idRol,
                nombre='Admin',
                apellido='Sistema',
                email='admin@itinerar.com',
                fechaNacimiento='1990-01-01'
            ),
            Usuario(
                idRol=rol_planificador.idRol,
                nombre='Juan',
                apellido='Planificador',
                email='planificador@itinerar.com',
                fechaNacimiento='1992-05-15'
            ),
            Usuario(
                idRol=rol_visitante.idRol,
                nombre='María',
                apellido='Visitante',
                email='visitante@itinerar.com',
                fechaNacimiento='1995-08-20'
            )
        ]
        
        # Establecer contraseñas (por defecto: 'password123')
        for usuario in usuarios:
            usuario.set_password('password123')
            db.session.add(usuario)
        db.session.commit()
        
        # Crear algunas provincias y ciudades de ejemplo
        print("Creando provincias y ciudades de ejemplo...")
        provincias_data = [
            {'nombre': 'Buenos Aires', 'ciudades': ['Buenos Aires', 'La Plata', 'Mar del Plata']},
            {'nombre': 'Córdoba', 'ciudades': ['Córdoba', 'Villa Carlos Paz', 'La Falda']},
            {'nombre': 'Salta', 'ciudades': ['Salta', 'Cafayate', 'San Salvador de Jujuy']},
            {'nombre': 'Mendoza', 'ciudades': ['Mendoza', 'San Rafael', 'Malargüe']},
            {'nombre': 'Santa Cruz', 'ciudades': ['El Calafate', 'Río Gallegos', 'El Chaltén']}
        ]
        
        for prov_data in provincias_data:
            provincia = Provincia(nombre=prov_data['nombre'])
            db.session.add(provincia)
            db.session.flush()  # Para obtener el idProvincia
            
            for ciudad_nombre in prov_data['ciudades']:
                ciudad = Ciudad(idProvincia=provincia.idProvincia, nombre=ciudad_nombre)
                db.session.add(ciudad)
        
        db.session.commit()
        
        # Crear un itinerario de ejemplo
        print("Creando itinerario de ejemplo...")
        usuario_planificador = Usuario.query.filter_by(email='planificador@itinerar.com').first()
        ciudad_salta = Ciudad.query.filter_by(nombre='Salta').first()
        
        if usuario_planificador and ciudad_salta:
            itinerario = Itinerario(
                idUsuario=usuario_planificador.idUsuario,
                titulo='Norte Argentino en 10 Días',
                descripcion='Un recorrido por las maravillas del norte argentino',
                esPrivado=0,  # Público
                fechaInicio='2024-12-15',
                fechaFin='2024-12-25'
            )
            db.session.add(itinerario)
            db.session.flush()
            
            # Crear algunas etapas de ejemplo
            etapa1 = Etapa(
                idItinerario=itinerario.idItinerario,
                idCiudad=ciudad_salta.idCiudad,
                actividadDelDia='Llegada a Salta. Check-in en hotel y recorrido por el centro histórico.',
                fechaInicio='2024-12-15',
                notaPersonal='Llevar protector solar y sombrero'
            )
            db.session.add(etapa1)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Base de datos inicializada correctamente!")
        print("="*50)
        print("\nUsuarios de prueba creados:")
        print("  - Admin: admin@itinerar.com / password123")
        print("  - Planificador: planificador@itinerar.com / password123")
        print("  - Visitante: visitante@itinerar.com / password123")
        print("\n" + "="*50)

if __name__ == '__main__':
    init_database()

