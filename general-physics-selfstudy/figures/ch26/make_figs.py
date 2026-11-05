"""26장 자기장과 자기력 그림 생성 스크립트.  python3 figures/ch26/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch, Wedge, Arc
from scipy.special import ellipk, ellipe

BB = dict(fc='white', ec='none', pad=0.5)
CUR = fs.VEL


def T(ax, p, s, **kw):
    kw.setdefault('fontsize', 10); kw.setdefault('ha', 'center'); kw.setdefault('va', 'center'); kw.setdefault('zorder', 10)
    ax.text(p[0], p[1], s, **kw)


def path_arrow(ax, xs, ys, i, color, ms=9):
    ax.add_patch(FancyArrowPatch((xs[i - 2], ys[i - 2]), (xs[i + 2], ys[i + 2]), arrowstyle='-|>',
                                 mutation_scale=ms, color=color, lw=0, zorder=6))


# ---------------------------------------------------------------- 26.1
def fig01():
    """로런츠 힘: F = qv×B는 v와 B가 이루는 면에 수직."""
    fig, ax = fs.canvas(3.8, 2.8, xlim=(-1.0, 4.6), ylim=(-1.0, 2.6))
    sk = np.array([0.75, 0.45])                 # 지면 안쪽 방향(빗각 투영)
    O = np.array([0.0, 0.0])
    plane = [O - 0.6 * sk + np.array([-0.3, 0]), O - 0.6 * sk + np.array([3.2, 0]),
             O + 1.6 * sk + np.array([3.2, 0]), O + 1.6 * sk + np.array([-0.3, 0])]
    ax.add_patch(Polygon(plane, closed=True, fc='#eef1f6', ec=fs.GRAY, lw=0.7))
    B = np.array([2.6, 0.0])
    phi = np.radians(40)
    v = 2.0 * (np.cos(phi) * np.array([1, 0]) + np.sin(phi) * sk / np.linalg.norm(sk) * 1.25)
    fs.vec(ax, O, B, color=fs.FIELD, lw=1.8)
    T(ax, B + np.array([0.2, -0.15]), '$\\vec{B}$', color=fs.FIELD, fontsize=11)
    fs.vec(ax, O, v, color=fs.VEL, lw=1.8)
    T(ax, v + np.array([0.12, 0.15]), '$\\vec{v}$', color=fs.VEL, fontsize=11)
    fs.vec(ax, O, (0, 2.1), color=fs.FORCE, lw=1.8)
    T(ax, (0.55, 2.2), '$\\vec{F}_B = q\\vec{v}\\times\\vec{B}$', color=fs.FORCE, fontsize=10, ha='left')
    t = np.linspace(0, 1, 30)
    arc = np.array([(1 - s) * B / np.linalg.norm(B) + s * v / np.linalg.norm(v) for s in t])
    arc = 0.75 * arc / np.linalg.norm(arc, axis=1)[:, None] * np.array([1, 1])
    ax.plot(arc[:, 0], arc[:, 1], color=fs.BLACK, lw=0.9)
    T(ax, (0.95, 0.28), '$\\phi$', fontsize=10)
    ax.plot(*O, 'o', color=fs.BLACK, ms=4)
    T(ax, (-0.25, -0.2), '$q$', fontsize=10)
    fs.save(fig, __file__, 'fig26_01')


def loop_psi(R, Z, a, z0):
    """반지름 a, 위치 z0인 원형 전류 고리의 자기 선속 함수 ψ = ρA_φ (상수 인자 생략)."""
    k2 = 4 * a * R / ((a + R) ** 2 + (Z - z0) ** 2 + 1e-12)
    k2 = np.clip(k2, 0, 1 - 1e-9)
    k = np.sqrt(k2)
    Aphi = np.sqrt(a / (R + 1e-12)) * ((1 - k2 / 2) * ellipk(k2) - ellipe(k2)) / (k + 1e-12)
    return R * Aphi


def fig02():
    """막대자석의 자기력선: 자석 안을 지나 닫힌 곡선."""
    fig, ax = fs.canvas(4.4, 3.0)
    Lm, a = 2.0, 0.35
    x = np.linspace(-3.2, 3.2, 500); y = np.linspace(-2.2, 2.2, 360)
    X, Y = np.meshgrid(x, y)
    psi = sum(loop_psi(np.abs(Y), X, a, z0) for z0 in np.linspace(-Lm / 2, Lm / 2, 40))
    levels = np.array([0.15, 0.4, 0.8, 1.4, 2.2, 3.2, 4.5]) * psi.max() / 6.5
    cs = ax.contour(X, Y, psi, levels=levels, colors=fs.FIELD, linewidths=0.9)
    # 화살표: 자석 밖에서는 N(오른쪽)→S(왼쪽)이므로 x = 0 부근(자석 위·아래)에서 왼쪽을 향한다
    for lev_paths in cs.allsegs:
        for seg in lev_paths:
            ok = np.where(np.abs(seg[:, 1]) > a + 0.15)[0]
            ok = ok[(ok > 2) & (ok < len(seg) - 3)]
            if len(ok) == 0:
                continue
            i = ok[np.argmin(np.abs(seg[ok, 0]))]
            if abs(seg[i, 0]) > 0.3:
                continue
            p = seg[i]
            ax.add_patch(FancyArrowPatch(p + np.array([0.06, 0]), p - np.array([0.1, 0]), arrowstyle='-|>', mutation_scale=9, color=fs.FIELD, lw=0, zorder=6))
    ax.add_patch(Rectangle((-Lm / 2, -a), Lm / 2, 2 * a, fc='#9dbbe0', ec=fs.BLACK, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((0, -a), Lm / 2, 2 * a, fc='#e8a39b', ec=fs.BLACK, lw=1.0, zorder=4))
    T(ax, (-0.5, 0), 'S', fontsize=12, zorder=5); T(ax, (0.5, 0), 'N', fontsize=12, zorder=5)
    fs.arrow(ax, (-0.25, -0.2), (0.25, -0.2), color=fs.FIELD, lw=1.2, ms=8, zorder=6)
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-2.2, 2.2); ax.set_aspect('equal')
    fs.save(fig, __file__, 'fig26_02')


# ---------------------------------------------------------------- 26.2
def fig03():
    """균일한 자기장(⊙) 속의 원운동: 양전하는 시계 방향, 음전하는 반시계 방향."""
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.6))
    for ax, sg, ti in zip(axs, (1, -1), ('(가) 양전하: 시계 방향', '(나) 음전하: 반시계 방향')):
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.5, 1.6); ax.set_aspect('equal'); ax.axis('off')
        fs.field_grid(ax, (-1.6, 1.6), (-1.5, 1.6), kind='out', step=0.52, r=0.05)
        r = 1.0
        ax.add_patch(Circle((0, 0), r, fc='none', ec=fs.BLACK, lw=1.2, zorder=3))
        t = np.linspace(0, 2 * np.pi, 200); xs, ys = r * np.cos(t), r * np.sin(t)
        for ang in (np.pi / 2 + 0.5, -np.pi / 2 + 0.5):
            i = int(ang % (2 * np.pi) / (2 * np.pi) * 200)
            if sg > 0:
                ax.add_patch(FancyArrowPatch((xs[i + 2], ys[i + 2]), (xs[i - 2], ys[i - 2]), arrowstyle='-|>', mutation_scale=9, color=fs.BLACK, lw=0, zorder=6))
            else:
                path_arrow(ax, xs, ys, i, fs.BLACK)
        p = np.array([0, r])
        fs.charge(ax, p, sg, r=0.13, fontsize=9)
        vdir = np.array([sg * 1.0, 0])
        fs.vec(ax, p + 0.15 * vdir, 0.65 * vdir, color=fs.VEL, lw=1.6)
        T(ax, p + 0.95 * vdir + np.array([0, 0.18]), '$\\vec{v}$', color=fs.VEL)
        fs.vec(ax, p + np.array([0, -0.15]), (0, -0.55), color=fs.FORCE, lw=1.6)
        T(ax, (0.28, 0.25), '$\\vec{F}$', color=fs.FORCE)
        ax.plot([0, r * np.cos(-0.6)], [0, r * np.sin(-0.6)], color=fs.GRAY, lw=0.8)
        T(ax, (0.45, -0.1), '$r$', fontsize=9, color=fs.GRAY)
        ax.set_title(ti, fontsize=9, y=-0.1)
    T(axs[0], (-1.25, 1.45), '$\\vec{B}$ ⊙', fontsize=9, color=fs.FIELD, bbox=BB)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig26_03')


def fig04():
    """나선 운동."""
    fig, ax = fs.canvas(4.6, 2.3, xlim=(-0.5, 6.2), ylim=(-1.3, 1.6))
    r, ry, p = 0.75, 0.28, 1.5
    t = np.linspace(0, 3.4 * 2 * np.pi, 1200)
    xs = 0.3 + p * t / (2 * np.pi) + 0.0 * np.sin(t)
    zs = r * np.cos(t); ys = ry * np.sin(t)
    X, Y = xs + 0.45 * np.sin(t), zs
    front = np.sin(t) < 0
    ax.plot(np.where(front, X, np.nan), np.where(front, Y, np.nan), color=fs.VEL, lw=1.4)
    ax.plot(np.where(~front, X, np.nan), np.where(~front, Y, np.nan), color=fs.VEL, lw=0.9, ls='--', alpha=0.7)
    for y0 in (-1.1, 1.3):
        fs.arrow(ax, (-0.3, y0), (6.0, y0), color=fs.FIELD, lw=1.0, ms=8)
    T(ax, (6.05, 1.5), '$\\vec{B}$', color=fs.FIELD)
    ax.plot([0, 6.0], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    k = int(np.argmin(np.abs(t - 4 * np.pi)))
    P = np.array([X[k], Y[k]])
    fs.vec(ax, P, (0.9, 0), color=fs.VEL, lw=1.4)
    T(ax, P + np.array([1.15, 0.12]), '$v_\\parallel$', color=fs.VEL, fontsize=9)
    fs.vec(ax, P, (0, -0.65), color=fs.ACC, lw=1.4)
    T(ax, P + np.array([0.25, -0.5]), '$v_\\perp$', color=fs.ACC, fontsize=9)
    k1 = int(np.argmin(np.abs(t - 2 * np.pi))); k2 = int(np.argmin(np.abs(t - 4 * np.pi)))
    fs.dim(ax, (X[k1], r), (X[k2], r), '피치 $p$', off=0.3, color=fs.BLACK, fontsize=9)
    k3 = int(np.argmin(np.abs(t - 6 * np.pi)))
    ax.plot([X[k3], X[k3]], [0, -r], color=fs.BLACK, lw=0.8)
    T(ax, (X[k3] + 0.15, -0.35), '$r$', fontsize=9)
    fs.save(fig, __file__, 'fig26_04')


def fig05():
    """속도 선택기."""
    fig, ax = fs.canvas(4.6, 2.5, xlim=(-1.4, 5.4), ylim=(-1.45, 1.55))
    L, h = 4.0, 1.0
    ax.add_patch(Rectangle((0, h), L, 0.1, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((0, -h - 0.1), L, 0.1, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    for xx in np.linspace(0.2, L - 0.2, 10):
        T(ax, (xx, h + 0.25), '+', color=fs.POS, fontsize=8)
        T(ax, (xx, -h - 0.25), '−', color=fs.NEG, fontsize=8)
    fs.field_grid(ax, (0, L), (-h, h), kind='in', step=0.5, r=0.05)
    for xx in (0.5, 3.5):
        fs.arrow(ax, (xx, 0.85), (xx, 0.35), color=fs.FIELD, lw=1.0, ms=7)
    T(ax, (3.75, 0.62), '$\\vec{E}$', color=fs.FIELD, fontsize=10)
    T(ax, (4.35, -0.75), '$\\vec{B}$ ⊗', color=fs.FIELD, fontsize=9, ha='left')
    x = np.linspace(0, L + 0.8, 100)
    ax.plot(np.r_[-1.2, x], np.r_[0, 0 * x], color=fs.BLACK, lw=1.3)
    ax.plot(x, 0.045 * x ** 2, color=fs.GRAY, lw=1.0, ls='--')
    ax.plot(x, -0.045 * x ** 2, color=fs.GRAY, lw=1.0, ls='--')
    T(ax, (L + 0.95, 0.95), '$v > E/B$', fontsize=8.5, ha='left')
    T(ax, (L + 0.95, 0.0), '$v = E/B$', fontsize=8.5, ha='left')
    T(ax, (L + 0.95, -0.95), '$v < E/B$', fontsize=8.5, ha='left')
    P = np.array([1.8, 0.0])
    fs.charge(ax, P, +1, r=0.12, fontsize=8)
    fs.vec(ax, P + np.array([0.15, 0]), (0.6, 0), color=fs.VEL, lw=1.5)
    T(ax, P + np.array([0.85, 0.15]), '$\\vec{v}$', color=fs.VEL, fontsize=9)
    fs.vec(ax, P + np.array([0, 0.14]), (0, 0.55), color=fs.FORCE, lw=1.5)
    T(ax, P + np.array([-0.45, 0.6]), '$q\\vec{v}\\times\\vec{B}$', color=fs.FORCE, fontsize=8.5)
    fs.vec(ax, P + np.array([0, -0.14]), (0, -0.55), color=fs.FORCE, lw=1.5)
    T(ax, P + np.array([-0.35, -0.6]), '$q\\vec{E}$', color=fs.FORCE, fontsize=8.5)
    fs.save(fig, __file__, 'fig26_05')


def fig06():
    """★ 교차된 장 속의 운동: 처음 속도에 따른 궤적(연습문제 15)."""
    fig, ax = fs.plot_axes(4.6, 2.6)
    t = np.linspace(0, 3 * 2 * np.pi, 1500)
    for v0, col, lab in ((0.0, fs.VEL, '$v_0 = 0$'), (1.0, fs.BLACK, '$v_0 = E/B$'), (2.0, fs.FORCE, '$v_0 = 2E/B$')):
        z = t + (v0 - 1) * (np.exp(-1j * t) - 1) / (-1j)    # 단위: 길이 E/(ωB), 시간 1/ω
        ax.plot(z.real, z.imag, color=col, lw=1.6, label=lab)
    ax.set_xlim(0, 19); ax.set_ylim(-2.6, 2.6); ax.set_aspect('equal')
    ax.set_xlabel('$x\\ /\\ (E/\\omega B)$', fontsize=9); ax.set_ylabel('$y\\ /\\ (E/\\omega B)$', fontsize=9)
    ax.legend(fontsize=8, frameon=False, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 1.0))
    fs.save(fig, __file__, 'fig26_06')


def fig07():
    """자기장 섹터형 질량분석기(예제 26.3, 두 궤도의 차이는 과장)."""
    fig, ax = fs.canvas(4.4, 3.1, xlim=(-1.4, 5.4), ylim=(-1.9, 2.9))
    ax.add_patch(Rectangle((-0.6, 0), 6.0, 2.85, fc='#f3eef7', ec='none', zorder=0))
    fs.field_grid(ax, (-0.6, 5.4), (0, 2.85), kind='out', step=0.5, r=0.05)
    r1, r2 = 2.0, 2.25
    for r, col, lab in ((r1, fs.VEL, '$300\\ \\mathrm{u}$'), (r2, fs.FORCE, '$301\\ \\mathrm{u}$')):
        th = np.linspace(np.pi, 0, 200)
        xs, ys = r + r * np.cos(th), r * np.sin(th)
        ax.plot(xs, ys, color=col, lw=1.5, zorder=3)
        path_arrow(ax, xs, ys, 60, col)
        T(ax, (r, r - 0.22 if r == r1 else r + 0.22), lab, color=col, fontsize=8.5, bbox=BB)
    ax.add_patch(Rectangle((3.6, -0.12), 1.5, 0.12, fc=fs.BLACK, ec='none', zorder=4))
    T(ax, (4.35, -0.35), '검출기', fontsize=8.5)
    ax.plot([-0.6, 3.6], [0, 0], color=fs.BLACK, lw=1.2)
    ax.plot([-0.3, 0.3], [-0.6, -0.6], color=fs.BLACK, lw=2.0)
    ax.plot([-0.3, -0.06], [-1.5, -1.5], color=fs.BLACK, lw=2.0); ax.plot([0.06, 0.3], [-1.5, -1.5], color=fs.BLACK, lw=2.0)
    ax.plot([0, 0], [-1.75, 0], color=fs.BLACK, lw=1.2)
    fs.arrow(ax, (0, -1.3), (0, -0.85), color=fs.BLACK, lw=1.3, ms=9)
    T(ax, (-0.55, -1.05), '$V$', fontsize=10)
    T(ax, (-0.85, -1.7), '이온원', fontsize=8.5)
    fs.dim(ax, (0, 0), (2 * r1, 0), '$2r$ (300 u)', off=-0.95, color=fs.GRAY, fontsize=9)
    T(ax, (4.9, 2.6), '$\\vec{B}$ ⊙', color=fs.FIELD, fontsize=9, bbox=BB)
    fs.save(fig, __file__, 'fig26_07')


def fig08():
    """사이클로트론(위에서 본 그림)."""
    fig, ax = fs.canvas(3.4, 3.3, xlim=(-2.1, 2.3), ylim=(-2.75, 2.2))
    R, g = 1.8, 0.12
    ax.add_patch(Wedge((g, 0), R, -90, 90, fc='#e5ecf5', ec=fs.BLACK, lw=1.2))
    ax.add_patch(Wedge((-g, 0), R, 90, 270, fc='#e5ecf5', ec=fs.BLACK, lw=1.2))
    # 디 안에서는 반원, 틈을 지날 때마다 가속되어 반지름이 커진다(시계 방향, B ⊙인 양이온).
    pts, y = [], 0.0
    for n in range(1, 40):
        r = 0.36 * np.sqrt(n)
        if r > R - 0.12:
            break
        if n % 2 == 1:
            cx, th = g, np.linspace(np.pi / 2, -np.pi / 2, 60)
            cy = y - r
        else:
            cx, th = -g, np.linspace(-np.pi / 2, -3 * np.pi / 2, 60)
            cy = y + r
        xs, ys = cx + r * np.cos(th), cy + r * np.sin(th)
        pts.extend(zip(xs, ys)); y = ys[-1]
    P = np.array(pts)
    P[:, 1] -= cy                       # 가장 바깥 궤도의 중심을 원점에 맞춘다
    ax.plot(P[:, 0], P[:, 1], color=fs.FORCE, lw=1.1, zorder=3)
    for i in range(45, len(P) - 5, 120):
        path_arrow(ax, P[:, 0], P[:, 1], i, fs.FORCE, ms=8)
    ax.plot(*P[0], 'o', color=fs.BLACK, ms=3.5, zorder=5)
    ax.plot([-1.0, -1.0, -0.3], [-1.5, -2.35, -2.35], color=fs.BLACK, lw=0.9)
    ax.plot([1.0, 1.0, 0.3], [-1.5, -2.35, -2.35], color=fs.BLACK, lw=0.9)
    ax.add_patch(Circle((0, -2.35), 0.3, fc='white', ec=fs.BLACK, lw=1.0, zorder=4))
    tt = np.linspace(-0.2, 0.2, 50); ax.plot(tt, -2.35 + 0.1 * np.sin(tt * np.pi / 0.2), color=fs.BLACK, lw=0.9, zorder=5)
    T(ax, (0.0, -2.62 + 0.0), '교류 전원 ($f = qB/2\\pi m$)', fontsize=8.5, va='top')
    T(ax, (-1.45, 1.75), '디', fontsize=9); T(ax, (1.45, 1.75), '디', fontsize=9)
    T(ax, (1.85, 2.05), '$\\vec{B}$ ⊙', color=fs.FIELD, fontsize=9)
    fs.save(fig, __file__, 'fig26_08')


# ---------------------------------------------------------------- 26.3
def fig09():
    """홀 효과(위에서 본 띠, B는 지면에서 나오는 방향)."""
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-1.4, 5.6), ylim=(-1.75, 1.85))
    L, w = 4.0, 2.0
    ax.add_patch(Rectangle((0, -w / 2), L, w, fc='#efe3cb', ec=fs.BLACK, lw=1.2))
    fs.field_grid(ax, (0.2, L - 0.2), (-w / 2 + 0.1, w / 2 - 0.1), kind='out', step=0.6, r=0.05, color='#b79ac9')
    for xx in np.linspace(0.3, L - 0.3, 9):
        T(ax, (xx, w / 2 - 0.12), '+', color=fs.POS, fontsize=8)
        T(ax, (xx, -w / 2 + 0.12), '−', color=fs.NEG, fontsize=9)
    ax.plot([-1.0, 0], [0, 0], color=fs.BLACK, lw=1.2); ax.plot([L, L + 1.0], [0, 0], color=fs.BLACK, lw=1.2)
    fs.arrow(ax, (-1.0, 0), (-0.3, 0), color=CUR, lw=1.5)
    T(ax, (-0.65, 0.25), '$I$', color=CUR)
    P = np.array([2.4, 0.15])
    ax.add_patch(Circle(P, 0.11, fc=fs.NEG, ec='none', zorder=7))
    T(ax, P, '−', color='white', fontsize=8, fontweight='bold', zorder=8)
    fs.vec(ax, P - np.array([0.13, 0]), (-0.6, 0), color=fs.VEL, lw=1.5)
    T(ax, P + np.array([-0.95, 0.2]), '$\\vec{v}_d$', color=fs.VEL, fontsize=9)
    fs.vec(ax, P - np.array([0, 0.13]), (0, -0.5), color=fs.FORCE, lw=1.5)
    T(ax, P + np.array([0.55, -0.45]), '$q\\vec{v}_d\\times\\vec{B}$', color=fs.FORCE, fontsize=8.5)
    fs.arrow(ax, (3.3, 0.6), (3.3, -0.15), color=fs.FIELD, lw=1.3, ms=8)
    T(ax, (3.2, 0.25), '$\\vec{E}_H$', color=fs.FIELD, fontsize=9.5, ha='right', bbox=BB)
    ax.add_patch(FancyArrowPatch((L + 0.45, w / 2), (L + 0.45, -w / 2), arrowstyle='<|-|>', mutation_scale=7, color=fs.BLACK, lw=0.8))
    T(ax, (L + 0.65, -0.45), '$w$', ha='left')
    ax.plot([1.0, 1.0, -0.9], [w / 2, w / 2 + 0.55, w / 2 + 0.55], color=fs.BLACK, lw=0.9)
    ax.plot([1.0, 1.0, -0.9, -0.9], [-w / 2, -w / 2 - 0.55, -w / 2 - 0.55, w / 2 + 0.55], color=fs.BLACK, lw=0.9)
    ax.add_patch(Circle((-0.9, 0.95), 0.32, fc='white', ec=fs.BLACK, lw=1.2, zorder=5))
    T(ax, (-0.9, 0.95), 'V', zorder=6)
    T(ax, (-0.35, 1.25), '$V_H$', fontsize=9.5, ha='left')
    T(ax, (2.6, -1.62), '$\\vec{B}$ ⊙,  두께 $t$', fontsize=9, color=fs.FIELD)
    fs.save(fig, __file__, 'fig26_09')


# ---------------------------------------------------------------- 26.4
def fig10():
    """자기장 속 직선 도선이 받는 힘."""
    fig, ax = fs.canvas(3.6, 2.3, xlim=(-0.3, 4.5), ylim=(-1.2, 1.8))
    fs.field_grid(ax, (-0.3, 4.5), (-1.2, 1.8), kind='in', step=0.55, r=0.05)
    ax.plot([0.0, 4.2], [0, 0], color='#b07a2a', lw=5, solid_capstyle='round', zorder=3)
    fs.arrow(ax, (0.6, 0), (1.4, 0), color=CUR, lw=1.8, zorder=7)
    T(ax, (1.0, -0.3), '$I$', color=CUR, bbox=BB)
    fs.dim(ax, (0.0, 0), (4.2, 0), '$\\vec{L}$', off=-0.75, color=fs.BLACK)
    fs.vec(ax, (2.6, 0.1), (0, 1.2), color=fs.FORCE, lw=2.0)
    T(ax, (3.35, 1.25), '$\\vec{F} = I\\vec{L}\\times\\vec{B}$', color=fs.FORCE, fontsize=9.5, bbox=BB)
    T(ax, (0.25, 1.55), '$\\vec{B}$ ⊗', color=fs.FIELD, fontsize=9, bbox=BB)
    fs.save(fig, __file__, 'fig26_10')


def fig11():
    """예제 26.6: 반원 도선이 받는 힘."""
    fig, ax = fs.canvas(3.8, 2.8, xlim=(-1.9, 1.9), ylim=(-1.25, 1.65))
    fs.field_grid(ax, (-1.9, 1.9), (-1.25, 1.65), kind='out', step=0.48, r=0.045, color='#b79ac9')
    R = 1.2
    th = np.linspace(np.pi, 0, 300)
    xs, ys = R * np.cos(th), R * np.sin(th)
    ax.plot(xs, ys, color='#b07a2a', lw=3.5, zorder=3)
    path_arrow(ax, xs, ys, 60, CUR, ms=11); path_arrow(ax, xs, ys, 240, CUR, ms=11)
    for ang in np.radians([150, 90, 30]):
        p = R * np.array([np.cos(ang), np.sin(ang)])
        fs.vec(ax, p, -0.42 * p / R, color=fs.FORCE, lw=1.3, ms=9)
    T(ax, (0.12, 0.62), '$d\\vec{F}$', color=fs.FORCE, fontsize=9)
    ang = np.radians(55); p = R * np.array([np.cos(ang), np.sin(ang)])
    tdir = np.array([np.sin(ang), -np.cos(ang)])
    fs.vec(ax, p, 0.45 * tdir, color=CUR, lw=1.4, ms=9)
    T(ax, p + 0.45 * tdir + np.array([0.22, 0.05]), '$d\\vec{\\ell}$', color=CUR, fontsize=9)
    ax.plot([0, R * np.cos(np.radians(125))], [0, R * np.sin(np.radians(125))], color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, (0, 0), 0.3, 0, 125, '$\\theta$', fontsize=9, tr=0.45)
    ax.plot([-R, R], [0, 0], color=fs.GRAY, lw=0.9, ls='--')
    fs.arrow(ax, (-R, -0.22), (R, -0.22), color=fs.GRAY, lw=1.0, ms=8)
    T(ax, (0.0, -0.45), '$\\vec{L}_{ab} = 2R\\,\\hat{i}$', color=fs.GRAY, fontsize=9, bbox=BB)
    T(ax, (-R - 0.18, 0.15), '$a$', fontsize=10); T(ax, (R + 0.18, 0.15), '$b$', fontsize=10)
    fs.vec(ax, (0, -0.65), (0, -0.5), color=fs.FORCE, lw=2.0)
    T(ax, (0.75, -1.0), '$\\vec{F} = -2IRB\\,\\hat{j}$', color=fs.FORCE, fontsize=9, bbox=BB)
    T(ax, (-1.45, 1.5), '$\\vec{B}$ ⊙', color=fs.FIELD, fontsize=9, bbox=BB)
    fs.save(fig, __file__, 'fig26_11')


# ---------------------------------------------------------------- 26.5
def fig12():
    """직사각형 고리의 토크: (가) 정면, (나) 회전축 방향에서 본 그림."""
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.8), gridspec_kw=dict(width_ratios=[1, 1.25]))
    ax = axs[0]
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.55, 1.5); ax.set_aspect('equal'); ax.axis('off')
    b2, a2 = 0.9, 1.1
    ax.add_patch(Rectangle((-b2, -a2), 2 * b2, 2 * a2, fc='#f3f6fa', ec='#b07a2a', lw=2.5))
    ax.plot([0, 0], [-1.45, 1.45], color=fs.GRAY, lw=0.9, ls='-.')
    T(ax, (0.22, 1.38), '축', fontsize=8.5, color=fs.GRAY)
    for p, q in (((-b2, a2 - 0.6), (-b2, -a2 + 0.6)), ((-b2 + 0.5, -a2), (b2 - 0.5, -a2)), ((b2, -a2 + 0.6), (b2, a2 - 0.6)), ((b2 - 0.5, a2), (-b2 + 0.5, a2))):
        fs.arrow(ax, p, q, color=CUR, lw=1.6, ms=10)
    T(ax, (-b2 - 0.25, 0), '$a$', fontsize=10); T(ax, (0.35, -a2 - 0.25), '$b$', fontsize=10)
    T(ax, (b2 + 0.28, 0.45), '$I$', color=CUR)
    fs.dot_out(ax, (0.45, 0.35), r=0.1)
    T(ax, (0.45, 0.65), '$\\hat{n}$', fontsize=10)
    ax.set_title('(가) 정면: $\\hat{n}$은 지면에서 나옴', fontsize=9, y=-0.1)
    ax = axs[1]
    ax.set_xlim(-1.9, 2.0); ax.set_ylim(-1.6, 1.6); ax.set_aspect('equal'); ax.axis('off')
    for y0 in (-1.45, 1.45):
        fs.arrow(ax, (-1.8, y0), (1.9, y0), color=fs.FIELD, lw=1.0, ms=8)
    T(ax, (1.85, 1.25), '$\\vec{B}$', color=fs.FIELD)
    alpha = np.radians(120); hb = 0.85
    P1 = hb * np.array([np.cos(alpha), np.sin(alpha)]); P2 = -P1
    ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color='#b07a2a', lw=3)
    ax.plot(0, 0, 'o', color=fs.BLACK, ms=4)
    fs.dot_out(ax, P1, r=0.12); fs.cross_in(ax, P2, r=0.12)
    fs.vec(ax, P1 + np.array([0, 0.14]), (0, 0.5), color=fs.FORCE, lw=1.6)
    fs.vec(ax, P2 - np.array([0, 0.14]), (0, -0.5), color=fs.FORCE, lw=1.6)
    T(ax, P1 + np.array([-0.42, 0.45]), '$IaB$', color=fs.FORCE, fontsize=9)
    T(ax, P2 + np.array([0.42, -0.45]), '$IaB$', color=fs.FORCE, fontsize=9)
    n = np.array([np.sin(alpha), -np.cos(alpha)])
    fs.vec(ax, (0, 0), 0.95 * n, color=fs.BLACK, lw=1.5)
    T(ax, 1.15 * n + np.array([0.05, 0.08]), '$\\hat{n}$', fontsize=10)
    ax.plot([0, 1.0], [0, 0], color=fs.GRAY, lw=0.8, ls='--')
    fs.angle_arc(ax, (0, 0), 0.55, 0, np.degrees(np.arctan2(n[1], n[0])), '$\\theta$', fontsize=9, tr=0.75)
    ax.plot([P1[0], P1[0]], [P1[1], -1.05], color=fs.GRAY, lw=0.6, ls=':')
    ax.plot([P2[0], P2[0]], [P2[1], -1.05], color=fs.GRAY, lw=0.6, ls=':')
    ax.add_patch(FancyArrowPatch((P1[0], -1.0), (P2[0], -1.0), arrowstyle='<|-|>', mutation_scale=7, color=fs.BLACK, lw=0.8))
    T(ax, (0, -0.82), '$b\\sin\\theta$', fontsize=9)
    T(ax, P1 + np.array([0.6, 0.0]) * 0.0 + np.array([-0.3, -0.25]), '', fontsize=9)
    ax.set_title('(나) 축 방향에서 본 그림', fontsize=9, y=-0.1)
    fig.tight_layout(w_pad=0.3)
    fs.save(fig, __file__, 'fig26_12')


def fig13():
    """예제 26.7: U(θ) = −μB cosθ와 토크 크기 μB sinθ."""
    mu, B = 50 * 0.50 * np.pi * 0.020 ** 2, 0.30
    th = np.linspace(0, 180, 300)
    U = -mu * B * np.cos(np.radians(th)) * 1e3
    tau = mu * B * np.sin(np.radians(th)) * 1e3
    fig, ax = fs.plot_axes(4.2, 2.6)
    ax.plot(th, U, color=fs.VEL, lw=1.8, label='$U$ (mJ)')
    ax.plot(th, tau, color=fs.FORCE, lw=1.5, ls='--', label='$\\tau$ (mN·m)')
    U30 = -mu * B * np.cos(np.radians(30)) * 1e3; t30 = mu * B * 0.5 * 1e3
    ax.plot([30, 30], [U30, t30], 'o', color=fs.BLACK, ms=4)
    ax.text(34, U30 - 0.3, '$\\theta = 30^\\circ$: $U = -8.2$', fontsize=8.5, va='top')
    ax.text(34, t30 + 0.2, '$\\tau = 4.7$', fontsize=8.5)
    ax.annotate('', xy=(178, mu * B * 1e3), xytext=(178, -mu * B * 1e3),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(172, 0.6, '$2\\mu B$', fontsize=9, color=fs.GRAY, ha='right')
    ax.set_xlim(0, 180); ax.set_ylim(-11, 11); ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax.set_xlabel('$\\vec{\\mu}$와 $\\vec{B}$ 사이의 각 $\\theta$ (°)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper left')
    fs.save(fig, __file__, 'fig26_13')


# ---------------------------------------------------------------- 연습문제
def fig14():
    """연습문제 9: 절반만 자기장 속에 있는 정사각형 고리."""
    fig, ax = fs.canvas(3.4, 2.5, xlim=(-1.6, 2.2), ylim=(-1.35, 1.45))
    ax.add_patch(Rectangle((0, -1.35), 2.2, 2.8, fc='#f3eef7', ec='none', zorder=0))
    fs.field_grid(ax, (0, 2.2), (-1.35, 1.45), kind='in', step=0.45, r=0.045)
    ax.plot([0, 0], [-1.35, 1.45], color=fs.FIELD, lw=1.0, ls='--')
    s = 1.0
    ax.add_patch(Rectangle((-s, -s), 2 * s, 2 * s, fc='none', ec='#b07a2a', lw=2.5, zorder=3))
    for p, q in (((-s, 0.3), (-s, -0.3)), ((-0.3, -s), (0.3, -s)), ((s, -0.3), (s, 0.3)), ((0.3, s), (-0.3, s))):
        fs.arrow(ax, p, q, color=CUR, lw=1.5, ms=9, zorder=6)
    T(ax, (-s - 0.25, 0), '$I$', color=CUR)
    fs.dim(ax, (-s, s), (s, s), '$L$', off=0.25, color=fs.BLACK)
    ax.texts[-1].set_position((-0.35, s + 0.42)); ax.texts[-1].set_bbox(BB)
    T(ax, (1.65, 1.25), '$\\vec{B}$ ⊗', color=fs.FIELD, fontsize=9, bbox=BB)
    T(ax, (-0.55, -1.2), '장 없음', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig26_14')


def fig15():
    """연습문제 11: 레일 위의 금속 막대(위에서 본 그림)."""
    fig, ax = fs.canvas(3.8, 2.3, xlim=(-1.0, 4.4), ylim=(-1.3, 1.5))
    for y in (1.0, -1.0):
        ax.add_patch(Rectangle((-0.6, y - 0.07), 4.8, 0.14, fc='#999999', ec=fs.BLACK, lw=0.8))
    ax.add_patch(Rectangle((1.9, -1.15), 0.2, 2.3, fc='#d9c7a7', ec=fs.BLACK, lw=1.0, zorder=3))
    fs.arrow(ax, (2.0, 0.6), (2.0, -0.2), color=CUR, lw=1.6, zorder=6)
    T(ax, (2.3, 0.35), '$I$', color=CUR)
    for x in (-0.3, 0.7, 3.2, 4.0):
        for y in (-0.45, 0.45):
            fs.dot_out(ax, (x, y), r=0.06, color=fs.FIELD)
    fs.dim(ax, (1.6, 1.0), (1.6, -1.0), '$L$', off=0.0, color=fs.BLACK)
    T(ax, (0.2, 1.35), '레일', fontsize=8.5, color=fs.GRAY)
    T(ax, (3.6, 1.32), '$\\vec{B}$ ⊙ (연직 위)', color=fs.FIELD, fontsize=8.5)
    fs.save(fig, __file__, 'fig26_15')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15):
        f()
