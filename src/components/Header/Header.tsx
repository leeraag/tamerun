import type { FC, ReactNode } from 'react';
import clsx from 'clsx';
import styles from './Header.module.scss';

type THeaderProps = {
    title?: string | ReactNode;
    pageType?: "home" | "page";
    className?: string;
};

const Header: FC<THeaderProps> = ({title, pageType}) => {
    return (
        <header className={
            clsx(
                styles.header,
                pageType === "home" ? styles.header_home : styles.header_page,
            )}
        >
            <p className={styles.header__title}>
                {title}
            </p>
        </header>
    );
};

export {Header};