from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Verificar si ya existe un collector
    collector = User.query.filter_by(rol='collector').first()
    if not collector:
        collector = User(
            name='Colector Principal',
            username='collector',
            phone='0987654321',
            rol='collector'
        )
        collector.set_password('collector123')
        db.session.add(collector)
        db.session.commit()
        print('✅ Usuario collector creado: usuario=collector, contraseña=collector123')
    else:
        print('⚠️  Ya existe un usuario collector')