import os
import requests
from urllib.parse import urlparse
import argparse
from utils import download_image

def fetch_spacex_images(launch_id: str = "latest", save_dir: str = "images"):
    
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    photos = data.get('links', {}).get('flickr', {}).get('original', [])
    os.makedirs(save_dir, exist_ok=True)
    for i, photo in enumerate(photos, start=1):
        filename = f"spacex_{i}.jpg"
        save_path = os.path.join(save_dir, filename)
        download_image(photo, save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacex_id", type=str, default="latest", help="SpaceX launch ID")
    parser.add_argument("--dir", type=str, default="images", help="Save directory")
    args = parser.parse_args()
    
    fetch_spacex_images(args.spacex_id, args.dir)