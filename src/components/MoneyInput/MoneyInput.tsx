import type { FC } from 'react';
import { InputNumber as InputNumberAntd } from 'antd';
import ruble from '../../assets/images/ruble.svg';

type TMoneyInputProps = {
    value: number | null;
    onChange: (value: number | null) => void;
    className?: string;
}
const MoneyInput: FC<TMoneyInputProps> = ({
    value,
    onChange,
    className,
}) => {
    const formatter = (value: number | undefined) => {
        if (!value) return '';
        
        return `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    };

    return (
        <InputNumberAntd
            style={{ width: '40%' }}
            formatter={formatter}
            step={0.01}
            decimalSeparator=","
            controls={false}
            min={9000000}
            max={1000000000}
            placeholder="Введите сумму"
            suffix={
                <img src={ruble} />
            }
            value={value}
            onChange={onChange}
            className={className}
        />
    );
};

export { MoneyInput };