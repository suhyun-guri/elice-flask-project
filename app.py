from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config) # config 에서 가져온 파일을 사용합니다.

    db.init_app(app) # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)
    
    with app.app_context():
        db.create_all()

    from views import main_view, book_detail_view
    from models import models
    app.register_blueprint(main_view.bp)
    app.register_blueprint(book_detail_view.bp)

    app.secret_key = "seeeeeeeeeeeecret"
    app.config['SESSION_TYPE'] = 'filesystem'
    
    return app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
