from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app
# from flask_login import login_required

# from app import db

main = Blueprint('main', __name__, template_folder='../templates')

@main.route('/')
def index():
    return render_template('index.html')
