import json

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from PIL import Image
import io

from .database import init_db, save_request, get_requests
from .model import generate_caption, MODELS  # Импортируем MODELS для выбора
import logging

# Настройка логирования
logging.basicConfig(filename="logs/app.log", level=logging.ERROR)
# Инициализация базы данных при запуске приложения
init_db()
app = FastAPI()


@app.post("/describe/")
async def describe_image(
        file: UploadFile = File(..., description="Загрузите изображение"),
        model_name: str = Query(
            default="blip-base",
            description="Выберите модель",
            enum=list(MODELS.keys()),  # Ограничиваем выбор моделей из MODELS
        ),
):
    """
    Генерация текстового описания для изображения.
    - **file**: Изображение для обработки.
    - **model_name**: Выберите модель из списка.
    """
    try:
        # Чтение изображения
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Генерация описания с использованием выбранной модели
        caption = generate_caption(image, model_name)
        # Сохранение запроса в базу данных

        save_request(model_name, caption)

        return JSONResponse(content={"description": caption})
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/history/")
def get_history():
    """
    Возвращает историю запросов.
    """
    try:
        requests = get_requests()
        return JSONResponse(content={"requests": requests})
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/models/")
def get_models():
    """
    Возвращает список доступных моделей и их описания.
    """
    models_info = {
        "models": {
            "blip-base": "Базовая модель BLIP для генерации описаний.",
            "blip-large": "Улучшенная модель BLIP с большим количеством параметров.",
            "blip2-opt-2.7b": "Мощная модель BLIP2 с 2.7 миллиардами параметров."
        }
    }
    # Преобразуем в JSON-строку
    json_response = json.dumps(models_info, ensure_ascii=False)
    return Response(
        content=json_response,
        media_type="application/json; charset=utf-8"  # Указываем кодировку
    )
