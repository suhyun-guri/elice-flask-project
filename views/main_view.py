from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash
from datetime import timedelta, datetime
from forms import *
'''
메인 화면 페이지
메인, 대여, 검색
'''
bp = Blueprint('main', __name__, url_prefix='/')

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@bp.route('/')
def home():
    page = request.args.get('page', type=int, default=1) #페이지
    book_list = Book_info.query.order_by('id')
    book_list = book_list.paginate(page, per_page=8)
    return render_template('main.html', book_list = book_list)

@bp.route('/rental/<int:book_id>')
def rental(book_id):
    user_id = session['id']
    target_book = Book_info.query.filter(Book_info.id == book_id).first()
    rental_check = Rental_return.query.filter(Rental_return.book_id==book_id, Rental_return.user_id == user_id, Rental_return.status==True).first()
    rental_cnt_check = Rental_return.query.filter(Rental_return.user_id == user_id, Rental_return.status==True).all()
    if target_book.count >= 1:
        if rental_check:
            flash("이미 빌린 책입니다.")
            return redirect(url_for("main.home"))
        if len(rental_cnt_check) >= 5:
            flash("현재 대여중인 책 5권이 존재합니다. 대여는 5권까지 가능합니다.")
            return redirect(url_for("main.home"))
        nowDate = datetime.utcnow() + timedelta(hours=9)
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

@bp.route('/search', methods = ['GET', 'POST'])
def search():
    #query string 가져오기
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    #검색어가 있다면,
    if keyword:
        count = Book_info.query.order_by('id').filter(Book_info.book_name.like(f"%{keyword}%")).count()
        result = Book_info.query.order_by('id').filter(Book_info.book_name.like(f"%{keyword}%")).order_by(Book_info.id).paginate(page=page, per_page=8)
    return render_template('search.html', book_list = result, keyword=keyword, count=count)

