"""32장 빛의 성질과 기하광학 그림.

광선은 모두 스넬 법칙·반사 법칙(또는 근축 렌즈·거울 식)으로 실제 계산해 그린다.
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Arc

RAY = fs.ORANGE
GLASS = '#dbe7f3'
WATER = '#d6ecf5'
D = np.radians


# ---------- 광선 계산 도우미 ----------
def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def refract(d, nrm, n1, n2):
    """입사 방향 d, 경계면 법선 nrm(입사 쪽을 향하게), 굴절률 n1→n2. 전반사면 None."""
    d = unit(d); nrm = unit(nrm)
    if np.dot(d, nrm) > 0:
        nrm = -nrm
    cosi = -np.dot(d, nrm); eta = n1 / n2
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return None
    return eta * d + (eta * cosi - np.sqrt(k)) * nrm


def reflect(d, nrm):
    d = unit(d); nrm = unit(nrm)
    return d - 2 * np.dot(d, nrm) * nrm


def hit_circle(p, d, c, R, far=False):
    """p에서 d 방향 직선이 원(c, R)과 만나는 점(양의 t 중 가까운 것 / far=True면 먼 것)."""
    p, d, c = map(lambda v: np.asarray(v, float), (p, d, c))
    d = unit(d); f = p - c
    b = np.dot(f, d); cc = np.dot(f, f) - R ** 2
    disc = b * b - cc
    ts = sorted([-b - np.sqrt(disc), -b + np.sqrt(disc)])
    ts = [t for t in ts if t > 1e-9]
    return p + (ts[-1] if far else ts[0]) * d


def hit_line_x(p, d, x):
    p, d = np.asarray(p, float), np.asarray(d, float)
    return p + (x - p[0]) / d[0] * d


def hit_line_y(p, d, y):
    p, d = np.asarray(p, float), np.asarray(d, float)
    return p + (y - p[1]) / d[1] * d


def normal_line(ax, p, half=1.0, angle=90, color=fs.GRAY):
    a = D(angle)
    u = np.array([np.cos(a), np.sin(a)])
    ax.plot([p[0] - half * u[0], p[0] + half * u[0]], [p[1] - half * u[1], p[1] + half * u[1]],
            color=color, lw=0.8, ls='--', zorder=2)


def obj_arrow(ax, x, h, color=fs.BLACK, ls='-', lw=1.8, label=None, loff=(0, 0)):
    fs.arrow(ax, (x, 0), (x, h), color=color, lw=lw, ls=ls, ms=11, zorder=6)
    if label:
        fs.label(ax, (x + loff[0], h + loff[1]), label, fontsize=10, color=color)


def axis_line(ax, x0, x1):
    ax.plot([x0, x1], [0, 0], color=fs.GRAY, lw=0.7, zorder=1)


def focal_mark(ax, x, text, dy=-0.55, fontsize=10):
    fs.dot(ax, (x, 0), r=0.18 if abs(x) > 3 else 0.05, color=fs.BLACK)
    fs.label(ax, (x, dy), text, fontsize=fontsize)


# ---------- 그림 32.1 반사와 굴절 ----------
def fig01():
    fig, ax = fs.canvas(4.0, 3.0, xlim=(-2.2, 2.2), ylim=(-1.65, 1.65))
    n1, n2 = 1.0, 1.5
    th1 = D(50); th2 = np.arcsin(n1 * np.sin(th1) / n2)
    ax.add_patch(Rectangle((-2.2, -1.65), 4.4, 1.65, fc=GLASS, ec='none', zorder=0))
    ax.plot([-2.2, 2.2], [0, 0], color=fs.BLACK, lw=1.1)
    normal_line(ax, (0, 0), 1.5)
    L = 1.75
    fs.ray(ax, [(-L * np.sin(th1), L * np.cos(th1)), (0, 0)], color=RAY, lw=1.5)
    fs.ray(ax, [(0, 0), (L * np.sin(th1), L * np.cos(th1))], color=RAY, lw=1.1)
    fs.ray(ax, [(0, 0), (L * np.sin(th2), -L * np.cos(th2))], color=RAY, lw=1.5)
    fs.angle_arc(ax, (0, 0), 0.55, 90, 90 + 50, r'$\theta_1$', tr=0.78)
    fs.angle_arc(ax, (0, 0), 0.62, 90 - 50, 90, r"$\theta_1'$", tr=0.85)
    fs.angle_arc(ax, (0, 0), 0.55, -90, -90 + np.degrees(th2), r'$\theta_2$', tr=0.78)
    fs.label(ax, (-1.9, 0.25), r'$n_1$', fontsize=11)
    fs.label(ax, (-1.9, -0.25), r'$n_2$', fontsize=11)
    fs.label(ax, (-1.25, 1.5), '입사 광선', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (1.25, 1.5), '반사 광선', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (1.35, -1.25), '굴절 광선', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (0.08, 1.58), '법선', fontsize=8.5, color=fs.GRAY, ha='left')
    fs.save(fig, __file__, 'fig32_01')


# ---------- 그림 32.2 페르마 원리: 굴절 ----------
def fig02():
    fig, ax = fs.canvas(4.0, 3.2, xlim=(-0.35, 1.45), ylim=(-1.3, 1.3))
    n1, n2 = 1.00, 1.33
    A = np.array([0.0, 1.0]); B = np.array([1.0, -1.0])
    from scipy.optimize import minimize_scalar
    x = minimize_scalar(lambda x: n1 * np.hypot(x, 1) + n2 * np.hypot(1 - x, 1), bounds=(0, 1),
                        method='bounded').x
    ax.add_patch(Rectangle((-0.35, -1.3), 1.8, 1.3, fc=WATER, ec='none', zorder=0))
    ax.plot([-0.35, 1.45], [0, 0], color=fs.BLACK, lw=1.1)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=fs.GRAY, lw=0.8, ls=':')
    fs.ray(ax, [A, (x, 0), B], color=RAY, lw=1.5)
    fs.dot(ax, A, r=0.025); fs.dot(ax, B, r=0.025)
    fs.label(ax, (A[0] - 0.08, A[1] + 0.08), r'$A$', fontsize=11)
    fs.label(ax, (B[0] + 0.08, B[1] - 0.06), r'$B$', fontsize=11)
    normal_line(ax, (x, 0), 0.75)
    th1 = np.degrees(np.arctan2(x, 1)); th2 = np.degrees(np.arctan2(1 - x, 1))
    fs.angle_arc(ax, (x, 0), 0.25, 90, 90 + th1, r'$\theta_1$', tr=0.36, fontsize=9)
    fs.angle_arc(ax, (x, 0), 0.25, -90, -90 + th2, r'$\theta_2$', tr=0.36, fontsize=9)
    # 치수
    ax.plot([0, 0], [0, 1], color=fs.GRAY, lw=0.6)
    fs.label(ax, (-0.08, 0.5), r'$a$', fontsize=10, color=fs.GRAY)
    ax.plot([1, 1], [0, -1], color=fs.GRAY, lw=0.6)
    fs.label(ax, (1.08, -0.5), r'$b$', fontsize=10, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((0, 0.07), (x, 0.07), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (x / 2, 0.16), r'$x$', fontsize=10, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((0, -1.15), (1, -1.15), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (0.5, -1.23), r'$d$', fontsize=10, color=fs.GRAY)
    ax.plot([0, 0], [0, -1.2], color=fs.GRAY, lw=0.4, ls=':')
    fs.label(ax, (1.3, 0.25), '공기 $n_1$', fontsize=8.5)
    fs.label(ax, (-0.12, -0.35), '물 $n_2$', fontsize=8.5)
    fs.save(fig, __file__, 'fig32_02')


# ---------- 그림 32.3 판유리를 지나는 광선의 옆걸음 (예제 32.1) ----------
def fig03():
    fig, ax = fs.canvas(4.0, 3.0, xlim=(-1.6, 2.4), ylim=(-2.4, 1.3))
    n = 1.50; t = 1.0
    th1 = D(45); th2 = np.arcsin(np.sin(th1) / n)
    ax.add_patch(Rectangle((-1.6, -t), 4.0, t, fc=GLASS, ec=fs.BLACK, lw=1.0, zorder=0))
    P0 = np.array([0.0, 0.0])
    P1 = np.array([t * np.tan(th2), -t])
    din = np.array([np.sin(th1), -np.cos(th1)])
    start = P0 - 1.5 * din
    end = P1 + 1.6 * din
    fs.ray(ax, [start, P0, P1, end], color=RAY, lw=1.5)
    # 원래 경로 연장
    q = P0 + 2.6 * din
    ax.plot([P0[0], q[0]], [P0[1], q[1]], color=RAY, lw=0.9, ls='--')
    normal_line(ax, P0, 0.8); normal_line(ax, P1, 0.8)
    fs.angle_arc(ax, P0, 0.45, 90, 135, r'$\theta_1$', tr=0.62, fontsize=9)
    fs.angle_arc(ax, P0, 0.45, -90, -90 + np.degrees(th2), r'$\theta_2$', tr=0.62, fontsize=9)
    fs.angle_arc(ax, P1, 0.45, -90, -45, r'$\theta_3$', tr=0.62, fontsize=9)
    # 옆걸음 d: P1에서 원래 경로까지의 수직 거리
    foot = P0 + np.dot(P1 - P0, din) * din
    ax.plot([P1[0], foot[0]], [P1[1], foot[1]], color=fs.FORCE, lw=1.1)
    m = (P1 + foot) / 2
    fs.label(ax, (m[0] + 0.14, m[1] + 0.1), r'$d$', fontsize=11, color=fs.FORCE)
    # 두께
    ax.add_patch(FancyArrowPatch((-1.25, 0), (-1.25, -t), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    fs.label(ax, (-1.1, -0.5), r'$t$', fontsize=11, color=fs.GRAY)
    fs.label(ax, (1.7, -0.5), r'$n = 1.50$', fontsize=9)
    fs.label(ax, (1.7, 0.5), '공기', fontsize=9)
    fs.save(fig, __file__, 'fig32_03')


# ---------- 그림 32.4 겉보기 깊이 ----------
def fig04():
    fig, ax = fs.canvas(3.6, 3.2, xlim=(-1.7, 1.7), ylim=(-2.35, 1.6))
    n = 1.33; h = 2.0; x = 0.5
    ax.add_patch(Rectangle((-1.7, -2.35), 3.4, 2.35, fc=WATER, ec='none', zorder=0))
    ax.plot([-1.7, 1.7], [0, 0], color=fs.BLACK, lw=1.1)
    coin = np.array([0, -h])
    ax.add_patch(Rectangle((-0.18, -h - 0.06), 0.36, 0.08, fc='#c8a04a', ec=fs.BLACK, lw=0.6, zorder=5))
    for s in (1, -1):
        P = np.array([s * x, 0.0])
        th1 = np.arctan2(x, h); th2 = np.arcsin(n * np.sin(th1))
        dout = np.array([s * np.sin(th2), np.cos(th2)])
        fs.ray(ax, [coin, P, P + 1.45 * dout], color=RAY, lw=1.3)
        img_y = -x / np.tan(th2)
        ax.plot([P[0], 0], [0, img_y], color=RAY, lw=0.8, ls='--')
    th1 = np.degrees(np.arctan2(x, h)); th2 = np.degrees(np.arcsin(n * np.sin(np.radians(th1))))
    normal_line(ax, (x, 0), 0.9)
    fs.angle_arc(ax, (x, 0), 0.5, -90, -90 - th1, r'$\theta_1$', tr=0.68, fontsize=9)
    fs.angle_arc(ax, (x, 0), 0.5, 90, 90 - th2, r'$\theta_2$', tr=0.7, fontsize=9)
    img_y = -x / np.tan(np.radians(th2))
    ax.add_patch(Rectangle((-0.18, img_y - 0.04), 0.36, 0.08, fc='none', ec='#c8a04a', lw=0.9, ls='--', zorder=5))
    fs.label(ax, (-0.55, img_y + 0.12), '상', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (-0.55, -h + 0.1), '동전', fontsize=8.5, color=fs.GRAY)
    # 치수 h, h'
    ax.add_patch(FancyArrowPatch((-1.15, 0), (-1.15, -h), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    fs.label(ax, (-1.3, -h / 2 - 0.3), r'$h$', fontsize=11, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((-0.85, 0), (-0.85, img_y), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    fs.label(ax, (-1.0, img_y / 2), r"$h'$", fontsize=11, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((0, 0.12), (x, 0.12), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (x / 2 - 0.02, 0.27), r'$x$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (1.3, -0.3), r'$n$', fontsize=11)
    fs.save(fig, __file__, 'fig32_04')


# ---------- 그림 32.5 임계각과 전반사 ----------
def fig05():
    fig, ax = fs.canvas(4.6, 2.8, xlim=(-2.6, 2.6), ylim=(-1.75, 1.35))
    n1, n2 = 1.5, 1.0
    thc = np.degrees(np.arcsin(n2 / n1))
    ax.add_patch(Rectangle((-2.6, -1.75), 5.2, 1.75, fc=GLASS, ec='none', zorder=0))
    ax.plot([-2.6, 2.6], [0, 0], color=fs.BLACK, lw=1.1)
    S = np.array([-1.6, -1.55])
    fs.dot(ax, S, r=0.05)
    cases = [(20, 'a'), (thc, 'c'), (60, 'b')]
    for th, kind in cases:
        d = np.array([np.sin(D(th)), np.cos(D(th))])
        P = S + (-S[1] / d[1]) * d
        normal_line(ax, P, 0.45)
        if kind == 'a':
            out = refract(d, (0, 1), n1, n2)
            fs.ray(ax, [S, P, P + 1.2 * out], color=RAY, lw=1.4)
            r = reflect(d, (0, 1))
            fs.ray(ax, [P, P + 0.8 * r], color=RAY, lw=0.6)
            fs.label(ax, (P[0] + 1.2 * out[0] + 0.1, P[1] + 1.2 * out[1] - 0.05), '굴절 + 부분 반사', fontsize=8,
                     ha='left')
        elif kind == 'c':
            fs.ray(ax, [S, P, (2.55, 0.0)], color=fs.FORCE, lw=1.4)
            fs.angle_arc(ax, P, 0.38, -90, -90 - th, r'$\theta_c$', tr=0.55, fontsize=9, color=fs.FORCE)
            fs.label(ax, (2.1, 0.17), r'$90°$로 굴절', fontsize=8, color=fs.FORCE)
        else:
            r = reflect(d, (0, 1))
            Q = hit_line_x(P, r, 2.5)
            fs.ray(ax, [S, P, Q], color=fs.FIELD, lw=1.4)
            fs.label(ax, (Q[0] - 0.05, Q[1] - 0.25), '전반사', fontsize=8.5, color=fs.FIELD, ha='right')
    fs.label(ax, (-2.25, 0.25), r'$n_2$', fontsize=11)
    fs.label(ax, (-2.25, -0.25), r'$n_1 > n_2$', fontsize=10, ha='left')
    fs.save(fig, __file__, 'fig32_05')


# ---------- 그림 32.6 광섬유의 수용각 ----------
def fig06():
    fig, ax = fs.canvas(5.2, 2.5, xlim=(-1.9, 6.0), ylim=(-1.45, 1.45))
    n0, n1 = 1.0, 1.5
    rc, rcl = 0.55, 0.95
    ax.add_patch(Rectangle((0, -rcl), 6.0, 2 * rcl, fc='#eef1f4', ec='none', zorder=0))
    ax.add_patch(Rectangle((0, -rc), 6.0, 2 * rc, fc=GLASS, ec='none', zorder=0))
    for y in (rc, -rc):
        ax.plot([0, 6.0], [y, y], color=fs.BLACK, lw=0.9)
    for y in (rcl, -rcl):
        ax.plot([0, 6.0], [y, y], color=fs.GRAY, lw=0.9)
    ax.plot([0, 0], [-rcl, rcl], color=fs.BLACK, lw=1.0)
    ax.plot([-1.9, 6.0], [0, 0], color=fs.GRAY, lw=0.5, ls='-.')
    th = D(30)
    din = np.array([np.cos(th), -np.sin(th)])
    P0 = np.array([0.0, 0.2])
    start = P0 - 1.85 * din
    d = refract(din, (-1, 0), n0, n1)
    pts = [start, P0]
    p = P0
    for _ in range(6):
        y = -rc if d[1] < 0 else rc
        q = hit_line_y(p, d, y)
        if q[0] > 6.0:
            pts.append(hit_line_x(p, d, 6.0)); break
        pts.append(q); p = q; d = reflect(d, (0, 1))
    fs.ray(ax, pts, color=RAY, lw=1.4)
    thr = np.arcsin(np.sin(th) / n1)
    # 각 표시
    ax.plot([-0.9, 0.9], [0.2, 0.2], color=fs.GRAY, lw=0.7, ls='--')
    fs.angle_arc(ax, P0, 0.6, 180, 180 - 30, r'$\theta$', tr=0.8, fontsize=10)
    fs.angle_arc(ax, P0, 0.7, -np.degrees(thr), 0, r'$\theta_r$', tr=0.92, fontsize=9)
    Q = pts[2]
    normal_line(ax, Q, 0.42)
    fs.angle_arc(ax, Q, 0.32, 90, 90 + 90 - np.degrees(thr), '', fontsize=8)
    fs.label(ax, (Q[0] - 0.62, Q[1] + 0.33), r'$90°-\theta_r$', fontsize=8.5)
    fs.label(ax, (-1.4, 0.75), r'$n_0$', fontsize=11)
    fs.label(ax, (5.55, 0.3), '코어 $n_1$', fontsize=8.5)
    fs.label(ax, (5.3, 0.77), '클래딩 $n_2$', fontsize=8.5, color=fs.GRAY)
    fs.label(ax, (5.3, -0.77), '클래딩 $n_2$', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig32_06')


# ---------- 그림 32.7 프리즘의 편향과 분산 ----------
def prism_tri(A_deg, base=2.6, apex=(0, 1.9)):
    a = D(A_deg) / 2
    H = base / 2 / np.tan(a)
    ap = np.array(apex, float)
    return ap, ap + np.array([-base / 2, -H]), ap + np.array([base / 2, -H])


def trace_prism(ap, bl, br, th1_deg, n, s0=0.55, s_out=1.6):
    """왼쪽 면에 입사각 th1(면의 법선 기준, 아래쪽에서 들어오는 방향)으로 들어오는 광선."""
    t_l = unit(ap - bl); n_l = np.array([-t_l[1], t_l[0]])        # 왼쪽 면 바깥 법선
    t_r = unit(br - ap); n_r = np.array([-t_r[1], t_r[0]])        # 오른쪽 면 바깥 법선
    P = bl + s0 * (ap - bl)
    # 입사 방향: 바깥 법선 -n_l에서 th1만큼 기울어, 꼭짓점 반대(아래)쪽에서 올라옴
    c, s = np.cos(D(th1_deg)), np.sin(D(th1_deg))
    din = -n_l * c - t_l * s * (-1)
    din = unit(c * (-n_l) + s * (-t_l) * -1)
    d2 = refract(din, n_l, 1.0, n)
    # 오른쪽 면과의 교점
    M = np.array([d2, -(br - ap)]).T
    t, u = np.linalg.solve(M, ap - P)
    Q = P + t * d2
    d3 = refract(d2, n_r, n, 1.0)
    return P, Q, din, d2, d3, n_l, n_r


def fig07():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.5, 2.9))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    # (가) 각의 정의
    ax = axs[0]
    ax.set_xlim(-2.6, 2.7); ax.set_ylim(-1.0, 2.3)
    A = 60; n = 1.5
    ap, bl, br = prism_tri(A, base=2.4, apex=(0, 2.0))
    ax.add_patch(Polygon([ap, bl, br], closed=True, fc=GLASS, ec=fs.BLACK, lw=1.1))
    P, Q, din, d2, d3, n_l, n_r = trace_prism(ap, bl, br, 55, n, s0=0.42)
    start = P - 1.5 * din; end = Q + 1.7 * d3
    fs.ray(ax, [start, P, Q, end], color=RAY, lw=1.4)
    # 연장선과 편향각
    ext = P + 2.6 * din
    ax.plot([P[0], ext[0]], [P[1], ext[1]], color=RAY, lw=0.7, ls='--')
    for X, nn in ((P, n_l), (Q, n_r)):
        ax.plot([X[0] - 0.75 * nn[0], X[0] + 0.75 * nn[0]], [X[1] - 0.75 * nn[1], X[1] + 0.75 * nn[1]],
                color=fs.GRAY, lw=0.7, ls='--')
    ang = lambda v: np.degrees(np.arctan2(v[1], v[0]))
    fs.angle_arc(ax, P, 0.42, ang(-din), ang(n_l), r'$\theta_1$', tr=0.6, fontsize=8.5)
    fs.angle_arc(ax, P, 0.42, ang(d2), ang(-n_l), r'$\theta_2$', tr=0.62, fontsize=8.5)
    fs.angle_arc(ax, Q, 0.42, ang(-n_r), ang(-d2), r'$\theta_3$', tr=0.62, fontsize=8.5)
    fs.angle_arc(ax, Q, 0.42, ang(d3), ang(n_r), r'$\theta_4$', tr=0.62, fontsize=8.5)
    # 편향각 delta: 원래 방향 연장선과 나가는 광선 사이
    # 두 직선의 교점
    M = np.array([din, -d3]).T
    t, u = np.linalg.solve(M, Q - P)
    X = P + t * din
    fs.angle_arc(ax, X, 0.55, ang(d3), ang(din), r'$\delta$', tr=0.75, fontsize=10, color=fs.FORCE)
    fs.angle_arc(ax, ap, 0.3, ang(bl - ap), ang(br - ap), r'$A$', tr=0.48, fontsize=9)
    ax.set_title('(가) 각의 정의', fontsize=9)
    # (나) 분산 (굴절률 차이를 과장)
    ax = axs[1]
    ax.set_xlim(-2.2, 3.0); ax.set_ylim(-1.0, 2.3)
    ap, bl, br = prism_tri(60, base=2.4, apex=(0, 2.0))
    ax.add_patch(Polygon([ap, bl, br], closed=True, fc=GLASS, ec=fs.BLACK, lw=1.1))
    cols = [('#d62728', 1.46), ('#ff9f1c', 1.49), ('#2ca02c', 1.52), ('#1f77b4', 1.555), ('#7b3fa0', 1.59)]
    for k, (col, nn) in enumerate(cols):
        P, Q, din, d2, d3, *_ = trace_prism(ap, bl, br, 50, nn, s0=0.42)
        if k == 0:
            fs.ray(ax, [P - 1.5 * din, P], color=fs.BLACK, lw=1.6)
            fs.label(ax, (P[0] - 1.25, P[1] - 0.45), '백색광', fontsize=8.5)
        ax.plot([P[0], Q[0]], [P[1], Q[1]], color=col, lw=0.8)
        end = Q + 1.9 * d3
        ax.plot([Q[0], end[0]], [Q[1], end[1]], color=col, lw=1.3)
        if k in (0, 4):
            fs.label(ax, (end[0] + 0.12, end[1]), '빨강' if k == 0 else '보라', fontsize=8, color=col, ha='left')
    ax.set_title('(나) 분산(굴절률 차이는 과장)', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig32_07')


# ---------- 그림 32.8 물방울 속 광선 (1차 무지개) ----------
def fig08():
    fig, ax = fs.canvas(4.4, 3.1, xlim=(-2.6, 1.9), ylim=(-1.75, 1.45))
    n = 1.333
    thi = np.arccos(np.sqrt((n ** 2 - 1) / 3))
    thr = np.arcsin(np.sin(thi) / n)
    R = 1.0
    ax.add_patch(Circle((0, 0), R, fc=WATER, ec=fs.BLACK, lw=1.1, zorder=0))
    din = np.array([1.0, 0.0])
    P1 = np.array([-np.sqrt(R ** 2 - np.sin(thi) ** 2), np.sin(thi)])
    d2 = refract(din, P1, 1.0, n)
    P2 = hit_circle(P1, d2, (0, 0), R, far=True)
    d3 = reflect(d2, P2)
    P3 = hit_circle(P2, d3, (0, 0), R, far=True)
    d4 = refract(d3, P3, n, 1.0)
    end = P3 + 1.75 * d4
    fs.ray(ax, [P1 - np.array([1.6, 0]), P1, P2, P3, end], color=RAY, lw=1.4)
    # 법선 (중심에서)
    for P in (P1, P2, P3):
        u = unit(P)
        ax.plot([0, P[0] + 0.45 * u[0]], [0, P[1] + 0.45 * u[1]], color=fs.GRAY, lw=0.7, ls='--')
    ang = lambda v: np.degrees(np.arctan2(v[1], v[0]))
    fs.angle_arc(ax, P1, 0.3, ang(-din), ang(P1), r'$\theta_i$', tr=0.46, fontsize=9)
    fs.angle_arc(ax, P1, 0.3, ang(d2), ang(-P1), r'$\theta_r$', tr=0.47, fontsize=9)
    fs.angle_arc(ax, P2, 0.25, ang(-d2), ang(-P2), r'$\theta_r$', tr=0.42, fontsize=8.5)
    fs.angle_arc(ax, P2, 0.25, ang(-P2), ang(d3), r'$\theta_r$', tr=0.42, fontsize=8.5)
    # 나가는 광선과 '태양 반대 방향'(입사 방향을 거꾸로) 사이의 각
    ax.plot([P3[0], P3[0] - 1.9], [P3[1], P3[1]], color=fs.GRAY, lw=0.8, ls=':')
    fs.angle_arc(ax, P3, 1.2, 180, ang(d4) % 360, '42°', tr=1.4, fontsize=9, color=fs.FORCE)
    fs.label(ax, (-2.2, P1[1] + 0.18), '햇빛', fontsize=8.5)
    fs.label(ax, (-1.55, P3[1] + 0.13), '태양 반대 방향', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig32_08')


# ---------- 그림 32.9 무지개 각 곡선 ----------
def fig09():
    fig, ax = fs.plot_axes(4.2, 2.7)
    ti = np.linspace(0, np.pi / 2, 2001)
    for n, col, name in [(1.331, '#d62728', '빨강 $n = 1.331$'), (1.343, '#7b3fa0', '보라 $n = 1.343$')]:
        tr = np.arcsin(np.sin(ti) / n)
        y = 180 - np.degrees(np.pi + 2 * ti - 4 * tr)
        ax.plot(np.degrees(ti), y, color=col, lw=1.4, label=name)
        k = np.argmax(y)
        ax.plot(np.degrees(ti[k]), y[k], 'o', color=col, ms=4)
        ax.annotate(f'{y[k]:.1f}°', (np.degrees(ti[k]), y[k]), xytext=(np.degrees(ti[k]) - 22, y[k] + (2.5 if n < 1.34 else -6)),
                    fontsize=8.5, color=col, arrowprops=dict(arrowstyle='-', color=col, lw=0.6))
    ax.set_xlim(0, 90); ax.set_ylim(0, 48)
    ax.set_xlabel(r'입사각 $\theta_i$ (°)', fontsize=9)
    ax.set_ylabel(r'$180° - D$ (°)', fontsize=9)
    ax.legend(fontsize=8, loc='lower center', frameon=False)
    fs.save(fig, __file__, 'fig32_09')


# ---------- 그림 32.10 평면 거울의 허상 ----------
def fig10():
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-2.6, 2.4), ylim=(-1.35, 1.6))
    ax.plot([0, 0], [-1.2, 1.4], color=fs.BLACK, lw=1.6)
    for y in np.linspace(-1.15, 1.3, 14):
        ax.plot([0, 0.13], [y, y + 0.13], color=fs.BLACK, lw=0.6)
    O = np.array([-1.5, 0.0]); I = np.array([1.5, 0.0])
    fs.dot(ax, O, r=0.05); fs.label(ax, (O[0], O[1] - 0.22), r'$O$', fontsize=11)
    ax.add_patch(Circle(I, 0.05, fc='white', ec=fs.BLACK, lw=1, zorder=6))
    fs.label(ax, (I[0], I[1] - 0.22), r'$I$', fontsize=11)
    for yh in (0.55, 0.9, 1.25):
        P = np.array([0, yh])
        dref = reflect(P - O, (1, 0))
        fs.ray(ax, [O, P, P + 1.5 * unit(dref)], color=RAY, lw=1.2)
        ax.plot([P[0], I[0]], [P[1], I[1]], color=RAY, lw=0.7, ls='--')
    ax.add_patch(FancyArrowPatch((-1.5, -0.75), (0, -0.75), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    ax.add_patch(FancyArrowPatch((0, -0.75), (1.5, -0.75), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    fs.label(ax, (-0.75, -0.95), r'$p$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (0.75, -0.95), r'$|i| = p$', fontsize=10, color=fs.GRAY)
    ax.plot([-2.4, 2.2], [0, 0], color=fs.GRAY, lw=0.5, ls=':')
    fs.label(ax, (1.65, 1.35), '거울 뒤', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig32_10')


# ---------- 그림 32.11 오목 거울의 상 공식 유도 ----------
def fig11():
    fig, ax = fs.canvas(5.0, 2.7, xlim=(-6.6, 0.8), ylim=(-0.6, 3.1))
    r = 4.0; C = np.array([-r, 0.0]); O = np.array([-6.0, 0.0]); h = 1.25
    th = np.linspace(-np.arcsin(2.0 / r), np.arcsin(2.0 / r), 200)
    ax.plot(C[0] + r * np.cos(th), r * np.sin(th), color=fs.BLACK, lw=1.8)
    for t in np.linspace(th[0], th[-1], 18):
        p = C + r * np.array([np.cos(t), np.sin(t)])
        ax.plot([p[0], p[0] + 0.15], [p[1], p[1] + 0.1], color=fs.BLACK, lw=0.5)
    ax.plot([-6.6, 0.6], [0, 0], color=fs.GRAY, lw=0.7)
    P = C + np.array([np.sqrt(r ** 2 - h ** 2), h])
    d = reflect(P - O, P - C)
    I = hit_line_y(P, d, 0.0)
    fs.ray(ax, [O, P, I], color=RAY, lw=1.4)
    ax.plot([C[0], P[0]], [C[1], P[1]], color=fs.GRAY, lw=0.9, ls='--')
    ax.plot([P[0], P[0]], [0, P[1]], color=fs.GRAY, lw=0.6, ls=':')
    for X, s in ((O, r'$O$'), (C, r'$C$'), (I, r'$I$')):
        fs.dot(ax, X, r=0.05); fs.label(ax, (X[0], -0.3), s, fontsize=11)
    fs.label(ax, (0.25, -0.3), r'$V$', fontsize=11)
    fs.label(ax, (P[0] + 0.2, P[1] + 0.2), r'$P$', fontsize=11)
    fs.label(ax, (P[0] + 0.18, h / 2), r'$h$', fontsize=10, color=fs.GRAY)
    ang = lambda v: np.degrees(np.arctan2(v[1], v[0]))
    fs.angle_arc(ax, O, 1.2, 0, ang(P - O), r'$\alpha$', tr=1.45, fontsize=10)
    fs.angle_arc(ax, C, 0.75, 0, ang(P - C), r'$\beta$', tr=0.98, fontsize=10)
    fs.angle_arc(ax, I, 0.5, 0, ang(P - I), r'$\gamma$', tr=0.72, fontsize=10)
    fs.angle_arc(ax, P, 0.7, ang(O - P), ang(C - P), '', fontsize=8)
    fs.angle_arc(ax, P, 0.85, ang(C - P), ang(I - P), '', fontsize=8)
    # 거리 p, r, i (아래쪽)
    for x0, x1, s, yy in ((O[0], 0, r'$p$', 2.75), (C[0], 0, r'$r$', 2.35), (I[0], 0, r'$i$', 1.95)):
        ax.add_patch(FancyArrowPatch((x0, yy), (x1, yy), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
        fs.label(ax, (x0 - 0.2, yy), s, fontsize=10, color=fs.GRAY)
        ax.plot([x0, x0], [0.05, yy + 0.08], color=fs.GRAY, lw=0.4, ls=':')
    fs.save(fig, __file__, 'fig32_11')


# ---------- 거울·렌즈 광선 작도 도우미 (근축: 반사·굴절은 x = 0 평면에서) ----------
def mirror_glyph(ax, ytop, kind='concave', x=0.0, sag=0.5):
    y = np.linspace(-ytop, ytop, 100)
    s = sag * (y / ytop) ** 2
    xs = x - s if kind == 'concave' else x + s
    ax.plot(xs, y, color=fs.BLACK, lw=1.8, zorder=3)
    for yy in np.linspace(-ytop, ytop * 0.92, 16):
        s0 = sag * (yy / ytop) ** 2
        x0 = x - s0 if kind == 'concave' else x + s0
        ax.plot([x0, x0 + 0.5], [yy, yy + 0.5], color=fs.BLACK, lw=0.5, zorder=3)


def seg(ax, p, q, dashed=False, color=RAY, lw=1.2):
    if dashed:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=0.8, ls='--', zorder=3)
    else:
        fs.ray(ax, [p, q], color=color, lw=lw)


def line_at(p, q, x):
    p, q = np.asarray(p, float), np.asarray(q, float)
    return p + (x - p[0]) / (q[0] - p[0]) * (q - p)


# ---------- 그림 32.12 오목 거울의 두 경우 (예제 32.4) ----------
def fig12():
    fig, axs = fs.plt.subplots(2, 1, figsize=(5.0, 3.5))
    f = 10.0; h = 2.0
    for k, (ax, p) in enumerate(zip(axs, (15.0, 5.0))):
        i = 1 / (1 / f - 1 / p); m = -i / p
        ax.set_aspect('equal'); ax.axis('off')
        xl = (-33, 3) if k == 0 else (-24, 13)
        ax.set_xlim(*xl); ax.set_ylim(-4.7, 4.7)
        axis_line(ax, xl[0], xl[1])
        mirror_glyph(ax, 4.5, 'concave', sag=0.5)
        T = np.array([-p, h]); Ip = np.array([-i, m * h])     # 거울 앞이 x < 0
        F = np.array([-f, 0]); Cc = np.array([-2 * f, 0])
        for X, s in ((F, r'$F$'), (Cc, r'$C$')):
            fs.dot(ax, X, r=0.25); fs.label(ax, (X[0], -0.95), s, fontsize=9)
        obj_arrow(ax, -p, h, label='물체', loff=(0, 0.75))
        xend = xl[0] + 0.5
        # 광선 1: 축에 나란히 → F를 지남
        A1 = np.array([0, h])
        seg(ax, T, A1)
        # 광선 2: F를 지나 → 축에 나란히
        A2 = line_at(T, F, 0.0)
        seg(ax, T, A2, color=fs.VEL)
        # 광선 3: 꼭짓점 → 대칭 반사
        A3 = np.array([0.0, 0.0])
        seg(ax, T, A3, color=fs.ACC)
        if i > 0:
            seg(ax, A1, line_at(A1, F, xend))
            seg(ax, A2, np.array([xend, A2[1]]), color=fs.VEL)
            seg(ax, A3, line_at(A3, np.array([-p, -h]), xend), color=fs.ACC)
            obj_arrow(ax, Ip[0], Ip[1], color=fs.FORCE, label='실상', loff=(-2.2, 0.3))
            ax.set_title(r'(가) $p = 15$ cm: $i = +30$ cm, $m = -2.0$', fontsize=9)
        else:
            e1 = line_at(A1, F, xend); seg(ax, A1, e1)
            seg(ax, A1, Ip, dashed=True)
            seg(ax, A2, np.array([xend, A2[1]]), color=fs.VEL); seg(ax, A2, Ip, dashed=True, color=fs.VEL)
            e3 = line_at(A3, np.array([-p, -h]), xend); seg(ax, A3, e3, color=fs.ACC); seg(ax, A3, Ip, dashed=True, color=fs.ACC)
            obj_arrow(ax, Ip[0], Ip[1], color=fs.FORCE, ls='--', label='허상', loff=(1.9, -0.3))
            ax.set_title(r'(나) $p = 5.0$ cm: $i = -10$ cm, $m = +2.0$', fontsize=9)
    fig.tight_layout(h_pad=0.6)
    fs.save(fig, __file__, 'fig32_12')


# ---------- 그림 32.13 볼록 거울 ----------
def fig13():
    fig, ax = fs.canvas(4.6, 2.2, xlim=(-19, 13), ylim=(-2.2, 6.0))
    f = -10.0; p = 15.0; h = 3.0
    i = 1 / (1 / f - 1 / p); m = -i / p      # i = -6, m = 0.4
    axis_line(ax, -19, 13)
    mirror_glyph(ax, 5.2, 'convex', sag=0.45)
    T = np.array([-p, h]); Ip = np.array([-i, m * h])
    F = np.array([-f, 0.0])
    fs.dot(ax, F, r=0.22); fs.label(ax, (F[0], -0.9), r'$F$', fontsize=9)
    obj_arrow(ax, -p, h, label='물체', loff=(0, 0.75))
    xend = -18.5
    A1 = np.array([0, h]); seg(ax, T, A1)
    e1 = line_at(F, A1, xend); seg(ax, A1, e1); seg(ax, A1, F, dashed=True)
    A2 = line_at(T, F, 0.0); seg(ax, T, A2, color=fs.VEL)
    seg(ax, A2, np.array([xend, A2[1]]), color=fs.VEL); seg(ax, A2, np.array([F[0], A2[1]]), dashed=True, color=fs.VEL)
    ax.plot([A2[0], F[0]], [A2[1], 0], color=fs.VEL, lw=0.6, ls=':')
    obj_arrow(ax, Ip[0], Ip[1], color=fs.FORCE, ls='--', lw=1.5)
    fs.label(ax, (Ip[0] + 0.3, Ip[1] + 0.8), '허상', fontsize=8.5, color=fs.FORCE)
    fs.save(fig, __file__, 'fig32_13')


# ---------- 그림 32.14 구면 굴절면 ----------
def fig14():
    fig, ax = fs.canvas(5.0, 2.4, xlim=(-6.5, 9.0), ylim=(-0.75, 2.45))
    n1, n2, r = 1.0, 2.0, 2.4
    C = np.array([r, 0.0]); O = np.array([-6.0, 0.0]); h = 1.1
    t = np.linspace(-0.32, 1.15, 120)
    sx, sy = C[0] - r * np.cos(t), r * np.sin(t)
    ax.add_patch(Polygon(list(zip(sx, sy)) + [(9.0, sy[-1]), (9.0, sy[0])], closed=True, fc=GLASS, ec='none', zorder=0))
    ax.plot(sx, sy, color=fs.BLACK, lw=1.4)
    ax.plot([-6.5, 9.0], [0, 0], color=fs.GRAY, lw=0.7)
    P = C + np.array([-np.sqrt(r ** 2 - h ** 2), h])
    d1 = unit(P - O)
    d2 = refract(d1, P - C, n1, n2)
    I = hit_line_y(P, d2, 0.0)
    fs.ray(ax, [O, P, I], color=RAY, lw=1.4)
    nrm = unit(P - C)
    ax.plot([C[0], P[0] + 1.0 * nrm[0]], [C[1], P[1] + 1.0 * nrm[1]], color=fs.GRAY, lw=0.8, ls='--')
    for X, s_ in ((O, r'$O$'), (C, r'$C$'), (I, r'$I$')):
        fs.dot(ax, X, r=0.06); fs.label(ax, (X[0], -0.35), s_, fontsize=11)
    fs.label(ax, (P[0] - 0.25, P[1] + 0.25), r'$P$', fontsize=11)
    ang = lambda v: np.degrees(np.arctan2(v[1], v[0]))
    fs.angle_arc(ax, O, 2.0, 0, ang(P - O), r'$\alpha$', tr=2.3, fontsize=10)
    fs.angle_arc(ax, C, 0.6, ang(P - C), 180, r'$\beta$', tr=0.85, fontsize=10)
    fs.angle_arc(ax, I, 1.4, ang(P - I), 180, r'$\gamma$', tr=1.65, fontsize=10)
    fs.angle_arc(ax, P, 0.55, ang(-d1), ang(nrm), r'$\theta_1$', tr=0.8, fontsize=9)
    fs.angle_arc(ax, P, 0.65, ang(d2), ang(-nrm), r'$\theta_2$', tr=0.92, fontsize=9)
    fs.label(ax, (-5.8, 1.9), r'$n_1$', fontsize=11)
    fs.label(ax, (8.3, 1.9), r'$n_2$', fontsize=11)
    fs.save(fig, __file__, 'fig32_14')


# ---------- 렌즈 작도 ----------
def thin_lens_rays(ax, T, f, xend, x_lens=0.0, colors=(RAY, fs.VEL, fs.ACC), extend_to=None):
    """T(물체 끝)에서 나온 세 주광선. 반환: 렌즈를 지난 뒤의 (점, 방향) 목록."""
    out = []
    # 1: 축에 나란히 → 뒤쪽 초점
    A1 = np.array([x_lens, T[1]]); d1 = unit(np.array([f, -T[1]]))
    # 2: 앞쪽 초점을 지나 → 나란히
    F = np.array([x_lens - f, 0.0]); A2 = line_at(T, F, x_lens); d2 = np.array([1.0, 0.0])
    # 3: 중심 → 직진
    A3 = np.array([x_lens, 0.0]); d3 = unit(A3 - T)
    for (A, d), c in zip(((A1, d1), (A2, d2), (A3, d3)), colors):
        seg(ax, T, A, color=c)
        seg(ax, A, A + (xend - A[0]) / d[0] * d, color=c)
        out.append((A, d, c))
    return out


def fig15():
    fig, axs = fs.plt.subplots(2, 1, figsize=(5.0, 3.5))
    f = 10.0; h = 2.0
    for k, (ax, p) in enumerate(zip(axs, (15.0, 6.0))):
        i = 1 / (1 / f - 1 / p); m = -i / p
        ax.set_aspect('equal'); ax.axis('off')
        xl = (-18, 33) if k == 0 else (-19, 22)
        H = 4.5 if k == 0 else 5.5
        ax.set_xlim(*xl); ax.set_ylim(-H - 0.3, H + 0.3)
        axis_line(ax, *xl)
        fs.lens(ax, 0.0, h=H, kind='convex', bulge=0.9)
        for X, s in ((-f, r'$F$'), (f, r"$F'$")):
            fs.dot(ax, (X, 0), r=0.25); fs.label(ax, (X, -0.95), s, fontsize=9)
        T = np.array([-p, h])
        obj_arrow(ax, -p, h, label='물체', loff=(0, 0.75))
        rays = thin_lens_rays(ax, T, f, xl[1] - 0.5)
        Ip = np.array([i, m * h])
        if i > 0:
            obj_arrow(ax, Ip[0], Ip[1], color=fs.FORCE, label='실상', loff=(2.2, 0.3))
            ax.set_title(r'(가) $p = 15$ cm, $f = 10$ cm: $i = +30$ cm, $m = -2.0$', fontsize=9)
        else:
            for A, d, c in rays:
                seg(ax, A, Ip, dashed=True, color=c)
            obj_arrow(ax, Ip[0], Ip[1], color=fs.FORCE, ls='--', label='허상', loff=(-2.0, -0.2))
            ax.set_title(r'(나) $p = 6.0$ cm, $f = 10$ cm: $i = -15$ cm, $m = +2.5$', fontsize=9)
    fig.tight_layout(h_pad=0.6)
    fs.save(fig, __file__, 'fig32_15')


# ---------- 그림 32.16 두 렌즈 계 (예제 32.5 나) ----------
def fig16():
    fig, ax = fs.canvas(5.4, 2.3, xlim=(-17, 49), ylim=(-7.4, 3.3))
    f1, f2, L = 10.0, 15.0, 40.0
    p1 = 15.0; h = 1.0
    i1 = 1 / (1 / f1 - 1 / p1); m1 = -i1 / p1
    p2 = L - i1; i2 = 1 / (1 / f2 - 1 / p2); m2 = -i2 / p2
    I1 = np.array([i1, m1 * h]); I2 = np.array([L - i2, m1 * m2 * h])    # i2 < 0: 렌즈 2 앞
    axis_line(ax, -17, 49)
    fs.lens(ax, 0.0, h=3.0, kind='convex', bulge=0.7)
    fs.lens(ax, L, h=5.0, kind='convex', bulge=0.8)
    fs.label(ax, (0, 3.1), '렌즈 1', fontsize=8)
    fs.label(ax, (L + 3.2, 4.4 - 1.6), '렌즈 2', fontsize=8)
    for X, s in ((f1, r"$F_1'$"), (-f1, r'$F_1$'), (L - f2, r'$F_2$'), (L + f2, r"$F_2'$")):
        fs.dot(ax, (X, 0), r=0.3); fs.label(ax, (X, 0.85), s, fontsize=8.5)
    T = np.array([-p1, h])
    obj_arrow(ax, -p1, h, lw=1.6)
    # 두 광선: 축에 나란한 것, 렌즈 1 중심을 지나는 것
    for d0, c in ((np.array([1.0, 0.0]), RAY), (unit(-T), fs.VEL)):
        A = np.array([0.0, T[1] + (0 - T[0]) * d0[1] / d0[0]])
        slope = d0[1] / d0[0] - A[1] / f1
        B = np.array([L, A[1] + L * slope])
        slope2 = slope - B[1] / f2
        E = B + np.array([7.5, 7.5 * slope2])
        fs.ray(ax, [T, A, B, E], color=c, lw=1.1)
        ax.plot([B[0], I2[0]], [B[1], I2[1]], color=c, lw=0.8, ls='--')
    obj_arrow(ax, I1[0], I1[1], color=fs.FORCE, lw=1.6)
    fs.label(ax, (I1[0] + 2.4, I1[1] - 0.3), r'$I_1$', fontsize=10, color=fs.FORCE)
    obj_arrow(ax, I2[0], I2[1], color=fs.FORCE, ls='--', lw=1.6)
    fs.label(ax, (I2[0] - 2.0, I2[1] + 0.3), r'$I_2$', fontsize=10, color=fs.FORCE)
    # 거리
    yy = -7.0
    ax.add_patch(FancyArrowPatch((0, yy), (L, yy), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (L / 2 + 6, yy + 0.0), '40 cm', fontsize=8, color=fs.GRAY, va='bottom')
    for xx in (0, L):
        ax.plot([xx, xx], [yy - 0.3, -3.2 if xx == 0 else -5.2], color=fs.GRAY, lw=0.4, ls=':')
    fs.save(fig, __file__, 'fig32_16')


# ---------- 그림 32.17 굴절 망원경 ----------
def fig17():
    fig, ax = fs.canvas(5.4, 2.4, xlim=(-4.0, 17.0), ylim=(-3.5, 3.0))
    fob, fey = 10.0, 3.0
    xe = fob + fey
    axis_line(ax, -4, 17)
    fs.lens(ax, 0.0, h=2.6, kind='convex', bulge=0.45)
    fs.lens(ax, xe, h=2.6, kind='convex', bulge=0.6)
    fs.label(ax, (0, 2.85), '대물렌즈', fontsize=8)
    fs.label(ax, (xe, 2.85), '접안렌즈', fontsize=8)
    th_ob = D(9)
    hp = -fob * np.tan(th_ob)        # 중간 상의 높이 (도립)
    ys = (1.2, 0.0, -1.2)
    for y0 in ys:
        A = np.array([0.0, y0])
        T0 = A + np.array([-3.6, 3.6 * np.tan(th_ob)])
        # 대물렌즈 뒤: 초점면의 점 (fob, hp)를 지남
        Bdir = unit(np.array([fob, hp]) - A)
        B = A + (xe - A[0]) / Bdir[0] * Bdir
        slope = Bdir[1] / Bdir[0] - B[1] / fey
        E = B + np.array([3.4, 3.4 * slope])
        fs.ray(ax, [T0, A, B, E], color=RAY, lw=1.0)
    obj_arrow(ax, fob, hp, color=fs.FORCE, lw=1.5)
    fs.label(ax, (fob - 0.7, hp / 2), r"$h'$", fontsize=10, color=fs.FORCE)
    ax.plot([fob, fob], [-3.0, 2.2], color=fs.GRAY, lw=0.5, ls=':')
    fs.angle_arc(ax, (0, 0), 2.2, 180 - 9, 180, r'$\theta_{\mathrm{ob}}$', tr=2.75, fontsize=9)
    ang_ey = np.degrees(np.arctan(-hp / fey))
    fs.angle_arc(ax, (xe, 0), 1.6, 0, ang_ey, r'$\theta_{\mathrm{ey}}$', tr=2.1, fontsize=9)
    yy = -3.1
    ax.add_patch(FancyArrowPatch((0, yy), (fob, yy), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    ax.add_patch(FancyArrowPatch((fob, yy), (xe, yy), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (fob / 2, yy - 0.35), r'$f_{\mathrm{ob}}$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (fob + fey / 2, yy - 0.35), r'$f_{\mathrm{ey}}$', fontsize=10, color=fs.GRAY)
    fs.save(fig, __file__, 'fig32_17')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14,
              fig15, fig16, fig17]:
        f()
