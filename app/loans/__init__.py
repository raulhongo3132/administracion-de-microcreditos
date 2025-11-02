from flask import Blueprint, render_template, redirect, url_for

auth_bp = Blueprint('loans', __name__, url_prefix='/loans')
