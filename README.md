# Сервис для описания изображений

Этот сервис позволяет загружать изображения и получать их текстовое описание с использованием предобученных моделей. Также поддерживается сохранение истории запросов в базу данных PostgreSQL.

## Возможности

- Генерация текстового описания для изображений.
- Поддержка нескольких моделей (BLIP Base, BLIP Large, BLIP2).
- Сохранение истории запросов в базу данных.
- Просмотр истории запросов через API.
- Запуск через Docker Compose.

## Установка

### Требования

- Docker и Docker Compose.
- Python 3.10 (если запуск без Docker).

### Запуск с Docker Compose

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/LeojBang/PythonProjectGradio.git
   cd image-captioning-service
   
2. Создайте файл .env в корне проекта:
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=image_captioning
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your_password

3. Запустите проект:
   ```bash
   docker-compose up --build
   
4. Сервис будет доступен по адресу http://localhost:8000.

### Использование
## API
- Генерация описания:
   Отправьте POST-запрос на /describe/ с изображением и выберите модель.
   Пример запроса через Swagger UI: http://localhost:8000/docs.
- Просмотр истории:
   Отправьте GET-запрос на /history/.
   Пример ответа:
````json
{
  "requests": [
    {
      "id": 1,
      "timestamp": "2024-10-01T12:34:56",
      "model_name": "blip-base",
      "description": "A cat sitting on a couch."
    }
  ]
}
````
## Дополнительные возможности

- Выбор модели: Выберите модель через параметр model_name в запросе.
- Фильтрация истории: Добавьте параметр model_name в запрос к /history/ для фильтрации.

## Структура проекта
````
PythonProjectGradio/
├── app/
│   ├── __init__.py
│   ├── api.py              # Основной файл FastAPI
│   ├── app.py              # Основной файл Gradio
│   ├── models.py            # Модели для генерации описаний
│   ├── database.py          # Логика работы с базой данных
│   └── config.py            # Конфигурация приложения
├── logs/                    # Логи приложения
├── requirements.txt         # Зависимости
├── Dockerfile               # Dockerfile для контейнеризации
├── docker-compose.yml       # Docker Compose для запуска PostgreSQL и приложения
└── README.md                # Документация
```
