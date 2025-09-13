import type {FC, ReactNode} from 'react';
import logoRazvitie from '../../assets/images/razvitie.webp';
import logoTamerun from '../../assets/images/tamerun.webp';
import logoMirmax from '../../assets/images/mirmax.webp';

import styles from './Footer.module.scss';

type TFooterProps = {
    children?: ReactNode;
};
const logo = [logoRazvitie, logoTamerun, logoMirmax];

const Footer: FC<TFooterProps> = ({}) => {
    return (
        <footer className={styles.footer}>
            <div className={styles.footer__content}>
                {
                    logo.map((item, index) => (
                        <div key={index} className={styles.footer__item}>
                            <img src={item}/>
                        </div>
                    ))
                }
            </div>
            
        </footer>
    );
};

export {Footer};