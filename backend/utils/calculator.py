import datetime
from dateutil.relativedelta import relativedelta

def get_date_formatted(date):
    """
    Возвращает дату в формате "авг. 2025" (сокращенное русское название месяца)

    Args:
        date: дата для форматирования
    """
    month_names_short = {
        1: "янв.", 2: "фев.", 3: "мар.", 4: "апр.", 5: "май", 6: "июн.",
        7: "июл.", 8: "авг.", 9: "сен.", 10: "окт.", 11: "ноя.", 12: "дек."
    }

    month_number = date.month
    year = date.year
    short_month_name = month_names_short.get(month_number)
    return f"{short_month_name} {year}"

def generate_payment_schedule(
        property_price,
        installment_percentage,
        initial_payment_percentage,
        installment_period,
        monthly_payment_percentage,
        intermediate_payments=None,
):
    """
    Генерирует график платежей для покупки недвижимости.

    Args:
        property_price (float): Полная стоимость объекта недвижимости
        installment_percentage (float): Процент на рассрочку
        initial_payment_percentage (float): Процент первоначального
            взноса (0-100)
        installment_period (int): Срок рассрочки в месяцах
        monthly_payment_percentage (float): Процент от стоимости (с учётом
            процентов), составляющий размер ежемеячного платежа
        intermediate_payments (list, optional): Список промежуточных платежей
            Каждый элемент списка - это кортеж (месяц, процент от стоимости)
            Например: [(6, 10), (12, 15)] означает 10% через 6 месяцев
            и 15% через 12 месяцев

    Returns:
        Кортеж: список словарей, описывающий схему выплат; итоговая стоимость
                покупки с учётом %
    """



    # Начисленная сумма процентов
    interest_amount = property_price * (installment_percentage / 100)
    # Стоимость с учетом процентов
    total_cost = property_price + interest_amount
    # Первоначальный взнос
    initial_payment = total_cost * (initial_payment_percentage / 100)
    # Ежемесячный платёж
    monthly_payment = total_cost * (monthly_payment_percentage / 100)

    schedule = []
    remaining_loan = total_cost
    for month in range(1, installment_period + 1):
        date_month = datetime.date.today() + relativedelta(months=(month - 1))
        payment_amount = 0
        note = ''

        if month == 1:
            payment_amount = initial_payment
            note = f'Внесение ПВ {initial_payment_percentage}%'
        elif any(payment and payment[0] == month
            for payment in intermediate_payments) :
            intermediate_payment_percentage = next(
                (payment[1] for payment in intermediate_payments if
                 payment and payment[0] == month),
                None  # Значение по умолчанию, если ничего не найдено
            )
            note = f'Внесение {intermediate_payment_percentage}%'
            payment_amount = total_cost * (intermediate_payment_percentage/100)
        elif month == installment_period:
            note = "Закрывающий платеж собственными средствами или переход на ипотеку"
            payment_amount = remaining_loan
        else:
            note = 'Ежемесячный платёж'
            payment_amount = monthly_payment

        remaining_loan -= payment_amount

        schedule.append(
            {
                "month": month,
                "date": get_date_formatted(date_month),
                "amount": int(round(payment_amount))
                    if remaining_loan >= 0
                    else 0,
                "note": note
            }
        )

    return schedule, total_cost
