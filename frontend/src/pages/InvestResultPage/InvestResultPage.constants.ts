export const INTEREST_RATE = 15;

export const COLUMNS = [
    {
        title: 'Год',
        dataIndex: 'year',
        key: 'year',
        width: 50,
    },
    {
        title: 'Начальная сумма',
        dataIndex: 'start_amount',
        key: 'start_amount',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
    {
        title: 'Доход',
        dataIndex: 'yearly_profit',
        key: 'yearly_profit',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
    {
        title: 'Конечная сумма',
        dataIndex: 'end_amount',
        key: 'end_amount',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
];