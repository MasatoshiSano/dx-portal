const GLOBAL = 'C:/Users/dw35816/AppData/Roaming/npm/node_modules';
const pptxgen = require(GLOBAL + '/pptxgenjs');
const html2pptx = require('C:/Users/dw35816/.claude/skills/pptx/scripts/html2pptx.js');
const path = require('path');

const DIR = path.resolve(__dirname);

(async () => {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: 'WIDE', width: 10, height: 5.625 });
  pptx.layout = 'WIDE';
  pptx.title = 'DX Portal 集合知化ロードマップ';
  pptx.author = 'DX Portal Team';

  const slides = [
    'slide01.html', // 1: タイトル
    'slide02.html', // 2: Executive Summary
    'slide03.html', // 3: 現状認識（書き直し）
    'slide04b.html',// 4: なぜ全員で共有するのか（新規）
    'slide04.html', // 5: 進め方の全体像
    'slide05.html', // 6: Phase 1 会話例
    'slide06.html', // 7: Phase 2 会話例
    'slide07.html', // 8: Phase 3① 会話例
    'slide08.html', // 9: Phase 3② 会話例
    'slide09.html', // 10: まず来週やること
  ];

  for (const file of slides) {
    console.log(`Rendering ${file}...`);
    await html2pptx(path.join(DIR, file), pptx);
  }

  const out = path.join(DIR, 'roadmap.pptx');
  await pptx.writeFile({ fileName: out });
  console.log(`Done: ${out}`);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
