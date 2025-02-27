import os
import requests
import argparse
from urllib.parse import urlparse

def get_image_extension(url: str) -> str:
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    _, ext = os.path.splitext(filename)
    return ext if ext else ".jpg"

def download_image(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Файл сохранен в: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание изображения по ссылке")
    parser.add_argument("url", type=str, help="Ссылка на изображение")
    parser.add_argument("--output", type=str, default=None, help="Путь сохранения файла (по умолчанию - текущее имя из ссылки)")
    args = parser.parse_args()
    
    if not args.output:
        ext = get_image_extension(args.url)
        filename = os.path.basename(urlparse(args.url).path) or f"downloaded_image{ext}"
        args.output = os.path.join(os.getcwd(), filename)
    
    download_image(args.url, args.output)
