import {useState, type FC, type ReactNode} from 'react';
import { Button } from '../../components';
import { calculateProfit, getTermWord } from '../../utils';
import { InputNumber, Select } from 'antd';
import styles from './CalculatePage.module.scss';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import ruble from '../../assets/images/ruble.svg';

type TCalculatePageProps = {
    children?: ReactNode;
};

const CalculatePage: FC<TCalculatePageProps> = ({}) => {
    const termOptions = Array.from({ length: 100 }, (_, i) => ({
        value: i + 1,
        label: `${i + 1} ${getTermWord(i + 1)}`,
    }));
    const navigate = useNavigate();

    const navigateToResult = () => navigate(RoutePath.result);
    const [initialAmount, setInitialAmount] = useState<number | null>(null);
    const [term, setTerm] = useState(0);

    const handleTermChange = (value: number) => {
        setTerm(value);
    };

    const formatter = (value: number | undefined) => {
        if (!value) return '';
        
        return `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    };

    const submitForm = () => {
        if (initialAmount && initialAmount > 0 && term) {
            const { total, yearlyData } = calculateProfit(initialAmount, 15, term);
            localStorage.setItem('initialAmount', initialAmount.toString());
            localStorage.setItem('profitData', JSON.stringify({
                total: total,
                yearlyData: yearlyData
            }));
            navigateToResult();
        } else {
            return;
        }
    }

    return (
        <section className={styles.container}>
            <div className={styles.content}>
                <div className={styles.inputContainer}>
                    <p className={styles.inputContainer__title}>Стартовый капитал</p>
                    <InputNumber
                        style={{ width: '40%' }}
                        formatter={formatter}
                        step={0.01}
                        decimalSeparator=","
                        controls={false}
                        min={9000000}
                        placeholder="Введите сумму"
                        suffix={
                            <img src={ruble} />
                        }
                        value={initialAmount}
                        onChange={setInitialAmount}
                        className={styles.inputContainer__input}
                    />
                </div>
                <div className={styles.inputContainer}>
                    <p className={styles.inputContainer__title}>Срок инвестирования</p>
                    <Select
                        placeholder="Выберите срок"
                        style={{ width: '40%' }}
                        listHeight={200}
                        options={termOptions}
                        onChange={handleTermChange}
                        className={styles.inputContainer__input}
                    />
                </div>
                <Button onClick={submitForm}>Рассчитать</Button>

            </div>
        </section>
    );
};

export {CalculatePage};