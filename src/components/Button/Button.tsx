import type {FC, ReactNode} from 'react';
import styles from './Button.module.scss';
import clsx from 'clsx';

type TButtonProps = {
    children?: ReactNode;
    onClick?: () => void;
    fullWidth?: boolean;
};

const Button: FC<TButtonProps> = ({children, onClick, fullWidth}) => {
    return (
        <button className={clsx(styles.button, fullWidth && styles.button_fullWidth)} onClick={onClick}>
            {children}
        </button>
    );
};

export {Button};