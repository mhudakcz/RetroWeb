// Vytáhne statická pole z hardware.ts (kind, tagline, intro, specs, canPlay, options)
// do překladových chunků .i18n-work/chunks/hardware_meta_NNN.json (1 zařízení = 1 chunk).
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.argv[2] || '.');
const src = fs.readFileSync(path.join(ROOT, 'src/data/hardware.ts'), 'utf8');

const start = src.indexOf('export const hardware');
const arrStart = src.indexOf('[', start);
const arrEnd = src.indexOf('\n];', arrStart);
const literal = src.slice(arrStart, arrEnd + 2);
// eslint-disable-next-line no-eval
const hardware = eval('(' + literal + ')');

const CH = path.join(ROOT, '.i18n-work', 'chunks');
fs.mkdirSync(CH, { recursive: true });

hardware.forEach((h, i) => {
  const obj = {
    [h.slug]: {
      kind: h.kind,
      tagline: h.tagline,
      intro: h.intro,
      specs: h.specs,
      canPlay: h.canPlay,
      options: h.options,
    },
  };
  const p = path.join(CH, `hardware_meta_${String(i).padStart(3, '0')}.json`);
  fs.writeFileSync(p, JSON.stringify(obj, null, 1), 'utf8');
});
console.log(`hardware_meta chunků: ${hardware.length}`);
