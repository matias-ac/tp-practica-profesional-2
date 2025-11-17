from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Factory function para crear la aplicación Flask"""
    # Rutas de templates y static en la raíz del proyecto
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, instance_relative_config=False)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Configurar la URI de la base de datos de forma robusta
    if 'SQLALCHEMY_DATABASE_URI' not in os.environ:
        db_path = os.path.join(basedir, 'data.db')
        os.environ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Importar modelos (después de db)
    from app.models import Usuario
    
    # Configurar user_loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Usuario.query.get(int(user_id))
        except Exception:
            return None
    
    # Registrar blueprints
    from app.routes import main, itinerarios, etapas, auth, lugares, dashboard, errors 
    app.register_blueprint(main.bp)
    app.register_blueprint(itinerarios.bp)
    app.register_blueprint(etapas.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(lugares.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(errors.bp)

    # Registrar filtro de Jinja2 para fechas
    from app.utils import format_date
    app.jinja_env.filters['format_date'] = format_date

    # Registrar comandos CLI
    from app import commands
    commands.init_app(app)
    
    return app
