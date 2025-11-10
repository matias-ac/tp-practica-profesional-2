from app import db
from datetime import datetime

class Itinerario(db.Model):
    """Modelo para los itinerarios de viaje"""
    __tablename__ = 'itinerario'
    
    idItinerario = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    esPrivado = db.Column(db.Integer, default=0, nullable=False)  # 0 = público, 1 = privado
    fechaInicio = db.Column(db.String(50), nullable=True)
    fechaFin = db.Column(db.String(50), nullable=True)
    
    # Relación con Etapa
    etapas = db.relationship('Etapa', backref='itinerario', lazy=True, cascade='all, delete-orphan', order_by='Etapa.fechaInicio')
    
    def es_publico(self):
        """Verifica si el itinerario es público"""
        return self.esPrivado == 0
    
    def __repr__(self):
        return f'<Itinerario {self.titulo}>'


class Etapa(db.Model):
    """Modelo para las etapas (días) de un itinerario"""
    __tablename__ = 'etapa'
    
    idEtapa = db.Column(db.Integer, primary_key=True)
    idItinerario = db.Column(db.Integer, db.ForeignKey('itinerario.idItinerario'), nullable=False)
    idCiudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'), nullable=True)
    idLugarInteres = db.Column(db.Integer, db.ForeignKey('lugar_interes.idLugarInteres'), nullable=True)
    actividadDelDia = db.Column(db.Text, nullable=False)
    fechaInicio = db.Column(db.String(50), nullable=True)
    fechaFin = db.Column(db.String(50), nullable=True)
    notaPersonal = db.Column(db.Text, nullable=True)
    
    # Relación con LugarInteres
    lugar_interes = db.relationship('LugarInteres', backref='etapas', lazy=True)
    
    def __repr__(self):
        return f'<Etapa {self.idEtapa} - {self.actividadDelDia[:30]}>'

