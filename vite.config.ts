import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


// https://vite.dev/config/
export default defineConfig({
  	plugins: [react()],
	base: './',
	server: {
		host: true,
		port: 5173,
		hmr: false,
		allowedHosts: ['0.0.0.0', 'localhost', 'tamerun-invest.ru'],
	},
})
