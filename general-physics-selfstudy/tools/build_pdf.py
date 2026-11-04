#!/usr/bin/env python3
"""장별 마크다운을 한 권의 PDF로 묶는다.

필요한 것: pandoc, node + playwright(chromium), npm 패키지 mathjax@3,
          Noto CJK KR 폰트, 파이썬 패키지 pypdf
사용법:   python3 tools/build_pdf.py <mathjax 패키지 폴더> <출력 PDF 경로>

동작
1. 장마다 pandoc으로 HTML을 만들고, Chromium으로 PDF를 인쇄한다(MathJax CHTML로 수식 렌더링).
   한 번에 인쇄하면 수식이 너무 많아 브라우저가 멈추므로 장별로 나눈다.
2. 표지와 차례(쪽번호 포함)를 만든다.
3. 모두 합친 뒤 쪽번호를 찍고, PDF 책갈피(북마크)를 단다.
"""
import os, re, subprocess, sys, datetime, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'chapters')
CSS = os.path.join(ROOT, 'tools', 'book.css')
mathjax_dir, out_pdf = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
work = os.path.join(os.path.dirname(out_pdf), '_build')
os.makedirs(work, exist_ok=True)
MJ = os.path.join(mathjax_dir, 'es5', 'tex-chtml-full.js')
MJ_FONTS = 'file://' + os.path.join(mathjax_dir, 'es5', 'output', 'chtml', 'fonts', 'woff-v2')

def order_key(f):
    m = re.match(r'ch(\d+)', f)
    if m: return (0, int(m.group(1)))
    if f.startswith('special'): return (1, f)
    if f.startswith('appendix'): return (2, f)
    return (3, f)

files = sorted([f for f in os.listdir(CH) if f.endswith('.md')], key=order_key)
if os.environ.get('ONLY'):  # 시험용: ONLY=ch01 처럼 일부 장만
    files = [f for f in files if f.startswith(os.environ['ONLY'])]

# 수식은 CHTML(웹폰트)로 렌더링한다. SVG보다 PDF가 절반 정도로 작다.
# 본문 폭보다 넓은 별도 줄 수식은 폭에 맞게 줄인다(MathJax 3은 자동 줄바꿈이 없다).
MJ_CFG = r'''<script>
window.MathJax = {
  tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']], processEscapes: true },
  chtml: { fontURL: '%s' },
  startup: { pageReady: () => MathJax.startup.defaultPageReady().then(() => document.fonts.ready).then(() => {
      for (const c of document.querySelectorAll('mjx-container[display="true"]')) {
        const b = c.closest('p,li,blockquote,td,th,div,body'), cs = getComputedStyle(b);
        const avail = b.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        const need = c.firstElementChild.getBoundingClientRect().width;
        if (need > avail) c.style.zoom = (avail / need * 0.98).toFixed(3);
      }
      document.body.setAttribute('data-mj-done', '1'); }) }
};
</script>''' % MJ_FONTS

def md_to_html(md_path, html_path, title, with_math=True):
    cmd = ['pandoc', md_path, '-f', 'gfm+tex_math_dollars',
           '-t', 'html5', '-s', '--metadata', f'pagetitle={title}', '--css', CSS, '-o', html_path]
    if with_math:
        cmd.insert(-2, f'--mathjax={MJ}')
    subprocess.run(cmd, check=True)
    h = open(html_path, encoding='utf-8').read()
    # pandoc가 넣는 외부 polyfill 스크립트는 오프라인에서 로딩을 막으므로 지운다
    h = re.sub(r'<script src="https://polyfill\.io[^"]*"></script>\s*', '', h)
    if with_math and os.path.basename(MJ) not in h:  # 수식이 없는 문서에는 pandoc이 MathJax를 넣지 않는다
        with_math = False
    if with_math:
        # 설정은 MathJax 스크립트보다 먼저 와야 한다
        h = h.replace('<head>', '<head>\n' + MJ_CFG, 1)
    else:
        h = h.replace('</body>', '<script>document.body.setAttribute("data-mj-done","1")</script></body>', 1)
    open(html_path, 'w', encoding='utf-8').write(h)

