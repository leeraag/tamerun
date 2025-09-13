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
              Tabs: {
                itemActiveColor: "#005229",
                itemSelectedColor: "#005229",
                itemHoverColor: "#ffffffff",
                itemColor: "#e7fff1ff",
                cardBg: "rgba(0, 0, 0, 0.27)",
              },
              Table: {
                cellPaddingInline: 8,
                cellPaddingBlock: 8,
                rowHoverBg: 'none',
              },
              Pagination: {
                itemSize: 25,
              },
              DatePicker: {
                activeBorderColor: "#4A491A",
                hoverBorderColor: "#4A491A",
                activeShadow: "none",
                cellRangeBorderColor: "#4A491A",
                colorPrimary: "#005229",
              }
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
