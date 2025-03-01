import os
import requests
import argparse
from urllib.parse import urlparse
from utils import get_image_extension, download_image 

def fetch_nasa_apod(api_key: str, count: int, dir_save: str):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params)
    response.raise_for_status()
    images = response.json()
    os.makedirs(dir_save, exist_ok=True)
    
    for i, image_data in enumerate(images):
        if image_data.get("media_type") == "image": 
            image_url = image_data.get("hdurl") or image_data.get("url")
            ext = get_image_extension(image_url)
            image_name = os.path.join(dir_save, f"nasa_apod_{i}{ext}")
            download_image(image_url, image_name)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Skipping non-image content: {image_data.get('media_type')} - {image_data.get('url')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", type=str, required=True, help="NASA API key")
    parser.add_argument("--count", type=int, default=5, help="Number of images")
    parser.add_argument("--dir", type=str, default="images", help="Save directory")
    args = parser.parse_args()
    
    fetch_nasa_apod(args.api_key, args.count, args.dir)
