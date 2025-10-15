from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Verificar si ya existe un admin
    admin = User.query.filter_by(rol='admin').first()
    if not admin:
        admin = User(
            name='Administrador principal',
            username='admin',
            phone='5562540486',
            rol='admin123'
        )
        admin.set_password('313271320')
        db.session.add(admin)
        db.session.commit()
        print('✅ Usuario admin creado: usuario=raulval, contraseña=313271320')
    else:
        print('⚠️  Ya existe un usuario admin')
