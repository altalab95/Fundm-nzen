import base64
import json
import os
import re  # Import the re module for regular expressions
import io
from pathlib import Path

import pandas as pd

from matcher import extract_matches_in_directory, detect_keypoints_and_match, visualise_matches
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template, send_file
from matplotlib import pyplot as plt

from functions import read_features, image_to_base64_blob, convert_tif_to_jpg, find_nearest_image
from utils import grayscale_directory, clahe_directory, circle_crop_directory, apply_denoise
import shutil

app = Flask(__name__)

# Store data temporarily for demonstration purposes
data_store = {}
image_dir = 'images'
IMAGE_FOLDER = 'grayimgs'
os.makedirs(image_dir, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
target_directory = "output/"#"directory_to_create_output/"
exp1 = target_directory+"grayscale/"
exp2 = target_directory+"Filter1/"
exp3 = target_directory+"Filter2/"
exp4 = target_directory+"Filter3/"
exp5= target_directory+"Filter4/"
folders = [exp1, exp2, exp3, exp4, exp5]

if not os.path.exists(target_directory):
    os.mkdir(target_directory)
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)



data_selected = {
    "normal": None,
    "albedo": None,
    "mesh": None ,
    "katlog" : None ,
    "grayscale" : None
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload_folder', methods=['POST'])
def upload_folder():
    # Get the uploaded files
    files = request.files.getlist('files[]')

    json_files = []
    kenom_list = []
    identifier_map = {}  # To map identifiers to kenom values

    for file in files:
        # Sanitize the filename to remove invalid characters
        sanitized_filename = re.sub(r'[<>:"/\\|?*]', '_', file.filename)

        # Save TIFF files to the 'images' directory
        if sanitized_filename.endswith('.tif') or sanitized_filename.endswith('.ply'):
            file.save(os.path.join(image_dir, sanitized_filename))
        elif sanitized_filename.endswith('.json'):
            json_files.append(sanitized_filename)
            # Read the JSON content
            file_content = json.load(file.stream)
            # Extract the 'kenom' and 'identifier' values
            kenom = file_content.get('kenom')
            identifier = file_content.get('identifier')
            kenom_list.append(kenom)
            identifier_map[identifier] = kenom  # Map identifier to kenom

    # Store the JSON file names, kenom values, and identifier map in the data_store
    data_store['json_files'] = json_files
    data_store['kenom_list'] = kenom_list
    data_store['identifier_map'] = identifier_map

    return jsonify({"message": "Folder uploaded", "kenom_list": kenom_list, "identifier_map": identifier_map})


@app.route('/api/get_images/<kenom>', methods=['GET'])
def get_images(kenom):
    # Assuming images are stored in a directory named 'images'
    imagesdetlies = {
        "imagenormal": None,
        "imagealbedo": None,
        "mesh": None
    }
    data_selected['katlog'] = kenom
    images = []
    print(kenom)
    kenom = re.sub(r'[<>:"/\\|?*]', '_', kenom)
    print(kenom)
    # List all files in the image directory
    for filename in os.listdir(image_dir):
        if (filename.endswith('.tif') or filename.endswith('.ply')) and kenom in filename:
            if filename.endswith('.tif'):
                with Image.open(os.path.join(image_dir, filename)) as img:
                    # Convert TIFF to PNG
                    img = img.convert("RGB")  # Convert to RGB if necessary
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')  # Save as PNG
                    img_byte_arr.seek(0)
                    encoded_string = base64.b64encode(img_byte_arr.read()).decode('utf-8')
                    blob_url = f"data:image/png;base64,{encoded_string}"  # Change to PNG
                    images.append(blob_url)
                    if 'normal' in filename:
                        data_selected['normal'] = filename
                        imagesdetlies["imagenormal"] = blob_url
                    elif 'albedo' in filename:
                        data_selected['albedo'] = filename
                        imagesdetlies["imagealbedo"] = blob_url
            elif filename.endswith('.ply') and 'mesh' in filename:
                data_selected['mesh'] = filename
                print(data_selected['mesh'] )
                with open(os.path.join(image_dir, filename), "rb") as mesh_file:
                    encoded_mesh = base64.b64encode(mesh_file.read()).decode('utf-8')
                    imagesdetlies["mesh"] = f"data:application/octet-stream;base64,{encoded_mesh}"
    return jsonify({"images": images, "imgs": imagesdetlies})

@app.route('/preview_grayscale', methods=['POST'])
def preview_grayscale():
    method = request.form.get('method')
    image_data = request.form.get('image')

    # Decode the base64 image
    image_data = image_data.split(",")[1]  # Remove the prefix
    image_bytes = base64.b64decode(image_data)
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Apply the selected grayscale method
    if method == 'Weighted Average':
        grayscale_img = img.convert('L')  # Weighted Average Grayscale
    elif method == 'Average':
        r, g, b = img.split()
        grayscale_img = Image.fromarray(np.uint8((np.array(r) + np.array(g) + np.array(b)) / 3))
    elif method == 'Lightness':
        r, g, b = img.split()
        grayscale_img = Image.fromarray(np.uint8((np.maximum(np.array(r), np.array(g), np.array(b)) + np.minimum(
            np.array(r), np.array(g), np.array(b))) / 2))
    elif method == 'Luminosity':
        r, g, b = img.split()
        grayscale_img = Image.fromarray(np.uint8(0.21 * np.array(r) + 0.72 * np.array(g) + 0.07 * np.array(b)))
    elif method == 'Inverted':
        grayscale_img = img.convert('L')
        grayscale_img = Image.fromarray(255 - np.array(grayscale_img))
    else:
        return jsonify({'error': 'Invalid method'})
    data_array = np.array(grayscale_img).tolist()
    # Convert the grayscale image to PNG and encode it in base64
    img_byte_arr = io.BytesIO()
    grayscale_img.save(img_byte_arr, format='PNG')  # Save as PNG
    img_byte_arr.seek(0)
    encoded_string = base64.b64encode(img_byte_arr.read()).decode('utf-8')
    blob_url = f"data:image/png;base64,{encoded_string}"
    return jsonify({'preview_url': blob_url })


@app.route('/comparefeatures', methods=['GET'])
def comparefeatures():
    convert_tif_to_jpg(image_dir,IMAGE_FOLDER)
    grayscale_directory(IMAGE_FOLDER,exp1)
    clahe_directory(exp1, exp3)
    circle_crop_directory(exp3, exp5)

    df = extract_matches_in_directory(exp5)
    df.head(5)
    print(df)
    df.to_csv("table_with_matches.csv")

    srfile = os.path.splitext(data_selected['normal'])[0] + '.jpg'

    dff = pd.read_csv('table_with_matches.csv')

    nearest_image ,nearest_distance   =find_nearest_image(dff ,srfile)
    print(nearest_image)
    print(nearest_distance)
    path1 = "output/Filter4/" + srfile
    path2 = "output/Filter4/"  + nearest_image
    matches, img1, kp1, img2, kp2 = detect_keypoints_and_match(path1, path2)
    result =  visualise_matches(img1, kp1, img2, kp2, matches)
    image_base64 = image_to_base64_blob(result)

    # Return the image
    return jsonify({'srcimg':  srfile , 'nearimg' :  nearest_image  , 'distance'  :  nearest_distance  , 'image' : image_base64 })


@app.route('/api/clear_folders', methods=['POST'])
def clear_folders():
    # List of directories to remove
    directories_to_remove = [image_dir, IMAGE_FOLDER, target_directory, exp1, exp2, exp3, exp4, exp5]

    for directory in directories_to_remove:
        if os.path.exists(directory):
            try:
                # Remove the directory and its contents
                shutil.rmtree(directory)
                print(f"Successfully removed directory: {directory}")
            except Exception as e:
                print(f'Failed to remove {directory}. Reason: {e}')

    return jsonify({"message": "All folders and their contents removed successfully"})

if __name__ == '__main__':
    app.run(debug=True)
