// practice.html -> PDF (+ 확인용 페이지 미리보기 PNG)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'practice.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const out = process.argv[2] || path.join(dir, '수행평가2_삼각형의성질_연습문제.pdf');
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-size:8px;color:#868e96;">- <span class="pageNumber"></span> / <span class="totalPages"></span> -</div>',
  });
  console.log('PDF:', out);
  await browser.close();
})();
