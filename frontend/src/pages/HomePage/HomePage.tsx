import { type FC, type ReactNode } from 'react';
import { Button, Header } from '../../components';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import styles from './HomePage.module.scss';

type THomePageProps = {
    children?: ReactNode;
};

const HomePage: FC<THomePageProps> = ({}) => {
    const navigate = useNavigate();

    const navigateToInvest = () => navigate(RoutePath.invest);
    const navigateToInstallment = () => navigate(RoutePath.installment);

    return (
        <>
            <Header 
                title={
                    <span>Рассчитайте специальные условия приобретения 
                        <br/> апартаментов Tamerun Grand Mirmax
                    </span>
                }
                pageType="home"
            />
            <section className={styles.container}>
                <div className={styles.buttons}>
                    <Button onClick={navigateToInvest} fullWidth bold>Инвестиционный калькулятор</Button>
                    <Button onClick={navigateToInstallment} fullWidth bold>Калькулятор рассрочек</Button>
                </div>
            </section>
        </>
    );
};

export { HomePage };