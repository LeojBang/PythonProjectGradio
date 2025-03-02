import gradio as gr
from model import generate_caption, MODELS  # Импортируем MODELS для выбора


def generate_caption_interface(image, model_name):
    """
    Функция для интерфейса Gradio.
    :param image: Загруженное изображение
    :param model_name: Выбранная модель
    :return: Текстовое описание
    """
    try:
        return generate_caption(image, model_name)
    except Exception as e:
        return f"Ошибка: {str(e)}"


# Интерфейс Gradio
interface = gr.Interface(
    fn=generate_caption_interface,
    inputs=[
        gr.Image(type="pil", label="Загрузите изображение"),
        gr.Dropdown(
            choices=list(MODELS.keys()), label="Выберите модель", value="blip-base"
        ),
    ],
    outputs=gr.Textbox(label="Описание изображения"),
    title="Сервис для описания изображений",
    description="Загрузите изображение и выберите модель для генерации описания.",
)

interface.launch(server_port=7860)
