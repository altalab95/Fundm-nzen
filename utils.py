import os
import cv2
import numpy as np
from joblib import Parallel, delayed
from plyfile import PlyData
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

def apply_circle_crop(src, img_size=224, percentage=0.95):
	image = cv2.imread(src)
	image = cv2.resize(image, (224, 224)) 
	circle_img = np.zeros((img_size, img_size), np.uint8)
	cv2.circle(circle_img, ((int)(img_size/2),(int)(img_size/2)), int(img_size/2*percentage), 1, thickness=-1)
	image = cv2.bitwise_and(image, image, mask=circle_img)

	return image

def circle_crop_directory(src, target, img_size=224, percentage=0.95):
	
	for root, dirs, files in os.walk(src, topdown=False):
	    for name in files:
	        img = os.path.join(root, name)
	        image = apply_circle_crop(img)
	        cv2.imwrite(os.path.join(target, name), image)


def apply_grayscale(src, img_size=512):
	image = cv2.imread(src)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.resize(image, (img_size, img_size), interpolation = cv2.INTER_LINEAR)

	return image

def grayscale_directory(src, target, img_size=224):
	
	for root, dirs, files in os.walk(src, topdown=False):
	    for name in files:
	        img = os.path.join(root, name)
	        image = apply_grayscale(img)
	        cv2.imwrite(os.path.join(target, name), image)




def apply_clahe(src):

    image = cv2.imread(src)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(2, 2))
    equalized = clahe.apply(gray)

    return equalized

def clahe_directory(src, target, img_size=224):
	
	for root, dirs, files in os.walk(src, topdown=False):
	    for name in files:
	        img = os.path.join(root, name)
	        image = apply_clahe(img)
	        cv2.imwrite(os.path.join(target, name), image)



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

def apply_rof(tmp):
    target_img = tmp[0]
    output = tmp[1]
    os.system(f"python image-processing/denoise.py {target_img} 'rof' -o {output}")

def apply_denoise(src, target):
    my_list = []
    for root, dirs, files in os.walk(src, topdown=False):
        for name in files:
            target_img = os.path.join(root, name)
            output = os.path.join(target, name)
            my_list.append((target_img, output))

    results = Parallel(n_jobs=12, prefer="threads")(delayed(apply_rof)(i) for i in my_list)