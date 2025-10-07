from app.auth.decorators import role_required
from . import collectors_bp

@collectors_bp.route('/collector/index')
@login_required
@role_required('collector')
def index():
    if getattr(current_user, 'role', None) != 'collector':
        abort(401)
    return render_template('collectors/index.html')
