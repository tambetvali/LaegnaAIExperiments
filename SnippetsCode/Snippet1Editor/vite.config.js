import { resolve } from 'path'

export default {
  build: {
    rollupOptions: {
      input: resolve(__dirname, 'frontend/main.js'),
      output: {
        entryFileNames: 'assets/main.js',
      },
    },
    outDir: 'static/js',
    emptyOutDir: true,
  },
}