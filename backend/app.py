from datetime import datetime
from flask import Flask, jsonify, render_template_string, request, Response
from flasgger import Swagger, swag_from
from flask_cors import CORS
from utils.calculator import generate_payment_schedule, generate_investment_forecast
from utils.pdf_generator import generate_pdf

app = Flask(__name__)
swagger = Swagger(app, template = {
    "swagger": "2.0",
    "info": {
        'title': 'API для tamerun-invest',
        'version': '1.0',
        'description': 'API для вычисления прогозов банковских операций '
                       'в сфере недвижиомсти'
    }
})

local_frontend_origin = "http://localhost:443"
production_frontend_origin = "https://tamerun-invest.ru"
some_frontend_origin = "http://0.0.0.0:443"

CORS(app,
     resources={
         r"/api/*": {
             "origins": [
                 local_frontend_origin,
                 production_frontend_origin,
                 some_frontend_origin,
             ]
         }
     },
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Disposition"])

"""
Convert to json result
:param key: key for json
:param result: result calculations
:param code: result code
:return: result calculations in json format
"""
def to_result_json(key, result, code):
    return jsonify({
        key: result
    }), code

@app.route('/api/<int:first>/<int:second>', methods=['GET'])
def calculation(first, second):
    return to_result_json('result', first + second, 200)

@app.route('/api/download_pdf_payment_schedule', methods=['POST'])
@swag_from({
    "tags": ["Расчет рассрочек"],
    "description": """
        Этот endpoint принимает детальные данные об объекте недвижимости,
        включая стоимость, параметры рассрочки, первоначальный взнос и
        дополнительные промежуточные платежи.
        В ответ возвращает график платежей по рассрочке как PDF файл для
        скачивания
    """,
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "property_price": {
                        "type": "number",
                        "format": "float",
                        "description": "Полная стоимость объекта недвижимости",
                        "example": 10102330
                    },
                    "installment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент на рассрочку (0-100)",
                        "example": 10
                    },
                    "initial_payment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент первоначального взноса (0-100)",
                        "example": 35
                    },
                    "installment_period": {
                        "type": "integer",
                        "description": "Срок рассрочки в месяцах",
                        "example": 24
                    },
                    "monthly_payment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент от стоимости (с учётом "
                                       "процентов), составляющий размер "
                                       "ежемесячного платежа",
                        "example": 0.99
                    },
                    "intermediate_payments": {
                        "type": "array",
                        "description": "Список промежуточных платежей. Каждый "
                                       "элемент - это массив/кортеж из двух "
                                       "элементов: (месяц, % от стоимости)",
                        "items": {
                            "type": "array",
                            "items": [
                                {"type": "integer",
                                  "description": "Месяц (1-installment_period)"
                                },
                                {"type": "number",
                                 "format": "float",
                                 "description": "Процент от стоимости (0-100)"
                                }
                            ],
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "nullable": True,
                        "example": [[12, 15]]
                    },
                    "initial_payment_date": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Начальная дата платежа в формате "
                                       "ISO 8601 с временной зоной:"
                                       " YYYY-MM-DDTHH:MM:SS±HH:MM",
                        "example": "2025-11-25T00:00:00+03:00"
                    },
                    "apartment_number": {
                        "type": "integer",
                        "description": "Номер апартаментов",
                        "example": 2
                    },
                },
                "required": [
                    "property_price",
                    "installment_percentage",
                    "initial_payment_percentage",
                    "installment_period",
                    "monthly_payment_percentage"
                ]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Успешный ответ с расписанием платежей в PDF файле",
            "schema": {
                "type": "string",
                "format": "binary",
                "example": "Бинарные данные, представляющие собой PDF-файл "
                           "(payment_schedule.pdf)"
            }
        },
        "400": {
            "description": "Некорректные входные данные или ошибка валидации",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Описание ошибки",
                        "example": "Не были предоставлены JSON данные"
                    }
                }
            }
        },
        "500": {
            "description": "Внутренняя ошибка сервера",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Описание ошибки",
                        "example": "Произошла непредвиденная ошибка: упс"
                    }
                }
            }
        }
    }
})
def download_pdf():
    """
        Endpoint генерирует PDF с графиком платежей по рассрочке на недвижимость
        и возвращает его для скачивания.
        Принимает JSON с параметрами недвижимости и рассрочки
    """
    # Получаем JSON-данные из запроса
    data = request.get_json()

    # Проверяем, были ли вообще получены данные
    if not data:
        return jsonify({"error": "Не были предоставлены JSON данные"}), 400

    # Извлекаем данные и выполняем валидацию (простейшая)
    try:
        property_price = float(data.get('property_price'))
        installment_percentage = float(data.get('installment_percentage'))
        initial_payment_percentage = float(
            data.get('initial_payment_percentage'))
        installment_period = int(data.get('installment_period'))
        monthly_payment_percentage = float(
            data.get('monthly_payment_percentage'))
        intermediate_payments = data.get('intermediate_payments') # Мб None
        apartment_number = data.get('apartment_number')
        initial_payment_date_str = data.get('initial_payment_date')
        initial_payment_date = datetime.now()
        try:
            # Парсим строку в datetime объект
            initial_payment_date = datetime.fromisoformat(initial_payment_date_str)
        except ValueError as e:
            return jsonify({
                    "error": f"Invalid date format: {e}"
            }), 400

        # Простейшая валидация типов и значений
        if not all([
            isinstance(property_price, (int, float))
                and property_price >= 0,
            isinstance(installment_percentage, (int, float))
                and 0 <= installment_percentage <= 100,
            isinstance(initial_payment_percentage, (int, float))
                and 0 <= initial_payment_percentage <= 100,
            isinstance(installment_period, int)
                and installment_period > 0,
            isinstance(monthly_payment_percentage, (int, float))
                and 0 <= monthly_payment_percentage <= 100,
            isinstance(apartment_number, int)
                and 0 <= apartment_number <= 999999,
        ]):
            return jsonify({
                "error": "Некорректные входные данные. "
                         "Проверьте типы и диапазоны значений"
            }), 400

        # Валидация intermediate_payments
        if intermediate_payments is not None:
            if not isinstance(intermediate_payments, list):
                return jsonify({
                    "error": "'intermediate_payments' должен быть списком"
                }), 400
            for payment in intermediate_payments:
                if not (isinstance(payment, (list, tuple))
                    and len(payment) == 2):
                    return jsonify({
                        "error": "Элементы 'intermediate_payments' должны быть "
                                 "кортежами (месяц, процент)"
                    }), 400
                month, percent = payment
                if not (isinstance(month, int)
                    and 0 < month <= installment_period):
                    return jsonify({
                        "error": "Некорректный номер месяца в "
                                 "'intermediate_payments'"
                    }), 400
                if not (isinstance(percent, (int, float))
                    and 0 <= percent <= 100):
                    return jsonify({
                        "error": "Некорректный процент в "
                                 "'intermediate_payments'"
                    }), 400
    except (TypeError, ValueError) as e:
        return jsonify({
            "error": f"Ошибка при парсинге входных данных: {e}. "
                     "Убедитесь, что все числовые поля корректны"
        }), 400
    except Exception as e:
        return jsonify({"error": f"Произошла непредвиденная ошибка: {e}"}), 500

    # Выполняем расчет графика платежей
    payment_schedule = generate_payment_schedule(
        property_price,
        installment_percentage,
        initial_payment_percentage,
        installment_period,
        monthly_payment_percentage,
        initial_payment_date,
        intermediate_payments,
    )

    # Выполняем генерацию PDF
    pdf_buffer = generate_pdf(payment_schedule[0],
                              property_price,
                              installment_period,
                              apartment_number)

    # Создаем объект Response
    # content_type='application/pdf' указывает браузеру, что это PDF
    # 'Content-Disposition': 'attachment; filename="payment_schedule.pdf"'
    #   'attachment' говорит браузеру, что файл нужно скачать.
    #   'filename="payment_schedule.pdf"' предлагает имя файла для скачивания.
    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': 'attachment;filename="payment_schedule.pdf"'
        }
    )

