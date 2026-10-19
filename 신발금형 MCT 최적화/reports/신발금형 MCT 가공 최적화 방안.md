# 신발금형 MCT 최적화, 사람보다 표준을 먼저 세우십시오

결론부터 말씀드리면, 경력 전문가 한 명을 채용해 어려운 가공을 맡기는 방식으로는 MCT 30대 규모 공장의 속도·품질 문제가 풀리기 어렵습니다. 공장 전체에 효과를 내는 개선은 PowerMill 가공 템플릿, 검증된 절삭조건이 담긴 공구 데이터베이스, 기계별 포스트프로세서, 컨트롤러 고속가공(HSM) 설정을 하나의 표준으로 묶어 모든 기계에 똑같이 적용하는 데서 나옵니다. 이 표준은 한 번 구축되면 작업자 숙련도와 상관없이 작동합니다. 다만 표준을 처음 만들고 계속 관리할 사람은 반드시 있어야 하므로, 경영진이 검토 중인 '경력 전문가 채용' 안은 직무를 '프로그래머'가 아니라 '공정 책임자(process owner)'로 다시 정의할 때 성공 가능성이 생깁니다. 외부 지원처는 실제로 있습니다. 호치민의 Autodesk 파트너 OneCAD Vietnam, 한국의 와이씨코퍼레이션·한국델켐, KITECH 호치민 사무소, Makino와 DN Solutions의 베트남 거점이 여기에 해당합니다. 그러나 '신발금형 MCT 공정 최적화'를 묶음 상품으로 파는 곳은 찾지 못했으므로, 범위를 정해 직접 주문하셔야 합니다. 상하판 조립 미세 오류는 기계와 소재의 열변형, 공구 길이 오차, 상판과 하판이 서로 다른 기준면(datum)을 쓰는 문제가 주원인으로 추정됩니다. 이 가운데 상당 부분은 워밍업 규칙, 상하판 동일 기계·동일 시간대 가공, 기계 위 공구 측정 같은 저비용 운영 규칙만으로 먼저 줄일 수 있습니다. 공개된 개선 수치는 대부분 판매사가 발표한 것이고 서로 더해지지도 않습니다. 따라서 모든 투자 결정에 앞서 자사 금형으로 1–2대 파일럿 비교 시험을 하셔야 하며, 권고 순서는 '외부 진단과 내부 베트남인 챔피언으로 3–6개월 파일럿 → 성과 확인 후 공정 엔지니어와 현지 부책임자 채용 → 30대 전체 확산'입니다.

> **읽는 법.** 괄호 안 링크가 붙은 문장은 출처로 확인한 사실입니다. **〔추론〕** 표시는 출처들을 조합한 공학적·경영적 판단이고, **〔벤더 주장〕** 표시는 소프트웨어·장비·공구 판매사가 스스로 발표한 수치로 독립 검증되지 않았습니다. 조사 과정에서 autodesk.com, help.autodesk.com, kitech.re.kr 등 여러 공식 페이지를 직접 열지 못해 검색 요약에 의존한 부분이 있으며, 해당 부분은 본문에 따로 밝혔습니다.

## 외부 지원처는 있지만 '최적화'는 범위를 정해 주문해야 합니다

첫 번째 질문에 대한 답은 "있습니다. 다만 한 곳이 모든 것을 해 주지는 않습니다"입니다. 지원처는 CAM 소프트웨어, 공구, 기계, 측정, 공공 지원의 다섯 갈래로 흩어져 있으며, 각자 자기 영역만 다룹니다.

