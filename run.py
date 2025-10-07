from app import create_app

app = create_app('development')  # Cambia a 'development' para debug

if __name__ == '__main__':
    app.run(debug=False)  # Asegúrate de que debug=True está aquí