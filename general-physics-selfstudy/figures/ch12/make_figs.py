"""12장 평형과 탄성 — 그림 생성 스크립트.

    python3 figures/ch12/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch


# ---------- 이 장 전용 도우미 ----------
def support(ax, x, y, s=0.22):
    """받침(삼각형)과 바닥 빗금. 꼭짓점이 (x, y)."""
    ax.add_patch(Polygon([(x - s, y - 1.6 * s), (x + s, y - 1.6 * s), (x, y)], closed=True,
                         fc='#dddddd', ec=fs.BLACK, lw=1.0, zorder=2))
    fs.ground(ax, x - 1.6 * s, x + 1.6 * s, y=y - 1.6 * s, depth=0.1)


def hinge(ax, p, r=0.08):
    ax.add_patch(Circle(p, r, fc='white', ec=fs.BLACK, lw=1.1, zorder=7))


def cg_mark(ax, p, r=0.11, color=fs.BLACK):
    """무게중심 기호(원 안의 +)."""
    ax.add_patch(Circle(p, r, fc='white', ec=color, lw=1.0, zorder=8))
    ax.plot([p[0] - r, p[0] + r], [p[1], p[1]], color=color, lw=0.9, zorder=9)
    ax.plot([p[0], p[0]], [p[1] - r, p[1] + r], color=color, lw=0.9, zorder=9)


def hdim(ax, x0, x1, y, text, color=fs.GRAY, fontsize=9, above=True, ticks=None):
    """수평 치수선 x0–x1 (높이 y). ticks=(y_from, ...)이면 그 높이에서 치수선까지 보조선."""
    ax.annotate('', (x0, y), (x1, y), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.8,
                                                       mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (0.06 if above else -0.06), text, fontsize=fontsize, color=color,
            ha='center', va='bottom' if above else 'top')
    if ticks is not None:
        for x, yt in zip((x0, x1), ticks):
            if yt is not None:
                ax.plot([x, x], [yt, y - 0.08 if yt > y else y + 0.08], color=color, lw=0.5)


def vdim(ax, x, y0, y1, text, color=fs.GRAY, fontsize=9, right=True):
    ax.annotate('', (x, y0), (x, y1), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.8,
                                                       mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(x + (0.08 if right else -0.08), (y0 + y1) / 2, text, fontsize=fontsize, color=color,
            ha='left' if right else 'right', va='center')


def rot(pts, ang, about=(0, 0)):
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s], [s, c]])
    return (np.asarray(pts, float) - about) @ R.T + about


# ---------- 그림 12.1 두 받침 위의 판자 ----------
def fig01():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.7, 4.8), ylim=(-2.45, 1.75))
    k = 1 / 400   # 1 N → 그림 단위
    ax.add_patch(Rectangle((0, 0), 4.0, 0.14, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    support(ax, 0.0, -0.02); support(ax, 4.0, -0.02)
    fs.arrow(ax, (0.0, 0.14), (0.0, 0.14 + 539 * k), color=fs.FORCE, label=r'$N_L$', loff=(-0.3, -0.25))
    fs.arrow(ax, (4.0, 0.14), (4.0, 0.14 + 245 * k), color=fs.FORCE, label=r'$N_R$', loff=(0.32, -0.1))
    fs.arrow(ax, (2.0, 0.07), (2.0, 0.07 - 196 * k), color=fs.FORCE, zorder=6)
    ax.text(2.12, -0.3, r'판자 무게 $196\ \mathrm{N}$', fontsize=8.5, color=fs.FORCE, ha='left', va='center')
    fs.arrow(ax, (1.0, 0.07), (1.0, 0.07 - 588 * k), color=fs.FORCE, zorder=6)
    ax.text(1.12, -1.2, r'사람이 누르는 힘 $588\ \mathrm{N}$', fontsize=8.5, color=fs.FORCE, ha='left', va='center')
    fs.dot(ax, (2.0, 0.07), r=0.05)
    hdim(ax, 0, 1.0, -1.85, r'$1.0\ \mathrm{m}$', ticks=(-0.5, -1.45))
    hdim(ax, 1.0, 2.0, -1.85, r'$1.0\ \mathrm{m}$', ticks=(None, -0.45))
    hdim(ax, 0, 4.0, -2.35, r'$4.0\ \mathrm{m}$', ticks=(-1.85, -0.4))
    fs.save(fig, __file__, 'fig12_01')


# ---------- 그림 12.2 매달아서 무게중심 찾기 ----------
def fig02():
    fig, axs = plt.subplots(1, 2, figsize=(4.6, 2.9))
    shape = np.array([(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)], float)
    cg = np.array([1.1, 1.1])          # 넓이 가중 평균: 3·(1.5, 0.5)과 2·(0.5, 2.0)
    holes = [np.array([2.75, 0.5]), np.array([0.5, 2.75])]
    names = ['A', 'B']
    for ax, h, nm in zip(axs, holes, names):
        v = cg - h
        ang = -np.pi / 2 - np.arctan2(v[1], v[0])
        sh = rot(shape, ang, h); c2 = rot(cg, ang, h)
        other = rot(holes[1 - names.index(nm)], ang, h)
        ax.add_patch(Polygon(sh, closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2))
        ax.plot([h[0], h[0]], [h[1] + 0.6, h[1]], color=fs.BLACK, lw=1.0)
        fs.ceiling(ax, h[0] - 0.5, h[0] + 0.5, h[1] + 0.6, depth=0.12)
        ax.add_patch(Circle(h, 0.09, fc='white', ec=fs.BLACK, lw=1.0, zorder=6))
        ax.add_patch(Circle(other, 0.07, fc='white', ec=fs.GRAY, lw=0.8, zorder=6))
        bot = h[1] - 3.5
        ax.plot([h[0], h[0]], [h[1], bot], ls='--', color=fs.FIELD, lw=1.0, zorder=5)
        ax.add_patch(Polygon([(h[0] - 0.09, bot), (h[0] + 0.09, bot), (h[0], bot - 0.2)], closed=True,
                             fc=fs.FIELD, ec='none', zorder=6))
        cg_mark(ax, c2)
        ax.text(h[0] + 0.2, h[1] + 0.12, nm, fontsize=11)
        ax.text(c2[0] + 0.2, c2[1] - 0.05, 'G', fontsize=11)
        ax.set_xlim(h[0] - 2.4, h[0] + 2.4); ax.set_ylim(h[1] - 3.9, h[1] + 0.8)
        ax.set_aspect('equal'); ax.axis('off')
    axs[0].text(holes[0][0], holes[0][1] - 4.1, '(가) A에 매달 때', fontsize=9, ha='center', va='top')
    axs[1].text(holes[1][0], holes[1][1] - 4.1, '(나) B에 매달 때', fontsize=9, ha='center', va='top')
    for ax in axs:
        ax.set_ylim(ax.get_ylim()[0] - 0.45, ax.get_ylim()[1])
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig12_02')


# ---------- 그림 12.3 넘어지기 직전의 상자 ----------
def fig03():
    fig, ax = fs.canvas(3.6, 2.9, xlim=(-0.3, 5.3), ylim=(-0.3, 4.2))
    th = np.arctan(0.40)                 # tanθ = w/h = 0.40 → 21.8°
    u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    fs.incline(ax, (0, 0), length=5.4, angle=np.degrees(th), angle_label=r'$\theta$')
    w, h = 0.8, 2.0
    c0 = 2.3 * u                      # 아래쪽 모서리
    box = [c0, c0 + w * u, c0 + w * u + h * n, c0 + h * n]
    ax.add_patch(Polygon(box, closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=3))
    G = c0 + w / 2 * u + h / 2 * n
    ax.plot([G[0], G[0]], [G[1] + 1.2, c0[1] - 0.45], ls='--', color=fs.GRAY, lw=1.0, zorder=4)
    ax.text(G[0] + 0.08, G[1] + 1.15, '연직선', fontsize=8, color=fs.GRAY, ha='left')
    fs.arrow(ax, G, G + np.array([0, -0.85]), color=fs.FORCE, lw=1.6, zorder=7)
    ax.text(G[0] - 0.15, G[1] - 0.7, r'$M\vec g$', color=fs.FORCE, fontsize=11, ha='right')
    cg_mark(ax, G)
    fs.dim(ax, c0 + h * n, c0 + w * u + h * n, r'$w$', off=0.25)
    fs.dim(ax, c0 + w * u, c0 + w * u + h * n, r'$h$', off=-0.28)
    fs.dot(ax, c0, r=0.05)
    ax.text(c0[0] - 0.2, c0[1] + 0.12, '모서리', fontsize=8, ha='right')
    fs.save(fig, __file__, 'fig12_03')


# ---------- 그림 12.4 줄로 지탱한 수평 보 ----------
def fig04():
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.6))
    th = np.radians(30); Lb = 3.0
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    # (가) 장치
    ax = axs[0]
    fs.wall(ax, -1.1, 2.3, x=0.0, side='left')
    ax.add_patch(Rectangle((0, -0.08), Lb, 0.16, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    hinge(ax, (0, 0))
    top = (0, Lb * np.tan(th))
    ax.plot([Lb, top[0]], [0, top[1]], color=fs.BLACK, lw=1.0)
    fs.dot(ax, top, r=0.04)
    fs.angle_arc(ax, (Lb, 0), 0.55, 150, 180, r'$30^\circ$', fontsize=9, tr=0.85)
    ax.plot([Lb - 0.1, Lb - 0.1], [-0.08, -0.55], color=fs.BLACK, lw=1.0)
    fs.block(ax, (Lb - 0.1, -0.8), w=0.55, h=0.5, text=r'$50\ \mathrm{kg}$', fontsize=8)
    hdim(ax, 0, Lb, -1.45, r'$3.0\ \mathrm{m}$', above=False, ticks=(-1.0, -0.15))
    ax.text(1.5, 0.22, r'$20\ \mathrm{kg}$', fontsize=8, ha='center')
    ax.text(0.25, -0.35, '경첩', fontsize=8)
    ax.set_xlim(-0.45, 3.5); ax.set_ylim(-1.85, 2.0)
    ax.text(1.5, -1.95, '(가) 장치', fontsize=9, ha='center', va='top')
    # (나) 보의 자유물체도
    ax = axs[1]
    ax.add_patch(Rectangle((0, -0.08), Lb, 0.16, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    hinge(ax, (0, 0))
    uT = np.array([-np.cos(th), np.sin(th)])
    fs.arrow(ax, (Lb, 0), (Lb, 0) + 1.5 * uT, color=fs.FORCE, lw=1.8, label=r'$\vec T$', lpos=1.0, loff=(0.0, 0.2))
    fs.angle_arc(ax, (Lb, 0), 0.5, 150, 180, r'$30^\circ$', fontsize=9, tr=0.78)
    fs.arrow(ax, (0, 0), (0.9, 0), color=fs.FORCE, lw=1.6, label=r'$H_x$', loff=(0.05, -0.3), zorder=6)
    fs.arrow(ax, (0, 0), (0, 0.85), color=fs.FORCE, lw=1.6, label=r'$H_y$', loff=(-0.3, -0.1), zorder=6)
    fs.arrow(ax, (1.5, 0), (1.5, -0.55), color=fs.FORCE, lw=1.6, zorder=6)
    ax.text(1.5, -0.85, r'$(20)(9.8)\ \mathrm{N}$', color=fs.FORCE, fontsize=8, ha='center')
    fs.arrow(ax, (Lb, 0), (Lb, -1.0), color=fs.FORCE, lw=1.6, zorder=6)
    ax.text(Lb - 0.1, -1.3, r'$(50)(9.8)\ \mathrm{N}$', color=fs.FORCE, fontsize=8, ha='center')
    fs.dot(ax, (1.5, 0), r=0.04)
    ax.set_xlim(-0.45, 3.5); ax.set_ylim(-1.85, 2.0)
    ax.text(1.5, -1.95, '(나) 보의 자유물체도', fontsize=9, ha='center', va='top')
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig12_04')


# ---------- 그림 12.5 벽에 기댄 사다리 ----------
def fig05():
    fig, ax = fs.canvas(3.4, 3.2, xlim=(-1.3, 3.2), ylim=(-0.6, 4.0))
    th = np.radians(55); L = 4.0
    xw = L * np.cos(th)
    fs.ground(ax, -1.2, xw + 0.05, y=0.0)
    fs.wall(ax, -0.1, 3.9, x=xw, side='right')
    top = np.array([xw, L * np.sin(th)])
    ax.plot([0, top[0]], [0, top[1]], color='#8a6d3b', lw=4.0, solid_capstyle='butt', zorder=3)
    mid = top / 2
    fs.dot(ax, mid, r=0.06)
    fs.arrow(ax, mid, mid + np.array([0, -1.2]), color=fs.FORCE, lw=1.6, label=r'$m\vec g$', loff=(0.35, 0.2), zorder=7)
    fs.arrow(ax, (0, 0), (0, 1.2), color=fs.FORCE, lw=1.6, label=r'$\vec N_f$', loff=(-0.35, -0.1), zorder=7)
    fs.arrow(ax, (0, 0), (0.75, 0), color=fs.FORCE, lw=1.6, label=r'$\vec f$', loff=(0.22, 0.15), zorder=7)
    fs.arrow(ax, top, top + np.array([-0.75, 0]), color=fs.FORCE, lw=1.6, label=r'$\vec N_w$', loff=(-0.1, 0.25), zorder=7)
    fs.angle_arc(ax, (0, 0), 0.55, 0, 55, r'$\theta$', fontsize=11, tr=0.8)
    fs.dim(ax, (0, 0), top, r'$L$', off=0.32)
    ax.text(xw - 0.12, 1.2, '마찰 없는 벽', fontsize=8, ha='right')
    fs.save(fig, __file__, 'fig12_05')


# ---------- 그림 12.6 세 가지 변형 ----------
def fig06():
    fig, ax = fs.canvas(5.6, 2.1, xlim=(-0.5, 13.3), ylim=(-1.3, 3.3))
    # (가) 인장
    L0, A = 3.2, 0.7
    ax.add_patch(Rectangle((0.5, 1.0), L0, A, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=2))
    ax.add_patch(Rectangle((0.5, 1.05), L0 + 0.6, A - 0.1, fc='none', ec=fs.GRAY, lw=0.9, ls='--', zorder=3))
    fs.arrow(ax, (0.5, 1.35), (-0.4, 1.35), color=fs.FORCE, lw=1.6, label=r'$\vec F_\perp$', loff=(0.2, 0.42))
    fs.arrow(ax, (L0 + 1.1, 1.35), (L0 + 1.95, 1.35), color=fs.FORCE, lw=1.6, label=r'$\vec F_\perp$', loff=(-0.2, 0.42))
    fs.dim(ax, (0.5, 1.0), (0.5 + L0, 1.0), r'$L_0$', off=-0.35)
    fs.dim(ax, (0.5 + L0, 1.0), (1.1 + L0, 1.0), r'$\Delta L$', off=-0.35)
    ax.text(0.85, 1.35, r'$A$', fontsize=10, ha='center', va='center')
    ax.text(2.3, -1.15, '(가) 인장', fontsize=9, ha='center')
    # (나) 전단
    x0, hh, ww, dx = 6.0, 2.0, 2.0, 0.6
    fs.ground(ax, x0 - 0.4, x0 + ww + 1.0, y=0.0)
    ax.add_patch(Rectangle((x0, 0), ww, hh, fc='none', ec=fs.GRAY, lw=0.9, ls='--', zorder=2))
    ax.add_patch(Polygon([(x0, 0), (x0 + ww, 0), (x0 + ww + dx, hh), (x0 + dx, hh)], closed=True,
                         fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    fs.arrow(ax, (x0 + dx + 0.2, hh + 0.12), (x0 + dx + 1.6, hh + 0.12), color=fs.FORCE, lw=1.6,
             label=r'$\vec F_\parallel$', loff=(0.15, 0.32))
    fs.dim(ax, (x0, hh), (x0 + dx, hh), r'$\Delta x$', off=0.75)
    fs.dim(ax, (x0, 0), (x0, hh), r'$h$', off=0.35)
    ax.text(x0 + 1.0, -1.15, '(나) 전단', fontsize=9, ha='center')
    # (다) 부피
    c = np.array([11.6, 1.2]); s0, s1 = 1.05, 0.88
    ax.add_patch(Rectangle(c - s0 / 2 * np.array([1.6, 1.6]), 1.6 * s0, 1.6 * s0, fc='none', ec=fs.GRAY, lw=0.9, ls='--', zorder=2))
    ax.add_patch(Rectangle(c - s1 / 2 * np.array([1.6, 1.6]), 1.6 * s1, 1.6 * s1, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    for ang in range(0, 360, 45):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
        p0 = c + d * 1.65; p1 = c + d * 0.95
        if ang % 90:
            p0 = c + d * 1.85; p1 = c + d * 1.2
        fs.arrow(ax, p0, p1, color=fs.FORCE, lw=1.2, ms=9)
    ax.text(c[0], c[1], r'$V_0 + \Delta V$', fontsize=7.5, ha='center', va='center', zorder=6)
    ax.text(c[0] + 1.25, c[1] + 1.8, r'$\Delta p$', fontsize=10, color=fs.FORCE)
    ax.text(c[0], -1.15, '(다) 부피 압축', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig12_06')


# ---------- 그림 12.7 응력–변형률 곡선 ----------
def stress(e):
    eA, sA = 1.0, 1.0           # 비례 한계
    eB, sB = 1.3, 1.10          # 항복점
    eC, sC = 6.0, 1.60          # 극한 강도
    eD = 7.6
    e = np.asarray(e, float); s = np.zeros_like(e)
    m = e <= eA; s[m] = e[m]
    m = (e > eA) & (e <= eB)    # A→B: 기울기 1에서 hardening 기울기로 매끄럽게(3차 에르미트)
    kB = 2 * (sC - sB) / (eC - eB)
    t = (e[m] - eA) / (eB - eA); hlen = eB - eA
    h00, h10, h01, h11 = 2*t**3 - 3*t**2 + 1, t**3 - 2*t**2 + t, -2*t**3 + 3*t**2, t**3 - t**2
    s[m] = h00 * sA + h10 * hlen * 1.0 + h01 * sB + h11 * hlen * kB
    m = (e > eB) & (e <= eC); s[m] = sC - (sC - sB) * ((eC - e[m]) / (eC - eB)) ** 2
    m = e > eC; s[m] = sC - 0.11 * (e[m] - eC) ** 2
    return s, (eA, sA, eB, sB, eC, sC, eD)


def fig07():
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    e = np.linspace(0, 7.6, 800)
    s, (eA, sA, eB, sB, eC, sC, eD) = stress(e)
    sD = stress([eD])[0][0]
    ax.plot(e, s, color=fs.VEL, lw=1.9)
    ax.plot(eD, sD, marker='x', color=fs.FORCE, ms=9, mew=2)
    for (x, y, nm, txt, dx, dy) in [(eA, sA, 'A', '비례 한계', 0.18, -0.08), (eB, sB, 'B', '항복점', -0.1, 0.16),
                                     (eC, sC, 'C', '극한 강도', 0.0, 0.12), (eD, sD, 'D', '파단', 0.2, 0.12)]:
        ax.plot(x, y, 'o', color=fs.BLACK, ms=3.5, zorder=5)
        ax.text(x + dx, y + dy, f'{nm}  {txt}' if nm != 'A' else f'{nm}  {txt}', fontsize=8.5,
                ha='left' if nm in ('A', 'D') else 'center')
    # 기울기 = Y
    ax.plot([0.35, 0.75, 0.75], [0.35, 0.35, 0.75], color=fs.GRAY, lw=0.8)
    ax.text(0.82, 0.48, r'기울기 $= Y$', fontsize=8.5, color=fs.GRAY)
    # 하중 제거
    eu = 4.0; su = stress([eu])[0][0]
    ax.plot([eu, eu - su], [su, 0], ls='--', color=fs.ORANGE, lw=1.2)
    ax.plot(eu, su, 'o', color=fs.ORANGE, ms=3.5)
    ax.add_patch(FancyArrowPatch((eu - su / 2 + 0.05, su / 2 + 0.05), (eu - su / 2 - 0.12, su / 2 - 0.12),
                                 arrowstyle='-|>', mutation_scale=9, color=fs.ORANGE, lw=0))
    ax.annotate('', (0, 0.06), (eu - su, 0.06), arrowprops=dict(arrowstyle='<->', color=fs.ORANGE, lw=0.9))
    ax.text((eu - su) / 2, 0.13, '영구 변형', fontsize=8, color=fs.ORANGE, ha='center')
    ax.text(eu + 0.05, su / 2, '힘을 없애면\n$OA$와 나란히 돌아온다', fontsize=8, color=fs.ORANGE, ha='left', va='center')
    ax.text(-0.15, -0.05, 'O', fontsize=9, ha='right', va='top')
    ax.set_xlim(0, 8.2); ax.set_ylim(0, 1.95)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel(r'변형률 $\varepsilon$'); ax.set_ylabel(r'응력 $\sigma$')
    fs.save(fig, __file__, 'fig12_07')


# ---------- 그림 12.8 세 줄에 매단 강체 막대 ----------
def fig08():
    fig, ax = fs.canvas(4.4, 2.8, xlim=(-0.7, 4.9), ylim=(-1.45, 2.75))
    L = 4.0; y0 = 0.9; top = 2.5
    fs.ceiling(ax, -0.4, L + 0.4, top)
    dl = np.array([7, 4, 1]) * 0.07       # 늘어난 길이 ∝ 장력 7:4:1 (과장)
    xs = np.array([0, L / 2, L])
    ys = y0 - dl
    ax.plot([0, L], [y0, y0], ls='--', color=fs.GRAY, lw=0.9)
    ax.text(3.0, y0 + 0.04, '처음 위치', fontsize=8, color=fs.GRAY, va='bottom', ha='center')
    nrm = np.array([-(ys[2] - ys[0]), L]); nrm = nrm / np.linalg.norm(nrm) * 0.07
    p0, p1 = np.array([0, ys[0]]), np.array([L, ys[2]])
    ax.add_patch(Polygon([p0 + nrm, p1 + nrm, p1 - nrm, p0 - nrm], closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    k = 0.11
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.plot([x, x], [top, y], color=fs.BLACK, lw=0.9, zorder=2)
        T = [7, 4, 1][i]
        fs.arrow(ax, (x + 0.12, y + 0.05), (x + 0.12, y + 0.05 + T * k), color=fs.FORCE, lw=1.5, ms=9, zorder=6)
        ax.text(x + 0.22, y + 0.12 + T * k / 2, rf'$T_{i + 1}$', color=fs.FORCE, fontsize=10, ha='left', va='center')
    xw = L / 4; yw = ys[0] + (ys[2] - ys[0]) * xw / L
    ax.plot([xw, xw], [yw, yw - 0.35], color=fs.BLACK, lw=0.9)
    fs.arrow(ax, (xw, yw - 0.35), (xw, yw - 0.35 - 12 * k * 0.6), color=fs.FORCE, lw=1.6, label=r'$W$', loff=(0.3, 0.25))
    for x, lab in zip([0, L / 4, L / 2, L], ['0', r'$L/4$', r'$L/2$', r'$L$']):
        ax.text(x, -1.35, lab, fontsize=9, ha='center')
        ax.plot([x, x], [-1.1, -1.0], color=fs.GRAY, lw=0.6)
    ax.plot([0, L], [-1.05, -1.05], color=fs.GRAY, lw=0.6)
    ax.text(-0.45, -1.05, r'$x$', fontsize=10, color=fs.GRAY, va='center')
    fs.save(fig, __file__, 'fig12_08')


# ---------- 그림 12.9 외팔보의 굽힘 ----------
def fig09():
    fig, ax = fs.canvas(4.6, 2.5, xlim=(-0.6, 6.4), ylim=(-2.4, 1.2))
    L, h, dlt = 4.6, 0.36, 1.1
    fs.wall(ax, -1.0, 1.0, x=0.0, side='left')
    x = np.linspace(0, L, 200)
    w = -dlt * x ** 2 * (3 * L - x) / (2 * L ** 3)
    wp = -dlt * (6 * L * x - 3 * x ** 2) / (2 * L ** 3)
    nx, ny = -wp / np.sqrt(1 + wp ** 2), 1 / np.sqrt(1 + wp ** 2)
    upper = np.c_[x + nx * h / 2, w + ny * h / 2]; lower = np.c_[x - nx * h / 2, w - ny * h / 2]
    ax.add_patch(Rectangle((0, -h / 2), L, h, fc='none', ec=fs.GRAY, lw=0.8, ls='--', zorder=1))
    ax.add_patch(Polygon(np.r_[upper, lower[::-1]], closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=2))
    ax.plot(x, w, ls='-.', color=fs.FIELD, lw=0.9, zorder=3)
    w1 = -dlt * 1.2 ** 2 * (3 * L - 1.2) / (2 * L ** 3)
    ax.annotate('중립축', (1.2, w1), (0.8, -1.0), fontsize=8, color=fs.FIELD, ha='center',
                arrowprops=dict(arrowstyle='-', color=fs.FIELD, lw=0.6))
    ax.text(1.4, 0.4, '위쪽: 늘어남(인장)', fontsize=8, ha='center')
    ax.text(2.6, -1.3, '아래쪽: 줄어듦(압축)', fontsize=8, ha='center')
    tip = np.array([L, w[-1]])
    fs.arrow(ax, tip + np.array([0, -h / 2]), tip + np.array([0, -h / 2 - 0.9]), color=fs.FORCE, lw=1.7,
             label=r'$\vec F$', loff=(0.25, 0.2))
    ax.plot([L, L + 0.5], [0, 0], color=fs.GRAY, lw=0.5)
    vdim(ax, L + 0.4, 0, w[-1], r'$\delta$')
    hdim(ax, 0, L, 0.85, r'$L$', ticks=(0.2, 0.2))
    # 단면
    cx, cy, b, hh = 5.85, -1.7, 0.55, 0.32
    ax.add_patch(Rectangle((cx - b / 2, cy - hh / 2), b, hh, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    ax.plot([cx - b / 2 - 0.12, cx + b / 2 + 0.12], [cy, cy], ls='-.', color=fs.FIELD, lw=0.8)
    ax.text(cx, cy - hh / 2 - 0.22, r'$b$', fontsize=9, ha='center')
    ax.text(cx + b / 2 + 0.12, cy + 0.2, r'$h$', fontsize=9, ha='left')
    ax.text(cx, cy + hh / 2 + 0.22, '단면', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig12_09')


# ---------- 그림 12.10 아래팔(연습문제 6) ----------
def fig10():
    fig, ax = fs.canvas(4.2, 2.9, xlim=(-1.0, 4.2), ylim=(-2.3, 2.4))
    # 위팔과 아래팔
    ax.add_patch(Rectangle((-0.2, 0.15), 0.4, 2.2, fc='#efe3d6', ec=fs.BLACK, lw=1.0, zorder=1))
    ax.add_patch(Rectangle((0, -0.15), 3.6, 0.3, fc='#efe3d6', ec=fs.BLACK, lw=1.0, zorder=2))
    ax.add_patch(Circle((0, 0), 0.08, fc='white', ec=fs.BLACK, lw=1.0, zorder=7))
    ax.text(-0.15, -0.05, '팔꿈치', fontsize=8, ha='right', va='center')
    # 이두근
    ax.plot([0.4, 0.4], [0.15, 1.9], color='#b9554b', lw=3.5, alpha=0.6, zorder=3)
    fs.arrow(ax, (0.4, 0.15), (0.4, 1.4), color=fs.FORCE, lw=1.8, label=r'$\vec F$', loff=(0.3, -0.05), zorder=6)
    ax.text(0.65, 1.85, '이두근', fontsize=8, ha='left')
    # 무게
    fs.arrow(ax, (1.5, 0), (1.5, -0.7), color=fs.FORCE, lw=1.5, zorder=6)
    ax.text(1.5, -0.9, '아래팔의 무게', fontsize=8, ha='center', color=fs.FORCE)
    fs.dot(ax, (1.5, 0), r=0.04)
    ax.add_patch(Circle((3.5, 0.45), 0.3, fc='#dfe6ee', ec=fs.BLACK, lw=1.0, zorder=3))
    ax.text(3.5, 0.45, r'$5.0$ kg', fontsize=7, ha='center', va='center', zorder=4)
    fs.arrow(ax, (3.5, 0), (3.5, -1.0), color=fs.FORCE, lw=1.5, zorder=6)
    ax.text(3.5, -1.2, '공의 무게', fontsize=8, ha='center', color=fs.FORCE)
    hdim(ax, 0, 0.4, -0.5, r'$4.0\ \mathrm{cm}$', above=False, fontsize=8, ticks=(-0.15, -0.15))
    hdim(ax, 0, 1.5, -1.45, r'$15\ \mathrm{cm}$', fontsize=8, ticks=(-0.75, -0.75))
    hdim(ax, 0, 3.5, -1.95, r'$35\ \mathrm{cm}$', above=False, fontsize=8, ticks=(-1.45, -1.3))
    fs.save(fig, __file__, 'fig12_10')


# ---------- 그림 12.11 턱을 넘는 바퀴(연습문제 9) ----------
def fig11():
    fig, ax = fs.canvas(3.4, 2.6, xlim=(-1.6, 3.6), ylim=(-0.4, 3.4))
    R, h = 1.5, 0.5
    C = np.array([0.0, R])
    qx = np.sqrt(R ** 2 - (R - h) ** 2)
    fs.ground(ax, -1.5, qx, y=0.0)
    ax.add_patch(Polygon([(qx, 0), (3.0, 0), (3.0, h), (qx, h)], closed=True, fc='#dddddd', ec=fs.BLACK, lw=1.1, zorder=1))
    ax.add_patch(Circle(C, R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2))
    fs.dot(ax, C, r=0.06)
    fs.arrow(ax, C, C + np.array([1.3, 0]), color=fs.FORCE, lw=1.8, label=r'$\vec F$', loff=(0.0, 0.25), zorder=7)
    fs.arrow(ax, C, C + np.array([0, -1.0]), color=fs.FORCE, lw=1.6, label=r'$W$', loff=(-0.3, 0.2), zorder=7)
    pR = C + R * np.array([np.cos(np.radians(125)), np.sin(np.radians(125))])
    ax.plot([C[0], pR[0]], [C[1], pR[1]], color=fs.BLACK, lw=0.8)
    ax.text((C[0] + pR[0]) / 2 + 0.1, (C[1] + pR[1]) / 2 + 0.15, r'$R$', fontsize=11)
    vdim(ax, 3.2, 0, h, r'$h$')
    ax.plot([3.0, 3.3], [h, h], color=fs.GRAY, lw=0.5); ax.plot([3.0, 3.3], [0, 0], color=fs.GRAY, lw=0.5)
    fs.dot(ax, (qx, h), r=0.05)
    ax.text(qx + 0.12, h + 0.15, '턱 모서리', fontsize=8, ha='left')
    fs.save(fig, __file__, 'fig12_11')


# ---------- 그림 12.12 처진 강철선(연습문제 14) ----------
def fig12():
    fig, ax = fs.canvas(4.0, 1.9, xlim=(-2.6, 2.6), ylim=(-1.5, 0.6))
    L, y = 2.0, 0.55
    for s in (-1, 1):
        fs.wall(ax, -0.4, 0.4, x=s * L, side='left' if s < 0 else 'right')
    ax.plot([-L, 0, L], [0, -y, 0], color=fs.BLACK, lw=1.0)
    ax.plot([-L, L], [0, 0], ls=':', color=fs.GRAY, lw=0.8)
    fs.dot(ax, (0, -y), r=0.05)
    fs.arrow(ax, (0, -y), (0, -y - 0.75), color=fs.FORCE, lw=1.6, label=r'$W$', loff=(0.25, 0.15))
    for s in (-1, 1):
        u = np.array([s * L, y]) / np.hypot(L, y)
        fs.arrow(ax, (0, -y), np.array([0, -y]) + 0.9 * u, color=fs.FORCE, lw=1.4, ms=9)
        ax.text(s * 0.8, -y + 0.48, r'$T$', color=fs.FORCE, fontsize=11, ha='center')
    vdim(ax, 0.0, 0, -y + 0.06, r'$y$')
    ax.annotate('', (-L, 0.4), (0, 0.4), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.annotate('', (0, 0.4), (L, 0.4), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(-L / 2, 0.47, r'$L$', fontsize=10, color=fs.GRAY, ha='center', va='bottom')
    ax.text(L / 2, 0.47, r'$L$', fontsize=10, color=fs.GRAY, ha='center', va='bottom')
    fs.save(fig, __file__, 'fig12_12')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12):
        f()
