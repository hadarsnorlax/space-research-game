import numpy as np
import subprocess
import datetime
import json
import os
import sys

from astropy.io import fits
import matplotlib.pyplot as plt

import pythreejs as p3
from IPython.display import display
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSizePolicy

def fetch_nasa_image(ra, dec, survey='dss'):
    position = f'{ra},{dec}'
    size = '0.5,0.5'
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'outputs/output_{survey}_{timestamp}.fits'
    command = [
        'java', '-jar', 'skyview.jar',
        f'position={position}',
        f'survey={survey}',
        f'size={size}',
        f'output={output_file}'
    ]

    try:
        subprocess.run(command, check=True)
        print(f'Image successfully generated and saved as {output_file}')
        return output_file
    except Exception as err:
        print(f"Error fetching NASA images: {err}")
        return None

def view_images(output_file):
    hdul = fits.open(output_file)
    image_data = hdul[0].data
    plt.figure(figsize=(8, 8))
    plt.imshow(image_data, cmap='gray', origin='lower')
    plt.colorbar()
    plt.show()

def store_image_metadata(ra, dec, output_file, metadata_name):
    metadata = {
        'ra': ra, 
        'dec': dec, 
        'file': output_file,
    }

    data = []
    if os.path.exists(metadata_name):
        with open(metadata_name, 'r') as f:
            data = json.load(f)
    data.append(metadata)

    with open(metadata_name, 'w') as f:
        json.dump(data, f)

    return metadata_name

def fetch_and_store_images(coords, metadata_name):
    for ra, dec in coords:
        image_file = fetch_nasa_image(ra, dec)
        if image_file:
            store_image_metadata(ra, dec, image_file, metadata_name)

def create_3d_interface(metadata_filename):
    data = None
    with open(metadata_filename, 'r') as f:
        data = json.load(f)

    objects = []
    for entry in data:
        ra = entry['ra']
        dec = entry['dec']
        file = entry['file']
        x = np.cos(np.radians(dec)) * np.cos(np.radians(ra))
        y = np.cos(np.radians(dec)) * np.sin(np.radians(ra))
        z = np.sin(np.radians(dec))
        
        hdul = fits.open(file)
        image_data = hdul[0].data
        
        texture = p3.DataTexture(data=image_data, format='LuminanceFormat')
        material = p3.SpriteMaterial(map=texture)
        sprite = p3.Sprite(material=material, position=[x, y, z])
        objects.append(sprite)
    
    scene = p3.Scene(children=objects)
    camera = p3.PerspectiveCamera(position=[0, 0, 5])
    renderer = p3.Renderer(camera=camera, scene=scene, controls=[p3.OrbitControls(controlling=camera)])
    
    return renderer, camera, scene

class PyThreeJsWidget(QWidget):
    def __init__(self, scene, camera, parent=None):
        super().__init__(parent)

        # Create a layout for the widget
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Create pythreejs Renderer
        self.renderer = p3.Renderer(scene=scene, camera=camera, controls=[p3.OrbitControls(controlling=camera)])

        # Add renderer to layout
        layout.addWidget(self.renderer)


if __name__ == "__main__":
    coords = [
        (12.514, 12.393),
        (12.515, 12.394),
        (12.516, 12.395),
        (12.517, 12.396),
        (12.518, 12.397)
    ]
    # ra = 63.617
    # dec = 23.6084
    # image_name = fetch_nasa_image(ra, dec)
    # view_images(image_name)
    metadata_filename = 'metadatas/test_1_metadata.json'
    # fetch_and_store_images(coords, metadata_filename)
    renderer, camera, scene = create_3d_interface(metadata_filename)
    
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("3D Space Viewer")
    main_window.setGeometry(100, 100, 800, 600)
    pythreejs_widget = PyThreeJsWidget(scene, camera)
    main_window.setCentralWidget(pythreejs_widget)
    main_window.show()
