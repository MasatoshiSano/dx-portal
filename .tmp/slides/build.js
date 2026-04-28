const path = require('path');
const globalModules = 'C:/Users/dw35816/AppData/Roaming/npm/node_modules';
const pptxgen = require(path.join(globalModules, 'pptxgenjs'));
const html2pptx = require(path.join(process.env.HOME || process.env.USERPROFILE, '.claude/skills/pptx/scripts/html2pptx'));

async function build() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'DX Solutions Group';
  pptx.title = '全員にAI秘書がつく開発と働き方';

  const slideDir = __dirname;
  const slides = [
    'slide1.html', 'slide2.html', 'slide3.html',
    'slide4.html', 'slide5.html', 'slide6.html',
    'slide6b.html', 'slide7.html', 'slide8.html',
    'slide9.html', 'slide10.html', 'slide11.html',
    'slide12.html'
  ];

  for (const file of slides) {
    console.log(`Processing ${file}...`);
    await html2pptx(path.join(slideDir, file), pptx);
  }

  const outPath = path.join(slideDir, '..', 'ai-collaborative-dev-platform.pptx');
  await pptx.writeFile({ fileName: outPath });
  console.log(`Saved to ${outPath}`);
}

build().catch(e => { console.error(e); process.exit(1); });
