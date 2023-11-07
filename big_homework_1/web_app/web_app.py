from flask import Flask, jsonify, request, render_template
from pysondb import db
import os
import json
from statistics import mean

app = Flask(__name__)

db_path = os.path.join('data', 'temperatures.json')
json_db = db.getDb(db_path)

@app.route('/')
@app.route('/home')
def index():
    all_data = json_db.getAll()
    device_ids = [f"thermometer-{i}" for i in range(1, 7)]
    return render_template('home.html', device_ids=device_ids)

@app.route('/data', methods=['POST'])
def data():
    content = request.json
    json_db.add(content)
    return jsonify({"success": True}), 200

@app.route('/graph/<thermometer_id>')
def graph(thermometer_id):
    data = json_db.getByQuery({"device_id": thermometer_id})
    data.sort(key=lambda x: x['timestamp'])
    timestamps = [entry['timestamp'] for entry in data]
    values = [entry['value'] for entry in data]
    
    return render_template('graph.html', device_id=thermometer_id, timestamps=timestamps, values=values)

@app.route('/stats')
def stats():
    all_data = json_db.getAll()
    stats = {}
    for entry in all_data:
        device_id = entry['device_id']
        value = entry['value']
        if device_id not in stats:
            stats[device_id] = []
        stats[device_id].append(value)
    
    stats_result = {device_id: {
        'average': mean(values),
        'max': max(values),
        'min': min(values)
    } for device_id, values in stats.items()}
    
    return render_template('stats.html', stats_result=stats_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
