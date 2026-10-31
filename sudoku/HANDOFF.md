# 스도쿠 앱 프로젝트 인계서

작성일: 2026-10-03
작성자: Claude (Fable 5.1), 사용자 김달균(dalgyun@gmail.com)과의 세션에서 작성
언어 규칙: 사용자에게 보내는 모든 글은 한국어로 쓴다. 짧은 진행 상황 한 줄도 한국어.

---

## 1. 프로젝트 한 줄 요약

사용자가 "스도쿠를 즐길 수 있는 앱"을 만들려고 한다. 사용자의 명시적 지시로 **코드 작업은 아직 착수하지 않았고**, 사전 조사(알려진 스도쿠 변형 전수 조사)만 완료된 상태다.

## 2. 현재 상태 (무엇이 끝났고 무엇이 남았나)

| 항목 | 상태 |
|---|---|
| 스도쿠 변형 전수 조사 | 완료. 72종을 7개 축으로 분류 |
| 변형별 규칙 그림 도감(아티팩트) | 완료. 사용자 확인 받음 |
| 앱 플랫폼·기술 스택 결정 | **미결** |
| 1차 범위(MVP에 넣을 변형) 결정 | **미결** |
| 퍼즐 소스(생성기 vs 수록) 결정 | **미결** |
| 코드 | 한 줄도 없음 |

## 3. 산출물 위치

| 산출물 | 위치 |
|---|---|
| 변형 도감 웹페이지(공개 링크, 사용자 계정 비공개) | https://claude.ai/artifact/5P2eZFeswfC5VtNMvgun5u |
| 같은 페이지의 소스 HTML | `docs/variants-catalog.html` |
| 변형 목록 기계판독용 JSON (72종, 7축, 한국어 규칙) | `docs/variants.json` |
| 이 인계서 | `HANDOFF.md` |

`variants-catalog.html` 안에는 **미니 격자 SVG 렌더러**가 들어 있다(`render(spec)` 함수, 약 120줄). 변형 제약을 선언적 DSL로 적으면 격자 그림을 그려 준다. 앱의 보드 렌더러를 설계할 때 출발점으로 재사용할 수 있다. DSL 요약은 7절 참조.

## 4. 조사 결과 요약: 7개 축

스도쿠 변형은 "무엇을 바꾸는가" 기준으로 7개 축으로 나뉜다. 1~6번 축은 서로 **직교**한다. 즉 하나의 퍼즐에 여러 축의 제약이 동시에 걸릴 수 있다.

| 축 | 내용 | 대표 변형 | 종수 |
|---|---|---|---|
| 01 크기·기호 | N과 박스 치수, 사용 기호 | 4×4, 6×6, 16×16, Wordoku | 6 |
| 02 영역 형태 | 박스를 다른 모양으로, 영역 추가, 영역 자체를 풀이 대상으로 | Jigsaw, Hyper(Windoku), Chaos Construction | 9 |
| 03 전역 배치 | 표시 없이 격자 전체에 걸리는 금지 규칙 | X(대각선), Anti-Knight, Anti-King, Non-Consecutive, Toroidal | 7 |
| 04 셀 사이 표시 | 인접 두세 칸 사이 점·기호·음영 | Kropki, XV, 부등호, 홀짝, Quadruple, Fortress | 10 |
| 05 선(Line) | 선을 따라 숫자열의 성질 | Thermo, Arrow, Renban, German Whispers, Region Sum, Entropic, Zipper | 18 |
| 06 케이지·바깥 단서 | 점선 우리 안 산술, 격자 밖에서 보는 단서 | Killer, Sandwich, X-Sums, Skyscraper, Little Killer, Numbered Rooms | 13 |
| 07 메타·하이브리드·디지털 | 격자 겹침·3D, 다른 펜슬퍼즐 결합, 앱 전용 장치 | Samurai, Tridoku, 3D, Fog of War, Doublers, Yin-Yang 하이브리드 | 9 |

전체 목록과 각 규칙은 `docs/variants.json`에 있다. 그림은 아티팩트 또는 `docs/variants-catalog.html`을 브라우저로 열면 된다.

