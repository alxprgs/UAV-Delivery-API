# UAV-Delivery-API

API для управления и отслеживания доставки с помощью беспилотных летательных аппаратов (БПЛА).

## Возможности

- Управление заказами на доставку
- Отслеживание статуса дронов и заказов
- Интеграция с внешними сервисами

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-org/UAV-Delivery-API.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd UAV-Delivery-API
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск

Для запуска в режиме разработки:
```
python run.py
```
или
```
uvicorn server:app --reload --host 0.0.0.0 --port 5005
```

Для запуска в production-режиме:
```
uvicorn server:app --host 0.0.0.0 --port 5005 --workers 4
```
или используйте Docker:
```
docker build -t uav-delivery-api .
docker run -p 5005:5005 --env-file .env uav-delivery-api
```

## Конфигурация

Создайте файл `.env` на основе `.env.example` и укажите необходимые переменные окружения.

## Документация API

Документация доступна по адресу: `/` после запуска сервера.

## Вклад

PR и предложения приветствуются!

## Лицензия

Apache 2.0 License
