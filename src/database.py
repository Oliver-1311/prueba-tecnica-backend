from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DB_URL')

db = SQLAlchemy()
try:
        with open('../init_db.sql', 'r') as sql_file:
            pass
        print("El archivo init_db.sql se ejecutó correctamente.")
except FileNotFoundError:
        print("El archivo init_db.sql no se encontró.")
except Exception as e:
        print(f"Error al ejecutar init_db.sql: {str(e)}")

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
      
    db.init_app(app)
    

    with app.app_context():
        db.create_all()