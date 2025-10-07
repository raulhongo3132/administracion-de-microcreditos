from flask import render_template, abort, current_app
from app.main import bp

@bp.route('/')
def index():
    current_app.logger.info('Página de inicio accedida')
    return render_template('index.html', title='Inicio')  # ← nombre simple

@bp.route('/about')
def about():
    current_app.logger.info('Página "Acerca de" accedida')
    return render_template('about.html', title='Acerca de')  # ← nombre simple

# ... resto del código igual

@bp.route('/test-404')
def test_404():
    current_app.logger.warning('Error 404 generado intencionalmente')
    abort(404)

@bp.route('/test-500')
def test_500():
    current_app.logger.error('Error 500 generado intencionalmente')
    raise Exception("Este es un error de prueba para logging!")

@bp.route('/test-log')
def test_log():
    current_app.logger.debug('Mensaje DEBUG - información detallada')
    current_app.logger.info('Mensaje INFO - operación normal')
    current_app.logger.warning('Mensaje WARNING - algo inusual')
    current_app.logger.error('Mensaje ERROR - problema serio')
    
    return "Logs de prueba generados. Revisa la consola y archivo de logs."