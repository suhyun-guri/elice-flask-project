from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *

bp = Blueprint('book_detail', __name__, url_prefix='/detail')

@bp.route('/<int:book_id>')
def book_detail(book_id):
    book = book_info.query.filter(book_info.id == book_id).first()
    review = Review.query.filter(Review.book_id == book_id).all()
    
    return render_template('book_detail.html', book=book, reviews=review)

@bp.route('/write_review/<int:book_id>', methods=['POST'])
def write_review(book_id):
    if 'name' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('book_detail.book_detail', book_id = book_id))
    rating = request.form['rating']
    content = request.form['review']
    user_id = session['id']
    
    review = Review(book_id, user_id, rating, content)
    db.session.add(review)
    db.session.commit()
    flash("리뷰 업로드 완료")
    return redirect(url_for('book_detail.book_detail', book_id=book_id))
    