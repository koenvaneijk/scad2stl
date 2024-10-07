# OpenSCAD Flask API

This project provides a Flask-based API that converts OpenSCAD (.scad) files to STL files, allowing for parameter customization.

## Setup

1. Ensure you have Docker installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/koenvaneijk/openscad-flask-api.git
   cd openscad-flask-api
   ```
3. Build the Docker image:
   ```
   docker build -t openscad-flask .
   ```
4. Run the Docker container:
   ```
   docker run -p 5000:5000 openscad-flask
   ```

The API will now be available at `http://localhost:5000`.

## API Usage

The API provides a single endpoint for converting SCAD files to STL:

### POST /convert

Converts a SCAD file to STL, applying custom parameters if provided.

#### Request

- Content-Type: `application/json`
- Body:
  - `scad`: The SCAD file content as a string (optional if file is provided)
  - `parameters`: An object containing parameter key-value pairs (optional)

OR

- Content-Type: `multipart/form-data`
- Body:
  - `file`: The .scad file to convert (optional if SCAD content is provided in JSON)
  - `data`: A JSON string containing:
    - `parameters`: An object with parameter key-value pairs (optional)

#### Response

- Content-Type: `application/octet-stream`
- Body: The resulting .stl file

#### Example cURL Requests

Using JSON with SCAD content:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"scad": "cube([10, 10, 10]);", "parameters": {"width": 10, "height": 20}}' http://localhost:5000/convert --output output.stl
```

Using multipart/form-data with file upload:
```bash
curl -X POST -F "file=@path/to/your/file.scad" -F 'data={"parameters": {"width": 10, "height": 20}}' http://localhost:5000/convert --output output.stl
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Bad Request (e.g., missing file/SCAD content, invalid file type, invalid JSON)
- 500: Internal Server Error (e.g., OpenSCAD conversion failure)

## Notes

- Ensure your SCAD file uses variables in the format `$variableName` for parameters you want to customize.
- The API temporarily modifies the SCAD file to apply the provided parameters before conversion.

## Example

See the `example.py` file for a Python script demonstrating how to use the API with the `requests` library.