PRINT_JS = r'''
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch({ args: ['--disable-dev-shm-usage'] });
  for (const j of jobs) {
    // A4 폭 210mm - 좌우 여백 32mm = 178mm ≈ 673px: 넓은 수식 축소 계산을 인쇄 폭 기준으로 하기 위함
    const p = await b.newPage({ viewport: { width: 673, height: 950 } });
    await p.goto('file://' + j.html, { waitUntil: 'load', timeout: 120000 });
    await p.waitForSelector('body[data-mj-done="1"]', { state: 'attached', timeout: 300000 });
    const errs = await p.$$eval('[data-mjx-error]', e => e.map(x => x.getAttribute('data-mjx-error')));
    await p.pdf({ path: j.pdf, format: 'A4', printBackground: true,
      margin: { top: '18mm', bottom: '20mm', left: '16mm', right: '16mm' } });
    console.log(JSON.stringify({ name: j.name, mathErrors: errs.slice(0, 5), nErr: errs.length }));
    await p.close();
  }
  await b.close();
})();
'''

def print_pdfs(jobs):
    jf = os.path.join(work, 'jobs.json')
    json.dump(jobs, open(jf, 'w'))
    js = os.path.join(work, 'print.js')
    open(js, 'w').write(PRINT_JS)
    r = subprocess.run(['node', js, jf])  # 진행 상황을 바로 출력
    if r.returncode != 0:
        sys.exit(1)

# 1) 장별 HTML → PDF
jobs, titles = [], []
for f in files:
    src = os.path.join(CH, f)
    first = next(l for l in open(src, encoding='utf-8') if l.startswith('# '))
    title = first[2:].strip()
    base = os.path.join(work, os.path.splitext(f)[0])
    md_to_html(src, base + '.html', title)
    jobs.append({'name': f, 'html': base + '.html', 'pdf': base + '.pdf'})
    titles.append(title)
print_pdfs(jobs)

from pypdf import PdfReader, PdfWriter
counts = [len(PdfReader(j['pdf']).pages) for j in jobs]

# 2) 표지와 차례
today = datetime.date.today().strftime('%Y. %m. %d.')
cover_md = os.path.join(work, 'cover.md')
open(cover_md, 'w', encoding='utf-8').write(f'''<div class="titlepage" style="page-break-before:avoid">
<div class="t1">입학 전 자습용<br>일반물리학</div>
<div class="t2">서울대 · KAIST · 연세대 등 주요 대학<br>1학년 일반물리 과정 기반 자습 교재</div>
<div class="t2">역학 · 파동 · 열 · 전자기 · 광학 · 현대물리</div>
<div class="t3">0~40장 · 특집 2 · 부록 3<br>{today} 판</div>
</div>
''')

def part_label(f):
    m = re.match(r'ch(\d+)', f)
    if m:
        n = int(m.group(1))
        for lo, hi, name in [(0, 1, '시작하기 전에'), (2, 14, '제1부 역학'), (15, 17, '제2부 진동과 파동'),
                             (18, 20, '제3부 열역학과 통계물리'), (21, 31, '제4부 전기와 자기'),
                             (32, 34, '제5부 광학'), (35, 40, '제6부 현대물리')]:
            if lo <= n <= hi: return name
    return '특집' if f.startswith('special') else '부록'

def build_toc(start_pages):
    rows, cur = [], None
    for f, t, sp in zip(files, titles, start_pages):
        pl = part_label(f)
        if pl != cur:
            cur = pl
            rows.append(f'<tr class="part"><td colspan="2">{pl}</td></tr>')
        rows.append(f'<tr><td class="t">{t}</td><td class="p">{sp}</td></tr>')
    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="file://{CSS}">
