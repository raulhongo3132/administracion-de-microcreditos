import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Base de datos (preparación para futuras lecciones)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'  # Más detallado en desarrollo
    
    # SQLite para desarrollo
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL', 
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    LOG_LEVEL = 'DEBUG'
    
    # Base de datos en memoria para tests
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL', 
        'sqlite:///:memory:'
    )

class ProductionConfig(Config):
    """Configuración para producción"""
    LOG_LEVEL = 'WARNING'  # Solo errores en producción
    
    # PostgreSQL o MySQL para producción
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )

# Diccionario para fácil acceso a las configuraciones
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
