"""31장 전자기파 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Ellipse

E_COL = fs.FORCE      # 전기장: 빨강 계열로 구분
B_COL = fs.VEL        # 자기장: 파랑
S_COL = fs.ACC        # 포인팅 벡터: 초록


# ---------- 비스듬한 투영 (x 오른쪽, y 위, z 앞쪽: 왼쪽 아래로) ----------
ZX, ZY = -0.55, -0.32


def P(x, y, z):
    return (x + ZX * z, y + ZY * z)


def P3(pts):
    pts = np.asarray(pts, float)
    return pts[:, 0] + ZX * pts[:, 2], pts[:, 1] + ZY * pts[:, 2]


# ---------- 그림 31.1 쌍극자 안테나와 복사의 방향 분포 ----------
def fig01():
    fig, ax = fs.canvas(5.0, 3.4, xlim=(-2.6, 3.4), ylim=(-1.9, 2.1))
    # 안테나: 위아래 도선과 가운데 교류 전원
    ax.plot([0, 0], [0.15, 1.1], color=fs.BLACK, lw=2.4)
    ax.plot([0, 0], [-1.1, -0.15], color=fs.BLACK, lw=2.4)
    ax.add_patch(Circle((-0.0, 0), 0.15, fc='white', ec=fs.BLACK, lw=1.1, zorder=5))
    t = np.linspace(-0.09, 0.09, 40)
    ax.plot(t, 0.05 * np.sin(t / 0.09 * np.pi), color=fs.BLACK, lw=0.9, zorder=6)
    fs.charge(ax, (0, 1.1), +1, r=0.13, fontsize=9)
    fs.charge(ax, (0, -1.1), -1, r=0.13, fontsize=9)
    ax.annotate('', xy=(-0.35, 0.9), xytext=(-0.35, 0.3),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.9, mutation_scale=9))
    fs.label(ax, (-0.72, 0.95), '진동', fontsize=8, color=fs.GRAY)
    # sin^2 복사 패턴 (극좌표: 안테나 축에서 잰 각 theta)
    th = np.linspace(0, 2 * np.pi, 400)
    r = 1.7 * np.sin(th) ** 2
    ax.plot(r * np.sin(th), r * np.cos(th), color=fs.ORANGE, lw=1.2, ls='--', zorder=2)
    ax.fill(r * np.sin(th), r * np.cos(th), color=fs.ORANGE, alpha=0.08, zorder=1)
    # 축 (점선) 과 각 theta
    ax.plot([0, 0], [1.25, 1.9], color=fs.GRAY, lw=0.7, ls=':')
    thP = np.radians(55)
    R = 2.35
    Pp = np.array([R * np.sin(thP), R * np.cos(thP)])
    ax.plot([0, Pp[0]], [0, Pp[1]], color=fs.GRAY, lw=0.7, ls=':')
    fs.angle_arc(ax, (0, 0), 0.75, 90 - 55, 90, r'$\theta$', fontsize=10)
    # 먼 점 P에서의 E (theta-hat), B (phi-hat: 지면 안쪽), S (r-hat)
    rhat = Pp / R
    thhat = np.array([np.cos(thP), -np.sin(thP)])
    fs.dot(ax, Pp, r=0.04)
    fs.vec(ax, Pp, 0.65 * rhat, color=S_COL, label=r'$\vec S$', loff=(0.12, 0.12))
    fs.vec(ax, Pp, 0.6 * thhat, color=E_COL, label=r'$\vec E$', loff=(0.18, -0.02))
    fs.cross_in(ax, Pp + np.array([-0.28, -0.12]), r=0.08, color=B_COL)
    fs.label(ax, Pp + np.array([-0.5, -0.2]), r'$\vec B$', color=B_COL, fontsize=11)
    fs.label(ax, (2.25, -1.45), '복사 세기 $\\propto\\sin^2\\theta$', fontsize=9, color=fs.ORANGE)
    fs.label(ax, (0.12, 1.85), '축 방향: 복사 없음', fontsize=8.5, color=fs.GRAY, ha='left')
    fs.label(ax, (-1.55, -1.05), '축에 수직: 가장 셈', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig31_01')


# ---------- 그림 31.2 +x 방향으로 진행하는 평면파 ----------
def fig02():
    fig, ax = fs.canvas(5.2, 3.0, xlim=(-1.3, 6.6), ylim=(-1.6, 1.75))
    lam = 2.6
    x = np.linspace(0, 5.6, 600)
    Em, Bm = 1.15, 1.15
    s = np.sin(2 * np.pi * x / lam)
    # 축
    for a, b, lab, off in [((0, 0, 0), (6.2, 0, 0), r'$x$', (0.18, 0)),
                           ((0, 0, 0), (0, 1.55, 0), r'$y$', (0, 0.15)),
                           ((0, 0, 0), (0, 0, 2.1), r'$z$', (-0.12, -0.12))]:
        p, q = P(*a), P(*b)
        fs.arrow(ax, p, q, color=fs.GRAY, lw=0.8, ms=8)
        fs.label(ax, (q[0] + off[0], q[1] + off[1]), lab, color=fs.GRAY, fontsize=10)
    # E (y 방향) 곡선과 화살표
    ex, ey = P3(np.c_[x, Em * s, 0 * x])
    ax.plot(ex, ey, color=E_COL, lw=1.4, zorder=4)
    bx, by = P3(np.c_[x, 0 * x, Bm * s])
    ax.plot(bx, by, color=B_COL, lw=1.4, zorder=4)
    for xi in np.arange(0.1625, 5.6, 0.325):
        si = np.sin(2 * np.pi * xi / lam)
        if abs(si) < 0.12:
            continue
        ax.add_patch(FancyArrowPatch(P(xi, 0, 0), P(xi, Em * si, 0), arrowstyle='-|>', mutation_scale=6,
                                     color=E_COL, lw=0.7, shrinkA=0, shrinkB=0, zorder=4))
        ax.add_patch(FancyArrowPatch(P(xi, 0, 0), P(xi, 0, Bm * si), arrowstyle='-|>', mutation_scale=6,
                                     color=B_COL, lw=0.7, shrinkA=0, shrinkB=0, zorder=3))
    # 진행 방향 c
    fs.arrow(ax, P(4.5, 1.25, 0), P(5.9, 1.25, 0), color=fs.BLACK, lw=1.5, label=r'$\vec c$',
             loff=(0.2, 0.12))
    fs.label(ax, P(0.65, Em + 0.25, 0), r'$\vec E$', color=E_COL, fontsize=12)
    fs.label(ax, P(0.65, -0.5, Bm + 0.2), r'$\vec B$', color=B_COL, fontsize=12)
    # 파장 표시
    y0 = -1.45
    xa, xb = lam * 0.75, lam * 1.75   # E의 두 골
    for xx in (xa, xb):
        ax.plot([xx, xx], [-Em - 0.05, y0 + 0.05], color=fs.GRAY, lw=0.5, ls=':')
    ax.add_patch(FancyArrowPatch((xa, y0), (xb, y0), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    fs.label(ax, ((xa + xb) / 2, y0 - 0.0), r'$\lambda$', fontsize=11, color=fs.GRAY, va='bottom')
    fs.save(fig, __file__, 'fig31_02')


# ---------- 그림 31.3 파동 방정식 유도에 쓰는 두 직사각형 경로 ----------
def fig03():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.4, 2.6))
    for ax in axs:
        ax.set_xlim(-0.3, 3.6); ax.set_ylim(-0.6, 2.7); ax.set_aspect('equal'); ax.axis('off')
    # (가) xy 평면, 패러데이
    ax = axs[0]
    x0, x1, y0, y1 = 1.0, 2.0, 0.4, 1.9
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fs.SURF, alpha=0.25, ec='none'))
    # 반시계 방향 경로
    fs.ray(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], color=fs.BLACK, lw=1.0)
    fs.dot_out(ax, (1.5, 1.15), r=0.11, color=B_COL)
    fs.label(ax, (1.5, 1.5), r'$\vec B$', color=B_COL, fontsize=10)
    fs.arrow(ax, (x0 - 0.25, 0.75), (x0 - 0.25, 1.45), color=E_COL, lw=1.4, ms=9)
    fs.label(ax, (x0 - 0.55, 1.1), r'$E(x)$', color=E_COL, fontsize=9, ha='right')
    fs.arrow(ax, (x1 + 0.25, 0.6), (x1 + 0.25, 1.7), color=E_COL, lw=1.4, ms=9)
    fs.label(ax, (x1 + 0.35, 1.15), r'$E(x\!+\!dx)$', color=E_COL, fontsize=9, ha='left')
    fs.dim(ax, (x0, y0), (x1, y0), r'$dx$', off=-0.25, fontsize=9)
    ax.add_patch(FancyArrowPatch((x0 + 0.18, y0), (x0 + 0.18, y1), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (x0 + 0.3, 0.75), r'$h$', fontsize=9, color=fs.GRAY)
    fs.arrow(ax, (0, 0), (0.6, 0), color=fs.GRAY, lw=0.8, ms=7); fs.label(ax, (0.72, 0), r'$x$', fontsize=9, color=fs.GRAY)
    fs.arrow(ax, (0, 0), (0, 0.6), color=fs.GRAY, lw=0.8, ms=7); fs.label(ax, (0, 0.72), r'$y$', fontsize=9, color=fs.GRAY)
    fs.dot_out(ax, (0, 0), r=0.06, color=fs.GRAY); fs.label(ax, (-0.17, -0.17), r'$z$', fontsize=9, color=fs.GRAY)
    ax.set_title('(가) $xy$ 평면: 패러데이 법칙', fontsize=9)
    # (나) xz 평면, 앙페르-맥스웰
    ax = axs[1]
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fs.SURF, alpha=0.25, ec='none'))
    # 법선 +j(지면 안쪽)에 대해 오른손 방향 = 보는 사람에게 시계 방향
    fs.ray(ax, [(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)], color=fs.BLACK, lw=1.0)
    fs.cross_in(ax, (1.5, 1.15), r=0.11, color=E_COL)
    fs.label(ax, (1.5, 1.5), r'$\vec E$', color=E_COL, fontsize=10)
    fs.arrow(ax, (x0 - 0.25, 0.6), (x0 - 0.25, 1.7), color=B_COL, lw=1.4, ms=9)
    fs.label(ax, (x0 - 0.55, 1.15), r'$B(x)$', color=B_COL, fontsize=9, ha='right')
    fs.arrow(ax, (x1 + 0.25, 0.8), (x1 + 0.25, 1.5), color=B_COL, lw=1.4, ms=9)
    fs.label(ax, (x1 + 0.35, 1.15), r'$B(x\!+\!dx)$', color=B_COL, fontsize=9, ha='left')
    fs.dim(ax, (x0, y0), (x1, y0), r'$dx$', off=-0.25, fontsize=9)
    ax.add_patch(FancyArrowPatch((x0 + 0.18, y0), (x0 + 0.18, y1), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (x0 + 0.3, 0.75), r'$h$', fontsize=9, color=fs.GRAY)
    fs.arrow(ax, (0, 0), (0.6, 0), color=fs.GRAY, lw=0.8, ms=7); fs.label(ax, (0.72, 0), r'$x$', fontsize=9, color=fs.GRAY)
    fs.arrow(ax, (0, 0), (0, 0.6), color=fs.GRAY, lw=0.8, ms=7); fs.label(ax, (0, 0.72), r'$z$', fontsize=9, color=fs.GRAY)
    fs.cross_in(ax, (0, 0), r=0.06, color=fs.GRAY); fs.label(ax, (-0.17, -0.17), r'$y$', fontsize=9, color=fs.GRAY)
    ax.set_title('(나) $xz$ 평면: 앙페르–맥스웰 법칙', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig31_03')


# ---------- 그림 31.4 넓이 A를 지나는 에너지 ----------
def fig04():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.4, 5.6), ylim=(-1.75, 1.9))
    w, hh, zz = 1.3, 0.9, 0.9      # 판 두께 c dt, 높이(반), 깊이(반)
    x0 = 1.8
    V = {(i, j, k): P(x0 + i * w, (2 * j - 1) * hh, (2 * k - 1) * zz) for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    # 보이는 면: 위(j=1), 앞(k=1), 오른쪽(i=1)
    faces = [[(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
             [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
             [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]]
    for f in faces:
        ax.add_patch(Polygon([V[v] for v in f], closed=True, fc=fs.SURF, alpha=0.22, ec='none', zorder=1))
    edges = [((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1))]   # 숨은 모서리
    for a, b in edges:
        ax.plot(*zip(V[a], V[b]), color=fs.GRAY, lw=0.8, ls='--', zorder=2)
    vis = [((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((1, 1, 0), (1, 1, 1)), ((0, 1, 1), (1, 1, 1)),
           ((0, 0, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1)), ((1, 0, 1), (1, 1, 1)),
           ((1, 0, 0), (1, 1, 0)), ((1, 0, 0), (1, 0, 1))]
    for a, b in vis:
        ax.plot(*zip(V[a], V[b]), color=fs.BLACK, lw=1.0, zorder=3)
    # 넓이 A (오른쪽 면)
    ax.add_patch(Polygon([V[v] for v in faces[2]], closed=True, fc=fs.ORANGE, alpha=0.25, ec='none', zorder=1))
    c = P(x0 + w, 0.0, 0.0)
    fs.label(ax, (c[0] + 0.25, c[1] + 0.05), r'$A$', fontsize=12)
    # 진행 방향
    for yy in (-0.45, 0.0, 0.45):
        fs.arrow(ax, P(-0.1, yy, 0), P(x0 + w + 1.6, yy, 0), color=S_COL, lw=1.0, ms=9, zorder=4)
    fs.label(ax, P(x0 + w + 1.75, 0.0, 0), r'$\vec S$', color=S_COL, fontsize=12, ha='left')
    a = V[(0, 0, 1)]; b = V[(1, 0, 1)]
    fs.dim(ax, a, b, r'$c\,dt$', off=-0.22)
    fs.label(ax, (-0.3, 1.6), '시간 $dt$ 동안 $A$를 지나는 에너지 $= u\\,(A\\,c\\,dt)$', fontsize=9, ha='left')
    fs.save(fig, __file__, 'fig31_04')


# ---------- 그림 31.5 저항 도선으로 흘러드는 포인팅 벡터 ----------
def fig05():
    fig, ax = fs.canvas(4.8, 3.0, xlim=(-0.7, 6.0), ylim=(-2.25, 1.95))
    r = 0.55
    fs.cylinder(ax, (2.7, 0), r, 5.0, vertical=False, fc=fs.LIGHT, alpha=0.9, ry=0.2)
    fs.arrow(ax, (-0.6, 0), (0.12, 0), color=fs.BLACK, lw=1.4)
    fs.label(ax, (-0.3, 0.24), r'$I$', fontsize=11)
    # S: 옆면으로 안쪽
    for xs in (0.9, 2.1, 3.3, 4.5):
        fs.arrow(ax, (xs, 1.5), (xs, r + 0.03), color=S_COL, lw=1.3, ms=9)
        fs.arrow(ax, (xs, -1.5), (xs, -r - 0.03), color=S_COL, lw=1.3, ms=9)
    fs.label(ax, (0.6, 1.3), r'$\vec S$', color=S_COL, fontsize=11)
    fs.label(ax, (0.6, -1.3), r'$\vec S$', color=S_COL, fontsize=11)
    # E (축 방향)
    fs.arrow(ax, (2.35, r + 0.2), (3.05, r + 0.2), color=E_COL, lw=1.5)
    fs.label(ax, (2.7, r + 0.45), r'$\vec E$', color=E_COL, fontsize=11)
    # B: 위쪽 ⊙, 아래쪽 ⊗ (도선을 감는 방향)
    fs.dot_out(ax, (1.5, r + 0.22), r=0.1, color=B_COL)
    fs.label(ax, (1.5, r + 0.52), r'$\vec B$', color=B_COL, fontsize=11)
    fs.cross_in(ax, (1.5, -r - 0.22), r=0.1, color=B_COL)
    fs.label(ax, (1.5, -r - 0.52), r'$\vec B$', color=B_COL, fontsize=11)
    # 반지름 a, 길이 l
    ax.plot([5.2, 5.2], [0, r], color=fs.GRAY, lw=0.8)
    fs.label(ax, (5.55, 0.28), r'$a$', fontsize=10, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((0.2, -1.85), (5.2, -1.85), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    for xx in (0.2, 5.2):
        ax.plot([xx, xx], [-r - 0.1, -1.95], color=fs.GRAY, lw=0.5)
    fs.label(ax, (2.7, -2.08), r'$\ell$', fontsize=11, color=fs.GRAY)
    fs.save(fig, __file__, 'fig31_05')


# ---------- 그림 31.6 흡수와 반사의 운동량 변화 ----------
def fig06():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.0, 2.0))
    for ax in axs:
        ax.set_xlim(-0.3, 3.4); ax.set_ylim(-0.9, 1.1); ax.set_aspect('equal'); ax.axis('off')
    titles = ['(가) 완전 흡수', '(나) 완전 반사']
    for k, ax in enumerate(axs):
        ax.add_patch(Rectangle((2.3, -0.8), 0.25, 1.7, fc='#444444' if k == 0 else '#d8dde3', ec=fs.BLACK, lw=1))
        fs.wave(ax, 0.0, 1.8, y0=0.5, amp=0.12, wavelength=0.45, color=fs.ORANGE, lw=1.1)
        fs.arrow(ax, (0.2, 0.15), (1.9, 0.15), color=fs.ORANGE, lw=1.4, label=r'$\vec p$', lpos=0.5,
                 loff=(0, -0.22))
        if k == 1:
            fs.arrow(ax, (2.15, -0.4), (0.45, -0.4), color=fs.ORANGE, lw=1.4, ls='--', label=r'$-\vec p$',
                     lpos=0.5, loff=(0, -0.22))
        fs.arrow(ax, (2.55, 0.05), (2.55 + (0.5 if k == 0 else 1.0) * 0.8, 0.05), color=fs.FORCE, lw=1.8,
                 label=r'$\vec F$', loff=(0.0, 0.25))
        ax.set_title(titles[k] + ('  $p_r = I/c$' if k == 0 else '  $p_r = 2I/c$'), fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig31_06')


# ---------- 그림 31.7 선편광과 원편광 ----------
def fig07():
    fig, axs = fs.plt.subplots(1, 2, figsize=(4.8, 2.5))
    for ax in axs:
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal'); ax.axis('off')
        fs.arrow(ax, (-1.4, 0), (1.45, 0), color=fs.GRAY, lw=0.7, ms=7)
        fs.arrow(ax, (0, -1.35), (0, 1.4), color=fs.GRAY, lw=0.7, ms=7)
        fs.label(ax, (1.45, -0.18), r'$x$', fontsize=9, color=fs.GRAY)
        fs.label(ax, (0.17, 1.38), r'$y$', fontsize=9, color=fs.GRAY)
        fs.dot_out(ax, (-1.2, -1.15), r=0.08, color=fs.GRAY)
        fs.label(ax, (-0.85, -1.15), '진행($z$)', fontsize=8, color=fs.GRAY, ha='left')
    # (가) 선편광: 한 직선 위에서 진동
    ax = axs[0]
    ang = np.radians(55)
    u = np.array([np.cos(ang), np.sin(ang)])
    ax.plot([-1.1 * u[0], 1.1 * u[0]], [-1.1 * u[1], 1.1 * u[1]], color=E_COL, lw=0.8, ls=':')
    for s, al in [(1.0, 1.0), (0.6, 0.55), (-0.6, 0.55), (-1.0, 1.0)]:
        fs.vec(ax, (0, 0), (s * u[0], s * u[1]), color=E_COL, lw=1.3, ms=9)
    fs.label(ax, (0.82, 1.1), r'$\vec E$', color=E_COL, fontsize=11)
    ax.set_title('(가) 선편광', fontsize=9)
    # (나) 원편광: z = 0에서 E = E0(cos wt, -sin wt) → 보는 쪽에서 시계 방향 회전
    ax = axs[1]
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=E_COL, lw=0.8, ls=':')
    for k, wt in enumerate(np.radians([0, 45, 90])):
        v = (np.cos(wt), -np.sin(wt))
        fs.vec(ax, (0, 0), v, color=E_COL, lw=1.3 if k == 0 else 0.9, ms=9)
    fs.label(ax, (0.5, 0.17), r'$\omega t=0$', fontsize=8, color=E_COL)
    fs.label(ax, (0.78, -0.88), r'$\pi/4$', fontsize=8, color=E_COL, ha='left')
    fs.label(ax, (0.12, -1.22), r'$\pi/2$', fontsize=8, color=E_COL, ha='left')
    ax.add_patch(FancyArrowPatch((1.15 * np.cos(0.6), 1.15 * np.sin(0.6)),
                                 (1.15 * np.cos(-0.1), 1.15 * np.sin(-0.1)), connectionstyle='arc3,rad=-0.3',
                                 arrowstyle='-|>', mutation_scale=9, color=fs.GRAY, lw=0.9))
    ax.set_title('(나) 원편광 ($z = 0$인 점)', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig31_07')


# ---------- 그림 31.8 편광판과 기울어진 안테나 ----------
def fig08():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.0, 2.6))
    for ax in axs:
        ax.set_xlim(-1.5, 1.6); ax.set_ylim(-1.5, 1.6); ax.set_aspect('equal'); ax.axis('off')
    # (가) 편광판의 투과축과 성분
    ax = axs[0]
    ax.add_patch(Circle((0, 0), 1.35, fc='#eef2f6', ec=fs.GRAY, lw=1.0))
    for xx in np.linspace(-1.1, 1.1, 12):
        hgt = np.sqrt(max(1.35 ** 2 - xx ** 2, 0)) * 0.92
        ax.plot([xx, xx], [-hgt, hgt], color='#c9d2dc', lw=0.6, zorder=1)
    ax.plot([0, 0], [-1.45, 1.45], color=fs.BLACK, lw=0.8, ls='--')
    fs.label(ax, (0.1, -1.48), '투과축', fontsize=8, ha='left')
    th = np.radians(35)
    E = 1.15 * np.array([np.sin(th), np.cos(th)])
    fs.vec(ax, (0, 0), E, color=E_COL, lw=1.6, label=r'$\vec E$', loff=(0.15, 0.08))
    fs.vec(ax, (0, 0), (0, E[1]), color=E_COL, lw=1.3, ls='-', label=r'$E\cos\theta$', loff=(-0.5, -0.1))
    ax.plot([0, E[0]], [E[1], E[1]], color=fs.GRAY, lw=0.7, ls=':')
    fs.vec(ax, (0, 0), (E[0], 0), color=fs.GRAY, lw=1.0, label=r'$E\sin\theta$', loff=(-0.2, -0.22))
    ax.plot([E[0], E[0]], [0, E[1]], color=fs.GRAY, lw=0.7, ls=':')
    fs.angle_arc(ax, (0, 0), 0.45, 90 - 35, 90, r'$\theta$', fontsize=9)
    fs.label(ax, (0.95, -0.75), '흡수', fontsize=8, color=fs.GRAY)
    ax.set_title('(가) 편광판: 투과축 성분만 통과', fontsize=9)
    # (나) 예제 31.6: 연직 편광 전파, 60° 기운 안테나
    ax = axs[1]
    for xx in (-1.3, -0.85):
        fs.arrow(ax, (xx, -0.7), (xx, 0.7), color=E_COL, lw=1.0, style='<|-|>', ms=8)
    fs.label(ax, (-1.075, 0.95), r'$\vec E$', color=E_COL, fontsize=11)
    a = np.radians(60)
    u = np.array([np.sin(a), np.cos(a)])
    c0 = np.array([0.55, -0.1])
    ax.plot([c0[0] - 1.0 * u[0], c0[0] + 1.0 * u[0]], [c0[1] - 1.0 * u[1], c0[1] + 1.0 * u[1]],
            color=fs.BLACK, lw=2.6)
    ax.plot([c0[0], c0[0]], [c0[1], c0[1] + 1.3], color=fs.GRAY, lw=0.7, ls='--')
    fs.angle_arc(ax, c0, 0.55, 90 - 60, 90, '60°', fontsize=9, tr=0.8)
    lo = c0 - 1.0 * u
    fs.label(ax, (1.3, 0.02), '안테나', fontsize=8)
    # 도선 방향 성분 E cos60°
    E0 = 1.0
    fs.vec(ax, c0, (0, -E0), color=E_COL, lw=1.0, ls='--')
    proj = -E0 * np.cos(a) * u
    fs.vec(ax, c0, proj, color=E_COL, lw=1.8, label=r'$E\cos 60^\circ$', loff=(-0.05, -0.42), fontsize=9)
    ax.plot([c0[0], c0[0] + proj[0]], [c0[1] - E0, c0[1] + proj[1]], color=fs.GRAY, lw=0.6, ls=':')
    ax.set_title('(나) 예제 31.6: 기울어진 안테나', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig31_08')


# ---------- 그림 31.9 전자기 스펙트럼 ----------
def fig09():
    import matplotlib.colors as mcolors
    fig, ax = fs.plt.subplots(figsize=(5.5, 2.9))
    ax.set_xlim(4.2, -13.2)   # log10(파장/m): 왼쪽이 긴 파장
    ax.set_ylim(-2.6, 2.6)
    ax.axis('off')
    regions = [  # (이름, log λ 끝(긴 쪽), log λ 끝(짧은 쪽), 색)
        ('라디오파', 4.2, 0.0, '#d9e4f0'),
        ('마이크로파', 0.0, -3.0, '#e3dcef'),
        ('적외선', -3.0, np.log10(700e-9), '#f3d9d4'),
        ('', np.log10(700e-9), np.log10(400e-9), None),
        ('자외선', np.log10(400e-9), -8.0, '#e7dcf3'),
        ('X선', -8.0, -11.0, '#dfe8dc'),
        ('감마선', -11.0, -13.2, '#f2ead0'),
    ]
    y0, y1 = 0.0, 0.8
    for name, a, b, col in regions:
        if col is None:
            # 가시광선: 무지개색
            xs = np.linspace(a, b, 40)
            for x_l, x_r in zip(xs[:-1], xs[1:]):
                lam = 10 ** ((x_l + x_r) / 2) * 1e9
                h = (1 - (lam - 400) / 300) * 0.78
                ax.add_patch(Rectangle((x_l, y0), x_r - x_l, y1 - y0, fc=mcolors.hsv_to_rgb((h, 0.9, 0.95)),
                                       ec='none'))
        else:
            ax.add_patch(Rectangle((a, y0), b - a, y1 - y0, fc=col, ec=fs.GRAY, lw=0.6))
            fs.label(ax, ((a + b) / 2, 0.4), name, fontsize=8)
    # 파장 눈금 (위)
    for e in range(4, -14, -2):
        ax.plot([e, e], [y1, y1 + 0.12], color=fs.BLACK, lw=0.7)
        fs.label(ax, (e, y1 + 0.35), r'$10^{%d}$' % e, fontsize=8)
    fs.label(ax, (4.0, y1 + 0.85), '파장 $\\lambda$ (m)', fontsize=8.5, ha='left')
    # 진동수 눈금 (아래): f = c/λ
    for ef in range(6, 22, 2):
        x = np.log10(2.998e8) - ef
        if 4.2 >= x >= -13.2:
            ax.plot([x, x], [y0, y0 - 0.12], color=fs.BLACK, lw=0.7)
            fs.label(ax, (x, y0 - 0.35), r'$10^{%d}$' % ef, fontsize=8)
    fs.label(ax, (4.0, y0 - 0.8), '진동수 $f$ (Hz)', fontsize=8.5, ha='left')
    # 가시광선 확대
    vx0, vx1 = np.log10(700e-9), np.log10(400e-9)
    xa, xb = -3.2, -10.2
    ya, yb = -2.35, -1.75
    xs = np.linspace(xa, xb, 120)
    for x_l, x_r in zip(xs[:-1], xs[1:]):
        lam = 700 - (0.5 * (x_l + x_r) - xa) / (xb - xa) * 300
        h = (1 - (lam - 400) / 300) * 0.78
        ax.add_patch(Rectangle((x_l, ya), x_r - x_l, yb - ya, fc=mcolors.hsv_to_rgb((h, 0.9, 0.95)), ec='none'))
    ax.plot([vx0, xa], [y0 - 0.5, yb], color=fs.GRAY, lw=0.6)
    ax.plot([vx1, xb], [y0 - 0.5, yb], color=fs.GRAY, lw=0.6)
    ax.plot([vx0, vx0], [y0, y0 - 0.5], color=fs.GRAY, lw=0.6)
    ax.plot([vx1, vx1], [y0, y0 - 0.5], color=fs.GRAY, lw=0.6)
    for lam in (700, 600, 500, 400):
        x = xa + (700 - lam) / 300 * (xb - xa)
        fs.label(ax, (x, ya - 0.2), f'{lam} nm', fontsize=8)
    fs.label(ax, ((xa + xb) / 2, yb + 0.2), '가시광선', fontsize=8)
    # 예제 값 표시
    marks = [(np.log10(3.0), 'FM 방송 3 m', 2.2), (np.log10(0.125), '와이파이 12.5 cm', -2.2),
             (np.log10(0.10e-9), 'X선 0.10 nm', -10.0)]
    for x, s, xt in marks:
        ax.annotate(s, xy=(x, y1), xytext=(xt, y1 + 1.25), ha='center', va='bottom', fontsize=7.5,
                    arrowprops=dict(arrowstyle='-|>', color=fs.FORCE, lw=0.8, mutation_scale=7),
                    color=fs.FORCE)
    fs.save(fig, __file__, 'fig31_09')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09]:
        f()
