from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import pathlib
from flask_cors import CORS
import subprocess
import shutil

app = Flask(__name__)
# Update CORS to accept requests from your production frontend URL
# For development, you can use * to allow all origins temporarily
CORS(app, resources={r"/*": {"origins": "*"}})  

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
ALLOWED_EXTENSIONS = {'.stl', '.obj'}

# Get the base URL from environment or default to localhost for development
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    file_ext = pathlib.Path(filename).suffix.lower()
    return file_ext in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """Create a secure version of a filename"""
    file_ext = pathlib.Path(filename).suffix.lower()
    return f"{uuid.uuid4()}{file_ext}"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Only STL and OBJ files are allowed."}), 400

    original_filename = file.filename
    unique_filename = secure_filename(original_filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    
    try:
        file.save(filepath)
        return jsonify({
            "url": f"{BASE_URL}/uploads/{unique_filename}",
            "original_filename": original_filename
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error saving file: {str(e)}"}), 500

@app.route("/convert", methods=["POST"])
def convert_file():
    try:
        data = request.get_json()
        file_url = data.get("file_url")
        original_filename = data.get("original_filename")

        if not file_url or not original_filename:
            return jsonify({"error": "Missing file URL or original filename"}), 400

        stored_filename = file_url.split("/")[-1]
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], stored_filename)

        if not os.path.exists(input_path):
            return jsonify({"error": "File not found"}), 404

        file_ext = pathlib.Path(original_filename).suffix.lower()
        
        if file_ext.lower() == '.obj':
            return jsonify({"error": "File is already in OBJ format"}), 400

        original_name_without_ext = os.path.splitext(original_filename)[0]
        converted_filename = secure_filename(f"{original_name_without_ext}.obj")
        output_path = os.path.join(app.config["CONVERTED_FOLDER"], converted_filename)

        if file_ext.lower() == '.stl':
            try:
                # First try with pymeshlab
                import pymeshlab
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(input_path)
                ms.save_current_mesh(output_path)
            except ImportError:
                # Fallback to meshlabserver
                try:
                    subprocess.run([
                        'meshlabserver', 
                        '-i', input_path, 
                        '-o', output_path
                    ], check=True)
                except (subprocess.SubprocessError, FileNotFoundError):
                    # Last resort: just copy the file
                    shutil.copy(input_path, output_path)
                    return jsonify({
                        "converted_url": f"{BASE_URL}/converted/{converted_filename}",
                        "warning": "Actual conversion not performed - you need to install pymeshlab or meshlabserver"
                    }), 200
        else:
            return jsonify({"error": f"Conversion from {file_ext} to OBJ is not supported"}), 400

        return jsonify({
            "converted_url": f"{BASE_URL}/converted/{converted_filename}"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Conversion error: {str(e)}"}), 500

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)

@app.route("/converted/<filename>")
def converted_file(filename):
    return send_from_directory(app.config["CONVERTED_FOLDER"], filename, as_attachment=True)

# Add a health check endpoint for Render
@app.route("/health")
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Use environment port if available (Render will provide this)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)