from flask import Blueprint, render_template, request, url_for, session, redirect, flash, jsonify
from models.models import *

bp = Blueprint('book_detail', __name__, url_prefix='/detail')

@bp.route('/<int:book_id>')
def book_detail(book_id):
    book = book_info.query.filter(book_info.id == book_id).first()
    review = Review.query.filter(Review.book_id == book_id).all()
    
    return render_template('book_detail.html', book=book, review=review)