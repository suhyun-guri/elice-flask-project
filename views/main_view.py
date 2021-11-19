from re import L
from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime

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
            session['id'] = user.id
            session['name'] = user.name
            
        flash(f"{user.name}님, 환영합니다🎉😃")
        return redirect(url_for('main.home'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@bp.route('/rental/<int:book_id>')
def rental(book_id):
    user_id = session['id']
    target_book = book_info.query.filter(book_info.id == book_id).first()
    rental_check = Rental_return.query.filter(Rental_return.book_id==book_id, Rental_return.user_id == user_id).first()
    if target_book.count >= 1:
        if rental_check:
            if rental_check.status==True:
                flash("이미 빌린 책입니다.")
                return redirect(url_for("main.home"))
        nowDate = datetime.now()
        duration = timedelta(weeks=2)
        endDate = datetime.now() + duration
        
        newRental = Rental_return(book_id, user_id, nowDate, endDate, True)
        
        target_book.count -= 1
        db.session.add(newRental)
        db.session.commit()
        flash(f"{target_book.book_name}을 대여하였습니다.")
    elif target_book.count == 0:
        flash(f"[{target_book.book_name}]의 재고가 없어 대여가 불가능합니다.")
    
    return redirect(url_for("main.home"))

@bp.route('/return_page')
def return_page():
    user_id = session['id']
    myrental = Rental_return.query.filter(Rental_return.user_id == user_id,Rental_return.status == True ).all()
    book_list = book_info.query.all()
    return render_template('return_page.html', myrental = myrental, book_list = book_list)

@bp.route('/return/<int:book_id>')
def return_book(book_id):
    user_id = session['id']
    myrental = Rental_return.query.filter(Rental_return.user_id == user_id,Rental_return.status == True, Rental_return.book_id == book_id).first()
    myrental.status = False
    
    book = book_info.query.filter(book_info.id == myrental.book_id).first()
    book.count += 1
    db.session.commit()
    flash(f"{book.book_name}이 반납완료되었습니다.")
    return redirect(url_for('main.return_page'))