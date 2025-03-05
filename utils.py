import os
import requests
import argparse
import random
from urllib.parse import urlparse
from telegram import Bot, error

def get_image_extension(url: str) -> str:
    
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    _, ext = os.path.splitext(filename)
    return ext if ext else ".jpg"

def download_image(url: str, file_path: str):
    
    os.makedirs(os.path.dirname( file_path), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    
    with open( file_path, 'wb') as file:
        file.write(response.content)

def get_photos(photo_dir: str):
    
    if not os.path.exists(photo_dir):
        print(f"Ошибка: Директория {photo_dir} не существует.")
        return []
    
    photos = [os.path.join(photo_dir, f) for f in os.listdir(photo_dir) 
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not photos:
        print("Ошибка: Нет доступных фото для публикации.")
        return []

    return photos

def publish_photo(bot: Bot, chat_id: str, photo_path: str):
    
    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id=chat_id, photo=photo_file)
        print(f"Фото {photo_path} успешно опубликовано в {chat_id}")
    except FileNotFoundError:
        print(f"Ошибка: Файл {photo_path} не найден.")
    except error.TelegramError as e:
        print(f"Ошибка Telegram API при отправке фото: {e}")
    except OSError as e:
        print(f"Ошибка при работе с файлом {photo_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание изображения по ссылке")
    parser.add_argument("url", type=str, help="Ссылка на изображение")
    parser.add_argument("--output", type=str, default=None,
                        help="Путь сохранения файла (по умолчанию - имя из ссылки)")
    args = parser.parse_args()
    
    if not args.output:
        ext = get_image_extension(args.url)
        filename = os.path.basename(urlparse(args.url).path) or f"downloaded_image{ext}"
        args.output = os.path.join(os.getcwd(), filename)
    
    download_image(args.url, args.output)
