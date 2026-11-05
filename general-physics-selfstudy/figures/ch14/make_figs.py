"""14장 유체 — 그림 생성 스크립트.

    python3 figures/ch14/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch

WATER = '#cfe4f5'
WATER_EDGE = '#6fa8d6'
HG = '#b9c0c8'       # 수은
GLASS = fs.BLACK


# ---------- 이 장 전용 도우미 ----------
def hdim(ax, x0, x1, y, text, color=fs.GRAY, fontsize=9, above=True):
    ax.annotate('', (x0, y), (x1, y), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.8,
                                                       mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (0.05 if above else -0.05), text, fontsize=fontsize, color=color,
            ha='center', va='bottom' if above else 'top')


def vdim(ax, x, y0, y1, text, color=fs.GRAY, fontsize=9, right=True):
    ax.annotate('', (x, y0), (x, y1), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.8,
                                                       mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(x + (0.08 if right else -0.08), (y0 + y1) / 2, text, fontsize=fontsize, color=color,
            ha='left' if right else 'right', va='center')


def surface_mark(ax, x, y, s=0.12, color=WATER_EDGE):
    """수면 기호(▽)."""
    ax.add_patch(Polygon([(x - s, y + 1.4 * s), (x + s, y + 1.4 * s), (x, y + 0.15 * s)], closed=True,
                         fc='none', ec=color, lw=0.9))


def mid_arrowheads(ax, pts, color, n=1, ms=9):
    pts = np.asarray(pts, float)
    for k in range(n):
        i = int(len(pts) * (k + 1) / (n + 1))
        ax.add_patch(FancyArrowPatch(pts[i - 1], pts[i + 1], arrowstyle='-|>', mutation_scale=ms, color=color, lw=0))


# ---------- 그림 14.1 쐐기 논증 ----------
def fig01():
    fig, ax = fs.canvas(3.6, 2.7, xlim=(-1.3, 3.9), ylim=(-1.2, 2.6))
    th = np.radians(35); s = 3.0
    A = np.array([0, 0]); B = np.array([s * np.cos(th), 0]); C = np.array([0, s * np.sin(th)])
    ax.add_patch(Polygon([A, B, C], closed=True, fc=WATER, ec=fs.BLACK, lw=1.2))
    fs.angle_arc(ax, B, 0.55, 180 - 35, 180, r'$\theta$', fontsize=11, tr=0.8)
    fs.arrow(ax, (-0.9, C[1] / 2), (-0.05, C[1] / 2), color=fs.FORCE, lw=1.6, label=r'$p_x$', lpos=0, loff=(0.0, 0.25))
    fs.arrow(ax, (B[0] / 2, -0.85), (B[0] / 2, -0.05), color=fs.FORCE, lw=1.6, label=r'$p_y$', lpos=0, loff=(0.3, 0.1))
    M = (B + C) / 2; nout = np.array([np.sin(th), np.cos(th)])
    fs.arrow(ax, M + 0.9 * nout, M + 0.05 * nout, color=fs.FORCE, lw=1.6, label=r'$p_n$', lpos=0, loff=(0.25, 0.1))
    G = (A + B + C) / 3
    fs.arrow(ax, G, G + np.array([0, -0.45]), color=fs.FORCE, lw=1.1, ms=8)
    ax.text(G[0] + 0.1, G[1] - 0.15, '무게', fontsize=8, color=fs.FORCE, ha='left')
    ax.text(-0.12, C[1] / 2 + 0.35, r'$s\sin\theta$', fontsize=9, ha='right')
    ax.text(B[0] / 2 + 0.55, -0.35, r'$s\cos\theta$', fontsize=9, ha='left', va='center')
    tg = (B - C) / np.linalg.norm(B - C)
    ax.text(*(M - 0.55 * tg + 0.25 * nout), r'$s$', fontsize=11, ha='center', va='center')
    fs.save(fig, __file__, 'fig14_01')


# ---------- 그림 14.2 얇은 유체 조각 ----------
def fig02():
    fig, ax = fs.canvas(3.6, 2.8, xlim=(-1.0, 4.4), ylim=(-0.3, 4.1))
    ax.add_patch(Rectangle((0, 0), 4.0, 3.6, fc=WATER, ec='none'))
    ax.plot([0, 4.0], [3.6, 3.6], color=WATER_EDGE, lw=1.2)
    surface_mark(ax, 3.5, 3.6)
    ax.text(0.15, 3.75, r'$p_0$', fontsize=10)
    y0, dy = 1.5, 0.6
    ax.add_patch(Rectangle((1.2, y0), 1.6, dy, fc='#9cc7ea', ec=fs.BLACK, lw=1.1, zorder=3))
    fs.arrow(ax, (2.0, y0 - 0.9), (2.0, y0), color=fs.FORCE, lw=1.7, label=r'$p(y)A$', lpos=0, loff=(0.55, 0.25))
    fs.arrow(ax, (2.0, y0 + dy + 0.8), (2.0, y0 + dy), color=fs.FORCE, lw=1.7, label=r'$p(y+dy)A$', lpos=0, loff=(0.8, -0.2))
    fs.arrow(ax, (2.3, y0 + dy / 2), (2.3, y0 + dy / 2 - 0.55), color=fs.FORCE, lw=1.1, ms=8, zorder=6)
    ax.text(2.42, y0 + 0.08, r'$dm\,g$', fontsize=9, color=fs.FORCE, ha='left', zorder=6)
    ax.text(1.12, y0 + dy / 2, r'$A$', fontsize=10, ha='right', va='center')
    ax.annotate('', (-0.5, 3.4), (-0.5, 0.2), arrowprops=dict(arrowstyle='-|>', lw=0.9, mutation_scale=9))
    ax.text(-0.65, 3.35, r'$y$', fontsize=11, ha='right')
    for yy, lab in [(y0, r'$y$'), (y0 + dy, r'$y + dy$')]:
        ax.plot([-0.55, 1.2], [yy, yy], ls=':', color=fs.GRAY, lw=0.8)
        ax.text(-0.6, yy, lab, fontsize=9, ha='right', va='center')
    fs.save(fig, __file__, 'fig14_02')


# ---------- 그림 14.3 정수압 역설 ----------
def fig03():
    fig, ax = fs.canvas(4.6, 1.9, xlim=(-0.4, 9.6), ylim=(-0.6, 2.6))
    h, b = 2.0, 1.4
    shapes = [[(0, 0), (b, 0), (b + 0.7, h + 0.3), (-0.7, h + 0.3)],
              [(3.7, 0), (3.7 + b, 0), (3.7 + b, h + 0.3), (3.7, h + 0.3)],
              [(7.3, 0), (7.3 + b, 0), (7.3 + b - 0.45, h + 0.3), (7.3 + 0.45, h + 0.3)]]
    for k, sh in enumerate(shapes):
        sh = np.array(sh, float)
        # 물(높이 h까지)
        def xat(side, y):
            p0, p1 = (sh[0], sh[3]) if side == 0 else (sh[1], sh[2])
            return p0[0] + (p1[0] - p0[0]) * y / (h + 0.3)
        wpoly = [sh[0], sh[1], (xat(1, h), h), (xat(0, h), h)]
        ax.add_patch(Polygon(wpoly, closed=True, fc=WATER, ec='none'))
        ax.plot([xat(0, h), xat(1, h)], [h, h], color=WATER_EDGE, lw=1.1)
        ax.plot([sh[3][0], sh[0][0], sh[1][0], sh[2][0]], [sh[3][1], sh[0][1], sh[1][1], sh[2][1]], color=GLASS, lw=1.4)
    ax.plot([-0.6, 9.4], [h, h], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, 9.25, 0, h, r'$h$')
    ax.text(4.4, -0.45, '세 그릇 모두 바닥의 압력은 $p_0 + \\rho g h$', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig14_03')


# ---------- 그림 14.4 기압계와 액주계 ----------
def fig04():
    fig, ax = fs.canvas(5.0, 2.9, xlim=(-0.4, 8.6), ylim=(-0.9, 4.6))
    # (가) 수은 기압계
    ax.add_patch(Rectangle((0, 0), 3.0, 0.7, fc=HG, ec='none'))
    ax.plot([0, 0, 3.0, 3.0], [1.0, 0, 0, 1.0], color=GLASS, lw=1.3)
    tx, tw = 1.25, 0.5
    ax.add_patch(Rectangle((tx, 0.25), tw, 3.1, fc=HG, ec='none', zorder=2))
    ax.add_patch(Rectangle((tx, 3.35), tw, 0.75, fc='white', ec='none', zorder=2))
    ax.plot([tx, tx, tx + tw, tx + tw], [0.25, 4.1, 4.1, 0.25], color=GLASS, lw=1.3, zorder=3)
    ax.text(tx + tw / 2, 3.72, '진공', fontsize=7.5, ha='center', va='center', zorder=4)
    for x in (0.45, 2.55):
        fs.arrow(ax, (x, 1.45), (x, 0.75), color=fs.FORCE, lw=1.3, ms=8)
    ax.text(0.45, 1.6, r'$p_0$', fontsize=10, color=fs.FORCE, ha='center')
    ax.plot([tx + tw, 2.7], [0.7, 0.7], ls=':', color=fs.GRAY, lw=0.7)
    ax.plot([tx + tw, 2.7], [3.35, 3.35], ls=':', color=fs.GRAY, lw=0.7)
    vdim(ax, 2.6, 0.7, 3.35, r'$h$')
    ax.text(1.5, -0.6, '(가) 수은 기압계', fontsize=9, ha='center')
    # (나) U자관 액주계
    lx, rx, w = 4.6, 7.0, 0.35
    yl, yr = 1.3, 2.5        # 액면 높이(기체 쪽이 낮다 → p > p0)
    ax.add_patch(Rectangle((4.0, 2.6), 1.6, 1.3, fc='#eef2f7', ec='none'))
    ax.add_patch(Rectangle((lx, yl), w, 2.6 - yl, fc='#eef2f7', ec='none'))
    ax.plot([lx, 4.0, 4.0, 5.6, 5.6, lx + w], [2.6, 2.6, 3.9, 3.9, 2.6, 2.6], color=GLASS, lw=1.3)
    ax.text(4.8, 3.25, '기체 ' + r'$p$', fontsize=9, ha='center', va='center')
    ax.add_patch(Rectangle((lx, 0.4), w, yl - 0.4, fc=WATER, ec='none'))
    ax.add_patch(Rectangle((rx, 0.4), w, yr - 0.4, fc=WATER, ec='none'))
    ax.add_patch(Rectangle((lx, 0.0), rx + w - lx, 0.4, fc=WATER, ec='none'))
    ax.plot([lx, lx, rx + w, rx + w], [2.6, 0.0, 0.0, 3.6], color=GLASS, lw=1.3)
    ax.plot([lx + w, lx + w, rx, rx], [2.6, 0.4, 0.4, 3.6], color=GLASS, lw=1.3)
    ax.text(rx + w / 2, 3.85, r'$p_0$', fontsize=10, ha='center', color=fs.FORCE)
    fs.arrow(ax, (rx + w / 2, 3.7), (rx + w / 2, 3.0), color=fs.FORCE, lw=1.2, ms=8)
    ax.plot([lx, rx + w + 0.3], [yl, yl], ls=':', color=fs.GRAY, lw=0.8)
    ax.plot([rx, rx + w + 0.3], [yr, yr], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, rx + w + 0.2, yl, yr, r'$\Delta h$')
    ax.text(6.0, -0.6, '(나) U자관 액주계', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig14_04')


# ---------- 그림 14.5 댐이 받는 힘(예제 14.2) ----------
def fig05():
    fig, ax = fs.canvas(4.2, 2.9, xlim=(-3.6, 2.3), ylim=(-0.6, 3.5))
    D = 2.6
    ax.add_patch(Rectangle((-3.4, 0), 3.4, D, fc=WATER, ec='none'))
    ax.plot([-3.4, 0], [D, D], color=WATER_EDGE, lw=1.2)
    surface_mark(ax, -3.0, D)
    ax.add_patch(Polygon([(0, 0), (1.3, 0), (0.45, D + 0.4), (0, D + 0.4)], closed=True, fc='#d9d4c7', ec=fs.BLACK, lw=1.2))
    fs.ground(ax, -3.5, 2.2, y=0.0)
    # 압력 분포
    k = 0.75
    ax.add_patch(Polygon([(0, D), (0, 0), (-k * D, 0)], closed=True, fc='none', ec=fs.FORCE, lw=0.8, ls='--'))
    for y in np.linspace(0.25, D - 0.25, 7):
        hh = D - y
        fs.arrow(ax, (-k * hh, y), (0, y), color=fs.FORCE, lw=1.0, ms=7)
    # 띠
    hs, dh = 0.8, 0.18
    ax.add_patch(Rectangle((-0.22, D - hs - dh / 2), 0.22, dh, fc=fs.SURF, ec=fs.BLACK, lw=0.7, zorder=5))
    ax.annotate(r'깊이 $h$, 두께 $dh$인 띠', (-0.2, D - hs + dh / 2), (-1.6, D + 0.5), fontsize=8.5,
                arrowprops=dict(arrowstyle='-', lw=0.6), ha='center')
    vdim(ax, -3.2, 0, D, r'$D$')
    # 합력
    ax.plot([0.0, 1.9], [D / 3, D / 3], ls=':', color=fs.GRAY, lw=0.7)
    vdim(ax, 1.8, 0, D / 3, r'$D/3$')
    fs.arrow(ax, (-1.4, D / 3), (-0.02, D / 3), color=fs.FORCE, lw=2.4, ms=12, zorder=6)
    ax.text(-1.45, D / 3, r'$F$', fontsize=11, color=fs.FORCE, ha='right', va='center')
    fs.save(fig, __file__, 'fig14_05')


# ---------- 그림 14.6 등온 대기의 압력(예제 14.3) ----------
def fig06():
    fig, ax = fs.plot_axes(3.8, 2.7)
    H = 1.013e5 / (1.20 * 9.8) / 1000
    z = np.linspace(0, 20, 300)
    ax.plot(np.exp(-z / H), z, color=fs.VEL, lw=1.9)
    p3 = np.exp(-3.0 / H)
    ax.plot([0, p3], [3, 3], ls=':', color=fs.GRAY, lw=0.9); ax.plot([p3, p3], [0, 3], ls=':', color=fs.GRAY, lw=0.9)
    ax.plot(p3, 3, 'o', color=fs.FORCE, ms=4)
    ax.annotate(rf'$z = 3.0$ km: $p/p_0 = {p3:.2f}$', (p3, 3), (0.62, 6.0), fontsize=9,
                arrowprops=dict(arrowstyle='->', lw=0.7))
    pH = np.exp(-1)
    ax.plot([0, pH], [H, H], ls=':', color=fs.GRAY, lw=0.9)
    ax.text(0.42, H + 0.3, rf'$z = H = {H:.1f}$ km: $p = p_0/e$', fontsize=8.5)
    ax.text(0.55, 14, r'$p = p_0 e^{-z/H}$', fontsize=11, color=fs.VEL)
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 20)
    ax.set_xlabel(r'$p/p_0$'); ax.set_ylabel(r'높이 $z$ (km)')
    fs.save(fig, __file__, 'fig14_06')


# ---------- 그림 14.7 유압 리프트 ----------
def fig07():
    fig, ax = fs.canvas(4.8, 2.6, xlim=(-0.6, 8.0), ylim=(-0.5, 4.0))
    a1, a2 = 0.6, 2.6          # 피스톤 폭
    x1, x2 = 0.4, 3.6
    yb = 0.0; yt = 2.0
    ax.add_patch(Rectangle((x1, yb), x2 + a2 - x1, 0.5, fc=WATER, ec='none'))
    ax.add_patch(Rectangle((x1, yb), a1, yt - 0.35, fc=WATER, ec='none'))
    ax.add_patch(Rectangle((x2, yb), a2, yt, fc=WATER, ec='none'))
    ax.plot([x1, x1, x2 + a2, x2 + a2], [yt + 1.2, yb, yb, yt + 0.8], color=GLASS, lw=1.4)
    ax.plot([x1 + a1, x1 + a1, x2, x2], [yt + 1.2, 0.5, 0.5, yt + 0.8], color=GLASS, lw=1.4)
    # 피스톤
    ax.add_patch(Rectangle((x1, yt - 0.35), a1, 0.2, fc='#777777', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((x2, yt), a2, 0.2, fc='#777777', ec=fs.BLACK, lw=1.0))
    fs.block(ax, (x2 + a2 / 2, yt + 0.6), w=1.8, h=0.6, text='자동차', fontsize=9)
    fs.arrow(ax, (x1 + a1 / 2, yt + 0.9), (x1 + a1 / 2, yt - 0.15), color=fs.FORCE, lw=1.8, label=r'$F_1$', lpos=0, loff=(0.0, 0.2))
    fs.arrow(ax, (x2 + a2 / 2, yt - 1.2), (x2 + a2 / 2, yt - 0.02), color=fs.FORCE, lw=2.6, ms=14, zorder=6)
    ax.text(x2 + a2 + 0.15, 1.15, r'$F_2 = F_1 A_2/A_1$', fontsize=9, color=fs.FORCE, ha='left')
    ax.text(x1 + a1 / 2, 0.75, r'$A_1$', fontsize=9, ha='center')
    ax.text(x2 + 0.35, 1.5, r'$A_2$', fontsize=9, ha='center')
    fs.arrow(ax, (-0.25, yt - 0.15), (-0.25, yt - 0.95), color=fs.BLACK, lw=1.0, ms=8)
    ax.text(-0.35, yt - 0.55, r'$d_1$', fontsize=9, ha='right')
    fs.arrow(ax, (x2 + a2 + 0.25, yt + 0.2), (x2 + a2 + 0.25, yt + 0.45), color=fs.BLACK, lw=1.0, ms=6)
    ax.text(x2 + a2 + 0.35, yt + 0.33, r'$d_2$', fontsize=9, ha='left')
    fs.save(fig, __file__, 'fig14_07')


# ---------- 그림 14.8 부력 ----------
def fig08():
    fig, ax = fs.canvas(5.0, 2.7, xlim=(-0.3, 9.3), ylim=(-0.4, 4.6))
    # (가) 잠긴 직육면체
    ax.add_patch(Rectangle((0, 0), 4.0, 4.0, fc=WATER, ec='none'))
    ax.plot([0, 4.0], [4.0, 4.0], color=WATER_EDGE, lw=1.2)
    surface_mark(ax, 3.6, 4.0)
    bx, by, bw, bh = 1.3, 1.0, 1.4, 1.4
    ax.add_patch(Rectangle((bx, by), bw, bh, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=3))
    for x in np.linspace(bx + 0.25, bx + bw - 0.25, 3):
        fs.arrow(ax, (x, by + bh + 0.55), (x, by + bh), color=fs.FORCE, lw=1.1, ms=8)
        fs.arrow(ax, (x, by - 0.85), (x, by), color=fs.FORCE, lw=1.1, ms=8)
    for y in np.linspace(by + 0.3, by + bh - 0.3, 2):
        L = 0.4 + 0.12 * (by + bh - y)
        fs.arrow(ax, (bx - L, y), (bx, y), color=fs.FORCE, lw=0.9, ms=7)
        fs.arrow(ax, (bx + bw + L, y), (bx + bw, y), color=fs.FORCE, lw=0.9, ms=7)
    vdim(ax, 0.3, by + bh, 4.0, r'$h$')
    vdim(ax, bx + bw + 0.75, by, by + bh, r'$L$')
    ax.text(bx + bw / 2, by + bh + 0.7, r'$p_0 + \rho_f g h$', fontsize=8.5, ha='center')
    ax.text(bx + bw / 2, by - 1.0, r'$p_0 + \rho_f g(h + L)$', fontsize=8.5, ha='center', va='center')
    ax.text(2.0, -0.35, '(가) 잠긴 물체가 받는 압력', fontsize=9, ha='center', va='top')
    # (나) 뜬 물체
    ox = 5.2
    ax.add_patch(Rectangle((ox, 0), 4.0, 2.6, fc=WATER, ec='none'))
    ax.plot([ox, ox + 4.0], [2.6, 2.6], color=WATER_EDGE, lw=1.2)
    surface_mark(ax, ox + 3.6, 2.6)
    fx, fw, fh, sub = ox + 1.3, 1.4, 1.2, 0.75
    ax.add_patch(Rectangle((fx, 2.6 - sub), fw, fh, fc='#e6d3b3', ec=fs.BLACK, lw=1.2, zorder=3))
    c = (fx + fw / 2, 2.6 - sub + fh / 2)
    fs.dot(ax, c, r=0.05)
    fs.arrow(ax, c, (c[0], c[1] - 1.3), color=fs.FORCE, lw=1.7, zorder=6)
    ax.text(c[0] - 0.1, c[1] - 1.15, r'$m\vec g$', color=fs.FORCE, fontsize=10, ha='right')
    cb = (fx + fw / 2 + 0.25, 2.6 - sub / 2)
    fs.arrow(ax, cb, (cb[0], cb[1] + 1.3), color=fs.FORCE, lw=1.7, zorder=6)
    ax.text(cb[0] + 0.12, cb[1] + 1.2, r'$\vec F_B$', color=fs.FORCE, fontsize=10, ha='left')
    vdim(ax, fx - 0.2, 2.6 - sub, 2.6, r'잠긴 부분', fontsize=8, right=False)
    ax.text(ox + 2.0, -0.35, '(나) 떠 있는 물체', fontsize=9, ha='center', va='top')
    fs.save(fig, __file__, 'fig14_08')


# ---------- 그림 14.9 흐름관과 연속 방정식 ----------
def tube(x):
    """흐름관 반폭(왼쪽 넓고 오른쪽 좁음)."""
    return 0.55 + 0.45 * (1 - np.tanh((x - 3.0) * 1.3)) / 2 * 2 * 0.5 + 0.0


def fig09():
    fig, ax = fs.canvas(4.6, 2.2, xlim=(-0.2, 6.4), ylim=(-1.6, 1.6))
    x = np.linspace(0, 6.2, 300)
    w = 0.35 + 0.65 * (1 - np.tanh((x - 3.1) * 1.4)) / 2
    ax.fill_between(x, -w, w, color=WATER, lw=0)
    ax.plot(x, w, color=fs.BLACK, lw=1.3); ax.plot(x, -w, color=fs.BLACK, lw=1.3)
    for f in (-0.6, -0.2, 0.2, 0.6):
        ax.plot(x, f * w, color=WATER_EDGE, lw=0.8)
        mid_arrowheads(ax, np.c_[x, f * w], WATER_EDGE, n=2, ms=7)
    for xs, lab, vl in [(0.9, '1', 0.5), (5.3, '2', 1.25)]:
        ws = 0.35 + 0.65 * (1 - np.tanh((xs - 3.1) * 1.4)) / 2
        ax.plot([xs, xs], [-ws, ws], color=fs.FORCE, lw=1.0, ls='--')
        ax.text(xs, -ws - 0.3, rf'$A_{lab}$', fontsize=10, ha='center')
        fs.arrow(ax, (xs - vl / 2, ws + 0.3), (xs + vl / 2, ws + 0.3), color=fs.VEL, lw=1.8, label=rf'$v_{lab}$', loff=(0.15, 0.15))
    ax.text(3.1, -1.45, r'$A_1 v_1 = A_2 v_2$', fontsize=10, ha='center')
    fs.save(fig, __file__, 'fig14_09')


# ---------- 그림 14.10 베르누이 방정식의 유도 ----------
def fig10():
    fig, ax = fs.canvas(5.0, 2.9, xlim=(-1.0, 8.5), ylim=(-0.4, 4.5))
    # 중심선: 낮고 넓은 1 → 높고 좁은 2
    t = np.linspace(0, 1, 300)
    cx = 0.3 + 7.2 * t
    cy = 1.0 + 2.0 * (3 * t ** 2 - 2 * t ** 3)
    w = 0.6 - 0.32 * (3 * t ** 2 - 2 * t ** 3)
    dx = np.gradient(cx); dyy = np.gradient(cy); n = np.c_[-dyy, dx] / np.hypot(dx, dyy)[:, None]
    up = np.c_[cx, cy] + n * w[:, None]; lo = np.c_[cx, cy] - n * w[:, None]
    ax.add_patch(Polygon(np.r_[up, lo[::-1]], closed=True, fc=WATER, ec='none'))
    ax.plot(up[:, 0], up[:, 1], color=fs.BLACK, lw=1.3); ax.plot(lo[:, 0], lo[:, 1], color=fs.BLACK, lw=1.3)
    ax.axhline(0, color=fs.GRAY, lw=0.7, xmin=0.02, xmax=0.98)
    ax.text(4.0, 0.08, '기준선', fontsize=8, color=fs.GRAY, ha='center', va='bottom')

    def slab(i0, i1, col):
        ax.add_patch(Polygon(np.r_[up[i0:i1 + 1], lo[i0:i1 + 1][::-1]], closed=True, fc=col, alpha=0.8, ec=fs.BLACK, lw=0.6, zorder=3))
    i0, i1 = 20, 40; slab(i0, i1, fs.SURF)
    j0, j1 = 262, 290; slab(j0, j1, fs.SURF)
    # 힘
    p1 = np.array([cx[i0], cy[i0]]); u1 = np.array([dx[i0], dyy[i0]]); u1 /= np.linalg.norm(u1)
    fs.arrow(ax, p1 - 0.95 * u1, p1, color=fs.FORCE, lw=1.8, label=r'$p_1A_1$', lpos=0, loff=(-0.1, 0.35))
    p2 = np.array([cx[j1], cy[j1]]); u2 = np.array([dx[j1], dyy[j1]]); u2 /= np.linalg.norm(u2)
    fs.arrow(ax, p2 + 0.95 * u2, p2, color=fs.FORCE, lw=1.8, label=r'$p_2A_2$', lpos=0, loff=(0.1, 0.35))
    # 속도
    fs.vec(ax, (cx[70], cy[70]), (0.7, 0.0), color=fs.VEL, lw=1.5, ms=9)
    ax.text(cx[70] + 0.35, cy[70] + 0.18, r'$v_1$', color=fs.VEL, fontsize=10)
    fs.vec(ax, (cx[195], cy[195]), (1.2, 0.0), color=fs.VEL, lw=1.5, ms=9)
    ax.text(cx[195] + 0.6, cy[195] + 0.18, r'$v_2$', color=fs.VEL, fontsize=10)
    ax.text(cx[30], cy[30] + w[30] + 0.3, r'$\Delta x_1$', fontsize=9, ha='center')
    ax.text(cx[276] + 0.05, cy[276] + 0.65, r'$\Delta x_2$', fontsize=9, ha='center')
    # 높이(중심선)
    ax.plot([-0.35, cx[0]], [cy[0], cy[0]], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, -0.25, 0, cy[0], r'$y_1$', right=False)
    ax.plot([cx[-1], 8.1], [cy[-1], cy[-1]], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, 7.95, 0, cy[-1], r'$y_2$')
    fs.save(fig, __file__, 'fig14_10')


# ---------- 그림 14.11 토리첼리 정리 ----------
def fig11():
    fig, ax = fs.canvas(4.2, 2.9, xlim=(-0.4, 6.8), ylim=(-0.4, 5.0))
    Hw, yh = 4.0, 1.0      # 수위, 구멍 높이 (연습문제 9)
    tw = 2.2
    ax.add_patch(Rectangle((0, 0), tw, Hw, fc=WATER, ec='none'))
    ax.plot([0, 0, tw, tw], [4.7, 0, 0, yh - 0.08], color=GLASS, lw=1.4)
    ax.plot([tw, tw], [yh + 0.08, 4.7], color=GLASS, lw=1.4)
    ax.plot([0, tw], [Hw, Hw], color=WATER_EDGE, lw=1.2)
    surface_mark(ax, 0.4, Hw)
    fs.ground(ax, -0.3, 6.6, y=0.0)
    h = Hw - yh
    v = np.sqrt(2 * 9.8 * h)
    tt = np.linspace(0, np.sqrt(2 * yh / 9.8), 100)
    jx = tw + v * tt; jy = yh - 0.5 * 9.8 * tt ** 2
    ax.plot(jx, jy, color=WATER_EDGE, lw=3.0, solid_capstyle='round')
    fs.dot(ax, (1.1, Hw), r=0.06); ax.text(1.1, Hw + 0.18, '1', fontsize=10, ha='center')
    fs.dot(ax, (tw + 0.08, yh), r=0.06); ax.text(tw + 0.2, yh + 0.25, '2', fontsize=10)
    fs.arrow(ax, (tw + 0.15, yh + 0.55), (tw + 1.1, yh + 0.55), color=fs.VEL, lw=1.6, label=r'$v = \sqrt{2gh}$', loff=(0.0, 0.35))
    ax.plot([0.9, tw], [yh, yh], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, 1.6, yh, Hw, r'$h$')
    vdim(ax, 0.6, 0, yh, r'$y$')
    fs.save(fig, __file__, 'fig14_11')


# ---------- 그림 14.12 탱크의 배수(예제 14.7) ----------
def fig12():
    fig, ax = fs.plot_axes(3.9, 2.6)
    g, H, Aa = 9.8, 2.0, (1.0 / 0.020) ** 2
    T = Aa * np.sqrt(2 * H / g)
    t = np.linspace(0, T, 300)
    ax.plot(t / 60, H * (1 - t / T) ** 2, color=fs.VEL, lw=1.9)
    th = T * (1 - 1 / np.sqrt(2))
    ax.plot([0, th / 60], [H / 2, H / 2], ls=':', color=fs.GRAY, lw=0.9)
    ax.plot([th / 60, th / 60], [0, H / 2], ls=':', color=fs.GRAY, lw=0.9)
    ax.plot(th / 60, H / 2, 'o', color=fs.FORCE, ms=4)
    ax.annotate(rf'$t = {th:.0f}$ s ($0.29T$)에 절반', (th / 60, H / 2), (9.5, 1.3), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.annotate(rf'$T = {T:.0f}$ s', (T / 60, 0), (21, 0.45), fontsize=8.5, arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.set_xlim(0, 28); ax.set_ylim(0, 2.1)
    ax.set_xlabel(r'시간 $t$ (min)'); ax.set_ylabel(r'수위 $h$ (m)')
    fs.save(fig, __file__, 'fig14_12')


# ---------- 그림 14.13 벤투리 관 ----------
def fig13():
    fig, ax = fs.canvas(4.6, 2.5, xlim=(-0.2, 7.2), ylim=(-1.2, 3.0))
    x = np.linspace(0, 7.0, 400)
    w = 0.75 - 0.4 * np.exp(-((x - 3.8) / 0.9) ** 2)
    ax.fill_between(x, -w, w, color=WATER, lw=0)
    ax.plot(x, w, color=fs.BLACK, lw=1.3); ax.plot(x, -w, color=fs.BLACK, lw=1.3)
    for f in (-0.5, 0.0, 0.5):
        ax.plot(x, f * w, color=WATER_EDGE, lw=0.7)
        mid_arrowheads(ax, np.c_[x, f * w], WATER_EDGE, n=3, ms=7)
    # 액주
    for xs, lev in [(1.2, 2.3), (3.8, 1.2)]:
        ws = 0.75 - 0.4 * np.exp(-((xs - 3.8) / 0.9) ** 2)
        ax.add_patch(Rectangle((xs - 0.12, ws), 0.24, lev - ws, fc=WATER, ec='none'))
        ax.plot([xs - 0.12, xs - 0.12], [ws, 2.8], color=GLASS, lw=1.1)
        ax.plot([xs + 0.12, xs + 0.12], [ws, 2.8], color=GLASS, lw=1.1)
        ax.plot([xs - 0.12, xs + 0.12], [lev, lev], color=WATER_EDGE, lw=1.1)
    ax.plot([1.35, 4.3], [2.3, 2.3], ls=':', color=fs.GRAY, lw=0.8)
    vdim(ax, 4.15, 1.2, 2.3, r'$\Delta p = \rho g\,\Delta h$', fontsize=8.5)
    ax.text(1.2, -1.05, r'$A_1,\ v_1,\ p_1$', fontsize=9, ha='center')
    ax.text(3.8, -0.75, r'$A_2,\ v_2,\ p_2$', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig14_13')


# ---------- 그림 14.14 점성: 두 평행판 ----------
def fig14():
    fig, ax = fs.canvas(4.0, 2.2, xlim=(-0.9, 5.6), ylim=(-0.6, 2.9))
    hgt = 2.0
    ax.add_patch(Rectangle((0, 0), 5.0, hgt, fc=WATER, ec='none'))
    ax.add_patch(Rectangle((0, -0.2), 5.0, 0.2, fc='#999999', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((0.5, hgt), 4.0, 0.2, fc='#999999', ec=fs.BLACK, lw=1.0))
    fs.arrow(ax, (4.6, hgt + 0.1), (5.4, hgt + 0.1), color=fs.FORCE, lw=1.8, label=r'$F$', loff=(0.0, 0.25))
    ax.text(2.5, hgt + 0.45, r'넓이 $A$, 속력 $u$', fontsize=8.5, ha='center')
    ax.text(2.5, -0.45, '고정된 판', fontsize=8.5, ha='center')
    x0 = 1.0
    for y in np.linspace(0.25, hgt - 0.15, 6):
        L = 2.6 * y / hgt
        fs.arrow(ax, (x0, y), (x0 + L, y), color=fs.VEL, lw=1.2, ms=8)
    ax.plot([x0, x0 + 2.6], [0, hgt], color=fs.VEL, lw=0.8, ls='--')
    ax.plot([x0, x0], [0, hgt], color=fs.BLACK, lw=0.6)
    ax.annotate('', (-0.4, hgt), (-0.4, 0), arrowprops=dict(arrowstyle='-|>', lw=0.9, mutation_scale=9))
    ax.text(-0.5, hgt - 0.1, r'$y$', fontsize=10, ha='right')
    ax.text(x0 + 2.75, 1.2, r'$v(y)$', fontsize=10, color=fs.VEL, ha='left')
    fs.save(fig, __file__, 'fig14_14')


# ---------- 그림 14.15 관 속 층흐름의 속도 분포 ----------
def fig15():
    fig, ax = fs.canvas(4.8, 2.4, xlim=(-0.8, 7.2), ylim=(-1.7, 2.0))
    R, L = 1.2, 6.0
    ax.add_patch(Rectangle((0, -R), L, 2 * R, fc=WATER, ec='none'))
    ax.plot([0, L], [R, R], color=fs.BLACK, lw=1.4); ax.plot([0, L], [-R, -R], color=fs.BLACK, lw=1.4)
    for xx in (0, L):
        ax.plot([xx, xx], [-R, R], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot([-0.3, L + 0.3], [0, 0], color=fs.GRAY, lw=0.6, ls='-.')
    # 포물선 분포
    x0, vmax = 3.4, 1.8
    yy = np.linspace(-R, R, 100)
    ax.plot(x0 + vmax * (1 - (yy / R) ** 2), yy, color=fs.VEL, lw=1.4)
    ax.plot([x0, x0], [-R, R], color=fs.BLACK, lw=0.6)
    for y in np.linspace(-R + 0.2, R - 0.2, 9):
        Lr = vmax * (1 - (y / R) ** 2)
        fs.arrow(ax, (x0, y), (x0 + Lr, y), color=fs.VEL, lw=1.0, ms=7)
    ax.text(x0 + vmax + 0.12, 0.0, r'$v_{\max}$', fontsize=9, color=fs.VEL, ha='left', va='center')
    # 반지름 r인 원기둥 계
    r = 0.55
    ax.add_patch(Rectangle((0.6, -r), 2.0, 2 * r, fc='none', ec=fs.FORCE, lw=1.1, ls='--'))
    fs.arrow(ax, (0.0, 0.0), (0.55, 0.0), color=fs.FORCE, lw=1.4, ms=8)
    ax.text(0.25, -0.25, r'$p_1$', fontsize=9, color=fs.FORCE, ha='center')
    fs.arrow(ax, (3.15, 0.0), (2.65, 0.0), color=fs.FORCE, lw=1.4, ms=8)
    ax.text(2.9, -0.25, r'$p_2$', fontsize=9, color=fs.FORCE, ha='center')
    fs.arrow(ax, (2.2, r + 0.12), (1.2, r + 0.12), color=fs.FORCE, lw=1.1, ms=7)
    ax.text(1.7, r + 0.3, '점성력', fontsize=8, color=fs.FORCE, ha='center')
    vdim(ax, 2.3, 0, r, r'$r$', fontsize=9)
    vdim(ax, -0.3, 0, R, r'$R$', right=False)
    hdim(ax, 0, L, -1.55, r'$L$')
    ax.text(0.0, R + 0.25, '흐름 방향 →', fontsize=8, ha='left')
    fs.save(fig, __file__, 'fig14_15')


# ---------- 그림 14.16 회전하는 그릇의 수면(연습문제 13) ----------
def fig16():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-2.2, 2.5), ylim=(-0.4, 4.2))
    R = 1.5; z0 = 1.4; k = 0.55      # 수면 z = z0 + k r^2 (그림용)
    r = np.linspace(-R, R, 200)
    z = z0 + k * r ** 2
    ax.fill_between(r, 0, z, color=WATER, lw=0)
    ax.plot(r, z, color=WATER_EDGE, lw=1.3)
    h0 = z0 + k * R ** 2 / 2
    ax.plot([-R, R], [h0, h0], ls='--', color=fs.GRAY, lw=0.8)
    ax.annotate('돌리기 전 수면', (-0.55, h0), (-0.6, 2.85), fontsize=7.5, color=fs.GRAY, ha='center', arrowprops=dict(arrowstyle='-', lw=0.5, color=fs.GRAY))
    ax.plot([-R, -R, R, R], [3.4, 0, 0, 3.4], color=GLASS, lw=1.4)
    ax.plot([0, 0], [-0.2, 3.9], ls='-.', color=fs.GRAY, lw=0.8)
    th = np.radians(np.linspace(200, 500, 80))
    pts = np.c_[0.5 * np.cos(th), 3.75 + 0.13 * np.sin(th)]
    ax.plot(pts[:-2, 0], pts[:-2, 1], color=fs.ACC, lw=1.1)
    ax.add_patch(FancyArrowPatch(pts[-4], pts[-1], arrowstyle='-|>', mutation_scale=9, color=fs.ACC, lw=1.1))
    ax.text(0.62, 3.85, r'$\omega$', fontsize=11, color=fs.ACC)
    ax.text(0.08, z0 - 0.25, r'$z_0$', fontsize=9, ha='left')
    vdim(ax, R + 0.35, 0, z0 + k * R ** 2, r'$z(R)$', fontsize=9)
    hdim(ax, 0, R, -0.3, r'$R$', above=False)
    ax.text(-1.0, 0.5, r'$z(r)$', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig14_16')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16):
        f()
