from datetime import datetime, timezone
from sqlalchemy import func

ALLOWED_EXTENSIONS = {'csv'}
# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





def update_summary_latest(csv_reader,Summary,db):
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
  


#ESTA FUNCIÓN USA TODOS LOS DATOS DE LA TABLA PARA CALCULAR EL PROMEDIO
def update_summary_full(Summary, db, MeasurementDetail):
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