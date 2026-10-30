import base from './R7/app/vite.config.js';
export default {...base, cacheDir: new URL('./.review-vite-cache-R7', import.meta.url).pathname};