@app.route('/api/calculate_payment_schedule', methods=['POST'])
@swag_from({
    "tags": ["Расчет рассрочек"],
    "summary": "Обработка данных о недвижимости, связанных с её покупкой "
               "в рассрочку",
    "description": """
        Этот endpoint принимает детальные данные об объекте недвижимости,
        включая стоимость, параметры рассрочки, первоначальный взнос и
        дополнительные промежуточные платежи.
        В ответ возвращает график платежей по рассрочке и финальную стоимость
        недвижимости с учётом процентов
    """,
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "property_price": {
                        "type": "number",
                        "format": "float",
                        "description": "Полная стоимость объекта недвижимости",
                        "example": 10102330
                    },
                    "installment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент на рассрочку (0-100)",
                        "example": 10
                    },
                    "initial_payment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент первоначального взноса (0-100)",
                        "example": 35
                    },
                    "installment_period": {
                        "type": "integer",
                        "description": "Срок рассрочки в месяцах",
                        "example": 24
                    },
                    "monthly_payment_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Процент от стоимости (с учётом "
                                       "процентов), составляющий размер "
                                       "ежемесячного платежа",
                        "example": 0.99
                    },
                    "intermediate_payments": {
                        "type": "array",
                        "description": "Список промежуточных платежей. Каждый "
                                       "элемент - это массив/кортеж из двух "
                                       "элементов: (месяц, % от стоимости)",
                        "items": {
                            "type": "array",
                            "items": [
                                {"type": "integer",
                                  "description": "Месяц (1-installment_period)"
                                },
                                {"type": "number",
                                 "format": "float",
                                 "description": "Процент от стоимости (0-100)"
                                }
                            ],
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "nullable": True,
                        "example": [[12, 15]]
                    },
                    "initial_payment_date": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Начальная дата платежа в формате "
                                       "ISO 8601 с временной зоной:"
                                       " YYYY-MM-DDTHH:MM:SS±HH:MM",
                        "example": "2025-11-25T00:00:00+03:00"
                    },
                },
                "required": [
                    "property_price",
                    "installment_percentage",
                    "initial_payment_percentage",
                    "installment_period",
                    "monthly_payment_percentage"
                ]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Успешный ответ с расписанием платежей",
            "schema": {
                "type": "object",
                "properties": {
                    "payment_schedule": {
                        "type": "array",
                        "description": "Список всех платежей согласно графику",
                        "items": {
                            "type": "object",
                            "properties": {
                                "amount": {
                                    "type": "number",
                                    "format": "float",
                                    "description": "Сумма платежа",
                                    "example": 110014
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Дата платежа (формат: "
                                                   "'мес. YYYY')",
                                    "example": "окт.2025"
                                },
                                "month": {
                                    "type": "integer",
                                    "description": "Номер месяца платежа "
                                                   "(начиная с 1)"
                                                   ,
                                    "example": 2
                                },
                                "note": {
                                    "type": "string",
                                    "description": "Описание платежа (например,"
                                                   " 'Внесение ПВ', "
                                                   "'Ежемесячный платеж').",
                                    "example": "Ежемесячный платеж"
                                },
                                "onetime_payment": {
                                    'type': 'boolean',
                                    "description": "Флаг единоразового крупного"
                                                   " платежа. False для "
                                                   "ежемесячных",
                                    "example": False
                                }
                            }
                        }
                    },
                    "total_cost": {
                        "type": "number",
                        "format": "float",
                        "description": "Общая стоимость объекта",
                        "example": 11112563
                    }
                }
            }
        },
        "400": {
            "description": "Некорректные входные данные или ошибка валидации",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Описание ошибки",
                        "example": "Не были предоставлены JSON данные"
                    }
                }
            }
        },
        "500": {
            "description": "Внутренняя ошибка сервера",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Описание ошибки",
                        "example": "Произошла непредвиденная ошибка: упс"
                    }
                }
            }
        }
    }
})
def calculate_payment_schedule():
    """
        Endpoint для составления графика платежей по рассрочке на недвижимость.
        Принимает JSON с параметрами недвижимости и рассрочки.
        Возвращает JSON с графиком платежей и финальную стоимость недвижимости
    """
    # Получаем JSON-данные из запроса
    data = request.get_json()

    # Проверяем, были ли вообще получены данные
    if not data:
        return jsonify({"error": "Не были предоставлены JSON данные"}), 400

    # Извлекаем данные и выполняем валидацию (простейшая)
    try:
        property_price = float(data.get('property_price'))
        installment_percentage = float(data.get('installment_percentage'))
        initial_payment_percentage = float(
            data.get('initial_payment_percentage'))
        installment_period = int(data.get('installment_period'))
        monthly_payment_percentage = float(
            data.get('monthly_payment_percentage'))
        intermediate_payments = data.get('intermediate_payments') # Мб None
        initial_payment_date_str = data.get('initial_payment_date')
        initial_payment_date = datetime.now()
        try:
            # Парсим строку в datetime объект
            initial_payment_date = datetime.fromisoformat(initial_payment_date_str)
        except ValueError as e:
            return jsonify({
                    "error": f"Invalid date format: {e}"
            }), 400

        # Простейшая валидация типов и значений
        if not all([
            isinstance(property_price, (int, float))
                and property_price >= 0,
            isinstance(installment_percentage, (int, float))
                and 0 <= installment_percentage <= 100,
            isinstance(initial_payment_percentage, (int, float))
                and 0 <= initial_payment_percentage <= 100,
            isinstance(installment_period, int)
                and installment_period > 0,
            isinstance(monthly_payment_percentage, (int, float))
                and 0 <= monthly_payment_percentage <= 100,
        ]):
            return jsonify({
                "error": "Некорректные входные данные. "
                         "Проверьте типы и диапазоны значений"
            }), 400

        # Валидация intermediate_payments
        if intermediate_payments is not None:
            if not isinstance(intermediate_payments, list):
                return jsonify({
                    "error": "'intermediate_payments' должен быть списком"
                }), 400
            for payment in intermediate_payments:
                if not (isinstance(payment, (list, tuple))
                    and len(payment) == 2):
                    return jsonify({
                        "error": "Элементы 'intermediate_payments' должны быть "
                                 "кортежами (месяц, процент)"
                    }), 400
                month, percent = payment
                if not (isinstance(month, int)
                    and 0 < month <= installment_period):
                    return jsonify({
                        "error": "Некорректный номер месяца в "
                                 "'intermediate_payments'"
                    }), 400
                if not (isinstance(percent, (int, float))
                    and 0 <= percent <= 100):
                    return jsonify({
                        "error": "Некорректный процент в "
                                 "'intermediate_payments'"
                    }), 400
    except (TypeError, ValueError) as e:
        return jsonify({
            "error": f"Ошибка при парсинге входных данных: {e}. "
                     "Убедитесь, что все числовые поля корректны"
        }), 400
    except Exception as e:
        return jsonify({"error": f"Произошла непредвиденная ошибка: {e}"}), 500

    # Выполняем расчет графика платежей
    payment_schedule = generate_payment_schedule(
        property_price,
        installment_percentage,
        initial_payment_percentage,
        installment_period,
        monthly_payment_percentage,
        initial_payment_date,
        intermediate_payments,
    )

    # Формируем JSON-ответ
    response_data = {
        "payment_schedule": payment_schedule[0],
        "total_cost": payment_schedule[1]
    }

    return jsonify(response_data), 200

