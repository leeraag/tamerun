import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


// https://vite.dev/config/
export default defineConfig({
  	plugins: [react()],
	build: {
		outDir: 'dist',
		sourcemap: false, // для продакшена лучше отключить
		minify: 'esbuild', // или 'terser'
		rollupOptions: {
		output: {
			manualChunks: {
			vendor: ['react', 'react-dom'],
			// дополнительные чанки для оптимизации
			}
		}
		}
 	},
	base: './',
	server: {
		host: true,
		port: 5173,
		hmr: false,
		allowedHosts: ['0.0.0.0', 'localhost', 'tamerun-invest.ru'],
	},
})
