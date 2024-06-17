import os
import requests
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")
BASE_URL = "https://images-api.nasa.gov"
headers = {
    "User-Agent": "Mozilla/5.0",
}
# telescope_keywords = ['Hubble', 'Spitzer', 'Chandra', 'James Webb', 'Kepler']

def fetch_nasa_images(query):
    url = f"{BASE_URL}/search"
    telescope_images_query = f"Hubble"
    params = {
        "media_type": "image",
        "q": telescope_images_query,
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        image_urls = []
        for item in data["collection"]["items"]:
            image_urls.append(item["links"][0]["href"])
        
        return image_urls
    except Exception as err:
        print(f"Error fetching NASA images: {err}")
        return []

if __name__ == "__main__":
    query = ""
    image_urls = fetch_nasa_images(query)

    if image_urls:
        print(f"Found {len(image_urls)} images related to '{query}':")
        for url in image_urls:
            print(url)
    else:
        print(f"No images found for '{query}'")
