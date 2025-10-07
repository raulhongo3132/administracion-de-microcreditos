from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Extensiones globales
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app(settings_module):
    """Factory de Flask para crear la aplicación"""
    app = Flask(__name__, instance_relative_config=True)

    # Configuración principal
    app.config.from_object(settings_module)

    # Si quieres, puedes mantener la carga de config desde archivo
    # if app.config.get("TESTING", False):
    #     app.config.from_pyfile("config-testing.py", silent=True)
    # else:
    #     app.config.from_pyfile("config.py", silent=True)

    # Inicialización de extensiones
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # ruta de login

    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Puedes dejar comentado el resto de blueprints y errores
    # from .admin import admin_bp
    # app.register_blueprint(admin_bp)
    #
    # from .public import public_bp
    # app.register_blueprint(public_bp)
    #
    # register_error_handlers(app)

    @app.route("/")
    def index():
        """
        Página raíz: si está autenticado redirige según su rol,
        si no, redirige al login.
        """
        if current_user.is_authenticated:
            role = getattr(current_user, 'role', None)
            if role == 'admin':
                return redirect(url_for('admin.index'))
            if role == 'collector':
                return redirect(url_for('collectors.index'))
            if role == 'customer':
                return redirect(url_for('customers.index'))

        # Por defecto, si no está autenticado, ir al login
        return redirect(url_for('auth.login'))

    return app

# =========================================================
# Opcional: manejadores de errores (dejarlos comentados por ahora)
# =========================================================
# def register_error_handlers(app):
#     from flask import render_template
#     @app.errorhandler(500)
#     def base_error_handler(e):
#         return render_template('500.html'), 500
# 
#     @app.errorhandler(404)
#     def error_404_handler(e):
#         return render_template('404.html'), 404
#     
#     @app.errorhandler(401)
#     def error_401_handler(e):
#         return render_template('401.html'), 401
