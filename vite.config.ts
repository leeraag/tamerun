import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


// https://vite.dev/config/
export default defineConfig({
  	plugins: [react()],
	base: './',
	server: {
		host: true,
		port: 443,
		hmr: false,
		allowedHosts: ['tamerun-invest.ru'],
	},
	optimizeDeps: {
		noDiscovery: true,
		include: []
	}
})
