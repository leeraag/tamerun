export const columns = [
    {
        title: 'Год',
        dataIndex: 'year',
        key: 'year',
        width: 50,
    },
    {
        title: 'Начальная сумма',
        dataIndex: 'initialAmount',
        key: 'initialAmount',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
    {
        title: 'Доход',
        dataIndex: 'income',
        key: 'income',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
    {
        title: 'Конечная сумма',
        dataIndex: 'finalAmount',
        key: 'finalAmount',
        render: (value: number) => `${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽`,
        width: 'auto',
    },
];