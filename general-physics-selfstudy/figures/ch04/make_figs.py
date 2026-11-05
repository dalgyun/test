"""4장 2차원과 3차원 운동 그림. 실행: python3 figures/ch04/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Arc

g = 9.8


def axes2d(ax, o, xl, yl, xlab=r'$x$', ylab=r'$y$', lw=0.9):
    fs.arrow(ax, (o[0], o[1]), (xl, o[1]), lw=lw, ms=9)
    fs.arrow(ax, (o[0], o[1]), (o[0], yl), lw=lw, ms=9)
    ax.text(xl + 0.05 * abs(xl - o[0]) / 4, o[1], xlab, va='center', fontsize=10)
    ax.text(o[0], yl, ylab, ha='center', va='bottom', fontsize=10)


def ksub(ax, x, y, base, sub, color=fs.BLACK, size=9, ha='left', va='center'):
    """수식 기호 base 뒤에 한글 아래첨자 sub를 붙인다(mathtext는 한글을 못 쓰므로)."""
    r = ax.figure.canvas.get_renderer()
    t1 = ax.text(0, 0, base, fontsize=size); w1 = t1.get_window_extent(r).width / ax.figure.dpi * 72; t1.remove()
    t2 = ax.text(0, 0, sub, fontsize=size * 0.72); w2 = t2.get_window_extent(r).width / ax.figure.dpi * 72; t2.remove()
    W = w1 + w2 + 0.5
    x0 = {'left': 0, 'center': -W / 2, 'right': -W}[ha]
    ax.annotate(base, xy=(x, y), xytext=(x0, 0), textcoords='offset points', fontsize=size, color=color,
                ha='left', va=va)
    ax.annotate(sub, xy=(x, y), xytext=(x0 + w1 + 0.5, -size * 0.38), textcoords='offset points',
                fontsize=size * 0.72, color=color, ha='left', va=va)


def style(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# ---------- 그림 4.1 위치 벡터와 변위, 속도 ----------
def fig01():
    fig, ax = fs.canvas(3.8, 2.8, xlim=(-0.4, 5.4), ylim=(-0.4, 3.8))
    axes2d(ax, (0, 0), 5.2, 3.6)
    s = np.linspace(0, 1, 300)
    cx = 0.8 + 4.0 * s; cy = 0.5 + 4.5 * s - 3.0 * s ** 2
    ax.plot(cx, cy, color=fs.BLACK, lw=1.4)
    ax.text(cx[-1] + 0.05, cy[-1] - 0.2, '궤적', fontsize=9)
    s1, s2 = 0.2, 0.62
    P1 = np.array([0.8 + 4 * s1, 0.5 + 4.5 * s1 - 3 * s1 ** 2]); P2 = np.array([0.8 + 4 * s2, 0.5 + 4.5 * s2 - 3 * s2 ** 2])
    ax.text(-0.15, -0.28, 'O', fontsize=10)
    fs.arrow(ax, (0, 0), tuple(P1), color=fs.BLACK, lw=1.3)
    fs.arrow(ax, (0, 0), tuple(P2), color=fs.BLACK, lw=1.3)
    ax.text(P1[0] * 0.5 - 0.15, P1[1] * 0.5 + 0.1, r'$\vec r(t)$', fontsize=10, ha='right')
    ax.text(P2[0] * 0.6 + 0.1, P2[1] * 0.6 - 0.2, r'$\vec r(t+\Delta t)$', fontsize=10, va='top')
    fs.arrow(ax, tuple(P1), tuple(P2), color=fs.GRAY, lw=1.3)
    m = (P1 + P2) / 2
    ax.text(m[0] + 0.1, m[1] - 0.12, r'$\Delta\vec r$', fontsize=10, color=fs.GRAY, va='top')
    d = np.array([4.0, 4.5 - 6 * s1]); d /= np.hypot(*d)
    fs.vec(ax, tuple(P1), 1.0 * d, color=fs.VEL, lw=1.8)
    ax.text(P1[0] + 1.0 * d[0] - 0.1, P1[1] + 1.0 * d[1] + 0.12, r'$\vec v$', color=fs.VEL, fontsize=11, ha='right')
    fs.dot(ax, P1, r=0.05); fs.dot(ax, P2, r=0.05)
    fs.save(fig, __file__, 'fig04_01')


# ---------- 그림 4.2 예제 4.1 ----------
def traj41(t):
    return 3.0 * t ** 2, 2.0 * t ** 3 - 4.0 * t


def fig02():
    fig, ax = fs.canvas(4.4, 3.2, xlim=(-1.2, 8.8), ylim=(-3.0, 3.3))
    axes2d(ax, (0, 0), 8.5, 3.0, xlab=r'$x$ (m)', ylab=r'$y$ (m)')
    ax.plot([0, 0], [0, -2.7], color=fs.BLACK, lw=0.9)
    for k in range(1, 8):
        ax.plot([k, k], [-0.06, 0.06], color=fs.BLACK, lw=0.7)
    for k in (2, 4, 6):
        ax.text(k, 0.12, str(k), ha='center', va='bottom', fontsize=7.5)
    for k in (-2, -1, 1, 2):
        ax.plot([-0.06, 0.06], [k, k], color=fs.BLACK, lw=0.7)
        ax.text(-0.12, k, str(k).replace('-', '−'), ha='right', va='center', fontsize=7.5)
    t = np.linspace(0, 1.62, 300)
    x, y = traj41(t)
    ax.plot(x, y, color=fs.BLACK, lw=1.4)
    xk, yk = traj41(1.5); fs.dot(ax, (xk, yk), r=0.06, color=fs.GRAY)
    ax.text(xk + 0.15, yk - 0.15, r'$t=1.5$ s', fontsize=7.5, color=fs.GRAY, va='top')
    P = (3.0, -2.0)
    fs.dot(ax, (0, 0), r=0.06); fs.dot(ax, P, r=0.07)
    ax.text(-0.15, 0.15, r'$t=0$', fontsize=8, ha='right')
    ax.text(3.15, -2.45, r'$t=1.0$ s', fontsize=8)
    fs.arrow(ax, (0, 0), P, color=fs.GRAY, lw=1.0, ls='--')
    ax.text(1.75, -0.85, r'$\Delta\vec r$', color=fs.GRAY, fontsize=9)
    fs.vec(ax, (0, 0), (0, -4.0 * 0.3), color=fs.VEL, lw=1.6)
    ax.text(0.12, -0.75, r'$\vec v(0)$', color=fs.VEL, fontsize=9, ha='left')
    sv, sa = 0.3, 0.14
    fs.vec(ax, P, (6.0 * sv, 2.0 * sv), color=fs.VEL, lw=1.8)
    ax.text(P[0] + 6 * sv + 0.1, P[1] + 2 * sv - 0.05, r'$\vec v$', color=fs.VEL, fontsize=11)
    fs.vec(ax, P, (6.0 * sa, 12.0 * sa), color=fs.ACC, lw=1.8)
    ax.text(P[0] + 6 * sa - 0.15, P[1] + 12 * sa - 0.05, r'$\vec a$', color=fs.ACC, fontsize=11, ha='right')
    fs.angle_arc(ax, P, 0.7, np.degrees(np.arctan2(2, 6)), np.degrees(np.arctan2(12, 6)), r'$45^\circ$', fontsize=8, tr=1.0)
    fs.save(fig, __file__, 'fig04_02')


# ---------- 그림 4.3 포물선 운동의 속도 벡터 ----------
def fig03():
    v0, th = 20.0, np.radians(55)
    vx, vy0 = v0 * np.cos(th), v0 * np.sin(th)
    tf = 2 * vy0 / g; R = vx * tf; H = vy0 ** 2 / (2 * g)
    fig, ax = fs.canvas(5.0, 2.9, xlim=(-3, R + 7), ylim=(-4.6, H + 6))
    fs.ground(ax, -2, R + 3, 0, depth=0.8, n=40)
    t = np.linspace(0, tf, 200)
    ax.plot(vx * t, vy0 * t - 0.5 * g * t ** 2, color=fs.BLACK, lw=1.3)
    s = 0.42
    for i, tk in enumerate(np.linspace(0, tf, 5)):
        x, y = vx * tk, vy0 * tk - 0.5 * g * tk ** 2
        vyk = vy0 - g * tk
        fs.dot(ax, (x, y), r=0.35)
        if i == 4:
            continue
        fs.vec(ax, (x, y), (vx * s, vyk * s), color=fs.VEL, lw=1.7, ms=10)
        if i in (1, 3):
            fs.vec(ax, (x, y), (vx * s, 0), color=fs.VEL, lw=0.9, ls='--', ms=7)
            fs.vec(ax, (x, y), (0, vyk * s), color=fs.VEL, lw=0.9, ls='--', ms=7)
        if i == 1:
            ax.text(x + vx * s / 2, y - 1.0, r'$v_x$', color=fs.VEL, fontsize=9, ha='center', va='top')
            ax.text(x - 0.5, y + vyk * s / 2, r'$v_y$', color=fs.VEL, fontsize=9, ha='right', va='center')
        if i == 3:
            ax.text(x + vx * s / 2, y + 0.6, r'$v_x$', color=fs.VEL, fontsize=9, ha='center', va='bottom')
    ax.text(vx * s * 0.6 - 0.6, vy0 * s * 0.6 + 0.6, r'$\vec v_0$', color=fs.VEL, fontsize=10, ha='right')
    fs.angle_arc(ax, (0, 0), 2.6, 0, np.degrees(th), r'$\theta_0$', fontsize=9, tr=3.7)
    ax.text(R / 2 + 0.5, H + 1.2, r'$v_y = 0$', color=fs.VEL, fontsize=8.5)
    # 가속도
    xa = R + 3.5
    fs.vec(ax, (xa, H + 3), (0, -5.0), color=fs.ACC, lw=1.7)
    ax.text(xa - 0.6, H + 0.6, r'$\vec a = -g\hat{j}$', color=fs.ACC, fontsize=9.5, ha='right')
    ax.plot([R * 0.5, R * 0.5], [0, H], color=fs.GRAY, lw=0.6, ls=':')
    fs.dim(ax, (R * 0.5, 0), (R * 0.5, H), r'$H$', off=-1.6, fontsize=10)
    fs.dim(ax, (0, 0), (R, 0), r'$R$', off=-2.0, fontsize=10)
    fs.save(fig, __file__, 'fig04_03')


# ---------- 그림 4.4 같은 사거리를 주는 두 발사각 ----------
def fig04():
    fig, ax = fs.plot_axes(4.4, 2.6)
    v0 = 20.0
    cols = {15: fs.ORANGE, 75: fs.ORANGE, 30: fs.ACC, 60: fs.ACC, 45: fs.VEL}
    for deg in (15, 30, 45, 60, 75):
        th = np.radians(deg)
        tf = 2 * v0 * np.sin(th) / g
        t = np.linspace(0, tf, 200)
        x = v0 * np.cos(th) * t; y = v0 * np.sin(th) * t - 0.5 * g * t ** 2
        ax.plot(x, y, color=cols[deg], lw=1.5 if deg == 45 else 1.2, ls='-' if deg <= 45 else '--')
        i = 70 if deg != 15 else 100
        xm, ym = x[np.argmax(y)], y.max()
        ax.text(xm, ym + 0.6, f'{deg}°', ha='center', fontsize=8, color=cols[deg])
    ax.set_xlabel(r'$x$ (m)'); ax.set_ylabel(r'$y$ (m)')
    ax.set_xlim(0, 44); ax.set_ylim(0, 21)
    ax.set_aspect('equal')
    ax.annotate(r'$R_{\max} = v_0^2/g$ (45°)', xy=(40.6, 0.3), xytext=(33, 14), fontsize=8.5, color=fs.VEL,
                ha='center', arrowprops=dict(arrowstyle='->', color=fs.VEL, lw=0.8))
    fs.save(fig, __file__, 'fig04_04')


# ---------- 그림 4.5 예제 4.2 절벽 ----------
def fig05():
    v0, th, y0 = 15.0, np.radians(30), 20.0
    vx, vy0 = v0 * np.cos(th), v0 * np.sin(th)
    tf = (vy0 + np.sqrt(vy0 ** 2 + 2 * g * y0)) / g
    xf = vx * tf; vyf = vy0 - g * tf
    fig, ax = fs.canvas(5.0, 2.9, xlim=(-9, 56), ylim=(-5.5, 29))
    ax.add_patch(Polygon([(-8, 0), (0, 0), (0, y0), (-8, y0)], fc='#ecebe6', ec=fs.BLACK, lw=1.2, zorder=1))
    fs.ground(ax, 0, 55, 0, depth=0.9, n=55)
    t = np.linspace(0, tf, 200)
    ax.plot(vx * t, y0 + vy0 * t - 0.5 * g * t ** 2, color=fs.BLACK, lw=1.4)
    fs.vec(ax, (0, y0), (vx * 0.5, vy0 * 0.5), color=fs.VEL, lw=1.7)
    ax.text(vx * 0.25 - 1.0, y0 + vy0 * 0.25 + 2.2, r'$15.0$ m/s', color=fs.VEL, fontsize=8.5, ha='center')
    ax.plot([0, 9], [y0, y0], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, (0, y0), 4.5, 0, 30, r'$30.0^\circ$', fontsize=8, tr=7.6)
    fs.dot(ax, (xf, 0), r=0.5)
    # 땅에 닿을 때의 속도: 착지점 오른쪽에 따로 그린다
    s = 0.55
    A = np.array([xf + 3.5, 0.8 - vyf * s])
    fs.vec(ax, A, (vx * s, vyf * s), color=fs.VEL, lw=1.8)
    fs.vec(ax, A, (vx * s, 0), color=fs.VEL, lw=0.8, ls='--', ms=7)
    ax.plot([A[0] + vx * s, A[0] + vx * s], [A[1], A[1] + vyf * s], color=fs.VEL, lw=0.8, ls='--')
    fs.angle_arc(ax, tuple(A), 3.2, np.degrees(np.arctan2(vyf, vx)), 0, None)
    am = np.radians(-29)
    ax.annotate(r'$58.5^\circ$', xy=(A[0] + 3.2 * np.cos(am), A[1] + 3.2 * np.sin(am)), xytext=(A[0] - 1.5, A[1] - 6),
                fontsize=8, ha='right', arrowprops=dict(arrowstyle='-', color=fs.BLACK, lw=0.5))
    ax.text(A[0] + vx * s / 2, A[1] + 0.7, r'$13.0$', color=fs.VEL, fontsize=8, ha='center')
    ax.text(A[0] + vx * s + 0.6, A[1] + vyf * s / 2, r'$-21.2$', color=fs.VEL, fontsize=8, va='center')
    ax.text(A[0] + 3.0, A[1] + 3.2, '땅에 닿을 때의 속도\n(24.8 m/s)', fontsize=8, color=fs.VEL, ha='center')
    ax.annotate('', xy=(-4, y0), xytext=(-4, 0), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(-3.6, y0 / 2, r'$20.0$ m', fontsize=8, color=fs.GRAY, va='center')
    fs.dim(ax, (0, 0), (xf, 0), r'$38.0$ m', off=-2.3, fontsize=8)
    ax.text(-0.6, -1.8, 'O', fontsize=9, ha='right')
    fs.save(fig, __file__, 'fig04_05')


# ---------- 그림 4.6 원숭이와 사냥꾼 ----------
def fig06():
    fig, ax = fs.canvas(4.8, 2.8, xlim=(-1, 23.5), ylim=(-1.8, 12.2))
    fs.ground(ax, -1, 23, 0, depth=0.4, n=55)
    M = np.array([18.0, 10.0])  # 원숭이 처음 위치
    G = np.array([0.0, 1.0])     # 총구
    d = M - G; L = np.hypot(*d); u = d / L
    v0 = 22.0
    T = L / v0
    ax.plot([G[0], M[0]], [G[1], M[1]], color=fs.GRAY, lw=0.9, ls='--')
    ax.text(7.5, 6.0, '조준선(중력이 없을 때의 경로)', fontsize=8, color=fs.GRAY, rotation=np.degrees(np.arctan2(d[1], d[0])),
            ha='center', va='bottom', rotation_mode='anchor')
    t = np.linspace(0, T, 200)
    bx = G[0] + v0 * u[0] * t; by = G[1] + v0 * u[1] * t - 0.5 * g * t ** 2
    ax.plot(bx, by, color=fs.VEL, lw=1.5)
    ax.plot([M[0], M[0]], [M[1], M[1] - 0.5 * g * T ** 2], color=fs.FORCE, lw=0.9, ls=':')
    for tk in (T / 3, 2 * T / 3, T):
        xb = G[0] + v0 * u[0] * tk; yl = G[1] + v0 * u[1] * tk; yb = yl - 0.5 * g * tk ** 2
        ax.plot([xb, xb], [yl, yb], color=fs.ACC, lw=1.0)
        fs.dot(ax, (xb, yb), r=0.18, color=fs.VEL)
        fs.dot(ax, (xb, yl), r=0.1, color=fs.GRAY)
        ym = M[1] - 0.5 * g * tk ** 2
        ax.add_patch(Circle((M[0], ym), 0.4, fc='#b07040', ec=fs.BLACK, lw=0.8, zorder=6, alpha=1.0 if tk == T else 0.45))
    xb2 = G[0] + v0 * u[0] * 2 * T / 3; yl2 = G[1] + v0 * u[1] * 2 * T / 3; yb2 = yl2 - 0.5 * g * (2 * T / 3) ** 2
    ax.text(xb2 + 0.3, (yl2 + yb2) / 2, r'$\frac{1}{2}gt^2$', color=fs.ACC, fontsize=10, ha='left', va='center')
    ax.add_patch(Circle(M, 0.4, fc='#b07040', ec=fs.BLACK, lw=0.8, zorder=6, alpha=0.45))
    ax.text(M[0] + 0.7, M[1] + 0.6, '원숭이(처음 위치)', fontsize=8, va='center')
    ax.text(M[0] + 0.7, M[1] - 0.5 * g * T ** 2, '만나는 점', fontsize=8, va='center')
    ax.plot([M[0] - 1.5, M[0] + 0.5], [M[1] + 0.4, M[1] + 0.4], color='#6b4f2a', lw=3)
    # 총
    ax.add_patch(Polygon([G - 0.6 * u + (-u[1] * 0.25, u[0] * 0.25), G + (-u[1] * 0.18, u[0] * 0.18),
                          G - (-u[1] * 0.18, u[0] * 0.18), G - 0.6 * u - (-u[1] * 0.25, u[0] * 0.25)],
                         fc=fs.BLACK, zorder=5))
    ax.plot([G[0] - 0.3, G[0] - 0.3], [0, G[1] - 0.2], color=fs.BLACK, lw=1.5)
    ax.text(0.2, -1.4, '사냥꾼', fontsize=8)
    ax.text(10.5, 2.4, '총알', fontsize=8, color=fs.VEL)
    fs.save(fig, __file__, 'fig04_06')


# ---------- 그림 4.7 등속 원운동 ----------
def fig07():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.6), gridspec_kw=dict(width_ratios=[1.25, 1]))
    for a in (a1, a2):
        a.axis('off'); a.set_aspect('equal')
    a1.set_xlim(-1.5, 1.9); a1.set_ylim(-1.35, 1.45)
    th = np.linspace(0, 2 * np.pi, 300)
    a1.plot(np.cos(th), np.sin(th), color=fs.BLACK, lw=1.1)
    fs.arrow(a1, (-1.4, 0), (1.45, 0), lw=0.7, ms=8, color=fs.GRAY)
    fs.arrow(a1, (0, -1.3), (0, 1.35), lw=0.7, ms=8, color=fs.GRAY)
    a1.text(1.5, -0.12, r'$x$', fontsize=9); a1.text(-0.12, 1.3, r'$y$', fontsize=9)
    p = np.radians(28)
    P = np.array([np.cos(p), np.sin(p)])
    a1.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=1.0)
    a1.text(0.38, 0.05, r'$\vec r$', fontsize=10)
    fs.angle_arc(a1, (0, 0), 0.25, 0, 28, None)
    a1.text(0.3, -0.12, r'$\omega t$', fontsize=8)
    T = np.array([-np.sin(p), np.cos(p)])
    fs.vec(a1, P, 0.8 * T, color=fs.VEL, lw=1.8)
    a1.text(P[0] + 0.8 * T[0] + 0.08, P[1] + 0.8 * T[1] + 0.05, r'$\vec v$', color=fs.VEL, fontsize=11)
    fs.vec(a1, P, -0.5 * P, color=fs.ACC, lw=2.0)
    a1.text(P[0] - 0.3 * P[0] - 0.05, P[1] - 0.3 * P[1] + 0.13, r'$\vec a$', color=fs.ACC, fontsize=11)
    fs.dot(a1, P, r=0.04)
    a1.text(-1.45, 1.3, '(가)', fontsize=9)
    a1.text(0.7, -1.15, r'반지름 $r$', fontsize=8)
    # (나) 속도 벡터의 변화: 원의 꼭대기 근처(위치각 70°→110°)
    a2.set_xlim(-2.0, 0.7); a2.set_ylim(-1.0, 1.4)
    p1, p2 = np.radians(70), np.radians(110)
    v1 = 1.4 * np.array([-np.sin(p1), np.cos(p1)]); v2 = 1.4 * np.array([-np.sin(p2), np.cos(p2)])
    O = np.array([0.0, 0.0])
    fs.vec(a2, O, v1, color=fs.VEL, lw=1.6)
    fs.vec(a2, O, v2, color=fs.VEL, lw=1.6)
    fs.arrow(a2, tuple(v1), tuple(v2), color=fs.ACC, lw=1.8)
    a2.text(v1[0] + 0.55, v1[1] + 0.12, r'$\vec v(t)$', color=fs.VEL, fontsize=9, ha='center')
    a2.text(v2[0] + 0.55, v2[1] - 0.15, r'$\vec v(t+\Delta t)$', color=fs.VEL, fontsize=9, ha='center', va='top')
    a2.text(v1[0] - 0.12, 0, r'$\Delta\vec v$', color=fs.ACC, fontsize=10, ha='right', va='center')
    fs.angle_arc(a2, O, 0.45, 160, 200, None)
    a2.text(-0.55, 0.0, r'$\omega\Delta t$', fontsize=8, ha='right', va='center')
    fs.dot(a2, O, r=0.03)
    a2.text(-1.95, 1.25, '(나)', fontsize=9)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig04_07')


# ---------- 그림 4.8 접선·법선 가속도와 곡률원 ----------
def fig08():
    fig, ax = fs.canvas(4.0, 3.0, xlim=(-0.3, 4.6), ylim=(-0.3, 3.4))
    # 곡률이 위치에 따라 변하는 곡선: 방향각을 곡률 kappa(s)로 적분
    ss = np.linspace(0, 5.0, 2000); ds = ss[1] - ss[0]
    s0, rho0 = 2.4, 1.3
    kappa = (1 / rho0) * np.exp(-((ss - s0) / 0.8) ** 2)
    ang = np.cumsum(kappa) * ds - 0.05
    xs = np.cumsum(np.cos(ang)) * ds; ys = np.cumsum(np.sin(ang)) * ds
    ax.plot(xs, ys, color=fs.BLACK, lw=1.4)
    i0 = np.searchsorted(ss, s0)
    P = np.array([xs[i0], ys[i0]]); T = np.array([np.cos(ang[i0]), np.sin(ang[i0])]); N = np.array([-T[1], T[0]])
    C = P + rho0 * N
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(C[0] + rho0 * np.cos(th), C[1] + rho0 * np.sin(th), color=fs.GRAY, lw=0.8, ls='--')
    fs.dot(ax, C, r=0.04, color=fs.GRAY)
    ax.plot([P[0], C[0]], [P[1], C[1]], color=fs.GRAY, lw=0.8)
    m = P + 0.7 * rho0 * N
    ax.text(m[0] - 0.12, m[1] - 0.05, r'$\rho$', fontsize=10, color=fs.GRAY, ha='right')
    ax.text(C[0], C[1] + 0.1, '곡률 중심', fontsize=8, color=fs.GRAY, ha='center', va='bottom')
    ax.text(C[0] - rho0 * 0.7, C[1] + rho0 * 0.8, '곡률원', fontsize=8, color=fs.GRAY, ha='right')
    at, an = 0.9, 0.8
    fs.vec(ax, P, at * T, color=fs.ACC, lw=1.1, ls='--', ms=8)
    fs.vec(ax, P, an * N, color=fs.ACC, lw=1.1, ls='--', ms=8)
    fs.vec(ax, P, at * T + an * N, color=fs.ACC, lw=1.9)
    q1, q2, q3 = P + at * T, P + an * N, P + at * T + an * N
    ax.plot([q1[0], q3[0]], [q1[1], q3[1]], color=fs.ACC, lw=0.5, ls=':')
    ax.plot([q2[0], q3[0]], [q2[1], q3[1]], color=fs.ACC, lw=0.5, ls=':')
    ax.text(q3[0] + 0.08, q3[1] + 0.02, r'$\vec a$', color=fs.ACC, fontsize=11)
    ax.text(q1[0] + 0.08, q1[1] - 0.12, r'$a_t\hat T$', color=fs.ACC, fontsize=9, va='top')
    q = P + 0.55 * an * N - 0.12 * T
    ax.text(q[0], q[1], r'$a_n\hat N$', color=fs.ACC, fontsize=9, ha='right', va='center')
    fs.dot(ax, P, r=0.05)
    ax.text(P[0] + 0.1, P[1] - 0.15, 'P', fontsize=9, va='top')
    ax.text(xs[-1] - 0.1, ys[-1] + 0.12, '궤적', fontsize=9, ha='right')
    fs.save(fig, __file__, 'fig04_08')


# ---------- 그림 4.9 예제 4.6 ----------
def fig09():
    fig, ax = fs.canvas(4.2, 3.3, xlim=(-2.9, 8.0), ylim=(-3.0, 6.6))
    t = np.linspace(0, 1.62, 300)
    x, y = traj41(t)
    ax.plot(x, y, color=fs.BLACK, lw=1.5)
    P = np.array([3.0, -2.0])
    v = np.array([6.0, 2.0]); a = np.array([6.0, 12.0])
    vn = np.hypot(*v); T = v / vn; N = np.array([-T[1], T[0]])
    at = a @ T; an = abs(v[0] * a[1] - v[1] * a[0]) / vn; rho = vn ** 3 / abs(v[0] * a[1] - v[1] * a[0])
    C = P + rho * N
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(C[0] + rho * np.cos(th), C[1] + rho * np.sin(th), color=fs.GRAY, lw=0.8, ls='--')
    fs.dot(ax, C, r=0.07, color=fs.GRAY)
    ax.plot([P[0], C[0]], [P[1], C[1]], color=fs.GRAY, lw=0.8)
    m = P + 0.7 * (C - P)
    ax.text(m[0] - 0.3, m[1], r'$\rho = 4.2$ m', fontsize=9, color=fs.GRAY, ha='right')
    s = 0.17
    fs.vec(ax, P, s * at * T, color=fs.ACC, lw=1.1, ls='--', ms=8)
    fs.vec(ax, P, s * an * N, color=fs.ACC, lw=1.1, ls='--', ms=8)
    fs.vec(ax, P, s * a, color=fs.ACC, lw=1.8)
    q = P + s * at * T
    ax.text(q[0] + 0.1, q[1] - 0.25, r'$a_t = 9.5\ \mathrm{m/s^2}$', color=fs.ACC, fontsize=8.5, va='top')
    ax.annotate(r'$a_n = 9.5\ \mathrm{m/s^2}$', xy=tuple(P + 0.6 * s * an * N), xytext=tuple(P + 1.0 * s * an * N - 1.4 * T),
                color=fs.ACC, fontsize=8.5, ha='right', va='center', arrowprops=dict(arrowstyle='-', color=fs.ACC, lw=0.5))
    q = P + s * a
    ax.text(q[0] + 0.15, q[1] + 0.1, r'$\vec a$', color=fs.ACC, fontsize=11)
    fs.vec(ax, P, 0.3 * v, color=fs.VEL, lw=1.6)
    ax.text(P[0] + 0.3 * v[0] + 0.15, P[1] + 0.3 * v[1] - 0.1, r'$\vec v$', color=fs.VEL, fontsize=11)
    fs.dot(ax, P, r=0.08)
    ax.text(P[0] + 0.1, P[1] - 0.5, r'$t = 1.0$ s, $(3.0, -2.0)$ m', fontsize=8, va='top')
    ax.text(x[-1] - 0.2, y[-1] + 0.4, '궤적', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig04_09')


# ---------- 그림 4.10 극좌표 단위벡터 ----------
def fig10():
    fig, ax = fs.canvas(3.2, 2.6, xlim=(-0.4, 4.0), ylim=(-0.4, 3.2))
    axes2d(ax, (0, 0), 3.8, 3.0)
    th = np.radians(35); r = 3.0
    P = r * np.array([np.cos(th), np.sin(th)])
    ax.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=1.0)
    th2 = np.linspace(0, np.radians(80), 100)
    ax.plot(r * np.cos(th2), r * np.sin(th2), color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, (0, 0), 0.6, 0, 35, r'$\theta$', fontsize=10, tr=0.85)
    ax.text(1.0, 1.0, r'$r$', fontsize=10)
    rh = np.array([np.cos(th), np.sin(th)]); thh = np.array([-np.sin(th), np.cos(th)])
    fs.vec(ax, P, 0.8 * rh, lw=1.6)
    fs.vec(ax, P, 0.8 * thh, lw=1.6)
    ax.text(P[0] + 0.85 * rh[0] + 0.05, P[1] + 0.85 * rh[1] - 0.05, r'$\hat r$', fontsize=11)
    ax.text(P[0] + 0.8 * thh[0] - 0.1, P[1] + 0.8 * thh[1] + 0.12, r'$\hat\theta$', fontsize=11)
    fs.dot(ax, P, r=0.05)
    # 다른 위치의 단위벡터
    th3 = np.radians(62); Q = r * np.array([np.cos(th3), np.sin(th3)])
    rh3 = np.array([np.cos(th3), np.sin(th3)]); thh3 = np.array([-np.sin(th3), np.cos(th3)])
    fs.vec(ax, Q, 0.55 * rh3, lw=1.0, color=fs.GRAY, ms=8)
    fs.vec(ax, Q, 0.55 * thh3, lw=1.0, color=fs.GRAY, ms=8)
    fs.dot(ax, Q, r=0.04, color=fs.GRAY)
    ax.text(-0.25, -0.3, 'O', fontsize=9)
    fs.save(fig, __file__, 'fig04_10')


# ---------- 그림 4.11 상대 위치 ----------
def fig11():
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-0.5, 6.0), ylim=(-0.6, 3.8))
    axes2d(ax, (0, 0), 2.0, 1.5, xlab=r'$x$', ylab=r'$y$')
    ax.text(-0.35, -0.4, '기준틀 $A$', fontsize=9)
    B = np.array([3.2, 0.7])
    fs.arrow(ax, tuple(B), (B[0] + 1.6, B[1]), lw=0.9, ms=9, color=fs.ORANGE)
    fs.arrow(ax, tuple(B), (B[0], B[1] + 0.95), lw=0.9, ms=9, color=fs.ORANGE)
    ax.text(B[0] + 1.65, B[1], r"$x'$", fontsize=10, va='center', color=fs.ORANGE)
    ax.text(B[0] - 0.05, B[1] + 0.95, r"$y'$", fontsize=10, ha='right', va='bottom', color=fs.ORANGE)
    ax.text(B[0] + 0.1, B[1] - 0.35, '기준틀 $B$', fontsize=9, color=fs.ORANGE)
    fs.vec(ax, (B[0] + 0.3, B[1] - 0.6), (1.0, 0), color=fs.VEL, lw=1.3, ms=9)
    ax.text(B[0] + 1.4, B[1] - 0.6, r'$\vec v_{B/A}$', color=fs.VEL, fontsize=9, va='center')
    P = np.array([4.7, 3.3])
    fs.dot(ax, P, r=0.07)
    ax.text(P[0] + 0.15, P[1] + 0.1, r'$P$', fontsize=11)
    fs.arrow(ax, (0, 0), tuple(B), lw=1.4, color=fs.ORANGE)
    fs.arrow(ax, tuple(B), tuple(P), lw=1.4)
    fs.arrow(ax, (0, 0), tuple(P), lw=1.4)
    ax.text(1.5, 0.62, r'$\vec r_{B/A}$', fontsize=10, color=fs.ORANGE, ha='center')
    ax.text(4.1, 1.8, r'$\vec r_{P/B}$', fontsize=10)
    ax.text(1.9, 1.9, r'$\vec r_{P/A}$', fontsize=10, ha='right')
    fs.save(fig, __file__, 'fig04_11')


# ---------- 그림 4.12 예제 4.7 강 건너기 ----------
def fig12():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.9))
    W = 120.0
    for ax, case in zip(axs, ('가', '나')):
        ax.axis('off'); ax.set_aspect('equal')
        ax.set_xlim(-32, 100); ax.set_ylim(-30, 150)
        ax.add_patch(Rectangle((-32, 0), 132, W, fc='#e3eef8', ec='none', zorder=0))
        ax.plot([-32, 100], [0, 0], color=fs.BLACK, lw=1.2); ax.plot([-32, 100], [W, W], color=fs.BLACK, lw=1.2)
        for yy in (30, 90):
            fs.arrow(ax, (62, yy), (87, yy), color=fs.GRAY, lw=0.9, ms=8)
        ax.text(74, 96, '물살', fontsize=8, color=fs.GRAY, ha='center')
        ax.text(74, 36, r'$1.5$ m/s', fontsize=7.5, color=fs.GRAY, ha='center')
        sc = 18
        O = np.array([0.0, 0.0])
        if case == '가':
            vbw = np.array([0, 2.5]); vbg = np.array([1.5, 2.5]); land = np.array([72.0, W])
        else:
            phi = np.arcsin(1.5 / 2.5)
            vbw = np.array([-2.5 * np.sin(phi), 2.5 * np.cos(phi)]); vbg = np.array([0, 2.0]); land = np.array([0.0, W])
        ax.plot([O[0], land[0]], [O[1], land[1]], color=fs.BLACK, lw=0.8, ls='--')
        fs.dot(ax, O, r=2.0); fs.dot(ax, land, r=2.0)
        fs.vec(ax, O, sc * vbw, color=fs.VEL, lw=1.6)
        fs.vec(ax, O + sc * vbw, sc * np.array([1.5, 0]), color=fs.GRAY, lw=1.4)
        fs.vec(ax, O, sc * vbg, color=fs.BLACK, lw=1.8)
        if case == '가':
            ksub(ax, -3, 24, r'$\vec v$', '배/물', color=fs.VEL, size=9, ha='right')
            ksub(ax, 14, 53, r'$\vec v$', '물/땅', color=fs.GRAY, size=9, ha='center')
            ksub(ax, 28, 24, r'$\vec v$', '배/땅', size=9)
            ax.text(72, W + 6, '도착(72 m 하류)', fontsize=7.5, ha='center')
            ax.text(-30, 140, '(가) 뱃머리를 수직으로: 48 s', fontsize=8)
            fs.arrow(ax, (72, -24), (90, -24), lw=0.8, ms=7)
            fs.arrow(ax, (72, -24), (72, -8), lw=0.8, ms=7)
            ax.text(92, -24, r'$+x$', fontsize=8, va='center'); ax.text(75, -8, r'$+y$', fontsize=8, va='center')
        else:
            ksub(ax, -24, 24, r'$\vec v$', '배/물', color=fs.VEL, size=9, ha='right')
            ksub(ax, -12, 46, r'$\vec v$', '물/땅', color=fs.GRAY, size=9, ha='right')
            ksub(ax, 4, 18, r'$\vec v$', '배/땅', size=9)
            fs.angle_arc(ax, O, 20, 90, 90 + np.degrees(phi), None)
            ax.text(-4, 25, r'$\phi$', fontsize=9, ha='center')
            ax.text(0, W + 6, '도착(정면)', fontsize=7.5, ha='center')
            ax.text(-30, 140, '(나) 상류 쪽으로 $\\phi = 36.9^\\circ$: 60 s', fontsize=8)
        ax.text(-30, -14, '출발', fontsize=7.5)
    fig.tight_layout(w_pad=0.3)
    fs.save(fig, __file__, 'fig04_12')


# ---------- 그림 4.13 비의 상대 속도 ----------
def fig13():
    fig, ax = fs.canvas(3.6, 2.4, xlim=(-3.4, 1.9), ylim=(-1.9, 1.3))
    s = 0.17
    O = np.array([0.0, 0.8])
    vr = np.array([0, -8.0]) * s; vc = np.array([15.0, 0]) * s
    fs.vec(ax, O, vr, color=fs.VEL, lw=1.7)
    fs.vec(ax, O + vr, -vc, color=fs.ORANGE, lw=1.5, ls='--')
    fs.vec(ax, O, vr - vc, color=fs.BLACK, lw=1.9)
    ksub(ax, O[0] + 0.12, O[1] + vr[1] / 2 + 0.12, r'$\vec v$', '비/땅', color=fs.VEL, size=9)
    ax.text(O[0] + 0.12, O[1] + vr[1] / 2 - 0.2, '8.0 m/s', color=fs.VEL, fontsize=8)
    ksub(ax, O[0] - vc[0] / 2, O[1] + vr[1] - 0.25, r'$-\vec v$', '차/땅', color=fs.ORANGE, size=9, ha='center')
    ax.text(O[0] - vc[0] / 2, O[1] + vr[1] - 0.55, '15 m/s', color=fs.ORANGE, fontsize=8, ha='center')
    ksub(ax, -1.75, 0.45, r'$\vec v$', '비/차', size=9, ha='right')
    ax.text(-1.75, 0.15, '17 m/s', fontsize=8, ha='right')
    ax.plot([O[0], O[0]], [O[1], O[1] + 0.35], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, O, 0.55, 270 - np.degrees(np.arctan(15 / 8)), 270, None)
    ax.text(O[0] - 0.3, O[1] - 0.75, r'$62^\circ$', fontsize=8, ha='center')
    # 차의 운동 방향
    fs.vec(ax, (0.5, 1.15), (1.0, 0), color=fs.ORANGE, lw=1.2, ms=8)
    ax.text(1.0, 1.0, '차의 진행 방향', fontsize=7.5, color=fs.ORANGE, ha='center', va='top')
    fs.save(fig, __file__, 'fig04_13')


# ---------- 그림 4.14 크랭크-슬라이더 ----------
def fig14():
    fig, ax = fs.canvas(4.4, 2.0, xlim=(-1.3, 6.4), ylim=(-1.4, 1.6))
    r, l, th = 1.0, 3.6, np.radians(50)
    C = np.array([r * np.cos(th), r * np.sin(th)])
    xp = r * np.cos(th) + np.sqrt(l ** 2 - r ** 2 * np.sin(th) ** 2)
    P = np.array([xp, 0.0])
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r * np.cos(tt), r * np.sin(tt), color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([-1.2, 6.2], [0, 0], color=fs.GRAY, lw=0.5, ls='-.')
    ax.plot([0, C[0]], [0, C[1]], color=fs.BLACK, lw=3, solid_capstyle='round')
    ax.plot([C[0], P[0]], [C[1], P[1]], color=fs.VEL, lw=3, solid_capstyle='round')
    ax.add_patch(Rectangle((P[0] - 0.35, -0.3), 1.2, 0.6, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=4))
    ax.plot([P[0] - 0.6, 6.2], [0.38, 0.38], color=fs.BLACK, lw=1.0)
    ax.plot([P[0] - 0.6, 6.2], [-0.38, -0.38], color=fs.BLACK, lw=1.0)
    for q in ((0, 0), tuple(C), tuple(P)):
        ax.add_patch(Circle(q, 0.07, fc='white', ec=fs.BLACK, lw=1.0, zorder=6))
    ax.text(P[0] + 0.25, 0.0, '피스톤', fontsize=8, va='center', zorder=7)
    fs.angle_arc(ax, (0, 0), 0.4, 0, 50, r'$\theta$', fontsize=10, tr=0.6)
    ax.text(C[0] / 2 - 0.25, C[1] / 2 + 0.1, r'$r$', fontsize=10)
    ax.text((C[0] + P[0]) / 2, (C[1] + P[1]) / 2 + 0.15, r'$\ell$', fontsize=11, color=fs.VEL)
    fs.dim(ax, (0, 0), (P[0], 0), r'$x(\theta)$', off=-0.85, fontsize=9)
    ax.text(-0.35, 0.2, '크랭크 축', fontsize=7.5, ha='right')
    fs.save(fig, __file__, 'fig04_14')


# ---------- 그림 4.15 안전 포물선 ----------
def fig15():
    fig, ax = fs.plot_axes(4.2, 2.5)
    v0 = 1.0; gg = 1.0  # 무차원: 길이 단위 v0^2/g
    for deg in range(10, 90, 10):
        th = np.radians(deg)
        tf = 2 * np.sin(th)
        t = np.linspace(0, tf, 200)
        ax.plot(np.cos(th) * t, np.sin(th) * t - 0.5 * t ** 2, color=fs.VEL, lw=0.8, alpha=0.75)
    x = np.linspace(0, 1.0, 200)
    ax.plot(x, 0.5 - 0.5 * x ** 2, color=fs.FORCE, lw=1.8, ls='--')
    ax.text(0.62, 0.42, r'$y = \frac{v_0^2}{2g} - \frac{g}{2v_0^2}x^2$', color=fs.FORCE, fontsize=9)
    ax.set_xlim(0, 1.08); ax.set_ylim(0, 0.6)
    ax.set_aspect('equal')
    ax.set_xticks([0, 0.5, 1.0]); ax.set_xticklabels(['0', r'$\frac{v_0^2}{2g}$', r'$\frac{v_0^2}{g}$'])
    ax.set_yticks([0, 0.5]); ax.set_yticklabels(['0', r'$\frac{v_0^2}{2g}$'])
    ax.set_xlabel(r'$x$', labelpad=0); ax.set_ylabel(r'$y$')
    fs.save(fig, __file__, 'fig04_15')


# ---------- 그림 4.16 비탈 위로 던지기 ----------
def fig16():
    fig, ax = fs.canvas(4.0, 2.5, xlim=(-0.4, 6.4), ylim=(-0.4, 3.8))
    al = np.radians(30); th = np.radians(60); v0 = 1.0
    L = 2 * v0 ** 2 * np.cos(th) * np.sin(th - al) / (g * np.cos(al) ** 2)
    S = 5.8 / (L * np.cos(al)) * 0.8     # 그림 축척
    ax.add_patch(Polygon([(0, 0), (6.2, 0), (6.2, 6.2 * np.tan(al))], fc='#f2f2f2', ec=fs.BLACK, lw=1.2, zorder=1))
    tf = 2 * v0 * np.sin(th - al) / (g * np.cos(al))
    t = np.linspace(0, tf, 200)
    x = S * v0 * np.cos(th) * t; y = S * (v0 * np.sin(th) * t - 0.5 * g * t ** 2)
    ax.plot(x, y, color=fs.BLACK, lw=1.4)
    fs.vec(ax, (0, 0), (1.2 * np.cos(th), 1.2 * np.sin(th)), color=fs.VEL, lw=1.6)
    ax.text(1.2 * np.cos(th) - 0.1, 1.2 * np.sin(th) + 0.1, r'$\vec v_0$', color=fs.VEL, fontsize=10, ha='right')
    fs.angle_arc(ax, (0, 0), 0.75, 0, 60, None)
    ax.text(0.95 * np.cos(np.radians(45)), 0.95 * np.sin(np.radians(45)) + 0.05, r'$\theta_0$', fontsize=9, ha='center', va='center')
    fs.angle_arc(ax, (0, 0), 1.9, 0, 30, None)
    ax.text(2.1 * np.cos(np.radians(13)), 2.1 * np.sin(np.radians(13)), r'$\alpha$', fontsize=10, va='center')
    fs.dot(ax, (x[-1], y[-1]), r=0.06)
    fs.dim(ax, (0, 0), (x[-1], y[-1]), r'$L$', off=-0.32, fontsize=10)
    fs.save(fig, __file__, 'fig04_16')


# ---------- 그림 4.17 사이클로이드 ----------
def fig17():
    fig, ax = fs.canvas(5.0, 1.9, xlim=(-0.4, 13.4), ylim=(-0.5, 2.9))
    R = 1.0
    fs.ground(ax, -0.3, 13.2, 0, depth=0.2, n=60)
    s = np.linspace(0, 4 * np.pi, 500)
    ax.plot(R * (s - np.sin(s)), R * (1 - np.cos(s)), color=fs.VEL, lw=1.4)
    phi = 2.2
    Cc = np.array([R * phi, R])
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(Cc[0] + R * np.cos(tt), Cc[1] + R * np.sin(tt), color=fs.BLACK, lw=1.1)
    P = np.array([R * (phi - np.sin(phi)), R * (1 - np.cos(phi))])
    ax.plot([Cc[0], P[0]], [Cc[1], P[1]], color=fs.BLACK, lw=1.0)
    fs.dot(ax, Cc, r=0.05); fs.dot(ax, P, r=0.08, color=fs.FORCE)
    m = (Cc + P) / 2
    ax.text(m[0] + 0.05, m[1] + 0.12, r'$R$', fontsize=9)
    fs.vec(ax, (Cc[0], Cc[1] + R + 0.3), (1.2, 0), color=fs.GRAY, lw=1.0, ms=8)
    ax.text(Cc[0] + 1.3, Cc[1] + R + 0.3, r'$R\omega$', color=fs.GRAY, fontsize=8, va='center')
    # 시계 방향 회전(오른쪽으로 굴러감)
    ax.add_patch(Arc(Cc, 1.0, 1.0, theta1=-60, theta2=40, color=fs.BLACK, lw=0.8))
    a0 = np.radians(-60); a1 = np.radians(-68)
    fs.arrow(ax, (Cc[0] + 0.5 * np.cos(a0), Cc[1] + 0.5 * np.sin(a0)),
             (Cc[0] + 0.5 * np.cos(a1), Cc[1] + 0.5 * np.sin(a1)), ms=7, lw=0.8)
    ax.text(Cc[0] + 0.62, Cc[1] - 0.05, r'$\omega$', fontsize=9)
    fs.dot(ax, (3 * np.pi, 2.0), r=0.05, color=fs.VEL)
    ax.text(3 * np.pi + 0.15, 2.1, '꼭대기\n($\\rho = 4R$)', fontsize=8, va='bottom')
    fs.dot(ax, (2 * np.pi, 0), r=0.05, color=fs.VEL)
    ax.text(2 * np.pi, 0.35, '$v = 0$', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig04_17')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13,
              fig14, fig15, fig16, fig17):
        f()
