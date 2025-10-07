from os.path import abspath, dirname

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# Clave secreta para sesiones, cookies, CSRF, etc.
SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Configuración de SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Entornos posibles
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

'''
# Configuración opcional de email (para logs o recuperación de contraseña)
MAIL_SERVER = 'tu servidor smtp'
MAIL_PORT = 587
MAIL_USERNAME = 'tu correo'
MAIL_PASSWORD = 'tu contraseña'
DONT_REPLY_FROM_EMAIL = 'dirección from'
ADMINS = ('juanjo@j2logo.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False
'''
