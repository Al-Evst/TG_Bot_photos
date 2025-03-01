import os
import time
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PHOTO_DIR = os.getenv("PHOTO_DIR", "images")  
PUBLISH_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", 4 * 60 * 60))  

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("Отсутствует токен бота или ID канала в переменных окружения.")

bot = Bot(token=BOT_TOKEN)

def get_photos(photo_dir):
    
    if not os.path.exists(photo_dir):
        print(f"Директория {photo_dir} не существует.")
        return []
    
    photos = [os.path.join(photo_dir, f) for f in os.listdir(photo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not photos:
        print("Нет доступных фото для публикации.")
        return []

    random.shuffle(photos)  
    return photos

def publish_photo(photo_path):
    
    try:
        bot.send_photo(chat_id=CHAT_ID, photo=open(photo_path, 'rb'))
        print(f"Фото {photo_path} успешно опубликовано в {CHAT_ID}")
        os.remove(photo_path)  
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Публикация всех фото из директории в бесконечном цикле")
    parser.add_argument("--photo_dir", default=PHOTO_DIR, help="Директория с фотографиями")
    parser.add_argument("--interval", type=int, default=PUBLISH_INTERVAL, help="Интервал публикации в секундах")
    args = parser.parse_args()

    print(f"Автоматическая публикация фотографий запущена... Интервал: {args.interval / 3600} часов.")

    while True:
        photos = get_photos(args.photo_dir) 
        for photo in photos:
            publish_photo(photo)
            print(f"Следующая публикация через {args.interval / 3600} часов...")
            time.sleep(args.interval)
