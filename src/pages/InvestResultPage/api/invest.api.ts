import type {AxiosPromise} from 'axios';
import {makeApiRequest, Methods} from '../../../services';
import { BASE_URL } from '../../../services/api';

export const postInvestCalculate = (
    annual_interest_rate: number,
    starting_capital: number,
    years: number,
): AxiosPromise => {
    const url = BASE_URL + 'api/calculate_investment_forecast/';

    return makeApiRequest({
        method: Methods.POST,
        url,
        data: {
            annual_interest_rate: annual_interest_rate,
            starting_capital: starting_capital,
            years: years
        }
    });
};

export const investApi = {
    postInvestCalculate,
};