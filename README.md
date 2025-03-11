# Dimensia - 3D Model Converter (Backend)

A Flask-based backend service for converting 3D model files from STL to OBJ format.

## Features

- RESTful API for 3D model conversion
- STL to OBJ file format transformation
- Cross-origin resource sharing support
- File handling and processing

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or newer
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PL-SaiPrakash/backend-Dimensia.git
   cd backend-Dimensia
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

This project relies on the following packages:
- Flask==2.0.1
- Werkzeug==2.0.3
- flask-cors==3.0.10
- gunicorn==20.1.0
- pymeshlab==2022.2.post3
- python-dotenv==0.19.0

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
   or
   ```bash
   flask run
   ```

2. The API will be available at:
   ```
   http://localhost:5000
   ```

## API Endpoints

### Upload STL File

```
POST /upload
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with a file field named `file` containing the STL file

**Response:**
- Success: 200 OK with confirmation message
- Error: 400 Bad Request with error message

### Convert STL to OBJ

```
POST /convert
```

**Request:**
- Content-Type: `application/json`
- Body: JSON with the filename to convert

**Response:**
- Success: 200 OK with the converted OBJ file for download
- Error: 400 Bad Request with error message

## Configuration

The application can be configured using environment variables in a `.env` file:
- `PORT`: The port on which the server runs (default: 5000)
- `DEBUG`: Enable debug mode (default: False)
- `UPLOAD_FOLDER`: Directory for temporary file storage
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)

## Deployment

For production deployment, the project includes Gunicorn as a WSGI HTTP server.

Example Gunicorn command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
## Related Projects

- [Dimensia Frontend](https://github.com/PL-SaiPrakash/frontend-Dimensia) - React frontend for this application
