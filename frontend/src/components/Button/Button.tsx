import type {FC, ReactNode} from 'react';
import styles from './Button.module.scss';
import clsx from 'clsx';

type TButtonProps = {
    children?: ReactNode;
    onClick?: () => void;
    fullWidth?: boolean;
    bold?: boolean;
};

const Button: FC<TButtonProps> = ({children, onClick, fullWidth, bold}) => {
    return (
        <button 
            className={
                clsx(styles.button, fullWidth && styles.button_fullWidth, bold && styles.button_bold)
            } 
            onClick={onClick}
        >
            {children}
        </button>
    );
};

export {Button};