import os
import requests
from datetime import datetime
import argparse
from utils import download_image

def fetch_nasa_epic(api_key: str, count: int, output_path: str):
    
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    images = response.json()[:count]
    os.makedirs(output_path, exist_ok=True)
    for image_data in images:
        image_name = image_data["image"]
        date_str = image_data["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        date_path = date_obj.strftime("%Y/%m/%d")
        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date_path}/png/{image_name}.png"
        file_path= os.path.join(output_path, f"{image_name}.png")
        download_image(image_url, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", type=str, required=True, help="NASA API key")
    parser.add_argument("--count", type=int, default=5, help="Number of images")
    parser.add_argument("--dir", type=str, default="images", help="Save directory")
    args = parser.parse_args()
    
    fetch_nasa_epic(args.api_key, args.count, args.dir)
