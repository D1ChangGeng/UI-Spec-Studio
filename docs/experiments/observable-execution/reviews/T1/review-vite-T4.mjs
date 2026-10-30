import base from './T4/app/vite.config.js';
export default {...base, cacheDir: new URL('./.review-vite-cache-T4', import.meta.url).pathname};
