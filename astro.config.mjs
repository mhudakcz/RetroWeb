import { defineConfig } from 'astro/config';

// Web o retro hraní – statický výstup.
export default defineConfig({
  site: 'https://retroweb.local',
  build: {
    format: 'directory',
  },
});