<style>
h1.toc {{ page-break-before: avoid; }}
table.toc {{ width: 100%; border: none; font-size: 10.5pt; }}
table.toc td {{ border: none; padding: 2px 4px; }}
table.toc td.p {{ text-align: right; width: 3em; }}
table.toc tr.part td {{ font-family: "Noto Sans CJK KR"; font-weight: 700; color: #1f4e79; padding-top: 10px; border-bottom: 1px solid #b7c4d4; }}
</style></head><body><h1 class="toc">차례</h1><table class="toc">{''.join(rows)}</table>
<script>document.body.setAttribute("data-mj-done","1")</script></body></html>'''
    p = os.path.join(work, 'toc.html')
    open(p, 'w', encoding='utf-8').write(html)
    return p

md_to_html(cover_md, os.path.join(work, 'cover.html'), '표지', with_math=False)
# 차례 쪽수를 먼저 알아낸 뒤 실제 쪽번호로 다시 만든다
toc_pages = 2
for _ in range(2):
    starts, page = [], 1 + toc_pages + 1
    for c in counts:
        starts.append(page); page += c
    build_toc(starts)
    print_pdfs([{'name': 'cover', 'html': os.path.join(work, 'cover.html'), 'pdf': os.path.join(work, 'cover.pdf')},
                {'name': 'toc', 'html': os.path.join(work, 'toc.html'), 'pdf': os.path.join(work, 'toc.pdf')}])
    n = len(PdfReader(os.path.join(work, 'toc.pdf')).pages)
    if n == toc_pages: break
    toc_pages = n

# 3) 합치기, 쪽번호, 책갈피
# 쪽번호는 페이지 합성(merge_page) 대신 작은 내용 스트림을 덧붙여 찍는다.
# 합성 방식은 페이지마다 자원을 복제해 파일이 거의 두 배가 된다.
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject, NameObject)
w = PdfWriter()
for p in [os.path.join(work, 'cover.pdf'), os.path.join(work, 'toc.pdf')] + [j['pdf'] for j in jobs]:
    w.append(p)
total = len(w.pages)
font = w._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                       NameObject('/Subtype'): NameObject('/Type1'),
                                       NameObject('/BaseFont'): NameObject('/Helvetica')}))
def stream(data):
    st = DecodedStreamObject(); st.set_data(data); return w._add_object(st)
q_open = stream(b'q\n')
for i, pg in enumerate(w.pages):
    if i == 0:  # 표지에는 쪽번호를 찍지 않는다
        continue
    pw = float(pg.mediabox.width)
    label = str(i + 1)
    x = pw / 2 - 8.5 * 0.556 * len(label) / 2  # Helvetica 숫자 폭 0.556em
    num = stream(f'Q\nq 0.4 g BT /FPgNum 8.5 Tf {x:.2f} 28.35 Td ({label}) Tj ET Q\n'.encode())
    old = pg.get('/Contents')
    old = list(old.get_object()) if isinstance(old.get_object(), ArrayObject) else [old]
    pg[NameObject('/Contents')] = ArrayObject([q_open] + old + [num])
    res = pg['/Resources'].get_object()
    fonts = res.get('/Font')
    if fonts is None:
        fonts = DictionaryObject(); res[NameObject('/Font')] = fonts
    fonts = fonts.get_object()
    fonts[NameObject('/FPgNum')] = font

w.add_outline_item('표지', 0)
w.add_outline_item('차례', 1)
parents, cur = {}, None
for f, t, sp in zip(files, titles, starts):
    pl = part_label(f)
    if pl not in parents:
        parents[pl] = w.add_outline_item(pl, sp - 1)
    w.add_outline_item(t, sp - 1, parent=parents[pl])
w.add_metadata({'/Title': '입학 전 자습용 일반물리학', '/Author': '입학 전 자습용 일반물리학 편집'})
w.page_mode = '/UseOutlines'
with open(out_pdf, 'wb') as fo:
    w.write(fo)
print(f'완료: {out_pdf} ({total}쪽)')
