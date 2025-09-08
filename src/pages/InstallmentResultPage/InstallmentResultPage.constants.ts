export const COLUMNS = [
    {
        title: '№',
        dataIndex: 'month',
        key: 'month',
        width: 50,
    },
    {
        title: 'Дата внесения платежа',
        dataIndex: 'date',
        key: 'date',
        width: 'auto',
    },
    {
        title: 'Сумма платежа',
        dataIndex: 'amount',
        key: 'amount',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
    {
        title: 'Пояснение',
        dataIndex: 'note',
        key: 'note',
        width: 'auto',
    },
];



export const INSTALLMENT_SETTINGS_6 = {
    initial_payment_percentage: 50,
    installment_percentage: 0,
    installment_period: 6,
    intermediate_payments: [],
    monthly_payment_percentage: 0,
};

export const INSTALLMENT_SETTINGS_12 = {
    initial_payment_percentage: 20,
    installment_percentage: 5,
    installment_period: 12,
    intermediate_payments: [[7, 10]],
    monthly_payment_percentage: 0.5,
};

export const INSTALLMENT_SETTINGS_18 = {
    initial_payment_percentage: 30,
    installment_percentage: 7.5,
    installment_period: 18,
    intermediate_payments: [[10, 10]],
    monthly_payment_percentage: 0.74,
};

export const INSTALLMENT_SETTINGS_24 = {
    initial_payment_percentage: 35,
    installment_percentage: 10,
    installment_period: 24,
    intermediate_payments: [[12, 15]],
    monthly_payment_percentage: 0.99,
};

export const INSTALLMENT_SETTINGS_36 = {
    initial_payment_percentage: 30,
    installment_percentage: 20,
    installment_period: 36,
    intermediate_payments: [[12, 10], [24,10]],
    monthly_payment_percentage: 0.16,
};