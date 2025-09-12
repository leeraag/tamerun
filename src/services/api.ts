import type {AxiosPromise, AxiosRequestConfig} from 'axios';
import axios from 'axios';

const BASE_URL = 'https://tamerun-invest.ru/';

enum Methods {
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    DELETE = 'DELETE',
}

type TRequestOptionsProps = {
    method: Methods;
    url: string;
    data?: any;
    headers?: any;
    type?: 'arraybuffer' | 'blob' | 'document' | 'json' | 'text' | 'stream';
    params?: any;
};

const makeApiRequest = ({method, url, data, headers, type, params}: TRequestOptionsProps): AxiosPromise => {
    const defaultHeaders = axios.create().defaults.headers;

    const config: AxiosRequestConfig = {
        method,
        url: `${url}`,
        headers: {
            ...defaultHeaders,
            'Content-Type': 'application/json',
            ...headers,
        },
        data,
        params,
        responseType: type,
    };

    return axios(config);
};

export {Methods, makeApiRequest, BASE_URL};