from flask import Blueprint, render_template, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *

bp = Blueprint('mylibrary', __name__, url_prefix='/mylibrary')

@bp.route('/')
def mylibrary():
    user_id = session['id']
    user_info = User.query.filter(User.id == user_id).first()
    myrental = Rental_return.query.filter(Rental_return.user_id == user_id).all()
    count = 0
    for rental in myrental:
        if rental.status == True:
            count+=1
    
    book_list = Book_info.query.all()
    myreview = Review.query.filter(Review.user_id == user_id).all()
    return render_template('mylibrary.html', user=user_info, myrental = myrental, book_list = book_list, myreview=myreview, nowrental = count)

@bp.route('/<int:rental_id>')
def delete_history(rental_id):
    user_id = session['id']
    myrental = Rental_return.query.filter(Rental_return.id == rental_id).first()
    
    if not myrental:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    if myrental.user_id != user_id:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))
    if myrental.status == True:
        flash("대여중이므로 삭제가 불가능합니다. 반납을 먼저 해주세요.")
        return redirect(url_for('mylibrary.mylibrary'))
    
    db.session.delete(myrental)
    db.session.commit()
    flash("대여기록이 삭제되었습니다.")
    return redirect(url_for("mylibrary.mylibrary"))

@bp.route('/delete_user')
def delete_user():
    user_id = session['id']
    user_info = User.query.filter(User.id == user_id).first()
    rental_return = Rental_return.query.filter(Rental_return.user_id == user_id, Rental_return.status == True).all()
    if rental_return:
        flash("반납하지 않은 책이 존재합니다. 모두 반납 후 탈퇴가 가능합니다.")
        return redirect(url_for("return_page.return_page"))
    if not user_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))
    if user_info.id != user_id:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))
    db.session.delete(user_info)
    db.session.commit()
    session.clear()

    flash("탈퇴 완료되었습니다. 안녕히가세요.")
    return redirect(url_for('main.home'))

@bp.route('/update_password', methods=['GET','POST'])
def update_password():
    if 'id' not in session: #로그인되어 있는 경우, home으로
        return redirect(url_for('auth.login'))
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.id == session['id']).first()
        current_password = form.data.get('current_password')
        new_password = form.data.get('new_password')
        
        if user and check_password_hash(user.password, current_password):
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('비밀번호가 변경되었습니다.')
            return redirect(url_for('mylibrary.mylibrary'))
        else:
            flash('현재 비밀번호가 틀렸습니다.')
    return render_template("update_password.html", form=form)