CAM 쪽에서 가장 근거가 확실한 현지 업체는 **OneCAD Vietnam**입니다. 호치민 1군 응우옌후에 거리에 있는 Autodesk 공식 파트너이며 ([Autodesk Partner Finder](https://www.autodesk.com/support/partners/onecad-vietnam/1385)), Autodesk가 공개한 사례에서 베트남 가공업체에 **PowerMill 현장 설치와 1:1 교육**을 제공한 이력이 확인됩니다 ([Autodesk 사례: Kenstone](https://www.autodesk.com/support/partners/success-stories/overcome-the-covid-pandemic-with-autodesk-powermill/9315); [Autodesk 사례: A Chau Engineering](https://www.autodesk.com/asean/support/partners/success-stories/tackle-complex-surfaces-with-autodesk-powermill-advanced-toolpaths/7800)). VietCAD도 CAD/CAM 컨설팅과 교육을 내세우는 Autodesk 파트너입니다 ([Autodesk Partner Finder: VietCAD](https://www.autodesk.com/support/partners/vietcad-co-ltd/1334)). 다만 여러 업체가 저마다 "최상위" 또는 "유일한" 파트너라고 주장하고 있어 등급은 직접 확인하셔야 합니다. 한국어 지원이 필요하시면 **와이씨코퍼레이션**이 PowerMill 교육과 함께 **포스트프로세서 구축**을 기술 서비스로 명시하고 있고 ([와이씨코퍼레이션 PowerMill](https://www.ycgroup.co.kr/powermill)), **한국델켐(HD Solutions)**은 서울 본사 교육센터에서 PowerMill 교육을 하면서 제조 공정 컨설팅도 언급합니다 ([한국델켐 교육](https://www.delcam.co.kr/estore_education)). 매크로와 API 기반 자동화를 원격으로 맡길 곳으로는 브라질의 OptiNC(PowerMill 플러그인, CAM 자동화, 맞춤 포스트프로세서), E&C Solutions(포스트 개발, 공정 최적화·자동화), Arkance(PowerMill 매크로 자동화와 포스트 튜닝 납품 사례)가 Autodesk 파트너 목록에서 확인됩니다 ([OptiNC](https://www.autodesk.com/support/partners/optinc/937); [E&C Solutions](https://www.autodesk.com/support/partners/e--c-solutions/1893); [Arkance 사례](https://www.autodesk.com/support/partners/success-stories/innovation-und-przision-durch-die-partnerschaftliche-zusammenarbeit-zwischen-murtfeldt-und-auron/7932)).

기계 쪽에서는 **Makino**가 2019년 사이공 하이테크파크에 문을 연 4,700 m² 규모 기술센터가 가장 강력한 현지 역량입니다. 이 센터는 쇼룸, 교육, 응용 엔지니어링을 제공합니다 ([VIR](https://vir.com.vn/makino-opens-vietnam-technology-centre-to-strengthen-customer-care-69697.html)). 한국계인 **DN Solutions**(옛 두산공작기계)는 2024년 3월 호치민 떤빈군에 DN Solutions Vina를 세워 영업과 기술지원을 강화했습니다 ([PR Newswire](https://www.prnewswire.com/apac/news-releases/dn-solutions-global-machine-tool-company-enhances-product-sales-and-technical-support-across-southeast-asia-with-new-subsidiary-in-vietnam-302076768.html)). DMG MORI는 호치민 본사를 두고 있고 ([DMG MORI](https://www.dmgmori.co.jp/corporate/en/company/base.html)), Heidenhain 컨트롤러는 호치민 10군의 AMS Co., Ltd가 공식 대리점이자 서비스센터입니다 ([Heidenhain 연락처](https://www.heidenhain.com/about-us/contact/heidenhain-around-the-world); [AMS](https://amsvn.com/en/authorized-distributor-of-heidenhain-in-vietnam.php)). 〔추론〕 현재 보유한 MCT의 제조사가 컨트롤러 고속가공 파라미터(룩어헤드, 스무딩, 공차 모드)를 조정할 첫 번째 창구이며, 보유 기계에 두산·DN 장비가 섞여 있다면 DN Solutions Vina가 한국어로 소통할 수 있는 자연스러운 상대입니다.

공구 쪽은 현지 기술센터가 약합니다. Mitsubishi Materials 동남아 법인은 시험 절삭, 교육, 기술 컨설팅, 생산라인 진단을 하는 가공기술센터를 운영한다고 밝히지만, 베트남 주소는 공개하지 않습니다 ([MMC SEA](https://www.mmc-carbide.com/sea/solution/applications/tech)). Sandvik Coromant의 생산성 센터가 베트남에 있는지는 확인되지 않았습니다. YG-1은 직원 10–24명 규모의 100% 투자 베트남 법인을 두고 있습니다 ([VietnamWorks](https://vietnamworks.com/nha-tuyen-dung/yg-1-co-ltd-c157018)). 〔추론〕 업계 관행상 공구사와 대리점은 공구 구매로 이어질 가능성이 있으면 무상 시험 가공을 해 주며, MCT 30대 규모라면 그 대상이 되기에 충분합니다. 한국어 지원 가능성은 YG-1·Korloy 같은 한국 브랜드가 가장 높습니다.

측정·교정은 공백이 큽니다. Renishaw의 ISO 17025 교정 서비스는 "현재 미국 고객 전용"이며 ([Renishaw 교정 서비스](https://www.renishaw.com/en/calibration-service-repair-and-recalibration--6877)), 베트남 현지 볼바(ballbar)·레이저 교정 서비스 업체는 확인되지 않았습니다. 〔추론〕 30대 규모라면 QC20 볼바 한 세트를 사서 보전 인력을 교육하는 편이 외부 서비스에 의존하는 것보다 현실적입니다(가격은 미확인).

공공 지원 가운데 가장 직접적인 창구는 **KITECH(한국생산기술연구원) 호치민 사무소**입니다. 이 사무소는 현지 진출 한국 기업에 대한 맞춤형 기술지원을 주요 임무로 밝히고 있습니다 ([KITECH 해외사무소](https://www.kitech.re.kr/corporate/global/abroad)). KITECH는 금형을 포함한 뿌리기술이 핵심 분야이고, 부천에 한국금형기술센터를 두고 있습니다 ([KITECH 임무](https://www.kitech.re.kr/introduce/purpose); [한국금형기술센터 브로셔](https://mold.kitech.re.kr/bbs/pdf/mold%20technology%20center%20brochure.pdf)). 별도의 '해외 진출 기업 지원' 메뉴도 있지만 페이지가 열리지 않아 내용은 확인하지 못했습니다 ([KITECH](https://www.kitech.re.kr/corporate/global/friendshoring)). KOICA 자문단은 퇴직 전문가를 파견하지만 목적이 개도국 개발협력이어서 민간 공장 지원에는 맞지 않습니다 ([KOICA 자문단](https://koica.go.kr/koica_kr/948/subview.do)).

| 필요 영역 | 1순위 접촉처 | 기대할 수 있는 것 | 확인된 한계 |
|---|---|---|---|
| PowerMill 교육·라이선스 | OneCAD Vietnam (호치민) | 현장 설치, 베트남어 1:1 교육 | 한국어 가능 여부·가격 미확인 |
| 템플릿·포스트프로세서 | 와이씨코퍼레이션, 한국델켐 (원격 또는 단기 방문) | 포스트 구축, 한국어 교육 | 신발금형 경험 미확인 |
| 매크로·API 자동화 | OptiNC, E&C Solutions, Arkance (원격) | 매크로·플러그인 기반 표준화 | 한국어 불가로 추정, 가격 미확인 |
| 컨트롤러 HSM 설정 | 보유 기계 제조사 (DN Solutions Vina, AMS/Heidenhain 등) | 룩어헤드·스무딩·공차 튜닝 | 유료 공정 컨설팅 여부 미확인 |
| 고속 정삭 벤치마크 | Makino 기술센터 (사이공 하이테크파크) | 시험 가공, 응용 엔지니어링 | 대개 장비 판매 관계와 연계 |
| 공구·절삭조건 | 공구사 대리점, YG-1 등 | 무상 시험 가공 (관행) | 베트남 내 기술센터 미확인 |
| 공공 기술지원 | KITECH 호치민 사무소 | 전문가 연결, 금형기술센터 연계 | 구체 프로그램 내용 미확인 |

〔추론〕 이 가운데 어느 곳도 "템플릿 표준화와 공정 최적화"를 패키지로 광고하지 않습니다. 따라서 의뢰서에 범위를 명시하셔야 합니다. 예를 들면 현행 PowerMill 프로젝트와 NC 출력물 감사, 소재별 템플릿 라이브러리, 공용 공구 DB, 컨트롤러별 포스트 검증, 대표 금형 사이클타임 벤치마크를 하나의 고정 범위 프로젝트로 묶는 방식입니다.

## 작업자와 무관한 개선은 '한 번 설정된 표준'에서 나옵니다

두 번째 질문의 핵심은 이렇습니다. 최신 소프트웨어는 "작업자 숙련과 무관한" 결과를 낼 수 있지만, "설정하는 사람 없이" 내지는 못합니다. 아래의 개선 수단은 모두 누군가 한 번 기준을 세워 두면, 그 뒤로는 어느 작업자가 어느 기계를 맡아도 같은 결과를 내는 성격을 지닙니다.

### PowerMill은 신버전보다 이미 가진 기능의 표준화가 핵심입니다

PowerMill 2026은 2025년 5월 무렵 출시되었습니다. Autodesk 커뮤니티 사용자들은 이 버전을 "서비스팩 수준"의 소폭 업데이트로 평가하며, Autodesk 인수 이후 새 가공 전략이 나오지 않았다고 지적합니다 ([Autodesk 포럼](https://forums.autodesk.com/t5/powermill-forum/powermill-2026/m-p/13885895)). 반면 Autodesk가 공식적으로 강조하는 기능은 이미 공장에 있는 것들입니다. **템플릿과 사용자 매크로로 모범 사례를 팀 전체에 공유하는 기능**, 재계산 없는 공구경로 편집, 자동 충돌 회피를 갖춘 3·5축 전략, 기계 시뮬레이션이 그것입니다 ([Autodesk PowerMill 기능](https://www.autodesk.com/products/powermill/features)). PowerMill은 매크로(.mac), Python API, .NET/COM 인터페이스를 제공합니다. 다만 이 정보는 Autodesk 공식 문서가 아닌 제3자 API 목록에서 확인한 것입니다 ([API Evangelist](https://providers.apievangelist.com/providers/autodesk-powermill/)).

고속 황삭 전략 Vortex는 Delcam 시절 시험에서 "통상 최소 40%" 절감을 보였고, 공구강에서 121분이 34분(−71%)으로 줄었습니다 **〔벤더 주장, 2014년〕** ([GfxSpeak](https://gfxspeak.com/archives/delcam-adds-vortex-high-speed-roughing-to-powermill/)). Delcam 스스로도 결과는 소재, 형상, 기계, 공구에 따라 달라진다고 밝혔습니다. 신발금형과 가장 가까운 선례는 오래된 것입니다. **Nike 금형센터는 PowerMILL 위에 'Cruncher'라는 자동화 계층을 만들어 공구경로 작업의 약 80%를 자동화**했고, 단순 작업은 2시간 만에 절삭을 시작했습니다 (2001년, [Leatherbiz](https://leatherbiz.com/News/69694)). ECCO 인도네시아는 아웃솔 금형용 PowerMill 5축 가공에 맞춤 매크로·API 프로그램을 도입했습니다. 다만 정량 지표는 공개되지 않았습니다 ([Autodesk 사례](https://www.autodesk.com/support/partners/success-stories/making-complex-mold-with-5axis-machining-achieving-great-accuracy--productivity/7398)). 반복 형상을 활용한 자동화의 다른 예로 타이어 금형이 있습니다. hyperMILL을 쓴 Northeast Tire Molds에서는 프로그래머 한 명이 이전 시스템으로 1년 걸리던 일을 3개월에 끝냈습니다 ([MMS](https://mmsonline.com/articles/cam-system-simplifies-tire-mold-programming)).

〔추론〕 사이즈별로 1개씩 만드는 신발금형은 위상이 같고 치수만 다른 '부품 패밀리'입니다. 따라서 귀사의 작업 방식은 표준화에 불리한 것이 아니라 오히려 템플릿 자동화에 가장 잘 맞는 구조입니다. 구체적으로는 각 사이즈 모델을 불러와 경계·블록을 자동 생성하고, 템플릿을 적용해 야간에 일괄 계산한 뒤, 충돌 검사와 포스트 출력까지 하는 Python/매크로 "사이즈 루프"가 Nike Cruncher에 가장 가까운 현대판입니다. 이렇게 되면 작업자의 일은 "모델 불러오기 → 템플릿 적용 → 시뮬레이션 확인 → 출력"으로 줄어듭니다. 이를 위해서는 설계와 CAM 사이에 곡면 명명 규칙(아웃솔 캐비티, 트레드, 파팅면, 로고·텍스처 영역 등)을 합의해야 합니다. 또 절삭조건은 작업자가 아니라 공구·소재 DB에 묶어 두어야 합니다.

### NC 최적화·검증과 컨트롤러 설정은 작업자의 판단을 아예 거치지 않습니다

이미 출력된 NC 코드를 물리 모델로 다시 계산해 이송속도를 조정하는 **VERICUT Force**는 금형에 특화된 근거가 가장 좋은 수단입니다. 한국 금형업체 **미주정밀**은 HP4M 강재 자동차 도어트림 금형의 중삭·정삭 프로그램 68개에 Force를 적용해 **절삭 시간을 9일에서 6일로(약 35%) 줄였습니다** **〔벤더 사례, 2023년〕** ([ETMM](https://www.etmm-online.com/software-reduces-cutting-time-from-nine-to-six-days-a-b47f891e672c757df32de397b0430462/)). 다수 캐비티 금형업체 iMFLUX는 단순 형상에서 17%, 복잡 형상에서 45%를 절감했고 공구 수명도 개선했다고 밝혔습니다 **〔벤더 사례〕** ([CGTech iMFLUX](https://vericut.com/hubfs/PDF/Imflux-User%20Story.pdf)). 판매사 CGTech는 20–70% 단축을 주장합니다 **〔벤더 주장〕** ([MMS](https://www.mmsonline.com/articles/cnc-optimization-software-reduces-cycle-times-25-or-more-and-can-double-tool-life)). 〔추론〕 미주정밀 사례에서 황삭은 제외되었습니다. 이는 이미 부하가 일정한 Vortex 황삭보다, 신발 밑창 캐비티의 코너 잔삭이나 급경사 벽처럼 부하가 들쭉날쭉한 중·정삭에서 효과가 크다는 뜻으로 읽힙니다. 알루미늄 금형에서는 공구 부하보다 기계 가감속이 속도를 제한하므로, 강재 금형보다 이득이 작을 것으로 예상됩니다.

컨트롤러 고속가공 기능은 비용이 가장 적게 드는 수단입니다. Fanuc의 AICC II와 Smooth Tolerance Control+, Smooth TCP ([Fanuc 5축 브로슈어](https://fanucamerica.com/docs/default-source/cnc-files/brochures/mba-025-en_03_1308_5axis_low.pdf)), Heidenhain의 ADP(점 분포가 불규칙한 CAM 프로그램도 매끄럽게 처리) ([Heidenhain US](https://www.heidenhain.us/resources-and-news/trend-setting-solutions-for-machining-tasks-in-tool-and-mold-making/)), Siemens의 Top Surface와 Top Speed Plus(최대 30% 단축 **〔벤더 주장〕**) ([Automation.com](https://www.automation.com/article/siemens-sinumerik-one-dynamics-technology-motion))가 여기에 해당합니다. 이 기능들이 고밀도 자유곡면 코드에서 실제로 나오는 이송속도와 면 품질을 좌우합니다. 〔추론〕 30대가 섞여 있다면 Fanuc G05.1 Q1, Heidenhain CYCL DEF 32, Siemens CYCLE832 같은 호출을 공정 종류(황삭·중삭·정삭)별로 포스트프로세서에 고정해 넣으면 됩니다. 그러면 작업자가 이 값을 고를 일이 아예 없어집니다. 출발값으로는 황삭 0.05–0.1 mm 속도 모드, 정삭 0.005–0.01 mm 정밀 모드를 두고 기계별로 조정합니다.

주축 부하에 따라 이송을 실시간 조정하는 적응제어도 있습니다. Siemens 사례로 GROB −18.1%, Turbo Energy −6~12%가 보고되었고 **〔벤더 사례〕** ([Siemens](https://references.siemens.com/en/reference/31260?id=31260)), OMATIVE는 "20% 이상"을 주장합니다 **〔벤더 주장〕** ([MMS](https://mmsonline.com/products/adaptive-software-machining-reduces-cycle-times)). 〔추론〕 다만 효과는 주로 강재 황삭과 공구 보호에 있고, 알루미늄 정삭에서는 작습니다.

### 가장 큰 숨은 용량은 '기계가 놀고 있는 시간'일 수 있습니다

모니터링 업체들은 잡숍(job shop)의 주축 가동률이 30–45%에 그친다고 말합니다 **〔벤더 주장〕** ([Fabrico](https://www.fabrico.io/ro/blog/oee-software-cnc-machining/)). 실시간 모니터링 도입 6개월 뒤 5축 셀의 OEE가 58%에서 73%로 올랐다는 2026년 항공 부품 사례도 있습니다 **〔벤더 사례〕** ([TeepTrak](https://teeptrak.com/en/us-aerospace-oee-case-study-2026/)). 다품종 소량 금형공장에서는 팔레트와 셀 컨트롤러로 5축 2대를 무인 운전해 **주축 가동률 최대 90%**를 낸 사례가 있습니다 ([MMS: PrecisionX](https://www.mmsonline.com/articles/cell-controller-boosts-production-flexibility)). 중국 신발금형업체 잔성(站胜)모구는 CNC 12대에 로봇 1대, 기상 프로빙 센터링을 갖춘 라인으로 조당 6명 감축과 효율 20% 향상을 기대한다고 밝혔습니다 **〔벤더 사례, 검색 요약 기반〕** ([EMAN](https://www.oureman.com/view_618.html)). 공구 측면에서는 열박음(shrink-fit) 홀더가 콜릿보다 강성이 높아 절삭속도를 약 10% 올린 금형공장 사례가 있습니다 ([MoldMaking Technology](https://www.moldmakingtechnology.com/articles/shrink-fit-system-helps-moldmaker-boost-cnc-accuracy-productivity-and-tool-life)). Haimer는 오프라인 프리세터로 공구 측정 시간이 약 70% 줄어든다고 주장합니다 **〔벤더 주장〕** ([Haimer](https://www.haimer.com/shop/catalog/downloads/files/2019-09_InnovationHighlights-DE-EN-screen/2019-09_InnovationHighlights-DE-EN-screen.pdf)).

정삭 공구 형상도 바꿀 수 있습니다. 볼엔드밀의 스텝오버는 보통 공구 지름의 3–5%에 불과하지만, 원호세그먼트(배럴) 공구는 훨씬 넓은 스텝오버를 쓸 수 있습니다 ([MoldMaking Technology](https://moldmakingtechnology.com/articles/improving-finishing-operations-with-circle-segment-cutters)). Emuge와 Seco는 5축 정삭이 80% 이상 빨라진다고 주장하며 **〔벤더 주장〕** ([Seco](https://www.secotools.com/article/117073)), 원추형 공구로 스텝오버를 10배 넘게 넓혀 약 90%를 단축한 단일 사례도 있습니다 ([MoldMaking Technology](https://www.moldmakingtechnology.com/articles/how-to-optimize-mold-finishing)). 〔추론〕 이런 공구는 넓은 측벽이나 파팅 플랜지에 맞고, 트레드 세부는 여전히 소형 볼엔드밀이 담당해야 합니다. 미세 텍스처는 GF의 레이저 텍스처링처럼 디지털 방식으로 반복 재현하는 대안이 있으므로 ([GF Machining Solutions](https://www.gfms.com/content/dam/gfms/pdf/laser/laser-p-u/en/GF%20MS_Flyer_shoe%20mold_2020_4pages_3.pdf)), 직접 투자할지 외주를 줄지 따져 볼 대상입니다.

### AI CAM은 아직 신발금형의 자유곡면을 대신하지 못합니다

CloudNC CAM Assist 2.0은 Fusion, Mastercam, NX를 지원하고 ([CTE Magazine](https://ctemag.com/?p=101213)), Siemens NX CAM Copilot의 초기 범위는 2.5축·3축 형상입니다 ([Engineering.com](https://www.engineering.com/?p=142526)). 조사한 범위에서 PowerMill을 지원하거나 자유곡면 5축 금형을 겨냥한 AI CAM은 확인되지 않았습니다. 〔추론〕 신발금형에서 중요한 결정은 경사도별 전략 선택, 공구 길이와 기울기 관리, 잔삭 처리이며, 현재 AI 도구는 이를 다루지 못합니다. 지금 귀사에 맞는 'AI에 가까운' 방식은 지식 기반 템플릿에, 금형 유형·소재별로 성공한 파라미터를 축적한 이력 DB를 더하는 것입니다.

| 수단 | 보고된 효과 | 근거 성격 | 작업자 의존도 | 귀사 적합도 〔추론〕 |
|---|---|---|---|---|
| 템플릿·공구DB·포스트 표준화 | Nike 공구경로 약 80% 자동화 (2001) | 업계지, 오래됨 | 구축 후 없음 | 최우선 |
| 컨트롤러 HSM 설정의 포스트 고정 | Top Speed Plus 최대 −30% | 벤더 | 없음 | 최우선, 저비용 |
| 가동률 모니터링·중앙 DNC | OEE 58→73% | 벤더 (타 업종) | 없음 | 높음 |
| 사이즈 루프 자동화 (Python/매크로) | 타이어 금형 12개월→3개월 | 업계지 | 구축 후 없음 | 높음 |
| VERICUT 시뮬레이션 + Force | −17~45%, 미주정밀 −35% | 벤더 사례 | 없음 | 강재 금형 중·정삭에 높음 |
| Vortex 고속 황삭 | −40~73% | 벤더, 2013–14 | 템플릿화하면 없음 | 이미 보유, 템플릿화 필요 |
| 배럴 공구 5축 정삭 | −80~90% | 벤더·단일 사례 | 템플릿화하면 없음 | 5축 기계·측벽에 한정 |
| 적응제어 | −6~20%+ | 벤더 | 없음 | 강재 황삭 위주 |
| AI CAM | 프로그래밍 시간 최대 −80% | 벤더 | 낮음 | 현재 부적합 (PowerMill 미지원) |

이 수치들은 서로 더해지지 않습니다. 황삭에서 이미 줄인 시간을 Force가 다시 줄일 수는 없기 때문입니다. 실제 효과는 귀사 금형으로 직접 측정해야만 알 수 있습니다.

## 상하판 조립 미세 오류는 열·공구·기준면 세 갈래에서 생깁니다

먼저 분명히 해 둘 점이 있습니다. 신발금형 파팅라인의 상하판 정합 허용공차를 숫자로 공개한 브랜드나 산업 표준은 찾지 못했습니다. 베트남·중국 금형업체들은 "3D 도면과 정확히 일치"라고만 광고합니다 ([Global Precision](https://globalprecision.vn/en/cnc-shoe-mold-processing-with-high-precision-to-create-a-prestigious-brand/)). 반면 정합 불량의 결과는 특허 문헌에 잘 기록되어 있습니다. 파팅라인의 밀봉이 불완전하면 소재가 새어 나와 플래시(flash)가 생기고, 플래시가 없어도 눈에 보이는 단차 능선이 남으며, 깨끗한 이음매를 얻으려면 손 다듬질이 많이 필요합니다 ([US 7861765B2](https://patents.google.com/patent/US7861765)). 따라서 목표 공차는 고객 브랜드 사양이나 귀사 자체 기준에서 정하셔야 합니다.

〔추론〕 진단의 첫걸음은 증상을 두 가지로 나누는 것입니다. 측면(X/Y) 어긋남은 옆벽 단차로 나타나며 기준면이나 가이드핀 문제를 가리킵니다. 높이(Z) 틈은 플래시나 두꺼운 파팅 스킨으로 나타나며 랜드 높이, Z 오프셋, 공구 길이 문제를 가리킵니다. 둘은 원인도 대책도 다릅니다.

### 무냉방 공장에서는 열이 가장 크고 가장 변덕스러운 오차원입니다

주축 모터와 베어링의 열로 주축이 **40–50 µm** 늘어날 수 있고 ([US 4471443](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4471443)), 시동 후 열평형까지 **20–45분**이 걸립니다 ([mfgrobots](https://www.mfgrobots.com/Article/repair/52139.html)). 한 연구에서는 수냉 주축이 약 20분 만에 안정되었지만, 비냉각 주축은 45분이 지나도 안정되지 않았습니다 ([Pajor et al.](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-49ae5a5e-84b9-4fab-b1be-219d1e2e8271/c/Pajor.pdf)). 수직 MCT는 워밍업 중에 YZ 평면 직각도가 12 µm/m, ZX 평면이 14 µm/m 변했습니다 ([Huddersfield 대학](https://pure.hud.ac.uk/en/publications/effect-of-thermal-changes-on-the-squareness-error-between-linear-/)). 공장 문을 여닫는 것만으로도 오차가 측정 가능하게 달라졌다는 연구도 있습니다 ([Optical Engineering 2007](https://proceedings.spiedigitallibrary.org/journals/optical-engineering/volume-46/issue-10/103401/Thermally-induced-errors-in-diamond-turning-of-optical-structured-surfaces/10.1117/1.2795571.full)). 소재 쪽에서는 알루미늄의 열팽창계수가 약 23 µm/m·K로 강철의 약 2.5배입니다 ([Keyence](https://www.keyence.co.in/ss/products/measure-sys/measurement-selection/environment/thermal-expansion.jsp)).

〔추론〕 이 수치를 귀사 상황에 대입해 보겠습니다. 길이 330 mm 알루미늄 금형 반쪽은 온도가 1°C 다를 때마다 약 7.6 µm 차이가 납니다. 하판을 시원한 오전에, 상판을 더운 오후에 깎아 소재 온도가 3°C만 달라도 약 23 µm의 길이 차이가 생기며, 이는 토(toe)와 힐(heel) 쪽에서 눈에 띄는 단차 수준입니다. 여기에 두 판을 서로 다른 기계에서 깎으면 기계마다 다른 열·기하 특성이 더해집니다. 기계가 30대라면 이 '기계 간 편차'가 정합 불량의 핵심 원인일 수 있습니다.

### 공구 길이와 기준면은 운영 규칙으로 고칠 수 있습니다

공구 길이 오차는 Z(틈·플래시)로, 반경 오차는 X/Y 벽면(단차)으로 그대로 옮겨 갑니다. Renishaw NC4 같은 기상 비접촉 공구 측정기는 반복정밀도 ±0.1 µm(2σ)이며 ([Renishaw NC4](https://www.renishaw.com/en/nc4-non-contact-tool-setter--6099)), 독일의 한 가공업체는 이를 가공 중 공구 길이 측정에 써서 열 성장을 보정합니다 ([Renishaw ZBG 사례](https://renishaw.com/resourcecentre/en/details/anwenderbericht-hoehere-prozesssicherheit-in-der-serie--19652)). 〔추론〕 프리세터는 공구를 차갑고 정지된 상태에서 재므로, 파팅라인 정삭 공구의 최종 길이는 워밍업 후 실제 회전수에서 기상 측정하는 것이 맞습니다. 상판과 하판 정삭 사이에도 다시 측정해 두 판의 공구 마모 상태를 맞춰야 합니다.

기준면 측면에서는 영점 클램핑(zero-point) 시스템이 표준형 5 µm, 고급형 2.5 µm 이내의 반복정밀도를 냅니다. 다만 설치 후 성능은 청결과 핀 상태에 좌우된다는 경고가 붙어 있습니다 ([Fabrico](https://www.fabrico.io/blog/zero-point-clamping-systems/)). 스트레인게이지 주축 프로브 OMP400의 반복정밀도는 0.25 µm(2σ)입니다 ([Renishaw](https://store.renishaw.com/en-LU/product/A-5069-2002)). 〔추론〕 가장 효과가 큰 구조적 대책은 상판과 하판이 같은 기준 체계를 쓰게 만드는 것입니다. 가이드핀·부시 구멍을 파팅면과 같은 셋업에서 가공하거나, 두 판을 영점 팔레트에 올려 같은 기준 형상을 프로빙하는 방식입니다. 판마다 바이스 조를 따로 인디케이팅하거나 엣지파인더로 원점을 따로 잡으면, 그때마다 독립적인 오차가 쌓입니다.

CAM·컨트롤러 측면의 원인은 신발금형에 특화된 정량 출처를 찾지 못해 실무 원칙으로만 제시합니다. 〔추론〕 파팅·셧오프 면 정삭 경로의 CAM 공차는 목표 공차의 5분의 1 이하로 잡고(목표가 0.02 mm라면 0.002–0.005 mm), 두 판 모두 여유량 0과 실측 반경을 쓰며, 중삭 템플릿의 잔여 여유가 한쪽 셧오프에만 남지 않게 해야 합니다. 컨트롤러 고속 스무딩은 정확도를 속도와 맞바꾸므로, 파팅라인 정삭 패스에서는 반드시 정밀 모드를 포스트에 고정해야 합니다. 사이즈 그레이딩 시에는 축척, 수축률 적용, 좌우 미러링, 코어·캐비티 분리를 하나의 스크립트 순서로 처리해야 수축률 이중 적용이나 원점 불일치를 막을 수 있습니다.

측정에는 PowerInspect OMV가 있습니다. 같은 클램핑 상태에서 프로브로 랜드, 핀 구멍, 주요 캐비티 점을 확인할 수 있고, PowerMill과 연동됩니다 ([Autodesk PowerInspect](https://www.autodesk.com/eu/products/powerinspect/features)). 한 금형공장은 OMV로 0.01 mm 이하 정확도를 얻었다고 보고했습니다 **〔벤더 사례〕** ([Autodesk FMPS 사례](https://www.autodesk.com/support/partners/success-stories/fmps--success-in-implementing-omv-inspection-on-cnc-machines/9850)). 〔추론〕 다만 OMV는 기계 자신의 축으로 측정하므로, 가공과 측정에 공통으로 끼는 기계 열·기하 오차는 잡아내지 못합니다. 따라서 볼바 교정과 주기적 CMM 감사를 함께 해야 합니다.

| 증상 | 유력 원인 〔추론〕 | 확인 방법 |
|---|---|---|
| 전 둘레 균일한 측면 단차 | 기준면·원점 오류, 핀 구멍 위치, 영점 팔레트 오염 | 두 판의 핀 구멍 중심을 공통 기준으로 프로빙 |
| 토·힐 쪽으로 커지는 단차 (축척형) | 두 판의 온도 차, 그레이딩·수축률 원점 오류, 축 스케일 오차 | 가공 시각·온도 비교, CAD 축척 원점 확인, 레이저 축 점검 |
| 회전된 단차 | 기준 회전, 기계 직각도 | 2점 구멍 프로빙, 볼바 직각도 |
| 균일한 Z 틈·플래시 | 공구 길이·주축 열 성장, 랜드 높이 오프셋, CAM 잔여 여유 | 기상 레이저 재측정, OMV 랜드 높이 측정 |
| 국부적으로 물결치는 Z 틈 | 판 변형·잔류응력, 클램핑 변형, 컨트롤러 스무딩, 공구 휨 | 언클램프 후 평면도, 정밀 모드 재가공 |
| 5축·사이드 몰드에서만 발생 | 회전 중심(pivot) 오차, 회전축 위치 오차 | AxiSet Check-Up, KinematicsOpt, XR20-W |
| 특정 기계 조합에서만 발생 | 기계 간 기하·열 특성 차이 | 볼바·레이저로 30대 순위화 후 상하판 동일 기계 배정 |

〔추론〕 출처에 나온 개별 수치를 조합해 보면, 위 대책이 갖춰질 경우 상하판 간 파팅 랜드·핀 정합 오차는 약 10–20 µm 수준까지 가능해 보입니다. 대책이 없으면 30–80 µm도 그럴듯한 범위입니다. 이는 측정 결과가 아니라 오차 예산 추정입니다. 비용 순서로 권하는 대책은 다음과 같습니다. 먼저 긴 정지 후 20–45분 표준 워밍업 프로그램을 운영하고, 상하판을 같은 기계(또는 검증된 기계 쌍)에서 같은 시간대에 정삭합니다. 다음으로 정삭 직전 기상 공구 측정과 기준 재프로빙을 하고, 문·선풍기 바람이 기계에 직접 닿지 않게 합니다. 그 뒤에 30대 볼바 순위화로 상위 기계를 파팅 정삭 전용으로 지정하고, 마지막으로 영점 팔레트와 OMV에 투자합니다. 무엇보다 지금 당장 금형마다 기계 번호, 가공 시각, 주변·주축 온도, 측정한 랜드 높이와 핀 위치를 기록하기 시작하시기 바랍니다. 이 기록을 몇 주만 모아도 원인이 열인지, 특정 기계인지, 셋업인지 드러납니다.

## 전문가의 몫은 프로그램을 짜는 것이 아니라 표준을 소유하는 것입니다

세 번째 질문인 "최신 기술 환경에서 전문가가 맡아야 할 몫"에 대해, MoldMaking Technology는 매크로, 가공 템플릿, 공구 DB 같은 공장 단위 표준을 결합하면 신입이 "대개 몇 주 만에" 실질적 가치를 낸다고 썼습니다. 또 그 방법으로 공장 엔지니어들의 프로그래밍 방식을 분석해 모범 사례를 매크로 묶음으로 정리하는 과정을 설명합니다 ([MoldMaking Technology](https://www.moldmakingtechnology.com/articles/cam-tools-automate-programming-aid-five-axis-machining-and-more)). 같은 매체는 모범 사례 DB가 "프로그래밍 DB보다 칩을 깎는 데 집중하는" 현장에 맞아야 한다고 경고합니다 ([MoldMaking Technology](https://www.moldmakingtechnology.com/articles/redefining-cam-technology-for-moldmakers)). 한 특허는 같은 부품을 두 사람이 프로그래밍하면 "아마도 다를 것"이며, 이런 개인화가 공정 표준화를 가로막는다고 문제를 정의합니다 ([US 7058472](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7058472)). 다시 말해 작업자는 표준을 만들지 않으므로, 누군가 만들고 지켜야 합니다.

한국과 베트남의 구인 공고는 여전히 직무를 "PowerMill·hyperMILL·NX 운용, NC 코드 작성"으로 좁게 씁니다. 국내 경력 CAM 직무는 연 3,000만–5,200만 원 수준입니다 ([invione](https://www.invione.com/jobs/recruitment/all/detail/K141122606250003); [theteams](https://www.theteams.kr/recruit/wanted/3616828)). 동나이성의 Carbori Molds Vietnam은 PowerMill 능숙자를 CAM 프로그래밍 엔지니어로 뽑고 있습니다 ([TopCV](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437)). 〔추론〕 귀사가 같은 방식으로 공고를 내면 '프로그래머 한 명 더'가 들어옵니다. 30대 공장에 필요한 역할을 우선순위대로 적으면 다음과 같습니다. 첫째, 신발금형 형상별 PowerMill 템플릿과 매크로를 만듭니다. 둘째, 소재·홀더·돌출 길이별로 검증된 절삭조건을 담은 단일 공구 DB를 만듭니다. 셋째, 포스트프로세서의 소유와 버전 관리, NC 검증을 맡습니다. 넷째, 컨트롤러별 HSM 파라미터를 조정합니다. 다섯째, 측정 결과를 여유량과 정삭 전략에 되먹이는 품질 순환 구조를 만듭니다. 여섯째, 가동률 데이터를 수집하고 주간 검토를 합니다. 일곱째, 작업자 교육과 자격 체계를 운영합니다. 여덟째, 공구사·리셀러 관리를 맡습니다. 직무기술서에는 소프트웨어 이름과 경력 연수 대신, 파일럿 금형 사이클타임 단축률, 공구 DB 커버리지, 표준 템플릿 수 같은 측정 가능한 산출물을 적어야 합니다.

### 나이 든 경력자가 최신 기술과 닿아 있는지는 연차로 알 수 없습니다

네 번째 질문에 대해, 한국에서 경력자를 데려온다면 그 인력 풀은 고령층입니다. 2023년 뿌리산업 실태조사에서 50대 이상이 약 **36.5%**였고, 부족 인원은 2018년 2,568명에서 2023년 18,232명으로 **약 7배** 늘었습니다 ([서울경제](https://www.sedaily.com/article/14032269)). 금형 업계지는 30–40대 기술자의 절대 부족 때문에 선후배 간 기술 전수가 막혀 있다고 보도해 왔습니다 ([kidd.co.kr](https://kidd.co.kr/news/163836)). 한편 금형은 역사적으로 전문가 노하우에 크게 의존했고, CAD/CAM/CAE 통합이 그 의존도를 줄인다는 연구가 있습니다 (2011년, [KoreaScience](https://koreascience.kr/article/JAKO201110334668264.pdf)).

정직하게 말씀드리면, 장기 근속 CAM 사용자가 Vortex·적응형 황삭, 5축, 프로빙을 실제로 얼마나 채택하는지에 대한 조사나 연구는 찾지 못했습니다. 〔추론〕 그래서 결론은 "나이가 문제다"가 아니라 "연차는 최신성의 증거가 아니다"입니다. 한국에서 오는 50대 이상 경력자는 금형 노하우, 보수적 절삭, 문제 해결에는 강하겠지만, 전체 날 길이를 쓰는 초경 Vortex 황삭, 스톡 모델 기반 잔삭, 깊은 리브의 3+2·5축, 기상 프로빙, NC 검증, 데이터 기반 가동률 관리에는 반드시 밝다고 할 수 없습니다. 이 최신성은 실기 시험으로 확인해야 합니다. 같은 논리로 공장 안의 베테랑 작업자들이 지켜 온 '안정성 우선 관행'도 무시할 대상이 아닙니다. 그 관행 안에는 공구 파손이나 깊은 캐비티 떨림 같은 실제 실패 이력이 담겨 있습니다. 각 관행이 왜 생겼는지 작업자에게 묻고 기록한 뒤, 새 조건과 비교 시험해 살릴 것과 버릴 것을 가려내는 것이 맞습니다. 베트남 쪽 고참 인력은 구인 공고에 22–35세 같은 연령 상한이 흔해 공고만으로는 잘 잡히지 않으므로 ([RGF](https://www.rgf-hragent.asia/vn/vietnam/mold-engineer-manufacturing-SDG-105757)), 헤드헌팅이 필요할 것으로 판단됩니다 〔추론〕.

## '경력 전문가 채용' 안은 방향은 맞지만 순서와 직무 정의를 바꿔야 합니다

〔추론〕 경영진의 채용 안에 대한 평가는 "조건부 찬성"입니다. 표준을 소유할 사람이 필요하다는 판단은 옳습니다. 그러나 경력자 한 명을 단독으로 들여와 바로 성과를 기대하는 방식은 세 가지 경로로 실패하기 쉽습니다. 첫째, 전문가가 가장 어려운 금형을 직접 프로그래밍하느라 표준을 만들지 못합니다. 둘째, 작업자들이 '전문가 프로그램'을 이송 오버라이드 50–70%로 낮춰 돌려서 개선 효과가 드러나지 않습니다. 셋째, 경영진이 공구 DB가 완성되기도 전인 3개월 시점에 성과를 판정합니다. 이 위험은 베트남 조직 문화 때문에 더 커집니다. 베트남 부하 직원은 상사에게 이의를 제기하기를 꺼리는 경향이 있다는 연구가 있고 ([Humanities and Social Sciences Communications 2025](https://www.nature.com/articles/s41599-025-06434-y)), 빈즈엉 한국계 기업 노동자 356명 설문 연구는 갈등의 주원인으로 근무 문화 차이를 꼽았으며 폭언을 들을 때 침묵하는 경우가 많았다고 보고했습니다 ([Journal of Industrial Relations 2020](https://journals.sagepub.com/doi/10.1177/0021909620935423)). 그래서 실패는 공개적인 반발보다 '조용한 미준수'의 형태로 나타날 가능성이 높습니다.

비용도 따져 봐야 합니다. 경력 외국인 엔지니어의 베트남 기본급은 월 약 3,200–6,000달러로 제시되고, 여기에 주거, 의료, 이주비, 보너스가 붙습니다 ([NRL](https://nrl.sites.sourceflow.co.uk/insights/working-globally/working-in-vietnam)). 한국 중소기업 주재원은 국내 급여의 1.2–1.3배를 받는다는 커뮤니티 증언이 있습니다 ([리멤버 커뮤니티](https://community.rememberapp.co.kr/post/65312)). 베트남의 금형·CAM 엔지니어 공고는 대체로 월 750만–2,500만 동 수준입니다 ([TopCV](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437); [RGF](https://www.rgf-hragent.asia/vn/vietnam/mold-engineer-manufacturing-SDG-105757)). 〔추론〕 이를 종합하면 한국인 경력 전문가의 총비용은 연 6만–10만 달러, 현지 시니어 CAM·공정 엔지니어(월 2,500만–4,500만 동, 약 1,000–1,700달러)의 3–5배로 추정됩니다. 이 비용은 기계 30대의 가공시간 절감으로 충분히 회수될 수 있는 규모입니다. 그러나 회수 여부는 귀사의 기계 시간당 가치에 달려 있습니다. "30대 × 연간 가동시간 × 시간당 가치 × 파일럿에서 측정한 절감률"로 직접 계산해 보시기 바랍니다. 그리고 어느 쪽을 택하든, 장기적으로 표준을 지킬 사람은 현지 엔지니어여야 합니다.

### 권고 로드맵: 측정 → 파일럿 → 채용 → 확산

| 단계 | 기간 | 핵심 활동 〔추론〕 | 담당 | 완료 판단 기준 |
|---|---|---|---|---|
| 0. 측정 기반 | 0–1개월 | 금형별 정합 오차·기계·시각·온도 기록 시작, 표준 워밍업 프로그램 시행, 상하판 동일 기계·동일 시간대 배정, 대표 금형 기준 사이클타임 측정, KITECH 호치민·OneCAD·기계 제조사·공구 대리점 접촉 | 한국인 관리자 + 베트남인 조장 | 4주치 기록 확보, 외부 견적 수령 |
| 1. 외부 진단·파일럿 | 1–6개월 | 1–2대·대표 금형 1종에서 현행 관행 대 새 표준 A/B 시험 (템플릿 + 검증 절삭조건 + 포스트의 HSM 설정), 공구 DB 1차본, 볼바로 기계 순위화, 기상 공구 측정·기준 재프로빙 규칙화 | 외부 컨설턴트(리셀러·공구사·기계사) + 생산에서 50% 빼낸 베트남인 챔피언 1–2명 | 파일럿 금형의 사이클타임·공구비·연마 시간·정합 오차 비교표 |
| 2. 공정 책임자 채용 | 6–12개월 | 파일럿 결과로 직무 확정 후 채용 (한국인·대만인 또는 현지 시니어), 템플릿을 전 기종으로 확대, 사이즈 루프 자동화, 중앙 DNC와 가동률 모니터링, 강재 금형에 VERICUT 시험 도입 | 공정 책임자 + 현지 부책임자 | 표준 템플릿으로 생성한 작업 비율, 평균 오버라이드 값 |
| 3. 확산·고도화 | 12–24개월 | 영점 팔레트 표준화, OMV, 5축 배럴 공구 정삭, 레이저 텍스처 투자·외주 판단, 1–2개 자동화 셀 검토 | 공정 책임자 | 30대 전체 OEE, 정합 불량 재작업 시간 |

〔추론〕 채용 단계에서는 이력서보다 실기 시험이 결정적입니다. 실제 아웃솔 캐비티 모델을 3–4시간 안에 황삭부터 정삭, 포스트 출력까지 프로그래밍하게 하고, 전략, 공구, 절삭조건, 컨트롤러 설정을 설명하게 하십시오. 평가 비중은 실기 35%, 고속가공·절삭 지식 20%, 템플릿·DB·포스트 구축 실적 20%, 측정·품질 10%, 교육·변화관리 15%를 제안합니다. 면접에서는 "황삭 시간을 크게 줄인 사례에서 무엇을 바꿨고 어떻게 증명했습니까?", "신발금형 캐비티에서 Vortex를 쓰지 않을 때는 언제입니까?", "작업자가 매번 이송을 60%로 낮춘다면 어떻게 하시겠습니까?"를 물어보십시오. 평판 조회에서는 후보자가 실제로 표준을 소유했는지, 그리고 그가 떠난 뒤에도 그 표준이 쓰였는지를 확인하셔야 합니다. 실기 시험 거부, 전후 데이터 부재, "작업자는 내 프로그램만 따르면 된다"는 태도는 위험 신호입니다.

변화관리 쪽에서 TWI(Training Within Industry) 작업지도는 일을 핵심 단계, 요점, 이유로 나눠 4단계로 가르치는 표준 교육법입니다 ([Fabrico](https://www.fabrico.io/blog/training-within-industry/)). 1945년 미국 약 600개 기업 보고에서는 86%가 생산을 25% 이상 늘렸다고 했지만, 이는 기업 자가 보고에 기반한 역사적 수치입니다 ([Misiurek & Koch 2014](https://journals.pan.pl//Content/89476/PDF/3-misiurek.pdf)). 〔추론〕 실행 원칙은 다음과 같습니다. 가장 존경받는 베테랑 작업자를 파일럿 공동 책임자로 세워 결과를 "우리 결과"로 만들고, 결과를 베트남어 현황판에 게시합니다. 표준은 한국어·베트남어 병기와 그림으로 작성합니다. 의견은 익명이나 그룹으로 받고, 공개 질책은 피합니다. 보상은 개인 책임 추궁이 아니라 파일럿 기계의 지표와 연동한 팀 보너스로 줍니다. 진척 지표로는 표준 템플릿 사용률, 공구 DB 커버리지, **평균 이송 오버라이드 값(프로그램에 대한 신뢰도의 대리 지표)**, 100주축시간당 공구 파손 수, 정삭 후 1차 치수 합격률을 권합니다. 무엇보다 한국인 경영진은 표준을 누가 결정하는지, 작업자가 표준에서 벗어날 수 있는지, 벗어날 때 어떻게 기록하는지를 명시적으로 위임해야 합니다. 이 위임이 없으면 어떤 인재를 채용해도 기존 관행을 이기지 못합니다.

## 아직 확인되지 않은 것들

이 보고서의 판단 근거에는 분명한 공백이 있습니다. 첫째, 신발금형에 특화된 2023–2026년 CAM 자동화나 사이클타임 단축 사례는 영어로도 한국어로도 찾지 못했습니다. 신발금형 근거는 2001년 Nike 사례와 정량 지표가 없는 ECCO 사례가 전부이며, 개선 수치 대부분은 일반 금형 또는 타 업종의 벤더 발표입니다. 둘째, PowerMill 2025·2026의 공식 신기능 목록은 Autodesk 도움말 사이트에 접속할 수 없어 확인하지 못했고, PowerMill 자체에 AI 기능이 있다는 근거도 없었습니다. 셋째, 모든 컨설팅, 교육, 포스트 개발, VERICUT, 모니터링 솔루션의 가격과 투자 회수 기간을 찾지 못했습니다. 호치민 파트너에 한국어 가능 엔지니어가 있는지도 미확인입니다. 넷째, 신발금형 파팅라인 정합 공차의 공개 기준이 없으며, 베트남 무냉방 공장의 실내 온도 범위나 열대 기후에서의 열변형 연구도 확인하지 못했습니다. 본문의 10–20 µm 대 30–80 µm 오차 예산은 추정치입니다. 다섯째, 베트남 엔지니어와 한국인 주재원 급여는 급여 가이드 원문 PDF를 열지 못해 공고와 커뮤니티 자료에서 추정했습니다. 여섯째, KITECH의 '해외 진출 기업 지원' 프로그램, KOTRA·중진공의 해외법인 기술지원, 퇴직 기술자 해외 파견 제도는 현행 여부를 확인하지 못했습니다. 일곱째, 베테랑 CAM 사용자의 최신 전략 채택률에 대한 직접 연구도 없었습니다. 이 공백들은 1단계 파일럿과 외부 업체 견적으로 대부분 메울 수 있습니다.

## 결론

이번 조사에서 가장 중요한 발견은 질문의 구도 자체가 바뀐다는 점입니다. "최신 소프트웨어로 사람 없이 최적화할 수 있는가"와 "경력자를 채용할 것인가"는 서로 다른 선택지가 아니라 하나의 설계입니다. 소프트웨어가 작업자 의존을 없애려면 먼저 그 소프트웨어에 공장의 지식을 넣을 사람이 필요하고, 그 사람의 가치는 본인이 깎는 금형이 아니라 그가 떠난 뒤에도 30대 기계에서 돌아가는 템플릿, 공구 DB, 포스트에서 나옵니다. 사이즈별 1개씩이라는 생산 방식은 표준화의 걸림돌처럼 보이지만, 실제로는 같은 위상을 반복하는 부품 패밀리여서 템플릿 자동화에 가장 유리한 구조입니다. 공개된 신발금형 CAM 사례가 거의 없다는 사실은, 귀사가 이를 해내고 기록하면 그 자체로 업계에서 드문 경쟁력이 된다는 뜻이기도 합니다.

상하판 정합 문제는 최신 기술보다 '같은 조건에서 두 판을 만드는 규율'의 문제일 가능성이 높습니다. 같은 기계, 같은 시간대, 같은 기준, 같은 공구 측정이라는 규칙은 비용이 거의 들지 않으면서 원인 진단 데이터까지 만들어 줍니다. 따라서 경영진께서 이번 분기에 내리실 첫 결정은 채용 공고가 아니라 측정 기록 시작과 파일럿 승인이어야 합니다. 파일럿 비교표가 나오면 어떤 전문가가 필요한지, 그에게 얼마를 줄 수 있는지가 데이터로 정해집니다.
