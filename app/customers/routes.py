from app.auth.decorators import role_required
from . import customers_bp

@collectors_bp.route('/customers/index')
@login_required
@role_required('customers')
def index():
    if getattr(current_user, 'role', None) != 'customer':
        abort(401)
    return render_template('customers/index.html')