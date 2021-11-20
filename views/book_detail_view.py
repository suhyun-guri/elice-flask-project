from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *
from datetime import timedelta, datetime


bp = Blueprint('book_detail', __name__, url_prefix='/detail')

@bp.route('/<int:book_id>')
def book_detail(book_id):
    book_info = Book_info.query.filter(Book_info.id == book_id).first()
    review_info = Review.query.filter(Review.book_id == book_id).all()
  
    if not book_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for("main.home"))
    avg = book_info.rating
    
    return render_template('book_detail.html', book=book_info, reviews=review_info, avg = avg)

@bp.route('/write_review/<int:book_id>', methods=['POST'])
def write_review(book_id):
    if 'name' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('book_detail.book_detail', book_id = book_id))
    
    book_info = Book_info.query.filter(Book_info.id == book_id).first()
    review_info = Review.query.filter(Review.book_id == book_id).all()
    temp = book_info.rating * len(review_info)
    user_id = session['id']
    
    check_myreview = Review.query.filter(Review.book_id == book_id, Review.user_id == user_id).first()
    if check_myreview:
        flash("이미 작성한 리뷰가 있습니다.")
        return redirect(url_for('book_detail.book_detail', book_id=book_id))
    
    if 'rating' in request.form:        
        rating = request.form['rating']
        content = request.form['review']
        user_name = session['name']
        
        review = Review(book_id, user_id, user_name, rating, content)
        db.session.add(review)
        
        newrating = round((temp + int(rating)) / (len(review_info) + 1), 2)
        book_info.rating = newrating
        db.session.commit() 
        flash("리뷰 업로드 완료")
        return redirect(url_for('book_detail.book_detail', book_id=book_id))
    else:
        flash("별점을 주세요!")
        return redirect(url_for('book_detail.book_detail', book_id=book_id))

@bp.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    if 'id' not in session:
        flash("권한이 없습니다. 로그인 후 이용하세요.")
        return redirect(url_for('main.home'))
    user_id = session['id']
    user_info = User.query.filter(User.id == user_id).first()
    myreview = Review.query.filter(Review.id == review_id).first()
    delete_rating = myreview.star
    book_id = myreview.book_id

    if not myreview:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    if not user_info or myreview.user_id != user_id:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))
    
    db.session.delete(myreview)
    
    book_info = Book_info.query.filter(Book_info.id == book_id).first()
    review_info = Review.query.filter(Review.book_id == book_id).all()
    
    rating_sum, average = 0, 0
    if review_info:
        for review in review_info:
            rating_sum += review.star
        average = round((rating_sum / len(review_info)), 1)
    book_info.rating = average
    
    db.session.commit()
    
    flash("리뷰가 삭제되었습니다.")
    return redirect(url_for('book_detail.book_detail', book_id=book_info.id))