# --- Константы для ограничений входных данных ---
MIN_STARTING_CAPITAL = 9000000
MAX_STARTING_CAPITAL = 1000000000
MIN_INVESTMENT_YEARS = 1
MAX_INVESTMENT_YEARS = 100
DEFAULT_INTEREST_RATE = 15 # 5% годовых (пример)

@app.route('/api/calculate_investment_forecast', methods=['POST'])
@swag_from({
    "tags": ["Расчет инвестиций"],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'starting_capital': {
                        'type': 'number',
                        'description': f'Стартовый капитал (от {MIN_STARTING_CAPITAL:,} до {MAX_STARTING_CAPITAL:,} руб.)',
                        'minimum': MIN_STARTING_CAPITAL,
                        'maximum': MAX_STARTING_CAPITAL,
                        'example': 9000000.00,
                    },
                    'years': {
                        'type': 'integer',
                        'description': f'Срок инвестирования в годах (от {MIN_INVESTMENT_YEARS} до {MAX_INVESTMENT_YEARS} лет)',
                        'minimum': MIN_INVESTMENT_YEARS,
                        'maximum': MAX_INVESTMENT_YEARS,
                        'example': 5,
                    },
                    'annual_interest_rate': {
                        'type': 'number',
                        'required': False,
                        'description': 'Годовая процентная ставка (по умолчанию 10%)',
                        'default': DEFAULT_INTEREST_RATE,
                        'minimum': 0,
                        'maximum': 100, # 100%
                        'example': 15
                    }
                },
                'required': ['starting_capital', 'years'] # Указываем обязательные поля тела запроса
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Прогноз доходности инвестиций',
            'schema': {
                'type': 'object',
                'properties': {
                    'total_amount': {
                        'type': 'number',
                        'description': 'Итоговая сумма (стартовый капитал + доход)',
                        'example': 18102214.69
                    },
                    'profit': {
                        'type': 'number',
                        'description': 'Доход за весь срок инвестирования',
                        'example': 9102214.69
                    },
                    'yearly_details': {
                        'type': 'array',
                        'description': 'Детализация по годам',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'year': {'type': 'integer', 'description': 'Номер года','example': 1},
                                'start_amount': {'type': 'number', 'description': 'Сумма в начале года', 'example': 9000000.00},
                                'yearly_profit': {'type': 'number', 'description': 'Доход за год (с учетом капитализации)', 'example': 1350000.00},
                                'end_amount': {'type': 'number', 'description': 'Конечная сумма по результатам года', 'example': 10350000.00}
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Ошибка входных данных',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Описание ошибки'}
                }
            }
        }
    }
})
def calculate_investment_forecast():
    """
    Рассчитывает прогнозную доходность инвестиций с ежегодным реинвестированием.
    """
    try:
        # Получаем JSON из тела запроса
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Тело запроса должно быть в формате JSON'}), 400

        starting_capital = float(data.get('starting_capital'))
        years = int(data.get('years'))
        # Используем get с default, если ключ отсутствует
        annual_interest_rate = float(data.get('annual_interest_rate', DEFAULT_INTEREST_RATE))

        # --- Валидация входных данных ---
        if not (MIN_STARTING_CAPITAL <= starting_capital <= MAX_STARTING_CAPITAL):
            return jsonify({'error': f'Стартовый капитал должен быть от {MIN_STARTING_CAPITAL:,} до {MAX_STARTING_CAPITAL:,} руб.'}), 400
        if not (MIN_INVESTMENT_YEARS <= years <= MAX_INVESTMENT_YEARS):
            return jsonify({'error': f'Срок инвестирования должен быть от {MIN_INVESTMENT_YEARS} до {MAX_INVESTMENT_YEARS} лет.'}), 400
        if not (0 <= annual_interest_rate <= 100):
            return jsonify({'error': 'Годовая процентная ставка должна быть от 0 до 100%).'}), 400

        # Выполняем расчет прогноза инвестирования
        investment_forecast = generate_investment_forecast(
            starting_capital,
            years,
            annual_interest_rate,
        )


        return jsonify({
            'total_amount': round(investment_forecast[0], 2),
            'profit': round(investment_forecast[1], 2),
            'yearly_details': investment_forecast[2]
        })

    except ValueError:
        return jsonify({'error': 'Некорректный формат числовых данных. Пожалуйста, введите числа.'}), 400
    except Exception as e:
        # Логирование ошибки для отладки
        app.logger.error(f"Произошла ошибка при расчете доходности: {e}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера при расчете доходности.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
