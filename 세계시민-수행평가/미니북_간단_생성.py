"""세계시민 미니북 간단판(손으로 옮겨 쓰기 좋은 분량) 생성기.

배치와 디자인은 미니북_생성.py를 그대로 쓰고, 각 쪽 내용만 짧게 바꾼다.
내용은 WFP 한국사무소 「배고픔을 끝내기 위해」(ko.wfp.org/ending-hunger) 한 페이지로
대부분 쓸 수 있도록 맞췄다.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('base', HERE / '미니북_생성.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.CSS = base.CSS.replace('font-size:6.7pt;line-height:1.42', 'font-size:8.4pt;line-height:1.55')
base.CSS += """
.panel h4{font-size:8.6pt;margin:2.2mm 0 .6mm}
.panel .hd .tt{font-size:9pt}
.panel li{margin:.6mm 0}
.lv{margin:1.4mm 0}
.lv b.k{display:inline-block;background:var(--main);color:#fff;border-radius:1mm;padding:0 1.2mm;margin-right:1mm;font-size:7.6pt}
.key{font-weight:800;color:var(--dark)}
"""
hd = base.hd

P = {}

P[1] = f"""
<div class="cover">
  <div class="who">2학년 ○반 ○번 ○○○</div>
  <div class="kicker">세계 시민 미니북</div>
  <div class="title">모두의 밥상,<br>하나의 지구</div>
  {base.GLOBE % ('38mm', '3mm 0 1mm')}
  <div class="meaning">
    <div class="h">세계 시민이란?</div>
    <p>지구 공동체의 한 사람으로서<br>세계 문제 해결에 함께하는 사람</p>
  </div>
</div>"""

P[2] = f"""
{hd('2면', '세계의 문제: 기아(배고픔)')}
<p>식량은 모두가 먹고도 남지만, <b>6억 명이 넘는 사람</b>이 굶주린다.</p>
<h4>원인</h4>
<p>분쟁 · 기후 위기 · 재난 · 불평등 · 식량 소실</p>
<h4>사례</h4>
<p>배고픈 사람의 <b>60%</b>가 분쟁 지역에 산다. (예멘, 남수단 등)</p>
<figure>
  <img src="사진/2면_분쟁지역_굶주림_남수단.jpg" style="height:31mm">
  <figcaption>나뭇잎으로 끼니를 잇는 남수단 사람들
  <span class="cr">사진: Oxfam East Africa / CC BY 2.0</span></figcaption>
</figure>"""

P[3] = f"""
{hd('3면', '기아가 미치는 영향')}
<div class="lv"><b class="k">개인</b>영양이 부족해 건강을 잃고, 학교 대신 일하러 가서 배우지 못한다.</div>
<div class="lv"><b class="k">사회</b>일할 사람이 줄어 지역 경제가 어려워진다.</div>
<div class="lv"><b class="k">국제</b>배고픔이 갈등과 난민을 낳고, 갈등이 다시 배고픔을 키우는 <span class="key">악순환</span>이 생긴다.</div>
<p style="margin-top:3mm;text-align:center" class="key">기아는 모두의 문제!</p>"""

P[4] = f"""
{hd('4면', '해결 방안과 기대 효과')}
<div class="lv"><b class="k">개인</b>음식 남기지 않기, 기부하기</div>
<div class="lv"><b class="k">사회</b>푸드뱅크, 사회 안전망 만들기</div>
<div class="lv"><b class="k">국제</b>긴급 식량 지원, 재난 조기 경보</div>
<h4>기대 효과</h4>
<div class="cp"><p>결핍에서 벗어나 안전하게 사는 <b>인간 안보</b>가 실현된다.</p></div>
<div class="cp"><p>배고픔 같은 구조적 폭력이 사라진 <b>적극적 평화</b>에 가까워진다.</p></div>"""

P[5] = f"""
{hd('5면', '유엔세계식량계획(WFP)')}
<p><b>목적:</b> 배고픔 없는 세상(제로 헝거)</p>
<h4>주요 활동</h4>
<ul><li>분쟁 지역에 식량 지원</li>
<li>기후 재난 조기 경보</li>
<li>일하면 식량·현금 지원</li></ul>
<h4>기여</h4>
<p>식량으로 평화의 길을 만든 공로로 <b>2020년 노벨 평화상</b></p>
<figure>
  <img src="사진/5면_WFP_수단_식량운반.jpg" style="height:24mm">
  <figcaption>수단에서 식량을 나르는 WFP
  <span class="cr">사진: WFP/Abubaker Garelnabei / CC BY 4.0</span></figcaption>
</figure>"""

PRACTICE_PHOTO = HERE / '사진' / '6면_실천_공정무역.jpg'
if PRACTICE_PHOTO.exists():
    practice = f"""<figure style="margin:1.6mm 0">
  <img src="사진/{PRACTICE_PHOTO.name}" style="height:34mm">
  <figcaption>공정무역 마크가 붙은 아이스크림을 샀다. <span class="cr">사진: 직접 촬영</span></figcaption>
</figure>"""
else:
    practice = '<div class="ph" style="height:34mm;margin:1.6mm 0"><b>[실천 사진]</b>공정무역 제품을 산 사진</div>'

P[6] = f"""
{hd('6면', '나의 실천')}
<ol><li><b>공정무역 제품 사기</b></li>
<li>급식 남기지 않기</li>
<li>필요한 만큼만 사기</li></ol>
{practice}
<h4>느낀 점</h4>
<p>공정무역 제품을 사면 농민이 제값을 받아 가난과 배고픔을 줄일 수 있다. 작은 소비도 세계를 바꿀 수 있다.</p>"""

P[7] = f"""
{hd('부록', '참고 자료')}
<ul>
<li>『오늘부터 나는 세계 시민입니다』</li>
<li>WFP 한국사무소<br>「배고픔을 끝내기 위해」<br>ko.wfp.org/ending-hunger</li>
</ul>
<h4>사진 출처</h4>
<ul><li>2면: Oxfam East Africa</li><li>5면: WFP</li><li>6면: 직접 촬영</li></ul>
<div class="cp" style="margin-top:3mm"><div class="h">SDGs 2번</div><p>기아 종식 (제로 헝거)</p></div>"""

P[8] = base.P[8]

base.P = P

if __name__ == '__main__':
    (HERE / '2차_미니북_간단_인쇄용.html').write_text(base.build_print(), encoding='utf-8')
    (HERE / '2차_미니북_간단_보기용.html').write_text(base.build_read(), encoding='utf-8')
    print('ok')
