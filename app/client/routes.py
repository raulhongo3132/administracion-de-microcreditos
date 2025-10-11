from flask import render_template
from flask_login import login_required
from . import client_bp

@client_bp.route("/")
@login_required
def index():
    return "Panel de cliente"
