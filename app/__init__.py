from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # User loader para Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Importar blueprints DESPUÉS de inicializar db para evitar importaciones circulares
    with app.app_context():
        from app.auth.routes import auth_bp
        from app.admin.routes import admin_bp
        from app.collectors.routes import collectors_bp
        # Si no tienes loans_bp, elimina esta línea
        # from app.loans.routes import loans_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(collectors_bp)
        # Si no tienes loans_bp, elimina esta línea
        # app.register_blueprint(loans_bp)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            # Redirigir según el rol del usuario
            if current_user.is_admin:
                return redirect(url_for('admin.inicio'))
            elif current_user.is_collector:
                return redirect(url_for('collectors.inicio'))
            # Eliminado el redirect para 'customer' ya que ahora son entidades separadas
        else:
            return redirect(url_for('auth.login'))
    
    # Manejo de errores personalizado
    @app.errorhandler(404)
    def not_found_error(error):
        return redirect(url_for('auth.login'))
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return redirect(url_for('auth.login'))
    
    return app