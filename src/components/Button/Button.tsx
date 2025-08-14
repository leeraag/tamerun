import type {FC, ReactNode} from 'react';
import styles from './Button.module.scss';

type TButtonProps = {
    children?: ReactNode;
    onClick?: () => void;
};

const Button: FC<TButtonProps> = ({children, onClick}) => {
    return (
        <button className={styles.button} onClick={onClick}>
            {children}
        </button>
    );
};

export {Button};