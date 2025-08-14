import type {FC, ReactNode} from 'react';
import { Button } from '../../components';
import styles from './ResultPage.module.scss';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';

type TResultPageProps = {
    children?: ReactNode;
};

const ResultPage: FC<TResultPageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToCalculate = () => navigate(RoutePath.calculate);
    const profit = localStorage.getItem('profit');
    const initialAmount = localStorage.getItem('initialAmount');
    const income = (Number(profit) - Number(initialAmount)).toFixed(2).toString();
    const profitShow = Number(profit).toFixed(2).toString();
    return (
        <section className={styles.container}>
            <div className={styles.content}>
                <div className={styles.field}>
                    <p className={styles.field__title}>Доход:</p>
                    <p className={styles.field__value}>{income.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽</p>
                </div>
                <div className={styles.field}>
                    <p className={styles.field__title}>Итоговая сумма:</p>
                    <p className={styles.field__value}>{profitShow?.replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽</p>
                </div>
                <Button onClick={navigateToCalculate}>Понятно</Button>
            </div>
        </section>
    );
};

export { ResultPage };