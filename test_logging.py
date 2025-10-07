import logging
from logging.handlers import RotatingFileHandler
import os

# Crear directorio logs si no existe
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configurar logger de prueba
logger = logging.getLogger('test_logger')
logger.setLevel(logging.INFO)

# File handler
file_handler = RotatingFileHandler('logs/test.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

logger.addHandler(file_handler)

# Probar escritura
logger.info("ESTE ES UN MENSAJE DE PRUEBA")
print("✅ Mensaje de prueba escrito en logs/test.log")

# Verificar si el archivo se creó
if os.path.exists('logs/test.log'):
    print("✅ Archivo logs/test.log creado exitosamente")
    with open('logs/test.log', 'r') as f:
        content = f.read()
        print(f"📄 Contenido: {content}")
else:
    print("❌ Archivo logs/test.log NO se creó")