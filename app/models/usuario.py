from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Rol(db.Model):
    """Modelo para los roles de usuario"""
    __tablename__ = 'rol'
    
    idRol = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relación con Usuario
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)
    
    def __repr__(self):
        return f'<Rol {self.titulo}>'


class Usuario(db.Model, UserMixin):
    """Modelo para los usuarios del sistema"""
    __tablename__ = 'usuario'
    
    idUsuario = db.Column(db.Integer, primary_key=True)
    idRol = db.Column(db.Integer, db.ForeignKey('rol.idRol'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)
    fechaNacimiento = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashPassword = db.Column(db.String(255), nullable=False)
    
    # Relación con Itinerario
    itinerarios = db.relationship('Itinerario', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def get_id(self):
        """Método requerido por Flask-Login"""
        return self.idUsuario
    
    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.hashPassword = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.hashPassword, password)
    
    def es_administrador(self):
        """Verifica si el usuario es administrador"""
        return self.rol.titulo == 'Administrador'
    
    def es_planificador(self):
        """Verifica si el usuario es planificador"""
        return self.rol.titulo == 'Planificador' or self.es_administrador()
    
    def es_visitante(self):
        """Verifica si el usuario es visitante"""
        return self.rol.titulo == 'Visitante'
    
    def __repr__(self):
        return f'<Usuario {self.email}>'



