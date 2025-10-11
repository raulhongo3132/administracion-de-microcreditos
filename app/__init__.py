from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = "auth.login"

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Inicializar extensiones
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar Blueprints
    from .auth import auth_bp
    from .admin import admin_bp
    from .collector import collector_bp
    from .client import client_bp
    from .loan import loan_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(collector_bp, url_prefix="/collector")
    app.register_blueprint(client_bp, url_prefix="/client")
    app.register_blueprint(loan_bp, url_prefix="/loan")

    # Definir la raíz **después** de registrar los Blueprints
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
