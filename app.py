from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola Mundo!'

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/saludo/<nombre>')
def saludo_personalizado(nombre):
    return render_template('index.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)