## 5. 조사에서 얻은 설계 관점 결론

다음은 조사 과정에서 사용자에게 보고한 핵심 관찰이다. 다음 작업자는 이것을 전제로 설계 논의를 시작하면 된다.

1. **대부분의 변형은 "제약 조합"이다.** 엔진을 `Constraint` 인터페이스(검증 + 후보 제거)로 추상화하면 40~60종을 개별 코드 없이 조합으로 커버할 수 있다. SudokuPad(Sven Neumann)와 f-puzzles가 이 구조다. 선 제약은 "셀 경로 + 술어", 바깥 단서는 "행/열/대각선 + 집계 함수"로 일반화된다.
2. **생성기(generator)가 진짜 난관이다.** 클래식 9×9 생성은 알고리즘이 확립됐지만, 변형 퍼즐은 대부분 사람이 손으로 만든다. 변형을 지원하려면 **유일해 검증 솔버**가 반드시 필요하고, 자동 생성은 Killer·Thermo·Kropki·X·Jigsaw 같은 단순 변형까지가 현실적이다. 복잡한 변형은 수록(큐레이션) 모델을 고려해야 한다.
3. **인기 순위**는 대략 Killer > X > Jigsaw > Hyper > Samurai > Thermo > Arrow > Kropki > Sandwich > Whispers. 현대 커뮤니티(Cracking the Cryptic 계열)에서는 Renban·Whispers·Region Sum·Fog of War가 급성장 중이다.
4. **경기용(WSC/GP) 타입**(6번 축)은 규칙이 정형화되어 구현 명세 잡기가 쉽다.
5. **디지털 전용 변형**(Fog of War, 3D, 토러스)은 앱이라서 가능한 차별점이다. Fog of War는 다른 변형 위에 얹는 레이어라 구현 비용이 낮다.
6. **선 색 관례**가 커뮤니티에 정착되어 있다. 저먼 위스퍼 초록, 더치 위스퍼 주황, 렌반 자홍, 리전 섬 파랑, 엔트로픽 복숭아, 모듈러 청록, 지퍼 연보라, 나브너 연두, 패리티 금색. 앱 UI 색을 정할 때 이를 따르면 기존 플레이어가 바로 알아본다. `variants-catalog.html`의 CSS 토큰(`--renban`, `--whisper` 등)에 값이 있다.

## 6. 다음 작업자가 사용자에게 먼저 확인할 것

사용자는 "우선 작업에 바로 착수하지 말고 조사부터"라고 했다. 조사는 끝났으므로 다음 단계는 범위 확정이다. 아래 질문의 답이 설계를 크게 바꾼다.

1. **플랫폼**: 웹(PWA), Windows 데스크톱, 모바일(iOS/Android) 중 무엇인가. 사용자의 다른 프로젝트는 대부분 Vite 기반 웹앱이었다(예: `C:\Users\kdgcr\sciencebox\app`, `train-watch`).
2. **1차 범위**: 클래식만 먼저 완성할지, 처음부터 변형 엔진을 깔지. 권장은 "제약 추상화는 처음부터, 노출 변형은 클래식 + 5종 내외(Killer, X, Jigsaw, Thermo, Kropki)".
3. **퍼즐 공급**: 자동 생성(클래식·단순 변형)만으로 갈지, 손으로 만든 변형 퍼즐을 수록할지, 외부 퍼즐 포맷(f-puzzles/SudokuPad JSON) 가져오기를 지원할지.
4. **플레이 기능 수준**: 펜슬마크(코너/센터), 되돌리기, 오류 표시, 힌트(다음 수 설명), 타이머, 난이도 등급 중 무엇을 1차에 넣을지.
5. **대상 사용자**: 본인용인지, 배포(스토어)용인지. 배포용이면 퍼즐 저작권(Nikoli 등 수록 불가)과 수익 모델이 따라온다.

## 7. 재사용 가능한 코드: 미니 격자 렌더러 DSL

