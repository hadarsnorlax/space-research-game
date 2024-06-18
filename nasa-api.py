import subprocess
import datetime

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def fetch_nasa_image(ra, dec, survey='dss'):
    position = f'{ra},{dec}'
    size = '2.0,2.0'
    output_file = f'output_{survey}_{timestamp}.fits'
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
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

def enhance_galaxies(image_data):
    smoothed_image = gaussian_filter(image_data, sigma=3.0)
    # Subtract the smoothed image from the original to enhance galaxies
    galaxy_enhanced = image_data - smoothed_image
    # Apply logarithmic scaling to enhance faint features
    galaxy_enhanced = np.log10(galaxy_enhanced + 1.0) # Adding 1 to avoid log(0)
    # Normalize to range [0, 1]
    galaxy_enhanced = (galaxy_enhanced - np.min(galaxy_enhanced)) / (np.max(galaxy_enhanced) - np.min(galaxy_enhanced))
    return galaxy_enhanced

def view_images():
    hdul = fits.open('output.fits')
    image_data = hdul[0].data
    # image_data = enhance_galaxies(image_data)
    plt.figure(figsize=(8, 8))
    plt.imshow(image_data, cmap='gray', origin='lower')
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    ra = 12.514
    dec = 12.393
    fetch_nasa_image(ra, dec)
    view_images()