export const meta = {
  name: 'ports-verify',
  description: 'Overi navrzena vydani her na dalsich platformach a zamitne vymyslena',
  phases: [{ title: 'Overeni', detail: 'davka vydani na agenta, vystup seznam potvrzenych', model: 'sonnet' }],
}

phase('Overeni')
const { base, batches } = typeof args === 'string' ? JSON.parse(args) : args
const pad = (n) => String(n).padStart(2, '0')

log(`Overeni portu: ${batches} davek`)

const jobs = Array.from({ length: batches }, (_, i) => ({
  i,
  in: `${base}/verify_${pad(i)}.json`,
  out: `${base}/verify_${pad(i)}_out.json`,
}))

const results = await parallel(jobs.map((j) => () => {
  const prompt = `Idempotentni uloha: overeni, ze hra na dane platforme SKUTECNE vysla.

KROK 1 - kontrola: Zkus nastrojem Read otevrit ${j.out}
Pokud EXISTUJE a je to VALIDNI JSON pole, jsi hotov — nic nezapisuj a vrat pouze: SKIP

KROK 2 - podklad: Read ${j.in}
Je to JSON pole objektu {id, name, platform, year}. Kazdy radek je TVRZENI, ze
titul vysel na dane platforme v danem roce.

KROK 3 - prace. U kazdeho radku rozhodni, jestli je tvrzeni pravdive.

Jsi ADVOKAT DABLA: tvym ukolem je najit tvrzeni, ktera neplati. Rada her byla
exkluzivni a snadno se splete port, ktery nikdy nevysel — flOw nikdy nevysel na
PC, Bloodborne neni na Xboxu, Halo neni na PlayStationu. Kdyz si u radku nejsi
JISTY, zamitni ho. Zamitnuty radek se jen nepouzije; potvrzeny se objevi na
webu jako fakt, takze omyl je tam draz.

Zamitni take radek, kde:
- hra na platforme vysla, ale az v jinem roce nez o pet let (spatny rok)
- jde o remaster nebo remake pod jinym nazvem, ne o tutez hru
- jde o zpetnou kompatibilitu nebo cloudovou sluzbu, ne o samostatne vydani

Uloz nastrojem Write do ${j.out} VALIDNI JSON pole objektu:
{"id": <id ze vstupu>, "ok": true|false, "proc": "<kratke zduvodneni u zamitnutych>"}
se VSEMI id ze vstupu. Zadny text mimo JSON.
Vrat kratke potvrzeni s poctem potvrzenych a zamitnutych.`
  return agent(prompt, { label: `overeni:${pad(j.i)}`, phase: 'Overeni', model: 'sonnet' })
}))

return { batches, done: results.filter(Boolean).length }
