from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/audit', methods=['POST'])
def audit():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get the absolute path to the script directory (one level up from backend)
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_path = os.path.join(script_dir, 'code_auditing_tool_with_reporting.py')
        file_path_abs = os.path.abspath(filepath)

        try:
            result = subprocess.run(
                ['python', script_path, file_path_abs],
                check=True,
                capture_output=True,
                text=True,
                cwd=script_dir  # So the script always runs in its own directory
            )
        except subprocess.CalledProcessError as e:
            return jsonify({'error': e.stderr}), 500

        report_path = os.path.join(script_dir, "audit_report.html")
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report not generated'}), 500

        with open(report_path, "r", encoding="utf-8") as f:
            html_report = f.read()
        return jsonify({"html_report": html_report})

    return jsonify({'error': 'Invalid file type, only .py files allowed'}), 400

if __name__ == '__main__':
    app.run(debug=False)