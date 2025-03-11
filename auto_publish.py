import os
import time
import argparse
import logging
from telegram import Bot, error
from dotenv import load_dotenv
from utils import get_photos, publish_photo

def publish_all_photos(bot, chat_id, photo_dir, interval, max_attempts=5, retry_delay=10):
    photos = get_photos(photo_dir)
    if not photos:
        raise ValueError("Нет доступных фото для публикации.")
       

    for photo in photos:
        attempts = 0
        while attempts < max_attempts:
            try:
                publish_photo(bot, chat_id, photo)
                logging.info(f"Фото {photo} отправлено. Следующая публикация через {interval / 3600} часов.")
                time.sleep(interval)
                break
            except FileNotFoundError:
                logging.error(f"Файл {photo} не найден, пропускаем.")
                break
            except (error.TelegramError, error.NetworkError, OSError) as e:
                logging.error(f"Ошибка при отправке {photo}: {e}")
                attempts += 1
                if attempts < max_attempts:
                    logging.info(f"Попытка {attempts} из {max_attempts}. Повтор через {retry_delay} секунд...")
                    time.sleep(retry_delay)
        else:
            logging.error(f"Не удалось отправить {photo} после {max_attempts} попыток.")

def main():
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    photo_dir = os.getenv("PHOTO_DIR", "images")  
    publish_interval = int(os.getenv("PUBLISH_INTERVAL", 4 * 60 * 60))  

    if not bot_token or not chat_id:
        raise ValueError("Отсутствует токен бота или ID канала в переменных окружения.")

    bot = Bot(token=bot_token)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser(description="Публикация всех фото из директории с проверками")
    parser.add_argument("--photo_dir", default=photo_dir, help="Директория с фотографиями")
    parser.add_argument("--interval", type=int, default=publish_interval, help="Интервал публикации в секундах")
    args = parser.parse_args()

    logging.info(f"Автоматическая публикация фотографий запущена... Интервал: {args.interval / 3600} часов.")
    publish_all_photos(bot, chat_id, args.photo_dir, args.interval)

if __name__ == "__main__":
    main()
