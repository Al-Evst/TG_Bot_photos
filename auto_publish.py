import os
import time
import argparse
from telegram import Bot, error
from dotenv import load_dotenv
from utils import get_photos, publish_photo 

def main():
    load_dotenv()

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    PHOTO_DIR = os.getenv("PHOTO_DIR", "images")  
    PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", 4 * 60 * 60))  

    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Отсутствует токен бота или ID канала в переменных окружения.")

    bot = Bot(token=BOT_TOKEN)

    parser = argparse.ArgumentParser(description="Публикация всех фото из директории в бесконечном цикле")
    parser.add_argument("--photo_dir", default=PHOTO_DIR, help="Директория с фотографиями")
    parser.add_argument("--interval", type=int, default=PUBLISH_INTERVAL, help="Интервал публикации в секундах")
    args = parser.parse_args()

    print(f"Автоматическая публикация фотографий запущена... Интервал: {args.interval / 3600} часов.")

    while True:
        photos = get_photos(args.photo_dir)  
        for photo in photos:
            publish_photo(bot, CHAT_ID, photo)  
            print(f"Следующая публикация через {args.interval / 3600} часов...")
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
