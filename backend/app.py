from flask import Flask, jsonify, render_template_string, request, Response
from flasgger import Swagger, swag_from
from flask_cors import CORS
from utils.calculator import generate_payment_schedule
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

CORS(app,
     resources={
         r"/api/*": {
             "origins": [
                 local_frontend_origin,
                 production_frontend_origin,
             ]
         }
     },
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

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
                    }
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
        intermediate_payments,
    )

    # Выполняем генерацию PDF
    pdf_buffer = generate_pdf(payment_schedule)

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
                    }
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
        intermediate_payments,
    )

    # Формируем JSON-ответ
    response_data = {
        "payment_schedule": payment_schedule[0],
        "total_cost": payment_schedule[1]
    }

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
