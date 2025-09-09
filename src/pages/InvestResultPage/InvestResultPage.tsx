import {useEffect, useState, type FC, type ReactNode} from 'react';
import { Button } from '../../components';

import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { Table, Tabs } from 'antd';
import { COLUMNS, INTEREST_RATE } from './InvestResultPage.constants';
import { investApi } from './api/invest.api';
import styles from './InvestResultPage.module.scss';

type TInvestResultPageProps = {
    children?: ReactNode;
};

type TYearlyDetails = {
  year: number;
  start_amount: number;
  yearly_profit: number;
  end_amount: number;
}

const InvestResultPage: FC<TInvestResultPageProps> = ({}) => {
    const navigate = useNavigate();

    const finishCalculate = () => {
        localStorage.clear();
        navigate(RoutePath.invest);
    }

    const [totalAmount, setTotalAmount] = useState<number>(0);
    const [profit, setProfit] = useState<number>(0);
    const [yearlyDetails, setYearlyDetails] = useState<TYearlyDetails[]>([]);
    const initialAmount = localStorage.getItem('initialAmount');
    const term = localStorage.getItem('term')

    const fetchInvest = async (
        interestRate: number,
        initialAmount: number,
        term: number,
    ) => {
        try {
            const response = await investApi.postInvestCalculate(
                interestRate,
                initialAmount,
                term
            );
            setTotalAmount(response.data.total_amount);
            setProfit(response.data.profit)
            setYearlyDetails(response.data.yearly_details);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchInvest(INTEREST_RATE, Number(initialAmount), Number(term));
    }, []);

    const tabsContent = [
        {
            label: "Общий доход",
            key: '1',
            children: 
                <div className={styles.content}>
                    <div className={styles.field}>
                        <p className={styles.field__title}>Доход:</p>
                        <p className={styles.field__value}>
                            {profit.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽
                        </p>
                    </div>
                    <div className={styles.field}>
                        <p className={styles.field__title}>Итоговая сумма:</p>
                        <p className={styles.field__value}>
                            {totalAmount.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽
                        </p>
                    </div>
                </div>
        },
        {
            label: "Детализация",
            key: '2',
            children: 
                <Table
                    columns={COLUMNS}
                    dataSource={yearlyDetails}
                    pagination={false}
                    scroll={{ y: 150 }}
                    style={{
                        borderRadius: '0 0 8px 8px',
                        overflow: 'hidden',
                    }}
                    rowKey={(record) => record.year}
                />
        },
    ];
    return (
        <section className={styles.container}>
            <div className={styles.tab}>
                <Tabs type="card" items={tabsContent} className={styles.tabs}/>
                <Button onClick={finishCalculate}>Понятно</Button>
            </div>
        </section>
    );
};

export { InvestResultPage };