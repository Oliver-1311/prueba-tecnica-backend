from flask import Flask, request, jsonify 
from models import MeasurementDetail, Summary 
from datetime import datetime
from io import TextIOWrapper
from database import db, init_db
from helpers import allowed_file, update_summary_latest
from flask_cors import CORS
import csv

#inicializar la app
app = Flask(__name__)



init_db(app)
  
CORS(app)



# creamos las APIS

@app.route('/')
def index():
    return "<p>hello world</p>"

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
        for row in csv_reader:
            measurement = MeasurementDetail(
                name_sensor=row['name_sensor'],
                value=float(row['value']),
                unit=row['unit'],
                timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S')
            )
            db.session.add(measurement)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        csv_data.seek(0)
        csv_reader = csv.DictReader(csv_data, delimiter=';')
        update_summary_latest(csv_reader,Summary,db)
        return jsonify({"message": "Datos cargados exitosamente"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/v1/list', methods=['GET'])
def get_summary():
    try:
        # Obtener los datos de resumen de la base de datos
        summary_data = Summary.query.all()

        # Formatear los datos de resumen
        summary_list = []
        for item in summary_data:
            summary_list.append({
                "Sensor": item.name_sensor,
                "Valor Promedio": item.average_value,
                "Unidad": item.unit,
                "Marca de Tiempo": item.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
            })

        return jsonify( summary_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')