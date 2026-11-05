"""1장 물리학을 위한 수학 도구 — 그림 생성 스크립트.

    python3 figures/ch01/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Arc

S = __file__


# ---------- 이 장 전용 도우미 ----------
def axes2d(ax, x0, x1, y0, y1, xl='$x$', yl='$y$', color=fs.GRAY, fontsize=11, origin=(0, 0)):
    """원점을 지나는 좌표축(화살표)."""
    ox, oy = origin
    fs.arrow(ax, (x0, oy), (x1, oy), color=color, lw=0.9, ms=9, zorder=1)
    fs.arrow(ax, (ox, y0), (ox, y1), color=color, lw=0.9, ms=9, zorder=1)
    ax.text(x1, oy - 0.08, xl, ha='right', va='top', fontsize=fontsize, color=color)
    ax.text(ox - 0.08, y1, yl, ha='right', va='top', fontsize=fontsize, color=color)


def schematic_axes(ax, xl, yl):
    """눈금 없는 그래프 축."""
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(xl); ax.set_ylabel(yl, rotation=0, labelpad=10)
    ax.plot(1, 0, '>k', transform=ax.get_yaxis_transform(), clip_on=False, ms=4)
    ax.plot(0, 1, '^k', transform=ax.get_xaxis_transform(), clip_on=False, ms=4)


# 비스듬한 투영(3차원 → 종이): x는 왼쪽 아래(앞쪽), y는 오른쪽, z는 위
EX = np.array([-0.50, -0.36]); EY = np.array([1.0, 0.0]); EZ = np.array([0.0, 1.0])


def P(x, y, z):
    return x * EX + y * EY + z * EZ


# ---------- 그림 1.1 벡터의 성분 ----------
def fig01():
    fig, ax = fs.canvas(3.6, 2.6, xlim=(-0.6, 4.6), ylim=(-0.65, 3.1))
    axes2d(ax, -0.4, 4.5, -0.4, 3.0)
    A = np.array([3.4, 2.2])
    ax.plot([A[0], A[0]], [0, A[1]], ls='--', color=fs.GRAY, lw=0.8)
    ax.plot([0, A[0]], [A[1], A[1]], ls='--', color=fs.GRAY, lw=0.8)
    fs.arrow(ax, (0, 0), (A[0], 0), color=fs.VEL, lw=1.3, ms=10)
    fs.arrow(ax, (0, 0), (0, A[1]), color=fs.VEL, lw=1.3, ms=10)
    fs.arrow(ax, (0, 0), A, color=fs.BLACK, lw=1.8)
    ax.text(1.55, 1.35, r'$\vec{A}$', fontsize=13, ha='center')
    ax.text(A[0] / 2, -0.28, r'$A_x = A\cos\theta$', color=fs.VEL, fontsize=10, ha='center', va='top')
    ax.text(-0.12, A[1] / 2, r'$A_y = A\sin\theta$', color=fs.VEL, fontsize=10, ha='right', va='center')
    fs.angle_arc(ax, (0, 0), 0.8, 0, np.degrees(np.arctan2(A[1], A[0])), r'$\theta$', tr=1.05)
    ax.text(A[0] + 0.1, A[1] + 0.1, r'$(A_x, A_y)$', fontsize=10, ha='left', va='bottom')
    fs.save(fig, S, 'fig01_01')


# ---------- 그림 1.2 arctan의 함정 ----------
def fig02():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-4.6, 4.2), ylim=(-4.6, 4.9))
    axes2d(ax, -4.2, 4.2, -4.4, 4.8)
    for v in (-3, -2, -1, 1, 2, 3):
        ax.plot([v, v], [-0.07, 0.07], color=fs.GRAY, lw=0.7)
        ax.plot([-0.07, 0.07], [v, v], color=fs.GRAY, lw=0.7)
    for v in (-3, 3):
        ax.text(v, -0.2, f'{v}'.replace('-', '−'), fontsize=8, ha='center', va='top', color=fs.GRAY)
    ax.text(0.15, 4, '4', fontsize=8, ha='left', va='center', color=fs.GRAY)
    ax.text(0.15, -4, '−4', fontsize=8, ha='left', va='center', color=fs.GRAY)
    ax.plot([-3, -3], [0, 4], ls='--', color=fs.GRAY, lw=0.7)
    ax.plot([-3, 0], [4, 4], ls='--', color=fs.GRAY, lw=0.7)
    fs.arrow(ax, (0, 0), (-3, 4), color=fs.BLACK, lw=1.8)
    ax.text(-2.0, 1.95, r'$\vec{A} = -3\hat{i} + 4\hat{j}$', fontsize=10, ha='right', va='center')
    fs.angle_arc(ax, (0, 0), 1.0, 0, 126.87, r'$126.9^\circ$', tr=1.75)
    # 잘못된 답
    fs.arrow(ax, (0, 0), (3, -4), color=fs.FORCE, lw=1.2, ls='--', ms=10)
    fs.angle_arc(ax, (0, 0), 1.3, -53.13, 0, None, color=fs.FORCE)
    ax.text(1.55, -1.2, r'$-53.1^\circ$', fontsize=10, color=fs.FORCE, ha='left')
    ax.text(1.5, -2.7, r'$\tan^{-1}(-4/3)$가' + '\n가리키는 방향(틀림)', fontsize=8.5, color=fs.FORCE,
            ha='right', va='center')
    fs.save(fig, S, 'fig01_02')


# ---------- 그림 1.3 예제 1.1 변위의 합 ----------
def fig03():
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-3.9, 3.2), ylim=(-0.75, 3.1))
    axes2d(ax, -3.7, 3.0, -0.5, 3.0, xl='동 ($+x$)', yl='북 ($+y$)', fontsize=9)
    d1 = np.array([3 * np.cos(np.pi / 4), 3 * np.sin(np.pi / 4)])
    d = d1 + np.array([-5.0, 0])
    fs.arrow(ax, (0, 0), d1, color=fs.BLACK, lw=1.7)
    fs.arrow(ax, d1, d, color=fs.BLACK, lw=1.7)
    fs.arrow(ax, (0, 0), d, color=fs.ORANGE, lw=2.0)
    ax.text(1.25, 0.72, r'$\vec{d}_1$ (3.0 km)', fontsize=10, ha='left', va='top')
    ax.text(-1.4, d1[1] + 0.12, r'$\vec{d}_2$ (5.0 km, 서쪽)', fontsize=10, ha='center', va='bottom')
    ax.text(-1.6, 1.3, r'$\vec{d}$ (3.58 km)', fontsize=10, color=fs.ORANGE, ha='right', va='bottom')
    fs.angle_arc(ax, (0, 0), 0.6, 0, 45, r'$45^\circ$', tr=0.9)
    fs.angle_arc(ax, (0, 0), 1.0, 180 - 36.36, 180, r'$36.4^\circ$', color=fs.ORANGE, tr=1.42)
    ax.text(-3.75, -0.12, '서', fontsize=9, color=fs.GRAY, ha='left', va='top')
    fs.dot(ax, (0, 0), r=0.05)
    ax.text(0.08, -0.12, '출발점', fontsize=8.5, ha='left', va='top')
    fs.save(fig, S, 'fig01_03')


# ---------- 그림 1.4 내적과 사영 ----------
def fig04():
    fig, ax = fs.canvas(3.6, 2.0, xlim=(-0.3, 4.6), ylim=(-0.7, 2.1))
    phi = np.radians(38)
    B = np.array([4.3, 0.0]); A = 2.6 * np.array([np.cos(phi), np.sin(phi)])
    fs.arrow(ax, (0, 0), B, color=fs.BLACK, lw=1.7)
    fs.arrow(ax, (0, 0), A, color=fs.VEL, lw=1.7)
    ax.plot([A[0], A[0]], [A[1], 0], ls='--', color=fs.GRAY, lw=0.8)
    s = 0.13
    ax.plot([A[0] - s, A[0] - s, A[0]], [0, s, s], color=fs.GRAY, lw=0.7)
    ax.plot([0, A[0]], [-0.0, -0.0], color=fs.ORANGE, lw=3.2, solid_capstyle='butt', zorder=4)
    ax.text(A[0] / 2, -0.12, r'$A\cos\phi$', color=fs.ORANGE, fontsize=11, ha='center', va='top')
    ax.text(B[0], -0.12, r'$\vec{B}$', fontsize=12, ha='center', va='top')
    ax.text(A[0] / 2 - 0.15, A[1] / 2 + 0.15, r'$\vec{A}$', color=fs.VEL, fontsize=12, ha='right')
    fs.angle_arc(ax, (0, 0), 0.7, 0, 38, r'$\phi$', tr=0.95)
    ax.text(2.6, 1.75, r'$\vec{A}\cdot\vec{B} = (A\cos\phi)\,B$', fontsize=10.5, ha='left')
    fs.save(fig, S, 'fig01_04')


# ---------- 그림 1.5 외적 ----------
def fig05():
    fig, ax = fs.canvas(3.6, 3.2, xlim=(-1.3, 3.8), ylim=(-1.9, 2.4))
    phi = np.radians(60)
    Ain = np.array([2.1, 0.0]); Bin = 1.6 * np.array([np.cos(phi), np.sin(phi)])  # 평면(u, v) 성분

    def pl(u, v, z=0.0):
        return u * EY + v * np.array([0.45, 0.55]) + z * EZ

    O = pl(0, 0); A = pl(*Ain); B = pl(*Bin); AB = pl(*(Ain + Bin))
    ax.add_patch(Polygon([O, A, AB, B], closed=True, fc=fs.SURF, alpha=0.45, ec=fs.GRAY, lw=0.6, ls='--', zorder=1))
    fs.arrow(ax, O, A, color=fs.VEL, lw=1.7)
    fs.arrow(ax, O, B, color=fs.FORCE, lw=1.7)
    ax.text(A[0] + 0.08, A[1] - 0.1, r'$\vec{A}$', color=fs.VEL, fontsize=12, ha='left', va='top')
    ax.text(B[0] - 0.05, B[1] + 0.12, r'$\vec{B}$', color=fs.FORCE, fontsize=12, ha='right', va='bottom')
    th = np.linspace(0, phi, 40)
    arc = np.array([pl(0.5 * np.cos(t), 0.5 * np.sin(t)) for t in th])
    ax.plot(arc[:, 0], arc[:, 1], color=fs.BLACK, lw=0.9)
    m = pl(0.72 * np.cos(phi / 2), 0.72 * np.sin(phi / 2))
    ax.text(m[0], m[1], r'$\phi$', fontsize=10, ha='center', va='center')
    C = 1.9
    fs.arrow(ax, O, pl(0, 0, C), color=fs.BLACK, lw=1.9)
    ax.text(0.1, C, r'$\vec{C} = \vec{A}\times\vec{B}$', fontsize=11, ha='left', va='center')
    fs.arrow(ax, O, pl(0, 0, -1.6), color=fs.GRAY, lw=1.3, ls='--')
    ax.text(0.1, -1.6, r'$\vec{B}\times\vec{A} = -\vec{C}$', fontsize=10, color=fs.GRAY, ha='left', va='center')
    c = pl(*(0.5 * (Ain + Bin)))
    ax.text(c[0] + 0.55, c[1] - 0.05, '넓이\n' + r'$AB\sin\phi$', fontsize=9, ha='center', va='center')
    ax.plot([0, 0.15, 0.15], [0.15, 0.15, 0], color=fs.BLACK, lw=0.7)
    fs.save(fig, S, 'fig01_05')


# ---------- 그림 1.6 예제 1.3 렌치의 토크 ----------
def fig06():
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-0.8, 4.6), ylim=(-0.9, 2.6))
    # 렌치 몸통
    ax.add_patch(Polygon([(0, -0.13), (3.0, -0.10), (3.0, 0.10), (0, 0.13)], closed=True,
                         fc='#dfe6ee', ec=fs.BLACK, lw=1.1, zorder=2))
    ax.add_patch(Circle((0, 0), 0.33, fc='#dfe6ee', ec=fs.BLACK, lw=1.1, zorder=2))
    hexa = np.array([[0.17 * np.cos(a), 0.17 * np.sin(a)] for a in np.radians(np.arange(0, 360, 60) + 30)])
    ax.add_patch(Polygon(hexa, closed=True, fc='white', ec=fs.BLACK, lw=0.9, zorder=3))
    # r 벡터
    fs.arrow(ax, (0, -0.55), (3.0, -0.55), color=fs.BLACK, lw=1.1, ms=9)
    ax.text(1.5, -0.65, r'$\vec{r} = 0.30\,\hat{i}\ \mathrm{m}$', fontsize=10, ha='center', va='top')
    # 힘
    E = np.array([3.0, 0.0]); k = 1 / 25.0
    F = np.array([20, 40]) * k * 1.0
    fs.arrow(ax, E, E + F, color=fs.FORCE, lw=2.0)
    fs.arrow(ax, E, E + np.array([F[0], 0]), color=fs.FORCE, lw=1.0, ls='--', ms=9)
    fs.arrow(ax, E, E + np.array([0, F[1]]), color=fs.FORCE, lw=1.0, ls='--', ms=9)
    ax.text(E[0] + F[0] + 0.1, E[1] + F[1], r'$\vec{F}$', color=fs.FORCE, fontsize=12, ha='left', va='center')
    ax.text(E[0] + F[0] + 0.05, -0.2, r'$F_x = 20\ \mathrm{N}$', color=fs.FORCE, fontsize=9, ha='left', va='top')
    ax.text(E[0] - 0.08, F[1] * 0.6, r'$F_y = 40\ \mathrm{N}$', color=fs.FORCE, fontsize=9, ha='right')
    # 토크 방향(반시계)
    ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=20, theta2=160, color=fs.BLACK, lw=1.0))
    a = np.radians(160)
    ax.add_patch(FancyArrowPatch((0.65 * np.cos(a - 0.15), 0.65 * np.sin(a - 0.15)),
                                 (0.65 * np.cos(a + 0.05), 0.65 * np.sin(a + 0.05)),
                                 arrowstyle='-|>', mutation_scale=10, color=fs.BLACK, lw=1.0))
    ax.text(-0.1, 0.95, r'$\vec{\tau} = 12\,\hat{k}\ \mathrm{N\cdot m}$', fontsize=10, ha='center', va='bottom')
    ax.text(-0.45, -0.32, '축', fontsize=9, ha='right', va='center')
    fs.save(fig, S, 'fig01_06')


# ---------- 그림 1.7 미분: 할선과 접선 ----------
def fig07():
    fig, ax = fs.plot_axes(3.8, 2.6)
    ax.grid(False)
    f = lambda t: 0.4 + 0.25 * t ** 2 - 0.02 * t ** 3
    t = np.linspace(0, 5.6, 200)
    ax.plot(t, f(t), color=fs.BLACK, lw=1.5)
    t0, dt = 1.8, 2.2
    x0, x1 = f(t0), f(t0 + dt)
    df = 0.5 * t0 - 0.06 * t0 ** 2
    tt = np.linspace(0.6, 4.6, 2)
    ax.plot(tt, x0 + df * (tt - t0), color=fs.VEL, lw=1.3)
    ts = np.linspace(1.0, 4.9, 2)
    ax.plot(ts, x0 + (x1 - x0) / dt * (ts - t0), color=fs.ORANGE, lw=1.2, ls='--')
    ax.plot([t0, t0 + dt], [x0, x0], color=fs.GRAY, lw=0.8)
    ax.plot([t0 + dt, t0 + dt], [x0, x1], color=fs.GRAY, lw=0.8)
    ax.plot([t0, t0 + dt], [x0, x1], 'o', color=fs.BLACK, ms=4)
    ax.text(t0 + dt / 2, x0 - 0.08, r'$\Delta t$', ha='center', va='top', fontsize=10)
    ax.text(t0 + dt + 0.08, (x0 + x1) / 2, r'$\Delta x$', ha='left', va='center', fontsize=10)
    ts_ = 4.6; tt_ = 4.3
    ax.annotate('할선 기울기\n' + r'$=\Delta x/\Delta t$ (평균 속도)', xy=(ts_, x0 + (x1 - x0) / dt * (ts_ - t0)),
                xytext=(5.3, 2.75), color=fs.ORANGE, fontsize=8.5, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color=fs.ORANGE, lw=0.7))
    ax.annotate('접선 기울기\n' + r'$=dx/dt$ (순간 속도)', xy=(tt_, x0 + df * (tt_ - t0)),
                xytext=(5.3, 1.55), color=fs.VEL, fontsize=8.5, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color=fs.VEL, lw=0.7))
    ax.text(5.5, f(5.5) + 0.05, r'$x(t)$', ha='left', va='bottom', fontsize=10)
    ax.set_xlim(0, 7.8); ax.set_ylim(0, 4.6)
    schematic_axes(ax, '', '$x$')
    ax.set_xticks([t0, t0 + dt]); ax.set_xticklabels([r'$t$', r'$t+\Delta t$'])
    for k in (t0, t0 + dt):
        ax.plot([k, k], [0, f(k)], color=fs.GRAY, lw=0.6, ls=':')
    ax.text(7.8, -0.1, '$t$', ha='right', va='top', fontsize=11)
    fs.save(fig, S, 'fig01_07')


# ---------- 그림 1.8 예제 1.4: v–t 그래프 아래 넓이 ----------
def fig08():
    fig, ax = fs.plot_axes(3.8, 2.6)
    v = lambda t: 2 + 3 * t ** 2
    t = np.linspace(0, 2.3, 200)
    dt = 0.2
    for t0 in np.arange(0, 2 - 1e-9, dt):
        ax.add_patch(Rectangle((t0, 0), dt, v(t0 + dt / 2), fc=fs.VEL, alpha=0.18, ec=fs.VEL, lw=0.5))
    ax.plot(t, v(t), color=fs.VEL, lw=1.7)
    ax.axvline(2, color=fs.GRAY, lw=0.8, ls='--')
    ax.text(1.2, 2.3, '넓이 $=\\Delta x = 12\\ \\mathrm{m}$', fontsize=9.5, ha='center')
    ax.text(1.85, 13.3, r'$v(t) = 2 + 3t^2$', color=fs.VEL, fontsize=10, ha='right')
    ax.set_xlim(0, 2.3); ax.set_ylim(0, 18)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    fs.save(fig, S, 'fig01_08')


# ---------- 그림 1.9 예제 1.5 밀도가 변하는 막대 ----------
def fig09():
    fig, ax = fs.canvas(4.2, 1.6, xlim=(-0.5, 5.2), ylim=(-0.95, 0.9))
    L = 4.5; h = 0.36
    n = 120
    for i in range(n):
        x = L * i / n
        ax.add_patch(Rectangle((x, -h / 2), L / n + 0.002, h, fc=fs.VEL, alpha=0.05 + 0.75 * (i + 0.5) / n,
                               ec='none', zorder=2))
    ax.add_patch(Rectangle((0, -h / 2), L, h, fc='none', ec=fs.BLACK, lw=1.1, zorder=3))
    xe, dx = 1.9, 0.22
    ax.add_patch(Rectangle((xe, -h / 2), dx, h, fc=fs.ORANGE, ec=fs.BLACK, lw=0.8, zorder=4))
    ax.text(xe + dx / 2, h / 2 + 0.1, r'$dm = \lambda\,dx$', fontsize=10, ha='center', va='bottom')
    fs.arrow(ax, (-0.3, -0.62), (L + 0.55, -0.62), color=fs.GRAY, lw=0.8, ms=8)
    ax.text(L + 0.55, -0.72, '$x$', fontsize=10, color=fs.GRAY, ha='right', va='top')
    for xv, s in ((0, '$0$'), (L, '$L$'), (xe, '$x$')):
        ax.plot([xv, xv], [-0.67, -0.57], color=fs.GRAY, lw=0.8)
        ax.text(xv, -0.72, s, fontsize=10, ha='center', va='top')
    xc = 2 * L / 3
    ax.add_patch(Polygon([(xc, -h / 2 - 0.02), (xc - 0.1, -h / 2 - 0.2), (xc + 0.1, -h / 2 - 0.2)],
                         closed=True, fc=fs.FORCE, ec='none', zorder=5))
    ax.plot([xc, xc], [-0.67, -0.57], color=fs.FORCE, lw=1.0)
    ax.text(xc, -0.72, r'$x_{\mathrm{cm}} = \frac{2}{3}L$', color=fs.FORCE, fontsize=10, ha='center', va='top')
    ax.text(L + 0.1, 0.0, '무거운 쪽', fontsize=8.5, ha='left', va='center')
    ax.text(-0.1, 0.0, '가벼운 쪽', fontsize=8.5, ha='right', va='center')
    ax.set_xlim(-1.1, 5.7)
    fs.save(fig, S, 'fig01_09')


# ---------- 그림 1.10 sin x의 테일러 근사 ----------
def fig10():
    fig, ax = fs.plot_axes(3.8, 2.6)
    x = np.linspace(-3.3, 3.3, 400)
    ax.plot(x, np.sin(x), color=fs.BLACK, lw=1.9, label=r'$\sin x$')
    ax.plot(x, x, color=fs.VEL, lw=1.2, ls='--', label=r'$x$')
    ax.plot(x, x - x ** 3 / 6, color=fs.FORCE, lw=1.2, ls='-.', label=r'$x - x^3/6$')
    ax.set_xlim(-3.3, 3.3); ax.set_ylim(-1.8, 1.8)
    ax.axhline(0, color=fs.GRAY, lw=0.6); ax.axvline(0, color=fs.GRAY, lw=0.6)
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_xticklabels([r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
    ax.set_xlabel(r'$x$ (rad)')
    ax.legend(loc='upper left', fontsize=9, frameon=False)
    fs.save(fig, S, 'fig01_10')


# ---------- 그림 1.11 예제 1.7 퍼텐셜 바닥의 포물선 근사 ----------
def fig11():
    fig, ax = fs.plot_axes(3.8, 2.6)
    ax.grid(False)
    D, a, x0 = 1.0, 1.3, 1.6
    x = np.linspace(0.85, 5.5, 400)
    U = D * (1 - np.exp(-a * (x - x0))) ** 2
    ax.plot(x, U, color=fs.BLACK, lw=1.7)
    xp = np.linspace(0.85, 3.0, 200)
    ax.plot(xp, 0.5 * 2 * D * a ** 2 * (xp - x0) ** 2, color=fs.VEL, lw=1.3, ls='--')
    ax.plot([x0], [0], 'o', color=fs.BLACK, ms=4)
    ax.text(x0, -0.06, r'$x_0$', ha='center', va='top', fontsize=11)
    ax.text(4.2, 0.82, r'$U(x)$', fontsize=11, ha='center')
    ax.text(2.55, 1.35, r'$U(x_0) + \frac{1}{2}U^{\prime\prime}(x_0)(x - x_0)^2$', color=fs.VEL, fontsize=9.5, ha='left')
    ax.set_xlim(0.6, 5.6); ax.set_ylim(-0.08, 1.55)
    schematic_axes(ax, '$x$', '$U$')
    ax.spines['bottom'].set_position(('data', 0))
    fs.save(fig, S, 'fig01_11')


# ---------- 그림 1.12 지수 감쇠와 반감기 ----------
def fig12():
    fig, ax = fs.plot_axes(3.8, 2.6)
    t = np.linspace(0, 4.2, 300)
    ax.plot(t, 2 ** (-t), color=fs.VEL, lw=1.8)
    for k in (1, 2, 3):
        y = 2.0 ** (-k)
        ax.plot([0, k, k], [y, y, 0], color=fs.GRAY, lw=0.8, ls='--')
        ax.plot([k], [y], 'o', color=fs.VEL, ms=4)
    ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', r'$t_{1/2}$', r'$2t_{1/2}$', r'$3t_{1/2}$', r'$4t_{1/2}$'])
    ax.set_yticks([0, 0.125, 0.25, 0.5, 1]); ax.set_yticklabels(['0', r'$N_0/8$', r'$N_0/4$', r'$N_0/2$', r'$N_0$'])
    ax.set_xlim(0, 4.2); ax.set_ylim(0, 1.08)
    ax.text(1.4, 0.62, r'$N(t) = N_0e^{-\lambda t}$', color=fs.VEL, fontsize=11)
    ax.set_xlabel('$t$'); ax.set_ylabel('$N$', rotation=0, labelpad=8)
    fs.save(fig, S, 'fig01_12')


# ---------- 그림 1.13 종단 속도에 다가가는 속도 ----------
def fig13():
    fig, ax = fs.plot_axes(3.8, 2.6)
    t = np.linspace(0, 5, 300)
    ax.plot(t, 1 - np.exp(-t), color=fs.VEL, lw=1.8)
    ax.axhline(1, color=fs.GRAY, lw=0.9, ls='--')
    ax.plot([0, 1.25], [0, 1.25], color=fs.ACC, lw=1.0, ls=':')
    ax.plot([1, 1], [0, 1 - np.exp(-1)], color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([0, 1], [1 - np.exp(-1)] * 2, color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([1], [1 - np.exp(-1)], 'o', color=fs.VEL, ms=4)
    ax.text(1.3, 1.18, '처음 기울기 $= g$', color=fs.ACC, fontsize=9, ha='left', va='center')
    ax.text(4.0, 1.04, r'종단 속도 $v_T = mg/b$', fontsize=9.5, ha='center', va='bottom')
    ax.text(2.5, 0.72, r'$v(t) = v_T\left(1 - e^{-t/\tau}\right)$', color=fs.VEL, fontsize=10.5)
    ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_xticklabels(['0', r'$\tau$', r'$2\tau$', r'$3\tau$', r'$4\tau$', r'$5\tau$'])
    ax.set_yticks([0, 1 - np.exp(-1), 1]); ax.set_yticklabels(['0', r'$0.63v_T$', r'$v_T$'])
    ax.set_xlim(0, 5); ax.set_ylim(0, 1.3)
    ax.set_xlabel('$t$'); ax.set_ylabel('$v$', rotation=0, labelpad=8)
    fs.save(fig, S, 'fig01_13')


# ---------- 그림 1.14 오일러 방법과 오일러–크로머 방법 ----------
def fig14():
    import matplotlib.pyplot as plt
    omega, dt, T = 2 * np.pi, 0.001, 3.0
    n = int(T / dt); t = np.arange(n) * dt
    res = {}
    for name in ('ec', 'e'):
        x = np.zeros(n); v = np.zeros(n); x[0] = 1.0
        for i in range(n - 1):
            v[i + 1] = v[i] - omega ** 2 * x[i] * dt
            x[i + 1] = x[i] + (v[i + 1] if name == 'ec' else v[i]) * dt
        res[name] = (x, v)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.4, 3.3), sharex=True, gridspec_kw=dict(height_ratios=[1.5, 1]))
    for a in (a1, a2):
        a.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    a1.plot(t, np.cos(omega * t), color=fs.BLACK, lw=2.2, label='정확한 해')
    a1.plot(t, res['ec'][0], color=fs.VEL, lw=1.0, ls='--', label='오일러–크로머')
    a1.plot(t, res['e'][0], color=fs.FORCE, lw=1.0, label='단순 오일러')
    a1.set_ylabel('$x$'); a1.set_ylim(-1.25, 1.45)
    a1.legend(loc='upper center', ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 1.18))
    for name, c, lab in (('ec', fs.VEL, '오일러–크로머'), ('e', fs.FORCE, '단순 오일러')):
        x, v = res[name]
        E = 0.5 * v ** 2 + 0.5 * omega ** 2 * x ** 2
        a2.plot(t, E / E[0], color=c, lw=1.2)
    a2.text(2.0, 1.105, '단순 오일러', color=fs.FORCE, fontsize=8.5, ha='right', va='bottom')
    a2.text(2.95, 1.01, '오일러–크로머', color=fs.VEL, fontsize=8.5, ha='right', va='bottom')
    a2.set_ylabel('$E/E_0$'); a2.set_xlabel('$t$ (s)')
    a2.set_ylim(0.97, 1.16); a2.set_xlim(0, 3)
    fs.save(fig, S, 'fig01_14')


# ---------- 그림 1.15 복소평면 ----------
def fig15():
    fig, ax = fs.canvas(3.2, 2.9, xlim=(-1.55, 1.75), ylim=(-1.3, 1.55))
    axes2d(ax, -1.45, 1.7, -1.25, 1.5, xl='실수축', yl='허수축', fontsize=9)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=fs.GRAY, lw=0.8, ls='--')
    t0 = np.radians(40); r = 1.0
    z = r * np.array([np.cos(t0), np.sin(t0)])
    ax.plot([z[0], z[0]], [0, z[1]], color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([0, z[0]], [z[1], z[1]], color=fs.GRAY, lw=0.8, ls=':')
    fs.arrow(ax, (0, 0), z, color=fs.VEL, lw=1.7)
    ax.text(z[0] + 0.05, z[1] + 0.05, r'$e^{i\theta}$', color=fs.VEL, fontsize=12, ha='left', va='bottom')
    fs.angle_arc(ax, (0, 0), 0.32, 0, 40, r'$\theta$', tr=0.45)
    ax.text(z[0] / 2, -0.06, r'$\cos\theta$', fontsize=9.5, ha='center', va='top')
    ax.text(-0.05, z[1] / 2 + 0.05, r'$\sin\theta$', fontsize=9.5, ha='right', va='center')
    fs.dot(ax, (-1, 0), r=0.04, color=fs.FORCE)
    ax.text(-1.05, 0.08, r'$e^{i\pi} = -1$', color=fs.FORCE, fontsize=9.5, ha='right', va='bottom')
    fs.dot(ax, (0, 1), r=0.04, color=fs.ACC)
    ax.text(0.07, 1.05, r'$e^{i\pi/2} = i$', color=fs.ACC, fontsize=9.5, ha='left', va='bottom')
    ax.text(1.05, -0.9, '단위원\n$|z| = 1$', fontsize=8.5, color=fs.GRAY, ha='center')
    fs.save(fig, S, 'fig01_15')


# ---------- 그림 1.16 예제 1.8 감쇠 진동 ----------
def fig16():
    fig, ax = fs.plot_axes(4.0, 2.5)
    w0, beta = 2 * np.pi, 0.35
    wd = np.sqrt(w0 ** 2 - beta ** 2)
    t = np.linspace(0, 8, 1200)
    env = np.exp(-beta * t)
    ax.plot(t, env, color=fs.FORCE, lw=1.0, ls='--')
    ax.plot(t, -env, color=fs.FORCE, lw=1.0, ls='--')
    ax.plot(t, env * np.cos(wd * t), color=fs.VEL, lw=1.5)
    ax.text(2.0, 0.66, r'$\pm Ae^{-\beta t}$', color=fs.FORCE, fontsize=10, ha='left', va='bottom')
    ax.text(5.2, -0.62, r'$x = Ae^{-\beta t}\cos(\omega_d t + \phi)$', color=fs.VEL, fontsize=10, ha='center')
    ax.set_xlim(0, 8); ax.set_ylim(-1.1, 1.1)
    ax.set_yticks([-1, 0, 1]); ax.set_yticklabels([r'$-A$', '0', r'$A$'])
    Td = 2 * np.pi / wd
    ax.set_xticks([0, 2 * Td, 4 * Td, 6 * Td, 8 * Td]); ax.set_xticklabels(['0', r'$2T_d$', r'$4T_d$', r'$6T_d$', r'$8T_d$'])
    ax.set_xlabel('$t$'); ax.set_ylabel('$x$', rotation=0, labelpad=6)
    fs.save(fig, S, 'fig01_16')


# ---------- 그림 1.17 예제 1.9 등퍼텐셜선과 -∇U ----------
def fig17():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    x = np.linspace(-0.6, 2.6, 300); y = np.linspace(0.4, 3.2, 300)
    X, Y = np.meshgrid(x, y)
    U = 3 * X ** 2 * Y - Y ** 3
    levels = [-14, -8, -4, -2, 0, 4, 8, 14]
    cs = ax.contour(X, Y, U, levels=levels, colors=fs.GRAY, linewidths=0.8, linestyles='solid')
    man = []
    for L in levels:
        if L < 0:      # 왼쪽 위 영역: x = -0.35 선 위에서 찾기
            yy = np.linspace(0.4, 3.2, 4000); xv = -0.35
            k = np.argmin(abs(3 * xv ** 2 * yy - yy ** 3 - L)); man.append((xv, yy[k]))
        elif L == 0:
            man.append((0.3, np.sqrt(3) * 0.3 + 0.0))
        else:          # 오른쪽 아래 영역: y = 0.8 선 위
            yv = 0.8; xv = np.sqrt((L + yv ** 3) / (3 * yv)); man.append((xv, yv))
    ax.clabel(cs, fontsize=7.5, fmt=lambda v: f'${v:g}$', inline_spacing=2, manual=man)
    cs2 = ax.contour(X, Y, U, levels=[-2], colors=fs.BLACK, linewidths=1.6, linestyles='solid')
    ax.set_aspect('equal')
    p = np.array([1.0, 2.0])
    F = np.array([-12.0, 9.0]); u = F / 15.0
    fs.arrow(ax, p, p + 0.75 * u, color=fs.FORCE, lw=2.0)
    fs.arrow(ax, p, p - 0.55 * u, color=fs.FORCE, lw=1.0, ls='--', ms=9)
    ax.plot(*p, 'o', color=fs.BLACK, ms=4, zorder=7)
    ax.text(p[0] - 0.08, p[1] - 0.06, '$(1, 2)$', fontsize=9, ha='right', va='top',
            bbox=dict(fc='white', ec='none', pad=0.5, alpha=0.85))
    q = p + 0.75 * u
    ax.text(q[0] - 0.05, q[1] + 0.07, r'$\vec{F} = -\nabla U$', color=fs.FORCE, fontsize=10, ha='center', va='bottom',
            bbox=dict(fc='white', ec='none', pad=0.5, alpha=0.85))
    r = p - 0.55 * u
    ax.text(r[0] + 0.04, r[1] - 0.04, r'$\nabla U$', color=fs.FORCE, fontsize=9.5, ha='left', va='top',
            bbox=dict(fc='white', ec='none', pad=0.5, alpha=0.85))
    ax.set_xlabel('$x$ (m)'); ax.set_ylabel('$y$ (m)')
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(0.4, 3.2)
    ax.set_title(r'$U = 3x^2y - y^3$의 등고선 (단위 J)', fontsize=9.5)
    fs.save(fig, S, 'fig01_17')


# ---------- 그림 1.18 선적분 ----------
def fig18():
    fig, ax = fs.canvas(3.8, 2.4, xlim=(-0.3, 5.0), ylim=(-0.45, 2.9))
    s = np.linspace(0, 1, 300)
    cx = 0.3 + 4.2 * s
    cy = 0.4 + 1.9 * np.sin(np.pi * s * 0.9) * (1 - 0.3 * s)
    ax.plot(cx, cy, color=fs.GRAY, lw=1.3)
    fs.dot(ax, (cx[0], cy[0])); fs.dot(ax, (cx[-1], cy[-1]))
    ax.text(cx[0] - 0.1, cy[0] - 0.05, '$a$', fontsize=12, ha='right', va='top')
    ax.text(cx[-1] + 0.1, cy[-1] - 0.05, '$b$', fontsize=12, ha='left', va='top')
    ax.text(0.75, 1.55, '$C$', fontsize=12)
    Ffield = lambda x, y: 0.95 * np.array([np.cos(np.radians(40)), np.sin(np.radians(40))])
    for k, idx in enumerate((22, 140, 235)):
        p = np.array([cx[idx], cy[idx]])
        tng = np.array([cx[idx + 1] - cx[idx - 1], cy[idx + 1] - cy[idx - 1]]); tng /= np.hypot(*tng)
        Fk = Ffield(*p)
        fs.arrow(ax, p, p + Fk, color=fs.FORCE, lw=1.5, zorder=4)
        fs.arrow(ax, p, p + 0.6 * tng, color=fs.BLACK, lw=2.0, ms=10, zorder=6)
        if k == 1:
            a1 = np.degrees(np.arctan2(tng[1], tng[0])); a2 = np.degrees(np.arctan2(Fk[1], Fk[0]))
            fs.angle_arc(ax, p, 0.5, min(a1, a2), max(a1, a2), r'$\theta$', fontsize=10, tr=0.72)
            ax.text(p[0] + 0.35, p[1] - 0.12, r'$d\vec{\ell}$', fontsize=11, ha='center', va='top')
            ax.text(p[0] + Fk[0] + 0.05, p[1] + Fk[1] + 0.02, r'$\vec{F}$', color=fs.FORCE, fontsize=12, ha='left', va='bottom')
    ax.text(2.6, -0.25, r'$\vec{F}\cdot d\vec{\ell} = F\cos\theta\,d\ell$', fontsize=10.5, ha='center', va='center')
    fs.save(fig, S, 'fig01_18')


# ---------- 그림 1.19 면적분과 선속 ----------
def fig19():
    fig, ax = fs.canvas(3.6, 2.7, xlim=(-1.9, 2.4), ylim=(-1.35, 1.95))
    d = np.array([0.75, 0.42])  # 깊이 방향
    w = np.array([1.9, 0.0])
    O = np.array([-1.2, -0.4])
    corners = [O, O + w, O + w + 1.6 * d, O + 1.6 * d]
    ax.add_patch(Polygon(corners, closed=True, fc=fs.SURF, alpha=0.5, ec=fs.BLACK, lw=1.1, zorder=2))
    ax.text(*(O + w + 1.6 * d + np.array([0.08, 0.0])), '$S$', fontsize=11, ha='left', va='center')
    # 작은 조각 dA
    c = O + 0.62 * w + 0.5 * d
    pw = w * 0.16; pd = d * 0.32
    ax.add_patch(Polygon([c, c + pw, c + pw + pd, c + pd], closed=True, fc=fs.ORANGE, alpha=0.8, ec=fs.BLACK, lw=0.7, zorder=3))
    m = c + (pw + pd) / 2
    fs.arrow(ax, m, m + np.array([0, 1.25]), color=fs.BLACK, lw=1.6, zorder=6)
    ax.text(m[0] - 0.07, m[1] + 1.25, r'$d\vec{A}$', fontsize=11, ha='right', va='center')
    # 장(필드) 화살표: 법선과 각 θ
    th = np.radians(35)
    u = np.array([np.sin(th), np.cos(th)])
    for off in (-1.1, -0.5, 0.2, 0.8):
        base = m + np.array([off, 0]) - 0.75 * u
        fs.arrow(ax, base, base + 2.15 * u, color=fs.FIELD, lw=1.1, ms=10, zorder=1 if off != 0.2 else 5)
    # 각도: 조각 위에서 법선과 F 사이
    fs.angle_arc(ax, m, 0.55, 90 - 35, 90, r'$\theta$', fontsize=10, tr=0.75)
    fs.arrow(ax, m, m + 0.95 * u, color=fs.FIELD, lw=1.9, zorder=6)
    ax.text(m[0] + 0.95 * u[0] + 0.1, m[1] + 0.95 * u[1] - 0.12, r'$\vec{F}$', color=fs.FIELD, fontsize=12, ha='left', va='center',
            bbox=dict(fc='white', ec='none', pad=0.3, alpha=0.8), zorder=7)
    ax.text(0.3, -1.22, r'$d\Phi = \vec{F}\cdot d\vec{A} = F\cos\theta\,dA$', fontsize=10, ha='center')
    fs.save(fig, S, 'fig01_19')


# ---------- 그림 1.20 발산과 회전 ----------
def fig20():
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.5))
    g = np.linspace(-1, 1, 7)
    X, Y = np.meshgrid(g, g)
    for ax, (U, V), title in ((axs[0], (X, Y), r'$\vec{F} = x\hat{i} + y\hat{j}$' + '\n' + r'$\nabla\cdot\vec{F} = 2,\ \nabla\times\vec{F} = 0$'),
                              (axs[1], (-Y, X), r'$\vec{F} = -y\hat{i} + x\hat{j}$' + '\n' + r'$\nabla\cdot\vec{F} = 0,\ \nabla\times\vec{F} = 2\hat{k}$')):
        ax.quiver(X, Y, U, V, color=fs.FIELD, angles='xy', scale_units='xy', scale=4.2, width=0.012)
        ax.set_aspect('equal'); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(fs.GRAY); s.set_linewidth(0.6)
        ax.set_title(title, fontsize=9)
    axs[0].set_xlabel('(가) 솟아나는 장', fontsize=9)
    axs[1].set_xlabel('(나) 소용돌이치는 장', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, S, 'fig01_20')


# ---------- 그림 1.21 연습문제 8: 원판을 고리로 나누기 ----------
def fig21():
    fig, ax = fs.canvas(2.8, 2.6, xlim=(-1.45, 1.6), ylim=(-1.3, 1.45))
    R = 1.2
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2))
    r, dr = 0.72, 0.13
    th = np.linspace(0, 2 * np.pi, 200)
    ring = np.concatenate([np.c_[(r + dr) * np.cos(th), (r + dr) * np.sin(th)],
                           np.c_[r * np.cos(th[::-1]), r * np.sin(th[::-1])]])
    ax.add_patch(Polygon(ring, closed=True, fc=fs.ORANGE, alpha=0.75, ec=fs.BLACK, lw=0.6))
    fs.dot(ax, (0, 0), r=0.035)
    a = np.radians(200)
    fs.arrow(ax, (0, 0), (r * np.cos(a), r * np.sin(a)), color=fs.BLACK, lw=1.0, ms=8)
    ax.text(0.5 * r * np.cos(a), 0.5 * r * np.sin(a) + 0.08, '$r$', fontsize=11, ha='center', va='bottom')
    b = np.radians(-35)
    fs.arrow(ax, (0, 0), (R * np.cos(b), R * np.sin(b)), color=fs.GRAY, lw=0.9, ms=8)
    ax.text(1.0 * np.cos(b) + 0.07, 1.0 * np.sin(b) + 0.1, '$R$', fontsize=11, color=fs.GRAY, ha='center', va='center')
    c = np.radians(60)
    p = np.array([(r + dr / 2) * np.cos(c), (r + dr / 2) * np.sin(c)])
    ax.annotate('폭 $dr$인 고리\n' + r'$dm = \frac{M}{\pi R^2}\,2\pi r\,dr$', xy=p, xytext=(0.75, 1.3), fontsize=8.5,
                ha='left', va='center', arrowprops=dict(arrowstyle='-', color=fs.BLACK, lw=0.7))
    fs.save(fig, S, 'fig01_21')


# ---------- 그림 1.22 연습문제 12: 두 경로와 힘의 장 ----------
def fig22():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    g = np.linspace(0, 1.2, 7)
    X, Y = np.meshgrid(g, g)
    ax.quiver(X, Y, 2 * X * Y, X ** 2, color=fs.FORCE, alpha=0.55, angles='xy', scale_units='xy', scale=9, width=0.008)
    s = np.linspace(0, 1, 100)
    ax.plot(s, s, color=fs.VEL, lw=1.8, label='(가) $y = x$')
    ax.plot(s, s ** 2, color=fs.ACC, lw=1.8, ls='--', label='(나) $y = x^2$')
    ax.plot([0, 1], [0, 1], 'o', color=fs.BLACK, ms=4)
    ax.text(0.03, -0.04, '$(0, 0)$', fontsize=9, ha='left', va='top')
    ax.text(1.0, 1.04, '$(1, 1)$', fontsize=9, ha='center', va='bottom')
    ax.set_aspect('equal'); ax.set_xlim(-0.08, 1.3); ax.set_ylim(-0.15, 1.3)
    ax.set_xlabel('$x$ (m)'); ax.set_ylabel('$y$ (m)')
    ax.legend(loc='upper left', fontsize=8.5, frameon=True, framealpha=0.9)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.text(0.03, 0.83, r'$\vec{F} = 2xy\,\hat{i} + x^2\,\hat{j}$', color=fs.FORCE, fontsize=9, ha='left', va='center',
            bbox=dict(fc='white', ec='none', pad=1.0, alpha=0.9))
    fs.save(fig, S, 'fig01_22')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11,
              fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20, fig21, fig22):
        f()
