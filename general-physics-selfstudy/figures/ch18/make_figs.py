"""18장 온도, 열, 열역학 제1법칙 그림. 실행: python3 figures/ch18/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch

F = __file__
HOT = '#e8a090'
COLD = '#9cc3e6'


def dline(ax, p, q, color=fs.GRAY, lw=0.8, ls='--', zorder=1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=zorder)


def darrow(ax, p, q, text=None, color=fs.BLACK, off=(0, 0.12), fontsize=10, ms=8, lw=0.8, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=ms, color=color, lw=lw, zorder=5))
    if text:
        m = ((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1])
        ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color, **kw)


def clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


def pv_axes(w=4.0, h=2.8):
    fig, ax = plt.subplots(figsize=(w, h))
    clean(ax)
    return fig, ax


def mid_arrow(ax, x, y, color, frac=0.5, ms=10):
    i = int(len(x) * frac)
    ax.add_patch(FancyArrowPatch((x[i - 1], y[i - 1]), (x[i + 1], y[i + 1]), arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=6))


# ---------------------------------------------------------------- 18.1 온도 척도
def fig01():
    fig, ax = fs.canvas(4.0, 3.5, xlim=(0.4, 7.3), ylim=(-0.3, 5.25))
    sc = 0.0125        # 1 K = 0.0125 단위
    pts = [(0.0, '절대영도'), (233.15, ''), (273.15, '물의 어는점'), (310.15, '체온'), (373.15, '물의 끓는점(1 atm)')]
    cols = [(1.0, 'K', lambda T: T), (2.6, '°C', lambda T: T - 273.15), (4.2, '°F', lambda T: (T - 273.15) * 9 / 5 + 32)]
    for x0, unit, f in cols:
        ax.add_patch(Rectangle((x0 - 0.12, 0), 0.24, 4.85, fc='white', ec=fs.BLACK, lw=1.0))
        ax.text(x0, 4.95, unit, ha='center', va='bottom', fontsize=10)
    for T, lab in pts:
        y = T * sc
        ax.plot([0.7, 4.5], [y, y], color=fs.GRAY, lw=0.6, ls='--', zorder=0)
        for x0, unit, f in cols:
            v = f(T)
            txt = f'{v:.2f}' if abs(v - round(v)) > 1e-6 else f'{v:.0f}'
            if unit == '°F' and T == 310.15:
                txt = '98.6'
            ax.text(x0 + 0.17, y + 0.04, txt, fontsize=7.5, va='bottom', ha='left')
        if lab:
            ax.text(4.95, y + (0.1 if T == 310.15 else (-0.1 if T == 273.15 else 0)), lab, fontsize=8, va='center')
    ax.text(4.95, 233.15 * sc, '$-40$ °C $=-40$ °F', fontsize=8, va='center', color=fs.FORCE)
    fs.save(fig, F, 'fig18_01')


# ---------------------------------------------------------------- 18.2 비대칭 퍼텐셜과 열팽창
def fig02():
    fig, ax = fs.plot_axes(4.2, 2.8)
    ax.grid(False)
    r = np.linspace(0.97, 2.4, 800)
    U = 4 * (r ** -12 - r ** -6)
    ax.plot(r, U, color=fs.VEL, lw=1.6)
    from scipy.optimize import brentq
    r0 = 2 ** (1 / 6)
    mids = []
    for E, c in ((-0.85, fs.ACC), (-0.6, fs.ORANGE), (-0.35, fs.FORCE)):
        f = lambda x: 4 * (x ** -12 - x ** -6) - E
        a = brentq(f, 0.98, r0); b = brentq(f, r0, 3.0)
        ax.plot([a, b], [E, E], color=c, lw=1.4)
        ax.plot([(a + b) / 2], [E], 'o', color=c, ms=4)
        mids.append(((a + b) / 2, E))
    ax.plot([r0, r0], [-1.05, 0.1], color=fs.GRAY, lw=0.6, ls=':')
    ax.annotate('', xy=(mids[2][0] - 0.03, mids[2][1] + 0.08), xytext=(mids[0][0] - 0.03, mids[0][1] - 0.12), arrowprops=dict(arrowstyle='-|>', color=fs.BLACK, lw=0.8, mutation_scale=8))
    ax.text(1.4, 0.4, '온도가 오르면(에너지가 커지면)\n평균 원자 간격(점)이 커진다', fontsize=8, va='center')
    ax.text(r0 + 0.01, -1.12, '$r_0$', fontsize=9, ha='left', va='top')
    ax.axhline(0, color=fs.GRAY, lw=0.6)
    ax.set_xlim(0.95, 2.4); ax.set_ylim(-1.2, 0.8)
    ax.set_xlabel('원자 사이 거리 $r$', fontsize=9); ax.set_ylabel('퍼텐셜 에너지 $U$', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    fs.save(fig, F, 'fig18_02')


# ---------------------------------------------------------------- 18.2 선팽창과 구멍
def fig03():
    fig, ax = fs.canvas(5.0, 2.2, xlim=(-0.2, 10.4), ylim=(-0.9, 3.6))
    # (가) 막대
    ax.add_patch(Rectangle((0, 2.4), 3.6, 0.4, fc=COLD, ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((0, 1.2), 4.3, 0.4, fc=HOT, ec=fs.BLACK, lw=1.0))
    ax.plot([0, 0], [0.9, 3.1], color=fs.BLACK, lw=1.2)
    dline(ax, (3.6, 2.4), (3.6, 1.0))
    darrow(ax, (0, 2.95), (3.6, 2.95), '$L_0$', off=(0, 0.2))
    darrow(ax, (3.6, 1.0), (4.3, 1.0), r'$\Delta L$', off=(0, -0.25))
    ax.text(4.0, 2.6, '$T$', fontsize=9, va='center')
    ax.text(4.5, 1.4, r'$T+\Delta T$', fontsize=9, va='center')
    ax.text(2.0, -0.6, r'(가) $\Delta L=\alpha L_0\Delta T$', ha='center', fontsize=9)
    # (나) 구멍 뚫린 판
    for (cx, sc, fc, lab) in ((6.4, 1.0, COLD, '$T$'), (8.9, 1.18, HOT, r'$T+\Delta T$')):
        w, h = 1.8 * sc, 1.8 * sc
        ax.add_patch(Rectangle((cx - w / 2, 1.6 - h / 2), w, h, fc=fc, ec=fs.BLACK, lw=1.0))
        ax.add_patch(Circle((cx, 1.6), 0.45 * sc, fc='white', ec=fs.BLACK, lw=1.0))
        ax.text(cx, 1.6 - h / 2 - 0.15, lab, ha='center', va='top', fontsize=9)
        darrow(ax, (cx - 0.45 * sc, 1.6), (cx + 0.45 * sc, 1.6), None, ms=6)
    fs.arrow(ax, (7.45, 1.6), (7.75, 1.6), color=fs.GRAY, lw=1.0, ms=8)
    ax.text(7.65, -0.6, '(나) 구멍도 같은 비율로 커진다', ha='center', fontsize=9)
    fs.save(fig, F, 'fig18_03')


# ---------------------------------------------------------------- 18.3 물의 가열 곡선
def fig04():
    m = 1.00
    ci, cw, Lf, Lv = 2100, 4186, 3.33e5, 2.26e6
    Q = [0]; T = [-20]
    Q.append(Q[-1] + m * ci * 20); T.append(0)
    Q.append(Q[-1] + m * Lf); T.append(0)
    Q.append(Q[-1] + m * cw * 100); T.append(100)
    Q.append(Q[-1] + m * Lv); T.append(100)
    Q = np.array(Q) / 1e6
    fig, ax = fs.plot_axes(4.6, 2.7)
    ax.plot(Q, T, color=fs.FORCE, lw=1.8, marker='o', ms=3)
    labs = ['얼음 가열', '녹음\n$mL_f$', '물 가열', '끓음  $mL_v$']
    pos = [((Q[0] + Q[1]) / 2 + 0.06, -17, 'left'), ((Q[1] + Q[2]) / 2, 8, 'center'), ((Q[2] + Q[3]) / 2 - 0.05, 55, 'right'),
           ((Q[3] + Q[4]) / 2, 106, 'center')]
    for lab, (x, y, ha) in zip(labs, pos):
        ax.text(x, y, lab, fontsize=8, ha=ha, va='bottom' if y > 0 else 'center')
    ax.text(2.9, 30, '수평 구간: 열을 받아도\n온도가 그대로(상변화)', fontsize=8, ha='right', color=fs.GRAY)
    ax.set_xlim(0, 3.2); ax.set_ylim(-25, 125)
    ax.set_xlabel('가한 열 $Q$ (MJ)', fontsize=9); ax.set_ylabel('온도 (°C)', fontsize=9)
    ax.set_yticks([-20, 0, 50, 100])
    ax.tick_params(labelsize=8)
    fs.save(fig, F, 'fig18_04')


# ---------------------------------------------------------------- 예제 18.4 디바이 비열
def fig05():
    from scipy.integrate import quad
    R, TD = 8.314, 300.0
    def debye(T):
        x = TD / T
        I = quad(lambda u: u ** 4 * np.exp(u) / np.expm1(u) ** 2, 0, x)[0]
        return 9 * R * (T / TD) ** 3 * I
    T = np.logspace(np.log10(4), np.log10(1200), 200)
    C = np.array([debye(t) for t in T])
    fig, ax = fs.plot_axes(4.3, 2.8)
    ax.loglog(T, C, color=fs.VEL, lw=1.7, label='디바이 모형 ($\\Theta_D=300$ K)')
    Tl = np.logspace(np.log10(4), np.log10(80), 50)
    ax.loglog(Tl, 1944 * (Tl / TD) ** 3, color=fs.FORCE, lw=1.2, ls='--', label='$T^3$ 법칙')
    ax.axhline(3 * R, color=fs.GRAY, lw=1.0, ls=':', label='뒬롱–프티 $3R$')
    ax.axvspan(10, 20, color=fs.ORANGE, alpha=0.2, lw=0)
    ax.text(14, 0.004, '예제\n10–20 K', fontsize=7.5, ha='center', color=fs.ORANGE)
    ax.set_xlim(4, 1200); ax.set_ylim(2e-3, 60)
    ax.set_xlabel('$T$ (K)', fontsize=9); ax.set_ylabel('$C_m$ (J/(mol·K))', fontsize=9)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7.5, loc='lower right', frameon=False)
    fs.save(fig, F, 'fig18_05')


# ---------------------------------------------------------------- 18.4 피스톤
def fig06():
    fig, ax = fs.canvas(3.8, 2.0, xlim=(-0.3, 7.0), ylim=(-0.6, 3.0))
    ax.plot([0, 6.2], [2.4, 2.4], color=fs.BLACK, lw=1.4)
    ax.plot([0, 6.2], [0.0, 0.0], color=fs.BLACK, lw=1.4)
    ax.plot([0, 0], [0, 2.4], color=fs.BLACK, lw=1.4)
    ax.add_patch(Rectangle((0, 0), 3.6, 2.4, fc='#fbe3d8', ec='none'))
    for xx, yy in np.random.default_rng(3).uniform([0.2, 0.25], [3.4, 2.15], (22, 2)):
        ax.add_patch(Circle((xx, yy), 0.05, fc=fs.GRAY, ec='none'))
    ax.add_patch(Rectangle((3.6, 0.05), 0.35, 2.3, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((3.95, 1.1), 2.6, 0.2, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((4.4, 0.05), 0.35, 2.3, fc='none', ec=fs.GRAY, lw=0.8, ls='--'))
    darrow(ax, (3.6, -0.25), (4.4, -0.25), '$ds$', off=(0, -0.2), fontsize=9)
    fs.arrow(ax, (2.3, 1.7), (3.5, 1.7), color=fs.FORCE, lw=1.6)
    ax.text(2.9, 1.95, '$F=pA$', color=fs.FORCE, fontsize=9, ha='center')
    ax.text(1.4, 0.75, '기체\n$p$, $V$', fontsize=9, ha='center', va='center', bbox=dict(fc='#fbe3d8', ec='none', pad=1), zorder=6)
    ax.text(3.78, 2.6, '넓이 $A$', fontsize=8, ha='center')
    fs.save(fig, F, 'fig18_06')


# ---------------------------------------------------------------- 18.4 일 = pV 곡선 아래 넓이
def fig07():
    fig, ax = pv_axes(3.8, 2.7)
    V = np.linspace(1, 4, 300)
    p = 3.2 / V ** 0.8
    ax.fill_between(V, 0, p, color='#dbe7f3')
    ax.plot(V, p, color=fs.VEL, lw=1.7)
    mid_arrow(ax, V, p, fs.VEL)
    Vs = 2.4; dV = 0.15
    ps = 3.2 / Vs ** 0.8
    ax.add_patch(Rectangle((Vs, 0), dV, ps, fc=fs.ORANGE, alpha=0.6, ec='none'))
    ax.annotate(r'$p\,dV$', (Vs + dV / 2, ps * 0.5), (2.95, 1.45), fontsize=9, color=fs.ORANGE,
                arrowprops=dict(arrowstyle='-', color=fs.ORANGE, lw=0.6))
    ax.plot([1, 4], [3.2, p[-1]], 'o', color=fs.BLACK, ms=4)
    ax.text(1.05, 3.25, '$i$', fontsize=10); ax.text(4.05, p[-1] + 0.05, '$f$', fontsize=10)
    ax.text(1.65, 0.6, r'$W=\int_{V_i}^{V_f}p\,dV$', fontsize=10, ha='center')
    ax.set_xticks([1, 4]); ax.set_xticklabels(['$V_i$', '$V_f$'])
    ax.set_yticks([])
    ax.set_xlim(0, 4.6); ax.set_ylim(0, 3.7)
    ax.set_xlabel('$V$', fontsize=10); ax.set_ylabel('$p$', fontsize=10, rotation=0)
    fs.save(fig, F, 'fig18_07')


# ---------------------------------------------------------------- 예제 18.5 세 경로
def fig08():
    fig, ax = pv_axes(4.0, 2.9)
    Vi, Vf, pi, pf = 2.0, 6.0, 3.0, 1.5
    ax.fill_between([Vi, Vf], 0, [pf, pf], color='#dbe7f3', lw=0)
    ax.plot([Vi, Vi, Vf], [pi, pf, pf], color=fs.ACC, lw=1.6)
    ax.plot([Vi, Vf, Vf], [pi, pi, pf], color=fs.FORCE, lw=1.6)
    ax.plot([Vi, Vf], [pi, pf], color=fs.VEL, lw=1.6)
    for (x0, y0, x1, y1, c) in ((Vi, pi, Vi, pf, fs.ACC), (Vi, pf, Vf, pf, fs.ACC), (Vi, pi, Vf, pi, fs.FORCE),
                                (Vf, pi, Vf, pf, fs.FORCE), (Vi, pi, Vf, pf, fs.VEL)):
        mid_arrow(ax, np.linspace(x0, x1, 21), np.linspace(y0, y1, 21), c)
    ax.plot([Vi, Vf], [pi, pf], 'o', color=fs.BLACK, ms=4, zorder=7)
    ax.text(Vi - 0.15, pi + 0.1, '$i$', fontsize=10, ha='right')
    ax.text(Vf + 0.12, pf - 0.1, '$f$', fontsize=10)
    ax.text(4.0, pi + 0.1, 'B: $W_B=1200$ J', color=fs.FORCE, fontsize=8.5, ha='center', va='bottom')
    ax.text(4.0, pf - 0.12, 'A: $W_A=600$ J', color=fs.ACC, fontsize=8.5, ha='center', va='top')
    ax.text(4.3, 2.35, 'C: $W_C=900$ J', color=fs.VEL, fontsize=8.5, ha='left', va='bottom')
    ax.text(4.0, 0.5, '경로 A의 일\n(색칠한 넓이)', fontsize=7.5, ha='center', color=fs.GRAY)
    ax.set_xlim(0, 7.2); ax.set_ylim(0, 3.7)
    ax.set_xticks([0, 2, 4, 6]); ax.set_yticks([0, 1.5, 3.0])
    ax.set_xlabel(r'$V$ ($10^{-3}$ m$^3$)', fontsize=9); ax.set_ylabel(r'$p$ ($10^5$ Pa)', fontsize=9)
    ax.grid(True, lw=0.4, color='#e0e0e0')
    fs.save(fig, F, 'fig18_08')


# ---------------------------------------------------------------- 18.5 여러 과정
def fig09():
    fig, ax = pv_axes(4.0, 2.9)
    V0, p0, g = 1.0, 3.0, 5 / 3
    V = np.linspace(V0, 3.2, 200)
    curves = [(V, np.full_like(V, p0), fs.FORCE, '등압', (3.25, p0)),
              (np.full(50, V0), np.linspace(p0, 0.6, 50), fs.ACC, '등적', (V0 + 0.07, 0.65)),
              (V, p0 * V0 / V, fs.VEL, '등온 ($pV$ 일정)', (3.25, p0 / 3.2)),
              (V, p0 * (V0 / V) ** g, fs.ORANGE, r'단열 ($pV^\gamma$ 일정)', (3.25, p0 / 3.2 ** g))]
    for x, y, c, lab, tp in curves:
        ax.plot(x, y, color=c, lw=1.6)
        mid_arrow(ax, x, y, c, frac=0.6)
        ax.text(tp[0], tp[1], lab, color=c, fontsize=8.5, va='center')
    Vt = np.linspace(0.6, 3.2, 200)
    for T in (0.6, 1.5, 4.5):
        ax.plot(Vt, T / Vt, color=fs.GRAY, lw=0.5, ls=':')
    ax.plot([V0], [p0], 'o', color=fs.BLACK, ms=4, zorder=7)
    ax.text(V0 - 0.08, p0 + 0.12, '처음 상태', fontsize=8, ha='right')
    ax.set_xlim(0, 4.6); ax.set_ylim(0, 3.8)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$V$', fontsize=10); ax.set_ylabel('$p$', fontsize=10, rotation=0)
    ax.text(0.65, 3.55, '점선: 등온선', fontsize=7.5, color=fs.GRAY)
    fs.save(fig, F, 'fig18_09')


# ---------------------------------------------------------------- 18.5 순환 과정
def fig10():
    fig, ax = pv_axes(3.6, 2.6)
    s = np.linspace(0, 2 * np.pi, 400)
    V = 2.5 + 1.3 * np.cos(s) + 0.15 * np.cos(2 * s)
    p = 2.0 - 0.95 * np.sin(s) + 0.1 * np.sin(2 * s)   # 시계 방향
    ax.fill(V, p, color='#dbe7f3')
    ax.plot(V, p, color=fs.VEL, lw=1.7)
    for fr in (0.12, 0.37, 0.62, 0.87):
        mid_arrow(ax, V, p, fs.VEL, frac=fr)
    ax.text(2.5, 2.0, '알짜 일\n$W=Q$\n(둘러싼 넓이)', ha='center', va='center', fontsize=8.5)
    ax.text(4.0, 3.1, '시계 방향이면 $W>0$', fontsize=8, ha='center', color=fs.GRAY)
    ax.set_xlim(0, 4.8); ax.set_ylim(0, 3.4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$V$', fontsize=10); ax.set_ylabel('$p$', fontsize=10, rotation=0)
    fs.save(fig, F, 'fig18_10')


# ---------------------------------------------------------------- 💡 자유 팽창
def fig11():
    fig, ax = fs.canvas(4.8, 1.8, xlim=(-0.2, 10.2), ylim=(-0.9, 2.8))
    rng = np.random.default_rng(7)
    for x0, full in ((0.0, False), (5.6, True)):
        ax.add_patch(Rectangle((x0, 0), 4.4, 2.2, fc='none', ec=fs.BLACK, lw=2.4))
        w = 4.4 if full else 2.2
        ax.add_patch(Rectangle((x0, 0), w, 2.2, fc='#fbe3d8', ec='none', zorder=0))
        n = 40 if full else 40
        pts = rng.uniform([x0 + 0.12, 0.12], [x0 + w - 0.12, 2.08], (n, 2))
        for q in pts:
            ax.add_patch(Circle(q, 0.05, fc=fs.GRAY, ec='none'))
        if not full:
            ax.plot([x0 + 2.2, x0 + 2.2], [0, 2.2], color=fs.BLACK, lw=1.6)
            ax.text(x0 + 3.3, 1.1, '진공', ha='center', va='center', fontsize=9)
    fs.arrow(ax, (4.65, 1.1), (5.35, 1.1), color=fs.BLACK, lw=1.4)
    ax.text(2.2, -0.45, '(가) 칸막이를 터뜨리기 전', ha='center', fontsize=8.5)
    ax.text(7.8, -0.45, '(나) 나중: $W=Q=0$, $\\Delta E_{\\mathrm{int}}=0$', ha='center', fontsize=8.5)
    ax.text(5.0, 2.55, '단열된 상자', ha='center', fontsize=8, color=fs.GRAY)
    fs.save(fig, F, 'fig18_11')


# ---------------------------------------------------------------- 18.6 평판의 전도
def fig12():
    fig, (a0, a1) = plt.subplots(2, 1, figsize=(3.8, 3.3), sharex=True, gridspec_kw=dict(height_ratios=[1.1, 1]))
    a0.set_xlim(-0.9, 1.9); a0.set_ylim(-0.1, 1.25); a0.axis('off')
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list('ht', [fs.FORCE, '#f3d0c8', COLD, fs.VEL])
    grad = np.linspace(0, 1, 200)[None, :]
    a0.imshow(grad, extent=(0, 1, 0.1, 1.0), aspect='auto', cmap=cm, alpha=0.75)
    a0.add_patch(Rectangle((0, 0.1), 1, 0.9, fc='none', ec=fs.BLACK, lw=1.2))
    a0.text(-0.08, 0.55, '$T_H$', ha='right', va='center', fontsize=10, color=fs.FORCE)
    a0.text(1.08, 0.55, '$T_C$', ha='left', va='center', fontsize=10, color=fs.VEL)
    a0.add_patch(FancyArrowPatch((0.15, 0.55), (0.85, 0.55), arrowstyle='-|>', mutation_scale=14, color=fs.BLACK, lw=1.8))
    a0.text(0.5, 0.67, '$P$', ha='center', fontsize=10)
    a0.text(0.5, 0.25, '열전도도 $k$, 넓이 $A$', ha='center', fontsize=8)
    a0.annotate('', xy=(1, 1.13), xytext=(0, 1.13), arrowprops=dict(arrowstyle='<|-|>', lw=0.8, mutation_scale=7))
    a0.text(0.5, 1.16, '$L$', ha='center', va='bottom', fontsize=10)
    a1.plot([0, 1], [1, 0], color=fs.BLACK, lw=1.6)
    a1.plot([-0.9, 0], [1, 1], color=fs.FORCE, lw=1.0, ls=':'); a1.plot([1, 1.9], [0, 0], color=fs.VEL, lw=1.0, ls=':')
    a1.set_yticks([0, 1]); a1.set_yticklabels(['$T_C$', '$T_H$'])
    a1.set_xticks([0, 1]); a1.set_xticklabels(['0', '$L$'])
    a1.set_xlabel('$x$', fontsize=10, labelpad=0); a1.set_ylabel('$T(x)$', fontsize=9)
    a1.set_ylim(-0.2, 1.25)
    a1.text(0.55, 0.62, r'기울기 $-P/(kA)$', fontsize=8)
    clean(a1)
    a1.spines['left'].set_position(('data', -0.9))
    fig.tight_layout(h_pad=0.2)
    fs.save(fig, F, 'fig18_12')


# ---------------------------------------------------------------- 예제 18.7 단일창·이중창 (그림 18.14)
def fig13():
    Ti, To = 20.0, -10.0
    hi, ho, kg, ka = 8.0, 25.0, 0.80, 0.026
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.6), sharey=True)
    film = 8.0     # 그림에서 대류 경계층의 폭(mm, 개념적)
    cases = [('(가) 단일창', [('in', 1 / hi, film), ('g', 0.004 / kg, 4.0), ('out', 1 / ho, film)]),
             ('(나) 이중창', [('in', 1 / hi, film), ('g', 0.004 / kg, 4.0), ('a', 0.010 / ka, 10.0), ('g', 0.004 / kg, 4.0), ('out', 1 / ho, film)])]
    for ax, (title, layers) in zip(axs, cases):
        Rt = sum(r for _, r, _ in layers)
        P = (Ti - To) / Rt
        x = 0.0; T = Ti
        xs = [x]; Ts = [T]
        for kind, r, w in layers:
            if kind == 'g':
                ax.axvspan(x, x + w, color='#b8d8e8', lw=0)
            elif kind == 'a':
                ax.axvspan(x, x + w, color='#f2f6f9', lw=0)
            else:
                ax.axvspan(x, x + w, color='#f4f4f4', lw=0, hatch='', zorder=0)
            x += w; T -= P * r
            xs.append(x); Ts.append(T)
        ax.plot(xs, Ts, color=fs.FORCE, lw=1.6, marker='o', ms=3)
        ax.axhline(0, color=fs.GRAY, lw=0.6, ls=':')
        ax.set_title(f'{title}: $P={P:.0f}$ W', fontsize=9)
        ax.text(xs[1] + 0.3, Ts[1] + (2.5 if Ts[1] < 5 else 2.0), f'{Ts[1]:.0f} °C', fontsize=8, color=fs.FORCE)
        ax.set_xticks([film / 2, xs[-1] - film / 2])
        ax.set_xticklabels(['실내\n경계층', '실외\n경계층'], fontsize=7.5)
        ax.set_xlim(0, xs[-1])
        clean(ax)
    axs[0].set_ylabel('온도 (°C)', fontsize=9)
    axs[0].set_ylim(-12, 22)
    axs[0].text(10.0, 13, '유리', fontsize=7.5, ha='center', color='#3b7ea1')
    axs[1].text(17.0, 13, '공기층', fontsize=7.5, ha='center', color=fs.GRAY)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, F, 'fig18_14')


# ---------------------------------------------------------------- 18.6 뉴턴 냉각 (그림 18.13)
def fig14():
    fig, ax = fs.plot_axes(4.0, 2.6)
    Tinf, T0, tau = 20.0, 90.0, 1.0
    t = np.linspace(0, 5, 300)
    ax.plot(t, Tinf + (T0 - Tinf) * np.exp(-t / tau), color=fs.FORCE, lw=1.7)
    ax.axhline(Tinf, color=fs.VEL, lw=1.0, ls='--')
    ax.text(4.95, Tinf + 2, r'$T_\infty$', color=fs.VEL, fontsize=10, ha='right', va='bottom')
    Te = Tinf + (T0 - Tinf) / np.e
    ax.plot([tau, tau], [0, Te], color=fs.GRAY, lw=0.7, ls=':'); ax.plot([0, tau], [Te, Te], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot([tau], [Te], 'o', color=fs.BLACK, ms=4)
    ax.annotate(r'$t=\tau$: 온도차가 처음의 $1/e$', (tau, Te), (1.35, 62), fontsize=8,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.plot([0, tau], [T0, Tinf], color=fs.GRAY, lw=0.8, ls='--')
    ax.text(0.08, T0, '$T_0$', fontsize=10, va='center')
    ax.set_xlim(0, 5); ax.set_ylim(0, 100)
    ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_xticklabels(['0', r'$\tau$', r'$2\tau$', r'$3\tau$', r'$4\tau$', r'$5\tau$'])
    ax.set_xlabel('$t$', fontsize=10); ax.set_ylabel('$T$ (°C)', fontsize=9)
    ax.tick_params(labelsize=8)
    fs.save(fig, F, 'fig18_13')


# ---------------------------------------------------------------- 🐍 열 방정식 수치 풀이
def fig15():
    L, N = 0.10, 51
    alpha = 1.1e-4
    dx = L / (N - 1)
    dt = 0.4 * dx ** 2 / alpha
    x = np.linspace(0, L, N)
    T = np.full(N, 20.0); T[0] = 100.0
    t, snaps = 0.0, {}
    for target in [5, 20, 60, 300]:
        while t < target:
            T[1:-1] += alpha * dt / dx ** 2 * (T[2:] - 2 * T[1:-1] + T[:-2])
            t += dt
        snaps[target] = T.copy()
    fig, ax = fs.plot_axes(4.2, 2.7)
    cols = [fs.ORANGE, fs.ACC, fs.VEL, fs.FIELD]
    for (tt, prof), c in zip(snaps.items(), cols):
        ax.plot(100 * x, prof, color=c, lw=1.5, label=f'$t={tt}$ s')
    ax.plot(100 * x, 100 - 800 * x, 'k--', lw=1.0, label='정상상태')
    ax.set_xlabel('$x$ (cm)', fontsize=9); ax.set_ylabel('$T$ (°C)', fontsize=9)
    ax.set_xlim(0, 10); ax.set_ylim(15, 105)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=7.5, frameon=False, loc='upper right')
    fs.save(fig, F, 'fig18_15')


# ---------------------------------------------------------------- 연습문제 10 원통 단열재
def fig16():
    fig, ax = fs.canvas(3.0, 3.0, xlim=(-2.0, 2.4), ylim=(-2.45, 2.0))
    r1, r2 = 0.7, 1.75
    ax.add_patch(Circle((0, 0), r2, fc='#f6efd6', ec=fs.BLACK, lw=1.2))
    ax.add_patch(Circle((0, 0), r1, fc=HOT, ec=fs.BLACK, lw=1.2))
    ax.add_patch(Circle((0, 0), 0.55, fc='white', ec=fs.BLACK, lw=0.8))
    ax.text(0.05, -0.28, '증기', ha='center', va='center', fontsize=8)
    ax.plot([0, r1 * np.cos(2.6)], [0, r1 * np.sin(2.6)], color=fs.BLACK, lw=0.8)
    ax.text(r1 * np.cos(2.6) - 0.22, r1 * np.sin(2.6) + 0.05, '$r_1$', fontsize=9, ha='center')
    ax.plot([0, r2 * np.cos(-2.4)], [0, r2 * np.sin(-2.4)], color=fs.BLACK, lw=0.8)
    ax.text(r2 * np.cos(-2.4) * 0.72 - 0.2, r2 * np.sin(-2.4) * 0.72, '$r_2$', fontsize=9)
    for a in np.linspace(0.3, 1.3, 3):
        fs.arrow(ax, (0.8 * np.cos(a), 0.8 * np.sin(a)), (1.65 * np.cos(a), 1.65 * np.sin(a)), color=fs.FORCE, lw=1.2, ms=8)
    ax.text(1.2, 1.4, '$P$', color=fs.FORCE, fontsize=10)
    ax.text(0.95, -0.35, '단열재\n$k$', fontsize=8, ha='center', va='center')
    ax.text(0.2, -2.05, '안쪽 면 150 °C, 바깥 면 30 °C', fontsize=7.5, va='center', ha='center')
    fs.save(fig, F, 'fig18_16')


for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16):
    f()
