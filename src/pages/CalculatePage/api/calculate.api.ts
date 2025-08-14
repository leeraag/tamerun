import type {AxiosPromise} from 'axios';
import {makeApiRequest, Methods} from '../../../services';

export const postInvestCalculate = (sum: number, term: number): AxiosPromise => {
    const url = 'https://calcus.ru/api/v1/Invest';
    const clientId = '40101';
    const apiKey = 'ip5TVjnqrr';

    return makeApiRequest({
        method: Methods.POST,
        url,
        headers: {
            'Api-Client-Id': clientId,
            'Api-Key': apiKey,
        },
        data: {
            type: 1,
            sum: sum,
            period: term,
            period_unit: 'y',
            rate: 20,
        }
    });
};

export const calculateApi = {
    postInvestCalculate,
};