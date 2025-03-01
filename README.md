# Загрузчик фото NASA & SpaceX Image  + Telegram Auto Publisher #

Этот проект включает несколько скриптов для загрузки изображений из NASA (APOD, EPIC) и SpaceX, а также автоматическую публикацию их в Telegram-канале.

## Установка ##

Создайте виртуальное окружение и установите зависимости:

```
pip install -r requirements.txt
```


Создайте ```.env``` файл и добавьте в него параметры окружения:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token;
TELEGRAM_CHAT_ID=your_chat_id;
PHOTO_DIR=images;
PUBLISH_INTERVAL=14400  # Интервал публикации (в секундах).
```

## Запуск скриптов ##

1. Загрузка изображений NASA APOD

Скрипт загружает изображения с сервиса "Astronomy Picture of the Day".

```
python fetch_nasa_apod.py --api_key YOUR_NASA_API_KEY --count 5 --dir images
```

2. Загрузка изображений NASA EPIC

Скрипт загружает изображения Земли с NASA EPIC.

```
python fetch_nasa_epic.py --api_key YOUR_NASA_API_KEY --count 5 --dir images
```

3. Загрузка изображений SpaceX

Скрипт загружает изображения с последнего запуска SpaceX.

```
python fetch_spacex_images.py --spacex_id latest --dir images
```

4. Публикация одного изображения в Telegram

Скрипт публикует одно изображение в Telegram-канал.

```
python publish_photo.py --photo path/to/photo.jpg
```

Если параметр ```--photo``` не указан, будет выбрано случайное изображение из ```PHOTO_DIR```.

5. Автопубликация всех изображений в Telegram

Скрипт публикует все изображения в бесконечном цикле с заданным интервалом.

```
python auto_publish.py --photo_dir images --interval 14400
```

6. Скачивание изображения по ссылке

Скрипт скачивает изображение по указанному URL.

```
python download_image.py "https://example.com/image.jpg" --output my_image.jpg
```

Если ```--output``` не указан, файл будет сохранен с оригинальным именем из ссылки.


