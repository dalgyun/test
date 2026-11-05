"""35장 특수 상대성 이론 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch

LIGHT_C = fs.ORANGE   # 빛(광선·빛 신호)


def gam(b):
    return 1 / np.sqrt(1 - b ** 2)


def axes2(ax, o, lx, ly, xl, yl, color=fs.BLACK, fontsize=11):
    """o에서 시작하는 x, y 좌표축 한 쌍."""
    fs.arrow(ax, o, (o[0] + lx, o[1]), color=color, lw=1.2, ms=10)
    fs.arrow(ax, o, (o[0], o[1] + ly), color=color, lw=1.2, ms=10)
    fs.label(ax, (o[0] + lx + 0.15, o[1] - 0.15), xl, color=color, fontsize=fontsize)
    fs.label(ax, (o[0] - 0.18, o[1] + ly + 0.05), yl, color=color, fontsize=fontsize)


def hdim(ax, x0, x1, y, text, color=fs.GRAY, ty=None, fontsize=10, tick=0.08):
    """수평 치수선: y 높이에 양쪽 화살표, 글자는 ty 높이(기본: 아래)."""
    from matplotlib.patches import FancyArrowPatch
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle='<|-|>', mutation_scale=8, color=color, lw=0.8, shrinkA=0, shrinkB=0))
    for xx in (x0, x1):
        ax.plot([xx, xx], [y - tick, y + tick], color=color, lw=0.6)
    ax.text((x0 + x1) / 2, y - 0.2 if ty is None else ty, text, ha='center', va='center', fontsize=fontsize, color=color)


def flash(ax, p, r=0.16, color='#f1c40f'):
    th = np.linspace(0, 2 * np.pi, 17)
    rr = np.where(np.arange(17) % 2 == 0, r, r * 0.45)
    ax.add_patch(Polygon(np.c_[p[0] + rr * np.cos(th), p[1] + rr * np.sin(th)], fc=color, ec=fs.ORANGE, lw=0.8, zorder=8))


# ---------------------------------------------------------------- 35.1 두 관성 기준틀
def fig01():
    fig, ax = fs.canvas(4.8, 2.9, xlim=(-0.5, 6.2), ylim=(-1.2, 2.9))
    axes2(ax, (0, 0), 5.6, 2.4, r'$x$', r'$y$')
    o2 = (2.0, 0.25)
    S2 = fs.VEL
    fs.arrow(ax, o2, (o2[0] + 3.6, o2[1]), color=S2, lw=1.2, ms=10)
    fs.arrow(ax, o2, (o2[0], o2[1] + 2.1), color=S2, lw=1.2, ms=10)
    fs.label(ax, (o2[0] + 3.75, o2[1] + 0.2), r"$x'$", color=S2)
    fs.label(ax, (o2[0] - 0.2, o2[1] + 2.15), r"$y'$", color=S2)
    fs.label(ax, (-0.25, -0.25), r'$O$'); fs.label(ax, (o2[0] - 0.22, o2[1] - 0.2), r"$O'$", color=S2)
    fs.label(ax, (0.55, 2.2), r'$S$', fontsize=13)
    fs.label(ax, (2.55, 2.2), r"$S'$", fontsize=13, color=S2)
    fs.vec(ax, (2.6, 1.55), (0.9, 0), color=fs.VEL, lw=2, label=r'$\vec v$', loff=(0.2, 0.0))
    P = (4.6, 1.3)
    fs.dot(ax, P, r=0.07, color=fs.FORCE)
    fs.label(ax, (P[0] + 0.15, P[1] + 0.25), '사건 $(x, t)$\n$(x\', t\')$', fontsize=9, ha='left')
    ax.plot([P[0], P[0]], [0, P[1]], ls=':', color=fs.GRAY, lw=0.9)
    hdim(ax, o2[0], P[0], o2[1] + 0.2, r"$x'$", color=S2, ty=o2[1] + 0.42)
    hdim(ax, 0, o2[0], -0.3, r'$vt$', ty=-0.52)
    hdim(ax, 0, P[0], -0.8, r'$x$', ty=-1.02)
    fs.save(fig, __file__, 'fig35_01')


# ---------------------------------------------------------------- 35.2 동시성의 상대성
def car(ax, x0, y0, w=4.0, h=0.8, ls='-', alpha=1.0):
    ax.add_patch(Rectangle((x0, y0), w, h, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, ls=ls, alpha=alpha, zorder=2))
    for xx in (x0 + 0.6, x0 + w - 0.6):
        ax.add_patch(Circle((xx, y0 - 0.12), 0.12, fc='white', ec=fs.BLACK, lw=0.9, alpha=alpha, zorder=2))


def fig02():
    fig, ax = fs.canvas(5.4, 3.5, xlim=(-3.6, 4.4), ylim=(-4.75, 1.4))
    b = 0.4
    # (가) S'
    y0 = 0.2
    car(ax, -2, y0)
    flash(ax, (0, y0 + 0.4))
    for s in (-1, 1):
        fs.arrow(ax, (0.2 * s, y0 + 0.4), (1.95 * s, y0 + 0.4), color=LIGHT_C, lw=1.6, ms=9)
    fs.label(ax, (0, y0 + 1.05), "(가) 기차 기준틀 $S'$: 빛이 앞뒤 벽에 동시에 도착", fontsize=9)
    fs.label(ax, (-2.0, y0 - 0.45), '뒷벽', fontsize=8.5); fs.label(ax, (2.0, y0 - 0.45), '앞벽', fontsize=8.5)
    # (나) S: 두 순간
    t1, t2 = 2 / (1 + b), 2 / (1 - b)
    fs.label(ax, (0.7, -0.75), '(나) 지면 기준틀 $S$: 기차가 $\\vec v$로 움직인다', fontsize=9)
    for k, (t, y) in enumerate(((t1, -1.95), (t2, -3.75))):
        car(ax, -2 + b * t, y, alpha=1.0)
        ax.plot([0, 0], [y - 0.75, y + 1.0], ls=':', color=fs.GRAY, lw=0.8)
        fs.dot(ax, (0, y + 0.4), r=0.05, color=fs.ORANGE)
        for s in (-1, 1):
            fs.arrow(ax, (0.12 * s, y + 0.4), (t * s, y + 0.4), color=LIGHT_C, lw=1.6, ms=9)
        hit = -t if k == 0 else t
        ax.add_patch(Circle((hit, y + 0.4), 0.13, fc='none', ec=fs.FORCE, lw=1.4, zorder=9))
        fs.vec(ax, (-2 + b * t + 4.15, y + 0.4), (0.55, 0), color=fs.VEL, lw=1.8, label=r'$\vec v$', loff=(0.15, 0.25))
        txt = '뒷벽에 먼저 도착' if k == 0 else '나중에 앞벽에 도착'
        fs.label(ax, (hit, y - 0.48), txt, fontsize=8.5, color=fs.FORCE)
    fs.label(ax, (0.0, -4.62), '섬광이 터진 자리', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig35_02')


# ---------------------------------------------------------------- 35.3 빛 시계
def mirror(ax, x, y, w=0.7):
    ax.add_patch(Rectangle((x - w / 2, y - 0.05), w, 0.1, fc='#b0bec5', ec=fs.BLACK, lw=0.8, zorder=3))


def fig03():
    fig, ax = fs.canvas(5.2, 2.8, xlim=(-1.2, 6.6), ylim=(-1.15, 2.0))
    D = 1.6
    # (가)
    mirror(ax, 0, 0); mirror(ax, 0, D)
    fs.arrow(ax, (-0.1, 0.07), (-0.1, D - 0.07), color=LIGHT_C, lw=1.5, ms=9)
    fs.arrow(ax, (0.1, D - 0.07), (0.1, 0.07), color=LIGHT_C, lw=1.5, ms=9)
    fs.dim(ax, (-0.35, 0), (-0.35, D), r'$D$', off=0.3)
    fs.label(ax, (0, -0.35), r"$\Delta t_0 = 2D/c$", fontsize=9.5)
    fs.label(ax, (0, -0.95), "(가) $S'$: 시계와 함께", fontsize=9)
    # (나) beta = 0.6
    b = 0.6
    half = D * b / np.sqrt(1 - b ** 2)  # v dt/2
    x0 = 1.9
    for k in range(3):
        xx = x0 + k * half
        mirror(ax, xx, 0, w=0.6)
        mirror(ax, xx, D, w=0.6)
    ax.plot([x0, x0 + half, x0 + 2 * half], [0.05, D - 0.05, 0.05], color=LIGHT_C, lw=1.5)
    fs.arrow(ax, (x0, 0.05), (x0 + 0.55 * half, 0.05 + 0.55 * (D - 0.1)), color=LIGHT_C, lw=0, ms=10)
    fs.arrow(ax, (x0 + half, D - 0.05), (x0 + 1.55 * half, D - 0.05 - 0.55 * (D - 0.1)), color=LIGHT_C, lw=0, ms=10)
    ax.plot([x0 + half, x0 + half], [0, D], ls='--', color=fs.GRAY, lw=0.9)
    fs.label(ax, (x0 + half + 0.2, D / 2 - 0.15), r'$D$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (x0 + 0.25 * half - 0.38, D / 2 + 0.25), r'$\frac{c\Delta t}{2}$', fontsize=12, color=LIGHT_C)
    hdim(ax, x0, x0 + half, -0.25, r'$v\Delta t/2$', ty=-0.5)
    fs.vec(ax, (x0 + 2 * half + 0.45, D / 2), (0.6, 0), color=fs.VEL, lw=1.8, label=r'$\vec v$', loff=(0.15, 0.22))
    fs.label(ax, (x0 + half, -0.95), "(나) $S$: 시계가 $v$로 움직임", fontsize=9)
    fs.save(fig, __file__, 'fig35_03')


# ---------------------------------------------------------------- gamma 그래프
def fig04():
    fig, ax = fs.plot_axes(4.2, 2.8)
    b = np.linspace(0, 0.995, 800)
    ax.plot(b, gam(b), color=fs.VEL, lw=1.8, label=r'$\gamma = 1/\sqrt{1-\beta^2}$')
    ax.plot(b, 1 + b ** 2 / 2, color=fs.GRAY, ls='--', lw=1.2, label=r'$1 + \beta^2/2$ (저속 근사)')
    ax.axvline(1, color=fs.FORCE, ls=':', lw=1)
    for bb, txt, dx, dy in ((0.6, '1.25', -0.08, 0.6), (0.8, '5/3', -0.08, 0.7), (0.95, '3.20', -0.1, 0.5), (0.99, '7.09', -0.11, 0.0)):
        g = gam(bb)
        ax.plot(bb, g, 'o', color=fs.FORCE, ms=4)
        ax.text(bb + dx, g + dy, txt, fontsize=9, ha='right', color=fs.FORCE)
    ax.set_xlim(0, 1.03); ax.set_ylim(0, 8)
    ax.set_xlabel(r'$\beta = v/c$'); ax.set_ylabel(r'$\gamma$')
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    fs.save(fig, __file__, 'fig35_04')


# ---------------------------------------------------------------- 쌍둥이 역설 시공간 도형
def fig05():
    fig, ax = plt.subplots(figsize=(4.2, 3.5))
    ax.set_aspect('equal')
    b = 0.6; g = gam(b)
    ax.plot([0, 0], [0, 10], color=fs.BLACK, lw=2)
    ax.plot([0, 3, 0], [0, 5, 10], color=fs.VEL, lw=2)
    for t in range(1, 10):
        ax.plot([-0.12, 0.12], [t, t], color=fs.BLACK, lw=1)
    # 여행자의 고유 시간 1년마다 눈금
    for k in range(1, 8):
        t = g * k if k <= 4 else 5 + g * (k - 4)
        x = b * t if k <= 4 else 3 - b * (t - 5)
        ax.plot(x, t, 'o', color=fs.VEL, ms=3.5)
    # 동시선
    xs = np.linspace(0, 3, 10)
    ax.plot(xs, 5 + b * (xs - 3), color=fs.FORCE, ls='--', lw=1)
    ax.plot(xs, 5 - b * (xs - 3), color=fs.ACC, ls='--', lw=1)
    ax.annotate('', xy=(0.05, 6.8), xytext=(0.05, 3.2),
                arrowprops=dict(arrowstyle='->', color=fs.ORANGE, lw=1.3))
    ax.text(-0.25, 3.2, '3.2', fontsize=9, ha='right', va='center', color=fs.FORCE)
    ax.text(-0.25, 6.8, '6.8', fontsize=9, ha='right', va='center', color=fs.ACC)
    ax.text(3.15, 5.0, '방향 전환', fontsize=8.5, va='center')
    ax.text(2.0, 1.0, '여행자(갈 때)\n$v = 0.6c$', fontsize=8.5, color=fs.VEL)
    ax.text(1.9, 8.3, '여행자(올 때)\n$v = 0.6c$', fontsize=8.5, color=fs.VEL)
    ax.text(-0.2, 9.0, '지구', fontsize=9, ha='right')
    ax.plot([0, 5.2], [0, 5.2], ls=':', color=LIGHT_C, lw=1)
    ax.text(4.9, 4.2, '빛', fontsize=8.5, color=LIGHT_C)
    ax.set_xlim(-1.0, 5.3); ax.set_ylim(0, 10.3)
    ax.set_xlabel('$x$ (광년)'); ax.set_ylabel('$ct$ (년)')
    ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_yticks(range(0, 11, 2))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fs.save(fig, __file__, 'fig35_05')


# ---------------------------------------------------------------- 길이 수축(예제 35.2)
def ship(ax, x0, y0, L, h=0.45, color=fs.LIGHT):
    pts = [(x0, y0), (x0 + L * 0.85, y0), (x0 + L, y0 + h / 2), (x0 + L * 0.85, y0 + h), (x0, y0 + h)]
    ax.add_patch(Polygon(pts, fc=color, ec=fs.BLACK, lw=1.1, zorder=3))


def satellite(ax, p):
    ax.add_patch(Rectangle((p[0] - 0.12, p[1] - 0.12), 0.24, 0.24, fc='#95a5a6', ec=fs.BLACK, lw=0.8, zorder=4))
    for s in (-1, 1):
        ax.add_patch(Rectangle((p[0] + s * 0.17 - (0.25 if s < 0 else 0), p[1] - 0.05), 0.25, 0.1, fc=fs.VEL, ec=fs.BLACK, lw=0.5, zorder=4))


def fig06():
    fig, ax = fs.canvas(5.0, 2.7, xlim=(-0.6, 6.6), ylim=(-1.7, 2.1))
    sc = 0.05  # 1 m = 0.05 단위
    # (가) 우주선 기준
    y = 1.0
    ship(ax, 0.5, y, 100 * sc)
    fs.dim(ax, (0.5, y + 0.45), (0.5 + 100 * sc, y + 0.45), r'$L_0 = 100\ \mathrm{m}$', off=0.25, fontsize=9)
    satellite(ax, (6.0, y + 0.22))
    fs.vec(ax, (6.0, y - 0.15), (-0.7, 0), color=fs.VEL, lw=1.6, label=r'$0.80c$', loff=(0.0, -0.22), fontsize=9)
    fs.label(ax, (3.0, y - 0.62), '(가) 우주선 기준: 위성이 지나가는 데 $417\\ \\mathrm{ns}$', fontsize=8.5)
    # (나) 위성 기준
    y = -1.0
    ship(ax, 0.5, y, 60 * sc)
    fs.dim(ax, (0.5, y + 0.45), (0.5 + 60 * sc, y + 0.45), r'$L = 60\ \mathrm{m}$', off=0.25, fontsize=9)
    fs.vec(ax, (3.75, y + 0.22), (0.7, 0), color=fs.VEL, lw=1.6, label=r'$0.80c$', loff=(0.0, 0.22), fontsize=9)
    satellite(ax, (6.0, y + 0.22))
    fs.label(ax, (3.0, y - 0.62), '(나) 위성 기준: 우주선이 지나가는 데 $250\\ \\mathrm{ns}$ (고유 시간)', fontsize=8.5)
    fs.save(fig, __file__, 'fig35_06')


# ---------------------------------------------------------------- 민코프스키 도형(예제 35.3)
def fig07():
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    ax.set_aspect('equal'); ax.axis('off')
    b = 0.6; g = gam(b)
    X0, X1, T0, T1 = -2.6, 4.6, -3.4, 3.2
    fs.arrow(ax, (X0, 0), (X1, 0), lw=1.1, ms=9); fs.arrow(ax, (0, T0), (0, T1), lw=1.1, ms=9)
    ax.text(X1, -0.35, '$x$ (km)', fontsize=10, ha='right')
    ax.text(0.12, T1, '$ct$ (km)', fontsize=10, va='top')
    # S' 축
    tt = np.array([T0, T1 - 0.3])
    ax.plot(b * tt, tt, color=fs.VEL, lw=1.3)
    ax.text(b * (T1 - 0.3) + 0.1, T1 - 0.3, "$ct'$", color=fs.VEL, fontsize=11)
    xx = np.array([X0, X1 - 0.2])
    ax.plot(xx, b * xx, color=fs.VEL, lw=1.3)
    ax.text(X1 - 0.2, b * (X1 - 0.2) + 0.15, "$x'$", color=fs.VEL, fontsize=11, ha='right')
    # 빛
    for s in (1, -1):
        ax.plot([-2.6, 2.6], [-2.6 * s, 2.6 * s], ls=':', color=LIGHT_C, lw=1)
    ax.text(2.45, 2.0, '빛', color=LIGHT_C, fontsize=8.5)
    # B를 지나는 S'의 동시선
    xs = np.linspace(-2.2, 4.4, 10)
    ax.plot(xs, b * (xs - 3), color=fs.FORCE, ls='--', lw=1.1)
    tc = -1.8 / (1 - b ** 2)
    ax.plot(b * tc, tc, 'o', color=fs.FORCE, ms=4)
    ax.text(b * tc + 0.4, tc - 0.05, "$ct' = -2.25$ km\n$(\\Delta t' = -7.5\\ \\mu\\mathrm{s})$", color=fs.FORCE, fontsize=8.5, va='top')
    for p, name in (((0, 0), 'A'), ((3, 0), 'B')):
        ax.add_patch(Circle(p, 0.11, color=fs.BLACK, zorder=6))
    ax.text(-0.35, 0.18, 'A', fontsize=10, fontweight='bold')
    ax.text(3.0, 0.25, 'B', fontsize=10, fontweight='bold', ha='center')
    ax.text(3.0, -0.38, '3.0', fontsize=8.5, ha='center')
    ax.text(4.6, 1.15, "B를 지나는\n$S'$의 동시선", fontsize=8, color=fs.FORCE, ha='right', va='bottom')
    ax.set_xlim(X0 - 0.2, X1 + 0.1); ax.set_ylim(T0 - 0.2, T1 + 0.1)
    fs.save(fig, __file__, 'fig35_07')


# ---------------------------------------------------------------- 빛원뿔과 불변 쌍곡선
def fig08():
    fig, ax = plt.subplots(figsize=(4.3, 3.1))
    ax.set_aspect('equal'); ax.axis('off')
    R = 7.5
    ax.fill([0, -R, R], [0, R, R], color='#fdebd0', zorder=0)
    ax.fill([0, -2.7, 2.7], [0, -2.7, -2.7], color='#fdebd0', zorder=0)
    fs.arrow(ax, (-R, 0), (R + 0.3, 0), lw=1.0, ms=9); fs.arrow(ax, (0, -2.7), (0, R + 0.3), lw=1.0, ms=9)
    ax.text(R + 0.3, -0.55, '$x$ (m)', ha='right', fontsize=9.5); ax.text(0.2, R + 0.3, '$ct$ (m)', fontsize=9.5, va='top')
    for s_ in (1, -1):
        ax.plot([-2.7 * s_, R * s_], [-2.7, R], color=LIGHT_C, lw=1.2)
    xs = np.linspace(-5.6, 5.6, 300)
    ax.plot(xs, np.sqrt(16 + xs ** 2), color=fs.VEL, lw=1.6)
    ts = np.linspace(-2.6, 5.0, 100)
    ax.plot(np.sqrt(9 + ts ** 2), ts, color=fs.FIELD, lw=1.1, ls='--')
    pts = [((3, 5), r"$S$", (3.25, 4.55), 'left'),
           ((0, 4), r"$\beta=0.6$", (0.15, 3.45), 'left'),
           ((1.048 * (3 - 1.5), 1.048 * (5 - 0.9)), r"$\beta=0.3$", (1.75, 3.95), 'left'),
           ((gam(0.9) * (3 - 4.5), gam(0.9) * (5 - 2.7)), r"$\beta=0.9$", (-3.65, 4.85), 'right')]
    for (p, txt, q, ha) in pts:
        ax.plot(*p, 'o', color=fs.FORCE, ms=4.5, zorder=6)
        ax.text(q[0], q[1], txt, fontsize=8, ha=ha, va='center', color=fs.FORCE)
    ax.text(-1.4, 6.6, '시간꼴(미래)', fontsize=8.5, ha='right')
    ax.text(-6.6, 1.4, '공간꼴', fontsize=8.5)
    ax.text(5.0, 1.4, '공간꼴', fontsize=8.5)
    ax.text(0.3, -2.0, '시간꼴(과거)', fontsize=8.5)
    ax.text(6.0, 5.0, '빛꼴', fontsize=8.5, color=LIGHT_C, ha='left')
    ax.text(1.0, 6.6, r'$(\Delta s)^2 = 16\ \mathrm{m}^2$', fontsize=8.5, color=fs.VEL)
    ax.text(3.95, -2.15, r'$(\Delta s)^2 = -9\ \mathrm{m}^2$', fontsize=8, color=fs.FIELD)
    ax.set_xlim(-R - 0.1, R + 0.4); ax.set_ylim(-2.8, R + 0.4)
    fs.save(fig, __file__, 'fig35_08')


# ---------------------------------------------------------------- 운동량·운동에너지 비교
def fig09():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.6))
    for ax in axs:
        ax.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    b = np.linspace(0, 0.995, 600)
    ax = axs[0]
    ax.plot(b, gam(b) * b, color=fs.VEL, lw=1.8, label=r'$\gamma\beta$ (상대론)')
    ax.plot(b, b, color=fs.GRAY, ls='--', lw=1.3, label=r'$\beta$ (뉴턴)')
    ax.axvline(1, color=fs.FORCE, ls=':', lw=1)
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 5)
    ax.set_xlabel(r'$\beta$'); ax.set_ylabel(r'$p/mc$')
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    ax.set_title('(가) 운동량', fontsize=9.5)
    ax = axs[1]
    K = 1.00 / 0.511
    b2 = np.linspace(0, 2.1, 400)
    ax.axvspan(1, 2.15, color='#f2f2f2')
    ax.plot(b, gam(b) - 1, color=fs.VEL, lw=1.8, label=r'$\gamma - 1$')
    ax.plot(b2, b2 ** 2 / 2, color=fs.GRAY, ls='--', lw=1.3, label=r'$\beta^2/2$')
    ax.axhline(K, color=fs.ORANGE, lw=1)
    bb = np.sqrt(1 - 1 / (1 + K) ** 2)
    ax.plot([bb], [K], 'o', color=fs.VEL, ms=4.5); ax.plot([np.sqrt(2 * K)], [K], 'o', color=fs.GRAY, ms=4.5)
    ax.text(bb + 0.06, K - 0.28, '0.941', fontsize=8.5, color=fs.VEL, ha='left')
    ax.text(np.sqrt(2 * K) - 0.05, K + 0.15, '1.98', fontsize=8.5, color=fs.GRAY, ha='right')
    ax.text(0.03, K + 0.08, r'$K = 1.00$ MeV', fontsize=8, color=fs.ORANGE, va='bottom')
    ax.text(1.55, 3.2, '$v > c$\n불가능', fontsize=8, ha='center', color=fs.GRAY)
    ax.set_xlim(0, 2.1); ax.set_ylim(0, 4)
    ax.set_xlabel(r'$\beta$'); ax.set_ylabel(r'$K/mc^2$')
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    ax.set_title('(나) 운동에너지', fontsize=9.5)
    fig.tight_layout(w_pad=1.2)
    fs.save(fig, __file__, 'fig35_09')


# ---------------------------------------------------------------- 에너지-운동량 삼각형
def fig10():
    fig, ax = fs.canvas(3.6, 2.0, xlim=(-0.4, 3.4), ylim=(-0.45, 1.3))
    s = 2.0  # 1 MeV = 2 단위
    pc, mc2 = 1.42 * s, 0.511 * s
    ax.add_patch(Polygon([(0, 0), (pc, 0), (pc, mc2)], fc='#eef3f9', ec='none'))
    fs.arrow(ax, (0, 0), (pc, 0), color=fs.VEL, lw=1.8, ms=10)
    fs.arrow(ax, (pc, 0), (pc, mc2), color=fs.GRAY, lw=1.8, ms=10)
    fs.arrow(ax, (0, 0), (pc, mc2), color=fs.FORCE, lw=2, ms=11)
    ax.add_patch(Rectangle((pc - 0.12, 0), 0.12, 0.12, fc='none', ec=fs.BLACK, lw=0.7))
    fs.label(ax, (pc / 2, -0.25), r'$pc = 1.42$ MeV', fontsize=9.5, color=fs.VEL)
    fs.label(ax, (pc + 0.12, mc2 / 2), r'$mc^2 = 0.511$ MeV', fontsize=9.5, color=fs.GRAY, ha='left')
    fs.label(ax, (pc / 2 - 0.35, mc2 / 2 + 0.25), r'$E = 1.511$ MeV', fontsize=9.5, color=fs.FORCE)
    fs.save(fig, __file__, 'fig35_10')


# ---------------------------------------------------------------- 파이온 붕괴
def particle(ax, p, name, color, r=0.22):
    ax.add_patch(Circle(p, r, fc=color, ec=fs.BLACK, lw=0.8, zorder=5))
    ax.text(p[0], p[1], name, ha='center', va='center', fontsize=10, color='white', zorder=6)


def fig11():
    fig, ax = fs.canvas(5.0, 1.5, xlim=(-0.6, 8.6), ylim=(-0.9, 1.0))
    particle(ax, (0.3, 0), r'$\pi^+$', fs.FIELD, r=0.3)
    fs.label(ax, (0.3, -0.6), '붕괴 전 (정지)', fontsize=8.5)
    fs.arrow(ax, (1.0, 0), (1.9, 0), color=fs.BLACK, lw=1.2, ms=10)
    c = (5.4, 0)
    ax.add_patch(Circle(c, 0.05, color=fs.GRAY))
    particle(ax, (c[0] + 1.9, 0), r'$\mu^+$', fs.FORCE)
    particle(ax, (c[0] - 1.9, 0), r'$\nu_\mu$', fs.ACC, r=0.2)
    fs.arrow(ax, (c[0] + 0.15, 0), (c[0] + 1.6, 0), color=fs.VEL, lw=1.8, ms=10)
    fs.arrow(ax, (c[0] - 0.15, 0), (c[0] - 1.6, 0), color=fs.VEL, lw=1.8, ms=10)
    fs.label(ax, (c[0] + 0.9, 0.35), r'$p$', color=fs.VEL); fs.label(ax, (c[0] - 0.9, 0.35), r'$p$', color=fs.VEL)
    fs.label(ax, (c[0], -0.6), r'붕괴 후: $pc = 29.79$ MeV, $K_\mu = 4.12$ MeV', fontsize=8.5)
    fs.save(fig, __file__, 'fig35_11')


# ---------------------------------------------------------------- 연습문제 15: 고정 표적과 충돌형
def fig12():
    fig, ax = fs.canvas(5.0, 1.9, xlim=(-0.3, 9.3), ylim=(-1.4, 1.3))
    particle(ax, (0.4, 0.5), '$p$', fs.FORCE, r=0.2)
    fs.vec(ax, (0.7, 0.5), (1.4, 0), color=fs.VEL, lw=1.8, label=r'$K$', loff=(-0.7, 0.3))
    particle(ax, (3.2, 0.5), '$p$', fs.FORCE, r=0.2)
    fs.label(ax, (3.2, 0.05), '정지', fontsize=8.5)
    fs.label(ax, (1.8, -0.6), '(가) 고정 표적', fontsize=9)
    particle(ax, (5.3, 0.5), '$p$', fs.FORCE, r=0.2)
    particle(ax, (8.7, 0.5), '$p$', fs.FORCE, r=0.2)
    fs.vec(ax, (5.6, 0.5), (1.0, 0), color=fs.VEL, lw=1.8, label=r'$K$', loff=(-0.5, 0.3))
    fs.vec(ax, (8.4, 0.5), (-1.0, 0), color=fs.VEL, lw=1.8, label=r'$K$', loff=(0.5, 0.3))
    fs.label(ax, (7.0, -0.6), '(나) 충돌형 (정면 충돌)', fontsize=9)
    fs.label(ax, (4.5, -1.15), r'두 경우 모두 $p + p \to p + p + p + \bar p$', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig35_12')


# ---------------------------------------------------------------- 연습문제 16: 중성 파이온 붕괴
def fig13():
    fig, ax = fs.canvas(3.8, 2.0, xlim=(-0.5, 4.6), ylim=(-1.35, 1.35))
    particle(ax, (0.2, 0), r'$\pi^0$', fs.FIELD, r=0.28)
    fs.vec(ax, (0.55, 0), (0.8, 0), color=fs.VEL, lw=1.8, label=r'$E$', loff=(-0.4, 0.25))
    o = (2.2, 0)
    ax.add_patch(Circle(o, 0.05, color=fs.GRAY))
    a1, a2 = np.radians(28), np.radians(-20)
    for a, nm in ((a1, r'$E_1$'), (a2, r'$E_2$')):
        p = (o[0] + 2.0 * np.cos(a), o[1] + 2.0 * np.sin(a))
        fs.ray(ax, [o, p], color=LIGHT_C, lw=1.5)
        ax.text(p[0] + 0.1, p[1], r'$\gamma$, ' + nm, fontsize=10, color=fs.ORANGE, va='center')
    fs.angle_arc(ax, o, 0.9, np.degrees(a2), np.degrees(a1), r'$\theta$', fontsize=11, tr=1.15)
    ax.plot([o[0], o[0] + 1.2], [0, 0], ls=':', color=fs.GRAY, lw=0.8)
    fs.save(fig, __file__, 'fig35_13')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
        f()
