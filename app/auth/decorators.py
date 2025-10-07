from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def role_required(required_role):
    """
    Decorador para restringir el acceso según el rol del usuario.
    :param required_role: str, uno de 'admin', 'collector', 'customer'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                # Redirige a login si no está autenticado
                return redirect(url_for('auth.login'))
            
            user_role = getattr(current_user, 'role', None)
            if user_role != required_role:
                # Aborta con 401 si no tiene el rol correcto
                abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
