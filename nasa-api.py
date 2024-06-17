import requests

BASE_URL = "https://skyview.gsfc.nasa.gov/current/cgi/query.pl"

def fetch_nasa_images(ra, dec, survey='DSS', width=0.5, height=0.5):
    """
    Parameters:
    ra (float): Right Ascension of the target location.
    dec (float): Declination of the target location.
    survey (str): type of the image (default is 'DSS') - DSS/SDSS/2MASS/WISE.
    width (float): Width of the image in degrees (default is 0.5).
    height (float): Height of the image in degrees (default is 0.5).
    """
    params = {
        "Position": f"{ra},{dec}",
        "Survey": survey,
        "Coordinates": "J2000",
        "Return": "URL",
        "Scaling": "Log",
        "Sampler": "Clip",
        "Size": f"{width},{height}",
        "pixels": "300,300"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.text.strip()
    except Exception as err:
        print(f"Error fetching NASA images: {err}")
        return []

if __name__ == "__main__":
    # Coordinates for the center of the Orion Nebula
    ra = 83.8221
    dec = -5.3911
    image_url = fetch_nasa_images(ra, dec)

    if image_url:
        print(f"Image URL: {image_url}")
    else:
        print("Failed to retrieve the image.")
