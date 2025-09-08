import { useState, type FC, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { HomeOutlined } from '@ant-design/icons';
import { Button as AntdButton, DatePicker } from 'antd';
import { Button, MoneyInput } from '../../components';
import ru_RU from 'antd/es/date-picker/locale/ru_RU';
import dayjs from 'dayjs';
import styles from './InstallmentPage.module.scss';

type TInstallmentPageProps = {
    children?: ReactNode;
};

const InstallmentPage: FC<TInstallmentPageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToHome = () => navigate(RoutePath.home);

    const [propertyPrice, setPropertyPrice] = useState<number | null>(null);
    const [initialPaymentDate, setInitialPaymentDate] = useState(null);
    const submitForm = () => {
        if (propertyPrice && propertyPrice > 0 && initialPaymentDate) {
            localStorage.setItem('propertyPrice', propertyPrice.toString());
            localStorage.setItem('initialPaymentDate', dayjs(initialPaymentDate).format());
            navigate(RoutePath.installment_result);
        } else {
            return;
        }
    }

    return (
        <section className={styles.container}>
            <div className={styles.content}>
                <AntdButton type="text" size="large" onClick={navigateToHome}>
                    <HomeOutlined style={{ fontSize: '20px', color: '#fff' }} />
                </AntdButton>
                <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Стоимость квартиры</p>
                        <MoneyInput value={propertyPrice} onChange={setPropertyPrice} className={styles.inputContainer__input} />
                    </div>
                    <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Дата внесения ПВ</p>
                        <DatePicker 
                            locale={ru_RU}
                            format="DD.MM.YYYY"
                            placeholder="Выберите дату"
                            style={{ width: '40%' }}
                            className={styles.inputContainer__input}
                            value={initialPaymentDate}
                            onChange={setInitialPaymentDate}
                        />
                    </div>
                <Button onClick={submitForm}>Рассчитать</Button>
            </div>
        </section>
    );
};

export { InstallmentPage };