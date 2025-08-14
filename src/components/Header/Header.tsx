import type { FC } from 'react';

import styles from './Header.module.scss';

type THeaderProps = {
    className?: string;
};

const Header: FC<THeaderProps> = ({}) => {
    return (
        <header className={styles.header}>
            <p className={styles.header__title}>
                Рассчитайте вашу прогнозную доходность
                <br/>
                от инвестиций в апартаменты
                <br/>
                Tamerun Grand Mirmax
            </p>
        </header>
    );
};

export {Header};