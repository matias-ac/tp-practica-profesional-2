from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Factory function para crear la aplicación Flask"""
    # Especificar la ruta de templates y static en la raíz del proyecto
    import os
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///itinerar.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Importar modelos (debe hacerse después de crear db)
    from app.models import Usuario, Rol, Itinerario, Etapa, Ciudad, Provincia, Aeropuerto, ParqueNacional
    
    # Configurar user_loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes import main, itinerarios, etapas, auth, lugares, dashboard, errors
    app.register_blueprint(main.bp)
    app.register_blueprint(itinerarios.bp)
    app.register_blueprint(etapas.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(lugares.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(errors.bp)
    
    return app

