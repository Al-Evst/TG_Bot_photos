import os
import random
import argparse
import sys
import logging
from telegram import Bot, error
from dotenv import load_dotenv
from utils import get_photos, publish_photo  

def publish_random_photo(photo_dir, photo_path=None):
    photos = get_photos(photo_dir)
    if not photos:
        return None
    return photo_path if photo_path else random.choice(photos)

def main():
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()

    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    photo_dir = os.getenv("PHOTO_DIR", "images")
    
    if not bot_token or not chat_id:
        logger.error("Отсутствует токен бота или ID канала в переменных окружения.")
        sys.exit(1)
    
    bot = Bot(token=bot_token)
    
    parser = argparse.ArgumentParser(description="Публикация фото в Telegram-канал")
    parser.add_argument("--photo", type=str, help="Путь к фото для публикации")
    args = parser.parse_args()
    
    try:
        photo_path = publish_random_photo(photo_dir, args.photo)
        
        if not photo_path:
            logger.error("Нет фото для публикации.")
            return
        
        publish_photo(bot, chat_id, photo_path)  
    
    except FileNotFoundError:
        logger.error(f"Файл {photo_path} не найден.")
        sys.exit(2)
    except PermissionError:
        logger.error(f"Ошибка доступа к файлу {photo_path}. Проверьте права доступа.")
        sys.exit(3)
    except error.NetworkError:
        logger.error("Ошибка сети при отправке фото.")
        sys.exit(4)
    except error.Unauthorized:
        logger.error("Неавторизованный доступ к Telegram API. Проверьте токен.")
        sys.exit(5)

if __name__ == "__main__":
    main()
