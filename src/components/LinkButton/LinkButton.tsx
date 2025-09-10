import type {FC, ReactNode} from 'react';
import {Button as AntdButton} from 'antd';
import styles from './LinkButton.module.scss';

type TLinkButtonProps = {
    children: ReactNode;
    onClick: () => void;
    icon?: ReactNode;
};

const LinkButton: FC<TLinkButtonProps> = ({children, onClick, icon}) => {
    return (
        <AntdButton 
            type="link"
            size="middle"
            onClick={onClick}
            icon={icon}
            className={styles.linkBtn}
        >            
            {children}
        </AntdButton>
    );
};

export {LinkButton};