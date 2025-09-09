import {useState, type FC, type ReactNode} from 'react';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { Button, MoneyInput } from '../../components';
import { getTermWord } from '../../utils';
import { Button as AntdButton, Select } from 'antd';
import { HomeOutlined } from '@ant-design/icons'
import styles from './InvestPage.module.scss';

type TInvestPageProps = {
    children?: ReactNode;
};

const InvestPage: FC<TInvestPageProps> = ({}) => {
    const termOptions = Array.from({ length: 100 }, (_, i) => ({
        value: i + 1,
        label: `${i + 1} ${getTermWord(i + 1)}`,
    }));
    const navigate = useNavigate();

    const navigateToResult = () => navigate(RoutePath.invest_result);
    const navigateToHome = () => navigate(RoutePath.home)
    const [initialAmount, setInitialAmount] = useState<number | null>(null);
    const [term, setTerm] = useState(0);

    const handleTermChange = (value: number) => {
        setTerm(value);
    };

    const submitForm = () => {
        if (initialAmount && initialAmount > 0 && term) {
            localStorage.setItem('initialAmount', initialAmount.toString());
            localStorage.setItem('term', term.toString());
            navigateToResult();
        } else {
            return;
        }
    }

    return (
        <section className={styles.container}>

            <div className={styles.content}>
                <AntdButton type="text" size="large" onClick={navigateToHome}>
                    <HomeOutlined style={{ fontSize: '30px', color: '#fff' }} />
                </AntdButton>
                <div className={styles.inputContainer}>
                    <p className={styles.inputContainer__title}>Стартовый капитал</p>
                    <MoneyInput value={initialAmount} onChange={setInitialAmount} className={styles.inputContainer__input} />
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

export {InvestPage};