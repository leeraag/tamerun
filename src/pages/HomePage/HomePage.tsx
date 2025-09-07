import { type FC, type ReactNode } from 'react';
import { Button } from '../../components';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import styles from './HomePage.module.scss';
import { Button as AntdButton } from 'antd';

type THomePageProps = {
    children?: ReactNode;
};

const HomePage: FC<THomePageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToInvest = () => navigate(RoutePath.invest);
    const navigateToInstallment = () => navigate(RoutePath.installment);

    return (
        <section className={styles.container}>
            <div className={styles.buttons}>
                {/* <AntdButton size="large" block ghost onClick={navigateToInvest}>Инвестиционный калькулятор</AntdButton>
                <AntdButton size="large" block ghost onClick={navigateToInstallment}>Калькулятор рассрочек</AntdButton> */}
                <Button onClick={navigateToInvest} fullWidth>Инвестиционный калькулятор</Button>
                <Button onClick={navigateToInstallment} fullWidth>Калькулятор рассрочек</Button>
            </div>

        </section>
    );
};

export { HomePage };