"""미니북 간단판에 붙일 사진만 실제 크기로 모은 A4 인쇄 페이지 생성기.

사진 크기와 자르는 범위는 미니북 간단판(미니북_간단_생성.py)과 같다.
칸 안쪽 너비 65.85mm = 74.25mm(A4 가로 1/4) - 좌우 여백 4.2mm x 2
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT = Path.home() / ".fonts" / "NotoSansKR-VF.ttf"
W = 65.85  # mm

PHOTOS = [
    ('2면', '2면_분쟁지역_굶주림_남수단.jpg', 31, '사진: Oxfam East Africa / CC BY 2.0'),
    ('5면', '5면_WFP_수단_식량운반.jpg', 24, '사진: WFP/Abubaker Garelnabei / CC BY 4.0'),
    ('6면', '6면_실천_공정무역.jpg', 34, '사진: 직접 촬영'),
]


def cell(label, fn, h, credit, spare=False):
    tag = f'{label} 예비' if spare else label
    if (HERE / '사진' / fn).exists():
        pic = f'<img src="사진/{fn}" style="width:{W}mm;height:{h}mm">'
    else:
        pic = f'<div class="miss" style="width:{W}mm;height:{h}mm">사진 파일 없음<br>{fn}</div>'
    return (f'<div class="cell"><div class="cut">{pic}</div>'
            f'<div class="lb"><b>{tag}</b> · {W:.1f}×{h}mm · {credit}</div></div>')


def build():
    cells = ''.join(cell(*p) + cell(*p, spare=True) for p in PHOTOS)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>미니북 사진 인쇄용</title>
<style>
@font-face{{font-family:'NK';src:url('{FONT.as_uri()}');font-weight:100 900;}}
@page{{size:A4;margin:15mm}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'NK',sans-serif;color:#222}}
h1{{font-size:13pt;color:#7b341e;margin-bottom:2mm}}
.hint{{font-size:8.5pt;color:#4a5568;margin-bottom:6mm;line-height:1.5}}
.grid{{display:grid;grid-template-columns:repeat(2,{W}mm);column-gap:20mm;row-gap:9mm}}
.cut{{outline:.2mm dashed #a0aec0;outline-offset:0;line-height:0}}
.cut img{{display:block;object-fit:cover}}
.miss{{display:flex;align-items:center;justify-content:center;text-align:center;font-size:8pt;
  color:#c53030;border:.4mm solid #feb2b2;background:#fff5f5;line-height:1.5}}
.lb{{font-size:6.5pt;color:#718096;margin-top:1.5mm}}
</style></head><body>
<h1>세계시민 미니북 사진 (실제 크기)</h1>
<p class="hint">A4, <b>실제 크기(100%)</b>로 인쇄한 뒤 점선을 따라 잘라 미니북에 붙이세요.
사진마다 예비로 한 장씩 더 넣었습니다. 사진 아래 출처는 미니북에 함께 적어 주세요.</p>
<div class="grid">{cells}</div>
</body></html>"""


if __name__ == '__main__':
    (HERE / '미니북_사진_인쇄용.html').write_text(build(), encoding='utf-8')
    print('ok')
