from flask_sqlalchemy import SQLAlchemy

host = 'localhost'
password = 'postgres1234'
database = 'pruebatecnica'

DATABASE_URL = f'postgresql://postgres:{password}@{host}/{database}'

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()