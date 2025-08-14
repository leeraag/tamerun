import { Suspense } from 'react';
import { Layout } from './layout';
import { AppRouter } from './routes';
import { ConfigProvider } from 'antd';

function App() {
  return (
    <>
      <Suspense fallback={"загрузка..."}>
        <ConfigProvider
          theme={{
            token: {
              fontFamily: 'Stolzl Book'
            },
            components: {
              InputNumber: {
                activeBorderColor: "#4A491A",
                hoverBorderColor: "#4A491A",
                activeShadow: "none",
              },
              Select: {
                activeBorderColor: "#4A491A",
                hoverBorderColor: "#4A491A",
                optionSelectedBg: "rgba(74, 73, 26, 0.19)",
                activeOutlineColor: "transparent",
              },
            },
          }}
        >
          <Layout>
            <AppRouter />
          </Layout>
        </ConfigProvider>
      </Suspense>
    </>
  )
}

export default App
