from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os # Для проверки существования файла

def generate_pdf(payment_schedule):
    """
    Создает PDF-документ с изображением. Тестовая реализация

    Args:
        payment_schedule: график платажей - кортеж: список словарей,
            описывающий схему выплат; итоговая стоимость покупки с учётом %

    Returns:
        PDF-документ
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Завершаем рисование
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
