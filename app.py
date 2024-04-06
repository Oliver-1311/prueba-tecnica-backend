from flask import Flask, request, jsonify
from sqlalchemy import func 
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
    
"""sumary_line


ESTA FUNCIÓN USA TODOS LOS DATOS DE LA TABLA PARA CALCULAR EL PROMEDIO

def update_summary_full():
    try:
        # Eliminar registros anteriores del resumen
        Summary.query.delete()
        # Calcular promedios y llenar Summary de todos los datos de la tabla
        sensors = db.session.query(MeasurementDetail.name_sensor).distinct()
        for sensor in sensors:
            average_value = db.session.query(func.avg(MeasurementDetail.value)).filter(MeasurementDetail.name_sensor == sensor[0]).scalar()
            summary = Summary(
                name_sensor=sensor[0],
                average_value=average_value,
                unit=MeasurementDetail.query.filter(MeasurementDetail.name_sensor == sensor[0]).first().unit,  # Suponiendo que todas las unidades sean iguales para un sensor dado
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(summary)

        # Confirmar los cambios en la base de datos
        db.session.commit()
        return True

    except Exception as e:
        # En caso de error, realizar un rollback
        db.session.rollback()
        raise e
"""
def update_summary_latest(csv_reader):
    try:
        # Eliminar registros anteriores del resumen
        Summary.query.delete()

        # Diccionario para mantener sumas parciales y recuentos de valores para cada sensor
        sensor_data = {}

        # Procesar datos del CSV y calcular sumas parciales y recuentos de valores para cada sensor
        for row in csv_reader:
            sensor_name = row['name_sensor']
            value = float(row['value'])

            if sensor_name not in sensor_data:
                sensor_data[sensor_name] = {'sum': value, 'count': 1}
            else:
                sensor_data[sensor_name]['sum'] += value
                sensor_data[sensor_name]['count'] += 1

        # Calcular promedios y llenar la tabla Summary
        for sensor_name, data in sensor_data.items():
            average_value = data['sum'] / data['count']
            unit = row['unit']  # Se supone que todas las unidades son iguales para un sensor dado
            summary = Summary(
                name_sensor=sensor_name,
                average_value=average_value,
                unit=unit,
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(summary)

        # Confirmar los cambios en la base de datos
        db.session.commit()
        return True

    except Exception as e:
        # En caso de error, realizar un rollback
        db.session.rollback()
        raise e


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
        update_summary_latest(csv_reader)
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

        return jsonify({"data": summary_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run()