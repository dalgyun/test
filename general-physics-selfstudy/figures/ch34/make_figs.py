"""34장 회절과 편광 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Arc
from scipy.special import j1

RAY = fs.ORANGE
GLASS = '#dbe7f3'
E_COL = fs.FORCE


def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def arc2(ax, center, r, a1, a2, text=None, **kw):
    diff = (a2 - a1) % 360
    if diff > 180:
        a1, diff = a2, 360 - diff
    fs.angle_arc(ax, center, r, a1, a1 + diff, text, **kw)


def darrow(ax, p, q, text=None, tpos=None, color=fs.GRAY, fontsize=10, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=7, color=color, lw=0.7))
    if text:
        tp = tpos if tpos is not None else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        fs.label(ax, tp, text, fontsize=fontsize, color=color, **kw)


def sinc2(x):
    return np.sinc(x) ** 2      # np.sinc(x) = sin(pi x)/(pi x)


def airy(u):
    u = np.where(np.abs(u) < 1e-9, 1e-9, u)
    return (2 * j1(u) / u) ** 2


# ---------- 그림 34.1 단일 슬릿: 짝짓기 논법 ----------
def fig01():
    fig, ax = fs.canvas(4.6, 3.0, xlim=(-1.5, 4.2), ylim=(-2.0, 2.0))
    a = 2.4
    th = np.radians(28)
    u = np.array([np.cos(th), np.sin(th)])
    # 슬릿 가림막
    ax.add_patch(Rectangle((-0.08, a / 2), 0.16, 0.75, fc=fs.BLACK, ec='none'))
    ax.add_patch(Rectangle((-0.08, -a / 2 - 0.75), 0.16, 0.75, fc=fs.BLACK, ec='none'))
    for y in np.linspace(-1.0, 1.0, 5):
        fs.arrow(ax, (-1.4, y), (-0.25, y), color=fs.GRAY, lw=0.8, ms=7)
    ax.plot([0, 0], [-a / 2, a / 2], color=fs.GRAY, lw=0.6, ls=':')
    pts = {'top': np.array([0, a / 2]), 'mid': np.array([0, 0.0]), 'q1': np.array([0, a / 4]),
           'q3': np.array([0, -a / 4]), 'bot': np.array([0, -a / 2])}
    for k, P in pts.items():
        col = RAY if k in ('top', 'mid') else '#f0b27a'
        fs.ray(ax, [P, P + 3.6 * u], color=col, lw=1.4 if k in ('top', 'mid') else 0.8)
        fs.dot(ax, P, r=0.045, color=col)
    # 위쪽 점에서 가운데 광선으로 내린 수선 -> 경로차 (a/2) sin(theta)
    top, mid = pts['top'], pts['mid']
    foot = mid + np.dot(top - mid, u) * u
    ax.plot([top[0], foot[0]], [top[1], foot[1]], color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([mid[0], foot[0]], [mid[1], foot[1]], color=fs.FORCE, lw=3.0, solid_capstyle='butt', zorder=6)
    fs.label(ax, (1.25, -0.25), r'$\frac{a}{2}\sin\theta$', fontsize=11, color=fs.FORCE)
    ax.plot([0, 1.6], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    arc2(ax, mid, 0.95, 0, 28, r'$\theta$', tr=1.15, fontsize=10)
    darrow(ax, (-0.4, -a / 2), (-0.4, a / 2), r'$a$', tpos=(-0.6, -0.55), fontsize=11)
    darrow(ax, (0.3, 0), (0.3, a / 2), None)
    fs.label(ax, (0.47, a / 4 + 0.05), r'$\frac{a}{2}$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (3.4, 1.85), '스크린 쪽($L \\gg a$)', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig34_01')


# ---------- 그림 34.2 단일 슬릿의 페이저 그림 ----------
def fig02():
    fig, axs = fs.plt.subplots(1, 3, figsize=(5.4, 2.0))
    Lc = 2.0   # 페이저 사슬의 전체 길이 (= E_m)
    for ax, (al, title) in zip(axs, ((0.0, r'$\alpha = 0$'), (np.pi / 2, r'$\alpha = \pi/2$'), (np.pi, r'$\alpha = \pi$'))):
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(-0.2, 2.2); ax.set_ylim(-0.25, 1.6)
        n = 12
        phis = np.linspace(0, 2 * al, n + 1)[:-1] + al / n   # 각 조각의 방향
        p = np.array([0.0, 0.0]); pts = [p.copy()]
        for ph in phis:
            p = p + Lc / n * np.array([np.cos(ph), np.sin(ph)]); pts.append(p.copy())
        for a_, b_ in zip(pts[:-1], pts[1:]):
            ax.add_patch(FancyArrowPatch(a_, b_, arrowstyle='-|>', mutation_scale=6, color=fs.VEL, lw=1.0,
                                         shrinkA=0, shrinkB=0))
        end = pts[-1]
        if np.hypot(*end) > 1e-6:
            fs.arrow(ax, (0, 0), tuple(end), color=fs.FORCE, lw=1.8, ms=10)
        if al == 0:
            fs.label(ax, (1.0, -0.18), r'$E_m$', fontsize=10, color=fs.FORCE)
        elif al < 3:
            fs.label(ax, (end[0] / 2 + 0.12, end[1] / 2 - 0.2), r'$E_\theta$', fontsize=10, color=fs.FORCE)
        else:
            fs.label(ax, (0.4, -0.15), r'합 $= 0$', fontsize=9, color=fs.FORCE)
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig34_02')


# ---------- 그림 34.3 단일 슬릿 세기 분포 ----------
def fig03():
    fig, ax = fs.plot_axes(4.6, 2.6)
    x = np.linspace(-3.6, 3.6, 3001)     # a sin(theta) / lambda = alpha/pi
    I = sinc2(x)
    ax.plot(x, I, color=fs.VEL, lw=1.5)
    ax.plot(x, 10 * I * (np.abs(x) > 1), color=fs.VEL, lw=0.8, ls='--')
    ax.text(2.95, 0.5, r'$\times 10$', fontsize=8.5, color=fs.VEL)
    for xm, val in ((1.4303, 0.0472), (2.4590, 0.0165)):
        for s in (1, -1):
            ax.plot(s * xm, 10 * val, 'o', color=fs.VEL, ms=3)
        ax.annotate(f'{val:.4f}', (xm, 10 * val), xytext=(xm + 0.15, 10 * val + 0.17), fontsize=8, color=fs.FORCE)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(0, 1.08)
    ax.set_xticks(range(-3, 4))
    ax.set_xlabel(r'$a\sin\theta/\lambda = \alpha/\pi$', fontsize=9)
    ax.set_ylabel(r'$I/I_m$', fontsize=9)
    fs.save(fig, __file__, 'fig34_03')


# ---------- 그림 34.4 유한한 폭의 이중 슬릿 (d = 4a) ----------
def fig04():
    fig, ax = fs.plot_axes(4.8, 2.6)
    x = np.linspace(-9.5, 9.5, 6001)     # d sin(theta)/lambda = beta/pi
    env = sinc2(x / 4)
    I = np.cos(np.pi * x) ** 2 * env
    ax.fill_between(x, I, color=fs.VEL, alpha=0.15, lw=0)
    ax.plot(x, I, color=fs.VEL, lw=1.2)
    ax.plot(x, env, color=fs.FORCE, lw=1.0, ls='--', label='회절 포락선')
    for m in (-4, 4, -8, 8):
        ax.annotate(f'{m:+d}' if m else '0', (m, 0.0), xytext=(m, 0.17), ha='center', fontsize=8, color=fs.FORCE,
                    arrowprops=dict(arrowstyle='-|>', color=fs.FORCE, lw=0.7, mutation_scale=7))
    ax.text(0, 1.03, '중앙 극대 안에 7개', ha='center', va='bottom', fontsize=8.5)
    ax.set_xlim(-9.5, 9.5); ax.set_ylim(0, 1.18)
    ax.set_xticks(range(-8, 9, 2))
    ax.set_xlabel(r'$d\sin\theta/\lambda$  (간섭 차수 $m$)', fontsize=9)
    ax.set_ylabel(r'$I/I_m$', fontsize=9)
    ax.text(5.6, 0.62, '빠진 차수\n$m = \\pm 4, \\pm 8$', fontsize=8, color=fs.FORCE, ha='center')
    ax.legend(fontsize=8, loc='upper right', frameon=False)
    fs.save(fig, __file__, 'fig34_04')


# ---------- 그림 34.5 원형 구멍의 회절(에어리 무늬) ----------
def fig05():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.4, 2.4), gridspec_kw=dict(width_ratios=[1.6, 1]))
    ax = axs[0]
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    x = np.linspace(-3.2, 3.2, 3001)      # D sin(theta)/lambda
    u = np.pi * x
    ax.plot(x, airy(u), color=fs.VEL, lw=1.4, label='원형 구멍')
    ax.plot(x, sinc2(x), color=fs.GRAY, lw=0.9, ls='--', label='슬릿(폭 $D$)')
    ax.axvline(1.22, color=fs.FORCE, lw=0.8, ls=':')
    ax.axvline(-1.22, color=fs.FORCE, lw=0.8, ls=':')
    ax.text(1.3, 0.75, '$1.22$', fontsize=8.5, color=fs.FORCE)
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(0, 1.05)
    ax.set_xlabel(r'$D\sin\theta/\lambda$', fontsize=9); ax.set_ylabel(r'$I/I_m$', fontsize=9)
    ax.legend(fontsize=7.5, frameon=False, loc='upper left')
    ax = axs[1]
    g = np.linspace(-3.2, 3.2, 500)
    X, Y = np.meshgrid(g, g)
    I = airy(np.pi * np.hypot(X, Y))
    ax.imshow(I ** 0.3, extent=(-3.2, 3.2, -3.2, 3.2), cmap='gray', origin='lower')
    ax.add_patch(Circle((0, 0), 1.22, fc='none', ec=fs.FORCE, lw=0.6, ls=':'))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('스크린의 무늬(밝기 과장)', fontsize=8.5)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig34_05')


# ---------- 그림 34.6 레일리 기준 ----------
def fig06():
    fig, axs = fs.plt.subplots(1, 3, figsize=(5.4, 1.9), sharey=True)
    x = np.linspace(-2.5, 4.2, 2001)
    for ax, (sep, title) in zip(axs, ((0.7, '분해 안 됨'), (1.22, '레일리 기준(겨우 분해)'), (2.2, '분해됨'))):
        I1 = airy(np.pi * x); I2 = airy(np.pi * (x - sep))
        ax.plot(x, I1, color=fs.GRAY, lw=0.8, ls='--'); ax.plot(x, I2, color=fs.GRAY, lw=0.8, ls='--')
        ax.plot(x, I1 + I2, color=fs.VEL, lw=1.4)
        ax.set_xlim(-2.5, 4.2); ax.set_ylim(0, 1.75)
        ax.set_xticks([0, sep]); ax.set_xticklabels(['0', f'{sep:g}'], fontsize=8)
        ax.set_yticks([])
        for s in ('top', 'right', 'left'):
            ax.spines[s].set_visible(False)
        ax.set_title(title, fontsize=8.5)
    axs[1].set_xlabel(r'각 위치 ($\lambda/D$ 단위)', fontsize=8.5)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig34_06')


# ---------- 그림 34.7 N개 슬릿의 세기 ----------
def fig07():
    fig, axs = fs.plt.subplots(3, 1, figsize=(4.6, 3.4), sharex=True)
    ph = np.linspace(-1.25, 1.25, 6001) * 2 * np.pi
    for ax, N in zip(axs, (2, 5, 20)):
        num = np.sin(N * ph / 2); den = np.sin(ph / 2)
        with np.errstate(invalid='ignore', divide='ignore'):
            I = np.where(np.abs(den) < 1e-9, N ** 2, (num / den) ** 2) / N ** 2
        ax.plot(ph / (2 * np.pi), I, color=fs.VEL, lw=1.1)
        ax.set_ylim(0, 1.1); ax.set_yticks([0, 1]); ax.set_yticklabels(['0', r'$N^2I_0$'], fontsize=8)
        ax.text(1.24, 0.75, f'$N = {N}$', fontsize=9, ha='right')
        ax.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    axs[2].set_xlim(-1.25, 1.25)
    axs[2].set_xticks([-1, 0, 1]); axs[2].set_xticklabels([r'$m=-1$', r'$0$', r'$m=1$'], fontsize=8)
    axs[2].set_xlabel(r'$d\sin\theta/\lambda = \phi/2\pi$', fontsize=9)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, __file__, 'fig34_07')


# ---------- 그림 34.8 회절격자의 주극대 방향 (예제 34.4) ----------
def fig08():
    fig, ax = fs.canvas(4.2, 3.4, xlim=(-1.6, 3.3), ylim=(-3.0, 3.0))
    ax.plot([0, 0], [-1.2, 1.2], color=fs.BLACK, lw=2.0)
    for y in np.linspace(-1.1, 1.1, 12):
        ax.plot([-0.08, 0.08], [y, y], color='white', lw=0.8)
    for y in (-0.4, 0.0, 0.4):
        fs.arrow(ax, (-1.5, y), (-0.15, y), color=RAY, lw=1.1, ms=8)
    d_over_lam = 1 / 0.300
    R = 2.6
    for m in range(-3, 4):
        s = m / d_over_lam
        th = np.arcsin(s)
        e = R * np.array([np.cos(th), np.sin(th)])
        fs.arrow(ax, (0, 0), tuple(e), color=RAY if m == 0 else fs.FIELD, lw=1.2 if m == 0 else 1.0, ms=8)
        lab = f'$m={m:+d}$' if m else '$m=0$'
        fs.label(ax, (1.13 * e[0] + 0.05, 1.13 * e[1]), lab, fontsize=8.5, ha='left' if m else 'left')
        if m > 0:
            fs.label(ax, (0.62 * e[0] + 0.0, 0.62 * e[1] + 0.2), f'{np.degrees(th):.1f}°', fontsize=8, color=fs.GRAY)
    fs.label(ax, (-0.8, 1.45), '격자\n600개/mm', fontsize=8)
    fs.label(ax, (-0.85, -0.75), r'$\lambda = 500$ nm', fontsize=8.5, color=RAY)
    fs.save(fig, __file__, 'fig34_08')


# ---------- 그림 34.9 브래그 반사 ----------
def fig09():
    fig, ax = fs.canvas(4.8, 2.9, xlim=(-3.2, 3.2), ylim=(-1.9, 1.8))
    d = 1.0
    th = np.radians(32)
    for k, y in enumerate((0.0, -d, -2 * d + 0.0)):
        if y < -1.9:
            continue
        ax.plot([-3.0, 3.0], [y, y], color=fs.GRAY, lw=0.6, ls='--')
        for x in np.arange(-2.8, 3.0, 0.7):
            fs.dot(ax, (x, y), r=0.07, color='#555555')
    fs.label(ax, (2.75, 0.18), '결정면 1', fontsize=8, color=fs.GRAY)
    fs.label(ax, (2.75, -d + 0.18), '결정면 2', fontsize=8, color=fs.GRAY)
    A = np.array([0.0, 0.0]); B = np.array([0.0, -d])
    kin = np.array([np.cos(th), -np.sin(th)])
    kout = np.array([np.cos(th), np.sin(th)])
    L = 2.6
    for P, c in ((A, RAY), (B, fs.VEL)):
        fs.ray(ax, [P - L * kin, P, P + L * kout], color=c, lw=1.2)
    # 추가 경로: A에서 아래 광선에 내린 수선의 발
    f1 = B + np.dot(A - B, -kin) * (-kin)       # 들어오는 아래 광선 위
    f2 = B + np.dot(A - B, kout) * kout         # 나가는 아래 광선 위
    for f in (f1, f2):
        ax.plot([A[0], f[0]], [A[1], f[1]], color=fs.GRAY, lw=0.8, ls=':')
        ax.plot([f[0], B[0]], [f[1], B[1]], color=fs.FORCE, lw=3.0, solid_capstyle='butt', zorder=6)
    fs.label(ax, (f1[0] - 0.62, (f1[1] + B[1]) / 2 - 0.1), r'$d\sin\theta$', fontsize=10, color=fs.FORCE)
    fs.label(ax, (f2[0] + 0.62, (f2[1] + B[1]) / 2 - 0.1), r'$d\sin\theta$', fontsize=10, color=fs.FORCE)
    arc2(ax, A, 0.7, 180 - np.degrees(th), 180, r'$\theta$', tr=0.9, fontsize=10)
    arc2(ax, A, 0.7, 0, np.degrees(th), r'$\theta$', tr=0.9, fontsize=10)
    darrow(ax, (-2.2, 0), (-2.2, -d), r'$d$', tpos=(-2.4, -d / 2))
    fs.label(ax, (-2.3, 1.45), '입사 X선', fontsize=8.5)
    fs.label(ax, (2.3, 1.45), '반사 X선', fontsize=8.5)
    fs.save(fig, __file__, 'fig34_09')


# ---------- 그림 34.10 편광판 세 장 (예제 34.7) ----------
ZX, ZY = -0.5, -0.3


def P3(x, y, z):
    return np.array([x + ZX * z, y + ZY * z])


def fig10():
    fig, ax = fs.canvas(5.4, 2.5, xlim=(-1.2, 9.2), ylim=(-1.6, 1.75))
    R = 0.95
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot([-1.0, 9.0], [0, 0], color=fs.GRAY, lw=0.5, ls='-.')
    xs = (1.6, 4.3, 7.0)
    axes_deg = (0, 45, 90)        # 연직에서 잰 투과축 각
    amps = (np.sqrt(0.5), 0.5, np.sqrt(0.125))
    labels = (r'$I_0/2$', r'$I_0/4$', r'$I_0/8$')
    # 편광되지 않은 빛
    for a in np.radians(np.arange(0, 180, 30)):
        v = 0.75 * np.array([0, np.cos(a), np.sin(a)])
        p, q = P3(0.0, *(v[1:])), P3(0.0, *(-v[1:]))
        ax.add_patch(FancyArrowPatch(q, p, arrowstyle='<|-|>', mutation_scale=6, color=E_COL, lw=0.8))
    fs.label(ax, (0.0, -1.3), '편광되지 않은 빛\n$I_0$', fontsize=8)
    for x0, ang, amp, lab in zip(xs, axes_deg, amps, labels):
        pts = np.array([P3(x0, R * np.cos(tt), R * np.sin(tt)) for tt in t])
        ax.fill(pts[:, 0], pts[:, 1], color='#dfe6ee', alpha=0.85, zorder=2)
        ax.plot(pts[:, 0], pts[:, 1], color=fs.BLACK, lw=0.9, zorder=3)
        a = np.radians(ang)
        e = np.array([np.cos(a), np.sin(a)])
        p, q = P3(x0, *(0.85 * R * e)), P3(x0, *(-0.85 * R * e))
        ax.plot([p[0], q[0]], [p[1], q[1]], color=fs.BLACK, lw=1.0, ls='--', zorder=4)
        fs.label(ax, (x0 + 0.05, 1.2), f'{ang}°', fontsize=9)
        # 지난 뒤의 전기장
        xe = x0 + 1.25
        v = amp * 1.1 * e
        p, q = P3(xe, *v), P3(xe, *(-v))
        ax.add_patch(FancyArrowPatch(q, p, arrowstyle='<|-|>', mutation_scale=7, color=E_COL, lw=1.4, zorder=5))
        fs.label(ax, (xe + 0.15, -1.3), lab, fontsize=9)
    fs.arrow(ax, (8.5, 0), (9.1, 0), color=fs.BLACK, lw=1.2, ms=8)
    fs.save(fig, __file__, 'fig34_10')


# ---------- 그림 34.11 브루스터 각 ----------
def fig11():
    fig, ax = fs.canvas(4.4, 3.2, xlim=(-2.4, 2.4), ylim=(-1.9, 1.9))
    n1, n2 = 1.0, 1.5
    thB = np.arctan(n2 / n1); tht = np.pi / 2 - thB
    ax.add_patch(Rectangle((-2.4, -1.9), 4.8, 1.9, fc=GLASS, ec='none', zorder=0))
    ax.plot([-2.4, 2.4], [0, 0], color=fs.BLACK, lw=1.1)
    ax.plot([0, 0], [-1.6, 1.6], color=fs.GRAY, lw=0.8, ls='--')
    L = 1.9
    din = np.array([np.sin(thB), -np.cos(thB)])
    dre = np.array([np.sin(thB), np.cos(thB)])
    dtr = np.array([np.sin(tht), -np.cos(tht)])
    S = -L * din
    fs.ray(ax, [S, (0, 0)], color=RAY, lw=1.4)
    fs.ray(ax, [(0, 0), L * dre], color=RAY, lw=1.4)
    fs.ray(ax, [(0, 0), 1.75 * dtr], color=RAY, lw=1.4)

    def marks(p0, d, s_on=True, p_amp=0.0, n=3, start=0.25, step=0.42):
        nrm = np.array([-d[1], d[0]])
        for k in range(n):
            c = p0 + (start + k * step) * d
            if s_on:
                ax.add_patch(Circle(c, 0.05, fc=E_COL, ec='none', zorder=6))
            if p_amp > 0:
                ax.add_patch(FancyArrowPatch(c - p_amp * nrm, c + p_amp * nrm, arrowstyle='<|-|>', mutation_scale=6,
                                             color=E_COL, lw=0.9, zorder=6))
    marks(S, din, True, 0.17, n=3, start=0.35)
    marks(np.zeros(2), dre, True, 0.0, n=3, start=0.6)
    marks(np.zeros(2), dtr, True, 0.17, n=3, start=0.45, step=0.4)
    arc2(ax, (0, 0), 0.55, 90, 90 + np.degrees(thB), r'$\theta_B$', tr=0.78, fontsize=9)
    arc2(ax, (0, 0), 0.55, 90 - np.degrees(thB), 90, r'$\theta_B$', tr=0.78, fontsize=9)
    arc2(ax, (0, 0), 0.55, -90, -90 + np.degrees(tht), r'$\theta_t$', tr=0.78, fontsize=9)
    # 반사 광선과 굴절 광선 사이의 직각 표시
    k = 0.22
    q0 = k * dre; q1 = k * dre + k * dtr; q2 = k * dtr
    ax.plot([q0[0] + 0.0, q1[0], q2[0]], [q0[1], q1[1], q2[1]], color=fs.BLACK, lw=0.8)
    fs.label(ax, (1.25, 0.12), '90°', fontsize=8.5)
    fs.label(ax, (-2.0, 0.25), r'$n_1$', fontsize=11); fs.label(ax, (-2.0, -0.25), r'$n_2$', fontsize=11)
    fs.label(ax, (-1.55, 1.65), '편광되지 않은 빛', fontsize=8)
    fs.label(ax, (1.45, 1.75), '입사면에 수직으로\n완전 편광', fontsize=8, va='center')
    fs.label(ax, (1.55, -1.6), '부분 편광', fontsize=8)
    fs.save(fig, __file__, 'fig34_11')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11]:
        f()
