import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Web o retro hraní – statický výstup.
export default defineConfig({
  site: 'https://retrowebcz.netlify.app',
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'cs',
        locales: { cs: 'cs', en: 'en', de: 'de', fr: 'fr' },
      },
    }),
  ],
  i18n: {
    defaultLocale: 'cs',
    locales: ['cs', 'en', 'de', 'fr'],
    routing: {
      prefixDefaultLocale: false, // čeština na /, angličtina /en/, němčina /de/, francouzština /fr/
    },
  },
  build: {
    format: 'directory',
  },
});
