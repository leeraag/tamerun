import {useEffect, useState, type FC, type ReactNode} from 'react';
import type { AxiosResponse } from 'axios';
import { useNavigate } from 'react-router-dom';
import { RoutePath } from '../../routes';
import { Tabs } from 'antd';
import { Button, InstallmentTable } from '../../components';
import { downloadFile } from '../../utils/downloadFile';
import { installmentApi } from './api/installment.api';
import { 
    COLUMNS,
    INSTALLMENT_SETTINGS_6,
    INSTALLMENT_SETTINGS_12,
    INSTALLMENT_SETTINGS_18,
    INSTALLMENT_SETTINGS_24,
    INSTALLMENT_SETTINGS_36
} from './InstallmentResultPage.constants';
import type { TInstallmentSettings } from './InstallmentResultPage.types';
import styles from './InstallmentResultPage.module.scss';

type TInstallmentResultPageProps = {
    children?: ReactNode;
};

const InstallmentResultPage: FC<TInstallmentResultPageProps> = ({}) => {
    const [paymentSchedule, setPaymentSchedule] = useState();
    const [totalCost, setTotalCost] = useState<number | null>(null);
    const navigate = useNavigate();

    const finishCalculate = () => {
        localStorage.clear();
        navigate(RoutePath.installment);
    };

    const apart_num = Number(localStorage.getItem('apartNum'));
    const property_price = Number(localStorage.getItem('propertyPrice'));
    const initial_payment_date = localStorage.getItem('initialPaymentDate');

    const fetchInstallment = async (
        property_price: number,
        initial_payment_date: string | null,
        installmentSettings: TInstallmentSettings
    ) => {
        try {
            const response = await installmentApi.postInstallmentCalculate(
                property_price,
                initial_payment_date,
                installmentSettings,
            );
            setPaymentSchedule(response.data.payment_schedule);
            setTotalCost(response.data.total_cost);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchFile = async (
        apart_num: number,
        property_price: number,
        initial_payment_date: string | null,
        installmentSettings: TInstallmentSettings
    ) => {
        try {
            await installmentApi.postDownloadPdfSchedule(
                apart_num,
                property_price,
                initial_payment_date,
                installmentSettings,
            )
            .then((response: AxiosResponse) => {
                downloadFile(response);
            })
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_6);
    }, []);

    const handleTabClick = (key: string) => {
        switch (key) {
            case '6':
                fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_6);
                break;
            case '12':
                fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_12);
                break;
            case '18':
                fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_18);
                break;
            case '24':
                fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_24);
                break;
            case '36':
                fetchInstallment(property_price, initial_payment_date, INSTALLMENT_SETTINGS_36);
        }
    };

    const tabsContent = [
        {
            label: "6 месяцев",
            key: '6',
            children:
                <InstallmentTable 
                    columns={COLUMNS}
                    dataSource={paymentSchedule}
                    totalCost={totalCost}
                    downloadFile={() => 
                        fetchFile(apart_num, property_price, initial_payment_date, INSTALLMENT_SETTINGS_6)
                    } 
                />
        },
        {
            label: "12 месяцев",
            key: '12',
            children: 
                <InstallmentTable 
                    columns={COLUMNS}
                    dataSource={paymentSchedule}
                    totalCost={totalCost}
                    downloadFile={() => 
                        fetchFile(apart_num, property_price, initial_payment_date, INSTALLMENT_SETTINGS_12)
                    } 
                />
        },
        {
            label: "18 месяцев",
            key: '18',
            children: 
                <InstallmentTable 
                    columns={COLUMNS}
                    dataSource={paymentSchedule}
                    totalCost={totalCost}
                    downloadFile={() => 
                        fetchFile(apart_num, property_price, initial_payment_date, INSTALLMENT_SETTINGS_18)
                    } 
                />
        },
        {
            label: "24 месяца",
            key: '24',
            children: 
                <InstallmentTable 
                    columns={COLUMNS}
                    dataSource={paymentSchedule}
                    totalCost={totalCost}
                    downloadFile={() => 
                        fetchFile(apart_num, property_price, initial_payment_date, INSTALLMENT_SETTINGS_24)
                    } 
                />
        },
        {
            label: "36 месяцев",
            key: '36',
            children: 
                <InstallmentTable 
                    columns={COLUMNS}
                    dataSource={paymentSchedule}
                    totalCost={totalCost}
                    downloadFile={() => 
                        fetchFile(apart_num, property_price, initial_payment_date, INSTALLMENT_SETTINGS_36)
                    } 
                />
        },
    ];
    return (
        <section className={styles.container}>
            <div className={styles.tab}>
                <Tabs type="card" items={tabsContent} className={styles.tabs} onTabClick={handleTabClick}/>
                <Button onClick={finishCalculate}>Понятно</Button>
            </div>
        </section>
    );
};

export { InstallmentResultPage };