import {memo, Suspense} from 'react';
import {Route, Routes} from 'react-router-dom';
import type {TAppRouterProps} from './routeConfig';
import {routeConfig} from './routeConfig';

const renderWithWrapper = (route: TAppRouterProps) => {
    const element = <Suspense fallback={"загрузка..."}>{route.element}</Suspense>;

    return <Route key={route.path} path={route.path} element={element} />;
};

const AppRouter = memo(() => <Routes>{Object.values(routeConfig).map(renderWithWrapper)}</Routes>);

export {AppRouter};