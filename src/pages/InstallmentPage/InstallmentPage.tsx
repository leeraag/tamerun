import { useState, type FC, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import styles from './InstallmentPage.module.scss';
import { HomeOutlined } from '@ant-design/icons';
import { Button as AntdButton, DatePicker } from 'antd';
import { Button, MoneyInput } from '../../components';
import ru_RU from 'antd/es/date-picker/locale/ru_RU';

type TInstallmentPageProps = {
    children?: ReactNode;
};

const InstallmentPage: FC<TInstallmentPageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToHome = () => navigate(RoutePath.home);

    const [initialAmount, setInitialAmount] = useState<number | null>(null);
    const submitForm = () => {
        // if (initialAmount && initialAmount > 0 && term) {
        //     const { total, yearlyData } = calculateProfit(initialAmount, 15, term);
        //     localStorage.setItem('initialAmount', initialAmount.toString());
        //     localStorage.setItem('profitData', JSON.stringify({
        //         total: total,
        //         yearlyData: yearlyData
        //     }));
        //     navigateToResult();
        // } else {
        //     return;
        // }
        // console.log('navigate');
        navigate(RoutePath.installment_result);
    }

    return (
        <section className={styles.container}>
            <div className={styles.content}>
                <AntdButton type="text" size="large" onClick={navigateToHome}>
                    <HomeOutlined style={{ fontSize: '20px', color: '#fff' }} />
                </AntdButton>
                <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Стоимость квартиры</p>
                        <MoneyInput value={initialAmount} onChange={setInitialAmount} className={styles.inputContainer__input} />
                    </div>
                    <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Дата внесения ПВ</p>
                        <DatePicker 
                            locale={ru_RU}
                            format="DD.MM.YYYY"
                            placeholder="Выберите дату"
                            style={{ width: '40%' }}
                            className={styles.inputContainer__input}
                        />
                    </div>
                <Button onClick={submitForm}>Рассчитать</Button>
            </div>
        </section>
    );
};

export { InstallmentPage };