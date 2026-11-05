"""16장 역학적 파동 그림. 실행: python3 figures/ch16/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch, Arc

F = __file__


def dline(ax, p, q, color=fs.GRAY, lw=0.8, ls='--', zorder=1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=zorder)


def darrow(ax, p, q, text=None, color=fs.BLACK, off=(0, 0.12), fontsize=10, ms=8, lw=0.8, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=ms, color=color, lw=lw, zorder=5))
    if text:
        m = ((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1])
        ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color, **kw)


def pulse(x, c=0.0, w=0.45):
    return np.exp(-((x - c) / w) ** 2)


# ---------------------------------------------------------------- 16.1 횡파와 종파
def fig01():
    fig, ax = fs.canvas(5.0, 3.0, xlim=(-0.3, 8.3), ylim=(-2.85, 1.45))
    # (가) 횡파: 줄 위의 사인파
    x = np.linspace(0, 7.2, 400)
    k = 2 * np.pi / 3.2
    y = 0.45 * np.sin(k * x)
    ax.plot(x, y + 0.6, color=fs.BLACK, lw=1.4)
    # 매질 점의 속도: y = A sin(kx - wt) → u = -wA cos(kx)
    for xi in np.arange(0.4, 7.0, 0.8):
        yi = 0.45 * np.sin(k * xi) + 0.6
        u = -np.cos(k * xi) * 0.38
        ax.add_patch(Circle((xi, yi), 0.06, color=fs.ORANGE, zorder=6))
        if abs(u) > 0.06:
            fs.vec(ax, (xi, yi), (0, u), color=fs.VEL, lw=1.2, ms=8)
    fs.arrow(ax, (7.35, 0.6), (8.2, 0.6), color=fs.BLACK, lw=1.4)
    ax.text(7.75, 0.78, '진행', ha='center', fontsize=8)
    ax.text(0.0, 1.35, '(가) 횡파: 매질은 진행 방향에 수직으로 진동', fontsize=9, va='center')
    # (나) 종파: 입자 위치가 소밀
    y0 = -1.65
    xe = np.arange(0.0, 7.21, 0.16)
    s = 0.12 * np.cos(k * xe)                     # 변위 s = s_m cos(kx) (t = 0)
    for xi, si in zip(xe, s):
        ax.plot([xi + si, xi + si], [y0 - 0.45, y0 + 0.45], color=fs.BLACK, lw=1.0)
    for xi in np.arange(0.4, 7.0, 0.8):
        u = np.sin(k * xi) * 0.38                 # u = ds/dt = w s_m sin(kx) (t = 0)
        if abs(u) > 0.06:
            fs.vec(ax, (xi + 0.12 * np.cos(k * xi) - u / 2, y0 + 0.62), (u, 0), color=fs.VEL, lw=1.2, ms=8)
    fs.arrow(ax, (7.35, y0), (8.2, y0), color=fs.BLACK, lw=1.4)
    ax.text(7.75, y0 + 0.18, '진행', ha='center', fontsize=8)
    ax.text(0.0, -0.55, '(나) 종파: 매질은 진행 방향과 나란히 진동', fontsize=9, va='center')
    for xc, lab in ((0.8, '밀'), (2.4, '소'), (4.0, '밀'), (5.6, '소')):
        ax.text(xc, y0 - 0.65, lab, ha='center', fontsize=8, color=fs.GRAY)
    fs.save(fig, F, 'fig16_01')


# ---------------------------------------------------------------- 16.2 진행 펄스
def fig02():
    fig, ax = fs.canvas(4.6, 1.9, xlim=(-1.6, 6.4), ylim=(-0.55, 1.6))
    x = np.linspace(-1.5, 6.3, 500)
    c0, c1 = 0.8, 3.8
    ax.plot(x, pulse(x, c0, 0.55), color=fs.GRAY, lw=1.3, ls='--')
    ax.plot(x, pulse(x, c1, 0.55), color=fs.VEL, lw=1.6)
    fs.arrow(ax, (-1.5, 0), (6.3, 0), color=fs.BLACK, lw=0.8, ms=8)
    ax.text(6.3, -0.15, '$x$', ha='right', va='top', fontsize=10)
    ax.text(c0, 1.12, '$t=0$\n$y=f(x)$', ha='center', va='bottom', fontsize=9, color=fs.GRAY)
    ax.text(c1, 1.12, '시각 $t$\n$y=f(x-vt)$', ha='center', va='bottom', fontsize=9, color=fs.VEL)
    darrow(ax, (c0, 0.5), (c1, 0.5), '$vt$', off=(0, 0.13))
    fs.arrow(ax, (c1 + 0.9, 0.75), (c1 + 1.7, 0.75), color=fs.VEL, lw=1.4)
    ax.text(c1 + 1.3, 0.92, '$v$', color=fs.VEL, fontsize=10, ha='center')
    for c in (c0, c1):
        dline(ax, (c, 0), (c, 1.0), lw=0.6, ls=':')
    fs.save(fig, F, 'fig16_02')


# ---------------------------------------------------------------- 16.2 사인파 (예제 16.1)
def fig03():
    ym, k, w = 20.0, 2.0, 30.0           # mm, rad/m, rad/s
    lam, T = 2 * np.pi / k, 2 * np.pi / w
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 3.4))
    x = np.linspace(0, 7.5, 600)
    a1.plot(x, ym * np.sin(k * x - w * T / 8), color=fs.GRAY, lw=1.0, ls='--', label='$t=T/8$')
    a1.plot(x, ym * np.sin(k * x), color=fs.VEL, lw=1.6, label='$t=0$')
    a1.set_xlabel('$x$ (m)', fontsize=9, labelpad=1)
    a1.set_ylabel('$y$ (mm)', fontsize=9)
    xp = lam / 4
    a1.annotate('', xy=(xp + lam, 27), xytext=(xp, 27), arrowprops=dict(arrowstyle='<|-|>', lw=0.8, mutation_scale=7))
    a1.text(xp + lam / 2, 30, rf'$\lambda={lam:.2f}$ m', ha='center', va='bottom', fontsize=8)
    a1.annotate('', xy=(9 * lam / 4, ym), xytext=(9 * lam / 4, 0), arrowprops=dict(arrowstyle='<|-|>', lw=0.8, mutation_scale=7))
    a1.text(9 * lam / 4 + 0.1, 7, '$y_m$', fontsize=9, va='center')
    a1.annotate('', xy=(6.9, -27), xytext=(6.1, -27), arrowprops=dict(arrowstyle='-|>', color=fs.VEL, lw=1.2, mutation_scale=9))
    a1.text(6.0, -27, '$v$', color=fs.VEL, ha='right', va='center', fontsize=9)
    a1.set_ylim(-36, 42); a1.set_xlim(0, 7.5)
    a1.legend(fontsize=7, loc='upper right', frameon=False, ncol=2, bbox_to_anchor=(1.0, 1.12))
    a1.text(-0.12, 1.02, '(가)', transform=a1.transAxes, fontsize=9)
    t = np.linspace(0, 0.5, 600)
    a2.plot(t, ym * np.sin(-w * t), color=fs.FORCE, lw=1.6)
    tp = 3 * T / 4
    a2.annotate('', xy=(tp + T, 27), xytext=(tp, 27), arrowprops=dict(arrowstyle='<|-|>', lw=0.8, mutation_scale=7))
    a2.text(tp + T / 2, 30, rf'$T={T:.2f}$ s', ha='center', va='bottom', fontsize=8)
    a2.set_xlabel('$t$ (s)', fontsize=9, labelpad=1)
    a2.set_ylabel('$y$ (mm)', fontsize=9)
    a2.set_ylim(-36, 42); a2.set_xlim(0, 0.5)
    a2.text(-0.12, 1.02, '(나)', transform=a2.transAxes, fontsize=9)
    for a in (a1, a2):
        a.axhline(0, color=fs.GRAY, lw=0.6)
        a.grid(True, lw=0.4, color='#d0d0d0')
        a.tick_params(labelsize=8)
        a.set_yticks([-20, 0, 20])
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    fig.tight_layout(h_pad=0.6)
    fs.save(fig, F, 'fig16_03')


# ---------------------------------------------------------------- 16.3 펄스 기준틀의 줄 조각
def fig04():
    fig, ax = fs.canvas(4.4, 3.0, xlim=(-3.3, 3.3), ylim=(-0.45, 3.3))
    R = 2.0
    th = np.radians(24)
    C = np.array([0.0, 0.6])
    # 펄스 전체 모양(배경): 꼭대기가 원호와 맞닿는 매끈한 곡선
    xx = np.linspace(-3.2, 3.2, 400)
    top = C[1] + R
    yy = C[1] + (top - C[1]) * 0 + (top - 0.15) * np.exp(-(xx / 1.25) ** 2) + 0.15
    ax.plot(xx, yy, color='#b8c4d0', lw=1.2, zorder=1)
    a = np.linspace(np.pi / 2 - th, np.pi / 2 + th, 100)
    ax.plot(C[0] + R * np.cos(a), C[1] + R * np.sin(a), color=fs.BLACK, lw=2.6, zorder=3)
    L = C + R * np.array([np.cos(np.pi / 2 + th), np.sin(np.pi / 2 + th)])
    Rt = C + R * np.array([np.cos(np.pi / 2 - th), np.sin(np.pi / 2 - th)])
    dline(ax, C, L); dline(ax, C, Rt); dline(ax, C, C + np.array([0, R]), ls=':')
    fs.dot(ax, C, r=0.04)
    ax.text(C[0] + 0.1, C[1] - 0.1, '원의 중심', fontsize=8, va='top', color=fs.GRAY)
    fs.angle_arc(ax, C, 0.55, 90, 90 + 24, r'$\theta$', fontsize=9, tr=0.75)
    fs.angle_arc(ax, C, 0.55, 90 - 24, 90, r'$\theta$', fontsize=9, tr=0.75)
    ax.text(C[0] - 0.6, C[1] + 0.85, '$R$', fontsize=10)
    # 장력
    tl = np.array([-np.cos(th), -np.sin(th)]); tr = np.array([np.cos(th), -np.sin(th)])
    fs.vec(ax, L, 1.15 * tl, color=fs.FORCE, lw=1.6)
    fs.vec(ax, Rt, 1.15 * tr, color=fs.FORCE, lw=1.6)
    ax.text(L[0] + 1.15 * tl[0] - 0.05, L[1] + 1.15 * tl[1] + 0.1, r'$\tau$', color=fs.FORCE, fontsize=11, ha='right')
    ax.text(Rt[0] + 1.15 * tr[0] + 0.05, Rt[1] + 1.15 * tr[1] + 0.1, r'$\tau$', color=fs.FORCE, fontsize=11, ha='left')
    # 수평선과 장력 사이 각
    dline(ax, L, L + np.array([-0.9, 0]), ls=':')
    fs.angle_arc(ax, L, 0.55, 180, 180 + 24, r'$\theta$', fontsize=9, tr=0.75)
    # 알짜 힘
    P = C + np.array([0, R])
    fs.vec(ax, P + np.array([0, -0.08]), (0, -0.9), color=fs.FORCE, lw=2.0)
    ax.text(P[0] + 0.1, P[1] - 0.95, r'$F_{\mathrm{net}}=2\tau\sin\theta$', color=fs.FORCE, fontsize=9, ha='left', va='center', bbox=dict(fc='white', ec='none', pad=0.3), zorder=8)
    ax.text(P[0], P[1] + 0.15, r'$\Delta\ell$', ha='center', va='bottom', fontsize=10)
    fs.arrow(ax, (1.9, 3.1), (0.9, 3.1), color=fs.VEL, lw=1.4)
    ax.text(2.0, 3.1, '$v$ (줄이 흐르는 방향)', color=fs.VEL, fontsize=8, va='center')
    fs.save(fig, F, 'fig16_04')


# ---------------------------------------------------------------- 16.4 에너지
def fig05():
    fig, ax = fs.canvas(4.8, 2.3, xlim=(-0.3, 7.8), ylim=(-1.55, 1.45))
    k = 2 * np.pi / 4.0
    x = np.linspace(0, 7.0, 500)
    A = 0.8
    ax.plot(x, A * np.sin(k * x), color=fs.BLACK, lw=1.4)
    ax.plot([0, 7.0], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    for xi in np.arange(0.25, 7.0, 0.5):
        u = -np.cos(k * xi) * 0.55
        yi = A * np.sin(k * xi)
        if abs(u) > 0.05:
            fs.vec(ax, (xi, yi), (0, u), color=fs.VEL, lw=1.1, ms=7)
    # 강조 조각
    for xc, col in ((4.0, fs.FORCE), (5.0, fs.GRAY)):
        xs = np.linspace(xc - 0.18, xc + 0.18, 30)
        ax.plot(xs, A * np.sin(k * xs), color=col, lw=4.0, alpha=0.55, solid_capstyle='round')
    ax.annotate('$y=0$: 가장 빠르고 가장 기울어짐\n$dK$, $dU$ 모두 최대', (4.05, -0.05), (4.35, -1.2), fontsize=8, color=fs.FORCE,
                arrowprops=dict(arrowstyle='-', color=fs.FORCE, lw=0.6), va='center')
    ax.text(5.0, A + 0.2, '마루: 정지, 기울기 0, $dK=dU=0$', fontsize=8, color=fs.GRAY, ha='center', va='bottom')
    fs.arrow(ax, (7.05, 0.0), (7.75, 0.0), color=fs.BLACK, lw=1.3)
    ax.text(7.4, 0.15, '$v$', ha='center', fontsize=10)
    ax.text(0.0, -1.3, r'파랑 화살표: 가로 속도 $u=\partial y/\partial t$', fontsize=8, color=fs.VEL, va='center')
    fs.save(fig, F, 'fig16_05')


# ---------------------------------------------------------------- 16.5 파동 방정식 유도
def fig06():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.2, 6.2), ylim=(-0.7, 3.0))
    f = lambda x: 0.9 + 0.22 * (x - 3.0) ** 2
    fp = lambda x: 0.44 * (x - 3.0)
    x = np.linspace(0.4, 5.6, 300)
    ax.plot(x, f(x), color='#b8c4d0', lw=1.2)
    x1, x2 = 1.9, 4.4
    xs = np.linspace(x1, x2, 100)
    ax.plot(xs, f(xs), color=fs.BLACK, lw=2.4)
    for xi, sgn, lab in ((x1, -1, 'x'), (x2, 1, 'x+dx')):
        yi = f(xi); s = fp(xi)
        d = sgn * np.array([1, s]) / np.hypot(1, s)
        fs.vec(ax, (xi, yi), 1.15 * d, color=fs.FORCE, lw=1.6)
        ax.text(xi + 1.15 * d[0] + sgn * 0.08, yi + 1.15 * d[1] + 0.05, r'$\tau$', color=fs.FORCE, fontsize=11,
                ha='left' if sgn > 0 else 'right')
        dline(ax, (xi, yi), (xi + sgn * 1.0, yi), ls=':')
        # 가로 성분
        fs.vec(ax, (xi + sgn * 0.08, yi), (0, 1.15 * d[1]), color=fs.FORCE, lw=0.9, ls='--', ms=8)
        dline(ax, (xi, -0.1), (xi, yi), ls=':', lw=0.6)
        ax.text(xi, -0.15, f'${lab}$', ha='center', va='top', fontsize=10)
    ax.text(x2 - 0.1, f(x2) + 0.75, r'$+\tau\left.\frac{\partial y}{\partial x}\right|_{x+dx}$', fontsize=9, color=fs.FORCE, ha='right', va='center')
    ax.text(x1 + 0.1, f(x1) + 0.55, r'$-\tau\left.\frac{\partial y}{\partial x}\right|_{x}$', fontsize=9, color=fs.FORCE, ha='left', va='center')
    fs.arrow(ax, (0, 0), (6.0, 0), color=fs.BLACK, lw=0.8, ms=8)
    ax.text(3.0, 0.45, r'질량 $\mu\,dx$', ha='center', fontsize=9)
    ax.text(6.0, -0.12, '$x$', ha='right', va='top', fontsize=10)
    fs.save(fig, F, 'fig16_06')


# ---------------------------------------------------------------- ★ 달랑베르 해: 펄스가 둘로 갈라짐
def fig07():
    fig, ax = fs.canvas(4.6, 2.9, xlim=(-4.6, 4.8), ylim=(-0.4, 5.2))
    x = np.linspace(-4.5, 4.5, 600)
    w = 0.6
    for i, (vt, lab) in enumerate(((0.0, '$t=0$'), (0.55, '$t_1$'), (2.4, '$t_2$'))):
        y0 = 3.6 - 1.75 * i
        y = 0.5 * (pulse(x, -vt, w) + pulse(x, vt, w))
        ax.plot(x, y0 + 1.1 * y, color=fs.VEL, lw=1.5)
        ax.plot([-4.5, 4.5], [y0, y0], color=fs.GRAY, lw=0.5)
        ax.text(-4.55, y0 + 0.3, lab, fontsize=9, ha='left')
        if i == 2:
            ax.plot(x, y0 + 1.1 * 0.5 * pulse(x, -vt, w), color=fs.VEL, lw=0)
            fs.arrow(ax, (vt + 0.3, y0 + 0.75), (vt + 1.1, y0 + 0.75), color=fs.BLACK, lw=1.2)
            fs.arrow(ax, (-vt - 0.3, y0 + 0.75), (-vt - 1.1, y0 + 0.75), color=fs.BLACK, lw=1.2)
            ax.text(vt + 0.7, y0 + 0.92, '$v$', ha='center', fontsize=9)
            ax.text(-vt - 0.7, y0 + 0.92, '$v$', ha='center', fontsize=9)
            ax.text(vt, y0 - 0.15, '$+vt_2$', ha='center', va='top', fontsize=8)
            ax.text(-vt, y0 - 0.15, '$-vt_2$', ha='center', va='top', fontsize=8)
        if i == 1:
            for s in (-1, 1):
                ax.plot(x, y0 + 1.1 * 0.5 * pulse(x, s * vt, w), color=fs.VEL, lw=0.8, ls=':')
    ax.text(4.75, 3.6 + 1.1, '높이 $h$', fontsize=8, ha='right', va='center', color=fs.GRAY)
    ax.text(4.75, 0.1 + 0.3, '높이 $h/2$', fontsize=8, ha='right', va='center', color=fs.GRAY)
    fs.save(fig, F, 'fig16_07')


# ---------------------------------------------------------------- 16.6 간섭
def fig08():
    fig, axs = plt.subplots(3, 1, figsize=(4.8, 3.4), sharex=True)
    x = np.linspace(0, 4 * np.pi, 600)
    for ax, (phi, lab) in zip(axs, ((0, r'$\phi=0$: 보강'), (2 * np.pi / 3, r'$\phi=120$°: $y_m^{\prime}=y_m$'), (np.pi, r'$\phi=\pi$: 상쇄'))):
        y1 = np.sin(x); y2 = np.sin(x + phi)
        ax.plot(x, y1, color=fs.GRAY, lw=1.0, ls='--')
        ax.plot(x, y2, color=fs.ORANGE, lw=1.0, ls=':')
        ax.plot(x, y1 + y2, color=fs.VEL, lw=1.7)
        ax.set_ylim(-2.3, 2.3); ax.set_yticks([-2, 0, 2]); ax.set_yticklabels(['$-2y_m$', '0', '$2y_m$'])
        ax.axhline(0, color=fs.GRAY, lw=0.5)
        ax.text(1.0, 1.02, lab, transform=ax.transAxes, ha='right', va='bottom', fontsize=8)
        ax.tick_params(labelsize=8)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    axs[0].plot([], [], color=fs.GRAY, lw=1.0, ls='--', label='$y_1$')
    axs[0].plot([], [], color=fs.ORANGE, lw=1.0, ls=':', label='$y_2$')
    axs[0].plot([], [], color=fs.VEL, lw=1.7, label='$y_1+y_2$')
    axs[0].legend(fontsize=7, ncol=3, loc='lower left', bbox_to_anchor=(0.0, 0.98), frameon=False, borderaxespad=0)
    axs[2].set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    axs[2].set_xticklabels(['0', r'$\lambda/2$', r'$\lambda$', r'$3\lambda/2$', r'$2\lambda$'])
    axs[2].set_xlabel('$x$ (한 순간의 모양)', fontsize=9)
    axs[2].set_xlim(0, 4 * np.pi)
    fig.tight_layout(h_pad=0.9)
    fs.save(fig, F, 'fig16_08')


# ---------------------------------------------------------------- 16.6 페이저 합
def fig09():
    fig, ax = fs.canvas(3.4, 2.2, xlim=(-0.3, 2.6), ylim=(-0.25, 1.45))
    a1, a2, ph = 1.4, 0.95, np.radians(60)
    p1 = np.array([a1, 0]); p2 = p1 + a2 * np.array([np.cos(ph), np.sin(ph)])
    fs.arrow(ax, (0, 0), p1, color=fs.BLACK, lw=1.8)
    fs.arrow(ax, p1, p2, color=fs.ORANGE, lw=1.8)
    fs.arrow(ax, (0, 0), p2, color=fs.VEL, lw=2.0)
    dline(ax, p1, p1 + np.array([0.7, 0]), ls=':')
    fs.angle_arc(ax, p1, 0.35, 0, 60, r'$\phi$', fontsize=10, tr=0.5)
    ang = np.degrees(np.arctan2(p2[1], p2[0]))
    fs.angle_arc(ax, (0, 0), 0.55, 0, ang, None, color=fs.VEL)
    ax.text(0.62, 0.12, '합성 위상', fontsize=7, color=fs.VEL)
    ax.text(a1 / 2, -0.12, '$y_{m1}$', ha='center', va='top', fontsize=10)
    ax.text(p1[0] + a2 / 2 * np.cos(ph) + 0.12, a2 / 2 * np.sin(ph), '$y_{m2}$', fontsize=10, color=fs.ORANGE, va='center')
    ax.text(p2[0] / 2 - 0.15, p2[1] / 2 + 0.12, r"$y_m^{\prime}$", fontsize=11, color=fs.VEL, ha='right')
    fs.save(fig, F, 'fig16_09')


# ---------------------------------------------------------------- 16.7 정상파 스냅숏
def fig10():
    fig, ax = fs.canvas(4.8, 2.4, xlim=(-0.4, 3 * np.pi + 0.5), ylim=(-2.9, 2.6))
    x = np.linspace(0, 3 * np.pi, 600)
    cols = plt.cm.Blues(np.linspace(0.45, 1.0, 5))
    for i, wt in enumerate(np.linspace(0, np.pi, 5)):
        ax.plot(x, 2 * np.sin(x) * np.cos(wt), color=cols[i] if i < 3 else plt.cm.Oranges(0.4 + 0.25 * (i - 2)), lw=1.2)
    ax.plot([0, 3 * np.pi], [0, 0], color=fs.GRAY, lw=0.5)
    for n in range(4):
        ax.add_patch(Circle((n * np.pi, 0), 0.1, fc='white', ec=fs.FORCE, lw=1.3, zorder=6))
        ax.text(n * np.pi, -0.3, 'N', ha='center', va='top', fontsize=9, color=fs.FORCE)
    for n in range(3):
        xa = (n + 0.5) * np.pi
        ax.text(xa, 2.15, 'A', ha='center', va='bottom', fontsize=9, color=fs.ACC)
    darrow(ax, (0, -2.45), (np.pi, -2.45), r'$\lambda/2$', off=(0, -0.28), fontsize=9)
    darrow(ax, (np.pi / 2 + 0.25, 0), (np.pi / 2 + 0.25, 2.0), r'$2y_m$', off=(0.42, 0), fontsize=9)
    fs.save(fig, F, 'fig16_10')


# ---------------------------------------------------------------- 16.7 고정단·자유단 반사
def fig11():
    fig, ax = fs.canvas(5.0, 2.6, xlim=(-0.2, 9.4), ylim=(-1.35, 3.3))
    def row(x0, y0, sign, inc):
        x = np.linspace(x0, x0 + 3.6, 300)
        c = x0 + (2.1 if inc else 1.2)
        y = sign * 0.75 * pulse(x, c, 0.32)
        ax.plot(x, y0 + y, color=fs.VEL if inc else fs.FORCE, lw=1.5)
        d = 1 if inc else -1
        ya = y0 + (0.95 if sign > 0 else 0.4)
        fs.arrow(ax, (c - 0.35 * d, ya), (c + 0.35 * d, ya), color=fs.BLACK, lw=1.1, ms=8)
    # (가) 고정단
    for y0, sign, inc in ((2.0, 1, True), (0.0, -1, False)):
        row(0.0, y0, sign, inc)
        fs.wall(ax, y0 - 0.9, y0 + 0.9, x=3.6, side='right')
    ax.text(1.8, -1.25, '(가) 고정단: 뒤집혀 반사', ha='center', fontsize=9)
    # (나) 자유단
    x0 = 5.4
    for y0, sign, inc in ((2.0, 1, True), (0.0, 1, False)):
        row(x0, y0, 1, inc)
        ax.plot([x0 + 3.75, x0 + 3.75], [y0 - 0.9, y0 + 0.9], color=fs.BLACK, lw=2.0)
        ax.add_patch(Circle((x0 + 3.68, y0), 0.09, fc='white', ec=fs.BLACK, lw=1.0, zorder=6))
    ax.text(x0 + 1.8, -1.25, '(나) 자유단: 그대로 반사', ha='center', fontsize=9)
    ax.text(-0.15, 2.0 + 0.2, '입사', fontsize=8, color=fs.VEL)
    ax.text(-0.15, 0.0 + 0.2, '반사', fontsize=8, color=fs.FORCE)
    fs.save(fig, F, 'fig16_11')


# ---------------------------------------------------------------- 16.7 조화파
def fig12():
    fig, ax = fs.canvas(4.0, 3.3, xlim=(-0.4, 6.9), ylim=(-0.75, 8.2))
    L = 4.0
    x = np.linspace(0, L, 400)
    for i, n in enumerate((1, 2, 3, 4)):
        y0 = 7.2 - 2.1 * i
        env = 0.65 * np.sin(n * np.pi * x / L)
        ax.fill_between(x, y0 - env, y0 + env, color='#dbe7f3', lw=0)
        ax.plot(x, y0 + env, color=fs.VEL, lw=1.4)
        ax.plot(x, y0 - env, color=fs.VEL, lw=1.0, ls='--')
        for xe in (0, L):
            ax.add_patch(Rectangle((xe - 0.12 if xe == 0 else xe, y0 - 0.45), 0.12, 0.9, fc=fs.GRAY, ec='none'))
        lam = {1: '2L', 2: 'L', 3: '2L/3', 4: 'L/2'}[n]
        fn = r'$f_1=v/2L$' if n == 1 else rf'$f_{n}={n}f_1$'
        ax.text(L + 0.35, y0 + 0.22, f'$n={n}$:  ' + fn, fontsize=9, va='center')
        ax.text(L + 0.35, y0 - 0.35, rf'$\lambda_{n}={lam}$', fontsize=9, va='center')
    darrow(ax, (0, -0.25), (L, -0.25), '$L$', off=(0, -0.25), fontsize=10)
    fs.save(fig, F, 'fig16_12')


# ---------------------------------------------------------------- 예제 16.7 진동자와 도르래
def fig13():
    fig, ax = fs.canvas(5.0, 2.4, xlim=(-1.2, 7.4), ylim=(-2.6, 1.6))
    L = 6.0
    # 진동자
    ax.add_patch(Rectangle((-1.0, -0.5), 0.75, 1.0, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1))
    ax.text(-0.62, 0, '진동자', fontsize=7, ha='center', va='center', rotation=90)
    ax.plot([-0.25, 0], [0, 0], color=fs.BLACK, lw=1.4)
    fs.arrow(ax, (-0.05, -0.35), (-0.05, 0.35), color=fs.BLACK, lw=0.8, style='<|-|>', ms=6)
    x = np.linspace(0, L, 400)
    env = 0.55 * np.sin(4 * np.pi * x / L)
    ax.fill_between(x, -env, env, color='#dbe7f3', lw=0)
    ax.plot(x, env, color=fs.VEL, lw=1.3); ax.plot(x, -env, color=fs.VEL, lw=1.0, ls='--')
    # 도르래와 추
    pr = 0.3
    P = (L, -pr)
    fs.pulley(ax, P, r=pr)
    ax.plot([L, L + pr], [0, 0], color=fs.BLACK, lw=0.8)
    ax.plot([L + pr, L + pr], [-pr, -1.6], color=fs.BLACK, lw=1.1)
    fs.block(ax, (L + pr, -1.9), w=0.44, h=0.55, text='$M$', fontsize=9)
    ax.add_patch(Rectangle((L - 0.05, -2.4), 0.1, 2.4 - pr, fc=fs.GRAY, ec='none', zorder=1))
    fs.ground(ax, L - 0.7, L + 0.05, y=-2.4)
    darrow(ax, (0, 0.85), (L, 0.85), r'$L=1.20\ \mathrm{m}$', off=(0, 0.25), fontsize=9)
    ax.text(3.0, -1.0, '고리(배) 4개', ha='center', fontsize=9, color=fs.VEL)
    ax.text(-0.6, -0.75, '$120$ Hz', ha='center', va='top', fontsize=8)
    fs.save(fig, F, 'fig16_13')


for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
    f()
