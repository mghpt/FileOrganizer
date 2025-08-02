from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os
import threading
from file_scanner import scan_drive, find_duplicates

app = Flask(__name__)
scan_data = None
scan_in_progress = False

@app.route('/')
def index():
    return render_template('index.html', files=[])

@app.route('/start-scan')
def start_scan():
    global scan_data, scan_in_progress

    if scan_in_progress:
        return jsonify({'status': 'in_progress'})

    def background_scan():
        global scan_data, scan_in_progress
        scan_in_progress = True
        scan_data = scan_drive().head(500).to_dict(orient='records')
        scan_in_progress = False

    threading.Thread(target=background_scan).start()
    return jsonify({'status': 'started'})

@app.route('/scan-status')
def scan_status():
    global scan_data, scan_in_progress
    if scan_in_progress:
        return jsonify({'status': 'in_progress'})
    elif scan_data:
        return jsonify({'status': 'done', 'data': scan_data})
    else:
        return jsonify({'status': 'idle'})

@app.route('/download')
def download_csv():
    df = scan_drive()
    output_path = os.path.join('download', 'file_inventory.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return send_file(output_path, as_attachment=True)

@app.route('/duplicates')
def duplicates_page():
    df = find_duplicates()
    return render_template('duplicates.html', duplicates=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(port=8088)
