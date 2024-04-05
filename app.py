from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# configuración de la BD
host = 'localhost'
password = 'postgres1234'
database = 'pruebatecnica'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#seed.py ... sembrando la base de datos


class MeasurementDetail(db.Model):
    __tablename__ = 'measurement_detail'
    id = db.Column(db.Integer, primary_key = True)
    name_sensor = db.Column(db.String(50), nullable = False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default = datetime.now(timezone.utc))

class Summary(db.Model):
    __tablename__ = 'summary'
    id = db.Column(db.Integer, primary_key=True)
    name_sensor = db.Column(db.String(50), nullable=False)
    average_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default = datetime.now(timezone.utc))
    
 


# las APIS
@app.route('/')
def index():
    return "<p>hello world</p>"

@app.route('/api/v1/load', methods=['POST'])
def load_data():
    return 'enviando datos'

@app.route('/api/v1/list', methods=['GET'])
def get_data():
    return 'buscando datos'
    

if __name__ == '__main__':
    app.run()