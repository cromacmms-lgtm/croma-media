// Renderiza un reel cuadro por cuadro: la página expone DURATION y render(t).
// Uso: node reels/render-reel.js <index.html> <carpeta-salida> [t1,t2,... para pruebas]
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require(process.env.PW_PATH || 'playwright')); }
const CANDIDATES = [process.env.CHROMIUM_PATH, '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'];
(async () => {
  const [html, out, test] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const exe = CANDIDATES.find(p => p && fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  if (test) {
    for (const t of test.split(',').map(Number)) {
      await p.evaluate(t => render(t), t);
      await p.screenshot({ path: path.join(out, `t-${t}.png`) });
    }
  } else {
    const fps = 30, D = await p.evaluate(() => DURATION), n = Math.round(D * fps);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / fps);
      await p.screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 93 });
    }
  }
  await b.close();
})();
