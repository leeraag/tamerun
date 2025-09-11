import { useState, type FC, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { HomeOutlined, LeftOutlined } from '@ant-design/icons';
import { DatePicker, InputNumber } from 'antd';
import { Button, Header, LinkButton, MoneyInput } from '../../components';
import ru_RU from 'antd/es/date-picker/locale/ru_RU';
import dayjs from 'dayjs';
import styles from './InstallmentPage.module.scss';

type TInstallmentPageProps = {
    children?: ReactNode;
};

const InstallmentPage: FC<TInstallmentPageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToHome = () => navigate(RoutePath.home);

    const [apartNum, setApartNum] = useState<number | null>(null);
    const [propertyPrice, setPropertyPrice] = useState<number | null>(null);
    const [initialPaymentDate, setInitialPaymentDate] = useState(null);

    const submitForm = () => {
        if (propertyPrice && propertyPrice > 0 && initialPaymentDate && apartNum) {
            localStorage.setItem('apartNum', apartNum.toString());
            localStorage.setItem('propertyPrice', propertyPrice.toString());
            localStorage.setItem('initialPaymentDate', dayjs(initialPaymentDate).format());
            navigate(RoutePath.installment_result);
        } else {
            return;
        }
    }

    return (
        <>
            <Header title={"Калькулятор рассрочек"} pageType="page" />
            <section className={styles.container}>
                <div className={styles.content}>
                    <LinkButton children={"На главную"} onClick={navigateToHome} icon={<LeftOutlined />} />
                    <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Апартамент №</p>
                        <InputNumber 
                            value={apartNum}
                            onChange={setApartNum}
                            controls={false}
                            step={1}
                            min={0}
                            max={100000}
                            placeholder="Введите номер"
                            suffix={
                                <HomeOutlined style={{ color: '#00000040'}} />
                            }
                            style={{ width: '40%' }}
                            className={styles.inputContainer__input}
                        />
                    </div>
                    <div className={styles.inputContainer}>
                        <p className={styles.inputContainer__title}>Стоимость апартамента</p>
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
                            showNow={false}
                        />
                    </div>
                    <Button onClick={submitForm}>Рассчитать</Button>
                </div>
            </section>
        </>
    );
};

export { InstallmentPage };