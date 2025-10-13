from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Verificar si ya existe un admin
    admin = User.query.filter_by(rol='admin').first()
    if not admin:
        admin = User(
            name='Administrador Principal',
            username='admin',
            phone='1234567890',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Usuario admin creado: usuario=admin, contraseña=admin123')
    else:
        print('⚠️  Ya existe un usuario admin')