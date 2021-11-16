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
    link = db.Column(db.String(1000))

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
    