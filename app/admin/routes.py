from app.auth.decorators import role_required
from . import admin_bp

@admin_bp.route('/admin/index')
@login_required
@role_required('admin')
def index():
    if getattr(current_user, 'role', None) != 'admin':
        abort(401)
    return render_template('admin/index.html')
