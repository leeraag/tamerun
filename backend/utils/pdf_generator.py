from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch # Единицы измерения (для удобства)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, \
    SimpleDocTemplate, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import LongTable
from io import BytesIO
import os # Для проверки существования файла

from utils.calculator import get_date_formatted

IMAGE_HEIGHT_TARGET = 0.9 * inch
LOGO_PATH = './src/images/logo.webp'  # Укажите путь к вашему файлу изображения

try:
    pdfmetrics.registerFont(TTFont('Stolzl-Regular', './src/fonts/Stolzl-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Stolzl-Book', './src/fonts/Stolzl-Book.ttf'))
except Exception as e:
    print(f"Ошибка при регистрации шрифтов: {e}. Используются стандартные шрифты.")
    # Если шрифты не найдены, ReportLab по умолчанию использует Helvetica
    font_regular = 'Helvetica'
    font_book = 'Helvetica'
else:
    font_regular = 'Stolzl-Regular'
    font_book = 'Stolzl-Book'

def generate_pdf(payment_schedule, property_price, installment_period, apartment_number):
    """
    Создает PDF-документ с изображением. Тестовая реализация

    Args:
        payment_schedule (list): Список словарей с данными о платежах.
            Каждый словарь должен содержать ключи:
            'month', 'date', 'amount', 'note'
        property_price (float): Стоимость квартиры
        installment_period (int): Количество месяцев рассрочки
        apartment_number (int): Номер апартаментов

    Returns:
        PDF-документ
    """
    buffer = BytesIO()
    # Отступы страницы: верхний и нижний должны быть достаточно большими,
    # чтобы вместить самую "большую" шапку/сноску.
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=1.7 * inch,
                            bottomMargin=2.0 * inch)
    story = []

    styles = getSampleStyleSheet()
    width, height = doc.pagesize
    available_width_for_images = width - 2 * inch

    # --- Определяем тексты ---
    title_text = f"Расчет графика платежей за Апартаменты № {apartment_number} Tamerun Grand Mirmax по рассрочке на {installment_period} месяцев*"
    current_time_t =  datetime.now() + timedelta(hours=3)
    current_date = current_time_t.strftime("%d.%m.%Y %H:%M:%S")
    date_text = f"Дата расчета: {current_date}"
    cost_text = f"Стоимость квартиры: {property_price:,.2f} руб."
    footnote_text = "*Предложение действительно в течение 30 дней с даты расчета и не является публичной офертой."

    # --- Стили ---
    title_style = ParagraphStyle(
        name='TitleStyle', fontName=font_regular, fontSize=14, leading=18,
        alignment=TA_CENTER,
    )
    info_style = ParagraphStyle(
        name='InfoStyle', fontName=font_book, fontSize=10, leading=12,
        alignment=TA_LEFT,
    )
    footer_text_style = ParagraphStyle(
        name='FooterTextStyle', fontName=font_book, fontSize=8, leading=10,
        alignment=TA_LEFT,
    )
    note_style = ParagraphStyle(
        name='NoteStyle',
        parent=styles['Normal'],
        fontName=font_book,
    )

    # --- Общая функция для отрисовки шапки и сноски ---
    # Эта функция будет вызываться из page_callback_first и page_callback_later
    # с разными значениями отступов.
    def render_header_and_footer(canvas, doc, y_offset_top_content,
                                 y_offset_bottom_content):
        canvas.saveState()

        # Отрисовка шапки
        header_y_start = height - y_offset_top_content  # Y-координата для начала отрисовки шапки

        # Заголовок
        title_paragraph = Paragraph(title_text, title_style)
        title_w, title_h = title_paragraph.wrapOn(canvas, width - 2 * inch,
                                                  height)
        title_paragraph.drawOn(canvas, inch, header_y_start - title_h)

        # Дата расчета
        date_paragraph = Paragraph(date_text, info_style)
        date_w, date_h = date_paragraph.wrapOn(canvas, width - 2 * inch,
                                               height)
        date_paragraph.drawOn(canvas, inch,
                              header_y_start - title_h - date_h - 0.2 * inch)

        # Стоимость квартиры
        cost_paragraph = Paragraph(cost_text, info_style)
        cost_w, cost_h = cost_paragraph.wrapOn(canvas, width - 2 * inch,
                                               height)
        cost_paragraph.drawOn(canvas, inch,
                              header_y_start - title_h - date_h - 0.2 * inch - cost_h - 0.05 * inch)

        # --- Отрисовка сноски с ОДНИМ изображением ---
        footer_y_start = y_offset_bottom_content

        # Подготовка текста сноски
        footer_paragraph = Paragraph(footnote_text, footer_text_style)
        footer_text_w, footer_text_h = footer_paragraph.wrapOn(canvas,
                                                               width - 2 * inch,
                                                               height)
        # --- Подготовка ОДНОГО изображения ---
        single_image_element = None
        try:
            img_reader = ImageReader(LOGO_PATH)
            img_width_orig, img_height_orig = img_reader.getSize()

            # Рассчитываем новую ширину, чтобы она заняла всю доступную ширину
            new_width = available_width_for_images

            # Рассчитываем новую высоту пропорционально, сохраняя исходное соотношение сторон
            # Используем новое соотношение сторон, чтобы новая высота была пропорциональна новой ширине
            new_height = img_height_orig * (new_width / img_width_orig)

            # Если задана целевая высота, можно использовать ее как максимум,
            # или для пропорционального масштабирования, если изображение слишком большое.
            # Для растяжения на всю ширину, мы в первую очередь ориентируемся на ширину.
            # Если картинка получилась слишком высокой, можно ее ограничить:
            if new_height > IMAGE_HEIGHT_TARGET * 1.5:  # Пример ограничения: если высота больше чем в 1.5 раза от целевой
                new_height = IMAGE_HEIGHT_TARGET * 1.5  # Ограничиваем высоту

            single_image_element = Image(LOGO_PATH, width=new_width,
                                         height=new_height)

        except Exception as e:
            print(f"Ошибка при загрузке изображения {LOGO_PATH}: {e}")

        # --- Компоновка изображения и текста ---
        if single_image_element:
            # Рисуем изображение
            # Y-позиция картинки: нижний край страницы + отступ + высота текста сноски + отступ
            image_y_pos = 0.5 * inch + footer_text_h + 0.1 * inch

            # Центрируем изображение по горизонтали
            image_draw_x = inch + (
                        available_width_for_images - single_image_element._width) / 2

            single_image_element.drawOn(canvas, image_draw_x, image_y_pos)

            # Рисуем текст сноски под изображением
            footer_paragraph.drawOn(canvas, inch, 0.5 * inch)

        else:  # Если изображение не загрузилось, рисуем только текст
            footer_paragraph.drawOn(canvas, inch, 0.5 * inch)

        canvas.restoreState()

    # --- Определяем отступы для первой и последующих страниц ---
    # Эти отступы определяют, сколько свободного места будет ДО основного контента.
    # На первой странице: большее место сверху (для шапки) и снизу (для сноски).
    # На последующих: меньшее место сверху (только для основного контента) и снизу (для сноски).

    # Первая страница:
    TOP_MARGIN_FIRST_PAGE = 0.5 * inch  # Отступ от верхнего края страницы до начала основной контентной области
    BOTTOM_MARGIN_FIRST_PAGE = 2.2 * inch  # Отступ от нижнего края страницы до низа сноски

    # Последующие страницы:
    TOP_MARGIN_LATER_PAGES = 0.5 * inch  # Отступ от верхнего края страницы до начала основной контентной области
    BOTTOM_MARGIN_LATER_PAGES = 1.5 * inch  # Отступ от нижнего края страницы до низа сноски

    def page_callback_first(canvas, doc):
        # Рисуем шапку и сноску с отступами, как для первой страницы.
        # y_offset_top_content: сколько места занимает шапка + отступ от нее до контента.
        # y_offset_bottom_content: сколько места занимает сноска + отступ от нее до нижнего края.
        render_header_and_footer(canvas, doc,
                                 y_offset_top_content=TOP_MARGIN_FIRST_PAGE,
                                 y_offset_bottom_content=BOTTOM_MARGIN_FIRST_PAGE)

    def page_callback_later(canvas, doc):
        # Рисуем ТОЛЬКО сноску с отступами, как для последующих страниц.
        # Здесь мы НЕ вызываем отрисовку шапки.
        # y_offset_bottom_content: отступ снизу для сноски.
        render_header_and_footer(canvas, doc, y_offset_top_content=TOP_MARGIN_LATER_PAGES,
                                 y_offset_bottom_content=BOTTOM_MARGIN_LATER_PAGES)

    # --- Таблица ---
    # --- Определение цвета для разовых платежей ---
    ONETIME_PAYMENT_BG_COLOR = colors.HexColor('#088B95')
    HEAD_BG_COLOR = colors.HexColor('#D2C0B1')
    table_data = [["№", "Дата внесения платежа", "Сумма платежа", "Пояснение"]]
    total_paid = 0.0
    current_row_index = 1 # Индекс текущей строки в table_data (0 - заголовок)

    table_style_commands = [
        ('BACKGROUND', (0, 0), (-1, 0), HEAD_BG_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), font_regular),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
        ('FONTNAME', (0, 1), (-1, -2), font_book),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
        ('TOPPADDING', (0, 1), (-1, -2), 8),

        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
        ('TEXTCOLOR', (0, -1), (0, -1), colors.black),
        ('FONTNAME', (0, -1), (0, -1), font_regular),
        ('GRID', (0, -1), (0, -1), 1, colors.black),

        ('TEXTCOLOR', (2, -1), (2, -1), colors.black),
        ('FONTNAME', (2, -1), (2, -1), font_regular),
        ('GRID', (2, -1), (2, -1), 1, colors.black),

        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        ('TOPPADDING', (0, -1), (-1, -1), 10),

        ('GRID', (0, 0), (-1, -2), 0.5, colors.black),
        ('GRID', (0, -1), (3, -1), 0.5, colors.black),

        ('SPAN', (0, -1), (1, -1)),
    ]

    for payment in payment_schedule:
        # Для столбца "Пояснение" создаем Paragraph
        note_paragraph = Paragraph(payment.get('note', ''), note_style)
        onetime_payment = payment.get('onetime_payment', False)

        table_data.append([
            f"{payment.get('month', 0)}",
            payment.get('date', ''),
            f"{payment.get('amount', 0.0):,.2f}".replace(',', ' ') + " руб.",
            note_paragraph
        ])
        total_paid += payment.get('amount', 0.0)

        # Если это разовый платеж, добавляем команду для его подсветки
        if onetime_payment:
            # Применяем фон ко всем ячейкам текущей строки (от столбца 0 до последнего)
            # row_index - это текущая строка в table_data (начиная с 0).
            # Так как мы добавили заголовок (индекс 0), а потом добавляем данные,
            # текущая строка для платежа будет current_row_index.
            table_style_commands.append(('BACKGROUND', (0, current_row_index), (-1, current_row_index), ONETIME_PAYMENT_BG_COLOR))
            # Можно также изменить цвет текста, если нужно
            # table_style_commands.append(('TEXTCOLOR', (0, current_row_index), (-1, current_row_index), colors.darkblue))

        current_row_index += 1 # Переходим к следующей строке

    table_data.append([
        "Итого выплачено:", "", f"{total_paid:,.2f} руб.", ""
    ])
    table_style_commands.append(('BACKGROUND', (0, current_row_index), (-1, current_row_index), HEAD_BG_COLOR))
    table_style_commands.append(('VALIGN', (0, current_row_index - 1), (-1, current_row_index - 1), 'MIDDLE'))

    col_widths = [0.5 * inch, 2.0 * inch, 1.5 * inch, 2.5 * inch]
    table = LongTable(table_data, colWidths=col_widths)

    table.setStyle(TableStyle(table_style_commands))

    story.append(table)

    # --- Отрисовка PDF ---
    # Первая страница: рисуем шапку и сноску с бОльшими отступами.
    # Последующие страницы: рисуем ТОЛЬКО сноску с меньшими отступами.
    doc.build(story, onFirstPage=page_callback_first,
              onLaterPages=page_callback_later)
    buffer.seek(0)
    return buffer
