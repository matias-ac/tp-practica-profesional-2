import click
from flask.cli import with_appcontext
from app import db
from app.models import Itinerario, Etapa

@click.command('backfill-orden')
@with_appcontext
def backfill_orden_command():
    """Asigna valores de orden a etapas existentes que no lo tienen."""
    itinerarios = Itinerario.query.all()
    total_actualizadas = 0
    
    print("Iniciando actualización de orden de etapas...")

    for itinerario in itinerarios:
        # Obtener el orden máximo actual para este itinerario (si lo hay)
        max_orden = db.session.query(db.func.max(Etapa.orden)).filter_by(idItinerario=itinerario.idItinerario).scalar() or 0
        
        # Obtener etapas sin orden, ordenadas por la lógica antigua (fecha, luego ID)
        etapas_a_ordenar = db.session.query(Etapa).filter(
            Etapa.idItinerario == itinerario.idItinerario,
            Etapa.orden.is_(None)
        ).order_by(Etapa.fechaInicio.asc().nullslast(), Etapa.idEtapa.asc()).all()
        
        if not etapas_a_ordenar:
            continue

        print(f"  -> Actualizando {len(etapas_a_ordenar)} etapas para el itinerario '{itinerario.titulo}' (ID: {itinerario.idItinerario})...")
        
        for etapa in etapas_a_ordenar:
            max_orden += 1
            etapa.orden = max_orden
            total_actualizadas += 1
            
    if total_actualizadas > 0:
        try:
            db.session.commit()
            print(f"\n¡Éxito! Se actualizaron {total_actualizadas} etapas.")
        except Exception as e:
            db.session.rollback()
            print(f"\nError al guardar los cambios: {e}")
    else:
        print("\nNo se encontraron etapas para actualizar.")

def init_app(app):
    """Registra los comandos en la aplicación."""
    app.cli.add_command(backfill_orden_command)

