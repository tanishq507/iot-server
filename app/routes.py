from flask import Blueprint, jsonify, request, render_template, send_file
from .models import Device, DeviceLog
from . import db
from datetime import datetime
import csv
from io import StringIO

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('devices.html', devices=Device.query.all())

@main.route('/dev', methods=['GET', 'POST', 'PUT'])
def devices():
    if request.method == 'GET':
        devices = Device.query.all()
        return render_template('devices.html', devices=devices)
    
    elif request.method == 'POST':
        data = request.json
        new_device = Device(
            name=data['device_name'],
            status=data['device_status']
        )
        db.session.add(new_device)
        db.session.commit()
        return jsonify({'message': 'Device added successfully'})
    
    elif request.method == 'PUT':
        data = request.json
        device = Device.query.get_or_404(data['device_id'])
        if 'device_name' in data:
            device.name = data['device_name']
        if 'device_status' in data:
            device.status = data['device_status']
        db.session.commit()
        return jsonify({'message': 'Device updated successfully'})

@main.route('/dev/<int:dev_id>/dev_info', methods=['GET', 'POST'])
def device_info(dev_id):
    device = Device.query.get_or_404(dev_id)
    
    if request.method == 'GET':
        logs = DeviceLog.query.filter_by(device_id=dev_id).order_by(DeviceLog.timestamp.desc()).limit(10).all()
        return render_template('device_info.html', device=device, logs=logs)
    
    elif request.method == 'POST':
        data = request.json
        device.address = data.get('address', device.address)
        db.session.commit()
        return jsonify({'message': 'Device info updated successfully'})

@main.route('/data', methods=['POST'])
def handle_data():
    data = request.json
    if 'device_id' in data:
        device = Device.query.get_or_404(data['device_id'])
        log = DeviceLog(
            device_id=device.id,
            temperature=data.get('temperature'),
            battery=data.get('battery'),
            uptime=data.get('uptime'),
            log_entry=data.get('log_entry')
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Data processed successfully'})
    return jsonify({'error': 'Invalid data format'}), 400

@main.route('/generate-report')
def generate_report():
    devices = Device.query.all()
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Device ID', 'Name', 'Status', 'Address', 'Last Temperature', 'Last Battery', 'Last Uptime'])
    
    # Write device data
    for device in devices:
        last_log = DeviceLog.query.filter_by(device_id=device.id).order_by(DeviceLog.timestamp.desc()).first()
        writer.writerow([
            device.id,
            device.name,
            device.status,
            device.address or 'N/A',
            f"{last_log.temperature}°C" if last_log and last_log.temperature else 'N/A',
            f"{last_log.battery}%" if last_log and last_log.battery else 'N/A',
            f"{last_log.uptime}h" if last_log and last_log.uptime else 'N/A'
        ])
    
    output.seek(0)
    return send_file(
        StringIO(output.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'device_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@main.route('/system-settings')
def system_settings():
    return render_template('system_settings.html')

@main.route('/view-logs')
def view_logs():
    logs = DeviceLog.query.order_by(DeviceLog.timestamp.desc()).limit(100).all()
    return render_template('logs.html', logs=logs)