import {useEffect, useState, type FC, type ReactNode} from 'react';
import { Button } from '../../components';
import styles from './ResultPage.module.scss';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { Table, Tabs } from 'antd';
import type { TYearlyData } from '../../utils/calculateProfit';
import { columns } from './ResultPage.constants';

type TResultPageProps = {
    children?: ReactNode;
};

const ResultPage: FC<TResultPageProps> = ({}) => {
    const navigate = useNavigate();

    const finishCalculate = () => {
        localStorage.clear();
        navigate(RoutePath.calculate);
    }
    const [totalProfit, setTotalProfit] = useState<number>(0);
    const [yearlyData, setYearlyData] = useState<TYearlyData[]>([]);
    const initialAmount = localStorage.getItem('initialAmount');
    useEffect(() => {
        const savedData = localStorage.getItem('profitData');
        if (savedData) {
            const { total, yearlyData } = JSON.parse(savedData);
            setTotalProfit(total);
            setYearlyData(yearlyData);
        }
    }, []);

    const profitShow = Number(totalProfit).toFixed(2).toString();
    const income = (Number(totalProfit) - Number(initialAmount)).toFixed(2).toString();

    const tabsContent = [
        {
            label: "Общий доход",
            key: '1',
            children: 
                <div className={styles.content}>
                    <div className={styles.field}>
                        <p className={styles.field__title}>Доход:</p>
                        <p className={styles.field__value}>{income.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽</p>
                    </div>
                    <div className={styles.field}>
                        <p className={styles.field__title}>Итоговая сумма:</p>
                        <p className={styles.field__value}>{profitShow?.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽</p>
                    </div>
                </div>
        },
        {
            label: "Детализация",
            key: '2',
            children: 
                <Table
                    columns={columns}
                    dataSource={yearlyData}
                    pagination={false}
                    scroll={{ y: 150 }}
                    style={{
                        borderRadius: '0 0 8px 8px',
                        overflow: 'hidden',
                    }}
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

export { ResultPage };