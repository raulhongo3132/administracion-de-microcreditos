from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Verificar si ya existe un customer
    customer = User.query.filter_by(rol='customer').first()
    if not customer:
        customer = User(
            name='Customer',
            username='customer',
            phone='1122334455',
            rol='customer'
        )
        customer.set_password('customer234')
        db.session.add(customer)
        db.session.commit()
        print('✅ Usuario customer creado: usuario=customer, contraseña=customer123')
    else:
        print('⚠️  Ya existe un usuario customer')