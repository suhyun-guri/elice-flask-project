from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    list = book_info.query.order_by('id')
    return render_template('main.html', book_list=list)

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        user = User.query.filter(User.email == request.form['email']).first()
        if not user:
            if request.form['password'] != request.form['check_password']:
                flash("비밀번호 확인이 다릅니다.")
                return redirect(url_for('main.register'))
            password = generate_password_hash(request.form['password'])
            user = User(request.form['name'], request.form['email'], password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            flash('이미 가입된 아이디입니다.')
            return redirect(url_for('main.register'))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email == email).first()
        if not user:
            flash("없는 이메일입니다.")
            return redirect(url_for('main.login'))
        elif not check_password_hash(user.password, password):
            flash("비밀번호가 틀렸습니다.")
            return redirect(url_for('main.login'))
        else:
            session.clear()
            session['email'] = email
            session['name'] = user.name
            
        flash(f"{user.name}님, 환영합니다🎉😃")
        return redirect(url_for('main.home'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))