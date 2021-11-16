from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    list = book_info.query.order_by('id')
    return render_template('main.html', book_list=list)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/register')
def register():
    return render_template('register.html')