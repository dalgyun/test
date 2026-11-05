"""15장 진동 그림. 실행: python3 figures/ch15/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, FancyArrowPatch

F = __file__


def dline(ax, p, q, color=fs.GRAY, lw=0.8, ls='--', zorder=1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=zorder)


def darrow(ax, p, q, text=None, color=fs.BLACK, off=(0, 0.12), fontsize=10, ms=8, lw=0.8, **kw):
    """양쪽 화살표(길이 표시)."""
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=ms, color=color, lw=lw, zorder=5))
    if text:
        m = ((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1])
        ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color, **kw)


# ---------------------------------------------------------------- 15.1 용수철 진자
def fig01():
    fig, ax = fs.canvas(4.6, 2.5, xlim=(-0.3, 5.4), ylim=(-0.75, 2.6))
    x_eq = 3.0
    for (y0, xb, tag) in ((1.55, x_eq, '(가) 평형 위치'), (0.0, x_eq + 0.85, '(나) 변위 $x$')):
        fs.wall(ax, y0, y0 + 0.9, x=0.0, side='left')
        fs.ground(ax, 0.0, 5.2, y=y0)
        fs.block(ax, (xb, y0 + 0.3), w=0.8, h=0.6, text='$m$')
        fs.spring(ax, (0.0, y0 + 0.3), (xb - 0.4, y0 + 0.3), coils=9, width=0.13)
        ax.text(5.2, y0 + 0.75, tag, ha='right', va='center', fontsize=9)
    ax.text(0.15, 1.55 + 0.62, '$k$', fontsize=10)
    dline(ax, (x_eq, -0.35), (x_eq, 2.5))
    ax.text(x_eq, 2.55, '$x=0$', ha='center', va='bottom', fontsize=9, color=fs.GRAY)
    # 변위와 힘
    fs.arrow(ax, (x_eq, -0.3), (x_eq + 0.85, -0.3), color=fs.BLACK, lw=1.1, ms=9)
    ax.text(x_eq + 0.43, -0.48, '$x$', ha='center', va='center', fontsize=10)
    xb = x_eq + 0.85
    fs.arrow(ax, (xb, 0.82), (xb - 0.95, 0.82), color=fs.FORCE, lw=1.6)
    ax.text(xb - 1.05, 0.82, '$F=-kx$', color=fs.FORCE, ha='right', va='center', fontsize=10)
    ax.text(2.0, -0.62, '마찰 없는 면', fontsize=8, color=fs.GRAY, ha='center')
    fs.save(fig, F, 'fig15_01')


# ---------------------------------------------------------------- 15.1 x, v, a 그래프 (예제 15.1)
def fig02():
    import matplotlib.pyplot as plt
    A, w, phi = 0.050, 20.0, 0.644
    T = 2 * np.pi / w
    t = np.linspace(0, 2 * T, 800)
    x = A * np.cos(w * t + phi)
    v = -w * A * np.sin(w * t + phi)
    a = -w ** 2 * A * np.cos(w * t + phi)
    fig, axs = plt.subplots(3, 1, figsize=(4.8, 3.5), sharex=True)
    data = [(x * 100, '$x$ (cm)', fs.BLACK, 5.0), (v, '$v$ (m/s)', fs.VEL, 1.0), (a, '$a$ (m/s$^2$)', fs.ACC, 20.0)]
    # 각 양이 최대가 되는 첫 시각: x는 wt+phi=2pi, v는 wt+phi=3pi/2, a는 wt+phi=pi
    tpk = [(2 * np.pi - phi) / w, (1.5 * np.pi - phi) / w, (np.pi - phi) / w]
    for ax, (y, lab, c, m), tp in zip(axs, data, tpk):
        ax.plot(t, y, color=c, lw=1.5)
        ax.axhline(0, color=fs.GRAY, lw=0.6)
        ax.set_ylabel(lab, fontsize=9)
        ax.set_ylim(-1.45 * m, 1.35 * m)
        ax.set_yticks([-m, 0, m])
        ax.tick_params(labelsize=8)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
        ax.plot([tp], [m], 'o', color=c, ms=4)
        for k in range(9):
            ax.axvline(k * T / 4, color='#e0e0e0', lw=0.5, zorder=0)
    axs[0].plot([0], [4.0], 's', color=fs.BLACK, ms=4, clip_on=False)
    axs[0].annotate('$x_0=4.0$ cm', (0, 4.0), (0.03, 5.6), fontsize=8, va='center')
    axs[1].plot([0], [-0.6], 's', color=fs.VEL, ms=4, clip_on=False)
    axs[1].annotate('$v_0=-0.60$ m/s', (0, -0.6), (0.03, -1.15), fontsize=8, va='center', color=fs.VEL)
    for tp in tpk:
        for ax in axs:
            ax.axvline(tp, color=fs.ORANGE, lw=0.7, ls=':')
    axs[2].annotate('', xy=(tpk[2], -25), xytext=(tpk[0], -25),
                    arrowprops=dict(arrowstyle='<|-|>', color=fs.ORANGE, lw=0.8, mutation_scale=7))
    axs[2].text((tpk[0] + tpk[2]) / 2, -25, '$T/2$', fontsize=8, color=fs.ORANGE, ha='center', va='center',
                bbox=dict(fc='white', ec='none', pad=0.5))
    axs[1].annotate('', xy=(tpk[1], -1.28), xytext=(tpk[0], -1.28),
                    arrowprops=dict(arrowstyle='<|-|>', color=fs.ORANGE, lw=0.8, mutation_scale=7))
    axs[1].text(tpk[0] + 0.006, -1.28, '$T/4$', fontsize=8, color=fs.ORANGE, ha='left', va='center')
    ticks = [k * T / 4 for k in range(9)]
    labs = ['0', '', '$T/2$', '', '$T$', '', '$3T/2$', '', '$2T$']
    axs[2].set_xticks(ticks); axs[2].set_xticklabels(labs, fontsize=8)
    axs[2].set_xlabel('$t$', fontsize=9)
    axs[2].set_xlim(0, 2 * T)
    fig.align_ylabels(axs)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, F, 'fig15_02')


# ---------------------------------------------------------------- 예제 15.2 연직 용수철
def fig03():
    fig, ax = fs.canvas(4.2, 3.4, xlim=(-0.4, 6.4), ylim=(-0.75, 4.6))
    top = 4.2
    fs.ceiling(ax, -0.2, 6.2, top)
    L0 = 1.6           # 자연 길이
    dl = 0.8           # 평형 늘음
    yp = 0.55          # 더 당긴 변위
    xs = [0.6, 2.9, 5.2]
    ends = [top - L0, top - L0 - dl, top - L0 - dl - yp]
    for i, (x, e) in enumerate(zip(xs, ends)):
        fs.spring(ax, (x, top), (x, e), coils=8, width=0.14)
        if i > 0:
            fs.block(ax, (x, e - 0.3), w=0.7, h=0.6, text='$m$')
    ax.text(xs[0], -0.6, '(가) 자연 길이', ha='center', fontsize=9)
    ax.text(xs[1], -0.6, '(나) 평형', ha='center', fontsize=9)
    ax.text(xs[2], -0.6, '(다) 진동 중', ha='center', fontsize=9)
    # 기준선
    y0 = top - L0
    yeq = y0 - dl
    dline(ax, (xs[0] - 0.5, y0), (6.3, y0))
    dline(ax, (xs[1] - 0.5, yeq), (6.3, yeq))
    ax.text(-0.35, y0, '$y=0$', ha='left', va='bottom', fontsize=9, color=fs.GRAY)
    darrow(ax, (xs[1] + 0.75, y0), (xs[1] + 0.75, yeq), r'$\Delta\ell=\dfrac{mg}{k}$', off=(0.65, 0), fontsize=9)
    darrow(ax, (xs[2] + 0.62, yeq), (xs[2] + 0.62, yeq - yp), r"$y'$", off=(0.25, 0), fontsize=10)
    # (나)의 힘
    cb = yeq - 0.3
    fs.arrow(ax, (xs[1] - 0.25, cb + 0.3), (xs[1] - 0.25, cb + 1.1), color=fs.FORCE, lw=1.5)
    ax.text(xs[1] - 0.35, cb + 0.7, r'$k\Delta\ell$', color=fs.FORCE, ha='right', fontsize=10)
    fs.arrow(ax, (xs[1], cb - 0.3), (xs[1], cb - 1.1), color=fs.FORCE, lw=1.5)
    ax.text(xs[1] + 0.1, cb - 0.95, '$mg$', color=fs.FORCE, ha='left', fontsize=10)
    # +y 방향
    fs.arrow(ax, (-0.15, 2.0), (-0.15, 1.2), color=fs.BLACK, lw=1.0, ms=9)
    ax.text(-0.05, 1.6, '$+y$', fontsize=9, ha='left', va='center')
    fs.save(fig, F, 'fig15_03')


# ---------------------------------------------------------------- 예제 15.3 레너드-존스 퍼텐셜
def fig04():
    fig, ax = fs.plot_axes(4.2, 2.8)
    r = np.linspace(0.96, 2.6, 600)
    U = 4 * (r ** -12 - r ** -6)
    r0 = 2 ** (1 / 6)
    k = 72 / r0 ** 2
    ax.plot(r, U, color=fs.VEL, lw=1.6, label='$U(r)$')
    rp = np.linspace(r0 - 0.28, r0 + 0.28, 200)
    ax.plot(rp, -1 + 0.5 * k * (rp - r0) ** 2, color=fs.FORCE, ls='--', lw=1.3,
            label=r'$U(r_0)+\frac{1}{2}k_{\mathrm{eff}}(r-r_0)^2$')
    ax.axhline(0, color=fs.GRAY, lw=0.7)
    ax.plot([r0], [-1], 'o', color=fs.BLACK, ms=4)
    ax.plot([r0, r0], [-1.25, -1], color=fs.GRAY, lw=0.7, ls=':')
    ax.annotate(r'$r_0=2^{1/6}\sigma$', (r0, -1), (1.42, -0.88), fontsize=9,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.set_xlim(0.95, 2.6); ax.set_ylim(-1.25, 1.5)
    ax.set_xlabel(r'$r/\sigma$'); ax.set_ylabel(r'$U/\varepsilon$')
    ax.set_yticks([-1, 0, 1])
    ax.legend(fontsize=8, loc='upper right', frameon=False)
    fs.save(fig, F, 'fig15_04')


# ---------------------------------------------------------------- 15.2 에너지 그래프
def fig05():
    fig, ax = fs.canvas(4.2, 2.8)
    x = np.linspace(-1.25, 1.25, 400)
    ax.plot(x, x ** 2, color=fs.VEL, lw=1.6)
    ax.plot([-1.3, 1.3], [1, 1], color=fs.BLACK, lw=1.2)
    ax.text(1.32, 1.0, r'$E=\frac{1}{2}kA^2$', va='center', fontsize=10)
    ax.text(-1.3, 1.45, r'$U=\frac{1}{2}kx^2$', color=fs.VEL, fontsize=10, ha='right')
    fs.arrow(ax, (-1.45, 0), (1.55, 0), color=fs.BLACK, lw=0.9, ms=8)
    fs.arrow(ax, (0, -0.05), (0, 1.65), color=fs.BLACK, lw=0.9, ms=8)
    ax.text(1.58, -0.02, '$x$', va='center', fontsize=10)
    ax.text(0.05, 1.67, '에너지', va='bottom', fontsize=9)
    for s in (-1, 1):
        dline(ax, (s, 0), (s, 1))
        ax.text(s, -0.1, '$-A$' if s < 0 else '$A$', ha='center', va='top', fontsize=10)
    ax.text(0, -0.1, '$0$', ha='center', va='top', fontsize=10)
    xp = 0.6
    ax.plot([xp, xp], [0, xp ** 2], color=fs.VEL, lw=3.5, solid_capstyle='butt', alpha=0.6)
    ax.plot([xp, xp], [xp ** 2, 1], color=fs.FORCE, lw=3.5, solid_capstyle='butt', alpha=0.6)
    ax.text(xp + 0.07, xp ** 2 / 2, '$U$', color=fs.VEL, va='center', fontsize=10)
    ax.text(xp + 0.07, (1 + xp ** 2) / 2, '$K$', color=fs.FORCE, va='center', fontsize=10)
    ax.text(xp, -0.1, '$x$', ha='center', va='top', fontsize=10)
    for s in (-1, 1):
        ax.text(s, -0.32, '(되돌이점)', fontsize=8, color=fs.GRAY, ha='center', va='top')
    ax.set_xlim(-2.1, 2.3); ax.set_ylim(-0.5, 1.8)
    fs.save(fig, F, 'fig15_05')


# ---------------------------------------------------------------- 예제 15.4 U자관
def fig06():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-2.5, 2.2), ylim=(-1.6, 2.6))
    ri, ro = 0.8, 1.2          # 관 안쪽/바깥쪽 굽은 반지름 (관 중심선 반지름 1.0)
    H = 2.2
    th = np.linspace(np.pi, 2 * np.pi, 100)
    h0 = 1.0                   # 평형 액면 높이
    y = 0.45
    # 액체 채우기
    liq = '#9cc3e6'
    ax.fill_between(np.cos(th) * ro, np.sin(th) * ro, 0, color=liq, lw=0)
    ax.add_patch(Polygon(np.c_[np.r_[ri * np.cos(th)], np.r_[ri * np.sin(th)]], closed=True, fc='white', ec='none', zorder=1))
    ax.add_patch(Rectangle((-ro, -0.03), ro - ri, h0 - y + 0.03, fc=liq, ec='none', zorder=1))
    ax.add_patch(Rectangle((ri, -0.03), ro - ri, h0 + y + 0.03, fc=liq, ec='none', zorder=1))
    # 관 벽
    for r in (ri, ro):
        ax.plot(r * np.cos(th), r * np.sin(th), color=fs.BLACK, lw=1.2, zorder=3)
        ax.plot([-r, -r], [0, H], color=fs.BLACK, lw=1.2, zorder=3)
        ax.plot([r, r], [0, H], color=fs.BLACK, lw=1.2, zorder=3)
    dline(ax, (-1.6, h0), (2.0, h0))
    ax.text(-2.45, h0, '평형\n액면', fontsize=8, va='center', ha='left', color=fs.GRAY)
    darrow(ax, (1.45, h0), (1.45, h0 + y), '$y$', off=(0.18, 0))
    darrow(ax, (-1.4 + 0.0, h0), (-1.4, h0 - y), '$y$', off=(-0.18, 0))
    ax.text(0, -1.45, r'액체 기둥 전체 길이 $L$, 밀도 $\rho$', ha='center', fontsize=8)
    ax.text(1.0, H + 0.12, '단면적 $A$', ha='center', fontsize=8)
    fs.save(fig, F, 'fig15_06')


# ---------------------------------------------------------------- 15.3 단진자
def fig07():
    fig, ax = fs.canvas(3.4, 3.4, xlim=(-1.9, 2.3), ylim=(-3.55, 0.5))
    L = 2.6
    th = np.radians(25)
    O = np.array([0.0, 0.0])
    P = O + L * np.array([np.sin(th), -np.cos(th)])
    fs.ceiling(ax, -0.6, 0.6, 0.0)
    dline(ax, O, (0, -L - 0.3))
    ax.plot([O[0], P[0]], [O[1], P[1]], color=fs.BLACK, lw=1.1)
    fs.angle_arc(ax, O, 0.7, -90, -90 + 25, r'$\theta$', tr=0.95)
    ax.text(P[0] / 2 + 0.12, P[1] / 2 + 0.05, '$L$', fontsize=10)
    a = np.linspace(-np.radians(35), np.radians(35), 100)
    ax.plot(L * np.sin(a), -L * np.cos(a), color=fs.GRAY, lw=0.7, ls=':')
    ax.add_patch(Circle(P, 0.16, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=6))
    ax.text(P[0] + 0.22, P[1] + 0.18, '$m$', fontsize=10)
    # 힘
    u = (O - P) / L
    fs.vec(ax, P, 0.95 * u, color=fs.FORCE, lw=1.6)
    ax.text(P[0] + 0.95 * u[0] - 0.22, P[1] + 0.95 * u[1], r'$\vec T$', color=fs.FORCE, fontsize=10, va='center')
    mg = 1.2
    fs.vec(ax, P, (0, -mg), color=fs.FORCE, lw=1.6)
    ax.text(P[0] + 0.08, P[1] - mg - 0.12, r'$m\vec g$', color=fs.FORCE, fontsize=10, va='top')
    tang = np.array([-np.cos(th), -np.sin(th)])   # 복원 방향(θ 감소)
    radial = np.array([np.sin(th), -np.cos(th)])
    ft = mg * np.sin(th) * tang; fr = mg * np.cos(th) * radial
    fs.vec(ax, P, ft, color=fs.FORCE, lw=1.1, ls='--')
    fs.vec(ax, P, fr, color=fs.FORCE, lw=1.1, ls='--')
    ax.plot([P[0] + ft[0], P[0] - 0 + ft[0] + fr[0]], [P[1] + ft[1], P[1] + ft[1] + fr[1]], color=fs.GRAY, lw=0.5, ls=':')
    ax.plot([P[0] + fr[0], P[0] + fr[0] + ft[0]], [P[1] + fr[1], P[1] + fr[1] + ft[1]], color=fs.GRAY, lw=0.5, ls=':')
    ax.text(P[0] + ft[0] - 0.02, P[1] + ft[1] + 0.12, r'$mg\sin\theta$', color=fs.FORCE, fontsize=9, ha='right', va='bottom')
    ax.text(P[0] + fr[0] + 0.1, P[1] + fr[1], r'$mg\cos\theta$', color=fs.FORCE, fontsize=9, ha='left', va='center')
    ax.text(-0.12, -0.2, '$O$', fontsize=10, ha='right')
    fs.save(fig, F, 'fig15_07')


# ---------------------------------------------------------------- 15.3 물리진자
def fig08():
    fig, ax = fs.canvas(3.2, 3.4, xlim=(-1.4, 2.4), ylim=(-3.1, 0.75))
    th = np.radians(22)
    d = 1.5
    O = np.array([0.0, 0.0])
    C = O + d * np.array([np.sin(th), -np.cos(th)])
    # 불규칙한 강체: 매끈한 닫힌 곡선
    s = np.linspace(0, 2 * np.pi, 300)
    rr = 1.0 + 0.1 * np.cos(2 * s) - 0.06 * np.sin(3 * s)
    loc = np.c_[0.95 * rr * np.cos(s), 1.95 * rr * np.sin(s)]
    ang = th
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    pts = loc @ R.T + C + np.array([0.0, 0.0])
    ax.add_patch(Polygon(pts, closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2))
    dline(ax, O, (0, -2.4), zorder=3)
    ax.plot([O[0], C[0]], [O[1], C[1]], color=fs.BLACK, lw=1.0, zorder=4)
    ax.add_patch(Circle(O, 0.07, fc='white', ec=fs.BLACK, lw=1.2, zorder=6))
    ax.text(0.15, 0.06, '$O$ (축)', fontsize=9, ha='left')
    fs.dot(ax, C, r=0.06)
    ax.text(C[0] + 0.12, C[1] + 0.05, 'CM', fontsize=9)
    ax.text((O[0] + C[0]) / 2 + 0.12, (O[1] + C[1]) / 2 + 0.05, '$d$', fontsize=10, zorder=7)
    fs.angle_arc(ax, O, 0.55, -90, -90 + 22, r'$\theta$', tr=0.78)
    fs.vec(ax, C, (0, -1.1), color=fs.FORCE, lw=1.6)
    ax.text(C[0] + 0.1, C[1] - 1.05, r'$M\vec g$', color=fs.FORCE, fontsize=10, va='top')
    fs.save(fig, F, 'fig15_08')


# ---------------------------------------------------------------- 예제 15.5 T(d)
def fig09():
    fig, ax = fs.plot_axes(4.0, 2.7)
    g, L = 9.8, 1.0
    d = np.linspace(0.04, 0.5, 400)
    T = 2 * np.pi * np.sqrt((L ** 2 / 12 + d ** 2) / (g * d))
    ax.plot(d, T, color=fs.VEL, lw=1.6)
    dm = L / np.sqrt(12)
    Tm = 2 * np.pi * np.sqrt(2 * dm / g)
    ax.plot([dm], [Tm], 'o', color=fs.FORCE, ms=4)
    ax.annotate(f'최소: $d=L/\\sqrt{{12}}=0.289$ m\n$T_{{\\min}}={Tm:.2f}$ s', (dm, Tm), (0.2, 2.2), fontsize=8,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    Te = 2 * np.pi * np.sqrt(2 * L / (3 * g))
    ax.plot([0.5], [Te], 'o', color=fs.BLACK, ms=4)
    ax.annotate(f'끝 축 $d=L/2$\n$T={Te:.2f}$ s', (0.5, Te), (0.39, 1.8), fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.set_xlim(0, 0.52); ax.set_ylim(1.3, 2.7)
    ax.set_xlabel('축과 질량중심 사이 거리 $d$ (m)', fontsize=9)
    ax.set_ylabel('주기 $T$ (s)', fontsize=9)
    ax.tick_params(labelsize=8)
    fs.save(fig, F, 'fig15_09')


# ---------------------------------------------------------------- 15.4 기준원
def fig10():
    fig, ax = fs.canvas(3.6, 3.4, xlim=(-1.75, 2.1), ylim=(-1.75, 1.7))
    A = 1.2
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(A * np.cos(t), A * np.sin(t), color=fs.GRAY, lw=1.0)
    fs.arrow(ax, (-1.6, 0), (1.95, 0), color=fs.BLACK, lw=0.9, ms=8)
    fs.arrow(ax, (0, -1.4), (0, 1.6), color=fs.BLACK, lw=0.9, ms=8)
    ax.text(1.98, -0.02, '$x$', va='center', fontsize=10)
    ax.text(0.06, 1.6, '$y$', va='center', fontsize=10)
    th = np.radians(35)
    P = A * np.array([np.cos(th), np.sin(th)])
    ax.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=1.3)
    ax.text(0.33, 0.43, '$A$', fontsize=10)
    fs.angle_arc(ax, (0, 0), 0.3, 0, 35, r'$\omega t+\phi$', tr=0.6, fontsize=9)
    dline(ax, P, (P[0], 0), color=fs.BLACK, lw=0.7, ls=':')
    # 속도와 가속도
    vdir = np.array([-np.sin(th), np.cos(th)])
    fs.vec(ax, P, 0.6 * vdir, color=fs.VEL, lw=1.5)
    ax.text(P[0] + 0.6 * vdir[0] + 0.08, P[1] + 0.6 * vdir[1] + 0.06, r'$\vec v$', color=fs.VEL, fontsize=10, ha='left')
    fs.vec(ax, P, -0.48 * P / A, color=fs.ACC, lw=1.8, zorder=6)
    ax.text(0.6, 0.7, r'$\vec a$', color=fs.ACC, fontsize=10, ha='left', va='center')
    fs.dot(ax, P, r=0.055)
    ax.text(P[0] + 0.1, P[1] + 0.08, '$P$', fontsize=10)
    Q = (P[0], 0)
    ax.add_patch(Circle(Q, 0.06, fc=fs.ORANGE, ec=fs.BLACK, lw=0.6, zorder=7))
    ax.text(P[0] + 0.05, -0.15, r'$x=A\cos(\omega t+\phi)$', fontsize=9, color=fs.ORANGE, va='top', ha='center')
    darrow(ax, (-A, -1.38), (A, -1.38), None, color=fs.ORANGE)
    ax.text(0, -1.5, '그림자는 $-A$와 $A$ 사이를 단조화 운동', fontsize=8, color=fs.ORANGE, ha='center', va='top')
    for s_ in (-1, 1):
        dline(ax, (s_ * A, 0), (s_ * A, -1.38), color=fs.ORANGE, lw=0.5, ls=':')
    fs.arrow(ax, (A * np.cos(1.75), A * np.sin(1.75)), (A * np.cos(2.05), A * np.sin(2.05)), color=fs.GRAY, lw=0.8, ms=8)
    ax.text(-0.72, 1.22, r'$\omega$', fontsize=10, color=fs.GRAY)
    fs.save(fig, F, 'fig15_10')


# ---------------------------------------------------------------- 15.4 페이저
def fig11():
    fig, ax = fs.canvas(3.6, 3.3, xlim=(-2.0, 2.0), ylim=(-1.75, 1.85))
    fs.arrow(ax, (-1.9, 0), (1.9, 0), color=fs.BLACK, lw=0.9, ms=8)
    fs.arrow(ax, (0, -1.7), (0, 1.75), color=fs.BLACK, lw=0.9, ms=8)
    ax.text(1.9, -0.13, 'Re', fontsize=9, ha='right', va='top')
    ax.text(0.08, 1.75, 'Im', fontsize=9, va='top')
    th = np.radians(35)
    w = 1.25
    A = 1.0
    z = A * np.array([np.cos(th), np.sin(th)])
    vz = w * A * np.array([np.cos(th + np.pi / 2), np.sin(th + np.pi / 2)])
    az = w ** 2 * A * np.array([np.cos(th + np.pi), np.sin(th + np.pi)])
    fs.vec(ax, (0, 0), z, color=fs.BLACK, lw=1.8)
    fs.vec(ax, (0, 0), vz, color=fs.VEL, lw=1.8)
    fs.vec(ax, (0, 0), az, color=fs.ACC, lw=1.8)
    ax.text(z[0] + 0.08, z[1] + 0.05, r'$\tilde z=\tilde Ae^{i\omega t}$', fontsize=10)
    ax.text(vz[0] - 0.05, vz[1] + 0.08, r'$i\omega\tilde z$ (속도)', fontsize=9, color=fs.VEL, ha='center', va='bottom')
    ax.text(az[0] - 0.05, az[1] - 0.12, r'$-\omega^2\tilde z$ (가속도)', fontsize=9, color=fs.ACC, ha='center', va='top')
    fs.angle_arc(ax, (0, 0), 0.32, 0, 35, r'$\omega t+\phi$', tr=0.6, fontsize=8)
    fs.angle_arc(ax, (0, 0), 0.22, 35, 125, None, color=fs.VEL)
    ax.text(0.04, 0.33, '90°', fontsize=8, color=fs.VEL)
    dline(ax, z, (z[0], 0), color=fs.BLACK, lw=0.7, ls=':')
    ax.plot([z[0]], [0], 'o', color=fs.ORANGE, ms=4, zorder=7)
    ax.text(z[0], -0.08, r'$x=\mathrm{Re}\,\tilde z$', fontsize=8, color=fs.ORANGE, ha='left', va='top')
    fs.save(fig, F, 'fig15_11')


# ---------------------------------------------------------------- 15.5 감쇠 진동
def fig12():
    fig, ax = fs.plot_axes(5.0, 2.8)
    t = np.linspace(0, 30, 2000)
    w0 = 1.0
    # 약한 감쇠 beta=0.1, x(0)=1, v(0)=0
    b = 0.1; wd = np.sqrt(w0 ** 2 - b ** 2)
    xu = np.exp(-b * t) * (np.cos(wd * t) + b / wd * np.sin(wd * t))
    Ap = np.sqrt(1 + (b / wd) ** 2)
    # 임계 감쇠 beta=1
    xc = (1 + t) * np.exp(-t)
    # 과감쇠 beta=2
    b2 = 2.0; s1 = -b2 + np.sqrt(b2 ** 2 - 1); s2 = -b2 - np.sqrt(b2 ** 2 - 1)
    C1 = -s2 / (s1 - s2); C2 = 1 - C1
    xo = C1 * np.exp(s1 * t) + C2 * np.exp(s2 * t)
    ax.plot(t, Ap * np.exp(-b * t), color=fs.VEL, lw=0.8, ls='--')
    ax.plot(t, -Ap * np.exp(-b * t), color=fs.VEL, lw=0.8, ls='--')
    ax.plot(t, xu, color=fs.VEL, lw=1.4, label=r'약한 감쇠 ($\beta=0.1\,\omega_0$)')
    ax.plot(t, xc, color=fs.FORCE, lw=1.6, label=r'임계 감쇠 ($\beta=\omega_0$)')
    ax.plot(t, xo, color=fs.ACC, lw=1.6, label=r'과감쇠 ($\beta=2\,\omega_0$)')
    ax.text(13, 0.36, r'포락선 $\pm A e^{-\beta t}$', color=fs.VEL, fontsize=8)
    ax.axhline(0, color=fs.GRAY, lw=0.6)
    ax.set_xlim(0, 30); ax.set_ylim(-1.05, 1.1)
    ax.set_xlabel(r'$\omega_0 t$', fontsize=9); ax.set_ylabel(r'$x/x_0$', fontsize=9)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=8, loc='upper right', frameon=True, framealpha=0.9, edgecolor='none')
    fs.save(fig, F, 'fig15_12')


# ---------------------------------------------------------------- 15.6 공명 곡선과 위상
def fig13():
    import matplotlib.pyplot as plt
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.6, 3.5), sharex=True, gridspec_kw=dict(height_ratios=[1.6, 1]))
    w = np.linspace(0.01, 2.0, 3000)
    cols = [fs.ACC, fs.VEL, fs.FORCE]
    for Q, c in zip([2, 5, 20], cols):
        b = 1 / (2 * Q)
        A = 1 / np.sqrt((1 - w ** 2) ** 2 + 4 * b ** 2 * w ** 2)
        d = np.degrees(np.arctan2(2 * b * w, 1 - w ** 2))
        a1.plot(w, A, color=c, lw=1.4, label=f'$Q={Q}$')
        a2.plot(w, d, color=c, lw=1.4)
        wr = np.sqrt(1 - 2 * b ** 2)
        a1.plot([wr], [1 / np.sqrt((1 - wr ** 2) ** 2 + 4 * b ** 2 * wr ** 2)], 'o', color=c, ms=3)
    a1.set_yscale('log'); a1.set_ylim(0.2, 40)
    a1.set_yticks([0.3, 1, 3, 10, 30]); a1.set_yticklabels(['0.3', '1', '3', '10', '30'])
    a1.set_ylabel(r'$A\,k/F_0$', fontsize=9)
    a1.legend(fontsize=8, frameon=False, loc='upper right')
    a1.text(0.05, 0.6, r'$\omega\ll\omega_0$: $A\to F_0/k$', fontsize=8)
    a2.set_ylabel(r'위상 지연 $\delta$', fontsize=9)
    a2.set_yticks([0, 90, 180]); a2.set_yticklabels(['0°', '90°', '180°'])
    a2.set_ylim(-5, 185)
    a2.set_xlabel(r'$\omega/\omega_0$', fontsize=9)
    for a in (a1, a2):
        a.grid(True, lw=0.4, color='#d0d0d0')
        a.axvline(1, color=fs.GRAY, lw=0.7, ls=':')
        a.tick_params(labelsize=8)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    a2.set_xlim(0, 2)
    fig.align_ylabels([a1, a2])
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, F, 'fig15_13')


# ---------------------------------------------------------------- 15.6 흡수 일률과 반치폭
def fig14():
    fig, ax = fs.plot_axes(4.4, 2.7)
    w = np.linspace(0.01, 2.0, 4000)
    cols = [fs.ACC, fs.VEL, fs.FORCE]
    for Q, c in zip([2, 5, 20], cols):
        b = 1 / (2 * Q)
        P = b * w ** 2 / ((1 - w ** 2) ** 2 + 4 * b ** 2 * w ** 2)
        ax.plot(w, P / P.max(), color=c, lw=1.4, label=f'$Q={Q}$')
    b = 0.1
    wp = np.sqrt(b ** 2 + 1) + b; wm = np.sqrt(b ** 2 + 1) - b
    ax.annotate('', xy=(wm, 0.5), xytext=(wp, 0.5), arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.plot([wm, wm], [0.42, 0.58], color=fs.BLACK, lw=0.6); ax.plot([wp, wp], [0.42, 0.58], color=fs.BLACK, lw=0.6)
    ax.annotate(r'$\Delta\omega=2\beta=\omega_0/Q$', (wp, 0.5), (1.33, 0.8), fontsize=9,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.axhline(0.5, color=fs.GRAY, lw=0.6, ls=':')
    ax.axvline(1, color=fs.GRAY, lw=0.7, ls=':')
    ax.set_xlim(0, 2); ax.set_ylim(0, 1.08)
    ax.set_xlabel(r'$\omega/\omega_0$', fontsize=9)
    ax.set_ylabel(r'$\langle P\rangle/\langle P\rangle_{\max}$', fontsize=9)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    fs.save(fig, F, 'fig15_14')


# ---------------------------------------------------------------- ★ 결합 진동자
def fig15():
    fig, ax = fs.canvas(5.0, 3.1, xlim=(-0.3, 7.3), ylim=(-3.45, 1.25))
    def row(y0, d1=0.0, d2=0.0, k_labels=False):
        fs.wall(ax, y0 - 0.4, y0 + 0.5, x=0.0, side='left')
        fs.wall(ax, y0 - 0.4, y0 + 0.5, x=7.0, side='right')
        x1, x2 = 2.2 + d1, 4.8 + d2
        fs.spring(ax, (0, y0), (x1 - 0.35, y0), coils=6, width=0.12)
        fs.spring(ax, (x1 + 0.35, y0), (x2 - 0.35, y0), coils=6, width=0.12, color=fs.ORANGE)
        fs.spring(ax, (x2 + 0.35, y0), (7.0, y0), coils=6, width=0.12)
        fs.block(ax, (x1, y0), w=0.7, h=0.6, text='$m$', fontsize=10)
        fs.block(ax, (x2, y0), w=0.7, h=0.6, text='$m$', fontsize=10)
        if k_labels:
            ax.text((x1 - 0.35) / 2, y0 + 0.25, '$k$', ha='center', fontsize=10)
            ax.text((x1 + x2) / 2, y0 + 0.25, '$k_c$', ha='center', fontsize=10, color=fs.ORANGE)
            ax.text((x2 + 0.35 + 7) / 2, y0 + 0.25, '$k$', ha='center', fontsize=10)
        return x1, x2
    x1, x2 = row(0.4, k_labels=True)
    ax.text(x1, 1.0, '$x_1$', ha='center', fontsize=10); ax.text(x2, 1.0, '$x_2$', ha='center', fontsize=10)
    a, b = row(-1.1, 0.25, 0.25)
    fs.vec(ax, (a - 0.3, -1.1 + 0.45), (0.6, 0), color=fs.VEL, lw=1.4)
    fs.vec(ax, (b - 0.3, -1.1 + 0.45), (0.6, 0), color=fs.VEL, lw=1.4)
    ax.text(3.5, -1.75, r'모드 1: 같은 방향, $\omega_1=\sqrt{k/m}$', ha='center', fontsize=8.5)
    a, b = row(-2.65, 0.25, -0.25)
    fs.vec(ax, (a - 0.3, -2.65 + 0.45), (0.6, 0), color=fs.VEL, lw=1.4)
    fs.vec(ax, (b + 0.3, -2.65 + 0.45), (-0.6, 0), color=fs.VEL, lw=1.4)
    ax.text(3.5, -3.3, r'모드 2: 반대 방향, $\omega_2=\sqrt{(k+2k_c)/m}$', ha='center', fontsize=8.5)
    fs.save(fig, F, 'fig15_15')


# ---------------------------------------------------------------- 연습문제 7 병렬·직렬
def fig16():
    fig, ax = fs.canvas(5.0, 1.9, xlim=(-0.3, 8.2), ylim=(-0.75, 1.55))
    # 병렬
    fs.wall(ax, -0.2, 1.3, x=0.0, side='left')
    fs.ground(ax, 0.0, 3.6, y=-0.2)
    fs.block(ax, (2.8, 0.55), w=0.7, h=1.3, text='$m$')
    fs.spring(ax, (0, 0.95), (2.45, 0.95), coils=7, width=0.1)
    fs.spring(ax, (0, 0.15), (2.45, 0.15), coils=7, width=0.1)
    ax.text(1.2, 1.15, '$k_1$', ha='center', fontsize=10)
    ax.text(1.2, 0.35, '$k_2$', ha='center', fontsize=10)
    ax.text(1.7, -0.6, '(가) 병렬', ha='center', fontsize=9)
    # 직렬
    x0 = 4.3
    fs.wall(ax, -0.2, 1.3, x=x0, side='left')
    fs.ground(ax, x0, 8.1, y=-0.2)
    fs.spring(ax, (x0, 0.25), (x0 + 1.5, 0.25), coils=5, width=0.1)
    fs.spring(ax, (x0 + 1.5, 0.25), (x0 + 3.0, 0.25), coils=5, width=0.1)
    fs.dot(ax, (x0 + 1.5, 0.25), r=0.05)
    fs.block(ax, (x0 + 3.35, 0.25), w=0.7, h=0.9, text='$m$')
    ax.text(x0 + 0.75, 0.48, '$k_1$', ha='center', fontsize=10)
    ax.text(x0 + 2.25, 0.48, '$k_2$', ha='center', fontsize=10)
    ax.text(x0 + 1.8, -0.6, '(나) 직렬', ha='center', fontsize=9)
    fs.save(fig, F, 'fig15_16')


# ---------------------------------------------------------------- 연습문제 16 지구 터널
def fig17():
    fig, ax = fs.canvas(3.4, 3.2, xlim=(-1.55, 1.75), ylim=(-1.5, 1.6))
    R = 1.3
    ax.add_patch(Circle((0, 0), R, fc='#eef3ea', ec=fs.BLACK, lw=1.2))
    yc = 0.62                                  # 터널(현)의 높이
    xe = np.sqrt(R ** 2 - yc ** 2)
    ax.add_patch(Rectangle((-xe, yc - 0.05), 2 * xe, 0.1, fc='white', ec=fs.BLACK, lw=0.8, zorder=3))
    fs.dot(ax, (0, 0), r=0.04)
    ax.text(0.05, -0.12, '$O$', fontsize=10)
    ax.plot([0, 0], [0, yc], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([-0.09, -0.09, 0], [yc - 0.05, yc - 0.14, yc - 0.14], color=fs.GRAY, lw=0.6)
    sx = 0.62
    P = (sx, yc)
    ax.add_patch(Rectangle((sx - 0.08, yc - 0.06), 0.16, 0.12, fc=fs.ORANGE, ec=fs.BLACK, lw=0.7, zorder=5))
    fs.arrow(ax, (0, 0), (sx - 0.02, yc - 0.06), color=fs.BLACK, lw=1.1, ms=8)
    ax.text(sx / 2 + 0.1, yc / 2 - 0.05, r'$\vec r$', fontsize=10)
    darrow(ax, (0, yc + 0.17), (sx, yc + 0.17), '$s$', off=(0, 0.13))
    ax.text(sx + 0.05, yc - 0.2, '$m$', fontsize=9)
    ang = np.radians(-40)
    ax.plot([0, R * np.cos(ang)], [0, R * np.sin(ang)], color=fs.BLACK, lw=0.9)
    ax.text(R * np.cos(ang) / 2 + 0.1, R * np.sin(ang) / 2 + 0.08, '$R$', fontsize=10)
    ax.text(-xe - 0.05, yc + 0.17, '터널', fontsize=8, ha='left')
    fs.save(fig, F, 'fig15_17')


for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17):
    f()
