from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    Blip2Processor,
    Blip2ForConditionalGeneration,
)
import logging

# Настройка логирования
logging.basicConfig(filename="logs/model.log", level=logging.ERROR)

# Словарь доступных моделей
MODELS = {
    "blip-base": {
        "path": "Salesforce/blip-image-captioning-base",
        "processor": BlipProcessor,
        "model": BlipForConditionalGeneration,
        "description": "Базовая модель BLIP для генерации описаний.",
    },
    "blip-large": {
        "path": "Salesforce/blip-image-captioning-large",
        "processor": BlipProcessor,
        "model": BlipForConditionalGeneration,
        "description": "Улучшенная модель BLIP с большим количеством параметров.",
    },
    "blip2-opt-2.7b": {
        "path": "Salesforce/blip2-opt-2.7b",
        "processor": Blip2Processor,
        "model": Blip2ForConditionalGeneration,
        "description": "Мощная модель BLIP2 с 2.7 миллиардами параметров.",
    },
}


def generate_caption(image, model_name="blip-base"):
    """
    Генерирует текстовое описание для изображения с использованием выбранной модели.
    :param image: Изображение в формате PIL.Image
    :param model_name: Название модели (по умолчанию "blip-base")
    :return: Текстовое описание
    """
    try:
        # Получаем информацию о модели
        model_info = MODELS.get(model_name)
        if not model_info:
            raise ValueError(f"Модель {model_name} не найдена")

        # Загружаем процессор и модель
        model_path = model_info["path"]
        processor_class = model_info["processor"]
        model_class = model_info["model"]
        processor = processor_class.from_pretrained(model_path)
        model = model_class.from_pretrained(model_path)

        # Генерация описания
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs, max_length=50)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error in generate_caption: {e}")
        raise
