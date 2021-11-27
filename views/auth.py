from flask import Blueprint, render_template, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
'''
auth 관련 기능
회원가입, 로그인, 로그아웃
'''
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    if 'id' in session: #로그인되어 있는 경우, home으로
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.data.get('email')
        name = form.data.get('name')
        password = form.data.get('password')
        hash_password = generate_password_hash(password)
        
        user = User(name, email, hash_password)
        db.session.add(user)
        db.session.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    if 'id' in session: #로그인되어 있는 경우, home으로
        return redirect(url_for('main.home'))
    
    form = LoginForm()    
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data.get('email')).first()
        password = form.data.get('password')
        if user and check_password_hash(user.password, password):
            session.clear()
            session['id'] = user.id
            session['name'] = user.name    
            flash(f"{user.name}님, 환영합니다🎉😃")
            return redirect(url_for('main.home'))
        else:
            flash("비밀번호가 틀렸습니다.")
    return render_template("login.html", form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


