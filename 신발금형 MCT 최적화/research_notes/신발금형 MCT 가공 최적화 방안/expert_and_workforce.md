# Expert Hiring, CAM/Process Engineer Role, and Workforce Change Management (Korean-owned shoe-mold factory, HCMC area, ~30 MCs, PowerMill)

Research date: 2026-10-19. Research caveat: web search worked, but full-page fetches failed (DNS errors) on most domains (adecco.com, manpower.com.vn, topcv.vn, hankyung.com, gvm.com.tw, hr1vietnam.com). Several figures below therefore come from search-result excerpts, not full documents. They are marked "(snippet)" where the original was not opened. The report writer should treat those as indicative and, where possible, check them against the primary PDFs before quoting them as final.

## 1. Role definition: what a CAM / manufacturing process engineer should own in a 2026 mold shop, and what job postings ask for

### Takeaway
Job postings in Korea and Vietnam still describe the role narrowly: "operate CAM (PowerMill / hyperMILL / NX), program parts, make NC code". The modern role is broader. It owns the standards (templates, macros, tool and cutting-data library, post-processors) that turn individual programmers' habits into a repeatable shop process, so that new staff become productive in weeks. For a 30-MC shop with no process engineer, the job should be written as "process owner", not "another programmer".

### Cited Findings
- Mold Making Technology says that combining smart macros, machining templates, tool databases and other shop-wide standards lets new recruits "add real value to the business as quickly as possible, often in just a matter of weeks". It also describes analyzing how a shop's engineers program parts and consolidating their best practices into a suite of macros. This is the codification of veteran know-how. Article is about 9 years old (older data). — [MoldMaking Technology: CAM Tools Automate Programming, Aid Five-Axis Machining](https://www.moldmakingtechnology.com/articles/cam-tools-automate-programming-aid-five-axis-machining-and-more)
- A second MoldMaking Technology piece warns that a stored best-practice / cutting-technique database must fit a machine-shop environment, where "staff [are] focused more on cutting chips than programming databases". The implication is that the process engineer must build and maintain the library, because operators will not. — [MoldMaking Technology: Redefining CAM Technology for Moldmakers](https://www.moldmakingtechnology.com/articles/redefining-cam-technology-for-moldmakers)
- A patent background describes the core problem directly: two programs written by two different people for the same part "are probably different", and this "personalized" methodology "prevents the standardization of the part manufacturing process" (vendor/patent framing). — [USPTO patent 7058472, Method and system for computer aided manufacturing](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7058472)
- A CAMWorks mold-shop case study notes a programmer is still needed even with automation. The shop lead both programs and oversees machining (vendor case study). — [CAMWorks: Making Programming Hands-Free](https://camworks.com/case-study/making-programming-hands-free/)
- Typical mold-shop programmer scope from an interview guide: "planning the manufacturing of the different mold components, including mold inserts and plates", and handling design and process changes. — [Siemens NX Manufacturing blog (via search)](https://blogs.sw.siemens.com/nx-manufacturing/wp-json/wp/v2/posts/6155)
- PowerMill high-speed roughing context, relevant to what the engineer should standardize. Vortex first appeared in PowerMILL 2013 as a high-speed area-clearance strategy that uses the full flute length of solid carbide tools. PowerMill 2019 added "Vortex from stock" (Vortex plus adaptive clearing), which shortened a P20 test mold's cycle. The previous "From Model" option took 48 min 28 s (vendor/trade data, older). — [MoldMaking Technology: High-Speed Roughing Strategy](https://www.moldmakingtechnology.com/products/high-speed-roughing-strategy); [CTE: PowerMill 2019 CAM Software](https://ctemag.com/products/powermill-2019-cam-software/)
- **Korean job postings (2024–2026), mostly via 고용24-sourced aggregators (snippets):**
  - A Daegu casting-mold maker does on-site CAM in PowerMill, prefers PowerMill users, and offers KRW 42M/yr. The posting closed 2024-12-30 (older). — [invione / theteams aggregator listings](https://www.theteams.kr/recruit/wanted/2463810)
  - A Dalseong-gun automotive press-die / casting firm is hiring experienced CAD/CAM staff and names POWER MILL as the CAM program (ongoing posting). — [invione listing](https://www.invione.com/jobs/recruitment/all/detail/K180522606010078)
  - A Gyeongju die maker asks for 1+ yr experience at KRW 30M/yr (negotiable) and prefers hyperMILL. A Gwangju injection-mold maker offers KRW 35–50M with CAD/CAM proficiency preferred. A Siheung injection-mold CAM operator role asks for 5+ yrs at KRW 50–52M. — [invione listings](https://www.invione.com/jobs/recruitment/all/detail/K141122606250003); [theteams](https://www.theteams.kr/recruit/wanted/3616828)
  - Across 고용24-based postings, experienced CAM roles range from roughly KRW 30–35M up to about KRW 50M/yr (aggregated from snippets). — same sources as above
- **Vietnamese job postings (2026, snippets):**
  - Carbori Molds Vietnam (Nhơn Trạch, Đồng Nai) is hiring a "Cam Programming Engineer" who must be proficient in PowerMill. Shuttle bus from Biên Hòa, Gò Vấp, Thủ Đức and Bà Rịa, plus a year-end bonus; salary not stated. — [TopCV: kỹ sư khuôn mẫu listings](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437)
  - Giày Apache Việt Nam (Tiền Giang, footwear) is hiring for 2D/3D sole-mold development at VND 7.5–20M/month (posted Feb 2026). Chingluh footwear (Long An) is hiring a "PCC Technical Engineer Footwear – Tooling" at a "competitive" salary. — [TopCV listings](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437); [CareerViet khuôn mẫu](https://careerviet.vn/viec-lam/Khu%C3%B4n-m%E1%BA%ABu-k-vi.html)
  - Woosung Mold Vietnam (a Korean-named plastic-mold firm in Đồng Nai) hired a PowerMill programmer at a negotiable salary (2023, older). — [vieclamnhamay.vn](https://vieclamnhamay.vn/viec-lam/188540-nhan-vien-lap-trinh-co-khi-khuon-ep-nhua)
  - A Vietnamese mold engineer posting combining CAM/CNC with mold cutting lists VND 11–13M/month, a bachelor's degree, and an age limit of 22–35 (location unclear). — [RGF HR Agent: Mold Engineer – Manufacturing](https://www.rgf-hragent.asia/vn/vietnam/mold-engineer-manufacturing-SDG-105757)
- Recent promotional content describes a Vietnamese mold shop whose experienced PowerMill team had toolpath and collision errors that CAM-side simulation missed. It added third-party machine-level verification (CAMplete TruePath) (vendor-adjacent, low reliability). — [sehatdiri.com article](https://www.sehatdiri.com/2026/09/camplete-truepath-powermill-vietnam-mold-shop.html)

### Inferences
- Recommended role charter for this factory (synthesis, not sourced as a single document). In priority order:
  1. Process standards: PowerMill templates, macros and toolpath strategy sets per shoe-mold feature (outsole cavity, sidewall texture area, parting line, vents, electrodes if any).
  2. A tool library with validated cutting data (vc, fz, ae/ap per material and tool holder/stick-out), held in one master database.
  3. Post-processor ownership and version control, plus NC verification and simulation.
  4. Machine HSM-parameter tuning per controller (look-ahead, smoothing and tolerance modes) and per mold stage.
  5. A metrology / QA feedback loop: probing, CMM or scanning results fed back into stock allowances and finishing strategies.
  6. OEE / spindle-utilization data collection and weekly review.
  7. Operator training and certification matrix.
  8. Tool and software vendor management, including Autodesk reseller support and tool-maker trials.
  9. DNC/MES integration roadmap.
- Postings in both countries list software and years of experience, not process-ownership outcomes. The factory's job description should state measurable deliverables (for example, cycle-time reduction on pilot molds, tool-library coverage percentage, number of standardized templates) so candidates self-select toward a process engineer rather than a pure programmer.
- Vietnamese postings often use age caps (22–35), which narrows the senior pool. A senior local hire will likely need to be headhunted, not recruited by posting.

### Gaps
- Full text of 사람인/잡코리아 "금형 CAM 엔지니어" job descriptions could not be fetched; the Korean examples come from 고용24-sourced aggregators (invione, theteams).
- No 2024–2026 global (US/EU) job description specifically titled "Mold Manufacturing Engineer / CAM process engineer" was retrieved with full text. ZipRecruiter shows PowerMill jobs in the US at USD 29–50/hr (listing headline only, Aug 2026). — [ZipRecruiter Powermill jobs](https://www.ziprecruiter.com/Jobs/Powermill)
- No source found on how shoe-mold-specific shops (outsole/EVA/PU/rubber molds with heavy texture work) define this role.

## 2. Single hire vs small team vs external consultant plus internal champion; failure modes

### Takeaway
No rigorous source compares these models for mold shops. The available evidence (codification of best practices into macros/templates, databases that must fit a "chip-cutting" culture, Vietnamese reluctance to challenge superiors) points to one conclusion: a lone expert without an internal counterpart and management backing is the highest-risk option. A hybrid is the lower-risk design: one senior hire or consultant who owns standards, plus 1–2 internal Vietnamese "champions" from the existing operators.

### Cited Findings
- Best practices must be captured from the shop's own engineers and consolidated into macros (MMT). This argues that the expert should mine existing operator know-how, not overwrite it. — [MoldMaking Technology](https://www.moldmakingtechnology.com/articles/cam-tools-automate-programming-aid-five-axis-machining-and-more)
- Best-practice databases fail if they don't fit a shop whose staff focus on cutting chips (MMT). This is a direct pointer to the "standards not adopted" failure mode. — [MoldMaking Technology](https://www.moldmakingtechnology.com/articles/redefining-cam-technology-for-moldmakers)
- In Vietnam, subordinates tend to avoid challenging superiors, making them reluctant to voice concerns (2025 study of change management in Vietnam; not Korea-specific). This makes silent non-adoption more likely than open pushback. — [Humanities and Social Sciences Communications (Nature), 2025: Managers and hybrid workers: cultural perspectives on change management practices in Vietnam](https://www.nature.com/articles/s41599-025-06434-y)
- Korean SMEs in Korea face extreme succession and skill gaps, for example a Jinhae precision-mold founder considering selling because skilled staff can't be found. A Korean hire therefore leaves a tight home market (see section 4). — [더퍼블릭](https://www.thepublic.kr/news/articleView.html?idxno=286264)

### Inferences
- **Option A, single senior expert (Korean expat or Taiwanese).**
  - Pros: fast technical uplift; can speak to Korean management directly.
  - Cons: language barrier with Vietnamese operators; risk of isolation; key-person dependency; highest cost (see section 3).
  - Failure modes: the expert ends up programming the hardest jobs himself and never builds standards; operators run "expert's programs" with conservative overrides (feed-override knob at 50–70%), so no gain shows up; management judges results in 3 months, before the tool library is built.
- **Option B, small team (expert plus 1–2 local CAM engineers).** Better knowledge transfer and continuity. The Vietnamese engineers become the long-term owners. Higher fixed cost, but local engineer salaries are low relative to expat cost (section 3).
- **Option C, external consultant (Autodesk reseller application engineer, tool-maker application engineer, or freelance Korean/Taiwanese expert) plus an internal champion.**
  - Pros: low fixed cost, a fast diagnostic, and access to tool-maker trial support.
  - Cons: knowledge leaves with the consultant unless the champion is given time (for example 50% released from production) and authority.
- Recommended for this profile (inference): Option C as phase 1 (3–6-month diagnostic and pilot on 1–2 machines). Then Option B (hire a senior expert, with a Vietnamese CAM engineer as deputy) once the pilot proves the gain and defines the job. An explicit mandate from Korean management is the precondition for every option: who decides the standard, whether operators may deviate, and how deviations are logged.

### Gaps
- No case studies or surveys found that quantify success or failure rates of "expert hired but isolated" in mold shops.
- No source on typical consulting day-rates for PowerMill or HSM experts in Vietnam.

## 3. Compensation: Korean expat, Vietnamese senior CAM engineer, Taiwanese engineer in Vietnam

### Takeaway
A Vietnamese CAM/mold engineer in southern Vietnam typically posts at about VND 11–25M/month (≈USD 420–950). Senior manufacturing roles reach about VND 45–70M/month (≈USD 1,700–2,700) per one 2026 guide. Experienced expats in engineering are generally quoted at about USD 3,200–6,000/month base before housing and other benefits. Korean expat packages are commonly described as 1.2–1.3× (SME) to 1.5–1.8× (large firm) the Korean base salary, plus housing. All figures are rough, because primary salary-guide PDFs could not be opened.

### Cited Findings
- **Vietnam statutory floor:** the Region I (HCMC etc.) minimum wage is VND 5.31M/month (≈USD 202) from Jan 2026 (snippet). — [工商時報 (China Times), 2025-12-02](https://www.chinatimes.com/newspapers/20251202000096-260202)
- **Market trend:** Manpower Vietnam's 2026 Salary Guide says pay for most junior and mid roles is flat to slightly lower, but manufacturing and engineering is an exception, with many roles stable or rising (snippet, Dec 2025). — [Manpower Vietnam Salary Guide 2026](https://www.manpower.com.vn/en/insights/blogs/2025/12/manpower-vietnam-releases-salary-guide-2026)
- **Adecco Vietnam Salary Guide 2026** has an Engineering & Manufacturing section with role ranges (engineering manager, NPI/R&D engineer, equipment/production engineer). The extracted figures could not be read reliably (PDF fetch failed). — [Adecco Vietnam Salary Guide 2026 PDF](https://www.adecco.com/-/jssmedia/project/adecco/adeccovn/pdf/adecco-vietnam-salary-guide-2026.pdf)
- **Senior manufacturing pay:** VND 45–70M/month, with about 5%/yr manufacturing salary growth (HR1 Vietnam 2026 sector guide, snippet; secondary). — [HR1 Vietnam Salary Guide by Sector 2026](https://hr1vietnam.com/en/news/vietnam-salary-guide-by-sector-2026-tech-banking-fmcg-manufacturing-1139.html)
- **Entry-level production engineers:** VND 12–20M/month (2026, recruiter blog). — [Shelby Global ASEAN](https://shelbyglobal.com.vn/blogs/salary-range-production-jobs-vietnam-2026/)
- **Manufacturing engineer average:** about VND 528M/yr (≈VND 44M/month; ERI modeled data, which likely overstates for SME mold shops). Conflicts with the posting-level data below. — [ERI: Manufacturing Engineer Salary Vietnam 2026](https://www.erieri.com/salary/job/manufacturing-engineer/vietnam); see also [ERI: Manufacturing Engineering Manager Vietnam](https://www.erieri.com/salary/job/manufacturing-engineering-manager/vietnam)
- **Posting-level local data:**
  - Footwear sole-mold 2D/3D development: VND 7.5–20M/month (Apache, Feb 2026). — [TopCV](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437)
  - Mold design engineer in Hưng Yên (north): VND 18–25M (early 2026). — [TopCV](https://www.topcv.vn/tim-viec-lam-ky-su-khuon-mau-cr417cb419cl437)
  - Mold/CAM engineer: VND 11–13M. — [RGF](https://www.rgf-hragent.asia/vn/vietnam/mold-engineer-manufacturing-SDG-105757)
  - CNC service engineer: USD 500–800 (2015, old). — [RGF HR Agent](https://www.rgf-hragent.asia/en/vietnam/cnc-machine-service-engineer-JO-150903-060912)
- **Expat engineering pay:** experienced expats in engineering, energy and tech earn about VND 80–150M/month (USD 3,200–6,000). Internationally mobilized expats also typically get housing, healthcare, relocation and annual bonuses (UK recruiter guide, updated Apr 2026). — [NRL: Working in Vietnam](https://nrl.sites.sourceflow.co.uk/insights/working-globally/working-in-vietnam)
- **Housing allowance benchmark:** a Hanoi manager-level posting lists USD 800/month housing plus manager and transport allowances, healthcare and an annual bonus (not engineering, not Korean). — [kamome.asia listing](https://kamome.asia/mobile_detail/detail/145008/)
- **Korean expat (주재원) structure (community posts, mostly older):**
  - SMEs raise pay 1.2–1.3× and some give no housing or tuition support (single posting only). Large firms pay 1.5× plus housing and tuition. — [리멤버 커뮤니티: 베트남주재원 처우](https://community.rememberapp.co.kr/post/65312)
  - A Blind post describes an offer of about KRW 15M/yr raise plus company housing or housing allowance. A commenter claims "usually 1.8× salary, private school for kids, apartment provided" (anecdotal). — [Blind: 베트남 주재원 연봉 1500 올려받고](https://www.teamblind.com/kr/post/%EB%B2%A0%ED%8A%B8%EB%82%A8-%EC%A3%BC%EC%9E%AC%EC%9B%90-%EC%97%B0%EB%B4%89-1500-%EC%98%AC%EB%A0%A4%EB%B0%9B%EA%B3%A0-%EA%B0%88%EB%A7%8C%ED%95%9C%EA%B0%80-AiUk3aM5)
  - JobKorea engineer 주재원 postings show KRW 45–80M/yr and "KRW 40M~" (snippets). — [JobKorea 베트남 주재원 search](https://www.jobkorea.co.kr/Search/?stext=%EB%B2%A0%ED%8A%B8%EB%82%A8+%EC%A3%BC%EC%9E%AC%EC%9B%90+%EC%B1%84%EC%9A%A9)
  - A WorldJob+ Vietnam-subsidiary posting lists "숙식: 월세 지원" (rent support). — [월드잡플러스](https://www.worldjob.or.kr/advnc/epmtLink.do?joCrtfcNo=E20211026015&joCrtfcDsp=1&joCrtfcDspSn=1&menuId=1000005782)
  - Advice: distinguish 주재원 (dispatched) from 현채 (local hire), since benefits differ greatly. Also check whether the contract follows Korean or Vietnamese labor standards. — [리멤버 커뮤니티](https://community.rememberapp.co.kr/post/65312)
- **Korean domestic benchmark for experienced mold CAM staff:** about KRW 30–52M/yr (section 1 postings). — [invione](https://www.invione.com/jobs/recruitment/all/detail/K141122606250003)
- **Taiwanese engineers (台幹) in Vietnam:**
  - No shoe-mold-specific pay data found. Vietnam CNC postings on 104 often say "待遇面議" (negotiable); one CNC engineer role required PRO/E, CAD, CAM and CNC operation. — [104人力銀行 越南 職缺](https://www.104.com.tw/jobs/search/?keyword=CNC%E7%B7%9A%E5%88%87%E5%89%B2%E6%A9%9F&area=6003002001)
  - Taiwan domestic CNC operator median: about TWD 34k/month under 1 yr and about TWD 40k over 10 yrs (104 Salary Guide 2026; domestic Taiwan, not Vietnam). — [104薪資情報](https://guide.104.com.tw/salary/job/2010001004?analyze=workexp&salary=monthly)
  - USD salaries for expats in Vietnam are often quoted net of tax, while VND salaries are gross. Foreigners resident 183+ days are Vietnamese tax residents. — [someone in vietnam: 外派台幹 越南薪資怎麼算](https://www.someoneinvietnam.com/post/%E5%A4%96%E6%B4%BE%E5%8F%B0%E5%B9%B9%E5%BF%85%E7%9C%8B-%E3%80%8E%E8%B6%8A%E5%8D%97%E8%96%AA%E8%B3%87%E6%80%8E%E9%BA%BC%E7%AE%97%EF%BC%9F%E3%80%8F%E2%80%9D)
  - An older (undated) report says Vietnamese worker pay and Taiwanese cadre pay can differ by up to 10×. — [CIER 中華經濟研究院](https://www.cier.edu.tw/focus-ch/12155/)
  - A 台幹 survey article on junior and senior Vietnam pay exists, but its figures could not be retrieved. — [遠見 GVM: 越南外派真的賺？](https://www.gvm.com.tw/article/106856)

### Inferences
- Indicative annual cost to employer (inference, rough):
  - Senior Vietnamese CAM/process engineer in HCMC/Bình Dương/Đồng Nai: about VND 25–45M/month (≈USD 1,000–1,700). The posting data (≤VND 25M) covers mid-level, and the HR1 senior band (VND 45–70M) covers managers.
  - Korean expat senior CAM expert: Korean base about KRW 50–70M × 1.2–1.5 uplift, plus housing at about USD 800–1,500/month, plus flights, insurance and Vietnamese PIT gross-up if pay is net. That totals roughly USD 60–100k/yr all-in, about 3–5× a senior local engineer.
  - Taiwanese 台幹: likely comparable to or slightly below the Korean expat cost, and typically includes a dormitory.
- Given a 3–5× cost ratio, the business case for an expat expert must rest on measurable machining-hour savings across 30 MCs. A 10–20% cycle-time reduction on 30 machines (inference, to be validated by the technical sections) would likely dwarf an expat package. A local hire still becomes the sustainable owner either way.

### Gaps
- Navigos, Robert Walters and KOTRA salary data could not be retrieved. The Adecco and Manpower PDFs could not be opened for exact engineering numbers.
- No direct source on Korean 현채 (local-hire Korean) engineer salaries in HCMC in 2025–2026.
- No reliable source on Taiwanese shoe-mold engineer pay in Vietnam (the footwear cluster around Bình Dương, Đồng Nai and Long An is largely Taiwanese-run, so this pool exists, but pay data is not published).

## 4. Veteran workforce: aging, skill obsolescence, adoption of modern strategies, knowledge capture, reskilling

### Takeaway
Korea's root industries (뿌리산업, which include 금형) are aging and short of staff:
- About 36.5% of workers were 50+ in 2023.
- Shortages grew about 7× from 2018 to 2023.
- Mid-career (30s–40s) engineers are scarce, which blocks knowledge transfer.

Long tenure means deep tacit skill but not necessarily current CAM technique. There is no direct evidence on Vortex/adaptive adoption by veterans. The gap is usually bridged by codifying their know-how into templates and libraries, plus structured mentoring and side-by-side trials.

### Cited Findings
- **2023 뿌리산업 실태조사 (국가뿌리산업진흥센터):** 40s were 31.7% (232,235 people), 50s 26.4% (193,125), and 60+ 10.1% (74,295), so 50+ ≈ 36.5%. The prior (2022) survey reported 50+ at 33.8%. — [서울경제: 부족인원 5년새 7배로 폭증…뿌리산업, 말라간다](https://www.sedaily.com/article/14032269)
- The six base processes (주조·금형·소성가공·용접·표면처리·열처리) employed 490,843 people in 2023, not back to 500k since 2020. Shortages rose from 2,568 (2018) to 18,232 (2023). — [서울경제](https://www.sedaily.com/article/14032269)
- About 10 in 100 뿌리산업 workers are foreigners (2024). — [전자신문 2024-04-08](https://www.etnews.com/20240408000328?mc=em_010_00001)
- "The owner is transferring skills to foreigners" because Korean workers have disappeared from factories. — [서울경제](https://www.sedaily.com/article/14034198)
- A Hankyung headline describes firms where "the youngest employee is 57" (April 2023; full text not fetched). — [한국경제 2023-04-24](https://www.hankyung.com/article/202304248287i)
- Mold-industry trade press reports aging staff and "no juniors to pass skills to". An absolute shortage of 30s–40s technicians hampers communication between senior and junior engineers and pushes young people out of the field (older articles). — [kidd.co.kr](https://kidd.co.kr/news/163836); [kidd.co.kr](https://kidd.co.kr/news/191306)
- The Korea Die & Mold Industry Cooperative (한국금형공업협동조합) set up 한국금형기술교육원 in 2017 for training and job placement. — [kidd.co.kr](https://kidd.co.kr/news/216550)
- A 2019 뿌리산업 manpower survey report (lead body: 한국금형공업협동조합) has age-distribution tables (older data; mold-specific breakdown not verified). — [2019 뿌리산업 인력현황조사·분석 보고서 PDF](http://www.ksdme.com/NFUpload/nfupload_down.php?tmp_name=20190917143402.6330.8.0.pdf&name=2019+%EB%BF%8C%EB%A6%AC%EC%82%B0%EC%97%85+%EC%9D%B8%EB%A0%A5%ED%98%84%ED%99%A9+%EC%A1%B0%EC%82%AC%EB%B6%84%EC%84%9D+%EB%B3%B4%EA%B3%A0%EC%84%9C%28%EC%B5%9C%EC%A2%85%EB%B3%B8%2C+190904%29-%EB%B3%B5%EC%82%AC.pdf)
- **Tacit-knowledge capture:**
  - AutoForm's "이음 프로젝트" digitized expert press-die know-how with 경북기계공업고. It ran for 6 months, and 10 vocational students secured jobs at die makers (company announcement; effect unverified). — [굿모닝경제](https://www.goodkyung.com/news/articleView.html?idxno=285532)
  - HRD Korea's Meister-net runs 1:1 숙련기술전수 mentoring from master technicians (명장) to successors. — [마이스터넷 숙련기술전수멘토링](https://meister.hrdkorea.or.kr/sub/2/5/1/20160615163908987100_view.do)
- An academic paper notes moldmaking historically depended heavily on expert know-how, and that CAD/CAM/CAE integration reduces this dependence and lead time (2011, older). — [KoreaScience](https://koreascience.kr/article/JAKO201110334668264.pdf)
- In the Korean CAM market, software with high share in subcontract shops and vocational training institutes is easier to hire for (2026 guide). PowerMill, hyperMILL and NX all appear in Korean postings. — [153LAB CAM 소프트웨어 정리 2026](https://153lab.com/cam-software-comprehensive-guide-2026)
- **Vietnam training supply:** a list of 15 CNC programming/operation training centers in Vietnam (vieclamnhamay). — [vieclamnhamay.vn](https://vieclamnhamay.vn/tin-tuc/danh-sach-15-trung-tam-dao-tao-lap-trinh-va-van-hanh-may-cnc-ban-can-biet)
- TWI Job Instruction helps achieve consistent task performance and reduce inconsistency, particularly with an aging workforce (2023 Univ. of Groningen thesis; small-scale). — [Thesis S. van Midden, RUG/HAN](https://www.han.nl/projecten/2023/flexibele-werkinstructies/Thesis_SophievMidden-RUG.pdf)

### Inferences
- A Korean veteran hired from Korea will most likely be 50+ (pool composition above). He will be strong in mold know-how, conservative cutting and problem-solving. He is not necessarily current on:
  - Vortex/adaptive roughing with full-flute carbide;
  - rest-machining and stock-model workflows;
  - 3+2 / 5-axis for deep ribs;
  - machine-side probing, NC verification and data-driven OEE.
- The interview must test currency explicitly (section 6). Tenure is not a proxy.
- The factory's own veteran operators carry conservative "standards" that are tacit knowledge. Those standards encode real failure history (tool breakage, chatter on deep sole cavities) and should be harvested, not dismissed. A practical method: interview operators about why each standard exists, record it, then test it A/B against modern parameters (section 5).
- **Reskilling options (inference; no sourced detail retrieved):**
  - Autodesk reseller PowerMill courses (Vietnam and Korea resellers exist, but schedules were not found);
  - Autodesk's free online learning content;
  - cutting-tool-maker application-engineer days (Sandvik, Mitsubishi, OSG, YG-1 etc.);
  - the 한국금형기술교육원 programs above for Korean staff.
- **Suggested KPIs for reskilling:**
  - % of jobs programmed from the standard template;
  - % of tools in the validated library;
  - feed-override average at the machine (proxy for trust in programs);
  - unplanned tool breakage per 100 spindle-hours;
  - first-pass dimensional yield after finishing.

### Gaps
- No direct evidence (surveys or studies) on whether long-tenured CAM users adopt Vortex/adaptive, 5-axis or probing.
- No mold-only 2023–2025 age statistic found; only all-뿌리산업 figures.
- No details found on Autodesk PowerMill certification availability in 2026, or on PowerMill training providers and prices in Vietnam or Korea.

## 5. Change management for process standardization: pilot cell, A/B trials, metrics, incentives, Vietnamese workforce and Korean–Vietnamese communication

### Takeaway
Standardize through a visible pilot: one or two machines, A/B against the current standard on the same mold features, with metrics the operators help collect. Teach the new standard with TWI-style Job Instruction. Given Vietnamese reluctance to challenge superiors and documented Korean-manager communication friction, build in safe feedback channels and avoid blame-oriented communication. Silent non-compliance is the likely failure mode.

### Cited Findings
- TWI (US, WWII) 1945 report on about 600 companies (historical and self-reported, cited via secondary sources):
  - 86% raised production ≥25%;
  - 100% cut training time ≥25%;
  - about 55% reduced scrap ≥25%. — [Misiurek & Koch 2014, journals.pan.pl](https://journals.pan.pl//Content/89476/PDF/3-misiurek.pdf); [IMCPA Standardized Job Instruction](https://imcpa.com/event/standardized-job-instruction/?print=pdf)
- TWI Job Instruction breaks a job into key steps, key points and reasons. It is taught in 4 stages (prepare, present, try out, follow up) so that every trainer teaches standard work the same way. TWI influenced TPS, TPM and Kaizen. — [Fabrico: Training Within Industry](https://www.fabrico.io/blog/training-within-industry/); [L2L: TWI in the 2020s](https://www.l2l.com/blog/training-within-industry-2020s)
- No rigorous controlled study of TWI-JI impact found; modern academic evidence is small-scale. — [Groningen thesis](https://www.han.nl/projecten/2023/flexibele-werkinstructies/Thesis_SophievMidden-RUG.pdf)
- **Korean firms in Bình Dương (2020 mixed-methods study, 356 survey responses plus 9 interviews):**
  - Vietnamese workers attribute conflicts with Korean managers mainly to working-culture gaps (especially time use) and attitude differences.
  - Apologizing was the most common resolution.
  - Workers often stayed silent when verbally abused. — [Nguyen Thi Hong-Xoan & Catherine Earl, Journal of Industrial Relations, 2020](https://journals.sagepub.com/doi/10.1177/0021909620935423)
- Serious strikes at Korean-invested firms in Vietnam have often traced back to cultural gaps between Korean managers and Vietnamese staff (Kim Tae Kyu, 2015). — [Neliti: Influence of Cultural Differences Between Korean Managers and Vietnamese Staff](https://www.neliti.com/publications/450973/influence-of-cultural-differences-between-korean-managers-and-vietnamese-staff-i)
- Korean managers are often sparing with praise. Confucian values are a shared base for Korean and Vietnamese organizations (2013). — [VNU Journal of Social Sciences and Humanities, 2013](https://js.vnu.edu.vn/SSH/article/download/1416/1380)
- Vietnamese subordinates tend to avoid challenging superiors and are reluctant to voice concerns (2025). — [Humanities & Social Sciences Communications, 2025](https://www.nature.com/articles/s41599-025-06434-y)
- Korean employees prefer compromising and collaborative conflict styles (2012, Korea–US comparison). — [Kim et al. 2012, Journal of Intercultural Communication](https://immi.se/index.php/intercultural/article/view/Kimetal-2012-2)
- Vietnamese expectations of foreign employers differ in work-related attitudes (Western-employer context). — [ResearchGate: Cultural Distance in the Workplace](https://www.researchgate.net/publication/319874790_Cultural_Distance_in_the_Workplace_Differences_in_Work-Related_Attitudes_between_Vietnamese_Employees_and_Western_Employers)
- In foreign-owned workplaces in Vietnam, Taiwanese factories are described as having long hours and dormitory life, versus shorter hours at other foreign firms (2024 personal account). — [商周 Business Weekly](https://www.businessweekly.com.tw/international/blog/3016420)

### Inferences
- **Pilot design (inference):**
  - Pick 1–2 MCs and one recurring mold type (for example an outsole cavity in the usual steel or aluminum).
  - Freeze a baseline under the current conservative standard. Record cycle time per operation, tool life and breakage, surface finish and need for hand polishing, dimensional result, and spindle utilization.
  - Run the new strategy (template plus validated cutting data plus HSM controller settings) on the same features.
  - Publish results on a shop-floor board in Vietnamese.
  - Involve the most respected veteran operator as co-owner of the trial, so the result is "our result".
- **Metrics:**
  - cycle time per mold;
  - spindle-on % / OEE on pilot machines;
  - tool cost per mold;
  - rework/polish hours;
  - first-pass yield;
  - feed-override usage;
  - number of standard deviations requested and approved.
- **Incentives:** small team-based bonuses tied to pilot-machine metrics rather than individual blame. Recognition matters, given that Korean managers are noted to be sparing with praise. Make adopting the standard part of operator skill levels (certification matrix tied to pay grades).
- **Communication:**
  - Use bilingual (Korean–Vietnamese) written standards with pictures.
  - Use a trusted Vietnamese team leader or interpreter as the channel.
  - Collect feedback anonymously or in groups, since individuals avoid challenging superiors.
  - Strictly avoid verbal abuse or public shaming, a documented conflict driver.
  - Korean management should visibly sponsor the pilot but let the process engineer and local champion run it.

### Gaps
- No mold-shop-specific change-management case studies found (for example a shop moving from operator-held standards to central CAM templates).
- No data on incentive schemes used in Vietnamese mold or footwear tooling plants.

## 6. Evaluation criteria and interview questions for hiring the expert

### Takeaway
Public interview guides are generic (G-code, troubleshooting, teamwork). For this role, use a work-sample test: a real shoe-mold part in PowerMill, done under time, with the candidate explaining strategy, tools, cutting data and controller settings. Add questions that probe currency (Vortex/adaptive, rest machining, 3+2/5-axis, probing, NC verification), standards-building ability, and the ability to teach Vietnamese operators.

### Cited Findings
- Generic CNC/CAM interview content (Indeed, RoleCatcher):
  - toolpath generation, part programs and simulation;
  - explaining and troubleshooting G-code;
  - a structured troubleshooting process rather than generic answers;
  - behavioral questions on quality catches and mentoring;
  - teamwork among machinists, programmers and inspectors. — [Indeed: CNC Programmer Interview Questions](https://ca.indeed.com/career-advice/interviewing/cnc-programmer-interview-questions); [RoleCatcher: Use CAM Software interview guide](https://rolecatcher.com/interviews/skills/hard-skills/working-with-computers/using-digital-tools-to-control-machinery/use-cam-software); [Betterteam: Mold Maker interview questions](https://www.betterteam.com/mold-maker-interview-questions)
- Mold-shop programmers plan machining of inserts and plates and must handle design changes mid-job. — [Siemens NX blog via search](https://blogs.sw.siemens.com/nx-manufacturing/wp-json/wp/v2/posts/6155)
- PowerMill Vortex and Vortex-from-stock are the reference high-speed roughing capabilities a modern PowerMill user should know. — [CTE: PowerMill 2019](https://ctemag.com/products/powermill-2019-cam-software/)

### Inferences
- **Evaluation criteria and weights (inference):**
  - (1) Practical PowerMill test, 35%:
    - Program a supplied outsole-mold cavity model (roughing, rest, semi-finish, finish of textured and parting areas) within 3–4 hrs.
    - Score cycle-time estimate, tool count, stock-model use, collision safety, and the postprocessed NC file.
  - (2) HSM and machining knowledge, 20%:
    - cutting data for carbide on the shop's mold steels and aluminum;
    - chip thinning;
    - controller HSM modes (e.g. Fanuc AI contour / smoothing tolerance, Heidenhain cycle 32);
    - holder and stick-out choices.
  - (3) Standards and systems, 20%: describe templates, macros, tool databases and post-processors they have built. Ask for artifacts (sanitized macro files, a tool-library export, before/after cycle-time records).
  - (4) Metrology and QA, 10%: on-machine probing, CMM or scan feedback, how they set finishing allowances.
  - (5) Teaching and change leadership, 15%:
    - mentoring evidence;
    - willingness to work through interpreters;
    - a written mini-plan for "first 90 days in a 30-MC shop with conservative operator standards".
- **Sample interview questions (inference):**
  - "Show a mold where you cut roughing time significantly. What did you change (strategy, tool, data, machine settings), and how did you prove it?"
  - "When would you not use Vortex/adaptive roughing on a shoe-mold cavity?"
  - "How do you set PowerMill tolerance and point distribution versus controller smoothing so you avoid faceting on textured surfaces?"
  - "An operator overrides your feeds to 60% every time. What do you do?"
  - "Describe a post-processor problem you fixed."
  - "How would you build the first version of our tool library in 60 days?"
  - "Which data would you collect weekly to show management progress?"
- **Reference checks:** confirm the candidate actually owned standards, not only programmed jobs, and how long their standards stayed in use after they left.
- **Red flags:**
  - refuses a practical test;
  - can only describe one CAM system or one machine;
  - no data-backed before/after examples;
  - "operators just need to follow my programs" attitude.

### Gaps
- No published PowerMill-specific or mold-specific practical-test rubric found.
- No source found on Autodesk PowerMill professional certification status in 2026 as a hiring filter.
