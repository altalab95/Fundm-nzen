import base64
import os

import numpy as np
from plyfile import PlyData
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image


def read_features(fileName: Path) -> np.ndarray:
    # Read the PLY file
    data = PlyData.read(fileName)

    x = np.asarray([x[0] for x in data['vertex'].data.tolist()])
    y = np.asarray([x[1] for x in data['vertex'].data.tolist()])
    f = np.asarray([x[-1] for x in data['vertex'].data.tolist()])
    x, ix = np.unique(x, return_inverse=True)
    y, iy = np.unique(y, return_inverse=True)
    rows = y.size
    cols = x.size
    n = f.shape[1]
    idx = ix + iy * cols
    feat = np.empty((rows * cols, n))
    feat.fill(np.nan)
    feat[idx, :] = f
    feat = np.reshape(feat, (rows, cols, n))
    feat = np.flip(feat, axis=0)
    return feat

def image_to_base64_blob(filename):

    try:
        with open(filename, "rb") as img_file:
            img_byte_arr = img_file.read()
            encoded_string = base64.b64encode(img_byte_arr).decode('utf-8')
            blob_url = f"data:image/png;base64,{encoded_string}"  # Change to PNG
            return blob_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def convert_tif_to_jpg(source_dir, target_dir):
    """
    Convert all .tif files in the source directory to .jpg format
    and save them in the target directory.
r: Directory to save converted .
    :param source_dir: Directory containing .tif files
    :param target_dijpg files
    """
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith('.tif'):
            # Construct full file path
            tif_file_path = os.path.join(source_dir, filename)
            # Open the .tif file
            with Image.open(tif_file_path) as img:
                # Convert to .jpg
                jpg_file_path = os.path.join(target_dir, f"{os.path.splitext(filename)[0]}.jpg")
                img.convert('RGB').save(jpg_file_path, 'JPEG')


def find_nearest_image(df, target_image):
    """
    Find the nearest image to the target image based on Euclidean distance.

    Parameters:
    df (pd.DataFrame): DataFrame containing image data.
    target_image (str): The image to find the nearest value for.

    Returns:
    str: The nearest image to the target image.
    """
    # Get the row corresponding to the target image
    target_row = df[df.iloc[:, 0] == target_image].iloc[:, 1:].values.flatten()

    # Initialize variables to find the nearest image
    nearest_image = None
    nearest_distance = float('inf')

    # Iterate through each image in the DataFrame
    for index, row in df.iterrows():
        current_image = row[0]
        if current_image == target_image:
            continue  # Skip the target image itself

        # Get the current image values
        current_row = row[1:].values.flatten()

        # Calculate the distance (Euclidean distance in this case)
        distance = np.linalg.norm(target_row - current_row)

        # Update nearest image if the current distance is smaller
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_image = current_image

    return nearest_image ,nearest_distance