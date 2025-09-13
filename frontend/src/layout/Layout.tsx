import type {FC, ReactNode} from 'react';
import { Footer } from '../components';
import styles from './Layout.module.scss';

type TLayoutProps = {
    children?: ReactNode;
};

const Layout: FC<TLayoutProps> = ({children}) => {
    return (
        <main className={styles.layout}>
            <div className={styles.layout__content}>{children}</div>
            <Footer />
        </main>
    );
};

export {Layout};