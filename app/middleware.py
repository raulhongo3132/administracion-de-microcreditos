import time
from flask import request, current_app

def log_requests(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            current_app.logger.info(
                f'{request.remote_addr} - "{request.method} {request.path} '
                f'{request.environ.get("SERVER_PROTOCOL")}" {response.status_code} '
                f'- {duration:.3f}s'
            )
        return response