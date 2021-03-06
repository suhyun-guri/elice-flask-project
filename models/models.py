from app import db
from datetime import datetime

class Book_info(db.Model):
    __tablename__ = 'book_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255))
    author = db.Column(db.String(50))
    publication_date = db.Column(db.Date)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.Integer)
    description = db.Column(db.Text)
    link = db.Column(db.String(1000))
    count = db.Column(db.Integer) #재고
    rating = db.Column(db.Integer) #별점
    img_path = db.Column(db.String(255)) #책 이미지 경로
    
    bookid1 = db.relationship("Rental_return", backref="book_info")
    bookid2 = db.relationship("Review", backref="book_info")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    rentalid1 = db.relationship("Rental_return", backref="user")
    rentalid2 = db.relationship("Review", backref="user")

class Rental_return(db.Model):
    __tablename__ = 'rental_return'
    id =  db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book_info.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    rental_date = db.Column(db.Date) #대여날짜
    return_date = db.Column(db.Date) #반납날짜 (대여중이면 반납기한(대여날짜 + 2주))
    status = db.Column(db.Boolean) #대여중이면 True, 반납완료면 False
    
    def __init__(self,book_id,user_id,rental_date,return_date,status):
        self.book_id = book_id
        self.user_id = user_id
        self.rental_date = rental_date
        self.return_date = return_date
        self.status = status
    
class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book_info.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    star = db.Column(db.Integer)
    content = db.Column(db.Text)
    created_date = db.Column(db.Date) 
    user_name = db.Column(db.String(255))
    
    def __init__(self, book_id, user_id, user_name, star, content, created_date):
        self.book_id = book_id
        self.user_id = user_id
        self.user_name = user_name
        self.star = star
        self.content = content
        self.created_date = created_date