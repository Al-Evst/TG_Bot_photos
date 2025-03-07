import os
import time
import argparse
import logging
from telegram import Bot, error
from dotenv import load_dotenv
from test_util import get_photos, publish_photo

def main():
    load_dotenv()

    time_to_sleep  = 10

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

    while True:
        photos = get_photos(args.photo_dir)
        if not photos:
            logging.error("Нет доступных фото для публикации. Скрипт завершает работу.")
            break
        
        for photo in photos:
            attempts = 0
            success = False

            while attempts < 5 and not success:  
                try:
                    publish_photo(bot, chat_id, photo)
                    logging.info(f"Следующая публикация через {args.interval / 3600} часов...")
                    success = True
                    time.sleep(args.interval)
                except FileNotFoundError:
                    logging.error(f"Ошибка: Файл {photo} не найден.")
                    success = True
                    break  
                except error.TelegramError as e:
                    logging.error(f"Ошибка Telegram API при отправке фото: {e}")
                      
                except error.NetworkError as e:
                    logging.error(f"Сетевая ошибка при отправке фото: {e}")
                      
                except OSError as e:
                    logging.error(f"Ошибка при работе с файлом {photo}: {e}")  
                    break
                
                finally:
                    attempts += 1
                    if attempts < 5:
                        logging.info(f"Попытка {attempts} из 5. Повторная попытка через {time_to_sleep} секунд...")
                        time.sleep(time_to_sleep)
            
            if not success:
                logging.error(f"Не удалось отправить фото {photo} после 5 попыток. Переходим к следующему.")
                

if __name__ == "__main__":
    main()
