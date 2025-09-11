import { defineConfig } from 'vite'
import dns from 'dns'
import react from '@vitejs/plugin-react'

dns.setDefaultResultOrder('verbatim')

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
})
