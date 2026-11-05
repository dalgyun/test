"""30장 맥스웰 방정식과 물질의 자성 — 그림 생성 스크립트.
python3 figures/ch30/make_figs.py  (FIG_PREVIEW=<폴더> 를 주면 PNG 미리보기도 저장)
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon, Ellipse, PathPatch
from matplotlib.path import Path
from scipy.special import ellipk, ellipe

F = fs.FIELD
NCOL, SCOL = '#d9534f', '#5b8bd0'


# ---------- 도우미 ----------
def tip(ax, p, d, color=F, ms=10, zorder=6):
    p = np.asarray(p, float); d = np.asarray(d, float); d = d / (np.hypot(*d) + 1e-12)
    ax.add_patch(FancyArrowPatch(p - d * 0.02, p + d * 0.02, arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=zorder))


def ring(ax, c, rx, ry, color=fs.BLACK, lw=1.4, sense=+1, arrows=(), ms=10, zorder=3, ls='-'):
    """위에서 비스듬히 본 수평 고리(아래 절반이 앞). sense=+1이면 위에서 볼 때 반시계."""
    ph = np.linspace(0, 2 * np.pi, 300)
    x = c[0] + rx * np.cos(ph); y = c[1] + ry * np.sin(ph)
    front = np.sin(ph) < 0
    xb, yb = x.copy(), y.copy(); xb[front] = np.nan
    xf, yf = x.copy(), y.copy(); xf[~front] = np.nan
    ax.plot(xb, yb, color=color, lw=lw * 0.7, ls='--' if ls == '-' else ls, zorder=zorder - 1)
    ax.plot(xf, yf, color=color, lw=lw, ls=ls, zorder=zorder + 1)
    for a in arrows:
        a = np.radians(a)
        tip(ax, (c[0] + rx * np.cos(a), c[1] + ry * np.sin(a)), sense * np.array([-rx * np.sin(a), ry * np.cos(a)]),
            color=color, ms=ms, zorder=zorder + 2)


def loop_B(z, rho, a=1.0, z0=0.0):
    zz = z - z0
    r = np.abs(rho) + 1e-9
    den = (a + r) ** 2 + zz ** 2
    k2 = 4 * a * r / den
    K = ellipk(k2); E = ellipe(k2)
    d2 = (a - r) ** 2 + zz ** 2
    Bz = 1 / np.sqrt(den) * (K + (a ** 2 - r ** 2 - zz ** 2) / d2 * E)
    Br = zz / (r * np.sqrt(den)) * (-K + (a ** 2 + r ** 2 + zz ** 2) / d2 * E)
    return Bz, Br * np.sign(rho + 1e-12)


def trace_closed(Bf, start, step=0.02, nmax=6000, box=(-5, 5, -4, 4), min_len=0.5):
    def run(sgn):
        p = np.array(start, float); pts = [p.copy()]; L = 0
        for _ in range(nmax):
            def f(x):
                b = np.array(Bf(x[0], x[1])); n = np.hypot(*b) + 1e-15; return sgn * b / n
            k1 = f(p); k2 = f(p + step / 2 * k1); k3 = f(p + step / 2 * k2); k4 = f(p + step * k3)
            p = p + step / 6 * (k1 + 2 * k2 + 2 * k3 + k4); pts.append(p.copy()); L += step
            if not (box[0] < p[0] < box[1] and box[2] < p[1] < box[3]):
                return np.array(pts), False
            if L > min_len and np.hypot(*(p - start)) < step * 1.5:
                pts.append(np.array(start)); return np.array(pts), True
        return np.array(pts), False
    fwd, closed = run(+1)
    if closed:
        return fwd
    bwd, _ = run(-1)
    return np.vstack([bwd[::-1], fwd[1:]])


def line_arrow(ax, pts, frac=0.5, color=F, ms=9):
    pts = np.asarray(pts)
    seg = np.hypot(*np.diff(pts, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
    i = int(np.clip(np.searchsorted(s, frac * s[-1]), 1, len(pts) - 2))
    ax.add_patch(FancyArrowPatch(pts[i], pts[i + 1], arrowstyle='-|>', mutation_scale=ms, color=color, lw=0, zorder=4))


def graph_ax(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def bar(ax, x0, y0, w, h, left='S', right='N', fs_=10):
    ax.add_patch(Rectangle((x0, y0 - h / 2), w / 2, h, fc=NCOL if left == 'N' else SCOL, ec=fs.BLACK, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((x0 + w / 2, y0 - h / 2), w / 2, h, fc=NCOL if right == 'N' else SCOL, ec=fs.BLACK, lw=1.0, zorder=4))
    ax.text(x0 + w / 4, y0, left, color='white', ha='center', va='center', fontsize=fs_, fontweight='bold', zorder=5)
    ax.text(x0 + 3 * w / 4, y0, right, color='white', ha='center', va='center', fontsize=fs_, fontweight='bold', zorder=5)


# ---------- 그림 30.1 자석을 잘라도 단극은 생기지 않는다 ----------
def fig01():
    fig, ax = fs.canvas(4.4, 1.7, xlim=(-0.2, 7.2), ylim=(-1.15, 1.45))
    bar(ax, 0.0, 0.85, 3.2, 0.5, 'S', 'N', 11)
    ax.text(3.6, 0.85, '자르면', fontsize=9, va='center')
    fs.arrow(ax, (4.5, 0.85), (5.1, 0.85), color=fs.BLACK, lw=1.2)
    bar(ax, 0.0, -0.4, 1.5, 0.5, 'S', 'N'); bar(ax, 1.7, -0.4, 1.5, 0.5, 'S', 'N')
    ax.plot([1.6, 1.6], [-0.75, 1.15], color=fs.GRAY, lw=0.8, ls='--')
    ax.text(3.6, -0.4, '다시 자르면', fontsize=9, va='center')
    fs.arrow(ax, (5.15, -0.4), (5.45, -0.4), color=fs.BLACK, lw=1.2)
    for k in range(2):
        bar(ax, 5.55 + k * 0.85, -0.4, 0.75, 0.4, 'S', 'N', 8)
    ax.text(5.3, 0.85, '각 조각이 다시\nS극과 N극을 가진다', fontsize=8.5, va='center')
    ax.text(5.55, -0.95, '…원자 수준까지', fontsize=8.5, va='center')
    fs.save(fig, __file__, 'fig30_01')


# ---------- 그림 30.2 막대자석과 전기 쌍극자 ----------
def fig02():
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.7))
    # (가) 막대자석 = 균일 자화 원통 = 표면 전류(솔레노이드)
    ax = axs[0]; ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.9, 1.9); ax.set_aspect('equal'); ax.axis('off')
    a, L = 0.35, 1.6
    zs = np.linspace(-L / 2, L / 2, 41)
    def Bf(x, y):
        bz = br = 0.0
        for z0 in zs:
            b1, b2 = loop_B(x, y, a, z0); bz += b1; br += b2
        return bz, br
    box = (-2.6, 2.6, -2.1, 2.1)
    for s in [0.0, 0.1, 0.2, 0.3]:
        for sg in ([1] if s == 0 else [1, -1]):
            pts = trace_closed(Bf, (0.0, sg * s), step=0.025, box=box, nmax=2500)
            ax.plot(pts[:, 0], pts[:, 1], color=F, lw=0.9, zorder=2)
            outer = [i for i, p in enumerate(pts) if abs(p[0]) < 0.3 and abs(p[1]) > 0.5 and abs(p[1]) < 1.85]
            if outer:
                i = outer[len(outer) // 2]; ax.add_patch(FancyArrowPatch(pts[i], pts[min(i + 3, len(pts) - 1)],
                                                                       arrowstyle='-|>', mutation_scale=9, color=F, lw=0, zorder=3))
    ax.add_patch(Rectangle((-L / 2, -a), L / 2, 2 * a, fc=SCOL, ec=fs.BLACK, lw=1.0, alpha=0.55, zorder=4))
    ax.add_patch(Rectangle((0, -a), L / 2, 2 * a, fc=NCOL, ec=fs.BLACK, lw=1.0, alpha=0.55, zorder=4))
    fs.arrow(ax, (-0.55, 0), (0.55, 0), color=F, lw=1.6, ms=10, zorder=6)
    ax.text(-0.6, 0.0, 'S', fontsize=10, fontweight='bold', color='white', ha='center', va='center', zorder=7)
    ax.text(0.65, 0.0, 'N', fontsize=10, fontweight='bold', color='white', ha='center', va='center', zorder=7)
    ax.add_patch(Ellipse((L / 2, 0), 0.75, 1.15, fc='none', ec=fs.BLACK, lw=1.1, ls='--', zorder=8))
    ax.text(L / 2 + 0.25, -0.75, '닫힌 곡면', fontsize=8, ha='left')
    ax.text(0, -1.85, '(가) 막대자석: 안에서 S → N', fontsize=9, ha='center')
    # (나) 전기 쌍극자
    ax = axs[1]; ax.set_aspect('equal'); ax.axis('off')
    d = 0.7
    fs.field_lines(ax, [(-d, 0, -1), (d, 0, 1)], (-2.4, 2.4), (-1.9, 1.9), per_unit=12, color=fs.GRAY, lw=0.8, r0=0.15)
    fs.charge(ax, (d, 0), +1, r=0.17); fs.charge(ax, (-d, 0), -1, r=0.17)
    fs.arrow(ax, (-0.35, -0.42), (0.35, -0.42), color=fs.BLACK, lw=1.4, ms=9)
    ax.text(0, -0.62, r'$\vec{p}$', fontsize=11, ha='center', va='top')
    ax.text(0, 0.22, r'$\vec{E}$', fontsize=10, color=fs.GRAY, ha='center')
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.9, 1.9)
    ax.text(0, -1.85, r'(나) 전기 쌍극자: 사이에서 $+ \to -$', fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, __file__, 'fig30_02')


# ---------- 그림 30.3 충전 중인 축전기와 두 면 ----------
def fig03():
    fig, ax = fs.canvas(4.6, 2.6, xlim=(-2.6, 3.4), ylim=(-1.6, 1.7))
    ax.plot([-2.5, 1.05], [0, 0], color=fs.BLACK, lw=2.0, zorder=5)
    ax.plot([1.75, 3.3], [0, 0], color=fs.BLACK, lw=2.0, zorder=5)
    for x in (1.05, 1.75):
        ax.add_patch(Rectangle((x - 0.04, -1.1), 0.08, 2.2, fc='#9aa3ad', ec=fs.BLACK, lw=0.8, zorder=6))
    for y in (-0.7, -0.25, 0.25, 0.7):
        fs.arrow(ax, (1.12, y), (1.68, y), color=F, lw=0.9, ms=7, zorder=4)
    ax.text(1.4, 1.2, r'$\vec{E}$', fontsize=10, color=F, ha='center')
    fs.arrow(ax, (-2.4, 0.18), (-1.7, 0.18), color=fs.ORANGE, lw=1.6)
    ax.text(-2.05, 0.35, r'$i$', fontsize=11, color=fs.ORANGE, ha='center')
    fs.arrow(ax, (2.5, 0.18), (3.2, 0.18), color=fs.ORANGE, lw=1.6)
    ax.text(2.85, 0.35, r'$i$', fontsize=11, color=fs.ORANGE, ha='center')
    # 경로 C (도선을 감는 원, 비스듬히)
    cx, rx, ry = -0.6, 0.28, 0.85
    # 면 S1: 평평한 원판
    ax.add_patch(Ellipse((cx, 0), 2 * rx, 2 * ry, fc=fs.SURF, alpha=0.5, ec='none', zorder=2))
    # 면 S2: 판 사이로 부풀린 주머니
    verts = [(cx, ry), (0.4, ry * 1.05), (1.4, 0.75), (1.4, 0.0), (1.4, -0.75), (0.4, -ry * 1.05), (cx, -ry)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    ax.add_patch(PathPatch(Path(verts, codes), fc='#cfe3c8', alpha=0.5, ec=fs.ACC, lw=1.2, ls='--', zorder=1))
    ph = np.linspace(0, 2 * np.pi, 300)
    X = cx - rx * np.sin(ph); Y = ry * np.cos(ph)
    ax.plot(X, Y, color=fs.BLACK, lw=1.8, zorder=7)
    for a in (40, 220):
        a = np.radians(a)
        tip(ax, (cx - rx * np.sin(a), ry * np.cos(a)), (-rx * np.cos(a), -ry * np.sin(a)), color=fs.BLACK, ms=11, zorder=8)
    ax.text(cx - 0.35, ry + 0.1, r'$C$', fontsize=12, ha='right')
    ax.text(cx - 0.1, -ry - 0.15, r'$S_1$', fontsize=11, color='#b8860b', ha='center', va='top')
    ax.text(0.75, -1.0, r'$S_2$', fontsize=11, color=fs.ACC, ha='center', va='top')
    ax.text(-2.55, -1.45, r'$S_1$: 도선이 뚫음 → $I_{\rm enc} = i$', fontsize=8.5)
    ax.text(0.45, -1.45, r'$S_2$: 판 사이 → $I_{\rm enc} = 0$', fontsize=8.5)
    fs.save(fig, __file__, 'fig30_03')


# ---------- 그림 30.4 원판 축전기 안의 자기장 (예제 30.1) ----------
def fig04():
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.5), gridspec_kw={'width_ratios': [1, 1.25]})
    ax = axs[0]; ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.5, 1.6); ax.set_aspect('equal'); ax.axis('off')
    R = 1.0
    for y in (0.75, -0.75):
        ax.add_patch(Ellipse((0, y), 2 * R, 0.5, fc='#c9ced6', ec=fs.BLACK, lw=1.0, zorder=2 if y < 0 else 6))
    ax.plot([0, 0], [0.75, 1.5], color=fs.BLACK, lw=1.8, zorder=7); ax.plot([0, 0], [-1.5, -0.75], color=fs.BLACK, lw=1.8, zorder=1)
    fs.arrow(ax, (0.12, -1.45), (0.12, -1.05), color=fs.ORANGE, lw=1.4, ms=8)
    ax.text(0.22, -1.3, r'$i$', color=fs.ORANGE, fontsize=10)
    for x in (-0.7, -0.35, 0.35, 0.7):
        fs.arrow(ax, (x, 0.6), (x, -0.6), color=F, lw=0.8, ms=6, zorder=3)
    ax.text(-0.95, 0.1, r'$\vec{E}$', fontsize=10, color=F, ha='right')
    ring(ax, (0, 0), 0.55, 0.15, color=fs.BLACK, lw=1.2, sense=-1, arrows=(-90,), ms=9, zorder=4)
    ring(ax, (0, 0), 1.6, 0.42, color=fs.BLACK, lw=1.2, sense=-1, arrows=(-90,), ms=9, zorder=4)
    ax.text(0.45, 0.1, r'$r<R$', fontsize=8, ha='left')
    ax.text(1.35, 0.42, r'$r>R$', fontsize=8, ha='left')
    ax.text(0, 1.62, r'전하가 늘어남: $d\vec{E}/dt$ 아래쪽', fontsize=8, ha='center', va='top') if False else None
    ax = axs[1]; graph_ax(ax)
    Rm, i = 0.05, 2.0
    r = np.linspace(0, 0.15, 400)
    B = np.where(r < Rm, 2e-7 * i * r / Rm ** 2, 2e-7 * i / np.maximum(r, 1e-9)) * 1e6
    ax.plot(r * 100, B, color=F, lw=1.8)
    ax.axvline(5, color=fs.GRAY, lw=0.7, ls=':')
    for rr, v in [(3, 4.8), (10, 4.0)]:
        ax.plot(rr, v, 'o', color=fs.BLACK, ms=4); ax.text(rr + 0.4, v + 0.35, f'{v} μT', fontsize=8.5)
    ax.text(5.3, 8.3, r'$r = R$', fontsize=8.5, color=fs.GRAY)
    ax.set_xlabel(r'$r$ (cm)'); ax.set_ylabel(r'$B$ ($\mu$T)'); ax.set_xlim(0, 15); ax.set_ylim(0, 9)
    fig.subplots_adjust(wspace=0.2)
    fs.save(fig, __file__, 'fig30_04')


# ---------- 그림 30.5 변하는 B가 E를, 변하는 E가 B를 만든다 ----------
def fig05():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.6))
    for ax, kind in [(axs[0], 'B'), (axs[1], 'E')]:
        ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.5, 1.6); ax.set_aspect('equal'); ax.axis('off')
        col_src = F if kind == 'B' else fs.ORANGE
        col_ind = fs.ORANGE if kind == 'B' else F
        for x in (-0.25, 0.0, 0.25):
            fs.arrow(ax, (x, -1.2), (x, 1.2), color=col_src, lw=1.3, ms=10, zorder=1)
        # B 증가(위쪽) → 위에서 볼 때 시계 방향 E (sense=-1), E 증가 → 반시계 B (sense=+1)
        sense = -1 if kind == 'B' else +1
        for y, rx in [(-0.4, 1.05), (0.4, 1.05)]:
            ring(ax, (0, y), rx, 0.28, color=col_ind, lw=1.4, sense=sense, arrows=(-90, 90), ms=10, zorder=3)
        if kind == 'B':
            ax.text(0.35, 1.25, r'$\dfrac{d\vec{B}}{dt}$', fontsize=11, color=F)
            ax.text(1.15, -0.75, r'$\vec{E}$', fontsize=11, color=fs.ORANGE)
            ax.text(0, -1.5, r'(가) 패러데이: $\oint\vec{E}\cdot d\vec{\ell} = -\dfrac{d\Phi_B}{dt}$', fontsize=9, ha='center')
        else:
            ax.text(0.35, 1.25, r'$\dfrac{d\vec{E}}{dt}$', fontsize=11, color=fs.ORANGE)
            ax.text(1.15, -0.75, r'$\vec{B}$', fontsize=11, color=F)
            ax.text(0, -1.5, r'(나) 맥스웰: $\oint\vec{B}\cdot d\vec{\ell} = +\mu_0\varepsilon_0\dfrac{d\Phi_E}{dt}$', fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.08)
    fs.save(fig, __file__, 'fig30_05')


# ---------- 그림 30.6 궤도 운동하는 전자의 자기 모멘트 ----------
def fig06():
    fig, ax = fs.canvas(2.9, 2.8, xlim=(-1.6, 1.8), ylim=(-1.6, 1.7))
    ring(ax, (0, 0), 1.2, 0.38, color=fs.GRAY, lw=1.2, sense=+1, arrows=(), zorder=3)
    ax.add_patch(Circle((0, 0), 0.1, color='#888888', zorder=5))
    # 전자: 앞쪽에서 오른쪽으로 → 위에서 볼 때 반시계
    e = np.array([0.0, -0.38])
    ax.add_patch(Circle(e, 0.1, fc=fs.NEG, ec='none', zorder=8))
    ax.text(e[0], e[1] - 0.01, '−', color='white', fontsize=9, ha='center', va='center', zorder=9, fontweight='bold')
    fs.arrow(ax, e + (0.12, 0), e + (0.75, 0), color=fs.VEL, lw=1.6)
    ax.text(0.5, -0.6, r'$\vec{v}$', fontsize=11, color=fs.VEL, ha='center', va='center')
    tip(ax, (-1.2 * np.cos(np.radians(30)) * 1.0, -0.38 * np.sin(np.radians(30))), (-1, 0.55), color=fs.ORANGE, ms=12)
    ax.text(-1.25, -0.5, r'$I$', fontsize=11, color=fs.ORANGE)
    fs.arrow(ax, (0.06, 0.05), (0.06, 1.3), color=fs.BLACK, lw=2.0)
    ax.text(0.18, 1.25, r'$\vec{L}$', fontsize=12)
    fs.arrow(ax, (-0.06, -0.05), (-0.06, -1.3), color=fs.FORCE, lw=2.0)
    ax.text(-0.18, -1.3, r'$\vec{\mu}$', fontsize=12, color=fs.FORCE, ha='right')
    ax.text(0.95, 0.42, r'$r$', fontsize=10, color=fs.GRAY)
    fs.save(fig, __file__, 'fig30_06')


# ---------- 그림 30.7 반자성·상자성·강자성 ----------
def fig07():
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(2, 3, figsize=(5.6, 3.4))
    nx, ny = 5, 4
    xs, ys = np.meshgrid(np.arange(nx) + 0.5, np.arange(ny) + 0.5)
    xs, ys = xs.ravel(), ys.ravel()
    angles_para = rng.uniform(0, 2 * np.pi, xs.size)
    # 강자성 구역: 네 구역
    def dom_angle(x, y, on):
        q = (0 if x < 2.5 else 1) + (0 if y < 2 else 2)
        base = [np.pi / 2, np.pi, 0.0, -np.pi / 2][q]
        if on:
            base = 0.0 if q in (0, 2, 3) else 0.0
        return base
    for col, kind in enumerate(['반자성', '상자성', '강자성']):
        for row, on in enumerate([False, True]):
            ax = axs[row, col]
            ax.set_xlim(-0.2, nx + 0.2); ax.set_ylim(-0.2, ny + 0.2); ax.set_aspect('equal'); ax.axis('off')
            ax.add_patch(Rectangle((0, 0), nx, ny, fc='#f4f4f4', ec=fs.GRAY, lw=0.8))
            for k, (x, y) in enumerate(zip(xs, ys)):
                if kind == '반자성':
                    if on:
                        fs.arrow(ax, (x + 0.12, y), (x - 0.12, y), color=fs.VEL, lw=1.0, ms=6)
                    else:
                        ax.add_patch(Circle((x, y), 0.07, color=fs.GRAY))
                    continue
                if kind == '상자성':
                    a = angles_para[k]
                    if on:
                        a = a * 0.45 if a < np.pi else (a - 2 * np.pi) * 0.45
                    L = 0.38
                else:
                    if on:
                        a = 0.0 if not (x > 2.5 and y > 2 and x < 3.5) else np.pi / 2
                    else:
                        q = (0 if x < 2.5 else 1) + (0 if y < 2 else 2)
                        a = [np.pi / 2, np.pi, 0.0, -np.pi / 2][q]
                    L = 0.4
                d = np.array([np.cos(a), np.sin(a)]) * L
                fs.arrow(ax, (x - d[0], y - d[1]), (x + d[0], y + d[1]), color=fs.FORCE, lw=1.2, ms=7)
            if kind == '강자성':
                if not on:
                    ax.plot([2.5, 2.5], [0, ny], color=fs.BLACK, lw=0.8, ls='--')
                    ax.plot([0, nx], [2, 2], color=fs.BLACK, lw=0.8, ls='--')
                else:
                    ax.plot([3.0, 3.0, 4.0, 4.0], [ny, 2.0, 2.0, ny], color=fs.BLACK, lw=0.8, ls='--')
            if row == 0:
                ax.set_title(kind, fontsize=10)
        axs[0, 0].text(-0.5, ny / 2, r'$B_0 = 0$', fontsize=9, rotation=90, ha='right', va='center')
        axs[1, 0].text(-0.5, ny / 2, r'$\vec{B}_0 \rightarrow$', fontsize=9, rotation=90, ha='right', va='center')
    fig.subplots_adjust(wspace=0.08, hspace=0.05, left=0.07)
    fs.save(fig, __file__, 'fig30_07')


# ---------- 그림 30.8 상자성: tanh와 퀴리 법칙 ----------
def fig08():
    x = np.linspace(0, 3, 400)
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.plot(x, np.tanh(x), color=fs.VEL, lw=1.9, label=r'$M/M_s = \tanh x$')
    ax.plot(x, x, color=fs.FORCE, lw=1.2, ls='--', label=r'퀴리 법칙 $M/M_s = x$')
    ax.axhline(1, color=fs.GRAY, lw=0.7, ls=':')
    ax.text(2.95, 1.02, '포화', fontsize=8.5, color=fs.GRAY, ha='right', va='bottom')
    ax.axvline(0.553, color=fs.GRAY, lw=0.7, ls='-.')
    ax.text(0.6, 0.12, r'$x = 0.553$' + '\n(오차 10%)', fontsize=8.5, color=fs.GRAY)
    for T, xx in [(4.2, 0.1599), (1.0, 0.6717), (0.3, 2.2390)]:
        ax.plot(xx, np.tanh(xx), 'o', color=fs.BLACK, ms=3.5)
        ax.text(xx + 0.05, np.tanh(xx) - 0.09, f'{T} K', fontsize=8)
    ax.set_xlabel(r'$x = \mu B/k_BT$'); ax.set_ylabel(r'$M/M_s$')
    ax.set_xlim(0, 3); ax.set_ylim(0, 1.25)
    ax.legend(fontsize=8.5, loc='lower right', frameon=False)
    fs.save(fig, __file__, 'fig30_08')


# ---------- 그림 30.9 자기 이력 곡선 ----------
def fig09():
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.6))
    for ax, Hc, w, title in [(axs[0], 0.45, 0.35, '(가) 경자성체(영구자석)'), (axs[1], 0.08, 0.25, '(나) 연자성체(변압기 철심)')]:
        ax.axhline(0, color=fs.BLACK, lw=0.7); ax.axvline(0, color=fs.BLACK, lw=0.7)
        H = np.linspace(-1.5, 1.5, 400)
        up = np.tanh((H - Hc) / w); dn = np.tanh((H + Hc) / w)
        ax.plot(H, up, color=fs.VEL, lw=1.8)
        ax.plot(H, dn, color=fs.VEL, lw=1.8)
        line_arrow(ax, np.column_stack([H, up]), 0.55, color=fs.VEL, ms=10)
        line_arrow(ax, np.column_stack([H[::-1], dn[::-1]]), 0.55, color=fs.VEL, ms=10)
        Hi = np.linspace(0, 1.5, 200)
        ax.plot(Hi, np.tanh(Hi / w) * (1 - 0.35 * np.exp(-Hi / 0.3)) if Hc > 0.2 else np.tanh(Hi / (w * 0.9)),
                color=fs.GRAY, lw=1.0, ls='--')
        Br = np.tanh(Hc / w)
        ax.plot(0, Br, 'o', color=fs.FORCE, ms=4); ax.plot(-Hc, 0, 'o', color=fs.ACC, ms=4)
        if Hc > 0.2:
            ax.text(0.06, Br + 0.12, '잔류 자화', fontsize=8.5, color=fs.FORCE)
            ax.text(-Hc - 0.05, -0.18, '보자력', fontsize=8.5, color=fs.ACC, ha='right', va='top')
            ax.text(1.45, 1.08, '포화', fontsize=8.5, ha='right', va='bottom')
            ax.text(0.55, 0.25, '처음 자화', fontsize=8, color=fs.GRAY)
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.35, 1.4)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ('top', 'right', 'left', 'bottom'): ax.spines[s].set_visible(False)
        ax.text(1.6, -0.1, r'$B_0$', fontsize=10, ha='right', va='top')
        ax.text(0.06, 1.38, r'$B$', fontsize=10, va='top')
        ax.set_title(title, fontsize=9)
    fs.save(fig, __file__, 'fig30_09')


# ---------- 그림 30.10 자화 전류 ----------
def fig10():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.2), gridspec_kw={'width_ratios': [1.3, 1]})
    ax = axs[0]; ax.set_xlim(-0.3, 4.3); ax.set_ylim(-0.3, 3.3); ax.set_aspect('equal'); ax.axis('off')
    for i in range(4):
        for j in range(3):
            c = (i + 0.5, j + 0.5)
            ax.add_patch(Rectangle((i + 0.1, j + 0.1), 0.8, 0.8, fc='none', ec=fs.ORANGE, lw=1.0))
            for p, d in [((c[0], j + 0.1), (1, 0)), ((i + 0.9, c[1]), (0, 1)), ((c[0], j + 0.9), (-1, 0)), ((i + 0.1, c[1]), (0, -1))]:
                tip(ax, p, d, color=fs.ORANGE, ms=7)
            fs.dot_out(ax, c, r=0.07, color=fs.FORCE)
    ax.add_patch(Rectangle((0, 0), 4, 3, fc='none', ec=fs.BLACK, lw=1.2))
    ax.text(2, -0.25, '이웃한 변의 전류는 상쇄된다', fontsize=8.5, ha='center', va='top')
    ax = axs[1]; ax.set_xlim(-0.3, 3.3); ax.set_ylim(-0.3, 3.3); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0.2, 0.2), 2.6, 2.6, fc='#f4f4f4', ec=fs.ORANGE, lw=2.0))
    for p, d in [((1.5, 0.2), (1, 0)), ((2.8, 1.5), (0, 1)), ((1.5, 2.8), (-1, 0)), ((0.2, 1.5), (0, -1))]:
        tip(ax, p, d, color=fs.ORANGE, ms=12)
    fs.dot_out(ax, (1.5, 1.5), r=0.12, color=fs.FORCE)
    ax.text(1.5, 1.15, r'$\vec{M}$', fontsize=11, color=fs.FORCE, ha='center', va='top')
    ax.text(2.95, 2.95, r'$K_M = M$', fontsize=9, color=fs.ORANGE, ha='right', va='bottom')
    ax.text(1.5, -0.25, '표면 전류만 남는다', fontsize=8.5, ha='center', va='top')
    fs.save(fig, __file__, 'fig30_10')


# ---------- 그림 30.11 마이스너 효과 ----------
def sphere_lines(ax, mode, R=0.8, lim=1.9, nlines=6):
    """mode: 'uniform' 균일, 'expel' 밀어냄, 'trap' 내부 균일+외부 쌍극자(외부 자기장 없음)."""
    x = np.linspace(-lim, lim, 500); y = np.linspace(-lim, lim, 500)
    X, Y = np.meshgrid(x, y)
    r = np.hypot(X, Y) + 1e-9
    rho2 = Y ** 2
    if mode == 'uniform':
        psi = 0.5 * rho2
    elif mode == 'expel':
        psi = np.where(r > R, 0.5 * rho2 * (1 - R ** 3 / r ** 3), np.nan)
    else:
        psi = np.where(r > R, 0.5 * rho2 * R ** 3 / r ** 3, 0.5 * rho2)
    if mode == 'trap':
        rhos = np.linspace(0.12, R * 0.95, 5)
    else:
        rhos = np.linspace(0.25, lim * 0.95, nlines)
    levels = 0.5 * rhos ** 2
    ax.contour(X, Y, psi, levels=levels, colors=F, linewidths=0.9)
    # 화살촉
    if mode == 'trap':
        for rr in rhos[::2]:
            for s in (1, -1):
                tip(ax, (0, s * rr), (1, 0), color=F, ms=8)
    else:
        for rr in rhos:
            for s in (1, -1):
                yy = rr if mode == 'uniform' else None
                xx = -lim * 0.8
                if mode == 'expel':
                    # x = -0.8 lim에서 같은 psi를 갖는 y
                    rg = np.linspace(0.01, lim, 2000)
                    rr_ = np.hypot(xx, rg)
                    ps = 0.5 * rg ** 2 * (1 - R ** 3 / rr_ ** 3)
                    yy = rg[np.argmin(abs(ps - 0.5 * rr ** 2))]
                tip(ax, (xx, s * yy), (1, 0), color=F, ms=8)


def fig11():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.6))
    for ax, mode, title in [(axs[0], 'uniform', r'(가) $T > T_c$: 자기장이 통과'),
                            (axs[1], 'expel', r'(나) $T < T_c$: 자기장을 밀어냄')]:
        ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.9, 1.9); ax.set_aspect('equal'); ax.axis('off')
        sphere_lines(ax, mode)
        ax.add_patch(Circle((0, 0), 0.8, fc='#dfe6ee' if mode == 'uniform' else '#cfe0f5', ec=fs.BLACK, lw=1.1,
                            alpha=0.85, zorder=3))
        if mode == 'expel':
            for a in np.radians([60, 120]):
                tip(ax, (0.8 * np.cos(a) * 0.95, 0.8 * np.sin(a) * 0.95), (np.cos(a + np.pi / 2), np.sin(a + np.pi / 2)),
                    color=fs.ORANGE, ms=0) if False else None
            ax.text(0, 0, r'$B = 0$', fontsize=10, ha='center', va='center', zorder=5)
        ax.set_title(title, fontsize=9)
    fs.save(fig, __file__, 'fig30_11')


# ---------- 그림 30.12 완전 도체와 초전도체 ----------
def fig12():
    fig, axs = plt.subplots(2, 3, figsize=(5.6, 3.5))
    steps = ['$T > T_c$, 자기장 켬', '$T_c$ 아래로 냉각', '바깥 자기장 끔']
    rows = [('완전 도체', ['uniform', 'uniform', 'trap']), ('초전도체', ['uniform', 'expel', 'none'])]
    for r_, (name, modes) in enumerate(rows):
        for c_, mode in enumerate(modes):
            ax = axs[r_, c_]; ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_aspect('equal'); ax.axis('off')
            if mode != 'none':
                sphere_lines(ax, mode, R=0.7, lim=1.6, nlines=5)
            cold = c_ > 0
            ax.add_patch(Circle((0, 0), 0.7, fc='#cfe0f5' if cold else '#e8e8e8', ec=fs.BLACK, lw=1.0, alpha=0.85, zorder=3))
            if mode in ('expel', 'none') or (mode == 'none'):
                ax.text(0, 0, r'$B=0$', fontsize=8.5, ha='center', va='center', zorder=5)
            if mode == 'trap':
                ax.text(0, -1.45, '선속이 갇힘', fontsize=8, ha='center', color=fs.FORCE)
            if r_ == 0:
                ax.set_title(steps[c_], fontsize=8.5)
            if c_ == 0:
                ax.text(-1.75, 0, name, fontsize=9, rotation=90, ha='right', va='center')
    fig.subplots_adjust(wspace=0.05, hspace=0.12, left=0.06)
    fs.save(fig, __file__, 'fig30_12')


# ---------- 그림 30.13 납의 임계 자기장 (연습문제 13) ----------
def fig13():
    Tc, B0 = 7.2, 0.080
    T = np.linspace(0, Tc, 200)
    Bc = B0 * (1 - (T / Tc) ** 2)
    fig, ax = fs.plot_axes(3.8, 2.5)
    ax.plot(T, Bc * 1e3, color=fs.VEL, lw=1.9)
    ax.fill_between(T, 0, Bc * 1e3, color=fs.VEL, alpha=0.12, lw=0)
    ax.text(2.0, 25, '초전도 상태', fontsize=9.5, color=fs.VEL)
    ax.text(5.2, 65, '정상 상태', fontsize=9.5)
    ax.set_xlabel(r'온도 $T$ (K)'); ax.set_ylabel(r'$B$ (mT)')
    ax.set_xlim(0, 8); ax.set_ylim(0, 95)
    ax.text(0.1, 82, r'$B_c(0) = 80$ mT', fontsize=8.5)
    ax.text(Tc + 0.05, 3, r'$T_c$', fontsize=9)
    fs.save(fig, __file__, 'fig30_13')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13]:
        f()
