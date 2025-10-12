from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    # Pasando variables a la plantilla
    return render_template('usuario.html', 
                         nombre=nombre, 
                         edad=25,
                         hobbies=['programar', 'leer', 'deportes'])

@app.route('/condicionales/<int:edad>')
def condicionales(edad):
    return render_template('condicionales.html', edad=edad)

@app.route('/herencia')
def herencia():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)