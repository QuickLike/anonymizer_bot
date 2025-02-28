﻿# [Telegram Bot Anonymizer](https://github.com/QuickLike/anonymizer_bot)

## Технологии:

- Python
- Aiogram 3

## Anonymizer:
Telegram Bot, который позволяет отправлять сообщение в группу анонимно.

Через данного бота пользователи могут анонимно общаться, или просто присылать разные данные, которые бот будет пересылать от своего имени в группу, указанную в настройках.

Группа администраторов - группа, куда бот будет пересылать сообщения пользователей с указанием их данных.

### Запуск проекта:
Клонируйте [репозиторий](https://github.com/QuickLike/anonymizer_bot) и перейдите в него в командной строке:
```
git clone https://github.com/QuickLike/anonymizer_bot

cd anonymizer_bot
```
Создайте виртуальное окружение и активируйте его

Windows
```
python -m venv venv
.\venv\Scripts\Activate
```

Linux/Ubuntu/MacOS
```
python3 -m venv venv
source venv/bin/activate
```
Обновите pip:
```
python -m pip install --upgrade pip
```
Установите зависимости:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env, и добавьте туда переменные окружения
```
BOT_TOKEN=<токен_вашего_бота>
ADMINS_IDS=<id_администраторов_через_запятую>
ANONIM_GROUP_ID=<id_группы_куда_бот_будет_пересылать_сообщения_анонимно>
FULL_DATA_GROUP_ID=<id_группы_администраторов>
```

Запуск бота
```
python main.py
```


## Автор

[Власов Эдуард](https://github.com/QuickLike)
