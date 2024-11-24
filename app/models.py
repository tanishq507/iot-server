from . import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100))
    logs = db.relationship('DeviceLog', backref='device', lazy=True)

class DeviceLog(db.Model):
    __tablename__ = 'device_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    temperature = db.Column(db.Float)
    battery = db.Column(db.Float)
    uptime = db.Column(db.Integer)
    log_entry = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)