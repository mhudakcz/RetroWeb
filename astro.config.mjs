import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Web o retro hraní – statický výstup.
export default defineConfig({
  site: 'https://retrowebcz.netlify.app',
  integrations: [sitemap()],
  build: {
    format: 'directory',
  },
});
