import os
import requests
from urllib.parse import urlparse
import argparse
from utils import download_image

def fetch_spacex_images(launch_id: str = "latest", output_path: str = "images"):
    
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    photos = data.get('links', {}).get('flickr', {}).get('original', [])
    os.makedirs(output_path, exist_ok=True)
    for i, photo in enumerate(photos, start=1):
        filename = f"spacex_{i}.jpg"
        path_save = os.path.join(output_path, filename)
        download_image(photo, path_save)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacex_id", type=str, default="latest", help="SpaceX launch ID")
    parser.add_argument("--dir", type=str, default="images", help="Save directory")
    args = parser.parse_args()
    
    fetch_spacex_images(args.spacex_id, args.dir)
