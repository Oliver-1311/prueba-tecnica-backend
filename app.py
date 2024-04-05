from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from io import TextIOWrapper
import csv
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}
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
    
 

# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# las APIS
@app.route('/')
def index():
    return "<p>hello world</p>"

#Carga y procesamiento de datos

@app.route('/api/v1/load', methods=['POST'])
def load_data():
    try:
        # Verificamos si se envió un archivo
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró ningún archivo en la solicitud"}), 400
        
        file = request.files['file']
        # Verificar si se envió un archivo con nombre
        if file.filename == '':
            return jsonify({"error": "Archivo no seleccionado"}), 400
        
        # Verificar si la extensión del archivo es válida
        if not allowed_file(file.filename):
            return jsonify({"error": "Extensión de archivo no permitida"}), 400
        
        csv_data = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.DictReader(csv_data, delimiter=';')

        # Procesar y guardar los datos en la base de datos
        # for row in csv_reader:
        #     measurement = MeasurementDetail(
        #         name_sensor=row['name_sensor'],
        #         value=float(row['value']),
        #         unit=row['unit'],
        #         timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S')
        #     )
        #     db.session.add(measurement)

        # db.session.commit()
        
        # Crear una lista para almacenar los datos del CSV
        csv_data_list = []

        # Iterar sobre el csv_reader y agregar cada fila a la lista
        for row in csv_reader:
            csv_data_list.append(row)

        # Devolver los datos del CSV como JSON
        return jsonify({"data": csv_data_list})


    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/v1/list', methods=['GET'])
def get_summary():
    return 'buscando datos'
    

if __name__ == '__main__':
    app.run()