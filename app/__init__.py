import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Cargar configuración según el entorno
    app.config.from_object(config[config_name])
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar middleware de logging
    from app.middleware import log_requests
    log_requests(app)
    
    # Registrar blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Log de inicio de aplicación
    app.logger.info('Aplicación Flask iniciada')
    
    return app

def setup_logging(app):
    """Configura el sistema de logging"""
    
    print("🎯 INICIANDO CONFIGURACIÓN DE LOGGING...")
    
    # Eliminar handlers por defecto
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # Configurar nivel de log (ESTA LÍNEA FALTABA)
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    app.logger.setLevel(log_level)
    
    print(f"📊 Nivel de log configurado: {app.config['LOG_LEVEL']}")
    
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.mkdir('logs')
        print("✅ Directorio logs creado")
    else:
        print("✅ Directorio logs ya existe")
    
    # Handler para archivo de log
    log_file_path = 'logs/app.log'
    print(f"📄 Intentando crear archivo: {log_file_path}")
    
    try:
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10240,  # 10KB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(log_level)
        
        print("✅ File handler configurado correctamente")
        
    except Exception as e:
        print(f"❌ Error configurando file handler: {e}")
        # Usar solo console handler como fallback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        app.logger.addHandler(console_handler)
        print("✅ Usando solo console handler como fallback")
        return

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(log_level)
    
    # Agregar handlers al logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    print("✅ Sistema de logging completamente configurado")