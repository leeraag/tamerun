import {useEffect, type FC, type ReactNode} from 'react';
import { Button } from '../../components';
import styles from './InstallmentResultPage.module.scss';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { Tabs } from 'antd';

type TInstallmentResultPageProps = {
    children?: ReactNode;
};

const InstallmentResultPage: FC<TInstallmentResultPageProps> = ({}) => {
    const navigate = useNavigate();

    const finishCalculate = () => {
        localStorage.clear();
        navigate(RoutePath.installment);
    }

    useEffect(() => {
        console.log('запрос на полную оплату');
    }, []);
    const handleTabClick = (key: string) => {
        console.log('tab key', key);
    };

    const tabsContent = [
        {
            label: "Полная оплата",
            key: '1',
            children: "Таблица на полную оплату",
        },
        {
            label: "3 месяца",
            key: '3',
            children: "Таблица на 3 месяца",
        },
        {
            label: "6 месяцев",
            key: '6',
            children: "Таблица на 6 месяцев",
        },
        {
            label: "12 месяцев",
            key: '12',
            children: "Таблица на 12 месяцев",
        },
        {
            label: "24 месяца",
            key: '24',
            children: "Таблица на 24 месяца",
        },
    ];
    return (
        <section className={styles.container}>
            <div className={styles.tab}>
                <Tabs type="card" items={tabsContent} className={styles.tabs} onTabClick={handleTabClick}/>
                <Button onClick={finishCalculate}>Понятно</Button>
            </div>
        </section>
    );
};

export { InstallmentResultPage };