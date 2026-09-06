import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Web o retro hraní – statický výstup.
// Nahled na GitHub Pages stavi jen cestinu (ONLY_CS=1). Promenna se sem musi
// dostat pres vite.define: Astro pousti do import.meta.env jen promenne s
// prefixem PUBLIC_ a holy process.env se v modulech pri buildu neprojevi.
const ONLY_CS = process.env.ONLY_CS === '1';

export default defineConfig({
  vite: {
    define: { __ONLY_CS__: JSON.stringify(ONLY_CS) },
  },
  site: 'https://retrowebcz.netlify.app',
  integrations: [
    sitemap({
      // osobni stranky do sitemap nepatri — pro nepřihlaseneho jsou prazdne
      filter: (stranka) => !/\/(prihlaseni|muj-seznam|admin)\/?$/.test(stranka),
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
