import type {AxiosPromise} from 'axios';
import {makeApiRequest, Methods} from '../../../services';
import type { TInstallmentSettings } from '../InstallmentResultPage.types';
import { BASE_URL } from '../../../services/api';

export const postInstallmentCalculate = (
    property_price: number,
    initial_payment_date: string | null,
    installmentSettings: TInstallmentSettings,
): AxiosPromise => {
    const url = BASE_URL + 'api/calculate_payment_schedule';

    return makeApiRequest({
        method: Methods.POST,
        url,
        data: {
            property_price: property_price,
            initial_payment_date: initial_payment_date,
            ...installmentSettings
        }
    });
};

export const postDownloadPdfSchedule = (
    property_price: number,
    initial_payment_date: string | null,
    installmentSettings: TInstallmentSettings,
): AxiosPromise => {
    const url = BASE_URL + 'api/download_pdf_payment_schedule';

    return makeApiRequest({
        method: Methods.POST,
        url,
        type: 'blob',
        data: {
            property_price: property_price,
            initial_payment_date: initial_payment_date,
            ...installmentSettings
        }
    });
};


export const installmentApi = {
    postInstallmentCalculate,
    postDownloadPdfSchedule,
};