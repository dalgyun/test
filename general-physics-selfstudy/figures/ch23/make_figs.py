"""23장 전기 퍼텐셜 그림 생성 스크립트.  python3 figures/ch23/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Ellipse, FancyArrowPatch, Rectangle, PathPatch
from matplotlib.path import Path


def lines_of(charges, xlim, ylim, **kw):
    """fs.field_lines가 그린 선의 좌표만 얻는다(빈 축에 그린 뒤 꺼냄)."""
    f, a = plt.subplots()
    fs.field_lines(a, charges, xlim, ylim, arrows=False, **kw)
    out = [l.get_xydata() for l in a.lines]
    plt.close(f)
    return out


def mid_arrow(ax, pts, color=fs.FIELD, frac=0.5, ms=9, xlim=None, ylim=None):
    pts = np.asarray(pts)
    idx = list(range(len(pts)))
    if xlim is not None:
        idx = [i for i in idx if xlim[0] < pts[i, 0] < xlim[1] and ylim[0] < pts[i, 1] < ylim[1]]
    if len(idx) < 6:
        return
    i = idx[int(len(idx) * frac)]
    j = min(i + 3, len(pts) - 1)
    ax.add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle='-|>', mutation_scale=ms, color=color, lw=0, zorder=2))


# ---------------------------------------------------------------- 23.1
def fig01():
    """쿨롱 힘의 일: 임의 경로와 dℓ의 지름 성분."""
    fig, ax = fs.canvas(4.6, 3.3, xlim=(-0.6, 5.6), ylim=(-0.5, 4.3))
    O = np.array([0.0, 0.0])
    fs.charge(ax, O, +1)
    fs.label(ax, (-0.05, -0.38), '$Q$')
    ra, rb = 1.6, 4.2
    tha, thb = np.radians(60), np.radians(12)
    a = O + ra * np.array([np.cos(tha), np.sin(tha)])
    b = O + rb * np.array([np.cos(thb), np.sin(thb)])
    # 반지름 ra, rb 원호(점선)
    for r in (ra, rb):
        t = np.linspace(0, np.pi / 2, 100)
        ax.plot(r * np.cos(t), r * np.sin(t), color=fs.GRAY, lw=0.7, ls='--')
    # 임의 경로(베지에)
    P0, P1, P2, P3 = a, np.array([1.0, 3.4]), np.array([4.4, 3.2]), b
    s = np.linspace(0, 1, 200)[:, None]
    curve = (1 - s) ** 3 * P0 + 3 * (1 - s) ** 2 * s * P1 + 3 * (1 - s) * s ** 2 * P2 + s ** 3 * P3
    ax.plot(curve[:, 0], curve[:, 1], color=fs.BLACK, lw=1.4)
    mid_arrow(ax, curve, color=fs.BLACK, frac=0.85)
    fs.dot(ax, a); fs.dot(ax, b)
    fs.label(ax, a + np.array([-0.25, 0.05]), '$a$')
    fs.label(ax, b + np.array([0.2, -0.2]), '$b$')
    # 경로 위 한 점에서 dℓ, r̂, dr: 접선과 r̂ 사이 각이 약 50°인 점을 고른다
    tang = np.gradient(curve, axis=0); tang /= np.linalg.norm(tang, axis=1)[:, None]
    rh = curve / np.linalg.norm(curve, axis=1)[:, None]
    cosang = np.sum(tang * rh, axis=1)
    k = int(np.argmin(np.abs(cosang[:120] - 0.64)))
    p = curve[k]; t = tang[k]; rhat = rh[k]
    dl = 1.1 * t
    ax.plot([0, p[0]], [0, p[1]], color=fs.GRAY, lw=0.8)
    proj = np.dot(dl, rhat) * rhat
    foot = p + proj
    ax.plot([p[0], foot[0]], [p[1], foot[1]], color=fs.GRAY, lw=0.8)
    q = p + dl
    ax.plot([q[0], foot[0]], [q[1], foot[1]], color=fs.GRAY, lw=0.8, ls=':')
    fs.vec(ax, p, dl, color=fs.VEL, lw=1.7, zorder=7)
    fs.label(ax, q + 0.3 * t, r'$d\vec{\ell}$', color=fs.VEL)
    fs.vec(ax, p, 0.55 * rhat, color=fs.FORCE, lw=1.5, zorder=8)
    side = np.array([-rhat[1], rhat[0]])          # r̂의 왼쪽(반시계) 방향
    if np.dot(side, t) > 0:
        side = -side                              # dℓ 반대쪽에 dr 치수와 r̂ 글자
    fs.label(ax, p + 0.85 * rhat, r'$\hat{r}$', color=fs.FORCE)
    o = 0.42 * side
    ax.add_patch(FancyArrowPatch(p + o, foot + o, arrowstyle='<|-|>', mutation_scale=7, color=fs.BLACK, lw=0.8))
    for e in (p, foot):
        ax.plot([e[0] + 0.1 * side[0], e[0] + o[0] * 1.15], [e[1] + 0.1 * side[1], e[1] + o[1] * 1.15], color=fs.BLACK, lw=0.5)
    fs.label(ax, (p + foot) / 2 + o * 1.6, '$dr$', fontsize=10)
    fs.label(ax, (ra, -0.25), '$r_a$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (rb, -0.25), '$r_b$', fontsize=10, color=fs.GRAY)
    fs.label(ax, p * 0.5 + np.array([-0.12, 0.15]), '$r$', fontsize=10, color=fs.GRAY)
    fs.save(fig, __file__, 'fig23_01')


def fig02():
    """예제 23.1 정삼각형 꼭짓점의 세 전하."""
    fig, ax = fs.canvas(3.0, 2.6, xlim=(-0.6, 2.6), ylim=(-0.55, 2.25))
    P = [np.array([0, 0]), np.array([2, 0]), np.array([1, np.sqrt(3)])]
    ax.add_patch(Polygon(P, closed=True, fc='none', ec=fs.GRAY, lw=1.0))
    qs = [(+1, '$q_1 = +2.0\\ \\mu\\mathrm{C}$', (-0.05, -0.4)),
          (-1, '$q_2 = -4.0\\ \\mu\\mathrm{C}$', (0.05, -0.4)),
          (+1, '$q_3 = +3.0\\ \\mu\\mathrm{C}$', (0, 0.36))]
    for p, (sg, s, off) in zip(P, qs):
        fs.charge(ax, p, sg)
        fs.label(ax, p + np.array(off), s, fontsize=10)
    for i, j, off in ((0, 1, (0, 0.17)), (1, 2, (0.28, 0.1)), (0, 2, (-0.28, 0.1))):
        m = (P[i] + P[j]) / 2 + np.array(off)
        fs.label(ax, m, '$a$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (1, 0.6), '$a = 0.10\\ \\mathrm{m}$', fontsize=9, color=fs.GRAY)
    fs.save(fig, __file__, 'fig23_02')


# ---------------------------------------------------------------- 23.2
def fig03():
    """균일한 장의 등전위면과 전위차."""
    fig, ax = fs.canvas(4.4, 2.5, xlim=(-0.3, 6.3), ylim=(-0.6, 3.1))
    for y in (0.45, 1.25, 2.05):
        fs.arrow(ax, (0.0, y + 0.4), (6.0, y + 0.4), color=fs.FIELD, lw=1.0, ms=9)
    fs.label(ax, (6.15, 2.85), r'$\vec{E}$', color=fs.FIELD)
    xs = [0.8, 2.2, 3.6, 5.0]
    labs = ['$V_0$', r'$V_0-Ed$', r'$V_0-2Ed$', r'$V_0-3Ed$']
    for x, s in zip(xs, labs):
        ax.plot([x, x], [0.2, 2.75], color=fs.ORANGE, lw=1.3, ls='--')
        fs.label(ax, (x, 3.0), s, fontsize=8.5, color=fs.ORANGE)
    fs.dim(ax, (2.2, 0.2), (3.6, 0.2), '$d$', off=-0.25, fontsize=10)
    # 양전하와 전자의 가속 방향
    fs.charge(ax, (1.5, 1.65), +1, r=0.15, fontsize=10)
    fs.arrow(ax, (1.7, 1.65), (2.35, 1.65), color=fs.FORCE, lw=1.6)
    fs.charge(ax, (4.6, 0.85), -1, r=0.15, fontsize=10)
    fs.arrow(ax, (4.4, 0.85), (3.75, 0.85), color=fs.FORCE, lw=1.6)
    fs.label(ax, (0.35, -0.3), '높은 전위', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (5.6, -0.3), '낮은 전위', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig23_03')


# ---------------------------------------------------------------- 23.3
def fig04():
    """쌍극자의 전위: 기하."""
    fig, ax = fs.canvas(3.2, 3.1, xlim=(-1.2, 3.2), ylim=(-1.6, 2.7))
    d2 = 0.6
    ax.plot([0, 0], [-1.5, 2.5], color=fs.GRAY, lw=0.8)
    fs.arrow(ax, (0, 2.3), (0, 2.6), color=fs.GRAY, lw=0.8, ms=8)
    fs.label(ax, (-0.2, 2.55), '$z$', fontsize=10, color=fs.GRAY)
    P = np.array([2.3, 1.8])
    for zc, sg, lab in ((d2, +1, '$+q$'), (-d2, -1, '$-q$')):
        fs.charge(ax, (0, zc), sg, r=0.15, fontsize=10)
        fs.label(ax, (-0.45, zc), lab, fontsize=10)
    ax.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=1.1)
    ax.plot([0, P[0]], [d2, P[1]], color=fs.VEL, lw=1.0, ls='--')
    ax.plot([0, P[0]], [-d2, P[1]], color=fs.FORCE, lw=1.0, ls='--')
    fs.dot(ax, P)
    fs.label(ax, P + np.array([0.18, 0.15]), '$P$')
    fs.label(ax, (1.35, 1.2), '$r$', fontsize=11)
    fs.label(ax, (0.95, 1.48), '$r_+$', fontsize=10, color=fs.VEL)
    fs.label(ax, (1.45, 0.45), '$r_-$', fontsize=10, color=fs.FORCE)
    th = np.degrees(np.arctan2(P[1], P[0]))
    fs.angle_arc(ax, (0, 0), 0.55, th, 90, r'$\theta$', fontsize=10, tr=0.78)
    fs.arrow(ax, (0.35, -d2), (0.35, d2), color=fs.FIELD, lw=1.4, ms=9)
    fs.label(ax, (0.62, -0.25), r'$\vec{p}$', color=fs.FIELD, fontsize=10)
    fs.dim(ax, (-0.75, -d2), (-0.75, d2), '$d$', off=0.0, fontsize=10)
    fs.save(fig, __file__, 'fig23_04')


def fig05():
    """예제 23.3 고리와 원판의 축 위 전위."""
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.8))
    for ax, kind in zip(axs, ('ring', 'disk')):
        ax.set_xlim(-1.5, 1.6); ax.set_ylim(-0.75, 2.6); ax.set_aspect('equal'); ax.axis('off')
        R, ry = 1.1, 0.33
        ax.plot([0, 0], [-0.6, 2.45], color=fs.GRAY, lw=0.8)
        fs.label(ax, (0.18, 2.45), '$z$', fontsize=10, color=fs.GRAY)
        P = np.array([0, 1.9])
        if kind == 'ring':
            fs.ellipse3d(ax, (0, 0), R, ry, color=fs.POS, lw=2.0, back_dashed=False)
            e = np.array([R * np.cos(np.radians(-35)), ry * np.sin(np.radians(-35))])
            ax.add_patch(Circle(e, 0.07, color=fs.BLACK, zorder=8))
            fs.label(ax, e + np.array([0.28, -0.12]), '$dq$', fontsize=10)
            ax.plot([e[0], P[0]], [e[1], P[1]], color=fs.VEL, lw=1.0)
            fs.label(ax, (0.95, 1.05), r'$\sqrt{z^2+R^2}$', fontsize=9.5, color=fs.VEL)
            ax.plot([0, -R], [0, 0], color=fs.BLACK, lw=0.8)
            fs.label(ax, (-R / 2, 0.14), '$R$', fontsize=10)
            fs.label(ax, (0, -0.65), '(가) 고리, 전하 $Q$', fontsize=9)
        else:
            ax.add_patch(Ellipse((0, 0), 2 * R, 2 * ry, fc='#f6d3cf', ec=fs.POS, lw=1.2, zorder=1))
            r1, r2 = 0.62, 0.78
            th = np.linspace(0, 2 * np.pi, 200)
            ring = np.concatenate([np.c_[r2 * np.cos(th), ry / R * r2 * np.sin(th)],
                                   np.c_[r1 * np.cos(th[::-1]), ry / R * r1 * np.sin(th[::-1])]])
            ax.add_patch(Polygon(ring, closed=True, fc=fs.POS, alpha=0.55, ec='none', zorder=2))
            e = np.array([0.70 * np.cos(np.radians(-60)), ry / R * 0.70 * np.sin(np.radians(-60))])
            ax.plot([e[0], P[0]], [e[1], P[1]], color=fs.VEL, lw=1.0, zorder=3)
            fs.label(ax, (0.62, 1.05), r'$\sqrt{z^2+r^2}$', fontsize=9.5, color=fs.VEL)
            ax.plot([0, -R], [0, 0], color=fs.BLACK, lw=0.8, zorder=3)
            fs.label(ax, (-0.95, 0.15), '$R$', fontsize=10)
            ax.plot([0, -0.7 * np.cos(np.radians(25))], [0, -0.7 * ry / R * np.sin(np.radians(25))], color=fs.BLACK, lw=0.6, zorder=3)
            fs.label(ax, (-0.42, -0.02), '$r$', fontsize=9)
            fs.label(ax, (1.05, -0.42), '폭 $dr$인 고리', fontsize=8.5, color=fs.POS)
            fs.label(ax, (0, -0.65), '(나) 원판, 면전하 밀도 $\\sigma$', fontsize=9)
        fs.dot(ax, P)
        fs.label(ax, P + np.array([-0.22, 0.12]), '$P$')
        ax.plot([-0.12, 0.12], [0, 0], color=fs.BLACK, lw=0.8)
        ax.annotate('', xy=(-0.28, P[1]), xytext=(-0.28, 0), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=7))
        fs.label(ax, (-0.45, 0.95), '$z$', fontsize=10, color=fs.GRAY)
    fig.tight_layout(w_pad=0.2)
    fs.save(fig, __file__, 'fig23_05')


def fig06():
    """예제 23.4 균일하게 대전된 구의 V(r)와 E(r)."""
    fig, ax = fs.plot_axes(4.2, 2.7)
    x = np.linspace(0, 4, 400)
    V = np.where(x < 1, 0.5 * (3 - x ** 2), 1 / np.maximum(x, 1e-9))
    E = np.where(x < 1, x, 1 / np.maximum(x, 1e-9) ** 2)
    ax.plot(x, V, color=fs.VEL, lw=1.8, label=r'$V(r)\ /\ (kQ/R)$')
    ax.plot(x, E, color=fs.FORCE, lw=1.5, ls='--', label=r'$E(r)\ /\ (kQ/R^2)$')
    ax.axvline(1, color=fs.GRAY, lw=0.8, ls=':')
    ax.annotate(r'중심: $\frac{3}{2}\,kQ/R$', xy=(0, 1.5), xytext=(0.35, 1.62), fontsize=9,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.text(1.05, 0.06, '$r = R$', fontsize=9, color=fs.GRAY)
    ax.set_xlim(0, 4); ax.set_ylim(0, 1.8)
    ax.set_xlabel('$r/R$'); ax.legend(fontsize=9, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig23_06')


# ---------------------------------------------------------------- 23.4
def fig07():
    """예제 23.5 원판 축 위의 V(z), E_z(z)."""
    fig, ax = fs.plot_axes(4.2, 2.7)
    x = np.linspace(0, 4, 400)
    V = np.sqrt(x ** 2 + 1) - x
    E = 1 - x / np.sqrt(x ** 2 + 1)
    ax.plot(x, V, color=fs.VEL, lw=1.8, label=r'$V(z)\ /\ (\sigma R/2\varepsilon_0)$')
    ax.plot(x, E, color=fs.FORCE, lw=1.5, ls='--', label=r'$E_z(z)\ /\ (\sigma/2\varepsilon_0)$')
    xx = np.linspace(0.35, 4, 200)
    ax.plot(xx, 1 / (2 * xx), color=fs.GRAY, lw=1.0, ls=':', label=r'점전하 $kQ/z$')
    ax.set_xlim(0, 4); ax.set_ylim(0, 1.15)
    ax.set_xlabel('$z/R$'); ax.legend(fontsize=9, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig23_07')


# ---------------------------------------------------------------- 23.5
def fig08():
    """점전하와 균일한 장의 전기력선과 등전위면."""
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.6))
    ax = axs[0]
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect('equal'); ax.axis('off')
    for k in range(12):
        a = 2 * np.pi * k / 12 + 0.13
        p0 = 0.2 * np.array([np.cos(a), np.sin(a)]); p1 = 2.0 * np.array([np.cos(a), np.sin(a)])
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=fs.FIELD, lw=0.9)
        ax.add_patch(FancyArrowPatch(1.25 * p1 / 2.0, 1.4 * p1 / 2.0, arrowstyle='-|>', mutation_scale=8, color=fs.FIELD, lw=0))
    # 같은 ΔV 간격의 등전위선: V = kq/r = V1·n → r = r1/n
    for n in (1, 2, 3, 4):
        r = 1.8 / n
        ax.add_patch(Circle((0, 0), r, fc='none', ec=fs.ORANGE, lw=1.1, ls='--'))
    fs.charge(ax, (0, 0), +1, r=0.17, fontsize=10)
    ax.set_title('(가) 점전하', fontsize=9, y=-0.08)
    ax = axs[1]
    ax.set_xlim(-0.2, 3.8); ax.set_ylim(-2, 2); ax.set_aspect('equal'); ax.axis('off')
    for y in np.linspace(-1.6, 1.6, 6):
        fs.arrow(ax, (0, y), (3.6, y), color=fs.FIELD, lw=0.9, ms=8)
    for x in np.linspace(0.5, 3.1, 4):
        ax.plot([x, x], [-1.9, 1.9], color=fs.ORANGE, lw=1.1, ls='--')
    ax.set_title('(나) 균일한 장', fontsize=9, y=-0.08)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig23_09')


def fig09():
    """전기 쌍극자의 전기력선과 등전위선."""
    fig, ax = fs.canvas(4.0, 3.2)
    xl, yl = (-2.5, 2.5), (-2.0, 2.0)
    ch = [(0, 0.5, 1), (0, -0.5, -1)]
    fs.field_lines(ax, ch, xl, yl, per_unit=14, lw=0.8, start_angle=360 / 28)
    X, Y = np.meshgrid(np.linspace(*xl, 400), np.linspace(*yl, 320))
    V = 1 / np.hypot(X, Y - 0.5) - 1 / np.hypot(X, Y + 0.5)
    lev = [-2.0, -1.0, -0.5, -0.2, 0.2, 0.5, 1.0, 2.0]
    ax.contour(X, Y, V, levels=lev, colors=fs.ORANGE, linewidths=1.0, linestyles='--')
    ax.contour(X, Y, V, levels=[0], colors=fs.ORANGE, linewidths=1.0, linestyles='--')
    fs.charge(ax, (0, 0.5), +1, r=0.16, fontsize=10)
    fs.charge(ax, (0, -0.5), -1, r=0.16, fontsize=10)
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal')
    ax.text(1.55, 0.1, '$V = 0$', fontsize=9, color=fs.ORANGE)
    fs.save(fig, __file__, 'fig23_10')


def fig10():
    """🐍 이완법: 위쪽 변 1 V인 상자의 등전위선."""
    N = 41
    V = np.zeros((N, N)); V[-1, :] = 1.0
    for it in range(20000):
        Vold = V.copy()
        V[1:-1, 1:-1] = 0.25 * (Vold[2:, 1:-1] + Vold[:-2, 1:-1] + Vold[1:-1, 2:] + Vold[1:-1, :-2])
        if np.abs(V - Vold).max() < 1e-7:
            break
    x = np.linspace(0, 1, N)
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    Ey, Ex = np.gradient(-V, 1 / (N - 1))
    ax.streamplot(x, x, Ex, Ey, color=fs.FIELD, linewidth=0.7, density=0.7, arrowsize=0.8,
                  start_points=np.c_[[0.08, 0.17, 0.27, 0.38, 0.62, 0.73, 0.83, 0.92], np.full(8, 0.97)])
    cs = ax.contour(x, x, V, levels=[0.05, 0.1, 0.25, 0.5, 0.75], colors=fs.ORANGE, linewidths=1.1)
    ax.clabel(cs, fmt='%.2f', fontsize=8, manual=[(0.5, 0.12), (0.5, 0.3), (0.62, 0.52), (0.5, 0.72), (0.5, 0.88)])
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=fs.BLACK, lw=1.5)
    ax.plot([0, 1], [1, 1], color=fs.FORCE, lw=3)
    ax.text(0.5, 1.04, '$V = 1\\ \\mathrm{V}$', ha='center', fontsize=9, color=fs.FORCE)
    ax.text(0.5, -0.07, '$V = 0$', ha='center', fontsize=9)
    ax.text(-0.04, 0.5, '$0$', ha='right', va='center', fontsize=9)
    ax.text(1.04, 0.5, '$0$', ha='left', va='center', fontsize=9)
    ax.plot(0.5, 0.5, 'o', color=fs.BLACK, ms=3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-0.1, 1.1); ax.set_ylim(-0.12, 1.12)
    fs.save(fig, __file__, 'fig23_08')


def fig11():
    """연결된 두 도체 구와 뾰족한 도체."""
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]
    ax.set_xlim(-1.0, 5.0); ax.set_ylim(-1.9, 1.4); ax.set_aspect('equal'); ax.axis('off')
    c1, R1 = np.array([0.0, 0.0]), 0.35
    c2, R2 = np.array([3.6, 0.0]), 1.05
    ax.plot([c1[0] + R1, c2[0] - R2], [0, 0], color=fs.BLACK, lw=1.0)
    for c, R, n, L, lab, ly in ((c1, R1, 8, 0.6, '$R_1,\\ Q_1$', -1.2), (c2, R2, 12, 0.2, '$R_2,\\ Q_2$', -1.55)):
        ax.add_patch(Circle(c, R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=3))
        for k in range(n):
            a_ = 2 * np.pi * (k + 0.5) / n
            u = np.array([np.cos(a_), np.sin(a_)])
            ax.text(*(c + 0.78 * R * u), '+', color=fs.POS, fontsize=7, ha='center', va='center', zorder=4)
            if (c is c1 and abs(a_) < 0.5) or (c is c2 and abs(a_ - np.pi) < 0.3):
                continue
            fs.arrow(ax, c + R * u, c + (R + L) * u, color=fs.FIELD, lw=1.0, ms=7)
        fs.label(ax, (c[0], ly), lab, fontsize=9)
    ax.set_title('(가) 연결된 두 구: $\\sigma_1/\\sigma_2 = R_2/R_1$', fontsize=9, y=-0.1)
    # (나) 뾰족한 도체(물방울 모양): 곡률 반지름이 작은 곳에 전하가 몰린다.
    ax = axs[1]
    ax.set_xlim(-1.3, 2.5); ax.set_ylim(-1.5, 1.4); ax.set_aspect('equal'); ax.axis('off')
    def shape(t):
        return np.c_[-0.9 * np.cos(t) + 0.3, 0.75 * np.sin(t) * ((1 + np.cos(t)) / 2) ** 0.7]
    t = np.linspace(0, 2 * np.pi, 1200)
    P = shape(t)
    ax.fill(P[:, 0], P[:, 1], fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=3)
    d1 = np.gradient(P, axis=0); d2 = np.gradient(d1, axis=0)
    kap = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]) / np.hypot(*d1.T) ** 3
    ds = np.hypot(*d1.T)
    tip = shape(np.array([np.pi]))[0]
    dist = np.hypot(*(P - tip).T)
    dens = 1 + 3.5 * np.exp(-dist / 0.35)          # 끝에 가까울수록 면전하 밀도가 크다(정성적)
    w = np.cumsum(dens * ds)
    marks = np.searchsorted(w, np.linspace(0, w[-1], 34, endpoint=False) + w[-1] / 68)
    def normal(i):
        nv = np.array([d1[i, 1], -d1[i, 0]]); nv /= np.linalg.norm(nv)
        if np.dot(nv, P[i] - np.array([0.1, 0])) < 0:
            nv = -nv
        return nv
    for i in marks:
        i = min(i, len(P) - 1)
        if abs(t[i] - np.pi) < 0.02:
            continue
        ax.text(*(P[i] - 0.11 * normal(i)), '+', color=fs.POS, fontsize=6.5, ha='center', va='center', zorder=4)
    for tt in (0.0, 0.8, 1.6, 2.3, 2 * np.pi - 0.8, 2 * np.pi - 1.6, 2 * np.pi - 2.3):
        i = int(np.argmin(np.abs(t - tt)))
        L = 0.22 + 0.5 * np.exp(-dist[i] / 0.35)
        fs.arrow(ax, P[i], P[i] + L * normal(i), color=fs.FIELD, lw=1.0, ms=7)
    fs.arrow(ax, tip, tip + np.array([1.0, 0]), color=fs.FIELD, lw=1.2, ms=8)
    ax.set_title('(나) 뾰족한 끝: 큰 $\\sigma$, 강한 $E$', fontsize=9, y=-0.1)
    fig.tight_layout(w_pad=0.3)
    fs.save(fig, __file__, 'fig23_11')


# ---------------------------------------------------------------- 연습문제
def fig12():
    """연습문제 1."""
    fig, ax = fs.canvas(3.4, 2.6, xlim=(-0.9, 5.0), ylim=(-0.95, 3.7))
    ax.plot([-0.5, 4.8], [0, 0], color=fs.GRAY, lw=0.7); ax.plot([0, 0], [-0.5, 3.6], color=fs.GRAY, lw=0.7)
    fs.label(ax, (4.85, 0.22), '$x$ (m)', fontsize=9, color=fs.GRAY, ha='right')
    fs.label(ax, (0.12, 3.55), '$y$ (m)', fontsize=9, color=fs.GRAY, ha='left')
    fs.charge(ax, (0, 0), +1, r=0.17, fontsize=10)
    fs.charge(ax, (4, 0), -1, r=0.17, fontsize=10)
    fs.label(ax, (0.1, -0.62), '$q_1 = +2.0\\ \\mu\\mathrm{C}$', fontsize=9)
    fs.label(ax, (3.8, -0.62), '$q_2 = -3.0\\ \\mu\\mathrm{C}$', fontsize=9)
    fs.dot(ax, (0, 3))
    fs.label(ax, (0.3, 3.2), '$P\\,(0,\\ 3.0)$', fontsize=9, ha='left')
    ax.plot([0, 4], [3, 0], color=fs.BLACK, lw=0.9, ls='--')
    fs.label(ax, (-0.12, 1.5), '3.0 m', fontsize=9, color=fs.GRAY, ha='right')
    fs.label(ax, (2.35, 1.75), '5.0 m', fontsize=9, color=fs.GRAY)
    fs.label(ax, (2.0, 0.22), '4.0 m', fontsize=9, color=fs.GRAY)
    fs.save(fig, __file__, 'fig23_12')


def fig13():
    """연습문제 2: 균일한 장 속 A→B의 두 경로."""
    fig, ax = fs.canvas(3.4, 2.8, xlim=(-0.08, 0.42), ylim=(-0.08, 0.47))
    for y in np.linspace(0.0, 0.44, 6):
        fs.arrow(ax, (-0.05, y), (0.40, y), color=fs.FIELD, lw=0.7, ms=7)
    fs.label(ax, (0.405, 0.465), r'$\vec{E}$', color=fs.FIELD, fontsize=10)
    A, B = np.array([0, 0]), np.array([0.30, 0.40])
    fs.arrow(ax, A, B, color=fs.BLACK, lw=1.5)
    fs.arrow(ax, A, (0.30, 0), color=fs.VEL, lw=1.4, ls='--')
    fs.arrow(ax, (0.30, 0), B, color=fs.VEL, lw=1.4, ls='--')
    fs.dot(ax, A, r=0.008); fs.dot(ax, B, r=0.008)
    fs.label(ax, (-0.03, -0.04), '$A\\,(0,0)$', fontsize=9, ha='left')
    fs.label(ax, (0.27, 0.415), '$B\\,(0.30,\\ 0.40)$', fontsize=9, ha='right', bbox=dict(fc='white', ec='none', pad=0.5))
    bb = dict(fc='white', ec='none', pad=0.5)
    fs.label(ax, (0.08, 0.2), '경로 1', fontsize=8.5, bbox=bb)
    fs.label(ax, (0.36, 0.2), '경로 2', fontsize=8.5, color=fs.VEL, bbox=bb)
    fs.save(fig, __file__, 'fig23_13')


def fig14():
    """연습문제 14: 접지된 도체 평면과 영상 전하."""
    fig, ax = fs.canvas(3.6, 3.2, xlim=(-2.2, 2.2), ylim=(-2.0, 2.0))
    xl, yl = (-2.2, 2.2), (-2.0, 2.0)
    d = 0.8
    L = lines_of([(0, d, 1), (0, -d, -1)], xl, yl, per_unit=14, start_angle=360 / 28)
    for pts in L:
        up = pts[:, 1] >= 0
        ax.plot(np.where(up, pts[:, 0], np.nan), np.where(up, pts[:, 1], np.nan), color=fs.FIELD, lw=0.9)
        ax.plot(np.where(~up, pts[:, 0], np.nan), np.where(~up, pts[:, 1], np.nan), color=fs.GRAY, lw=0.6, ls=':')
        sel = pts[up]
        if len(sel) > 20:
            mid_arrow(ax, sel, frac=0.45, xlim=xl, ylim=(0.05, 2.0))
    ax.add_patch(Rectangle((-2.2, -2.0), 4.4, 2.0, fc='#eeeeee', ec='none', zorder=0))
    ax.plot([-2.2, 2.2], [0, 0], color=fs.BLACK, lw=2.0, zorder=3)
    fs.charge(ax, (0, d), +1, r=0.16, fontsize=10)
    ax.add_patch(Circle((0, -d), 0.16, fc='white', ec=fs.NEG, lw=1.2, ls='--', zorder=7))
    ax.text(0, -d, '−', color=fs.NEG, ha='center', va='center', fontsize=10, zorder=8)
    fs.label(ax, (0.38, d + 0.12), '$q$', fontsize=11)
    fs.label(ax, (0.62, -d), '$-q$ (영상)', fontsize=9, color=fs.NEG)
    fs.dim(ax, (-0.7, 0), (-0.7, d), '$d$', off=0.0, color=fs.BLACK, fontsize=10)
    fs.label(ax, (1.35, -0.22), '접지된 도체 평면 $z = 0$', fontsize=8.5, zorder=9)
    ax.set_xlim(*xl); ax.set_ylim(*yl)
    fs.save(fig, __file__, 'fig23_14')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
        f()
