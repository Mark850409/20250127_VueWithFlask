import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import fs from 'fs'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // 明確指定環境檔案路徑
  const envDir = __dirname
  const envFile = mode === 'development' ? '.env.development' : '.env.production'
  const envPath = path.resolve(envDir, envFile)

  // 確保環境檔案存在
  if (!fs.existsSync(envPath)) {
    console.error(`環境檔案不存在: ${envPath}`)
    process.exit(1)
  }

  // 只載入指定的環境檔案
  const env = loadEnv(mode, envDir, '')
  
  console.log('Build Info:', {
    mode,
    command,
    envFile,
    envPath,
    loadedEnv: env
  })

  // 根據模式設定預設值
  const defaultConfig = {
    development: {
      apiUrl: 'http://localhost:5000',
      backendUrl: 'http://localhost:5000'
    },
    production: {
      apiUrl: 'https://backend-recommend-app.azurewebsites.net/api',
      backendUrl: 'https://backend-recommend-app.azurewebsites.net'
    }
  }[mode]

  return {
    plugins: [vue()],
    envDir: envDir,
    envFile: envFile, // 明確指定環境檔案
    server: {
      host: '0.0.0.0',
      port: 3000,
      proxy: {
        '/api': {
          target: mode === 'development' 
            ? defaultConfig.backendUrl 
            : (env.VITE_BACKEND_URL || defaultConfig.backendUrl),
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '/api'),
          secure: false
        }
      }
    },
    build: {
      sourcemap: mode === 'development'
    },
    css: {
      postcss: {
        plugins: [
          require('tailwindcss'),
          require('autoprefixer'),
        ],
      }
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    define: {
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: mode === 'development',
      'process.env': {
        ...env,
        MODE: mode,
        VITE_API_URL: mode === 'development' 
          ? defaultConfig.apiUrl 
          : (env.VITE_API_URL || defaultConfig.apiUrl),
        VITE_BACKEND_URL: mode === 'development'
          ? defaultConfig.backendUrl
          : (env.VITE_BACKEND_URL || defaultConfig.backendUrl)
      }
    }
  }
}) 