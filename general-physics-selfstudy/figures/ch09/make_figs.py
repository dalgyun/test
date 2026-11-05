import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
"""9장 질량중심과 선운동량 그림."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Ellipse

F = __file__
D2R = np.pi / 180


def u(ang):
    return np.array([np.cos(ang * D2R), np.sin(ang * D2R)])


def ball(ax, p, r, text=None, fc=fs.LIGHT, fontsize=10, ls='-', ec=fs.BLACK):
    ax.add_patch(Circle(p, r, fc=fc, ec=ec, lw=1.1, ls=ls, zorder=5))
    if text:
        ax.text(p[0], p[1], text, ha='center', va='center', fontsize=fontsize, zorder=6)


def dimh(ax, x0, x1, y, text, color=fs.BLACK, fontsize=9.5, dy=0.18):
    ax.annotate('', xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color=color, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + dy, text, ha='center', va='center', fontsize=fontsize, color=color)


# ---------------------------------------------------------------- 그림 9.1 입자계의 질량중심
def fig01():
    fig, ax = fs.canvas(3.6, 2.8, xlim=(-0.4, 4.4), ylim=(-0.4, 3.2))
    O = np.array([0.0, 0.0])
    pts = [(np.array([1.0, 0.6]), 1, r'$m_1$'), (np.array([3.6, 1.0]), 2, r'$m_2$'), (np.array([1.8, 2.6]), 3, r'$m_3$')]
    M = sum(m for _, m, _ in pts)
    cm = sum(p * m for p, m, _ in pts) / M
    for k, (p, m, t) in enumerate(pts):
        fs.arrow(ax, O, p, color=fs.GRAY, lw=1.0, ms=9)
        ball(ax, p, 0.09 + 0.04 * m)
        ax.text(p[0] + 0.25, p[1] + 0.18, t, fontsize=10)
        lab = r'$\vec{r}_%d$' % (k + 1)
        sg = -1 if k == 0 else 1
        ax.text(*(p * 0.55 + sg * np.array([-p[1], p[0]]) / np.linalg.norm(p) * 0.18), lab, fontsize=10, color=fs.GRAY,
                ha='center', va='center')
    fs.arrow(ax, O, cm, color=fs.BLACK, lw=1.8)
    ax.plot(*cm, marker='o', ms=7, mfc='white', mec=fs.BLACK, mew=1.5, zorder=7)
    ax.plot(*cm, marker='+', ms=7, color=fs.BLACK, mew=1.2, zorder=8)
    ax.text(cm[0] + 0.15, cm[1] - 0.25, r'$\vec{r}_{\mathrm{cm}}$', fontsize=11)
    fs.dot(ax, O, r=0.05); ax.text(-0.15, -0.2, 'O', fontsize=9)
    fs.save(fig, F, 'fig09_01')


# ---------------------------------------------------------------- 그림 9.2 예제 9.1 반원판
def fig02():
    R = 2.0
    fig, ax = fs.canvas(3.4, 2.1, xlim=(-2.5, 2.7), ylim=(-0.35, 2.5))
    th = np.linspace(0, np.pi, 200)
    ax.add_patch(Polygon(np.c_[R * np.cos(th), R * np.sin(th)], closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.3))
    y0, dy = 1.1, 0.14
    hw = np.sqrt(R ** 2 - y0 ** 2)
    ax.add_patch(Rectangle((-hw, y0), 2 * hw, dy, fc=fs.SURF, ec=fs.BLACK, lw=0.8, zorder=3))
    fs.arrow(ax, (-2.4, 0), (2.6, 0), lw=0.9, ms=8); ax.text(2.6, -0.2, r'$x$', fontsize=10)
    fs.arrow(ax, (0, 0), (0, 2.45), lw=0.9, ms=8); ax.text(0.12, 2.4, r'$y$', fontsize=10)
    ax.annotate('', xy=(-hw, y0 + dy + 0.12), xytext=(hw, y0 + dy + 0.12),
                arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK, shrinkA=0, shrinkB=0))
    ax.text(0.62, y0 + dy + 0.38, r'$2\sqrt{R^2-y^2}$', fontsize=9.5, ha='center')
    ax.annotate('', xy=(hw + 0.35, y0), xytext=(hw + 0.35, y0 + dy),
                arrowprops=dict(arrowstyle='-', lw=0.6, color=fs.BLACK))
    ax.text(hw + 0.45, y0 + dy / 2, r'$dy$', fontsize=9.5, va='center')
    ax.plot([hw, hw + 0.4], [y0, y0], color=fs.GRAY, lw=0.5); ax.plot([hw, hw + 0.4], [y0 + dy, y0 + dy], color=fs.GRAY, lw=0.5)
    ax.annotate('', xy=(-1.75, 0), xytext=(-1.75, y0), arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK,
                                                                        shrinkA=0, shrinkB=0))
    ax.text(-1.6, 0.5, r'$y$', fontsize=10)
    ycm = 4 * R / (3 * np.pi)
    ax.plot(0, ycm, marker='o', ms=6, mfc='white', mec=fs.FORCE, mew=1.5, zorder=7)
    ax.text(0.15, ycm - 0.15, r'$y_{\mathrm{cm}}=\frac{4R}{3\pi}$', fontsize=9.5, color=fs.FORCE, va='center')
    ax.plot([0, R * np.cos(2.6)], [0, R * np.sin(2.6)], color=fs.GRAY, lw=0.8)
    ax.text(-0.75, 0.2, r'$R$', fontsize=10, color=fs.GRAY)
    fs.save(fig, F, 'fig09_02')


# ---------------------------------------------------------------- 그림 9.3 내력과 외력
def fig03():
    fig, ax = fs.canvas(3.8, 2.4, xlim=(-0.3, 5.0), ylim=(-0.4, 2.9))
    ax.add_patch(Ellipse((2.3, 1.25), 3.6, 2.2, fc='none', ec=fs.GRAY, ls='--', lw=1.0))
    ax.text(0.65, 2.45, '계', fontsize=9, color=fs.GRAY)
    p1, p2 = np.array([1.3, 1.0]), np.array([3.3, 1.6])
    d = (p2 - p1) / np.linalg.norm(p2 - p1)
    ball(ax, p1, 0.16, r'$i$', fontsize=9); ball(ax, p2, 0.16, r'$j$', fontsize=9)
    fs.vec(ax, p1 + d * 0.16, d * 0.75, color=fs.FORCE, lw=1.6)
    ax.text(*(p1 + d * 0.75 + np.array([-0.1, 0.33])), r'$\vec{F}_{ij}$', fontsize=10, color=fs.FORCE)
    fs.vec(ax, p2 - d * 0.16, -d * 0.75, color=fs.FORCE, lw=1.6)
    ax.text(*(p2 - d * 0.75 + np.array([0.1, -0.35])), r'$\vec{F}_{ji}$', fontsize=10, color=fs.FORCE)
    fs.vec(ax, p1 - np.array([0, 0.16]), (-0.3, -1.0), color=fs.ACC, lw=1.6)
    ax.text(p1[0] - 0.85, p1[1] - 0.95, r'$\vec{F}_i^{\mathrm{ext}}$', fontsize=10, color=fs.ACC)
    fs.vec(ax, p2 + np.array([0.16, 0]), (1.3, 0.3), color=fs.ACC, lw=1.6)
    ax.text(p2[0] + 1.25, p2[1] + 0.45, r'$\vec{F}_j^{\mathrm{ext}}$', fontsize=10, color=fs.ACC)
    ax.text(2.3, -0.25, r'$\vec{F}_{ij}=-\vec{F}_{ji}$ (내력은 상쇄)', fontsize=9, ha='center', color=fs.FORCE)
    fs.save(fig, F, 'fig09_03')


# ---------------------------------------------------------------- 그림 9.4 예제 9.2 폭발하는 포탄
def fig04():
    R, H = 4.0, 1.6
    fig, ax = fs.canvas(4.6, 2.2, xlim=(-0.3, 6.6), ylim=(-0.75, 2.2))
    fs.ground(ax, -0.3, 6.6, 0)
    x = np.linspace(0, R, 200)
    y = 4 * H * x * (R - x) / R ** 2
    ax.plot(x[x <= R / 2], y[x <= R / 2], color=fs.BLACK, lw=1.6)
    ax.plot(x[x >= R / 2], y[x >= R / 2], color=fs.GRAY, lw=1.2, ls='--')
    ax.plot([R / 2, R / 2], [H, 0], color=fs.VEL, lw=1.6)
    x2 = np.linspace(R / 2, 1.5 * R, 200)
    y2 = H * (1 - ((x2 - R / 2) / R) ** 2)
    ax.plot(x2, y2, color=fs.FORCE, lw=1.6)
    for xx, yy, c in ((R / 2, H / 2, fs.VEL), ):
        ax.add_patch(FancyArrowPatch((xx, yy + 0.05), (xx, yy - 0.05), arrowstyle='-|>', mutation_scale=10, color=c, lw=0))
    i = 110
    ax.add_patch(FancyArrowPatch((x2[i], y2[i]), (x2[i + 2], y2[i + 2]), arrowstyle='-|>', mutation_scale=10,
                                 color=fs.FORCE, lw=0))
    ax.add_patch(FancyArrowPatch((x[50], y[50]), (x[52], y[52]), arrowstyle='-|>', mutation_scale=10,
                                 color=fs.BLACK, lw=0))
    ax.plot(R / 2, H, marker='*', ms=13, color=fs.ORANGE, zorder=6)
    ax.text(R / 2, H + 0.25, '폭발', fontsize=9, ha='center')
    for xx, t, c in ((0, '0', fs.BLACK), (R / 2, r'$R/2$', fs.VEL), (R, r'$R$', fs.GRAY), (1.5 * R, r'$3R/2$', fs.FORCE)):
        ax.plot(xx, 0, 'o', ms=4, color=c, zorder=6)
        ax.text(xx, -0.45, t, fontsize=10, ha='center', color=c)
    ax.text(R + 0.15, 0.55, '질량중심', fontsize=8.5, color=fs.GRAY)
    ax.text(R / 2 - 0.12, 0.6, '조각 1', fontsize=8.5, color=fs.VEL, ha='right')
    ax.text(5.1, 1.0, '조각 2', fontsize=8.5, color=fs.FORCE)
    fs.save(fig, F, 'fig09_04')


# ---------------------------------------------------------------- 그림 9.5 예제 9.3 보트 위의 사람
def boat(ax, x0, y, L=4.0):
    ax.add_patch(Polygon([(x0, y + 0.35), (x0 + L, y + 0.35), (x0 + L - 0.25, y - 0.1), (x0 + 0.25, y - 0.1)],
                         closed=True, fc='#d9c7a7', ec=fs.BLACK, lw=1.1, zorder=3))


def person(ax, x, y):
    ax.plot([x, x], [y + 0.35, y + 0.95], color=fs.BLACK, lw=1.6, zorder=4)
    ax.add_patch(Circle((x, y + 1.08), 0.13, fc='white', ec=fs.BLACK, lw=1.2, zorder=4))


def fig05():
    fig, ax = fs.canvas(4.4, 3.2, xlim=(-2.0, 5.0), ylim=(-1.4, 3.6))
    L = 4.0
    db = -L * 70 / 210
    xcm = (70 * 0 + 140 * L / 2) / 210
    for y, x0, xp, t in ((2.0, 0.0, 0.0, '처음'), (0.0, db, db + L, '나중')):
        ax.add_patch(Rectangle((-2.0, y - 0.6), 7.0, 0.55, fc='#e3eef8', ec='none', zorder=1))
        ax.plot([-2.0, 5.0], [y - 0.05, y - 0.05], color=fs.VEL, lw=0.8, zorder=2)
        boat(ax, x0, y, L)
        person(ax, xp, y)
        ax.text(-1.9, y + 0.9, t, fontsize=9)
    ax.plot([xcm, xcm], [-1.0, 3.5], color=fs.FORCE, ls='--', lw=1.0, zorder=5)
    ax.text(xcm + 0.08, 3.4, r'$x_{\mathrm{cm}}$ (변하지 않음)', fontsize=9, color=fs.FORCE, va='center')
    ax.plot([0, 0], [-0.9, 2.2], color=fs.GRAY, lw=0.6, ls=':')
    dimh(ax, db, 0, -0.85, r'보트 $1.3\ \mathrm{m}$', fontsize=9, dy=-0.25)
    dimh(ax, 0, db + L, -0.85, r'사람 $2.7\ \mathrm{m}$', fontsize=9, dy=-0.25)
    dimh(ax, 0, L, 2.7, r'$4.0\ \mathrm{m}$', fontsize=9, dy=0.3)
    fs.save(fig, F, 'fig09_05')


# ---------------------------------------------------------------- 그림 9.6 예제 9.4 충격력
def fig06():
    J = 0.058 * 55
    tau = 5.0e-3
    Fav = J / tau
    Fmax = np.pi * J / (2 * tau)
    t = np.linspace(0, tau, 200)
    Ft = Fmax * np.sin(np.pi * t / tau)
    fig, ax = fs.plot_axes(3.8, 2.6)
    ax.fill_between(t * 1e3, Ft, color=fs.FORCE, alpha=0.2, lw=0)
    ax.plot(t * 1e3, Ft, color=fs.FORCE, lw=2)
    ax.plot([0, 0, 5, 5], [0, Fav, Fav, 0], color=fs.BLACK, lw=1.2, ls='--')
    ax.text(5.15, Fav, r'$F_{\mathrm{avg}}=638\ \mathrm{N}$', fontsize=9, va='center')
    ax.text(2.5, Fmax + 40, r'$F_{\max}=1.0\times10^3\ \mathrm{N}$', fontsize=9, ha='center', color=fs.FORCE)
    ax.text(2.5, 250, r'넓이 $=J=3.19\ \mathrm{N\cdot s}$', fontsize=9, ha='center')
    ax.set_xlim(-0.3, 7.6); ax.set_ylim(0, 1200)
    ax.set_xlabel(r'$t$ (ms)'); ax.set_ylabel(r'$F$ (N)')
    fs.save(fig, F, 'fig09_06')


# ---------------------------------------------------------------- 그림 9.7 예제 9.5 탄도 진자
def fig07():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-0.6, 6.4), ylim=(-0.6, 3.6))
    fs.ceiling(ax, 1.0, 5.0, 3.4)
    Ls = 2.6
    # 처음 위치(점선)
    bx, by = 3.0, 3.4 - Ls
    for dx in (-0.35, 0.35):
        ax.plot([bx + dx, bx + dx], [3.4, by + 0.25], color=fs.GRAY, lw=0.8, ls='--')
    ax.add_patch(Rectangle((bx - 0.5, by - 0.25), 1.0, 0.5, fc='white', ec=fs.GRAY, ls='--', lw=1.0, zorder=3))
    # 올라간 위치
    phi = 30 * D2R
    h = Ls * (1 - np.cos(phi))
    cx, cy = bx + Ls * np.sin(phi), by + h
    for dx in (-0.35, 0.35):
        ax.plot([bx + dx, cx + dx], [3.4, cy + 0.25], color=fs.BLACK, lw=1.0)
    ax.add_patch(Rectangle((cx - 0.5, cy - 0.25), 1.0, 0.5, fc='#d9c7a7', ec=fs.BLACK, lw=1.1, zorder=4))
    ax.text(cx, cy, r'$M+m$', fontsize=8.5, ha='center', va='center', zorder=5)
    ax.plot([bx + 0.5, cx + 1.4], [by, by], color=fs.GRAY, lw=0.6, ls=':')
    ax.annotate('', xy=(cx + 1.2, by), xytext=(cx + 1.2, cy), arrowprops=dict(arrowstyle='<->', lw=0.8,
                                                                               color=fs.BLACK, shrinkA=0, shrinkB=0))
    ax.plot([cx + 0.5, cx + 1.4], [cy, cy], color=fs.GRAY, lw=0.6, ls=':')
    ax.text(cx + 1.3, (by + cy) / 2, r'$h$', fontsize=10, va='center')
    ax.text(bx, by - 0.45, r'$M$', fontsize=9.5, ha='center', color=fs.GRAY)
    # 총알
    ax.add_patch(Rectangle((0.2, by - 0.05), 0.3, 0.1, fc=fs.BLACK, ec=fs.BLACK, zorder=5))
    ax.text(0.35, by - 0.3, r'$m$', fontsize=9.5, ha='center')
    fs.arrow(ax, (0.6, by), (1.6, by), color=fs.VEL, lw=1.8)
    ax.text(1.1, by + 0.25, r'$v$', fontsize=11, color=fs.VEL, ha='center')
    fs.vec(ax, (bx + 0.55, by), (0.55, 0.0), color=fs.VEL, lw=1.4, ms=9)
    ax.text(bx + 0.85, by - 0.25, r'$V$', fontsize=10, color=fs.VEL, ha='center')
    fs.save(fig, F, 'fig09_07')


# ---------------------------------------------------------------- 그림 9.8 1차원 충돌 전후
def fig08():
    fig, ax = fs.canvas(4.4, 2.0, xlim=(-0.3, 6.3), ylim=(-0.5, 2.6))
    for y, t, v1, v2, l1, l2 in ((1.6, '충돌 전', 1.1, -0.5, r'$v_{1i}$', r'$v_{2i}$'),
                                 (0.0, '충돌 후', -0.4, 1.0, r'$v_{1f}$', r'$v_{2f}$')):
        ax.plot([-0.2, 6.2], [y - 0.32, y - 0.32], color=fs.BLACK, lw=1.0)
        x1, x2 = (1.4, 4.4) if y > 0 else (2.4, 3.9)
        ball(ax, (x1, y), 0.32, r'$m_1$', fontsize=9.5)
        ball(ax, (x2, y), 0.25, r'$m_2$', fontsize=8.5)
        for x, r, v, l in ((x1, 0.32, v1, l1), (x2, 0.25, v2, l2)):
            s = np.sign(v)
            fs.arrow(ax, (x + s * r, y), (x + s * r + v, y), color=fs.VEL, lw=1.8)
            ax.text(x + s * r + v / 2, y + 0.3, l, color=fs.VEL, fontsize=10, ha='center')
        ax.text(-0.2, y + 0.5, t, fontsize=9)
    fs.arrow(ax, (5.3, 2.35), (6.1, 2.35), lw=1.0, ms=8); ax.text(6.15, 2.35, r'$+x$', fontsize=9, va='center')
    fs.save(fig, F, 'fig09_08')


# ---------------------------------------------------------------- 그림 9.9 예제 9.6 같은 질량의 2차원 탄성 충돌
def fig09():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.4), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]; ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.7, 2.4); ax.set_ylim(-1.6, 1.5)
    s = 1.0          # 1 m/s 당 길이
    ax.plot([-2.6, 2.3], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    ball(ax, (-2.45, 0), 0.17, '1', fontsize=8)
    fs.arrow(ax, (-2.25, 0), (-2.25 + 2.0 * s, 0), color=fs.VEL, lw=1.8)
    ax.text(-1.25, 0.25, r'$2.0\ \mathrm{m/s}$', fontsize=9, color=fs.VEL, ha='center')
    ball(ax, (0.0, 0), 0.17, '2', fontsize=8, fc='white', ls='--', ec=fs.GRAY)
    v1, v2 = 2.0 * np.cos(30 * D2R), 2.0 * np.sin(30 * D2R)
    fs.vec(ax, (0, 0), v1 * u(30), color=fs.VEL, lw=1.8)
    fs.vec(ax, (0, 0), v2 * u(-60), color=fs.VEL, lw=1.8)
    ball(ax, v1 * u(30) + 0.22 * u(30), 0.17, '1', fontsize=8)
    ball(ax, v2 * u(-60) + 0.22 * u(-60), 0.17, '2', fontsize=8)
    fs.angle_arc(ax, (0, 0), 0.6, 0, 30, r'$30^{\circ}$', fontsize=8.5, tr=0.9)
    fs.angle_arc(ax, (0, 0), 0.5, -60, 0, r'$60^{\circ}$', fontsize=8.5, tr=0.82)
    ax.text(*(v1 * u(30) * 0.55 + np.array([-0.35, 0.3])), r'$v_{1f}$', fontsize=10, color=fs.VEL)
    ax.text(*(v2 * u(-60) * 0.6 + np.array([-0.4, -0.05])), r'$v_{2f}$', fontsize=10, color=fs.VEL)
    ax.text(0.0, -1.55, '(가) 충돌 전후', fontsize=9, ha='center')
    ax = axs[1]; ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-0.3, 2.4); ax.set_ylim(-1.6, 1.5)
    A = np.array([0.0, -0.5])
    B = A + v1 * u(30)
    C = A + np.array([2.0, 0.0])
    fs.arrow(ax, A, C, color=fs.VEL, lw=1.8)
    fs.arrow(ax, A, B, color=fs.VEL, lw=1.6)
    fs.arrow(ax, B, C, color=fs.VEL, lw=1.6)
    ax.text(1.0, -0.78, r'$\vec{v}_{1i}$', fontsize=10, ha='center', color=fs.VEL)
    ax.text(*((A + B) / 2 + np.array([-0.2, 0.2])), r'$\vec{v}_{1f}$', fontsize=10, ha='center', color=fs.VEL)
    ax.text(*((B + C) / 2 + np.array([0.3, 0.12])), r'$\vec{v}_{2f}$', fontsize=10, ha='center', color=fs.VEL)
    e1, e2 = -u(30) * 0.15, (C - B) / np.linalg.norm(C - B) * 0.15
    ax.plot([B[0] + e1[0], B[0] + e1[0] + e2[0], B[0] + e2[0]], [B[1] + e1[1], B[1] + e1[1] + e2[1], B[1] + e2[1]],
            color=fs.BLACK, lw=0.8)
    ax.text(1.0, -1.55, '(나) 속도 삼각형', fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, F, 'fig09_09')


# ---------------------------------------------------------------- 그림 9.10 충돌 매개변수
def fig10():
    D, b = 1.0, 0.5
    fig, ax = fs.canvas(4.0, 2.2, xlim=(-2.6, 2.0), ylim=(-1.15, 1.3))
    c2 = np.array([0.0, 0.0])
    c1 = np.array([-np.sqrt(D ** 2 - b ** 2), b])
    ax.plot([-2.6, 1.9], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    ax.plot([-2.6, c1[0]], [b, b], color=fs.GRAY, lw=0.8, ls='--')
    fs.arrow(ax, (-1.6, b + 0.62), (-1.0, b + 0.62), color=fs.VEL, lw=1.6)
    ax.text(-1.3, b + 0.82, r'$\vec{v}_1$', color=fs.VEL, fontsize=10, ha='center')
    ball(ax, c1, D / 2)
    ball(ax, c2, D / 2)
    ax.text(c1[0] - 0.62, c1[1] + 0.32, r'$m_1$', fontsize=10, ha='right')
    ax.text(c2[0] + 0.25, c2[1] - 0.62, r'$m_2$', fontsize=10)
    fs.dot(ax, c1, r=0.03); fs.dot(ax, c2, r=0.03)
    ax.annotate('', xy=(-2.45, 0), xytext=(-2.45, b), arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK,
                                                                       shrinkA=0, shrinkB=0))
    ax.text(-2.55, b / 2, r'$b$', fontsize=11, ha='right', va='center')
    n = (c2 - c1) / D
    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], color=fs.BLACK, lw=0.8, ls='--', zorder=6)
    fs.vec(ax, c2, n * 0.95, color=fs.FORCE, lw=1.8, zorder=7)
    ax.text(*(c2 + n * 1.05 + np.array([0.15, 0.0])), r'$\hat{n}$', fontsize=11, color=fs.FORCE)
    ax.text(*((c1 + c2) / 2 + np.array([0.5, 0.866]) * 0.16), r'$D$', fontsize=10, ha='center', va='center',
            bbox=dict(fc=fs.LIGHT, ec='none', pad=0.3), zorder=8)
    fs.save(fig, F, 'fig09_10')


# ---------------------------------------------------------------- 그림 9.11 로켓 방정식
def rocket(ax, x, y, L=1.4, H=0.45, text=None):
    ax.add_patch(Polygon([(x, y - H / 2), (x + L, y - H / 2), (x + L + 0.35, y), (x + L, y + H / 2), (x, y + H / 2)],
                         closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=4))
    ax.add_patch(Polygon([(x, y + H / 2), (x - 0.2, y + H / 2 + 0.15), (x + 0.25, y + H / 2)], closed=True,
                         fc=fs.GRAY, ec=fs.BLACK, lw=0.8, zorder=3))
    ax.add_patch(Polygon([(x, y - H / 2), (x - 0.2, y - H / 2 - 0.15), (x + 0.25, y - H / 2)], closed=True,
                         fc=fs.GRAY, ec=fs.BLACK, lw=0.8, zorder=3))
    if text:
        ax.text(x + L / 2 + 0.1, y, text, ha='center', va='center', fontsize=9.5, zorder=5)


def fig11():
    fig, ax = fs.canvas(4.4, 2.4, xlim=(-1.6, 5.4), ylim=(-0.6, 3.0))
    rocket(ax, 0.6, 2.2, text=r'$M$')
    fs.arrow(ax, (2.45, 2.2), (3.45, 2.2), color=fs.VEL, lw=1.8)
    ax.text(3.55, 2.2, r'$v$', color=fs.VEL, fontsize=11, va='center')
    ax.text(-1.5, 2.75, '(가) 시각 $t$', fontsize=9)
    rocket(ax, 1.4, 0.5, text=r'$M+dM$')
    fs.arrow(ax, (3.25, 0.5), (4.45, 0.5), color=fs.VEL, lw=1.8)
    ax.text(4.55, 0.5, r'$v+dv$', color=fs.VEL, fontsize=11, va='center')
    for k in range(7):
        ax.add_patch(Circle((0.85 - 0.18 * k + 0.05 * (k % 2), 0.5 + 0.12 * ((k % 3) - 1)), 0.07,
                            fc=fs.ORANGE, ec='none', alpha=0.8, zorder=3))
    ax.text(0.2, 0.0, r'기체 $-dM$', fontsize=9, ha='center')
    fs.arrow(ax, (-0.1, 0.9), (-0.9, 0.9), color=fs.VEL, lw=1.4)
    ax.text(0.0, 1.12, r'$v_{\mathrm{rel}}$ (로켓에 대해)', fontsize=9, color=fs.VEL, ha='center')
    ax.text(-1.5, 1.6, '(나) 시각 $t+dt$', fontsize=9)
    ax.text(5.3, -0.45, r'($v$, $v+dv$는 지면 기준)', fontsize=8, ha='right', color=fs.GRAY)
    fs.save(fig, F, 'fig09_11')


# ---------------------------------------------------------------- 그림 9.12 로켓 방정식 그래프
def fig12():
    r = np.linspace(1, 20, 400)
    fig, ax = fs.plot_axes(3.8, 2.6)
    ax.plot(r, np.log(r), color=fs.VEL, lw=2)
    ax.plot(5, np.log(5), 'o', color=fs.FORCE, ms=5)
    ax.plot([5, 5], [0, np.log(5)], color=fs.FORCE, lw=0.7, ls=':')
    ax.plot([1, 5], [np.log(5)] * 2, color=fs.FORCE, lw=0.7, ls=':')
    ax.text(5.5, np.log(5) - 0.25, r'예제 9.7: $M_i/M_f=5$, $\Delta v=1.61\,v_{\mathrm{rel}}$', fontsize=8.5,
            color=fs.FORCE)
    ax.set_xlim(1, 20); ax.set_ylim(0, 3.2)
    ax.set_xlabel(r'질량비 $M_i/M_f$'); ax.set_ylabel(r'$\Delta v/v_{\mathrm{rel}}$')
    ax.set_xticks([1, 5, 10, 15, 20])
    fs.save(fig, F, 'fig09_12')


# ---------------------------------------------------------------- 그림 9.13 연습문제 9 교차로 충돌
def car(ax, c, w, h, color, text):
    ax.add_patch(Rectangle((c[0] - w / 2, c[1] - h / 2), w, h, fc=color, ec=fs.BLACK, lw=1.0, zorder=4))
    ax.text(c[0], c[1], text, ha='center', va='center', fontsize=8, zorder=5)


def fig13():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-2.8, 2.4), ylim=(-2.8, 1.8))
    for s_ in (-0.6, 0.6):
        ax.plot([-2.8, -0.6], [s_, s_], color=fs.GRAY, lw=1.0); ax.plot([0.6, 2.4], [s_, s_], color=fs.GRAY, lw=1.0)
        ax.plot([s_, s_], [-2.8, -0.6], color=fs.GRAY, lw=1.0); ax.plot([s_, s_], [0.6, 1.8], color=fs.GRAY, lw=1.0)
    car(ax, (-1.8, -0.25), 0.8, 0.4, fs.LIGHT, r'$1500$ kg')
    fs.arrow(ax, (-1.35, -0.25), (-0.55, -0.25), color=fs.VEL, lw=1.8)
    ax.text(-1.8, 0.15, r'$20\ \mathrm{m/s}$', fontsize=9, color=fs.VEL, ha='center')
    car(ax, (0.25, -1.9), 0.4, 0.8, '#f3e2c7', '')
    ax.text(0.55, -1.9, r'$2000$ kg', fontsize=8, va='center', ha='left')
    fs.arrow(ax, (0.25, -1.45), (0.25, -0.75), color=fs.VEL, lw=1.8)
    ax.text(0.45, -1.15, r'$15\ \mathrm{m/s}$', fontsize=9, color=fs.VEL, ha='left')
    fs.arrow(ax, (1.4, 1.0), (1.4, 1.6), lw=1.0, ms=8); ax.text(1.4, 1.72, '북', fontsize=8.5, ha='center')
    fs.arrow(ax, (1.4, 1.0), (2.0, 1.0), lw=1.0, ms=8); ax.text(2.15, 1.0, '동', fontsize=8.5, va='center')
    fs.save(fig, F, 'fig09_13')


# ---------------------------------------------------------------- 그림 9.14 연습문제 16 질량중심 기준틀 작도
def fig14():
    m1, m2 = 2.0, 1.0
    M = m1 + m2
    V = m1 / M * 3.0
    up = m2 / M * 3.0
    fig, ax = fs.canvas(3.8, 2.2, xlim=(-0.3, 3.4), ylim=(-1.1, 1.3))
    O = np.array([0.0, 0.0]); C = np.array([V, 0.0])
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(C[0] + up * np.cos(th), up * np.sin(th), color=fs.GRAY, lw=1.0, ls='--')
    fs.arrow(ax, O, C, color=fs.BLACK, lw=1.8)
    ax.text(V / 2 - 0.35, -0.22, r'$\vec{V}$', fontsize=11, ha='center')
    a = 120
    P = C + up * u(a)
    fs.arrow(ax, C, P, color=fs.ACC, lw=1.6)
    ax.text(*(C + up * u(a) * 0.5 + np.array([0.18, 0.08])), r"$\vec{u}\,'$", fontsize=11, color=fs.ACC)
    fs.arrow(ax, O, P, color=fs.VEL, lw=1.8)
    ax.text(*(P * 0.5 + np.array([-0.15, 0.22])), r"$\vec{v}_{1f}=\vec{V}+\vec{u}\,'$", fontsize=9.5, color=fs.VEL,
            ha='center')
    ang = np.degrees(np.arctan2(P[1], P[0]))
    fs.angle_arc(ax, O, 0.55, 0, ang, r'$\theta$', tr=0.75)
    ax.text(C[0] + up * 0.75, -up - 0.05, r"반지름 $u\,'$", fontsize=8.5, color=fs.GRAY)
    fs.dot(ax, C, r=0.035)
    fs.save(fig, F, 'fig09_14')


for f_ in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
    f_()
