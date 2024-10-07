import requests
import json

# API endpoint
url = 'http://localhost:5000/convert'

# Example 1: Using SCAD content directly
scad_content = """
$fn = 100;
difference() {
    cube([10, 10, $height]);
    translate([5, 5, -1])
        cylinder(r=$radius, h=$height+2);
}
"""

data = {
    'scad': scad_content,
    'parameters': {
        'height': 20,
        'radius': 2
    }
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open('output_from_content.stl', 'wb') as f:
        f.write(response.content)
    print("STL file saved successfully as 'output_from_content.stl'")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Example 2: Using file upload
scad_file_path = 'path/to/your/file.scad'

with open(scad_file_path, 'rb') as scad_file:
    files = {'file': ('input.scad', scad_file, 'application/x-openscad')}
    data = {
        'data': json.dumps({
            'parameters': {
                'width': 10,
                'height': 20,
                'depth': 15
            }
        })
    }
    
    response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open('output_from_file.stl', 'wb') as f:
        f.write(response.content)
    print("STL file saved successfully as 'output_from_file.stl'")
else:
    print(f"Error: {response.status_code}")
    print(response.text)