`docs/variants-catalog.html`의 `render(spec)`는 아래 선언으로 SVG를 만든다. 앱 보드 렌더러의 데이터 모델 초안으로 쓸 수 있다.

```
spec = { n: 9, box: [3,3] | null, regions: ["AAAABBBBC", ...], draw: [ ...primitives ] }
```

| 프리미티브 | 뜻 |
|---|---|
| `{t:'d', r, c, v, k}` | 숫자. k='s' 파란(규칙으로 정해진 값), 'w' 빨강 |
| `{t:'ds', r, c, v:'53..7....'}` | 한 행 숫자열, '.'은 빈칸 |
| `{t:'shade'|'region'|'fog', cells}` | 음영 / 추가 영역 / 안개 |
| `{t:'diag'}` | 두 대각선 |
| `{t:'line', cells, color, w, bulb, arrow, circ:[i], diamond:[i], pill:[i,j]}` | 선. 온도계 전구, 화살촉, 끝 원, 마름모, 알약 |
| `{t:'cage', cells, sum}` | 점선 케이지 + 좌상단 합 |
| `{t:'dot', a, b, fill:'black'|'white'}` | 크롭키 점 |
| `{t:'edge', a, b, text, rot}` | 칸 사이 글자(X, V, >, <) |
| `{t:'bar', a, b}` | 연속 막대 |
| `{t:'odd'|'even', r, c}` | 홀짝 표시 |
| `{t:'quad', r, c, text}` | 네 칸 교점 원 |
| `{t:'batt', r, c}` | 배튼버그 체크 |
| `{t:'slash', r, c, a, b}` | 타이트 핏 빗금 칸 |
| `{t:'out', side, i, text}` | 바깥 단서 |
| `{t:'wall', segs:[[r,c,side]]}`, `{t:'box', r, c, size}` | 굵은 경계 조각 / 박스 윤곽 |
| `{t:'pm'|'mark'|'badge'|'note', ...}` | 펜슬마크 / 빨간 표시 / 셀 배지 / 설명 글 |

사무라이·트리도쿠·3D는 `CUSTOM` 함수로 따로 그린다.

## 8. 참고 자료

- eev.ee Variant sudoku reference (현대 변형 가장 체계적): https://eev.ee/fyi/variant-sudoku/
- Complete Sudoku Variations List (100+ 이름): https://sudoku-online-puzzles.com/blog/sudoku-variations-list/
- Logic Wiz 40+ variants: https://logic-wiz.com/variants/
- Wikipedia Glossary of Sudoku: https://en.wikipedia.org/wiki/Glossary_of_Sudoku
- SudokuVariants.com help: https://sudokuvariants.com/help/variants/
- GM Puzzles 규칙 모음(경기용 타입): https://www.gmpuzzles.com/blog/sudoku-rules-and-info/
- WPF Sudoku GP 2026(대회 지시서): https://gp.worldpuzzle.org/content/sudoku-gp2026
- WSC 2025 Instruction Booklet(PDF, 대용량): https://www.wspc2025.hu/wp-content/uploads/2025/09/WSC2025_INSTRUCTION_BOOKLET_v2.pdf
- SudokuPad 제약 기능 논의 저장소: https://github.com/SudokuPad/puzzle-features
- CTC Catalogue(변형별 퍼즐 수 통계): https://ctc-catalogue.com/
- Fog of War 규칙: https://sudokustreak.com/en/types/fog-of-war/

## 9. 작업 방식에 대한 메모

- 사용자는 "바로 만들지 말고 먼저 알아봐" 식으로 단계를 끊어 지시한다. 지시 범위를 넘어 코드를 쓰지 말 것.
- 글 설명만으로는 이해가 어렵다고 했고, 그림을 붙인 아티팩트를 선호했다. 설계 제안도 그림(격자 예시, 화면 목업)과 함께 내는 편이 좋다.
- 사용자 환경: Windows 11, PowerShell, Node 24, 작업 루트 `C:\Users\kdgcr`. 이 프로젝트 폴더는 `C:\Users\kdgcr\sudoku` (git 미초기화).
