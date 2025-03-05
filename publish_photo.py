import os
import random
import argparse
import sys
from telegram import Bot, error
from dotenv import load_dotenv
from utils import get_photos, publish_photo  

def main():
    load_dotenv()  

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    PHOTO_DIR = os.getenv("PHOTO_DIR", "images")

    if not BOT_TOKEN or not CHAT_ID:
        print("Ошибка: Отсутствует токен бота или ID канала в переменных окружения.", file=sys.stderr)
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN)

    def publish_random_photo(photo_path=None):
        photos = get_photos(PHOTO_DIR)
        if not photos:
            return None

        if not photo_path:
            photo_path = random.choice(photos)

        return photo_path

    parser = argparse.ArgumentParser(description="Публикация фото в Telegram-канал")
    parser.add_argument("--photo", type=str, help="Путь к фото для публикации")
    args = parser.parse_args()

    try:
        photo_path = publish_random_photo(args.photo)
        if not photo_path:
            print("Ошибка: Нет фото для публикации.", file=sys.stderr)
            return

        publish_photo(bot, CHAT_ID, photo_path)  

    except FileNotFoundError:
        print(f"Ошибка: Файл {photo_path} не найден.", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"Ошибка: Ошибка доступа к файлу {photo_path}. Проверьте права доступа.", file=sys.stderr)
        sys.exit(3)
    except error.NetworkError:
        print(f"Ошибка: Ошибка сети при отправке фото.", file=sys.stderr)
        sys.exit(4)
    except error.Unauthorized:
        print("Ошибка: Неавторизованный доступ к Telegram API. Проверьте токен.", file=sys.stderr)
        sys.exit(5)

if __name__ == "__main__":
    main()
