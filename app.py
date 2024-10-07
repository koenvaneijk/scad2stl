import os
from flask import Flask, request, send_file
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_scad_to_stl():
    data = request.json
    if not data:
        return 'No JSON data provided', 400

    # Extract parameters
    params = data.get('parameters', {})
    
    # Create a temporary directory to store the files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Check if SCAD content is provided in the request
        if 'scad' in data:
            scad_content = data['scad']
            scad_path = os.path.join(tmpdir, 'input.scad')
            with open(scad_path, 'w') as f:
                f.write(scad_content)
        else:
            # If no SCAD content, check for file upload
            if 'file' not in request.files:
                return 'No file part and no SCAD content provided', 400
            file = request.files['file']
            if file.filename == '':
                return 'No selected file and no SCAD content provided', 400
            
            # Check if the file is a .scad file
            if not file.filename.lower().endswith('.scad'):
                return 'Invalid file type. Please upload a .scad file.', 400

            # Save the uploaded .scad file
            scad_path = os.path.join(tmpdir, 'input.scad')
            file.save(scad_path)

        # Modify the .scad file with the provided parameters
        with open(scad_path, 'r') as f:
            scad_content = f.read()

        for key, value in params.items():
            scad_content = scad_content.replace(f'${key}', str(value))

        with open(scad_path, 'w') as f:
            f.write(scad_content)

        # Output .stl file path
        stl_path = os.path.join(tmpdir, 'output.stl')

        # Run OpenSCAD to convert .scad to .stl
        try:
            subprocess.run(['openscad', '-o', stl_path, scad_path], check=True)
        except subprocess.CalledProcessError:
            return 'Error during OpenSCAD conversion', 500

        # Send the resulting .stl file
        return send_file(stl_path, as_attachment=True, download_name='output.stl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)