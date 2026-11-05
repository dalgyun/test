import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
"""8장 퍼텐셜 에너지와 에너지 보존 그림."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Arc, Rectangle, FancyArrowPatch, Ellipse
from scipy.interpolate import PchipInterpolator

F = __file__
D2R = np.pi / 180


def u(ang):
    return np.array([np.cos(ang * D2R), np.sin(ang * D2R)])


def mid_arrow(ax, x, y, frac=0.5, color=fs.BLACK, ms=11, reverse=False):
    """곡선 (x, y)의 frac 지점에 진행 방향 화살촉."""
    i = int(frac * (len(x) - 1))
    j = i + 2 if not reverse else i - 2
    ax.add_patch(FancyArrowPatch((x[i], y[i]), (x[j], y[j]), arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=6))


def wsub(ax, p, main, sub, color=fs.BLACK, fontsize=10, ha='center'):
    """수식에 한글 아래첨자."""
    ax.text(p[0], p[1], main, color=color, fontsize=fontsize, ha='right', va='baseline')
    ax.text(p[0], p[1], sub, color=color, fontsize=fontsize * 0.7, ha='left', va='top')


# ---------------------------------------------------------------- 그림 8.1 두 경로와 닫힌 경로
def fig01():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.0))
    a, b = np.array([0.0, 0.0]), np.array([3.0, 1.2])
    s = np.linspace(0, 1, 200)
    def path(bulge):
        base = a[None, :] + (b - a)[None, :] * s[:, None]
        nrm = np.array([-(b - a)[1], (b - a)[0]]) / np.linalg.norm(b - a)
        return base + nrm[None, :] * (bulge * np.sin(np.pi * s))[:, None]
    p1, p2 = path(0.8), path(-0.6)
    for k, ax in enumerate(axs):
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(-0.5, 3.6); ax.set_ylim(-1.0, 2.2)
        ax.plot(p1[:, 0], p1[:, 1], color=fs.VEL, lw=1.8)
        ax.plot(p2[:, 0], p2[:, 1], color=fs.FORCE if k == 0 else fs.FORCE, lw=1.8)
        mid_arrow(ax, p1[:, 0], p1[:, 1], color=fs.VEL)
        mid_arrow(ax, p2[:, 0], p2[:, 1], color=fs.FORCE, reverse=(k == 1))
        for p, t, off in ((a, r'$a$', (-0.25, -0.1)), (b, r'$b$', (0.25, 0.05))):
            fs.dot(ax, p, r=0.07); fs.label(ax, p + off, t, fontsize=12)
        fs.label(ax, p1[100] + (-0.3, 0.25), '경로 1', fontsize=9, color=fs.VEL)
        fs.label(ax, p2[100] + (0.35, -0.25), '경로 2' if k == 0 else '경로 2 (거꾸로)', fontsize=9, color=fs.FORCE)
        fs.label(ax, (1.55, -0.95), '(가) $a\\to b$의 두 경로' if k == 0 else '(나) 닫힌 경로', fontsize=9.5)
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, F, 'fig08_01')


# ---------------------------------------------------------------- 그림 8.2 세 가지 기본 퍼텐셜
def fig02():
    fig, axs = plt.subplots(1, 3, figsize=(5.4, 1.9))
    for ax in axs:
        for s_ in ('top', 'right'):
            ax.spines[s_].set_visible(False)
        ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
        ax.set_xticks([]); ax.set_yticks([])
    y = np.linspace(-0.3, 1.0, 50)
    axs[0].plot(y, y, color=fs.VEL, lw=1.8)
    axs[0].set_xlim(-0.35, 1.1); axs[0].set_ylim(-0.4, 1.1)
    axs[0].text(1.1, -0.12, r'$y$', ha='right', fontsize=10); axs[0].text(0.05, 1.05, r'$U$', fontsize=10)
    axs[0].text(0.62, 0.32, r'$mgy$', fontsize=10, color=fs.VEL)
    axs[0].set_title('(가) 지표 근처 중력', fontsize=9)
    x = np.linspace(-1, 1, 100)
    axs[1].plot(x, x ** 2, color=fs.VEL, lw=1.8)
    axs[1].set_xlim(-1.1, 1.1); axs[1].set_ylim(-0.2, 1.1)
    axs[1].text(1.1, -0.12, r'$x$', ha='right', fontsize=10); axs[1].text(0.05, 1.05, r'$U$', fontsize=10)
    axs[1].text(0.12, 0.55, r'$\frac{1}{2}kx^2$', fontsize=10, color=fs.VEL)
    axs[1].set_title('(나) 용수철', fontsize=9)
    r = np.linspace(0.18, 3, 200)
    axs[2].plot(r, -1 / r, color=fs.VEL, lw=1.8)
    axs[2].set_xlim(-0.1, 3.1); axs[2].set_ylim(-3.2, 0.5)
    axs[2].text(3.1, 0.12, r'$r$', ha='right', fontsize=10); axs[2].text(0.1, 0.35, r'$U$', fontsize=10)
    axs[2].text(1.1, -1.8, r'$-\dfrac{GMm}{r}$', fontsize=10, color=fs.VEL)
    axs[2].set_title('(다) 만유인력', fontsize=9)
    fig.subplots_adjust(wspace=0.35)
    fs.save(fig, F, 'fig08_02')


# ---------------------------------------------------------------- 그림 8.3 예제 8.2 진자
def fig03():
    L, th0 = 2.4, 50
    fig, ax = fs.canvas(3.6, 2.9, xlim=(-2.4, 2.0), ylim=(-3.4, 0.35))
    fs.ceiling(ax, -0.6, 0.6, 0)
    O = np.array([0.0, 0.0])
    P0 = O + L * np.array([-np.sin(th0 * D2R), -np.cos(th0 * D2R)])
    P1 = O + np.array([0, -L])
    ax.plot([O[0], P0[0]], [O[1], P0[1]], color=fs.GRAY, lw=1.0, ls='--')
    ax.plot([O[0], P1[0]], [O[1], P1[1]], color=fs.BLACK, lw=1.1)
    t = np.linspace(-90 - th0, -90, 50) * D2R
    ax.plot(L * np.cos(t), L * np.sin(t), color=fs.GRAY, lw=0.8, ls=':')
    fs.angle_arc(ax, O, 0.55, -90 - th0, -90, r'$\theta_0$', tr=0.8)
    ax.add_patch(Circle(P0, 0.13, fc='white', ec=fs.GRAY, ls='--', lw=1.0, zorder=5))
    ax.add_patch(Circle(P1, 0.13, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=5))
    fs.label(ax, (O + P0) / 2 + (-0.2, 0.12), r'$L$', fontsize=11)
    # 높이 차
    ax.plot([P0[0] - 0.15, P1[0] + 0.25], [P0[1], P0[1]], color=fs.GRAY, lw=0.6, ls=':')
    ax.plot([P0[0] - 0.15, P1[0] - 0.15], [P1[1], P1[1]], color=fs.GRAY, lw=0.6, ls=':')
    ax.annotate('', xy=(P0[0] - 0.1, P0[1]), xytext=(P0[0] - 0.1, P1[1]),
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8, shrinkA=0, shrinkB=0))
    fs.label(ax, (P0[0] - 0.2, (P0[1] + P1[1]) / 2), r'$L(1-\cos\theta_0)$', fontsize=9.5, ha='right')
    # 최하점 힘과 속도
    fs.vec(ax, P1 + (0, 0.13), (0, 0.8), color=fs.FORCE, lw=1.8)
    fs.label(ax, P1 + (0.3, 0.75), r'$\vec{T}$', color=fs.FORCE)
    fs.vec(ax, P1 - (0, 0.13), (0, -0.6), color=fs.FORCE, lw=1.8)
    fs.label(ax, P1 + (0.38, -0.65), r'$m\vec{g}$', color=fs.FORCE)
    fs.vec(ax, P1 + (0.13, 0), (0.85, 0), color=fs.VEL, lw=1.8)
    fs.label(ax, P1 + (1.15, 0.12), r'$\vec{v}$', color=fs.VEL)
    fs.label(ax, P0 + (-0.1, 0.32), '놓는 곳', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, F, 'fig08_03')


# ---------------------------------------------------------------- 그림 8.4 예제 8.3 원형 궤도
def fig04():
    R = 1.0
    h = 2.5 * R
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-0.6, 6.3), ylim=(-0.5, 3.1))
    xc = 3.9
    # 내려오는 궤도
    x = np.linspace(0, xc, 200)
    s = np.clip(x / 3.2, 0, 1)
    y = h * (1 - (3 * s ** 2 - 2 * s ** 3))
    ax.plot(x, y, color=fs.BLACK, lw=1.6)
    ax.plot([xc, 6.2], [0, 0], color=fs.BLACK, lw=1.6)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(xc + R * np.cos(th), R + R * np.sin(th), color=fs.BLACK, lw=1.6)
    ax.plot([-0.5, 6.2], [-0.12, -0.12], color=fs.GRAY, lw=0.6)
    # 출발점 수레
    ax.add_patch(Circle((0.0, h + 0.1), 0.1, fc=fs.LIGHT, ec=fs.BLACK, zorder=5))
    ax.annotate('', xy=(-0.35, h), xytext=(-0.35, 0), arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8,
                                                                      shrinkA=0, shrinkB=0))
    ax.plot([-0.45, 0.0], [h, h], color=fs.GRAY, lw=0.6, ls=':')
    fs.label(ax, (-0.5, h / 2), r'$h$', fontsize=11, ha='right')
    ax.plot([xc - 0.1, xc + 1.6], [2 * R, 2 * R], color=fs.GRAY, lw=0.6, ls=':')
    ax.annotate('', xy=(xc + 1.45, 2 * R), xytext=(xc + 1.45, 0), arrowprops=dict(arrowstyle='<->', color=fs.BLACK,
                                                                                lw=0.8, shrinkA=0, shrinkB=0))
    fs.label(ax, (xc + 1.62, R), r'$2R$', fontsize=10, ha='left')
    C = np.array([xc, R]); fs.dot(ax, C, r=0.035)
    ax.plot([xc, xc + R * np.cos(-0.6)], [R, R + R * np.sin(-0.6)], color=fs.GRAY, lw=0.8)
    fs.label(ax, C + (0.48, -0.08), r'$R$', fontsize=10)
    # 꼭대기 수레와 힘
    T = np.array([xc, 2 * R - 0.1])
    ax.add_patch(Circle(T, 0.1, fc=fs.LIGHT, ec=fs.BLACK, zorder=5))
    fs.vec(ax, T + (0.13, -0.05), (0, -0.6), color=fs.FORCE, lw=1.8)
    fs.label(ax, T + (0.45, -0.55), r'$m\vec{g}$', color=fs.FORCE, fontsize=10)
    fs.vec(ax, T + (-0.13, -0.05), (0, -0.45), color=fs.FORCE, lw=1.8)
    fs.label(ax, T + (-0.4, -0.42), r'$\vec{N}$', color=fs.FORCE, fontsize=10)
    fs.vec(ax, T + (-0.12, 0.25), (-0.7, 0), color=fs.VEL, lw=1.8)
    fs.label(ax, T + (-0.55, 0.47), r'$\vec{v}_{\mathrm{top}}$', color=fs.VEL, fontsize=10)
    fs.save(fig, F, 'fig08_04')


# ---------------------------------------------------------------- 그림 8.5 예제 8.4 번지점프 위치
def fig05():
    m, g, k, L0 = 60.0, 9.8, 200.0, 15.0
    x0 = m * g / k
    xb = (m * g + np.sqrt((m * g) ** 2 + 2 * k * m * g * L0)) / k
    fig, ax = fs.canvas(3.6, 3.4, xlim=(-2.9, 4.2), ylim=(-30.5, 2.5))
    ax.set_aspect(0.19)
    ax.add_patch(Rectangle((-2.0, 0), 2.4, 1.0, fc='#dddddd', ec=fs.BLACK, lw=1.1))
    fs.label(ax, (-2.1, 0.5), '다리', fontsize=9, ha='right')
    marks = [(0, '출발 ($v=0$)'), (L0, r'줄이 팽팽해짐 ($L_0=15$ m)'), (L0 + x0, '최대 속력 ($17.9$ m)'),
             (L0 + xb, r'최저점 ($27.8$ m)')]
    ax.plot([0, 0], [0, -(L0 + xb)], color=fs.GRAY, lw=0.6, ls=':')
    for d, t in marks:
        ax.plot([-0.25, 0.25], [-d, -d], color=fs.BLACK, lw=0.9)
        ax.text(0.45, -d, t, fontsize=8.5, va='center')
    # 줄(최저점 상태)
    yy = np.linspace(0, -(L0 + xb), 400)
    ax.plot(-0.9 + 0 * yy, yy, color=fs.ORANGE, lw=1.4)
    ax.add_patch(Ellipse((-0.9, -(L0 + xb) - 0.6), 0.45, 1.6, fc=fs.LIGHT, ec=fs.BLACK, zorder=5))
    ax.annotate('', xy=(-1.6, 0), xytext=(-1.6, -L0), arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK,
                                                                       shrinkA=0, shrinkB=0))
    fs.label(ax, (-1.75, -L0 / 2), r'$L_0$', fontsize=10, ha='right')
    ax.annotate('', xy=(-1.6, -L0), xytext=(-1.6, -(L0 + xb)), arrowprops=dict(arrowstyle='<->', lw=0.8,
                                                                                color=fs.BLACK, shrinkA=0, shrinkB=0))
    fs.label(ax, (-1.75, -(L0 + xb / 2)), r'$x$', fontsize=10, ha='right')
    fs.save(fig, F, 'fig08_05')


# ---------------------------------------------------------------- 그림 8.6 예제 8.4 에너지 그래프
def fig06():
    m, g, k, L0 = 60.0, 9.8, 200.0, 15.0
    x0 = m * g / k
    xb = (m * g + np.sqrt((m * g) ** 2 + 2 * k * m * g * L0)) / k
    yb = L0 + xb
    y = np.linspace(0, yb, 500)
    Ug = m * g * (yb - y)
    Us = np.where(y > L0, 0.5 * k * (y - L0) ** 2, 0)
    E = m * g * yb
    K = E - Ug - Us
    fig, ax = fs.plot_axes(4.2, 3.0)
    ax.plot(y, Ug / 1e3, color=fs.GRAY, lw=1.6, label=r'중력 퍼텐셜 $U_g$')
    ax.plot(y, Us / 1e3, color=fs.ORANGE, lw=1.6, label=r'줄의 퍼텐셜 $U_s$')
    ax.plot(y, K / 1e3, color=fs.VEL, lw=2, label=r'운동에너지 $K$')
    ax.axhline(E / 1e3, color=fs.BLACK, lw=1, ls='--', label=r'역학적 에너지 $E$')
    ax.axvline(L0, color=fs.GRAY, lw=0.6, ls=':'); ax.axvline(L0 + x0, color=fs.VEL, lw=0.6, ls=':')
    ax.text(L0 - 0.4, 17.5, r'$15$', fontsize=8.5, ha='right', color=fs.GRAY)
    ax.text(L0 + x0 + 0.3, 17.5, r'$17.9$', fontsize=8.5, ha='left', color=fs.VEL)
    ax.set_xlim(0, 29); ax.set_ylim(0, 19)
    ax.set_xlabel('다리에서 내려온 거리 (m)'); ax.set_ylabel('에너지 (kJ)')
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False)
    fs.save(fig, F, 'fig08_06')


# ---------------------------------------------------------------- 그림 8.7 등퍼텐셜선과 힘
def fig07():
    fig, ax = fs.canvas(3.4, 2.6, xlim=(-2.6, 2.6), ylim=(-1.8, 1.8))
    X, Y = np.meshgrid(np.linspace(-2.6, 2.6, 300), np.linspace(-1.8, 1.8, 300))
    U = X ** 2 / 4 + Y ** 2
    levels = [0.25, 0.75, 1.5, 2.5]
    ax.contour(X, Y, U, levels=levels, colors=[fs.FIELD], linewidths=1.0)
    for lv, ang in zip(levels[1:], (25, 140, 250)):
        a = ang * D2R
        r = 1 / np.sqrt(np.cos(a) ** 2 / 4 + np.sin(a) ** 2) * np.sqrt(lv)
        p = r * np.array([np.cos(a), np.sin(a)])
        gU = np.array([p[0] / 2, 2 * p[1]])
        Fv = -gU / np.linalg.norm(gU) * 0.6
        fs.vec(ax, p, Fv, color=fs.FORCE, lw=1.6)
        fs.dot(ax, p, r=0.04)
    p = np.array([1.2, 0.0]) * np.sqrt(0.75) * 2 / 1.2
    fs.label(ax, (1.95, 1.55), r'$U=$ 일정', fontsize=9, color=fs.FIELD, bbox=dict(fc='white', ec='none', pad=0.5))
    fs.label(ax, (0.55, -1.3), r'$\vec{F}=-\nabla U$', fontsize=9.5, color=fs.FORCE, ha='left', bbox=dict(fc='white', ec='none', pad=0.5))
    fs.label(ax, (0, 0), r'$U$ 최소', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, F, 'fig08_07')


# ---------------------------------------------------------------- 그림 8.8 퍼텐셜 에너지 곡선 읽기
def fig08():
    xs = [0, 1, 2, 3, 4, 5, 6, 7.5, 8.5, 9.3]
    us = [4.6, 2.4, 0.8, 2.2, 3.2, 2.0, 1.6, 1.6, 3.0, 4.6]
    Uf = PchipInterpolator(xs, us)
    x = np.linspace(0, 9.3, 600)
    U = Uf(x)
    E = 2.6
    fig, ax = fs.plot_axes(4.6, 2.9)
    ax.grid(False)
    ax.fill_between(x, U, E, where=U > E, color=fs.GRAY, alpha=0.25, lw=0)
    ax.plot(x, U, color=fs.VEL, lw=2)
    ax.axhline(E, color=fs.FORCE, lw=1.2, ls='--')
    ax.text(9.3, E + 0.12, r'$E$', color=fs.FORCE, fontsize=11, ha='right', va='bottom')
    # 전환점 (왼쪽 우물)
    from scipy.optimize import brentq
    x1 = brentq(lambda t: Uf(t) - E, 0.2, 2); x2 = brentq(lambda t: Uf(t) - E, 2, 4)
    for xx, t in ((x1, r'$x_1$'), (x2, r'$x_2$')):
        ax.plot([xx, xx], [0, E], color=fs.FORCE, lw=0.7, ls=':')
        ax.plot(xx, E, 'o', color=fs.FORCE, ms=4)
        ax.text(xx, -0.3, t, ha='center', va='top', fontsize=10)
    ax.annotate('', xy=(x1, 0.22), xytext=(x2, 0.22),
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text((x1 + x2) / 2 + 0.55, 0.3, '운동 영역', fontsize=8, ha='left', va='bottom')
    ax.text(2.12, 1.75, r'$K=E-U$', fontsize=8.5, ha='left', color=fs.ACC)
    ax.annotate('', xy=(2.0, 0.8), xytext=(2.0, E), arrowprops=dict(arrowstyle='<->', color=fs.ACC, lw=1.0,
                                                                     shrinkA=0, shrinkB=0))
    ax.text(1.55, 0.62, '안정', fontsize=8.5, ha='right', color=fs.VEL)
    ax.text(4.0, 3.45, '불안정', fontsize=8.5, ha='center', color=fs.VEL)
    ax.text(6.75, 1.25, '중립', fontsize=8.5, ha='center', color=fs.VEL)
    for xe, ue in ((2, 0.8), (4, 3.2)):
        ax.plot(xe, ue, 'o', color=fs.VEL, ms=4)
    ax.plot([6, 7.5], [1.6, 1.6], color=fs.VEL, lw=4, alpha=0.4)
    ax.annotate('금지 영역 $(U>E)$', xy=(4.25, 2.8), xytext=(5.3, 4.1), fontsize=8, color=fs.GRAY,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.set_xlim(0, 9.4); ax.set_ylim(0, 4.8)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(r'$x$', loc='right'); ax.set_ylabel(r'$U(x)$')
    fs.save(fig, F, 'fig08_08')


# ---------------------------------------------------------------- 그림 8.9 예제 8.5 이중 우물
def fig09():
    xi = np.linspace(-1.75, 1.75, 400)
    U = xi ** 4 - 2 * xi ** 2
    fig, ax = fs.plot_axes(4.2, 2.8)
    ax.plot(xi, U, color=fs.VEL, lw=2)
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    Ea = -0.5
    xa1, xa2 = np.sqrt(1 - 1 / np.sqrt(2)), np.sqrt(1 + 1 / np.sqrt(2))
    ax.plot([xa1, xa2], [Ea, Ea], color=fs.FORCE, lw=1.8)
    ax.plot([-xa2, -xa1], [Ea, Ea], color=fs.FORCE, lw=1.8, ls=(0, (3, 2)))
    ax.text(1.55, Ea - 0.05, r'$E<0$', color=fs.FORCE, fontsize=9.5, va='top')
    Eb = 0.4
    xb = np.sqrt(1 + np.sqrt(1 + Eb))
    ax.plot([-xb, xb], [Eb, Eb], color=fs.ACC, lw=1.8)
    ax.text(xb + 0.05, Eb, r'$E>0$', color=fs.ACC, fontsize=9.5, va='center')
    for xe, ue, t in ((0, 0, '불안정'), (1, -1, '안정'), (-1, -1, '안정')):
        ax.plot(xe, ue, 'o', color=fs.BLACK, ms=4, zorder=5)
        ax.text(xe, ue - 0.12 if ue < 0 else ue + 0.12, t, ha='center', va='top' if ue < 0 else 'bottom', fontsize=8.5)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels([r'$-a$', '0', r'$a$'])
    ax.set_yticks([-1, 0]); ax.set_yticklabels([r'$-U_0$', '0'])
    ax.set_xlim(-1.8, 2.0); ax.set_ylim(-1.35, 1.2)
    ax.set_xlabel(r'$x$'); ax.set_ylabel(r'$U(x)$')
    fs.save(fig, F, 'fig08_09')


# ---------------------------------------------------------------- 그림 8.10 레너드-존스 퍼텐셜
def fig10():
    r = np.linspace(0.92, 3.0, 400)
    U = 4 * (r ** -12 - r ** -6)
    rm = 2 ** (1 / 6)
    fig, ax = fs.plot_axes(3.8, 2.6)
    ax.plot(r, U, color=fs.VEL, lw=2)
    ax.axhline(0, color=fs.BLACK, lw=0.7)
    ax.axhline(-1, color=fs.GRAY, lw=0.7, ls=':')
    ax.plot([rm, rm], [-1, 0], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot(rm, -1, 'o', color=fs.VEL, ms=4)
    ax.annotate('', xy=(2.2, -1), xytext=(2.2, 0), arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8,
                                                                    shrinkA=0, shrinkB=0))
    ax.text(2.27, -0.5, r'$\varepsilon$ (우물 깊이)', fontsize=9, va='center')
    ax.text(rm + 0.04, 0.15, r'$r_m=2^{1/6}\sigma$', fontsize=9)
    ax.plot(1, 0, 'o', color=fs.BLACK, ms=3)
    ax.text(0.97, 0.12, r'$\sigma$', fontsize=10, ha='right')
    ax.text(1.35, 1.3, '척력', fontsize=9, color=fs.FORCE)
    ax.text(2.4, 0.3, '인력', fontsize=9, color=fs.FORCE)
    ax.set_xlim(0.85, 3.0); ax.set_ylim(-1.3, 2.0)
    ax.set_xlabel(r'$r/\sigma$'); ax.set_ylabel(r'$U/\varepsilon$')
    fs.save(fig, F, 'fig08_10')


# ---------------------------------------------------------------- 그림 8.11 예제 8.6 마찰 있는 빗면
def fig11():
    th = 30
    fig, ax = fs.canvas(4.0, 2.7, xlim=(-0.3, 5.6), ylim=(-0.4, 3.6))
    fs.incline(ax, (0, 0), 5.6, th, show_angle=False)
    fs.angle_arc(ax, (0, 0), 0.7, 0, th, r'$30^{\circ}$', tr=1.1, fontsize=9)
    t, n = u(th), u(th + 90)
    s0, h = 4.0, 0.55
    c = s0 * t + n * h / 2
    fs.block(ax, c, 0.8, h, angle=th)
    fs.vec(ax, c, (0, -1.15), color=fs.FORCE, lw=1.8)
    fs.label(ax, c + (0.38, -1.05), r'$m\vec{g}$', color=fs.FORCE)
    fs.vec(ax, c + n * h / 2, n * 0.85, color=fs.FORCE, lw=1.8)
    fs.label(ax, c + n * (h / 2 + 1.0), r'$\vec{N}$', color=fs.FORCE)
    fs.vec(ax, c + t * 0.4 - n * 0.18, t * 0.65, color=fs.FORCE, lw=1.8)
    fs.label(ax, c + t * 1.25 - n * 0.05, r'$\vec{f}_k$', color=fs.FORCE)
    # 미끄러지는 방향과 거리
    p0 = s0 * t + n * (h + 0.35)
    fs.arrow(ax, p0 - t * 0.2, p0 - t * 3.2, lw=1.3)
    fs.label(ax, p0 - t * 1.7 + n * 0.3, r'$d=3.0\ \mathrm{m}$', fontsize=10)
    fs.label(ax, c - t * 0.2 + n * 0.05, r'$m$', fontsize=10, zorder=9)
    fs.save(fig, F, 'fig08_11')


# ---------------------------------------------------------------- 그림 8.12 연습문제 8 반구
def fig12():
    R = 2.0
    fig, ax = fs.canvas(3.2, 2.4, xlim=(-2.4, 2.6), ylim=(-0.3, 3.2))
    th = np.linspace(0, np.pi, 200)
    ax.add_patch(Polygon(np.c_[R * np.cos(th), R * np.sin(th)], closed=True, fc='#eeeeee', ec=fs.BLACK, lw=1.4))
    fs.ground(ax, -2.4, 2.6, 0)
    O = np.array([0.0, 0.0])
    a = 35
    p = R * np.array([np.sin(a * D2R), np.cos(a * D2R)])
    ax.plot([0, 0], [0, R + 0.6], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([0, p[0]], [0, p[1]], color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, O, 0.6, 90 - a, 90, r'$\theta$', tr=0.85)
    rh = p / R
    c = p + rh * 0.11
    ax.add_patch(Circle(c, 0.11, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=6))
    fs.vec(ax, c + rh * 0.11, rh * 0.6, color=fs.FORCE, lw=1.6)
    fs.label(ax, c + rh * 0.95, r'$\vec{N}$', color=fs.FORCE)
    fs.vec(ax, c, (0, -0.85), color=fs.FORCE, lw=1.6)
    fs.label(ax, c + (0.35, -0.75), r'$m\vec{g}$', color=fs.FORCE)
    tg = np.array([np.cos(a * D2R), -np.sin(a * D2R)])
    fs.vec(ax, c + rh * 0.15 + tg * 0.12, tg * 0.6, color=fs.VEL, lw=1.6)
    fs.label(ax, c + tg * 0.9 + rh * 0.3, r'$\vec{v}$', color=fs.VEL)
    fs.label(ax, p * 0.5 + (0.15, -0.15), r'$R$', fontsize=10)
    fs.save(fig, F, 'fig08_12')


# ---------------------------------------------------------------- 그림 8.13 연습문제 11 못이 있는 진자
def fig13():
    L, d = 2.5, 1.6
    r = L - d
    fig, ax = fs.canvas(3.8, 2.7, xlim=(-1.5, 3.4), ylim=(-2.9, 0.4))
    fs.ceiling(ax, -0.4, 0.4, 0)
    O = np.array([0.0, 0.0]); Nn = np.array([0.0, -d])
    ax.plot([0, L], [0, 0], color=fs.GRAY, lw=1.0, ls='--')
    ax.add_patch(Circle((L, 0), 0.11, fc='white', ec=fs.GRAY, ls='--', zorder=5))
    t = np.linspace(0, -np.pi / 2, 60)
    ax.plot(L * np.cos(t), L * np.sin(t), color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([0, 0], [0, -L], color=fs.BLACK, lw=1.1)
    ax.add_patch(Circle((0, -L), 0.11, fc=fs.LIGHT, ec=fs.BLACK, zorder=5))
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r * np.cos(tt), -d + r * np.sin(tt), color=fs.VEL, lw=1.0, ls='--')
    ax.add_patch(Circle(Nn, 0.06, fc=fs.BLACK, zorder=6))
    fs.label(ax, Nn + (0.12, 0.17), '못', fontsize=9, ha='left')
    ax.annotate('', xy=(-1.1, 0), xytext=(-1.1, -d), arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK,
                                                                        shrinkA=0, shrinkB=0))
    fs.label(ax, (-1.25, -d / 2), r'$d$', fontsize=10)
    ax.plot([-1.2, 0], [-d, -d], color=fs.GRAY, lw=0.6, ls=':')
    fs.label(ax, (L / 2, 0.15), r'$L$', fontsize=10)
    fs.label(ax, (0.2 + r * 0.9, -d - r * 0.5), r'$L-d$', fontsize=9, color=fs.VEL, ha='left')
    ax.plot([0, r * 0.9], [-d, -d - r * 0.44], color=fs.VEL, lw=0.8)
    fs.save(fig, F, 'fig08_13')


# ---------------------------------------------------------------- 그림 8.14 연습문제 12 빗면과 용수철
def fig14():
    th = 30
    fig, ax = fs.canvas(4.2, 2.5, xlim=(-0.3, 6.0), ylim=(-0.3, 3.4))
    top = fs.incline(ax, (0, 0), 6.2, th, show_angle=False)
    fs.angle_arc(ax, (0, 0), 0.75, 0, th, r'$30^{\circ}$', tr=1.15, fontsize=9)
    t, n = u(th), u(th + 90)
    # 빗면 아래쪽 끝에 고정판, 용수철
    s_w = 0.5
    base = s_w * t
    ax.plot(*zip(base, base + n * 0.6), color=fs.BLACK, lw=2.0)
    Ls = 1.5
    fs.spring(ax, base + n * 0.25, base + t * Ls + n * 0.25, coils=7, width=0.12)
    ax.plot(*zip(base + t * Ls + n * 0.05, base + t * Ls + n * 0.45), color=fs.BLACK, lw=1.4)
    sb = s_w + Ls + 1.5
    c = sb * t + n * 0.27 + t * 0.35
    fs.block(ax, c, 0.7, 0.54, angle=th, text=r'$m$', fontsize=10)
    # 1.5 m 거리
    p0 = (s_w + Ls) * t + n * 0.95
    p1 = sb * t + n * 0.95
    ax.annotate('', xy=p0, xytext=p1, arrowprops=dict(arrowstyle='<->', lw=0.8, color=fs.BLACK, shrinkA=0, shrinkB=0))
    fs.label(ax, (p0 + p1) / 2 + n * 0.25, r'$1.5\ \mathrm{m}$', fontsize=9.5)
    fs.label(ax, base + t * Ls / 2 + n * 0.65, r'$k$', fontsize=10)
    fs.label(ax, (4.4, 0.45), r'$\mu_k=0.20$', fontsize=9.5)
    fs.save(fig, F, 'fig08_14')


# ---------------------------------------------------------------- 그림 8.15 연습문제 14 회전하는 고리
def fig15():
    R = 1.5
    fig, ax = fs.canvas(3.0, 3.0, xlim=(-2.0, 2.2), ylim=(-2.2, 2.4))
    ax.plot([0, 0], [-2.0, 2.1], color=fs.BLACK, lw=1.0, ls='-.')
    ax.add_patch(Ellipse((0, 0), 2 * R, 2 * R, fc='none', ec=fs.BLACK, lw=1.6))
    # 회전 표시
    ax.add_patch(Arc((0, 1.85), 0.9, 0.25, theta1=200, theta2=520 - 180, color=fs.BLACK, lw=1.0))
    ax.add_patch(FancyArrowPatch((0.32, 1.78), (0.45, 1.84), arrowstyle='-|>', mutation_scale=9, color=fs.BLACK, lw=0))
    fs.label(ax, (0.7, 2.05), r'$\omega$', fontsize=11)
    th = 50
    p = R * np.array([np.sin(th * D2R), -np.cos(th * D2R)])
    ax.plot([0, p[0]], [0, p[1]], color=fs.GRAY, lw=0.8)
    ax.plot([0, 0], [0, -R], color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, (0, 0), 0.45, -90, -90 + th, r'$\theta$', tr=0.68)
    ax.add_patch(Circle(p, 0.1, fc=fs.ORANGE, ec=fs.BLACK, lw=0.8, zorder=6))
    fs.label(ax, p * 0.5 + (0.2, 0.12), r'$R$', fontsize=10)
    ax.plot([0, p[0]], [p[1], p[1]], color=fs.GRAY, lw=0.8, ls=':')
    fs.label(ax, (p[0] / 2, p[1] - 0.2), r'$R\sin\theta$', fontsize=9, color=fs.GRAY)
    fs.label(ax, (0.25, -R - 0.2), '최하점', fontsize=8.5, ha='left')
    fs.save(fig, F, 'fig08_15')


for f_ in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15):
    f_()
