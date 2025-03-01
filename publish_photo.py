import os
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv

def get_photos(photo_dir):
    if not os.path.exists(photo_dir):
        return []
    
    try:
        photos = [os.path.join(photo_dir, f) for f in os.listdir(photo_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    except OSError:
        return []
    
    return photos

def publish_photo(bot_token, chat_id, photo_dir, photo_path=None):
    try:
        bot = Bot(token=bot_token)
    except Exception:
        return
    
    photos = get_photos(photo_dir)
    if not photos:
        return
    
    if not photo_path:
        photo_path = random.choice(photos)
    
    try:
        with open(photo_path, 'rb') as photo:
            try:
                bot.send_photo(chat_id=chat_id, photo=photo)
            except Exception:
                pass
    except (FileNotFoundError, IOError):
        pass

if __name__ == "__main__":
    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    photo_dir = os.getenv("PHOTO_DIR", "images")  

    if not bot_token or not chat_id:
        raise ValueError("Отсутствует токен бота или ID канала в переменных окружения.")
    
    parser = argparse.ArgumentParser(description="Публикация фото в Telegram-канал")
    parser.add_argument("--photo", type=str, help="Путь к фото для публикации")
    args = parser.parse_args()
    
    publish_photo(bot_token, chat_id, photo_dir, args.photo)
