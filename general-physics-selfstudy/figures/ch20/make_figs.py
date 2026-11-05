"""20장 엔트로피와 열역학 제2법칙 그림. python3 figures/ch20/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from math import comb, lgamma
from matplotlib.patches import Circle, Polygon, Rectangle, FancyBboxPatch, FancyArrowPatch

HEAT = fs.ORANGE   # 열의 흐름
WORK = fs.VEL      # 일


def styled_axes(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def reservoir(ax, center, w, h, text, fc):
    x, y = center
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02,rounding_size=0.12',
                                fc=fc, ec=fs.BLACK, lw=1.0, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5, zorder=4)


def fat_arrow(ax, p, q, color, width=0.22, label=None, loff=(0.15, 0), ha='left', fontsize=10, cross=False):
    """에너지 흐름을 나타내는 굵은 화살표."""
    a = FancyArrowPatch(p, q, arrowstyle=f'simple,head_width={width * 2.2:.2f},head_length={width * 1.6:.2f},'
                                         f'tail_width={width:.2f}', mutation_scale=20, fc=color, ec='none', zorder=2)
    ax.add_patch(a)
    if label:
        m = ((p[0] + q[0]) / 2 + loff[0], (p[1] + q[1]) / 2 + loff[1])
        ax.text(*m, label, color=color, fontsize=fontsize, ha=ha, va='center', zorder=5)


def device(ax, center, r, text):
    ax.add_patch(Circle(center, r, fc='white', ec=fs.BLACK, lw=1.2, zorder=4))
    ax.text(center[0], center[1], text, ha='center', va='center', fontsize=9.5, zorder=5)


def flow_diagram(ax, x0=0.0, kind='engine', hot='고온 열저장체 $T_H$', cold='저온 열저장체 $T_C$',
                 qh=r'$Q_H$', qc=r'$Q_C$', w=r'$W$', dev=None, show_w=True, show_qc=True, show_qh=True, w_off=(0, 0.3), rw=2.6):
    """x0를 가운데로 하는 열기관(engine) 또는 냉동기(fridge) 에너지 흐름도. 세로 범위 0~4."""
    reservoir(ax, (x0, 3.6), rw, 0.62, hot, '#f6d5cc')
    reservoir(ax, (x0, 0.4), rw, 0.62, cold, '#d5e3f2')
    c = (x0, 2.0)
    device(ax, c, 0.45, dev or ('열기관' if kind == 'engine' else '냉동기'))
    if kind == 'engine':
        if show_qh:
            fat_arrow(ax, (x0, 3.27), (x0, 2.47), HEAT, label=qh)
        if show_qc:
            fat_arrow(ax, (x0, 1.53), (x0, 0.73), HEAT, width=0.14, label=qc)
        if show_w:
            fat_arrow(ax, (x0 + 0.47, 2.0), (x0 + 1.35, 2.0), WORK, width=0.16, label=w, loff=w_off, ha='center')
    else:
        if show_qh:
            fat_arrow(ax, (x0, 2.47), (x0, 3.27), HEAT, label=qh)
        if show_qc:
            fat_arrow(ax, (x0, 0.73), (x0, 1.53), HEAT, width=0.14, label=qc)
        if show_w:
            fat_arrow(ax, (x0 + 1.35, 2.0), (x0 + 0.47, 2.0), WORK, width=0.16, label=w, loff=(0, 0.3), ha='center')


# ---------------------------------------------------------------- 예제 20.2 자유 팽창
def fig01():
    fig = plt.figure(figsize=(5.5, 2.4))
    ax = fig.add_axes([0.0, 0.05, 0.52, 0.9])
    ax.set_xlim(-0.1, 4.6); ax.set_ylim(-0.2, 3.9); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(3)

    def box(y0, filled_right, title):
        ax.add_patch(Rectangle((0, y0), 4.0, 1.4, fc='none', ec=fs.BLACK, lw=2.4, zorder=3))
        ax.text(-0.05, y0 + 1.55, title, fontsize=9.5, ha='left')
        n = 40
        xs = rng.uniform(0.12, 3.88 if filled_right else 1.88, n)
        ys = rng.uniform(y0 + 0.12, y0 + 1.28, n)
        for x, y in zip(xs, ys):
            ax.add_patch(Circle((x, y), 0.05, fc=fs.VEL, ec='none', zorder=4))
    box(2.0, False, '(가) 처음: 칸막이 왼쪽에만 기체')
    ax.plot([2, 2], [2.0, 3.4], color=fs.BLACK, lw=1.6, zorder=4)
    ax.text(3.0, 2.7, '진공', fontsize=10, ha='center', va='center', color=fs.GRAY)
    box(0.0, True, '(나) 칸막이 제거 후')
    ax.plot([2, 2], [0.0, 1.4], color=fs.GRAY, lw=0.8, ls=':', zorder=4)
    ax2 = fig.add_axes([0.62, 0.2, 0.36, 0.72])
    styled_axes(ax2)
    V = np.linspace(0.8, 2.2, 200)
    ax2.plot(V, 1 / V, color=fs.GRAY, lw=0.8, ls='--')
    Vr = np.linspace(1, 2, 100)
    ax2.plot(Vr, 1 / Vr, color=fs.ACC, lw=1.8)
    ax2.add_patch(FancyArrowPatch((1.45, 1 / 1.45), (1.55, 1 / 1.55), arrowstyle='-|>', mutation_scale=10,
                                  color=fs.ACC, lw=0))
    ax2.plot([1, 2], [1, 0.5], 'ko', ms=4, zorder=5)
    ax2.text(1.03, 1.03, '$i$', fontsize=10)
    ax2.text(2.03, 0.53, '$f$', fontsize=10)
    ax2.text(1.55, 0.86, '가역 등온 경로\n(계산용)', fontsize=8.5, color=fs.ACC, ha='left')
    ax2.annotate('', xy=(1.95, 0.52), xytext=(1.05, 0.98),
                 arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.9, ls=(0, (2, 2)),
                                 connectionstyle='arc3,rad=0.35'))
    ax2.text(1.2, 0.5, '자유 팽창\n(경로 없음)', fontsize=8.5, color=fs.FORCE, ha='center')
    ax2.set_xticks([1, 2]); ax2.set_xticklabels(['$V$', '$2V$'])
    ax2.set_yticks([0.5, 1]); ax2.set_yticklabels([r'$p/2$', '$p$'])
    ax2.set_xlim(0.7, 2.3); ax2.set_ylim(0.3, 1.25)
    ax2.set_xlabel('부피'); ax2.set_ylabel('압력')
    ax2.set_title('(다)', fontsize=9.5, loc='left')
    fs.save(fig, __file__, 'fig20_01')


# ---------------------------------------------------------------- 열기관
def fig02():
    fig, ax = fs.canvas(3.0, 2.6, xlim=(-1.5, 2.1), ylim=(0.0, 4.0))
    flow_diagram(ax, 0.0, 'engine')
    fs.save(fig, __file__, 'fig20_02')


# ---------------------------------------------------------------- 카르노 순환 (p-V)
TH, TC, GAM = 500.0, 250.0, 5 / 3
VA, VB = 1.0, 2.5
K = (TH / TC) ** (1 / (GAM - 1))
VC, VD = VB * K, VA * K


def fig03():
    fig, ax = fs.plot_axes(4.0, 2.9)
    nR = 1.0
    ab = np.linspace(VA, VB, 200); bc = np.linspace(VB, VC, 200)
    cd = np.linspace(VC, VD, 200); da = np.linspace(VD, VA, 200)
    p_ab = nR * TH / ab; p_cd = nR * TC / cd
    p_bc = nR * TH / VB * (VB / bc) ** GAM; p_da = nR * TC / VD * (VD / da) ** GAM
    Vloop = np.r_[ab, bc, cd, da]; ploop = np.r_[p_ab, p_bc, p_cd, p_da]
    ax.fill(Vloop, ploop, color=fs.SURF, alpha=0.45, lw=0)
    ax.plot(ab, p_ab, color=fs.FORCE, lw=1.8); ax.plot(cd, p_cd, color=fs.VEL, lw=1.8)
    ax.plot(bc, p_bc, color=fs.BLACK, lw=1.4); ax.plot(da, p_da, color=fs.BLACK, lw=1.4)
    # 연장 등온선(점선)
    vv = np.linspace(0.7, 8.2, 300)
    ax.plot(vv, TH / vv, color=fs.FORCE, lw=0.6, ls=':'); ax.plot(vv, TC / vv, color=fs.VEL, lw=0.6, ls=':')
    for V, p, lab, off in [(VA, TH / VA, '$a$', (-0.2, 0)), (VB, TH / VB, '$b$', (0.15, 15)),
                           (VC, TC / VC, '$c$', (0.1, -20)), (VD, TC / VD, '$d$', (-0.2, -18))]:
        ax.plot(V, p, 'ko', ms=4, zorder=5)
        ax.text(V + off[0], p + off[1], lab, fontsize=11, ha='center', va='center')
    # 방향 화살표
    for seg_V, seg_p in [(ab, p_ab), (bc, p_bc), (cd, p_cd), (da, p_da)]:
        i = len(seg_V) // 2
        ax.add_patch(FancyArrowPatch((seg_V[i - 3], seg_p[i - 3]), (seg_V[i + 3], seg_p[i + 3]), arrowstyle='-|>',
                                     mutation_scale=11, color=fs.BLACK, lw=0, zorder=4))
    ax.text(1.95, 330, r'$Q_H$ 흡수' + '\n' + r'($T_H$ 등온)', fontsize=9, color=fs.FORCE, ha='left')
    ax.text(4.2, 18, r'$Q_C$ 방출 ($T_C$ 등온)', fontsize=9, color=fs.VEL, ha='left')
    ax.text(5.0, 85, '단열', fontsize=9, ha='left')
    ax.text(1.55, 160, '단열', fontsize=9, ha='right')
    ax.text(2.72, 126, '$W$', fontsize=11, ha='center', va='center')
    ax.set_xlim(0, 8.2); ax.set_ylim(0, 560)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('부피 $V$'); ax.set_ylabel('압력 $p$')
    fs.save(fig, __file__, 'fig20_03')


# ---------------------------------------------------------------- 카르노 순환 (T-S)
def fig04():
    fig, ax = fs.plot_axes(3.6, 2.6)
    ax.grid(False)
    S1, S2 = 1.0, 3.0
    ax.add_patch(Rectangle((S1, 0), S2 - S1, TC, fc=HEAT, alpha=0.18, lw=0))
    ax.add_patch(Rectangle((S1, TC), S2 - S1, TH - TC, fc=fs.SURF, alpha=0.6, lw=0))
    ax.plot([S1, S2], [TH, TH], color=fs.FORCE, lw=1.8)
    ax.plot([S2, S1], [TC, TC], color=fs.VEL, lw=1.8)
    ax.plot([S2, S2], [TH, TC], color=fs.BLACK, lw=1.4)
    ax.plot([S1, S1], [TC, TH], color=fs.BLACK, lw=1.4)
    for (x, y), lab, off in [((S1, TH), '$a$', (-0.18, 0)), ((S2, TH), '$b$', (0.18, 0)),
                             ((S2, TC), '$c$', (0.18, 0)), ((S1, TC), '$d$', (-0.18, 0))]:
        ax.plot(x, y, 'ko', ms=4, zorder=5)
        ax.text(x + off[0], y + off[1], lab, fontsize=11, ha='center', va='center')
    for (p, q) in [((1.9, TH), (2.1, TH)), ((S2, 385), (S2, 365)), ((2.1, TC), (1.9, TC)), ((S1, 365), (S1, 385))]:
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=11, color=fs.BLACK, lw=0, zorder=4))
    ax.text(2.0, 375, r'$W = Q_H - Q_C$', fontsize=10, ha='center', va='center')
    ax.text(2.0, 140, r'$Q_C = T_C\,\Delta S$', fontsize=10, ha='center', va='center', color='#a0521d')
    ax.text(2.0, TH + 50, r'$Q_H = T_H\,\Delta S$ (색칠한 전체 넓이)', fontsize=9, ha='center', va='center',
            color=fs.FORCE)
    ax.annotate('', xy=(S2, 30), xytext=(S1, 30),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(2.0, 55, r'$\Delta S = Q_H/T_H$', fontsize=9, ha='center')
    ax.set_xlim(0, 4.6); ax.set_ylim(0, 620)
    ax.set_xticks([]); ax.set_yticks([TC, TH]); ax.set_yticklabels(['$T_C$', '$T_H$'])
    ax.set_xlabel('엔트로피 $S$'); ax.set_ylabel('온도 $T$')
    fs.save(fig, __file__, 'fig20_04')


# ---------------------------------------------------------------- 오토 순환
def fig05():
    fig, ax = fs.plot_axes(4.0, 2.9)
    r, g = 10.0, 1.4
    V1, V2 = 10.0, 1.0
    T1, T3 = 300.0, 2000.0
    T2 = T1 * r ** (g - 1); T4 = T3 / r ** (g - 1)
    p1, p2, p3, p4 = T1 / V1, T2 / V2, T3 / V2, T4 / V1
    v12 = np.linspace(V1, V2, 200); p12 = p1 * (V1 / v12) ** g
    v34 = np.linspace(V2, V1, 200); p34 = p3 * (V2 / v34) ** g
    ax.fill(np.r_[v12, [V2], v34, [V1]], np.r_[p12, [p3], p34, [p1]], color=fs.SURF, alpha=0.45, lw=0)
    ax.plot(v12, p12, color=fs.BLACK, lw=1.4); ax.plot(v34, p34, color=fs.BLACK, lw=1.4)
    ax.plot([V2, V2], [p2, p3], color=fs.FORCE, lw=1.8); ax.plot([V1, V1], [p4, p1], color=fs.VEL, lw=1.8)
    for V, p, lab, off in [(V1, p1, '1', (0.35, -45)), (V2, p2, '2', (-0.35, 0)), (V2, p3, '3', (-0.35, 0)),
                           (V1, p4, '4', (0.35, 75))]:
        ax.plot(V, p, 'ko', ms=4, zorder=5)
        ax.text(V + off[0], p + off[1], lab, fontsize=11, ha='center', va='center')
    for seg_V, seg_p in [(v12, p12), (v34, p34)]:
        i = 60
        ax.add_patch(FancyArrowPatch((seg_V[i - 3], seg_p[i - 3]), (seg_V[i + 3], seg_p[i + 3]), arrowstyle='-|>',
                                     mutation_scale=11, color=fs.BLACK, lw=0, zorder=4))
    ax.add_patch(FancyArrowPatch((V2, 1200), (V2, 1300), arrowstyle='-|>', mutation_scale=11, color=fs.FORCE, lw=0))
    ax.add_patch(FancyArrowPatch((V1, 60), (V1, 50), arrowstyle='-|>', mutation_scale=11, color=fs.VEL, lw=0))
    ax.text(V2 + 0.45, 1250, r'점화: $Q_H$ 흡수', fontsize=9, color=fs.FORCE, ha='left', va='center')
    ax.text(V1 - 0.25, 180, r'$Q_C$ 방출', fontsize=9, color=fs.VEL, ha='right', va='center')
    ax.text(10.9, 2050, '1→2  단열 압축\n2→3  등적 가열(점화)\n3→4  단열 팽창\n4→1  등적 냉각(배기)',
            fontsize=8.5, ha='right', va='top', linespacing=1.5, multialignment='left')
    ax.set_xticks([V2, V1]); ax.set_xticklabels(['$V_2 = V_1/r$', '$V_1$'])
    ax.set_yticks([])
    ax.set_xlim(0, 11.2); ax.set_ylim(0, 2150)
    ax.set_xlabel('부피 $V$'); ax.set_ylabel('압력 $p$')
    fs.save(fig, __file__, 'fig20_05')


# ---------------------------------------------------------------- 냉동기와 열펌프
def fig06():
    fig, ax = fs.canvas(3.0, 2.6, xlim=(-1.5, 2.1), ylim=(0.0, 4.0))
    flow_diagram(ax, 0.0, 'fridge', dev='냉동기\n열펌프')
    fs.save(fig, __file__, 'fig20_06')


# ---------------------------------------------------------------- 불가능한 장치
def fig07():
    fig, ax = fs.canvas(5.4, 2.7, xlim=(-1.5, 6.0), ylim=(-0.45, 4.0))
    flow_diagram(ax, 0.0, 'engine', show_qc=False, qh='$Q$', w='$W = Q$', w_off=(0.25, 0.32))
    flow_diagram(ax, 4.2, 'fridge', show_w=False, qh='$Q$', qc='$Q$', dev='냉동기')
    for x in (0.0, 4.2):
        ax.plot([x - 0.55, x + 0.55], [1.45, 2.55], color=fs.FORCE, lw=2.2, zorder=6)
        ax.plot([x - 0.55, x + 0.55], [2.55, 1.45], color=fs.FORCE, lw=2.2, zorder=6)
    ax.text(0.0, -0.25, '(가) 켈빈–플랑크 표현 위반', fontsize=9.5, ha='center')
    ax.text(4.2, -0.25, '(나) 클라우지우스 표현 위반', fontsize=9.5, ha='center')
    fs.save(fig, __file__, 'fig20_07')


# ---------------------------------------------------------------- 분자 4개의 미시 상태
def fig08():
    fig, ax = fs.canvas(5.4, 3.1, xlim=(-1.6, 11.2), ylim=(-0.9, 6.4))
    cols = [fs.FORCE, fs.VEL, fs.ACC, fs.ORANGE]
    import itertools
    rows = {n: [] for n in range(4, -1, -1)}
    for mask in itertools.product([0, 1], repeat=4):     # 1 = 왼쪽
        rows[sum(mask)].append(mask)
    bw, bh = 1.5, 0.75
    for r_i, n in enumerate(range(4, -1, -1)):
        y = 5.3 - r_i * 1.15
        ax.text(-1.5, y + bh / 2, f'왼쪽 {n}개', fontsize=9, va='center', ha='left')
        ax.text(10.4, y + bh / 2, f'$W={len(rows[n])}$', fontsize=10, va='center', ha='left')
        for k, mask in enumerate(rows[n]):
            x = 0.2 + k * 1.7
            ax.add_patch(Rectangle((x, y), bw, bh, fc='white', ec=fs.BLACK, lw=0.9))
            ax.plot([x + bw / 2] * 2, [y, y + bh], color=fs.GRAY, lw=0.6, ls=':')
            li = ri = 0
            for m, side in enumerate(mask):
                if side:
                    cx = x + 0.2 + (li % 2) * 0.33; cy = y + 0.53 - (li // 2) * 0.3; li += 1
                else:
                    cx = x + bw / 2 + 0.2 + (ri % 2) * 0.33; cy = y + 0.53 - (ri // 2) * 0.3; ri += 1
                ax.add_patch(Circle((cx, cy), 0.11, fc=cols[m], ec='none', zorder=4))
    ax.text(4.8, -0.65, '빨강·파랑·초록·주황: 구별되는 분자 4개 (칸 왼쪽 절반 | 오른쪽 절반)', fontsize=8.5,
            ha='center')
    fs.save(fig, __file__, 'fig20_08')


# ---------------------------------------------------------------- 분포의 날카로움
def fig09():
    fig, ax = fs.plot_axes(4.0, 2.6)
    for N, c in [(10, fs.VEL), (100, fs.ACC), (1000, fs.FORCE)]:
        n = np.arange(N + 1)
        lnW = np.array([lgamma(N + 1) - lgamma(k + 1) - lgamma(N - k + 1) for k in n])
        Wr = np.exp(lnW - lnW.max())
        if N == 10:
            ax.plot(n / N, Wr, 'o-', color=c, ms=3.5, lw=1.0, label=f'$N={N}$')
        else:
            ax.plot(n / N, Wr, color=c, lw=1.5, label=f'$N={N}$')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.08)
    ax.set_xlabel('왼쪽 절반에 있는 비율 $n/N$'); ax.set_ylabel(r'$W(n)/W_{\max}$')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig20_09')


# ---------------------------------------------------------------- 열저장체와 작은 계
def fig10():
    fig, ax = fs.canvas(3.6, 2.3, xlim=(0, 6.0), ylim=(0, 3.8))
    ax.add_patch(FancyBboxPatch((0.1, 0.1), 5.8, 3.6, boxstyle='round,pad=0.02,rounding_size=0.2',
                                fc='#f6d5cc', ec=fs.BLACK, lw=1.0))
    ax.text(0.35, 3.35, '열저장체 (온도 $T$)', fontsize=9.5, ha='left', va='center')
    ax.text(0.35, 2.9, '에너지 $E_0 - E_i$,  미시 상태 수 $W_R(E_0 - E_i)$', fontsize=8.5, ha='left', va='center')
    ax.add_patch(Circle((3.0, 1.3), 0.62, fc='white', ec=fs.BLACK, lw=1.2, zorder=3))
    ax.text(3.0, 1.38, '작은 계', fontsize=9, ha='center', va='center', zorder=4)
    ax.text(3.0, 1.05, '상태 $i$, $E_i$', fontsize=8.5, ha='center', va='center', zorder=4)
    for a in (160, 20):
        t = np.radians(a)
        p = (3.0 + 1.45 * np.cos(t), 1.3 + 1.45 * np.sin(t)); q = (3.0 + 0.7 * np.cos(t), 1.3 + 0.7 * np.sin(t))
        fs.arrow(ax, p, q, color=HEAT, lw=1.6, ms=11, style='<|-|>')
    ax.text(4.45, 1.95, '에너지 교환', fontsize=8.5, color=HEAT, ha='center')
    ax.text(3.0, 0.35, '전체 에너지 $E_0$ 일정 (고립계)', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig20_10')


# ---------------------------------------------------------------- 2준위계
def fig11():
    fig = plt.figure(figsize=(5.3, 2.4))
    ax = fig.add_axes([0.0, 0.12, 0.36, 0.8]); ax.axis('off')
    ax.set_xlim(0, 3.2); ax.set_ylim(-0.6, 2.4)
    for j, (kt, lab) in enumerate([(0.25, r'$k_BT = 0.25\varepsilon$'), (1.0, r'$k_BT = \varepsilon$'),
                                   (5.0, r'$k_BT = 5\varepsilon$')]):
        x0 = 0.15 + j * 1.05
        f2 = np.exp(-1 / kt) / (1 + np.exp(-1 / kt)); f1 = 1 - f2
        for y, f in [(0.0, f1), (1.5, f2)]:
            ax.plot([x0, x0 + 0.8], [y, y], color=fs.BLACK, lw=1.4)
            ax.add_patch(Rectangle((x0 + 0.15, y + 0.03), 0.5, 0.75 * f, fc=fs.VEL, alpha=0.75, ec='none'))
        ax.text(x0 + 0.4, -0.3, lab, fontsize=8, ha='center')
    ax.text(0.05, 1.5, r'$\varepsilon$', fontsize=10, ha='right', va='center')
    ax.text(0.05, 0.0, '0', fontsize=10, ha='right', va='center')
    ax2 = fig.add_axes([0.5, 0.2, 0.48, 0.72]); styled_axes(ax2)
    x = np.linspace(0.01, 5, 400)
    ax2.plot(x, np.exp(-1 / x), color=fs.VEL, lw=1.7, label=r'$N_2/N_1 = e^{-\varepsilon/k_BT}$')
    ax2.plot(x, np.exp(-1 / x) / (1 + np.exp(-1 / x)), color=fs.FORCE, lw=1.5, ls='--', label=r'$N_2/N$')
    ax2.axhline(1, color=fs.GRAY, lw=0.6, ls=':'); ax2.axhline(0.5, color=fs.GRAY, lw=0.6, ls=':')
    ax2.set_xlim(0, 5); ax2.set_ylim(0, 1.05)
    ax2.set_xlabel(r'$k_BT/\varepsilon$'); ax2.legend(fontsize=8.5, frameon=False, loc='lower right')
    fs.save(fig, __file__, 'fig20_11')


# ---------------------------------------------------------------- 활성화 에너지
def fig12():
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.grid(False)
    x = np.linspace(0, 10, 400)
    U = 0.0 + 1.0 * np.exp(-((x - 5) / 1.3) ** 2) - 0.45 / (1 + np.exp(-(x - 5) * 1.6))
    ax.plot(x, U, color=fs.BLACK, lw=1.6)
    ax.axhline(0, xmin=0.0, xmax=0.5, color=fs.GRAY, lw=0.7, ls='--')
    top = U.max(); xt = x[U.argmax()]
    ax.plot([0.5, xt], [top, top], color=fs.GRAY, lw=0.7, ls='--')
    ax.annotate('', xy=(1.4, top), xytext=(1.4, 0),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=1.0, mutation_scale=9))
    ax.text(1.55, top / 2, '$E_a$', fontsize=11, color=fs.FORCE, va='center')
    ax.text(0.8, -0.12, '반응물', fontsize=9, ha='center', va='top')
    ax.text(9.0, -0.57, '생성물', fontsize=9, ha='center', va='top')
    ax.text(xt, top + 0.08, '활성화 상태', fontsize=9, ha='center', va='bottom')
    ax.set_xlim(0, 10); ax.set_ylim(-0.8, 1.35)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('반응 진행'); ax.set_ylabel('에너지')
    # 볼츠만 분포 꼬리 삽입 그림
    ins = fig.add_axes([0.66, 0.55, 0.3, 0.32])
    E = np.linspace(0, 6, 300)
    for kt, c in [(0.8, fs.VEL), (1.3, fs.FORCE)]:
        ins.plot(E, np.exp(-E / kt) / kt, color=c, lw=1.2)
        ins.fill_between(E[E > 3.5], 0, np.exp(-E[E > 3.5] / kt) / kt, color=c, alpha=0.35, lw=0)
    ins.axvline(3.5, color=fs.BLACK, lw=0.7, ls='--')
    ins.text(3.6, 0.9, '$E_a$', fontsize=8.5)
    ins.set_xticks([]); ins.set_yticks([]); ins.set_xlabel('에너지', fontsize=8)
    ins.set_title('높은 $T$(빨강)일수록 꼬리가 큼', fontsize=8)
    for s in ('top', 'right'):
        ins.spines[s].set_visible(False)
    fs.save(fig, __file__, 'fig20_12')


# ---------------------------------------------------------------- 연습문제 15
def fig13():
    fig, ax = fs.canvas(3.2, 2.6, xlim=(-1.75, 2.1), ylim=(0.0, 4.0))
    flow_diagram(ax, 0.0, 'engine', hot=r'뜨거운 물 1 kg, 온도 $T_1$', cold=r'차가운 물 1 kg, 온도 $T_2$', rw=3.3,
                 qh=r'$\delta Q_1$', qc=r'$\delta Q_2$', w=r'$\delta W$', dev='가역\n기관')
    fs.save(fig, __file__, 'fig20_13')


if __name__ == '__main__':
    names = sys.argv[1:] or [f'fig{i:02d}' for i in range(1, 14)]
    for n in names:
        globals()[n]()
