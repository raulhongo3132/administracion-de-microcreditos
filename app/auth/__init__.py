from flask import Blueprint, render_template, current_app

# QUITA template_folder
bp = Blueprint('auth', __name__)

from app.auth import routes

# Handlers de error (mantener igual)
@bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.warning(f'Error 404: {request.url}')
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error(f'Error 500: {str(error)}')
    return render_template('errors/500.html'), 500