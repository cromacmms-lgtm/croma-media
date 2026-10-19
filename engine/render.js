// Renderiza cada página HTML a JPG. Uso: node engine/render.js jobs.json
// Requiere playwright (npm i playwright). Si hay un Chromium preinstalado, se usa con CHROMIUM_PATH.
const fs = require('fs');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require(process.env.PLAYWRIGHT_MODULE || 'playwright'); }
const fallbacks = [process.env.CHROMIUM_PATH, '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'].filter(Boolean);
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const exe = fallbacks.find(p => fs.existsSync(p));
  const browser = await pw.chromium.launch(exe ? { executablePath: exe } : {});
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await page.goto('file://' + j.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);
    await page.screenshot({ path: j.out, type: 'jpeg', quality: 92 });
    await page.close();
  }
  await browser.close();
})();
