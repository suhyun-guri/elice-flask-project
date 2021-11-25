import csv
from datetime import date, datetime

from app import db, create_app
from models.models import Book_info
app = create_app()
with app.app_context():
    with open('library.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            published_at = datetime.strptime(row['publication_date'], '%Y-%m-%d').date()
        image_path = f"/image/{row['book_id']}"
        try:
            open(f'static/image/{image_path}.png')
            image_path += '.png'
        except:
            image_path += '.jpg'
        book = Book_info(
            book_name=row['book_name'], publisher=row['publisher'],
            author=row['author'], publication_date=published_at, pages=int(row['pages']),
            isbn=row['isbn'], description=row['description'], link=row['link'],
            count=5, rating=0,img_path=image_path)
        
        db.session.add(book) 
    db.session.commit()
