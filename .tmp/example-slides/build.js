const path = require('path');
const globalModules = path.join(process.env.APPDATA || '', 'npm/node_modules');
const pptxgen = require(path.join(globalModules, 'pptxgenjs'));
const html2pptx = require(path.join(process.env.USERPROFILE || process.env.HOME, '.claude/skills/pptx/scripts/html2pptx'));

async function main() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'DX Portal Team';
  pptx.title = 'AI Collaborative Dev Platform - Examples';

  const slideFiles = [
    'slide-ex1.html',
    'slide-ex2.html',
    'slide-ex3.html',
    'slide-ex4.html',
    'slide-ex5.html',
  ];

  const baseDir = path.resolve(__dirname);

  for (const file of slideFiles) {
    const htmlPath = path.join(baseDir, file);
    console.log(`Processing: ${file}`);
    await html2pptx(htmlPath, pptx);
  }

  const outPath = path.join(baseDir, 'examples.pptx');
  await pptx.writeFile({ fileName: outPath });
  console.log(`Created: ${outPath}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
