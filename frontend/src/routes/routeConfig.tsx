import { InvestPage, HomePage, InvestResultPage, InstallmentPage, InstallmentResultPage } from '../pages';
import type {RouteProps} from 'react-router-dom';

export type TAppRouterProps = RouteProps & {
    authOnly?: boolean;
};

export enum AppRouters {
    HOME = 'home',
    INVEST = 'invest',
    INVEST_RESULT = 'invest_result',
    INSTALLMENT = 'installment',
    INSTALLMENT_RESULT = 'installment_result',
}

export const RoutePath: Record<AppRouters, string> = {
    [AppRouters.HOME]: '/',
    [AppRouters.INVEST]: `/${AppRouters.INVEST}`,
    [AppRouters.INVEST_RESULT]: `/${AppRouters.INVEST_RESULT}`,
    [AppRouters.INSTALLMENT]: `/${AppRouters.INSTALLMENT}`,
    [AppRouters.INSTALLMENT_RESULT]: `/${AppRouters.INSTALLMENT_RESULT}`,
};

export const routeConfig: Record<AppRouters, TAppRouterProps> = {
    [AppRouters.HOME]: {
        path: RoutePath.home,
        element: <HomePage />,
    },
    [AppRouters.INVEST]: {
        path: RoutePath.invest,
        element: <InvestPage />,
    },
    [AppRouters.INVEST_RESULT]: {
        path: RoutePath.invest_result,
        element: <InvestResultPage />,
    },
    [AppRouters.INSTALLMENT]: {
        path: RoutePath.installment,
        element: <InstallmentPage />,
    },
    [AppRouters.INSTALLMENT_RESULT]: {
        path: RoutePath.installment_result,
        element: <InstallmentResultPage />,
    },
};