"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"""
"""
from app import create_app

app = create_app('production')  # Cambiar a 'production'

if __name__ == '__main__':
    app.run()
"""
from app import create_app

app = create_app('development')  # Cambia a 'development' para debug

if __name__ == '__main__':
    app.run(debug=True)  # Asegúrate de que debug=True está aquí