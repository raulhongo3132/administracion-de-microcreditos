#from flask import render_template
#from app.main import bp

#@bp.route('/')
#def index():
#    return render_template('main/index.html', title='Inicio')

#@bp.route('/about')
#def about():
#    return render_template('main/about.html', title='Acerca de')

from flask import render_template
from app.main import bp
import os

@bp.route('/')
def index():
    # Listar qué plantillas encuentra Flask
    print("Buscando plantillas en:", bp.template_folder)
    return render_template('main/index.html', title='Inicio')

@bp.route('/about')
def about():
    return render_template('main/about.html', title='Acerca de')