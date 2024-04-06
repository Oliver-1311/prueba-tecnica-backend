from database import db
from datetime import datetime, timezone
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