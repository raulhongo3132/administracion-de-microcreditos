from app import login_manager
from app.models.user import User

# Configuración de Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))