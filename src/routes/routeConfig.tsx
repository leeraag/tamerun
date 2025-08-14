import { CalculatePage, ResultPage } from '../pages';
import type {RouteProps} from 'react-router-dom';

export type TAppRouterProps = RouteProps & {
    authOnly?: boolean;
};

export enum AppRouters {
    CALCULATE = 'calculate',
    RESULT = 'result'
}

export const RoutePath: Record<AppRouters, string> = {
    [AppRouters.CALCULATE]: '/',
    [AppRouters.RESULT]: `/${AppRouters.RESULT}`,
};

export const routeConfig: Record<AppRouters, TAppRouterProps> = {
    [AppRouters.CALCULATE]: {
        path: RoutePath.calculate,
        element: <CalculatePage />,
    },
    [AppRouters.RESULT]: {
        path: RoutePath.result,
        element: <ResultPage />,
    }
};