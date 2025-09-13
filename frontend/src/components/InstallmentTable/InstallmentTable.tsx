import type { FC } from 'react';
import { Button, Table as TableAntd } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { DownloadOutlined } from '@ant-design/icons';
import styles from './InstallmentTable.module.scss';

type TInstallmentTableProps = {
    columns: ColumnsType;
    dataSource: any;
    totalCost: number | null;
    downloadFile?: () => void;
}
const InstallmentTable: FC<TInstallmentTableProps> = ({
    columns,
    dataSource,
    totalCost,
    downloadFile
}) => {
    return (
        <TableAntd
            columns={columns}
            dataSource={dataSource}
            pagination={false}
            scroll={{ y: 150 }}
            style={{
                borderRadius: '0 0 8px 8px',
                overflow: 'hidden',
            }}
            rowKey={(record) => record.month}
            title={() => <p style={{textAlign: "center", margin: '0', fontFamily: 'Stolzl Regular'}}>График платежей Дольщика</p>}
            footer={() => 
                <>
                    <p className={styles.totalCost}>
                        Итого выплачено: {totalCost?.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')} ₽
                    </p>
                    <Button 
                        block
                        type="text"
                        onClick={downloadFile}
                        icon={<DownloadOutlined style={{ fontSize: '20px' }}/>}
                        className={styles.downloadButton}
                    >
                        Выгрузить PDF
                    </Button>
                </>
            }
            className={styles.installmentTable}
            rowClassName={(record) => record.onetime_payment === true ? styles.markedRow : ''}
        />
    );
};

export { InstallmentTable };