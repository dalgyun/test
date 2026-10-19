# Upper/lower (and side-mold) mismatch in CNC-machined shoe molds: root causes and modern countermeasures

Scope note: this covers footwear outsole and midsole molds (rubber, EVA, PU, Phylon/IP/compression) that are CNC-machined in aluminum or steel on about 30 3-axis and 5-axis machining centers using PowerMill, in a hot, humid plant near Ho Chi Minh City. The research budget was about 17 search and fetch calls. Two fetches failed with DNS errors (machinery.co.uk and globalprecision.vn), so some findings rest on search-result summaries rather than full-page reads. Treat vendor figures as vendor claims. Wherever a statement is an engineering inference rather than a cited fact, it sits under "Inferences".

---

## 1. Typical tolerance requirements for shoe-mold parting lines and mating halves, and what mismatch causes

### Takeaway
I found no public numeric tolerance for how well shoe-mold halves must align at the parting line. Supplier pages only claim "exact to 3D". The consequences are well documented in patents: flash, a visible ridge or step even without flash, hand-trimming labour, and hand-fitting of the seam. Numeric targets therefore have to come from the brand's or the plant's own specification. Section 8 gives a derived error budget.

### Cited Findings
- On molded outsoles, the parting line is where the mold portions meet and seal. Because that seal is often imperfect, material escapes and forms flash. The parting line is usually placed on an upper edge of the outsole, which often follows a complex 3D curve. — [US 7861765B2, multi-element mold assembly for footwear components](https://patents.google.com/patent/US7861765); [WO2006078653A2](https://patents.google.com/patent/WO2006078653A2/en)
- The same patent family says a parting line can leave a visible ridge even when there is no flash. Getting a clean seam often takes a lot of hand finishing, and heavy cast mold halves can warp as they cool. Machined molds were meant to avoid both problems. — [US 7861765B2](https://patents.google.com/patent/US7861765); [Justia: US 20060175036](https://patents.justia.com/patent/20060175036)
- Two-part shoe molds locate the upper and lower halves with conical positioning posts that seat into notches (US 9878509). Blow-mold tooling aligns its halves with dowels and grooves (US 10703021). Neither patent gives a tolerance value. — [US 9878509 shoe mold structure](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9878509); [US 10703021 cavity mold alignment](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10703021)
- In two-stage shoe injection, a middle mold is removed and the top and bottom molds are then pressed together. This means multi-plate shoe molds stack up alignment error across more than two plates. — [US 8662875](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8662875)
- General molding practice is to repair or replace tooling until flash is within an acceptable tolerance or gone. Otherwise flash has to be removed afterwards by hand trimming, tumbling, media blasting or cryogenic deflashing. — [Apple Rubber, excessive flash](https://www.applerubber.com/seal-design-guide/oring-basics/excessive-flash/)
- Vietnamese and Chinese shoe-mold suppliers advertise high-speed 3-axis and 4-axis CNC and accuracy "exact compared to the 3D drawing", but publish no numeric tolerance. — [Global Precision VN (search snippet)](https://globalprecision.vn/en/cnc-shoe-mold-processing-with-high-precision-to-create-a-prestigious-brand/); [Kinghope shoe mould](https://kinghopegroup.com/shoe-mould/)

### Inferences
- **Mechanism.** Elastomer and foam flash forms where the gap at the land is larger than the melt or compound can bridge. Low-viscosity PU and expanding EVA/IP are the least forgiving. Rubber compression molds deliberately use overflow grooves, but a lateral shift still shows up as a step on the sidewall.
- **Two separate failure modes.** These need different fixes:
  - **Lateral (X/Y) mismatch** shows up as a step line or offset sidewall. It points to a datum or guide-pin problem.
  - **Gap (Z) mismatch** shows up as flash or thick parting skin. It points to a land-height, flatness, Z-offset or tool-length problem.
- **Indicative targets (unverified).** Precision mold-making often works with roughly 0.01–0.02 mm for the shut-off land and roughly 0.01 mm for pin and bushing fits. I found no source confirming these figures for footwear, so the report should label them as unverified.

### Gaps
- No brand-level (Nike, adidas and similar) or industry-standard tolerance for shoe-mold parting-line step or gap was found.
- I could not open the Korean document "신발금형의 관한 모든 것" (happycampus, 31 pages, 2023). It may cover PHYLON and PU mold design. — [happycampus](https://www.happycampus.com/doc/28116077)
- No Vietnamese or Taiwanese case study quantified flash rework cost.

---

## 2. Machine-level error sources: geometry, thermal growth, backlash, calibration, machine-to-machine variation

### Takeaway
Thermal error is the biggest and most variable machine-level error for a plant without climate control. A spindle grows 40–50 µm, needs 20–45 minutes to stabilize, and squareness drifts by 10–14 µm/m as the machine warms. Linear encoders, a fixed warm-up routine, thermal compensation, and periodic ballbar, laser and AxiSet checks are the standard countermeasures. Making the halves of one mold on two different machines adds each machine's own geometric and thermal signature. With 30 machines this is a key source of mismatch.

### Cited Findings
**Thermal**
- Heat from the spindle motor and bearings can lengthen the spindle by 40–50 µm, which reduces Z-axis positioning accuracy. — [US 4471443, thermal displacement compensation](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4471443)
- Warm-up times reported in the literature:
  - An industry article puts spindle time to thermal equilibrium after startup at 20–45 minutes. — [mfgrobots](https://www.mfgrobots.com/Article/repair/52139.html)
  - A micro-milling study found the water-cooled spindle stable after about 20 minutes, while the uncooled spindle was still not stable after 45 minutes. — [Pajor et al., BazTech PDF](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-49ae5a5e-84b9-4fab-b1be-219d1e2e8271/c/Pajor.pdf)
- A first-order thermal model based on the air temperature inside the machine enclosure predicted drift. In that study, opening and closing the shop doors measurably changed the error. — [Optical Engineering 46(10) 103401, 2007](https://proceedings.spiedigitallibrary.org/journals/optical-engineering/volume-46/issue-10/103401/Thermally-induced-errors-in-diamond-turning-of-optical-structured-surfaces/10.1117/1.2795571.full)
- Strong seasonal swings in ambient temperature make thermal-error models less accurate and less robust. Researchers therefore build separate models for different ambient-temperature ranges. — [Sensors 2022, via DOAJ](https://doaj.org/article/c48af10508f7410d893b1d7218ede068)
- Reported compensation results:
  - An RBF neural-network model on a four-axis machining center cut Z-axis thermal error to about 25% of its original value, and improved Z precision by about 65% across different ambient temperatures. — [Springer, Int J Adv Manuf Technol, s00170-012-3978-6](https://link.springer.com/article/10.1007/s00170-012-3978-6)
  - A sensor-based compensation model running in the Siemens 840D compensation module reduced the maximum Z thermal error by about 87% from a cold start and about 50% from a warm state. — [Springer, s00170-023-11877-1](https://link.springer.com/article/10.1007/s00170-023-11877-1)
- On a vertical machining center, warm-up changed squareness by 12 µm/m in the YZ plane and 14 µm/m in the ZX plane, with almost no change in XY. A separate study reported X–Y squareness and scaling drift of more than 10 µm/m during warm-up. — [Univ. of Huddersfield, effect of thermal changes on squareness](https://pure.hud.ac.uk/en/publications/effect-of-thermal-changes-on-the-squareness-error-between-linear-/); [bibliotekanauki.pl](https://bibliotekanauki.pl/articles/103158.pdf)
- Laser-based volumetric characterization of a large machine at 40–60 minute intervals has about 10 µm measurement uncertainty. — [US 11150628](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11150628)

**Encoders and kinematics (Heidenhain)**
- Closed-loop linear scales effectively compensate thermal error in the feed direction, because they measure the actual axis position rather than inferring it from the ball screw. — [Heidenhain US, 2016](https://www.heidenhain.us/?p=13017); [Design News: encoder fights thermal drift](https://www.designnews.com/motion-control/encoder-fights-thermal-drift)
- KinematicsOpt is a TNC cycle in which a touch probe measures a ball on the table. The control then minimizes the spatial error caused by tilting movements and writes the corrected values to the kinematics table. It is described as keeping 5-axis accuracy despite thermal and mechanical change, but it captures the geometry only at the moment of measurement. — [automation.com](https://www.automation.com/article/heidenhain-adds-kinematicsopt-software-to-cnc); [Machinery: Heidenhain spatial-error routines](https://www.machinery.co.uk/machinery-products/heidenhain-software-routines-helps-compensate-for-machining-spatial-errors)

**Renishaw calibration tools**
- The QC20 ballbar separates two kinds of error. Positional errors (scaling, squareness) do not change with feedrate. Dynamic errors (backlash, reversal spikes, servo gain mismatch) do. — [Renishaw QC20-W](https://renishaw.com/resourcecentre/en/download/qc20-w--74856); [Design World](https://www.designworldonline.com/assess-machine-tool-positioning-and-servo-control-performance/)
- A low-authority source warns that a wrong ambient-temperature entry, or a bar warmed by heat from the spindle, still produces a circle plot but skews the squareness and backlash results. — [industrialmonitordirect (low authority)](https://industrialmonitordirect.com/de/blogs/knowledgebase/how-ballbar-tests-determine-angle-renishaw-position-mapping)
- AxiSet Check-Up:
  - Uses the existing spindle probe and a calibration sphere to report pivot-point error along the linear axes, and lathe centre-line error on mill-turns.
  - Recommends correction values and, where possible, corrects the on-machine pivot-point parameters automatically.
  - Renishaw's reasoning: without accurate pivot-point data, the controller cannot reliably control the relative positions of tool and part while the rotary axes move.
  - The analysis app gives PASS/FAIL against tolerances you define and runs on Windows 10 or later.
  - — [Renishaw AxiSet](https://www.renishaw.com/axiset); [Machinery](https://www.machinery.co.uk/content/product-launches/renishaws-axiset-check-up-reveals-centres-of-rotation-relative-to-linear-axes)
- The XR20-W rotary calibrator works with the XL-80 laser interferometer to measure rotary positioning accuracy. Off-axis software allows measurement on 5-axis configurations where the unit cannot sit on the centre of rotation. — [Renishaw news release](https://www.renishaw.com/resourcecentre/en/download/news-release-new-developments-in-understanding-rotary-axes-performance--48113); [Machinery XR20-W](https://www.machinery.co.uk/content/product-launches/renishaw-expands-on-capabilities-of-xr20-w-rotary-axis-calibrator-software)

### Inferences
- **Size of the problem near HCMC.** Workshops without climate control typically see a day/night and process-driven swing of several °C. If one half is cut in the cool morning and the mating half in the hot afternoon, possibly on a different machine, the two inherit different Z growth (tens of µm, uncompensated) and different squareness states (>10 µm/m). That is enough to explain step lines and land gaps with no other fault. The typical ambient range near HCMC was not sourced.
- **Countermeasures, in priority order:**
  1. A standard spindle warm-up program of at least 20–45 minutes, run after every long stop including lunch and shift change.
  2. Linear scales, or the controller's thermal compensation (Fanuc, Siemens 840D or Heidenhain), on machines that cut parting lines.
  3. Assign both halves of a size to the same machine, or to a "matched pair" of machines, and in the same thermal window.
  4. Probe a reference artifact and re-zero Z immediately before the parting-line finishing pass.
  5. A fleet calibration routine:
     - weekly ballbar test at a fixed thermal state
     - laser or XL-80 linear compensation once a year or after crashes
     - AxiSet or KinematicsOpt on 5-axis machines weekly, or before critical side-mold work
  6. Enclose and shade the machines. Keep doors and fans from blowing directly on the machines, since door opening is a documented drift factor.
  7. Log machine temperatures for each job.
- **Matching the fleet.** With 30 machines, rank them by ballbar and positioning results. Reserve the best for shut-off and parting-line finishing, and use the rest for roughing and texture.

### Gaps
- I found no µm-to-µm before/after Z thermal result, only percentages, and no study of shops in tropical, non-climate-controlled plants.
- I found no published residual-error figure for KinematicsOpt or AxiSet after correction.
- I found no source on humidity effects on machine geometry beyond corrosion of mating surfaces and coolant behaviour, which I did not research.

---

## 3. Tool-level error sources: tool length and radius, wear, runout, holders, deflection

### Takeaway
Tool length error passes directly into Z, which is the land gap and flash. Radius error passes into X/Y on walls, which is the step line. An on-machine non-contact setter such as Renishaw NC4 (±0.1 µm 2σ repeatability) measures length and radius at spindle speed and temperature. That captures the spindle's thermal growth, which an off-machine presetter cannot. Shrink-fit holders beat ER collets on runout and rigidity, but runout must be checked at the actual overhang.

### Cited Findings
- Renishaw rates NC4 tool-measurement repeatability at ±0.1 µm 2σ. NC4+ Blue F100 models reach 0.1 µm 2σ and detect tool defects as small as 5 µm. — [Renishaw NC4](https://www.renishaw.com/en/nc4-non-contact-tool-setter--6099); [TMTS listing](https://www.tmts.tw/en/product/179)
- In Renishaw's ZBG case study, a German automotive machining shop uses the NC4 to check tool wear and breakage and to measure tool length during operation, so the machine compensates for thermal growth. This is a customer use, not a published compensation specification. — [Renishaw ZBG case study](https://renishaw.com/resourcecentre/en/details/anwenderbericht-hoehere-prozesssicherheit-in-der-serie--19652)
- Holder runout and rigidity:
  - Shrink-fit holders generally beat ER chucks on balance, nose profile and runout, while ER chucks win on flexibility and cost. — [Protool](https://www.protool-ltd.co.uk/blogs/blog/shrink-fit-tool-holders-explained); [industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/er-vs-tg-collets-cnc-collet-system-selection-guide)
  - One guide gives shrink-fit runout as under 0.005 mm. — [industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/er-vs-tg-collets-cnc-collet-system-selection-guide)
  - A mold-shop case study found shrink fit more rigid than collets, which let the shop raise cutting speed by about 10% and cut cycle time by a similar amount. — [MoldMaking Technology](https://www.moldmakingtechnology.com/articles/shrink-fit-system-helps-moldmaker-boost-cnc-accuracy-productivity-and-tool-life)
  - A vendor claims its integrated ER extension holders keep TIR under 0.0002 in (about 5 µm) at full extension. This is a vendor claim. — [Robbjack ER25-M3](https://robbjack.com/tools/ER25-M3)

### Inferences
- **Measure tools on the machine, not only on a presetter.**
  - A presetter measures the tool cold and at rest. Use it for kitting and as a gross-error check.
  - The final length and radius of the parting-line finishing tool should come from the on-machine laser at operating rpm, after warm-up, immediately before the pass.
  - Re-measure between the core and cavity finishing passes so that tool wear does not differ between the two halves.
- **Ball-mill profile.** Ball-nose profile error and radius tolerance from the tool maker (often ±5–10 µm on stock ball mills) feed straight into 3D surface offset error. Measure with laser profile cycles, or use tight-tolerance ball mills for shut-off surfaces. The stock tolerance figure is my estimate and was not sourced.
- **Long-reach tools.** Long-reach deflection makes walls "uncut" (stock left on) by different amounts on the core and the cavity when their geometry differs. Countermeasures:
  - Use the shortest stick-out possible.
  - Use shrink-fit or hydraulic holders.
  - Use constant engagement in the finishing pass, with equal stepover and stepdown strategies on mating faces.
  - Add a spring pass on the shut-off land.

### Gaps
- I found no published deflection figures for long-reach ball mills in aluminum or P20/NAK80 for shoe molds.
- I found no direct comparison of NC4 against a presetter with thermal effects isolated.
- Blum LaserControl specs were not retrieved.

---

## 4. Setup and datum strategy: common datum, zero-point clamping, on-machine probing, multi-setup consistency, guide-pin sequence

### Takeaway
The most effective structural countermeasure for lateral mismatch is to make every half reference one shared datum system. That means either:
- the guide-pin and bushing holes (or the mold-plate datum edges and bores) are machined in the same setup as the parting surfaces, or
- both halves sit on zero-point pallets and are probed against the same datum features.

Zero-point systems repeat to about 2.5–5 µm. Strain-gauge spindle probes repeat to 0.25 µm 2σ and support 5-axis 3D probing.

### Cited Findings
- Erowa's own pages say zero-point systems repeat "in the micron range" even with frequent changes, with the spigot centering and clamping automatically when inserted. Erowa publishes no number on these pages. — [Erowa: zero-point clamping explained](https://www.erowa.com/en/news/zero-point-clamping-system-explained-function-benefits-n4816); [Erowa VPC/UPC](https://www.erowa.com/en/news/what-zero-point-clamping-systems-enable-in-manufacturing-erowa-n5137)
- A third-party guide says standard zero-point modules repeat within 0.005 mm and premium lines to 0.0025 mm or better. It warns that installed performance depends on cleanliness, pin condition and correct pin roles (locating, compensating and clamping pins). — [Fabrico blog](https://www.fabrico.io/blog/zero-point-clamping-systems/)
- System 3R is listed among the cross-brand-compatible standards, with positioning below 0.005 mm. The source does not cite where the figure comes from. — [Baidu B2B wiki](https://b2bwiki.baidu.com/en/encyclopedic/zero-point-clamping-system)
- Renishaw lists the OMP400 at 0.25 µm 2σ repeatability with 3D performance suited to 5-axis machines. RENGAGE strain-gauge probes such as the OMP400 and RMP600 have sub-µm 2D and 3D pre-travel variation and suit long styli. The RMP400S is also rated 0.25 µm 2σ and is aimed at form verification. — [Renishaw store, OMP400](https://store.renishaw.com/en-LU/product/A-5069-2002); [Renishaw inspection probe technology](https://renishaw.com/en/inspection-probe-technology--32933); [RMP400S](https://www.engineering.com/?p=149613)

### Inferences
- **Recommended datum strategy for shoe molds:**
  1. Machine the reference faces and edges and the pin and bushing bores of both halves first, in one clamping each, on a high-accuracy machine.
  2. Mount each half on a zero-point pallet, or use the bores as locating features (a pin-in-bore, or a probed bore center) for every later operation.
  3. On each machine, re-probe the datum features with a strain-gauge probe before finishing. Use bore centers for X/Y, the land or reference face for Z, and two bores for rotation.
  4. Finish the parting land and the shut-off of both halves in the same thermal window, on the same machine where possible.
  - Avoid indicating the vise jaws, or using an edge-finder, separately for each half. Each such re-datum adds roughly 5–20 µm of independent error (an engineering estimate, not sourced).
- **Guide-pin sequence.** Common practice is either:
  - to machine the pin and bushing holes with the cavity and parting surfaces in one setup, or
  - to bore the pin holes after finishing, with the halves clamped together or located on dowels.

  Either approach avoids the two halves' bores being independently referenced to different machine zeros. I found no shoe-specific source stating the sequence, so this is an inference.
- **Fixturing in heat and humidity.** Dust, chips, rust and coolant film on pallet pins and receivers degrade zero-point repeatability, as Fabrico notes. In a humid tropical plant this argues for:
  - blow-off and air-sense checks
  - cover caps on the receivers
  - stainless or coated receivers
- **Lower-cost zero-point systems.** These exist from Korean, Chinese and Taiwanese makers (OEM pallet systems that copy System 3R/Erowa interfaces, for example). I found no verified repeatability data for them. Require the vendor's repeatability test certificate and test the system in-house with a probe and a master pallet.

### Gaps
- No current Lang (Quick-Point), System 3R or Schunk (VERO-S) repeatability datasheet was retrieved. These vendors typically quote below 5 µm or below 2 µm, which needs verifying.
- No data was found on Korean or Chinese zero-point equivalents.
- No shoe-mold-specific datum or pin-sequence document was found.

---

## 5. CAM and data error sources: CAD tolerance, stitching, mirroring and grading, shrinkage, CAM tolerance and stock, controller smoothing

### Takeaway
I found no shoe-specific or PowerMill-specific source that quantifies these errors. The items below are a structured checklist from engineering knowledge. All of them are uncited, so the report-writer should present them as practices, not sourced facts.

### Cited Findings
- None of the sources I found quantify CAD stitching gaps, mirror or grading errors, or controller smoothing effects specifically for shoe molds. The PowerInspect/OMV sources confirm that PowerInspect integrates with PowerMill and can catch program errors on the machine (see Section 6). — [Autodesk PowerInspect features](https://www.autodesk.com/eu/products/powerinspect/features); [Machinery: Delcam at DMG MORI](https://www.machinery.co.uk/content/technology-spotlights/delcams-latest-cam-developments-filmed-at-dmg-mori)

### Inferences
These are practices, not cited facts.
- **CAD and data**
  - Parting surfaces that come from separate core and cavity models, or that are re-stitched after grading, can carry gaps or overlaps of tens of µm. Build one master parting surface and derive both halves from it as a single body.
  - Size grading by non-uniform scaling, plus mirroring for left and right, can leave the core and cavity scaled about different origins, or the shrinkage factor applied twice. Use one scripted grading pipeline: scale, apply shrink, mirror, then split core and cavity.
  - Shrinkage factors differ for EVA/IP (expanding foam), rubber, PU and TPU. They must be applied identically to both halves and to the pin pattern.
- **CAM in PowerMill**
  - The tolerance on the finishing toolpath for parting and shut-off surfaces should be no more than one-fifth of the target. For example, 0.002–0.005 mm on lands where the target is 0.02 mm.
  - Use thickness = 0, with an identical tool definition (measured radius) on both halves.
  - Do not leave "stock" left over from a semi-finishing template on the shut-off of one half.
  - Use identical lead-in and lead-out and stepover on mating faces.
  - On 5-axis machines, verify the tool-axis definition and collision-avoidance tilt. Tilting changes the effective tool contact point and exposes pivot-point error (see Section 2).
- **Controller smoothing**
  - High-speed smoothing modes (Fanuc AI contour control/Nano Smoothing tolerance, Heidenhain CYCL 32 tolerance, Siemens CYCLE832 tolerance) trade accuracy for speed.
  - On the parting-line finishing pass, set the controller tolerance to the precision level, about 0.005 mm or less, rather than the roughing or texture setting.
  - Put the tolerance mode explicitly in the post-processor so it does not differ from machine to machine across the 30-machine fleet.

### Gaps
- No source quantified controller-smoothing form error, or PowerMill tolerance effects, on parting lines.
- No shoe-specific CAD grading or mirroring error study was found.
- Material shrinkage factor tables were not retrieved.

---

## 6. Measurement and QA: on-machine verification, CMM and 3D scanning, SPC, closed-loop feedback

### Takeaway
On-machine verification in the same clamping, using PowerInspect OMV with a Renishaw strain-gauge probe, lets the shop check the parting land, pin bores and key cavity points before unclamping. One vendor-reported mold-shop case claims below 0.01 mm. Off-machine checks (CMM or blue-light scanning) should then compare both halves to the same CAD datum, at a controlled or compensated temperature.

### Cited Findings
- PowerInspect OMV:
  - It checks the part in place on any CNC with a probe. A Delcam demo showed it catching deliberately inserted program errors, which were then fixed with a corrected program. — [Machinery: Delcam at DMG MORI](https://www.machinery.co.uk/content/technology-spotlights/delcams-latest-cam-developments-filmed-at-dmg-mori); [CIMdata](https://www.cimdata.com/en/industry-summary-articles/item/4708-delcam-at-dmg-mori-open-house-videos-show-latest-cam-developments)
  - The multi-axis option lets 4-, 5- and 6-axis machines check undercuts and angled holes without repositioning the part. — [Machinery: multi-axis OMV](https://www.machinery.co.uk/content/product-launches/multi-axis-option-for-on-machine-verification-package); [MMS](https://mmsonline.com/products/inspection-software-features-multi-axis-option)
  - It integrates with PowerMill. — [Autodesk PowerInspect](https://www.autodesk.com/eu/products/powerinspect/features)
- Inspection sequences can be programmed offline with simulation to limit machine downtime. Renishaw spindle probes such as the MP700 and OMP400 were named as data sources. — [Renishaw and Delcam partnership](https://www.machinery.co.uk/content/news/renishaw-and-delcam-join-up-to-boost-productivity); [Autodesk partner story: probes already installed](https://www.autodesk.com/support/partners/success-stories/giving-good-use-to-probes-already-installed-in-cnc-machines/9808)
- An Autodesk partner story (FMPS) reports a mold shop doing OMV with Fusion and PowerInspect features, at accuracy below 0.01 mm. This is a vendor-reported figure. — [Autodesk: FMPS OMV success](https://www.autodesk.com/support/partners/success-stories/fmps--success-in-implementing-omv-inspection-on-cnc-machines/9850)

### Inferences
- **OMV limitation.** OMV uses the machine's own axes, so it cannot detect machine geometric or thermal errors that are common to cutting and measuring. It can detect tool, wear, setup and program errors. Pair it with periodic CMM or scan audits and with the machine calibration in Section 2.
- **3D scanning.** Blue-light scanners such as Zeiss/GOM ATOS, or lower-cost Shining3D units, are well suited to comparing the whole mold surface with CAD as a color map. Their typical accuracy (roughly 5–20 µm for metrology-grade units, worse for low-cost units) is marginal for verifying a parting-line gap of about 10 µm. Use a CMM or probing for the land and the bores. These accuracy figures are not sourced.
- **SPC and closed loop.**
  - Record, for each mold and size: the probed land height, the pin-bore position, machine ID, ambient and spindle temperature, and time of day.
  - Plotting mismatch against machine and temperature will quickly show whether the fleet problem is thermal, machine-specific or setup-specific.
  - Feed systematic offsets back as work-offset or tool-wear corrections, or into the machine thermal-compensation tables.

### Gaps
- No Renishaw Productivity+ or Blum on-machine-measurement accuracy figures were retrieved.
- No GOM/Zeiss or Shining3D accuracy specs were retrieved.
- No SPC case study for shoe molds was found.

---

## 7. Material and thermal error sources: aluminum expansion, stress relief, clamping deformation

### Takeaway
Aluminum expands at about 23 µm/m·K, about 2.5 times as much as steel. A typical shoe-mold half 300–350 mm long therefore changes by about 7–8 µm per °C. Parts that are measured warm or cut at different temperatures carry tens of µm of apparent error. Stress-relieved plate (T651), roughing followed by rest or stress relief before finishing, symmetric material removal, and low-distortion clamping control the distortion side.

### Cited Findings
- **Thermal expansion of the part**
  - ISO 1 sets 20 °C as the reference temperature for dimensional measurement. Aluminum's coefficient is about 23 µm/m·K. A 200 mm aluminum part grows about 46 µm for a 10 K rise, about 2.5 times as much as steel. — [Keyence: temperature and measurement](https://www.keyence.co.in/ss/products/measure-sys/measurement-selection/environment/thermal-expansion.jsp); [mabri.vision 2026](https://mabri.vision/en/2026/08/04/temperature-influence-measurement-technology/)
  - A part measured straight off the machine, warmer than ambient, carries its whole thermal variation into the measurement as error. The standard correction is ΔL = L·α·ΔT. — [MMS: temperature compensation](https://www.mmsonline.com/columns/temperature-compensation); [Verisurf KB](https://support.verisurf.com/portal/en/kb/articles/compensating-fo)
  - Temperature fluctuations significantly affect gauge R&R on the shop floor once tolerances are tight relative to the part size. — [Machine Design: correcting for thermal measurement errors](https://www.machinedesign.com/archive/article/21818680/correcting-for-thermal-measurement-errors)
  - Vendor guidance suggests soaking parts for at least an hour after moving them between locations. An ASQ study guide notes that the right soak time depends on reaching equilibrium and on gradients, not on a universal rule. — [Keyence](https://www.keyence.ca/ss/products/measure-sys/measurement-selection/basic/error-factors.jsp); [ASQ CCT study guide](https://open-exam-prep.com/study-guides/asq-cct/calibration-environment/environmental-control-monitoring)
- **Residual stress and distortion**
  - In thick aluminum plate, distortion is driven mainly by the bulk residual stress in the stock. Machining-induced stress matters more for thin-walled parts. — [Mondragon University paper (PDF)](https://ebiltegia.mondragon.edu/xmlui/bitstream/20.500.11984/5651/3/Reduction%20of%20distortions%20in%20large%20aluminium%20parts%20by%20controlling%20machining%20induced%20residual%20stresses.pdf)
  - 6061-T6 and 7075-T6 can bow or twist, especially in thin sections. In one example, a 2 in block cut down to 0.5 in distorted by more than 0.100 in. — [RapidDirect: CNC machining warping](https://www.rapiddirect.com/blog/cnc-machining-warping-causes-and-fixes/)
  - Asymmetric removal causes uneven stress relief. Balance the cuts or alternate sides, and use temporary supports. — [RapidDirect](https://www.rapiddirect.com/blog/cnc-machining-warping-causes-and-fixes/); [industrialmonitordirect: aluminum warping](https://industrialmonitordirect.com/blogs/knowledgebase/resolving-aluminum-warping-in-cnc-milling-operations)
  - Stretched T651 temper has much lower residual stress than T6. One seller blog claims ≤50 MPa against 120–150 MPa, and ≤0.05 mm/m distortion. This is unverified. — [Alibaba seller blog, 6061-T651](https://seller.alibaba.com/blogs/2026/southeast-asia/metals-materials/6061-t651-stress-relieved-aluminum-machining-guide-alibaba-b2b)
  - Shop practice (forum): stress relief at about 350 °F (177 °C) for 8–10 hours before final machining, cooled in still air. This has no formal specification behind it. — [Engineers Edge forum](https://www.engineersedge.com/wwwboard/posts/8920.html)
  - Clamping technique significantly affects the surface topography of milled aluminum. — [NSF PAR](https://par.nsf.gov/biblio/10313957)

### Inferences
- **Worked example.** This applies the 23 µm/m·K coefficient from the sources.
  - A 330 mm aluminum mold half cut at 28 °C and measured or mated at 34 °C differs by 330 mm × 23e-6 × 6 = about 46 µm in length.
  - If the core is cut on a cooled morning machine and the cavity on a hot afternoon machine, a 3 °C difference between the part temperatures alone gives about 23 µm of length mismatch. That is on the order of a visible step at the toe and heel.
  - Steel halves would show about 40% of this.
- **Countermeasures**
  - Keep both halves at the same temperature: flood or through-coolant at a controlled temperature (a coolant chiller), and stage stock in the machining hall overnight.
  - Probe and finish both halves within a short window.
  - Measure with temperature compensation (probe software and CMM both support α·ΔT).
  - Add a symmetric roughing allowance, then unclamp and rest (or stress-relieve), then re-clamp lightly and finish.
  - Use a vacuum chuck or zero-point clamping on the plate's underside rather than heavy side-clamping on vise jaws, which distorts thin side-mold plates.
- **Humidity.** In HCMC conditions the main effects are corrosion or oxide film on the steel datum faces, pin bores and zero-point receivers, and condensation when stock or molds move between cooled and hot areas. Protect with rust-preventive oil and receiver caps. These effects are not sourced.

### Gaps
- No ambient-temperature data was retrieved for Vietnamese shoe-mold factories.
- No coolant-chiller case study for aluminum mold machining was found.
- No primary datasheet stress figures for 6061-T651 or 7075-T651 were found (only a seller blog).

---

## 8. Best practices from precision mold makers (Japan, Germany, Taiwan), and shoe-mold literature

### Takeaway
I found no shoe-mold-specific technical literature or case study with quantitative alignment data. Precision mold makers in Japan and Germany, judging from vendor and trade sources, combine these elements:
- climate-controlled or thermally managed machining halls
- linear scales and thermal compensation
- zero-point pallets used across machines and the EDM/CMM
- on-machine probing and OMV
- shrink-fit tooling with on-machine laser tool setting
- periodic ballbar, laser and kinematics calibration

All of these address the error sources in Sections 2–7.

### Cited Findings
- A German machining shop uses the NC4 to compensate for thermal growth during machining. — [Renishaw ZBG case study](https://renishaw.com/resourcecentre/en/details/anwenderbericht-hoehere-prozesssicherheit-in-der-serie--19652)
- Heidenhain's approach (closed-loop linear scales plus KinematicsOpt) targets thermal and kinematic drift. — [Heidenhain US](https://www.heidenhain.us/?p=13017); [automation.com](https://www.automation.com/article/heidenhain-adds-kinematicsopt-software-to-cnc)
- A Norwegian user (Norcam) reported that all the probes already fitted to its machining centers were compatible with OMV. — [Autodesk partner story](https://www.autodesk.com/support/partners/success-stories/giving-good-use-to-probes-already-installed-in-cnc-machines/9808)

### Inferences
- **Diagnosis tree for the report.** Classify each mismatch case by its symptom.

| Symptom | Likely sources | Test |
|---|---|---|
| Lateral step that is constant all round | Datum or work-offset error, pin-bore position, zero-point contamination | Probe the pin-bore centers on both halves against the shared datum |
| Lateral step that grows toward toe and heel (scale-like) | Thermal size difference (part or machine), grading/shrink scaling error, linear-axis scale error | Compare temperatures at the time of cutting, check the CAD scale origin, laser-check the axis |
| Lateral step that is twisted (rotation) | Datum rotation, squareness of the machine | Two-bore rotation probing, ballbar squareness |
| Uniform Z gap or flash | Tool-length or Z thermal growth, land-height offset, CAM stock left on | On-machine laser re-measure, OMV probe of land height |
| Z gap that varies (wavy, local) | Plate distortion or residual stress, clamping deformation, controller smoothing, tool deflection | Flatness check after unclamping, recut with a tighter controller tolerance, spring pass |
| Mismatch only on 5-axis or side molds | Pivot-point or kinematic error, rotary positioning error | AxiSet Check-Up / KinematicsOpt, XR20-W |
| Mismatch only between certain machine pairs | Machine-to-machine geometric or thermal signature | Ballbar and XL-80 ranking across the fleet; pair halves on the same machine |

- **Indicative error budget for an aluminum shoe mold at about 300 mm, in a plant without climate control.** These are ranges assembled from the cited figures, for each source when uncontrolled:

| Source | Uncontrolled | Controlled |
|---|---|---|
| Part thermal | ~7 µm per °C of difference between halves | |
| Spindle Z growth | up to 40–50 µm | a few µm (warm-up, compensation, in-cycle laser re-measure) |
| Squareness drift | >10 µm/m (~3 µm over 300 mm) | |
| Zero-point repeatability | 2.5–5 µm | |
| Probe | ≤1 µm | |
| Tool setter | ≤1 µm (plus ball-profile error) | |

- **Achievable result.** With the controls in place, a parting-land and pin-alignment mismatch of about 10–20 µm between halves looks achievable. Without them, 30–80 µm is plausible. This is an inference from the component figures, not a measured result.

### Gaps
- No Japanese (e.g. Makino or Sodick white papers), Taiwanese or Korean shoe-mold-maker case study with numeric results was retrieved.
- No Vietnamese shoe-mold industry study was found.
- Fetches of globalprecision.vn and machinery.co.uk failed with DNS errors.
