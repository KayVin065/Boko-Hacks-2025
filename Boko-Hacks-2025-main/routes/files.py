from flask import Blueprint, render_template, request, jsonify, session, send_file
from extensions import db
from models.user import User
from models.file import File
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import requests

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'} 
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


files_bp = Blueprint('files', __name__, url_prefix='/apps/files')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/')
def files():
    """Render files page with all files uploaded by the current user"""
    print("=== FILES LISTING ROUTE ACCESSED ===")
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    print(f"Loading files for user: {current_user.username} (ID: {current_user.id})")
    
    all_files = File.query.filter_by(user_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    print(f"Found {len(all_files)} files")
    
    for file in all_files:
        print(f"  - ID: {file.id}, Filename: {file.filename}, Uploaded: {file.uploaded_at}")
    
    return render_template('files.html', files=all_files, current_user_id=current_user.id)

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload with intentional vulnerability"""
    print("\n=== FILE UPLOAD ATTEMPT ===")
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")
    print(f"Files: {request.files}")
    
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    file = request.files.get('file')
    print(f"Received file: {file}")
    
    if not file:
        print("No file part in request")
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    if file:  
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"File path: {file_path}")
        
        try:
            file.save(file_path)
            print(f"File saved successfully at {file_path}")

            new_file = File(
                filename=filename,
                file_path=file_path,
                user_id=current_user.id
            )
            db.session.add(new_file)
            db.session.commit()
            print(f"File record saved to database with ID: {new_file.id}")

            return jsonify({
                'success': True,
                'message': 'File uploaded successfully!',
                'file': new_file.to_dict()
            })
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        print("File type not allowed or no file uploaded")
        return jsonify({'success': False, 'error': 'File type not allowed'}), 400

'''
# Retrieve the VirusTotal API Key from the environment variable
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
VIRUS_TOTAL_URL = "https://www.virustotal.com/api/v3/files/"

files_bp = Blueprint('files', __name__, url_prefix='/apps/files')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/')
def files():
    """Render files page with all files uploaded by the current user"""
    print("=== FILES LISTING ROUTE ACCESSED ===")
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    print(f"Loading files for user: {current_user.username} (ID: {current_user.id})")
    
    all_files = File.query.filter_by(user_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    print(f"Found {len(all_files)} files")
    
    for file in all_files:
        print(f"  - ID: {file.id}, Filename: {file.filename}, Uploaded: {file.uploaded_at}")
    
    return render_template('files.html', files=all_files, current_user_id=current_user.id)

# Function to scan file using VirusTotal API
def scan_file_virustotal(file):
    """Scan the uploaded file with VirusTotal"""
    headers = {
        "x-apikey": VIRUS_TOTAL_API_KEY  # Make sure you store your API key securely in env variables
    }

    # Read the file into memory
    file_data = file.read()  # 'file' is the file object from request.files
    
    # Create a memory-based file-like object
    file_memory = BytesIO(file_data)

    # Make the request to VirusTotal
    response = requests.post(
        VIRUS_TOTAL_URL,
        headers=headers,
        files={"file": file_memory}
    )

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()

        print(f"Scanned file: {file.filename}")
        print(f"VirusTotal Response: {response.json()}")
        # If any of the antivirus engines detected a virus, return False
        if result['data']['attributes']['last_analysis_stats']['malicious'] > 0:
            return False
        else:
            return True
    else:
        # Handle any error from VirusTotal (e.g., invalid API key or rate limit)
        print(f"Error scanning with VirusTotal: {response.status_code} {response.text}")
        return False


@files_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload with intentional vulnerability"""
    print("\n=== FILE UPLOAD ATTEMPT ===")
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")
    print(f"Files: {request.files}")
    
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    file = request.files.get('file')
    print(f"Received file: {file}")
    
    if not file:
        print("No file part in request")
        return jsonify({'success': False, 'error': 'No file part'}), 400

        # Scan the file in memory
    is_clean = scan_file_virustotal(file)
    if not is_clean:
        return jsonify({'error': 'Virus detected in the uploaded file.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(file_path)  # Now save the file after scanning
        print(f"File saved successfully at {file_path}")

        new_file = File(
                filename=filename,
                file_path=file_path,
                user_id=current_user.id
            )
        db.session.add(new_file)
        db.session.commit()
        print(f"File record saved to database with ID: {new_file.id}")

        return jsonify({
                'success': True,
                'message': 'File uploaded successfully!',
                'file': new_file.to_dict()
            }), 200
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return jsonify({'success': False, 'error': 'File save failed'}), 500
'''        
    
@files_bp.route('/delete/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file"""
    print(f"\n=== FILE DELETE ATTEMPT: ID {file_id} ===")
    
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
        
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    try:
        file = File.query.get_or_404(file_id)
        print(f"Found file {file_id}: {file.filename}")
        
        if file.user_id != current_user.id:
            print(f"Access denied: File {file_id} belongs to user {file.user_id}, not {current_user.id}")
            return jsonify({'success': False, 'error': 'Access denied'}), 403

        file_path = file.file_path
        
        db.session.delete(file)
        db.session.commit()
        print(f"File record deleted from database")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted from filesystem: {file_path}")
        else:
            print(f"Warning: File not found on filesystem: {file_path}")
            
        return jsonify({'success': True, 'message': 'File deleted successfully'})
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

from flask import send_from_directory

@files_bp.route('/download/<int:file_id>')
def download_file(file_id):
    """Download a file using send_from_directory for maximum compatibility"""
    print(f"\n=== FILE DOWNLOAD ATTEMPT: ID {file_id} ===")
    
    if 'user' not in session:
        print("User not logged in")
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    current_user = User.query.filter_by(username=session['user']).first()
    if not current_user:
        print(f"User {session['user']} not found in database")
        return jsonify({'success': False, 'error': 'User not found'}), 404

    try:
        file = File.query.get_or_404(file_id)
        print(f"Found file {file_id}: {file.filename}")
        
        
        # Get the directory and filename
        directory = os.path.dirname(file.file_path)
        filename = os.path.basename(file.file_path)
        
        if os.path.exists(file.file_path):
            print(f"Sending file: {file.file_path}")
            
            return send_from_directory(
                directory,
                filename,
                as_attachment=True
            )
        else:
            print(f"Error: File not found on filesystem: {file.file_path}")
            return jsonify({'success': False, 'error': 'File not found on server'}), 404
    except Exception as e:
        print(f"Error sending file: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500