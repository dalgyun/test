"""27장 전류가 만드는 자기장 — 그림 생성 스크립트.
python3 figures/ch27/make_figs.py  (FIG_PREVIEW=<폴더> 를 주면 PNG 미리보기도 저장)
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon, Arc, Ellipse, Wedge
from scipy.special import ellipk, ellipe

MU0 = 4e-7 * np.pi
F = fs.FIELD


# ---------- 이 장 전용 도우미 ----------
def head(ax, pts, frac=0.5, color=F, ms=10, reverse=False, zorder=4):
    """폴리라인 pts 위 frac 지점에 진행 방향 화살촉."""
    pts = np.asarray(pts, float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = frac * s[-1]
    i = int(np.clip(np.searchsorted(s, t), 1, len(pts) - 1))
    a, b = pts[i - 1], pts[i]
    w = (t - s[i - 1]) / (seg[i - 1] + 1e-12)
    m = a + (b - a) * w
    d = (b - a) / (np.hypot(*(b - a)) + 1e-12)
    if reverse:
        d = -d
    ax.add_patch(FancyArrowPatch(m - d * 0.02, m + d * 0.02, arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=zorder))


def circ_arrow(ax, c, r, th0, th1, color=F, lw=1.0, ms=10, arrow_at=None, ls='-', zorder=3):
    """중심 c, 반지름 r인 원호(도, th0→th1 방향). arrow_at 위치(도)들에 화살촉."""
    th = np.radians(np.linspace(th0, th1, 200))
    x = c[0] + r * np.cos(th); y = c[1] + r * np.sin(th)
    ax.plot(x, y, color=color, lw=lw, ls=ls, zorder=zorder)
    sgn = 1 if th1 > th0 else -1
    for a in (arrow_at or []):
        a = np.radians(a)
        p = np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a)])
        d = sgn * np.array([-np.sin(a), np.cos(a)])
        ax.add_patch(FancyArrowPatch(p - d * 0.01, p + d * 0.01, arrowstyle='-|>', mutation_scale=ms,
                                     color=color, lw=0, zorder=zorder + 1))


def loop_B(z, rho, a=1.0, z0=0.0):
    """반지름 a, 위치 z0인 원형 고리(전류 +, 축 +z 방향 쌍극자)의 (B_z, B_rho), mu0 I/(2 pi) = 1 단위."""
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
    """자기장선 추적: start에서 출발해 상자를 벗어나거나 출발점으로 돌아오면 멈춘다(양방향)."""
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


def wire_dot(ax, p, r=0.12, color=fs.BLACK):
    fs.dot_out(ax, p, r=r, color=color)


def wire_cross(ax, p, r=0.12, color=fs.BLACK):
    fs.cross_in(ax, p, r=r, color=color)


# ---------- 그림 27.1 비오–사바르 법칙의 기하 ----------
def fig01():
    fig, ax = fs.canvas(4.0, 2.9, xlim=(-1.0, 4.2), ylim=(-0.5, 3.4))
    t = np.linspace(-0.4, 3.3, 200)
    xw = 0.25 * np.sin(1.1 * t) - 0.2
    ax.plot(xw, t, color=fs.BLACK, lw=2.2, zorder=2)
    ax.text(-0.75, 2.9, r'$I$', fontsize=12)
    fs.arrow(ax, (-0.55, 2.5), (-0.55, 3.1), color=fs.BLACK, lw=1.2)
    # 전류 조각
    s0 = 1.15
    S = np.array([0.25 * np.sin(1.1 * s0) - 0.2, s0])
    tang = np.array([0.25 * 1.1 * np.cos(1.1 * s0), 1.0]); tang /= np.hypot(*tang)
    fs.arrow(ax, S - tang * 0.05, S + tang * 0.55, color=fs.FORCE, lw=2.4, ms=13)
    ax.text(S[0] - 0.75, S[1] + 0.35, r'$I\,d\vec{\ell}$', fontsize=12, color=fs.FORCE)
    P = np.array([3.3, 2.3])
    fs.arrow(ax, S, P, color=fs.BLACK, lw=1.3)
    ax.text(1.75, 1.95, r'$\vec{r}$', fontsize=12)
    u = (P - S) / np.hypot(*(P - S))
    fs.arrow(ax, S, S + u * 0.55, color=fs.VEL, lw=2.0, ms=11)
    ax.text(S[0] + 0.55, S[1] - 0.12, r'$\hat{r}$', fontsize=12, color=fs.VEL)
    # 각
    a1 = np.degrees(np.arctan2(tang[1], tang[0])); a2 = np.degrees(np.arctan2(u[1], u[0]))
    fs.angle_arc(ax, S, 0.32, a2, a1, r'$\theta$', fontsize=11, tr=0.45)
    fs.dot(ax, P, r=0.05)
    ax.text(P[0] + 0.05, P[1] + 0.22, r'$P$', fontsize=12)
    fs.cross_in(ax, (P[0] + 0.0, P[1] - 0.55), r=0.13, color=F)
    ax.text(P[0] + 0.22, P[1] - 0.55, r'$d\vec{B}$', fontsize=12, color=F, va='center')
    ax.text(P[0] - 0.45, P[1] - 1.05, '(지면으로 들어감)', fontsize=8.5, color=F)
    fs.save(fig, __file__, 'fig27_01')


# ---------- 그림 27.2 직선 도선의 자기장선 ----------
def fig02():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.8), gridspec_kw={'width_ratios': [1, 1.05]})
    ax = axs[0]; ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.9); ax.set_aspect('equal'); ax.axis('off')
    for y0, r in [(-1.0, 1.25), (0.0, 1.0), (1.0, 0.7)]:
        ry = r * 0.3
        th = np.linspace(0, np.pi, 100)
        ax.plot(r * np.cos(th), y0 + ry * np.sin(th), color=F, lw=1.0, zorder=1)
        th = np.linspace(np.pi, 2 * np.pi, 100)
        ax.plot(r * np.cos(th), y0 + ry * np.sin(th), color=F, lw=1.0, zorder=3)
        # 앞쪽(아래 절반)에서 오른쪽으로 → 위에서 보면 반시계
        for th0, z_ in [(-0.6, 4), (0.6, 1)]:   # 앞쪽(아래, 오른쪽으로)과 뒤쪽(위, 왼쪽으로)
            t0 = np.pi + th0 if z_ == 4 else th0
            t0 = 1.5 * np.pi + 0.5 if z_ == 4 else 0.5 * np.pi + 0.5
            p = np.array([r * np.cos(t0), y0 + ry * np.sin(t0)])
            dd = np.array([-r * np.sin(t0), ry * np.cos(t0)]); dd /= np.hypot(*dd)
            ax.add_patch(FancyArrowPatch(p - dd * 0.02, p + dd * 0.02, arrowstyle='-|>', mutation_scale=10,
                                         color=F, lw=0, zorder=z_))
    ax.plot([0, 0], [-1.6, 1.85], color=fs.BLACK, lw=2.4, zorder=2)
    fs.arrow(ax, (0.22, 1.25), (0.22, 1.8), color=fs.BLACK, lw=1.3)
    ax.text(0.35, 1.55, r'$I$', fontsize=12)
    ax.text(0.95, -0.15, r'$\vec{B}$', fontsize=12, color=F)
    ax.text(0, -1.95, '(가) 도선을 감는 자기장선', ha='center', fontsize=9)
    ax = axs[1]; ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_aspect('equal'); ax.axis('off')
    for r in [0.45, 0.85, 1.4]:
        circ_arrow(ax, (0, 0), r, 0, 360, arrow_at=[45, 225])
    wire_dot(ax, (0, 0), r=0.13)
    ax.text(0.16, -0.25, r'$I$', fontsize=11)
    a = np.radians(110); p = 0.85 * np.array([np.cos(a), np.sin(a)])
    fs.arrow(ax, (0, 0), p, color=fs.BLACK, lw=0.9, ms=8)
    ax.text(-0.12, 0.42, r'$r$', fontsize=11)
    tdir = np.array([-np.sin(a), np.cos(a)])
    fs.arrow(ax, p, p + tdir * 0.6, color=F, lw=2.0)
    ax.text(p[0] - 0.75, p[1] - 0.05, r'$\vec{B}$', fontsize=12, color=F)
    ax.text(0, -1.95, '(나) 위에서 본 모습: 전류가 나오는 방향(⊙)', ha='center', fontsize=9)
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, __file__, 'fig27_02')


# ---------- 그림 27.3 유한한 직선 도선 ----------
def fig03():
    fig, ax = fs.canvas(3.8, 3.4, xlim=(-1.1, 3.6), ylim=(-1.7, 2.75))
    z1, z2, d = -1.2, 2.3, 2.9
    ax.plot([0, 0], [z1, z2], color=fs.BLACK, lw=2.4, zorder=2)
    ax.plot([0, 0], [z2, 2.7], color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([0, 0], [-1.6, z1], color=fs.GRAY, lw=0.8, ls=':')
    fs.arrow(ax, (-0.55, -0.9), (-0.55, -0.2), color=fs.BLACK, lw=1.2)
    ax.text(-0.75, -0.55, r'$I$', fontsize=12, ha='right', va='center')
    ax.text(-0.12, 2.6, r'$z$', fontsize=11, ha='right')
    P = np.array([d, 0.0])
    ax.plot([0, d], [0, 0], color=fs.GRAY, lw=0.9, ls='--')
    ax.text(0.75, 0.05, r'$d$', fontsize=11, color=fs.GRAY, va='bottom')
    ax.text(-0.1, -0.05, r'$O$', fontsize=10, ha='right', va='top')
    zc = 1.15
    ax.plot([0, 0], [zc - 0.13, zc + 0.13], color=fs.FORCE, lw=4.5, solid_capstyle='butt', zorder=3)
    ax.text(-0.15, zc, r'$dz$', fontsize=10, color=fs.FORCE, ha='right', va='center')
    ax.annotate('', xy=(0.12, zc), xytext=(0.12, 0), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.7))
    ax.text(0.2, 0.55, r'$z$', fontsize=10, color=fs.GRAY)
    fs.arrow(ax, (0, zc), P, color=fs.BLACK, lw=1.1)
    ax.text(0.9, 0.95, r'$\vec{r}$', fontsize=11)
    for zz in (z1, z2):
        ax.plot([0, d], [zz, 0], color=fs.GRAY, lw=0.8, ls=':')
    fs.dot(ax, P)
    ax.text(d + 0.12, 0.12, r'$P$', fontsize=12)
    def ang(z): return np.degrees(np.arctan2(z, -d))      # P에서 본 방향(도)
    def lab(r, a, s):
        t = np.radians(a); ax.text(P[0] + r * np.cos(t), P[1] + r * np.sin(t), s, fontsize=10, ha='center', va='center')
    fs.angle_arc(ax, P, 0.6, ang(zc), 180, None)
    lab(0.78, (ang(zc) + 180) / 2, r'$\theta$')
    fs.angle_arc(ax, P, 1.35, ang(z2), 180, None)
    lab(1.55, (ang(z2) + 180) / 2 + 3, r'$\theta_2$')
    a1 = ang(z1) + 360
    fs.angle_arc(ax, P, 1.05, 180, a1, None)
    lab(1.25, (180 + a1) / 2, r'$\theta_1$')
    fs.cross_in(ax, (P[0], -0.6), r=0.12, color=F)
    ax.text(P[0] + 0.2, -0.6, r'$\vec{B}$', fontsize=12, color=F, va='center')
    ax.text(0.15, z2, r'$z_2$', fontsize=10, va='center')
    ax.text(0.15, z1, r'$z_1$', fontsize=10, va='center')
    fs.save(fig, __file__, 'fig27_03')


# ---------- 그림 27.4 정사각형 고리 (예제 27.1) ----------
def fig04():
    fig, ax = fs.canvas(2.9, 2.7, xlim=(-1.45, 1.75), ylim=(-1.35, 1.45))
    h = 1.0
    sq = np.array([[-h, -h], [h, -h], [h, h], [-h, h], [-h, -h]])
    ax.plot(sq[:, 0], sq[:, 1], color=fs.BLACK, lw=2.2, zorder=2)
    for a, b in zip(sq[:-1], sq[1:]):
        m = (a + b) / 2; dd = (b - a) / 2
        ax.add_patch(FancyArrowPatch(m - dd * 0.05, m + dd * 0.05, arrowstyle='-|>', mutation_scale=12,
                                     color=fs.BLACK, lw=0, zorder=3))
    ax.text(h + 0.1, 0.55, r'$I$', fontsize=11)
    ax.add_patch(Circle((0, 0), h, fc='none', ec=fs.GRAY, lw=0.8, ls='--'))
    ax.plot([0, 0], [0, h], color=fs.GRAY, lw=0.9)
    ax.text(-0.06, 0.55, r'$a/2$', fontsize=9, ha='right', color=fs.GRAY)
    ax.plot([0, h], [0, h], color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([0, h], [0, -h], color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([0, h], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, (0, 0), 0.38, 0, 45, '45°', fontsize=8.5, tr=0.62)
    fs.angle_arc(ax, (0, 0), 0.38, -45, 0, '45°', fontsize=8.5, tr=0.62)
    fs.dot_out(ax, (0, 0), r=0.1, color=F)
    ax.text(-0.18, -0.2, r'$\vec{B}$', fontsize=11, color=F, ha='right')
    fs.dim(ax, (-h, -h), (h, -h), r'$a$', off=-0.2)
    fs.save(fig, __file__, 'fig27_04')


# ---------- 그림 27.5 머리핀 도선 (예제 27.2) ----------
def fig05():
    fig, ax = fs.canvas(3.8, 1.9, xlim=(-1.4, 4.4), ylim=(-1.35, 1.35))
    R = 0.9
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.BLACK, lw=2.2)
    ax.plot([0, 3.8], [R, R], color=fs.BLACK, lw=2.2)
    ax.plot([0, 3.8], [-R, -R], color=fs.BLACK, lw=2.2)
    for y in (R, -R):
        ax.plot([3.8, 4.3], [y, y], color=fs.BLACK, lw=2.2, ls=(0, (1, 1.5)))
    head(ax, [(2.4, R), (1.6, R)], color=fs.BLACK, ms=13)
    head(ax, [(1.6, -R), (2.4, -R)], color=fs.BLACK, ms=13)
    head(ax, [(R * np.cos(np.radians(178)), R * np.sin(np.radians(178))),
              (R * np.cos(np.radians(182)), R * np.sin(np.radians(182)))], color=fs.BLACK, ms=13)
    ax.text(2.0, R + 0.2, r'$I$', fontsize=11, ha='center')
    ax.text(2.0, -R - 0.3, r'$I$', fontsize=11, ha='center')
    fs.dot_out(ax, (0, 0), r=0.1, color=F)
    ax.text(0.15, 0.18, r'$C$', fontsize=11)
    ax.text(0.2, -0.22, r'$\vec{B}$', fontsize=10, color=F)
    a = np.radians(135)
    fs.arrow(ax, (0, 0), (R * np.cos(a), R * np.sin(a)), color=fs.GRAY, lw=0.8, ms=8)
    ax.text(-0.5, 0.15, r'$R$', fontsize=10, color=fs.GRAY)
    fs.save(fig, __file__, 'fig27_05')


# ---------- 그림 27.6 원형 고리의 축 위 ----------
def fig06():
    fig, ax = fs.canvas(4.2, 3.0, xlim=(-1.0, 4.4), ylim=(-1.75, 2.15))
    R, z = 1.3, 2.4
    ax.add_patch(Ellipse((0, 0), 0.55, 2 * R, fc='none', ec=fs.GRAY, lw=1.0, ls='--'))
    ax.plot([-0.9, 4.3], [0, 0], color=fs.GRAY, lw=0.8)
    ax.text(4.3, 0.12, r'$z$', fontsize=11, ha='right')
    wire_dot(ax, (0, R), r=0.12)
    wire_cross(ax, (0, -R), r=0.12)
    ax.text(-0.25, R + 0.2, r'$d\vec{\ell}$', fontsize=11, ha='right')
    ax.text(-0.18, -R - 0.12, r'$I$', fontsize=11, ha='right', va='top')
    fs.arrow(ax, (0, 0), (0, R - 0.14), color=fs.GRAY, lw=0.8, ms=8)
    ax.text(0.08, 0.55, r'$R$', fontsize=10, color=fs.GRAY, ha='left')
    P = np.array([z, 0.0])
    fs.arrow(ax, (0, R), P, color=fs.BLACK, lw=1.1)
    ax.text(1.25, 0.82, r'$\vec{r}$', fontsize=11)
    ax.plot([0, z], [-R, 0], color=fs.GRAY, lw=0.7, ls=':')
    fs.dot(ax, P)
    ax.text(z - 0.08, -0.28, r'$P$', fontsize=11, ha='right')
    ax.text(z / 2, -0.25, r'$z$', fontsize=10, color=fs.GRAY)
    rv = P - np.array([0, R]); rv /= np.hypot(*rv)
    dB = np.array([-rv[1], rv[0]])  # r에 수직, 위쪽 성분 양
    if dB[0] < 0: dB = -dB
    Lb = 1.25
    q = P + dB * Lb
    fs.arrow(ax, P, q, color=F, lw=2.0)
    ax.text(q[0] + 0.05, q[1] + 0.12, r'$d\vec{B}$', fontsize=11, color=F)
    fs.arrow(ax, P, (q[0], 0), color=F, lw=1.4, ls='--', ms=10)
    ax.text(q[0] + 0.05, -0.25, r'$dB_z$', fontsize=10, color=F)
    fs.arrow(ax, P, (P[0], q[1]), color=F, lw=1.0, ls='--', ms=9)
    ax.text(P[0] - 0.1, q[1], r'$dB_\perp$', fontsize=10, color=F, ha='right')
    ax.plot([q[0], q[0]], [0, q[1]], color=F, lw=0.5, ls=':')
    ax.plot([P[0], q[0]], [q[1], q[1]], color=F, lw=0.5, ls=':')
    fs.angle_arc(ax, P, 0.45, 0, np.degrees(np.arctan2(dB[1], dB[0])), r'$\alpha$', fontsize=10, tr=0.6)
    # 반대편 조각의 기여
    q2 = P + np.array([dB[0], -dB[1]]) * Lb
    fs.arrow(ax, P, q2, color=F, lw=1.0, ls=':', ms=9)
    ax.text(q2[0] + 0.05, q2[1] - 0.1, '반대편 조각의 $d\\vec{B}$', fontsize=8.5, color=F, va='top')
    # 직각 표시
    c = P - rv * 0.18
    ax.plot([c[0], c[0] + dB[0] * 0.18, P[0] + dB[0] * 0.18], [c[1], c[1] + dB[1] * 0.18, P[1] + dB[1] * 0.18],
            color=fs.GRAY, lw=0.6)
    fs.save(fig, __file__, 'fig27_06')


# ---------- 그림 27.7 코일 축 위 자기장 (예제 27.3) ----------
def fig07():
    N, R, I = 50, 0.10, 2.0
    z = np.logspace(np.log10(0.03), np.log10(2.0), 300)
    B = N * MU0 * I * R ** 2 / (2 * (R ** 2 + z ** 2) ** 1.5)
    Ba = N * MU0 * I * R ** 2 / (2 * z ** 3)
    fig, ax = fs.plot_axes(4.2, 2.9)
    ax.loglog(z, B, color=fs.VEL, lw=1.8, label=r'정확한 값 $\dfrac{N\mu_0IR^2}{2(R^2+z^2)^{3/2}}$')
    ax.loglog(z, Ba, color=fs.FORCE, lw=1.2, ls='--', label=r'쌍극자 근사 $\dfrac{N\mu_0IR^2}{2z^3}$')
    ax.axhline(N * MU0 * I / (2 * R), color=fs.GRAY, lw=0.8, ls=':')
    ax.text(0.032, 7.2e-4, r'중심값 $6.3\times10^{-4}$ T', fontsize=8.5, color=fs.GRAY, va='bottom')
    for zz, lab in [(0.2, '(나)'), (1.0, '(다)')]:
        b = N * MU0 * I * R ** 2 / (2 * (R ** 2 + zz ** 2) ** 1.5)
        ax.plot(zz, b, 'o', color=fs.VEL, ms=4)
        ax.text(zz * 1.12, b * 1.25, lab, fontsize=9)
    ax.set_xlabel(r'축 위 거리 $z$ (m)')
    ax.set_ylabel(r'$B$ (T)')
    ax.set_ylim(1e-7, 3e-3)
    ax.legend(fontsize=8.5, loc='lower left', frameon=False)
    fs.save(fig, __file__, 'fig27_07')


# ---------- 그림 27.8 평행 도선 사이의 힘 ----------
def fig08():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    for ax, same, title in [(axs[0], True, '(가) 같은 방향 전류: 인력'), (axs[1], False, '(나) 반대 방향 전류: 척력')]:
        ax.set_xlim(-1.2, 3.2); ax.set_ylim(-1.45, 1.45); ax.set_aspect('equal'); ax.axis('off')
        d = 2.0
        circ_arrow(ax, (0, 0), d, -38, 38, arrow_at=[20], lw=0.9)
        circ_arrow(ax, (0, 0), 0.9, 0, 360, arrow_at=[90, 270], lw=0.9)
        wire_dot(ax, (0, 0))
        (wire_dot if same else wire_cross)(ax, (d, 0))
        ax.text(-0.3, -0.35, r'$I_1$', fontsize=11, ha='center')
        ax.text(d + 0.32, -0.38, r'$I_2$', fontsize=11, ha='center')
        fs.arrow(ax, (d, 0.18), (d, 1.0), color=F, lw=1.6)
        ax.text(d + 0.12, 0.85, r'$\vec{B}_1$', fontsize=11, color=F)
        sgn = -1 if same else 1
        fs.arrow(ax, (d + sgn * 0.17, 0), (d + sgn * 0.85, 0), color=fs.FORCE, lw=2.0)
        fs.arrow(ax, (-sgn * 0.17, 0), (-sgn * 0.85, 0), color=fs.FORCE, lw=2.0)
        if same:
            ax.text(d - 0.6, 0.15, r'$\vec{F}_{21}$', fontsize=10, color=fs.FORCE, ha='center')
            ax.text(0.6, 0.15, r'$\vec{F}_{12}$', fontsize=10, color=fs.FORCE, ha='center')
        else:
            ax.text(d + 0.6, 0.15, r'$\vec{F}_{21}$', fontsize=10, color=fs.FORCE, ha='center')
            ax.text(-0.6, 0.15, r'$\vec{F}_{12}$', fontsize=10, color=fs.FORCE, ha='center')
        ax.annotate('', xy=(d, -1.0), xytext=(0, -1.0), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
        ax.text(d / 2, -0.9, r'$d$', fontsize=10, color=fs.GRAY, ha='center', va='bottom')
        ax.text(1.0, -1.42, title, fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.08)
    fs.save(fig, __file__, 'fig27_08')


# ---------- 그림 27.9 앙페르 법칙: 임의의 경로 ----------
def fig09():
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.9), gridspec_kw={'width_ratios': [1.15, 1]})
    ph = np.linspace(0, 2 * np.pi, 400)
    # (가) 도선을 감는 경로
    ax = axs[0]; ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.9, 2.0); ax.set_aspect('equal'); ax.axis('off')
    rc = lambda p: 1.35 + 0.3 * np.cos(2 * p) + 0.15 * np.sin(3 * p)
    x = rc(ph) * np.cos(ph); y = rc(ph) * np.sin(ph)
    ax.plot(x, y, color=fs.BLACK, lw=1.4)
    for f in (0.45, 0.85):
        head(ax, np.column_stack([x, y]), f, color=fs.BLACK, ms=11)
    wire_dot(ax, (0, 0))
    ax.text(0.15, -0.3, r'$I$', fontsize=11)
    p0, dp = np.radians(52), np.radians(30)
    Q = rc(p0) * np.array([np.cos(p0), np.sin(p0)])
    Q2 = rc(p0 + dp) * np.array([np.cos(p0 + dp), np.sin(p0 + dp)])
    ax.plot([0, Q[0]], [0, Q[1]], color=fs.GRAY, lw=0.8)
    ax.plot([0, Q2[0] * 1.1], [0, Q2[1] * 1.1], color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, (0, 0), 0.3, np.degrees(p0), np.degrees(p0 + dp), None, color=fs.GRAY)
    ax.text(0.48 * np.cos(p0 + dp / 2), 0.48 * np.sin(p0 + dp / 2), r'$d\varphi$', fontsize=8.5, color=fs.GRAY, ha='center', va='center')
    ax.text(0.75 * np.cos(p0) + 0.12, 0.75 * np.sin(p0) - 0.05, r'$r$', fontsize=10, color=fs.GRAY, va='top')
    fs.arrow(ax, Q, Q2, color=fs.BLACK, lw=1.8, ms=10)
    mq = (Q + Q2) / 2
    ax.text(mq[0] - 0.02, mq[1] - 0.22, r'$d\vec{\ell}$', fontsize=10, ha='center', va='center')
    tdir = np.array([-np.sin(p0), np.cos(p0)])
    fs.arrow(ax, Q, Q + tdir * 0.75, color=F, lw=1.8)
    ax.text(Q[0] + tdir[0] * 0.75 + 0.12, Q[1] + tdir[1] * 0.75, r'$\vec{B}$', fontsize=11, color=F)
    ax.text(-1.65, -1.55, r'$C$', fontsize=11)
    fig.text(0.28, 0.03, r'(가) 도선을 감는 경로: $\oint d\varphi = 2\pi$', fontsize=9, ha='center')
    # (나) 도선을 감지 않는 경로
    ax = axs[1]; ax.set_xlim(-0.6, 3.4); ax.set_ylim(-1.9, 2.0); ax.set_aspect('equal'); ax.axis('off')
    c = np.array([2.1, 0.3])
    xx = c[0] + 0.85 * np.cos(ph) + 0.15 * np.cos(2 * ph); yy = c[1] + 0.7 * np.sin(ph)
    ax.plot(xx, yy, color=fs.BLACK, lw=1.4)
    for f in (0.2, 0.7):
        head(ax, np.column_stack([xx, yy]), f, color=fs.BLACK, ms=11)
    wire_dot(ax, (0, 0))
    ax.text(0.0, -0.35, r'$I$', fontsize=11, ha='center')
    ang = np.arctan2(yy, xx)
    for a in (ang.min(), ang.max()):
        ax.plot([0, 3.3 * np.cos(a)], [0, 3.3 * np.sin(a)], color=fs.GRAY, lw=0.8, ls='--')
    fs.angle_arc(ax, (0, 0), 0.75, np.degrees(ang.min()), np.degrees(ang.max()), None, color=fs.GRAY)
    ax.text(0.95, 0.05, r'$\Delta\varphi$', fontsize=9, color=fs.GRAY)
    ax.text(c[0] + 0.15, c[1] + 0.85, r'$C\,^\prime$', fontsize=11)
    fig.text(0.77, 0.03, r"(나) 감지 않는 경로: $\oint d\varphi = 0$", fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, __file__, 'fig27_09')


# ---------- 그림 27.10 굵은 도선 (예제 27.5) ----------
def fig10():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.5), gridspec_kw={'width_ratios': [1, 1.5]})
    ax = axs[0]; ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_aspect('equal'); ax.axis('off')
    # 전류 밀도 J ∝ r: 바깥으로 갈수록 진하게
    for k in range(30, 0, -1):
        r = k / 30
        ax.add_patch(Circle((0, 0), r, fc=(0.75 - 0.4 * r, 0.80 - 0.35 * r, 0.92 - 0.2 * r), ec='none', zorder=1))
    ax.add_patch(Circle((0, 0), 1, fc='none', ec=fs.BLACK, lw=1.2, zorder=2))
    circ_arrow(ax, (0, 0), 0.55, 0, 360, arrow_at=[60], color=F, ls='--', lw=1.0)
    circ_arrow(ax, (0, 0), 1.4, 0, 360, arrow_at=[60], color=F, ls='--', lw=1.0)
    ax.plot([0, 0.55 * np.cos(np.radians(-30))], [0, 0.55 * np.sin(np.radians(-30))], color=fs.BLACK, lw=0.7)
    ax.text(0.28, -0.32, r'$r$', fontsize=9)
    ax.plot([0, np.cos(np.radians(-120))], [0, np.sin(np.radians(-120))], color=fs.BLACK, lw=0.7)
    ax.text(-0.42, -0.45, r'$R$', fontsize=9)
    fs.dot_out(ax, (0, 0), r=0.08)
    ax.text(1.05, 1.15, r'$r>R$', fontsize=8.5, color=F)
    ax.text(-0.35, 0.22, r'$r<R$', fontsize=8.5, color=F)
    ax.text(0, -1.68, r'$J = J_0 r/R$ (진할수록 큼)', fontsize=8.5, ha='center')
    ax = axs[1]
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    r = np.linspace(0, 3, 400)
    B1 = np.where(r < 1, r ** 2, 1 / np.maximum(r, 1e-9))
    B2 = np.where(r < 1, r, 1 / np.maximum(r, 1e-9))
    ax.plot(r, B1, color=fs.VEL, lw=1.8, label=r'$J = J_0r/R$: 안 $\propto r^2$')
    ax.plot(r, B2, color=fs.FORCE, lw=1.3, ls='--', label=r'균일한 $J$: 안 $\propto r$')
    ax.axvline(1, color=fs.GRAY, lw=0.8, ls=':')
    ax.text(2.0, 0.55, r'밖: $\dfrac{\mu_0 I}{2\pi r}$', fontsize=9)
    ax.set_xlabel(r'$r/R$'); ax.set_ylabel(r'$B\,/\,(\mu_0I/2\pi R)$')
    ax.set_xlim(0, 3); ax.set_ylim(0, 1.1)
    ax.legend(fontsize=8, loc='upper right', frameon=False)
    fig.subplots_adjust(wspace=0.25)
    fs.save(fig, __file__, 'fig27_10')


# ---------- 그림 27.11 무한 전류 판 ----------
def fig11():
    fig, ax = fs.canvas(4.0, 2.3, xlim=(-2.4, 2.6), ylim=(-1.35, 1.35))
    ax.add_patch(Rectangle((-2.3, -0.06), 4.6, 0.12, fc='#dfe6ee', ec='none', zorder=1))
    for x in np.arange(-2.1, 2.2, 0.35):
        fs.dot_out(ax, (x, 0), r=0.09)
    for x in (-1.6, 0.0, 1.6):
        fs.arrow(ax, (x + 0.35, 0.75), (x - 0.35, 0.75), color=F, lw=1.6)
        fs.arrow(ax, (x - 0.35, -0.75), (x + 0.35, -0.75), color=F, lw=1.6)
    ax.text(-2.3, 0.95, r'$\vec{B}$', fontsize=11, color=F)
    ax.text(-2.3, -1.05, r'$\vec{B}$', fontsize=11, color=F)
    # 앙페르 경로
    x0, x1, y0, y1 = 0.55, 1.35, -0.45, 0.45
    pts = np.array([[x1, y0], [x1, y1], [x0, y1], [x0, y0], [x1, y0]])
    ax.plot(pts[:, 0], pts[:, 1], color=fs.BLACK, lw=1.1, ls='--', zorder=3)
    for a, b in zip(pts[:-1], pts[1:]):
        head(ax, [a, b], 0.5, color=fs.BLACK, ms=9)
    ax.text((x0 + x1) / 2, y1 + 0.1, r'$\ell$', fontsize=10, ha='center', va='bottom')
    ax.text(2.35, 0.12, r'$K$', fontsize=11)
    # 좌표축
    o = np.array([-2.1, -1.2])
    fs.arrow(ax, o, o + (0.4, 0), color=fs.GRAY, lw=0.8, ms=7); ax.text(o[0] + 0.48, o[1], r'$y$', fontsize=8, color=fs.GRAY, va='center')
    fs.arrow(ax, o, o + (0, 0.4), color=fs.GRAY, lw=0.8, ms=7); ax.text(o[0], o[1] + 0.5, r'$z$', fontsize=8, color=fs.GRAY, ha='center')
    fs.dot_out(ax, o, r=0.06, color=fs.GRAY); ax.text(o[0] - 0.12, o[1] - 0.05, r'$x$', fontsize=8, color=fs.GRAY, ha='right')
    fs.save(fig, __file__, 'fig27_11')


# ---------- 그림 27.13 솔레노이드와 앙페르 경로 ----------
def fig12():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-2.6, 2.6), ylim=(-1.55, 1.65))
    a = 0.75
    xs = np.arange(-2.3, 2.35, 0.3)
    for x in xs:
        fs.dot_out(ax, (x, a), r=0.1)
        fs.cross_in(ax, (x, -a), r=0.1)
    for y in (-0.42, -0.1):
        fs.arrow(ax, (-2.4, y), (2.4, y), color=F, lw=1.1, ms=10)
    ax.text(2.45, -0.26, r'$\vec{B}$', fontsize=11, color=F, va='center')
    # 경로 abcd
    x0, x1, yb, yt = -0.9, 0.9, 0.25, 1.35
    pts = np.array([[x0, yb], [x1, yb], [x1, yt], [x0, yt], [x0, yb]])
    ax.plot(pts[:, 0], pts[:, 1], color=fs.BLACK, lw=1.3, zorder=7)
    for p, q in zip(pts[:-1], pts[1:]):
        head(ax, [p, q], 0.55 if p[1] == q[1] else (0.25 if q[1] > p[1] else 0.75), color=fs.BLACK, ms=10, zorder=8)
    for p, s, off in [((x0, yb), 'a', (-0.15, -0.12)), ((x1, yb), 'b', (0.15, -0.12)),
                      ((x1, yt), 'c', (0.15, 0.1)), ((x0, yt), 'd', (-0.15, 0.1))]:
        ax.text(p[0] + off[0], p[1] + off[1], '$' + s + '$', fontsize=11, ha='center', va='center')
    ax.text(0, 0.2, r'$h$', fontsize=10, ha='center', va='top')
    ax.text(-2.3, 1.42, r'바깥 $B\approx 0$', fontsize=9)
    ax.text(-2.55, -1.42, r'단위 길이당 감은 수 $n$, 전류 $I$', fontsize=9)
    fs.save(fig, __file__, 'fig27_13')


# ---------- 그림 27.12 유한 솔레노이드의 자기장선 (계산) ----------
def fig13():
    a, L, Nl = 1.0, 4.0, 41
    zs = np.linspace(-L / 2, L / 2, Nl)
    def Bf(x, y):
        bz = br = 0.0
        for z0 in zs:
            b1, b2 = loop_B(x, y, a, z0); bz += b1; br += b2
        return bz, br
    fig, ax = fs.canvas(4.8, 2.9, xlim=(-4.0, 4.0), ylim=(-2.4, 2.4))
    box = (-4.0, 4.0, -2.4, 2.4)
    seeds = [0.0, 0.2, 0.4, 0.6, 0.78, 0.9]
    for s in seeds:
        for sgn in ([1] if s == 0 else [1, -1]):
            pts = trace_closed(Bf, (0.0, sgn * s), step=0.03, box=(box[0] - 0.3, box[1] + 0.3, box[2] - 0.3, box[3] + 0.3), nmax=2500)
            ax.plot(pts[:, 0], pts[:, 1], color=F, lw=0.9, zorder=1)
            # 화살촉: 안쪽(x≈0)과 바깥 귀환 부분
            i0 = np.argmin(np.hypot(pts[:, 0] - 0.0, pts[:, 1] - sgn * s))
            j = min(i0 + 3, len(pts) - 1)
            ax.add_patch(FancyArrowPatch(pts[i0], pts[j], arrowstyle='-|>', mutation_scale=9, color=F, lw=0, zorder=2))
            outer = [i for i, p in enumerate(pts) if abs(p[1]) > 1.25 and abs(p[0]) < 0.6 and box[2] < p[1] < box[3]]
            if outer:
                i = outer[len(outer) // 2]; j = min(i + 3, len(pts) - 1)
                ax.add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle='-|>', mutation_scale=9, color=F, lw=0, zorder=2))
    for z0 in zs[::3]:
        fs.dot_out(ax, (z0, a), r=0.09)
        fs.cross_in(ax, (z0, -a), r=0.09)
    ax.set_xlim(*box[:2]); ax.set_ylim(*box[2:])
    fs.save(fig, __file__, 'fig27_12')


# ---------- 그림 27.14 유한 솔레노이드의 축 위 자기장 ----------
def fig14():
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.4), gridspec_kw={'width_ratios': [1.15, 1]})
    ax = axs[0]; ax.set_xlim(-2.3, 2.5); ax.set_ylim(-1.3, 1.5); ax.set_aspect('equal'); ax.axis('off')
    L, R = 3.6, 0.9
    ax.add_patch(Rectangle((-L / 2, -R), L, 2 * R, fc='#f3eef7', ec=fs.BLACK, lw=1.1))
    for x in np.linspace(-L / 2, L / 2, 13):
        ax.plot([x, x], [-R, R], color=fs.GRAY, lw=0.3, alpha=0.6)
    ax.plot([-2.25, 2.4], [0, 0], color=fs.GRAY, lw=0.8)
    ax.text(2.4, 0.1, r'$+z$', fontsize=9, ha='right', va='bottom')
    P = np.array([-0.3, 0.0]); fs.dot(ax, P)
    ax.text(P[0], -0.2, r'$P$', fontsize=10, ha='center', va='top')
    for xe, lab, r_, tr in [(L / 2, r'$\theta_1$', 0.75, 0.95), (-L / 2, r'$\theta_2$', 0.32, 0.5)]:
        ax.plot([P[0], xe], [0, R], color=fs.BLACK, lw=0.9)
        a = np.degrees(np.arctan2(R, xe - P[0]))
        fs.angle_arc(ax, P, r_, 0, a, lab, fontsize=10, tr=tr)
    ax.text(0, R + 0.15, r'길이 $L$, 반지름 $R$', fontsize=8.5, ha='center', va='bottom')
    ax.text(0, -1.25, '(가) 끝 가장자리를 바라본 각', fontsize=9, ha='center')
    ax = axs[1]
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    Ls, Rs = 0.20, 0.02
    z = np.linspace(-0.16, 0.16, 400)
    c1 = (z + Ls / 2) / np.hypot(z + Ls / 2, Rs); c2 = (z - Ls / 2) / np.hypot(z - Ls / 2, Rs)
    ax.plot(z * 100, 0.5 * (c1 - c2), color=fs.VEL, lw=1.8)
    ax.axvspan(-10, 10, color=fs.FIELD, alpha=0.08, lw=0)
    for zz, v in [(0, 0.981), (5, 0.960), (10, 0.498), (15, 0.034)]:
        ax.plot(zz, v, 'o', color=fs.FORCE, ms=3.5)
    ax.text(10.6, 0.52, '끝: 약 1/2', fontsize=8.5)
    ax.set_xlabel(r'$z$ (cm)'); ax.set_ylabel(r'$B\,/\,\mu_0nI$')
    ax.set_ylim(0, 1.1); ax.set_xlim(-16, 16)
    ax.set_title(r'(나) $L = 20$ cm, $R = 2$ cm', fontsize=9)
    fig.subplots_adjust(wspace=0.25)
    fs.save(fig, __file__, 'fig27_14')


# ---------- 그림 27.15 토로이드 ----------
def fig15():
    fig, ax = fs.canvas(3.4, 3.3, xlim=(-2.1, 2.1), ylim=(-2.1, 2.05))
    a, b = 1.0, 1.55
    ax.add_patch(Wedge((0, 0), b, 0, 360, width=b - a, fc='#f3eef7', ec=fs.BLACK, lw=1.1))
    nw = 24
    for k in range(nw):
        t = 2 * np.pi * k / nw
        ax.plot([a * np.cos(t), b * np.cos(t)], [a * np.sin(t), b * np.sin(t)], color=fs.GRAY, lw=0.6)
        if k % 2 == 0:
            fs.dot_out(ax, (a * np.cos(t), a * np.sin(t)), r=0.06)
            fs.cross_in(ax, (b * np.cos(t), b * np.sin(t)), r=0.06)
    rm = (a + b) / 2
    circ_arrow(ax, (0, 0), rm, 0, 360, arrow_at=[100, 220, 340], color=F, ls='--', lw=1.1)
    circ_arrow(ax, (0, 0), 0.55, 0, 360, color=fs.GRAY, ls=':', lw=0.9)
    circ_arrow(ax, (0, 0), 1.95, 0, 360, color=fs.GRAY, ls=':', lw=0.9)
    t = np.radians(-35)
    ax.plot([0, rm * np.cos(t)], [0, rm * np.sin(t)], color=fs.BLACK, lw=0.7)
    ax.text(0.55, -0.55, r'$r$', fontsize=10)
    ax.text(0, 0.1, r'$B=0$', fontsize=8.5, ha='center', color=fs.GRAY)
    ax.text(1.5, 1.55, r'$B=0$', fontsize=8.5, color=fs.GRAY)
    ax.text(1.75 * np.cos(np.radians(118)), 1.75 * np.sin(np.radians(118)), r'$\vec{B}$', fontsize=11, color=F, ha='center', va='center')
    ax.text(-2.1, -2.05, r'감은 수 $N$, 전류 $I$', fontsize=8.5)
    fs.save(fig, __file__, 'fig27_15')


# ---------- 그림 27.16 전류 고리의 쌍극자장 (계산) ----------
def fig16():
    a = 1.0
    def Bf(x, y):
        return loop_B(x, y, a, 0.0)
    fig, ax = fs.canvas(3.8, 3.1, xlim=(-3.0, 3.0), ylim=(-2.4, 2.4))
    box = (-3.3, 3.3, -2.7, 2.7)
    for s in [0.0, 0.25, 0.5, 0.7, 0.85, 0.94]:
        for sgn in ([1] if s == 0 else [1, -1]):
            pts = trace_closed(Bf, (0.0, sgn * s), step=0.02, box=box, nmax=3000)
            ax.plot(pts[:, 0], pts[:, 1], color=F, lw=0.9, zorder=1)
            i0 = np.argmin(np.hypot(pts[:, 0], pts[:, 1] - sgn * s)); j = min(i0 + 3, len(pts) - 1)
            ax.add_patch(FancyArrowPatch(pts[i0], pts[j], arrowstyle='-|>', mutation_scale=9, color=F, lw=0, zorder=2))
            outer = [i for i, p in enumerate(pts) if abs(p[0]) < 0.4 and abs(p[1]) > 1.3 and abs(p[1]) < 2.35]
            if outer:
                i = outer[len(outer) // 2]; j = min(i + 3, len(pts) - 1)
                ax.add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle='-|>', mutation_scale=9, color=F, lw=0, zorder=2))
    ax.add_patch(Ellipse((0, 0), 0.35, 2 * a, fc='none', ec=fs.BLACK, lw=1.0, ls='--', zorder=3))
    fs.dot_out(ax, (0, a), r=0.12)
    fs.cross_in(ax, (0, -a), r=0.12)
    ax.text(0.2, a + 0.18, r'$I$', fontsize=11)
    fs.arrow(ax, (-0.05, 0), (0.75, 0), color=fs.FORCE, lw=2.6, ms=13, zorder=8)
    ax.text(0.5, 0.25, r'$\vec{\mu}$', fontsize=12, color=fs.FORCE)
    ax.set_xlim(-3.0, 3.0); ax.set_ylim(-2.4, 2.4)
    fs.save(fig, __file__, 'fig27_16')


# ---------- 그림 27.17 헬름홀츠 코일 ----------
def fig17():
    f = lambda u: (1 + u ** 2) ** -1.5
    z = np.linspace(-1.0, 1.0, 400)
    fig, ax = fs.plot_axes(4.0, 2.8)
    for d, col, ls, lab in [(0.6, fs.ACC, '--', r'$d = 0.6R$'), (1.0, fs.VEL, '-', r'$d = R$ (헬름홀츠)'),
                            (1.4, fs.ORANGE, '-.', r'$d = 1.4R$')]:
        s = d / 2
        B = (f(z - s) + f(z + s)) / (2 * f(s))
        ax.plot(z, B, color=col, ls=ls, lw=1.8 if d == 1.0 else 1.3, label=lab)
    ax.axvspan(-0.2, 0.2, color=fs.GRAY, alpha=0.12, lw=0)
    ax.set_xlabel(r'중심에서 축 방향 거리 $z/R$'); ax.set_ylabel(r'$B(z)/B(0)$')
    ax.set_ylim(0.4, 1.3); ax.set_xlim(-1, 1)
    ax.legend(fontsize=8.5, loc='lower center', frameon=False, ncol=1)
    ax.text(0, 1.24, r"$|z|<0.2R$", fontsize=8.5, ha='center', color=fs.GRAY)
    fs.save(fig, __file__, 'fig27_17')


# ---------- 그림 27.18 동축 케이블 (연습문제 7) ----------
def fig18():
    fig, ax = fs.canvas(2.8, 2.7, xlim=(-1.6, 1.7), ylim=(-1.55, 1.6))
    a, b, c = 0.45, 1.05, 1.35
    ax.add_patch(Wedge((0, 0), c, 0, 360, width=c - b, fc='#dfe6ee', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), a, fc='#dfe6ee', ec=fs.BLACK, lw=1.0))
    fs.dot_out(ax, (0, 0), r=0.1)
    for t in np.radians([45, 135, 225, 315]):
        fs.cross_in(ax, ((b + c) / 2 * np.cos(t), (b + c) / 2 * np.sin(t)), r=0.08)
    for r, t, lab in [(a, 90, r'$a$'), (b, 160, r'$b$'), (c, 200, r'$c$')]:
        tt = np.radians(t)
        fs.arrow(ax, (0, 0), (r * np.cos(tt), r * np.sin(tt)), color=fs.BLACK, lw=0.7, ms=7)
        ax.text(r * 0.6 * np.cos(tt) + 0.1 * np.cos(tt + 1.6), r * 0.6 * np.sin(tt) + 0.1 * np.sin(tt + 1.6),
                lab, fontsize=10, ha='center', va='center')
    ax.text(0.18, -0.22, r'$I$', fontsize=9)
    ax.text(c * 0.72 + 0.12, -c * 0.72 - 0.1, r'$I$', fontsize=9)
    fs.save(fig, __file__, 'fig27_18')


# ---------- 그림 27.19 부채꼴 고리 (연습문제 8) ----------
def fig19():
    fig, ax = fs.canvas(2.7, 2.5, xlim=(-0.45, 2.3), ylim=(-0.45, 2.3))
    a, b = 1.0, 2.0
    th = np.linspace(0, np.pi / 2, 100)
    ax.plot(b * np.cos(th), b * np.sin(th), color=fs.BLACK, lw=2.0)
    ax.plot(a * np.cos(th), a * np.sin(th), color=fs.BLACK, lw=2.0)
    ax.plot([a, b], [0, 0], color=fs.BLACK, lw=2.0)
    ax.plot([0, 0], [a, b], color=fs.BLACK, lw=2.0)
    ax.plot([0, a], [0, 0], color=fs.GRAY, lw=0.7, ls=':'); ax.plot([0, 0], [0, a], color=fs.GRAY, lw=0.7, ls=':')
    head(ax, [(b * np.cos(0.8), b * np.sin(0.8)), (b * np.cos(0.82), b * np.sin(0.82))], color=fs.BLACK, ms=12)
    head(ax, [(0, 1.55), (0, 1.45)], color=fs.BLACK, ms=12)
    head(ax, [(a * np.cos(0.82), a * np.sin(0.82)), (a * np.cos(0.8), a * np.sin(0.8))], color=fs.BLACK, ms=12)
    head(ax, [(1.45, 0), (1.55, 0)], color=fs.BLACK, ms=12)
    fs.dot(ax, (0, 0), r=0.04)
    ax.text(-0.08, -0.08, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(0.45, 0.12, r'$a$', fontsize=10); ax.text(1.5, -0.2, r'$b-a$', fontsize=9, ha='center')
    fs.angle_arc(ax, (0, 0), 0.3, 0, 90, '90°', fontsize=8.5, tr=0.5)
    ax.text(1.55, 1.55, r'$I$', fontsize=11)
    fs.save(fig, __file__, 'fig27_19')


# ---------- 그림 27.20 도선과 직사각형 고리 (연습문제 9) ----------
def fig20():
    fig, ax = fs.canvas(3.2, 2.6, xlim=(-0.7, 3.4), ylim=(-1.75, 1.75))
    ax.plot([0, 0], [-1.7, 1.7], color=fs.BLACK, lw=2.2)
    fs.arrow(ax, (-0.25, -0.3), (-0.25, 0.4), color=fs.BLACK, lw=1.2)
    ax.text(-0.45, 0.05, r'$30$ A', fontsize=9, ha='right')
    x0, x1, h = 0.35, 3.15, 1.3
    pts = np.array([[x0, -h], [x0, h], [x1, h], [x1, -h], [x0, -h]])
    ax.plot(pts[:, 0], pts[:, 1], color=fs.BLACK, lw=1.8)
    for p, q in zip(pts[:-1], pts[1:]):
        head(ax, [p, q], 0.5, color=fs.BLACK, ms=11)
    ax.text(1.75, 0, r'$20$ A', fontsize=9, ha='center')
    ax.annotate('', xy=(x0, -1.55), xytext=(0, -1.55), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.7))
    ax.text(x0 + 0.08, -1.55, '1.0 cm', fontsize=8, color=fs.GRAY, ha='left', va='center')
    ax.annotate('', xy=(x1, 1.5), xytext=(0, 1.5), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.7))
    ax.text(x1 / 2, 1.55, '9.0 cm', fontsize=8, color=fs.GRAY, ha='center', va='bottom')
    ax.annotate('', xy=(x1 + 0.15, h), xytext=(x1 + 0.15, -h), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.7))
    ax.text(x1 + 0.22, 0, '30 cm', fontsize=8, color=fs.GRAY, rotation=90, va='center')
    fs.save(fig, __file__, 'fig27_20')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10,
              fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20]:
        f()
