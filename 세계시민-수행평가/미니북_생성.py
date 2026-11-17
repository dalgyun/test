"""세계시민 미니북(A4 1장 = 8칸) HTML 생성기.

A4 가로 한 장을 4열 x 2행으로 나눈 '한 장 접이 미니북' 배치로 만든다.
윗줄은 거꾸로(180도) 배치해야 접었을 때 바로 읽힌다.

  윗줄(거꾸로):  5쪽 | 4쪽 | 3쪽 | 2쪽
  아랫줄:        6쪽 | 7쪽 | 8쪽(뒤표지) | 1쪽(앞표지)

1쪽 = 1면(표지), 2~6쪽 = 2~6면, 7쪽 = 참고 자료, 8쪽 = 뒤표지
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT = Path.home() / ".fonts" / "NotoSansKR-VF.ttf"

CSS = """
@font-face{font-family:'NK';src:url('%s');font-weight:100 900;}
:root{--main:#c05621;--dark:#7b341e;--soft:#fffaf0;--line:#fbd38d;--blue:#2b6cb0;--gray:#718096;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'NK',sans-serif;color:#222;word-break:keep-all;-webkit-print-color-adjust:exact}
.panel{width:74.25mm;height:105mm;padding:4.5mm 4.2mm 4mm;overflow:hidden;position:relative;
  font-size:6.7pt;line-height:1.42;display:flex;flex-direction:column;background:#fff}
.hd{display:flex;align-items:center;gap:1.5mm;border-bottom:.6mm solid var(--main);padding-bottom:1mm;margin-bottom:1.6mm}
.hd .no{background:var(--main);color:#fff;font-weight:800;border-radius:1mm;padding:.2mm 1.6mm;font-size:7pt}
.hd .tt{font-weight:800;color:var(--dark);font-size:7.8pt;line-height:1.25}
h4{font-size:6.8pt;color:var(--main);margin:1.4mm 0 .4mm}
ul,ol{padding-left:3.2mm} li{margin:.15mm 0}
b{color:var(--dark)}
.box{border:.3mm solid var(--line);background:var(--soft);border-radius:1.2mm;padding:1mm 1.6mm;margin:.9mm 0}
.box .h{font-weight:800;color:var(--dark);font-size:6.6pt}
.cp{border-left:.8mm solid var(--blue);background:#ebf8ff;border-radius:0 1.2mm 1.2mm 0;padding:.9mm 1.6mm;margin:.9mm 0}
.cp .h{font-weight:800;color:#2c5282;font-size:6.6pt}
figure{margin:1.2mm 0 0}
figure img{width:100%%;display:block;border-radius:.8mm;object-fit:cover}
figcaption{font-size:5.4pt;line-height:1.35;color:#2d3748;margin-top:.5mm}
.cr{display:block;color:var(--gray);font-size:4.8pt}
.ph{border:.4mm dashed #a0aec0;border-radius:1.2mm;color:var(--gray);text-align:center;font-size:5.8pt;
  display:flex;align-items:center;justify-content:center;flex-direction:column;padding:1mm}
table{border-collapse:collapse;width:100%%;font-size:5.6pt;margin:.6mm 0}
th,td{border:.2mm solid #cbd5e0;padding:.3mm .6mm;text-align:center}
th{background:#fefcbf}
.pn{position:absolute;bottom:1.6mm;left:0;right:0;text-align:center;font-size:5pt;color:#a0aec0}
/* 표지 */
.cover{border:.7mm solid var(--main);border-radius:3mm;flex:1;display:flex;flex-direction:column;align-items:center;
  text-align:center;padding:2.5mm 3mm;background:linear-gradient(#fffaf0,#fff 45%%)}
.who{align-self:flex-end;font-size:6pt;border:.2mm solid #cbd5e0;border-radius:1mm;padding:.3mm 1.6mm;background:#fff}
.kicker{margin-top:3mm;font-size:6pt;color:var(--gray);letter-spacing:.6mm}
.title{font-size:15pt;font-weight:900;color:var(--dark);line-height:1.25;margin:.8mm 0}
.sub{font-size:6.8pt;color:var(--main);font-weight:700}
.meaning{margin-top:auto;text-align:left;border-top:.4mm dashed var(--line);padding-top:1.6mm;width:100%%}
.meaning .h{font-weight:800;color:var(--dark);font-size:6.8pt}
"""

GLOBE = """<svg viewBox="0 0 230 210" style="width:%s;margin:%s">
<circle cx="115" cy="88" r="66" fill="#4299e1"/>
<path d="M78 52c14-10 34-8 40 4 6 12-8 18-4 30 4 10-10 16-22 10-12-6-26-4-28-18-2-12 4-20 14-26z" fill="#48bb78"/>
<path d="M138 40c12 0 26 10 28 24 2 12-10 14-14 26-4 10-16 6-18-6-2-10-10-16-6-28 2-10 4-16 10-16z" fill="#48bb78"/>
<path d="M120 118c10-2 22 2 24 10 1 6-8 8-16 8-10 0-16-4-16-10 0-4 4-7 8-8z" fill="#48bb78"/>
<ellipse cx="115" cy="88" rx="66" ry="22" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<ellipse cx="115" cy="88" rx="26" ry="66" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>
<path d="M20 120h190c0 50-42 78-95 78S20 170 20 120z" fill="#dd6b20"/>
<rect x="20" y="114" width="190" height="10" rx="5" fill="#c05621"/>
<path d="M40 140c20 6 130 6 150 0" stroke="#fbd38d" stroke-width="4" fill="none" stroke-dasharray="2 10" stroke-linecap="round"/>
<rect x="190" y="20" width="8" height="70" rx="4" fill="#a0aec0" transform="rotate(20 194 55)"/>
<ellipse cx="206" cy="18" rx="12" ry="17" fill="#a0aec0" transform="rotate(20 206 18)"/>
</svg>"""


def hd(no, title):
    return f'<div class="hd"><span class="no">{no}</span><span class="tt">{title}</span></div>'


P = {}

P[1] = f"""
<div class="cover">
  <div class="who">2학년 ○반 ○번 ○○○</div>
  <div class="kicker">세계 시민 미니북</div>
  <div class="title">모두의 밥상,<br>하나의 지구</div>
  <div class="sub">굶주림 없는 세상을 꿈꾸는 세계 시민</div>
  {GLOBE % ('34mm', '2.5mm 0 1mm')}
  <div class="meaning">
    <div class="h">세계 시민이란?</div>
    <p>국가와 민족의 경계를 넘어 자신을 <b>지구 공동체의 한 구성원</b>으로 여기고,
    인류가 함께 겪는 문제를 해결하기 위해 <b>책임감 있게 행동하는 사람</b>이다.</p>
  </div>
</div>"""

P[2] = f"""
{hd('2면', '세계 시민이 겪는 문제: 기아(굶주림)')}
<p><b>기아</b>란 오랫동안 충분히 먹지 못해 건강한 생활을 할 수 없는 상태다.
세계 식량은 모두가 먹기에 충분한데도 2025년 <b>약 13명 중 1명(6억 4,500만 명)</b>이 굶주렸다.</p>
<h4>발생 원인</h4>
<ol>
  <li><b>분쟁:</b> 농사·식량 운송이 막힌다.</li>
  <li><b>기후 변화:</b> 가뭄·홍수로 수확이 준다.</li>
  <li><b>빈곤·불평등:</b> 식량을 살 돈이 없다.</li>
  <li><b>식량 낭비:</b> 생산량의 약 1/3이 버려진다.</li>
</ol>
<h4>구체적 사례</h4>
<ul>
  <li><b>러시아–우크라이나 전쟁(2022~):</b> 밀 수출이 막혀 곡물값이 오르고 중동·아프리카가 피해를 입었다.</li>
  <li><b>수단 내전(2023~):</b> 2024년 다르푸르 난민촌에서 '기근'이 공식 확인되었다.</li>
</ul>
<figure>
  <img src="사진/2면_분쟁지역_굶주림_남수단.jpg" style="height:27mm">
  <figcaption>분쟁을 피해 온 사람들이 나뭇잎과 풀로 끼니를 잇는다. (남수단)
  <span class="cr">사진: Oxfam East Africa / Wikimedia Commons / CC BY 2.0</span></figcaption>
</figure>"""

P[3] = f"""
{hd('3면', '기아가 세계에 미치는 영향')}
<div class="box"><div class="h">개인적 차원</div>
<ul><li>영양실조로 성장·두뇌 발달이 늦어지고 병에 약해진다.</li>
<li>아이들이 학교 대신 일터로 가서 <b>가난이 대물림</b>된다.</li>
<li>곡물 자급률이 약 20%인 우리나라도 세계 곡물값이 오르면 라면·빵 값이 오른다.</li></ul></div>
<div class="box"><div class="h">사회적 차원</div>
<ul><li>일할 사람이 줄어 <b>경제 발전이 늦어진다</b>.</li>
<li>식량을 두고 다툼·폭동·범죄가 늘어난다.</li>
<li>의료비 부담이 커지고 교육 같은 공공 서비스가 무너진다.</li></ul></div>
<div class="box"><div class="h">국제적 차원</div>
<ul><li>먹을 것을 찾아 떠나는 <b>난민</b>이 늘어 주변국에 부담이 된다.</li>
<li>굶주림 → 분쟁 → 굶주림의 <b>악순환</b>이 생긴다.</li>
<li>식량 위기가 세계 곡물값과 <b>세계 경제</b>를 흔든다.</li></ul></div>
<p style="margin-top:1mm"><b>정리:</b> 기아는 한 사람의 배고픔이 아니라 사회의 발전과 세계 평화를 위협하는 <b>모두의 문제</b>다.</p>"""

P[4] = f"""
{hd('4면', '해결 방안과 기대 효과')}
<div class="box"><div class="h">개인적 차원</div>
<p>먹을 만큼만 덜어 <b>음식 남기지 않기</b>, 공정무역 제품 사기, 기부·캠페인 참여</p></div>
<div class="box"><div class="h">사회적 차원</div>
<p><b>푸드뱅크</b> 늘리기, 기업의 남는 식품 기부, <b>소비기한 표시제</b> 알리기</p></div>
<div class="box"><div class="h">국제적 차원</div>
<p><b>긴급 식량 원조</b>, 개발도상국 <b>농업 기술 지원</b>, 기후 변화 공동 대응(SDGs 2번 '기아 종식')</p></div>
<h4>기대 효과</h4>
<div class="cp"><div class="h">인간 안보</div>
<p>국가가 아닌 <b>사람 한 명 한 명</b>이 공포와 결핍에서 벗어나 안전하게 사는 것.
굶주림이 줄면 <b>'결핍으로부터의 자유'</b>가 보장되어 인간 안보가 실현된다.</p></div>
<div class="cp"><div class="h">적극적 평화</div>
<p>갈퉁은 전쟁이 없는 <b>소극적 평화</b>를 넘어 가난·굶주림 같은 <b>구조적 폭력</b>까지 사라진 상태를
<b>적극적 평화</b>라 했다. 기아 해결은 구조적 폭력을 없애 적극적 평화로 가는 길이다.</p></div>"""

P[5] = f"""
{hd('5면', '기아 해결을 돕는 기구: 유엔 세계식량계획(WFP)')}
<div style="display:flex;gap:1.6mm;align-items:center">
  <img src="사진/5면_WFP_로고.png" style="width:10mm;height:10mm;border-radius:1mm">
  <p>UN 산하 <b>국제기구</b> · 1961년 설립<br>본부: 이탈리아 로마</p>
</div>
<h4>설립 목적</h4>
<p>긴급 상황에서 <b>생명을 구하고</b>, 스스로 식량을 마련하도록 도와 <b>굶주림을 없애는 것(Zero Hunger)</b></p>
<h4>주요 활동</h4>
<ul><li><b>긴급 식량 지원:</b> 전쟁·재난 지역에 식량 전달</li>
<li><b>학교 급식:</b> 아이들의 영양과 교육을 함께 지킴</li>
<li><b>자립 지원:</b> 농지·저수지 만들기에 참여하면 식량·현금 지원</li></ul>
<h4>기여 방식</h4>
<ul><li>2025년 <b>1억 명 이상</b> 지원 (120여 개 나라·지역)</li>
<li><b>2020년 노벨 평화상</b> 수상</li>
<li>한국도 예전에 도움받았지만 지금은 돕는 나라</li></ul>
<figure>
  <img src="사진/5면_WFP_수단_식량운반.jpg" style="height:21mm">
  <figcaption>수단에서 WFP 밀가루 포대를 나르는 모습 (2024)
  <span class="cr">사진: WFP/Abubaker Garelnabei / Wikimedia Commons / CC BY 4.0</span></figcaption>
</figure>"""

P[6] = f"""
{hd('6면', '세계 시민으로서 나의 실천')}
<h4 style="margin-top:0">실천 행동 목록</h4>
<ol><li>급식 <b>잔반 0</b> 도전 (먹을 만큼만 받기)</li>
<li>가족과 장보기 목록 만들기</li>
<li><b>공정무역</b> 제품 골라 사기</li>
<li>기아 문제 카드뉴스 공유하기</li>
<li>WFP 앱으로 한 끼 기부하기</li></ol>
<h4>실천 기록</h4>
<table><tr><th>날짜</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th></tr>
<tr><td>잔반 0</td><td>○</td><td>○</td><td>△</td><td>○</td><td>○</td></tr></table>
<div class="ph" style="height:24mm"><b>[실천 사진 붙이는 곳]</b>직접 찍은 사진 1장 이상</div>
<h4>실천하고 느낀 점</h4>
<p>처음부터 먹을 만큼만 받으니 생각보다 쉽게 잔반을 줄일 수 있었다. 내가 버리던 음식이 누군가에게는
한 끼가 될 수 있다는 것을 느꼈다. 작은 습관이 모이면 세계도 바뀔 수 있다고 믿는다.</p>"""

P[7] = f"""
{hd('부록', '참고 자료 및 사진 출처')}
<h4 style="margin-top:0">참고 도서</h4>
<p>『오늘부터 나는 세계 시민입니다』, 공윤희·윤예림, 창비교육</p>
<h4>참고 자료</h4>
<ul><li>FAO 등, 「세계 식량 안보와 영양 현황 2026」</li>
<li>유엔 세계식량계획(WFP) 누리집</li>
<li>유엔 지속가능발전목표(SDGs) 2번 '기아 종식'</li></ul>
<h4>사진 출처</h4>
<ul><li>2면: Oxfam East Africa (Aimee Brown), Wikimedia Commons, CC BY 2.0</li>
<li>5면: WFP/Abubaker Garelnabei, Wikimedia Commons, CC BY 4.0</li>
<li>5면 로고: World Food Programme, Wikimedia Commons</li>
<li>6면: 직접 촬영</li></ul>
<div class="cp" style="margin-top:2.5mm"><div class="h">SDGs 2번 · 기아 종식</div>
<p>2030년까지 굶주림을 끝내고, 모든 사람이 일 년 내내 안전하고 영양가 있는 음식을 충분히 먹을 수 있게 한다.</p></div>"""

P[8] = f"""
<div class="cover" style="justify-content:center;gap:2mm">
  {GLOBE % ('24mm', '0')}
  <div class="title" style="font-size:10pt">음식을 남기지 않는 것,<br>세계 시민의 첫걸음</div>
  <p style="color:var(--gray);font-size:5.8pt;margin-top:2mm">2학년 도덕 수행평가<br>세계 시민 프로젝트</p>
</div>"""


def panel(n, upside=False, show_no=True):
    style = ' style="transform:rotate(180deg)"' if upside else ''
    num = f'<div class="pn">{n}</div>' if show_no and n not in (1, 8) else ''
    return f'<div class="panel"{style}>{P[n]}{num}</div>'


def page(head_css, body):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>세계시민 미니북</title>'
            f'<style>{CSS % FONT.as_uri()}{head_css}</style></head><body>{body}</body></html>')


def build_print():
    css = """
@page{size:297mm 210mm;margin:0}
.sheet{width:297mm;height:210mm;display:grid;grid-template-columns:repeat(4,74.25mm);grid-template-rows:105mm 105mm;position:relative;break-after:page}
.guide{position:absolute;inset:0;pointer-events:none}
.howto{width:297mm;height:210mm;padding:14mm 18mm;font-size:10.5pt;line-height:1.75}
.howto h2{color:var(--dark);border-bottom:.8mm solid var(--main);padding-bottom:2mm;margin-bottom:4mm;font-size:16pt}
.howto ol{padding-left:6mm} .howto li{margin:1.2mm 0}
.howto .map{display:grid;grid-template-columns:repeat(4,30mm);grid-template-rows:16mm 16mm;border:.4mm solid #4a5568;width:120mm;margin:4mm 0}
.howto .map div{border:.2mm dashed #a0aec0;display:flex;align-items:center;justify-content:center;font-size:9pt;font-weight:700}
.howto .map .up{transform:rotate(180deg);color:var(--main)}
"""
    order = [(5, True), (4, True), (3, True), (2, True), (6, False), (7, False), (8, False), (1, False)]
    cells = ''.join(panel(n, up) for n, up in order)
    guide = """<svg class="guide" viewBox="0 0 297 210" width="297mm" height="210mm">
<g stroke="#cbd5e0" stroke-width=".25" stroke-dasharray="1.5 1.5">
<line x1="74.25" y1="0" x2="74.25" y2="210"/><line x1="148.5" y1="0" x2="148.5" y2="210"/>
<line x1="222.75" y1="0" x2="222.75" y2="210"/><line x1="0" y1="105" x2="297" y2="105"/></g>
<line x1="74.25" y1="105" x2="222.75" y2="105" stroke="#e53e3e" stroke-width=".5"/>
<text x="148.5" y="103.6" font-size="2.4" fill="#e53e3e" text-anchor="middle">✂ 빨간 선만 자르기</text>
</svg>"""
    names = {1: '1면 표지', 2: '2면', 3: '3면', 4: '4면', 5: '5면', 6: '6면', 7: '참고 자료', 8: '뒤표지'}
    mp = ''.join(f'<div class="{"up" if up else ""}">{names[n]}</div>' for n, up in order)
    howto = f"""<div class="howto">
<h2>미니북 접는 방법 (A4 한 장 → 8쪽 미니북)</h2>
<ol>
<li>1쪽만 <b>A4 가로, 실제 크기(100%)</b>로 인쇄한다. (이 안내 쪽은 인쇄하지 않아도 된다.)</li>
<li>종이를 <b>위아래 반</b>으로 접었다 편다. → 다시 <b>좌우 반</b>으로 접었다 펴고, 각 반을 또 반으로 접었다 펴서 8칸 접는 선을 만든다.</li>
<li>종이를 <b>좌우 반</b>으로 접은 상태에서, 접힌 쪽 가운데의 가로선(<b>빨간 선</b>)을 따라 다음 접는 선까지 <b>한 칸 길이만</b> 자른다.</li>
<li>종이를 펴고 그림이 바깥으로 오게 <b>위아래 반</b>으로 접은 뒤, 양 끝을 가운데로 밀면 가운데 구멍이 벌어지며 십자 모양이 된다.</li>
<li>책처럼 접어 정리하면 <b>앞표지(1면) → 2~6면 → 참고 자료 → 뒤표지</b> 순서의 미니북이 완성된다.</li>
</ol>
<p style="margin-top:3mm"><b>인쇄 면 배치</b> (윗줄은 거꾸로 인쇄되는 것이 정상입니다)</p>
<div class="map">{mp}</div>
</div>"""
    body = f'<div class="sheet">{cells}{guide}</div>{howto}'
    return page(css, body)


def build_read():
    css = "@page{size:74.25mm 105mm;margin:0}.panel{break-after:page}"
    return page(css, ''.join(panel(n, show_no=False) for n in range(1, 9)))


if __name__ == '__main__':
    (HERE / '2차_미니북_인쇄용.html').write_text(build_print(), encoding='utf-8')
    (HERE / '2차_미니북_보기용.html').write_text(build_read(), encoding='utf-8')
    print('ok')
