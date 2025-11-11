from app import db

class Provincia(db.Model):
    """Modelo para las provincias de Argentina"""
    __tablename__ = 'provincia'
    
    idProvincia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relaciones
    ciudades = db.relationship('Ciudad', backref='provincia', lazy=True, cascade='all, delete-orphan')
    parques_nacionales = db.relationship('ParqueNacional', backref='provincia', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Provincia {self.nombre}>'


class Ciudad(db.Model):
    """Modelo para las ciudades de Argentina"""
    __tablename__ = 'ciudad'
    
    idCiudad = db.Column(db.Integer, primary_key=True)
    idProvincia = db.Column(db.Integer, db.ForeignKey('provincia.idProvincia'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    aeropuertos = db.relationship('Aeropuerto', backref='ciudad', lazy=True, cascade='all, delete-orphan')
    etapas = db.relationship('Etapa', backref='ciudad', lazy=True)
    
    def __repr__(self):
        return f'<Ciudad {self.nombre}>'


class Aeropuerto(db.Model):
    """Modelo para los aeropuertos"""
    __tablename__ = 'aeropuerto'
    
    idAeropuerto = db.Column(db.Integer, primary_key=True)
    idCiudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<Aeropuerto {self.nombre}>'


class ParqueNacional(db.Model):
    """Modelo para los parques nacionales"""
    __tablename__ = 'parque_nacional'  # Nota: en el ERD aparece como 'ParqueNacional' pero SQLAlchemy usa snake_case
    
    idParqueNacional = db.Column(db.Integer, primary_key=True)
    idProvincia = db.Column(db.Integer, db.ForeignKey('provincia.idProvincia'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<ParqueNacional {self.nombre}>'


class LugarInteres(db.Model):
    """Modelo genérico para lugares de interés (Parques Nacionales, Alojamientos, Fiestas, etc.)"""
    __tablename__ = 'lugar_interes'
    
    idLugarInteres = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)  # 'Parque Nacional', 'Alojamiento', 'Fiesta/Evento', etc.
    idProvincia = db.Column(db.Integer, db.ForeignKey('provincia.idProvincia'), nullable=True)
    idCiudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'), nullable=True)
    fuente = db.Column(db.String(200), nullable=True)  # Ej: 'datos.gob.ar'
    identificadorExterno = db.Column(db.String(100), nullable=True)  # ID en el dataset original
    enlaceFicha = db.Column(db.String(500), nullable=True)  # URL a la ficha del lugar
    
    # Relaciones
    provincia = db.relationship('Provincia', backref='lugares_interes', lazy=True)
    ciudad = db.relationship('Ciudad', backref='lugares_interes', lazy=True)
    
    def __repr__(self):
        return f'<LugarInteres {self.nombre} ({self.categoria})>'

