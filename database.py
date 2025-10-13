from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Muestra las consultas SQL en consola
    
    # Inicializar la base de datos con la app
    db.init_app(app)
    
    # Crear las tablas
    with app.app_context():
        db.create_all()