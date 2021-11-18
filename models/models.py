from app import db

class book_info(db.Model):
    __tablename__ = 'book_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255))
    author = db.Column(db.String(50))
    publication_date = db.Column(db.Date)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.Integer)
    description = db.Column(db.Text)
    link = db.Column(db.String(1000)),
    count = db.Column(db.Integer)
    
    bookid1 = db.relationship("rental_return", backref="book_info")
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
    rentalid1 = db.relationship("rental_return", backref="user")
    rentalid2 = db.relationship("Review", backref="user")

class rental_return(db.Model):
    __tablename__ = 'rental_return'
    id =  db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book_info.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    rental_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    status = db.Column(db.Boolean)
    
class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book_info.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    star = db.Column(db.Integer)
    content = db.Column(db.Text)
    
    def __init__(self, book_id, user_id, star, content):
        self.book_id = book_id
        self.user_id = user_id
        self.star = star
        self.content = content