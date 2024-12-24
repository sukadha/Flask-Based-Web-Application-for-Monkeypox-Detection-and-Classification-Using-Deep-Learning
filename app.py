from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
import json

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle image upload and redirect to results page."""
    if 'file' not in request.files:
        return render_template('index.html', error="No file selected.")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No file selected.")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Simulate disease detection
        try:
            result = subprocess.run(
                ['python', 'process_image.py', file_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                disease_info = json.loads(result.stdout)
            else:
                disease_info = {"error": "Failed to process the image."}
        except Exception as e:
            disease_info = {"error": str(e)}
        
        return render_template('nextpage.html', image_url=file_path, disease_info=disease_info)

    return render_template('index.html', error="Invalid file type.")

@app.route('/nextpage', methods=['GET'])
def next_page():
    """Display results (for testing purposes)."""
    return render_template('nextpage.html')

if __name__ == '__main__':
    app.run(debug=True)
