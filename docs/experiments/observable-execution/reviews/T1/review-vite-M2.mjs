import base from './M2/app/vite.config.js';
export default {...base, cacheDir: new URL('./.review-vite-cache-M2', import.meta.url).pathname};
