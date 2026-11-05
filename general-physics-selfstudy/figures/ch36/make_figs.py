"""36장 광자와 물질파 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch, Ellipse, FancyArrowPatch

h, c, kB = 6.62607015e-34, 299792458.0, 1.380649e-23
eV = 1.602176634e-19
LIGHT_C = fs.ORANGE


def axes_clean(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def photon(ax, p, q, color=LIGHT_C, amp=0.08, nw=4, lw=1.3, label=None, loff=(0, 0.2), fontsize=10):
    """p에서 q로 가는 물결선 광자(끝에 화살촉)."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p; L = np.hypot(*d); u = d / L; n = np.array([-u[1], u[0]])
    t = np.linspace(0, L * 0.88, 300)
    w = amp * np.sin(2 * np.pi * nw * t / (L * 0.88))
    pts = p + np.outer(t, u) + np.outer(w, n)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=4)
    ax.add_patch(FancyArrowPatch(p + u * L * 0.86, q, arrowstyle='-|>', mutation_scale=10, color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=4))
    if label:
        m = (p + q) / 2
        ax.text(m[0] + loff[0], m[1] + loff[1], label, color=color, fontsize=fontsize, ha='center', va='center')


def electron(ax, p, r=0.13, label=True):
    ax.add_patch(Circle(p, r, fc=fs.NEG, ec='none', zorder=6))
    if label:
        ax.text(p[0], p[1] - 0.01, '−', color='white', ha='center', va='center', fontsize=9, fontweight='bold', zorder=7)


# ---------------------------------------------------------------- 공동 복사
def fig01():
    fig, ax = fs.canvas(3.4, 2.1, xlim=(-1.45, 3.8), ylim=(-0.1, 2.75))
    t = 0.18
    outer = Rectangle((0, 0), 3.6, 2.6, fc='#9aa5b1', ec=fs.BLACK, lw=1.1, zorder=1)
    ax.add_patch(outer)
    ax.add_patch(Rectangle((t, t), 3.6 - 2 * t, 2.6 - 2 * t, fc='#fff3e0', ec=fs.BLACK, lw=0.9, zorder=2))
    ax.add_patch(Rectangle((-0.01, 1.62), t + 0.02, 0.22, fc='white', ec='none', zorder=3))
    ax.plot([0, t], [1.62, 1.62], color=fs.BLACK, lw=0.9, zorder=3); ax.plot([0, t], [1.84, 1.84], color=fs.BLACK, lw=0.9, zorder=3)
    pts = [(-1.3, 2.25), (t, 1.73), (3.42, 0.6), (1.9, t), (0.6, 2.42), (3.42, 1.9), (2.6, 2.42), (1.2, t)]
    fs.ray(ax, pts, color=LIGHT_C, lw=1.1)
    ax.text(-1.35, 2.5, '들어온 빛', fontsize=8.5, color=LIGHT_C)
    ax.text(-0.7, 1.25, '작은 구멍', fontsize=8.5, ha='center')
    ax.text(2.3, 1.25, '공동\n(온도 $T$)', fontsize=9, ha='center', va='center', zorder=6,
            bbox=dict(fc='#fff3e0', ec='none', pad=1.5))
    fs.save(fig, __file__, 'fig36_01')


# ---------------------------------------------------------------- 플랑크 vs 레일리–진스
def fig02():
    fig, ax = fs.plot_axes(4.2, 2.8)
    T = 5000
    f = np.linspace(1e12, 1.2e15, 800)
    u_pl = 8 * np.pi * h * f ** 3 / c ** 3 / np.expm1(h * f / (kB * T))
    u_rj = 8 * np.pi * f ** 2 / c ** 3 * kB * T
    sc = 1e-16
    ax.axvspan(c / 750e-9 / 1e14, c / 380e-9 / 1e14, color='#fff2cc', zorder=0)
    ax.text(c / 520e-9 / 1e14, 0.6, '가시광선', fontsize=8, ha='center', color='#8a6d00')
    ax.plot(f / 1e14, u_pl / sc, color=fs.VEL, lw=1.8, label='플랑크 법칙')
    ax.plot(f / 1e14, u_rj / sc, color=fs.FORCE, lw=1.5, ls='--', label='레일리–진스 법칙')
    ax.set_xlim(0, 12); ax.set_ylim(0, 16)
    ax.set_xlabel(r'진동수 $f$ ($10^{14}$ Hz)'); ax.set_ylabel(r'$u(f)$ ($10^{-16}$ J·s/m$^3$)')
    ax.text(1.9, 13.0, '자외선 파탄\n($\\propto f^2$)', fontsize=8.5, color=fs.FORCE)
    ax.text(8.5, 3.0, '$T = 5000$ K', fontsize=9)
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig36_02')


# ---------------------------------------------------------------- 여러 온도의 흑체 스펙트럼
def fig03():
    fig, ax = fs.plot_axes(4.4, 2.9)
    lam = np.linspace(50e-9, 3000e-9, 3000)
    u = lambda l, T: 8 * np.pi * h * c / l ** 5 / np.expm1(h * c / (l * kB * T))
    ref = u(2.897771955e-3 / 5800, 5800)
    from matplotlib.colors import hsv_to_rgb
    for l0 in np.arange(380, 750, 4):
        hue = 0.78 * (1 - (l0 - 380) / 370)
        ax.axvspan(l0, l0 + 4, color=hsv_to_rgb((hue, 0.35, 1)), lw=0, zorder=0)
    cols = {3000: fs.FORCE, 4000: fs.ORANGE, 5000: fs.ACC, 5800: fs.VEL}
    for T in (3000, 4000, 5000, 5800):
        y = u(lam, T) / ref
        ax.plot(lam * 1e9, y, color=cols[T], lw=1.6)
        i = np.argmax(y)
        ax.plot(lam[i] * 1e9, y[i], 'o', color=cols[T], ms=3.5)
        ax.text(lam[i] * 1e9 + 60, y[i] + 0.02, f'{T} K', fontsize=8.5, color=cols[T], va='bottom')
    Ts = np.linspace(2700, 6400, 100)
    b = 2.897771955e-3
    ax.plot(b / Ts * 1e9, u(b / Ts, Ts) / ref, ls=':', color=fs.GRAY, lw=1.2)
    ax.text(1250, 0.32, r'$\lambda_{\max}T = b$', fontsize=9, color=fs.GRAY)
    ax.set_xlim(0, 2500); ax.set_ylim(0, 1.15)
    ax.set_xlabel(r'파장 $\lambda$ (nm)'); ax.set_ylabel(r'$u(\lambda)$ (5800 K 최댓값 = 1)')
    fs.save(fig, __file__, 'fig36_03')


# ---------------------------------------------------------------- 광전 효과 장치
def battery_var(ax, x, y, w=0.5):
    """세로 배치 가변 전원 기호(긴 판이 +). 위쪽이 +."""
    ax.plot([x - 0.25, x + 0.25], [y + 0.08, y + 0.08], color=fs.BLACK, lw=1.4)
    ax.plot([x - 0.13, x + 0.13], [y - 0.08, y - 0.08], color=fs.BLACK, lw=2.4)
    fs.arrow(ax, (x - 0.35, y - 0.3), (x + 0.38, y + 0.33), lw=0.9, ms=8)


def fig04():
    fig, ax = fs.canvas(4.0, 2.9, xlim=(-1.2, 5.0), ylim=(-2.6, 2.1))
    ax.add_patch(FancyBboxPatch((0.2, -0.5), 3.4, 2.0, boxstyle='round,pad=0.05,rounding_size=0.5', fc='#f4f8fc', ec=fs.BLACK, lw=1.1))
    ax.text(1.9, 1.75, '진공관', fontsize=8.5, ha='center')
    ax.add_patch(Rectangle((0.55, -0.15), 0.14, 1.3, fc='#7f8c8d', ec=fs.BLACK, lw=0.8, zorder=3))
    ax.add_patch(Rectangle((3.1, -0.15), 0.14, 1.3, fc='#bdc3c7', ec=fs.BLACK, lw=0.8, zorder=3))
    ax.text(0.62, -0.78, '금속판(음극)', fontsize=8, ha='center')
    ax.text(3.17, -0.78, '수집판', fontsize=8, ha='center')
    for k, yy in enumerate((1.9, 1.55)):
        photon(ax, (-1.1, yy + 0.3), (0.52, yy - 1.05 + 0.1 * k), amp=0.06, nw=4)
    ax.text(-0.95, 1.05, '빛 ($hf$)', fontsize=9, color=LIGHT_C)
    for yy in (0.25, 0.75):
        electron(ax, (1.6 + (yy - 0.25) * 0.8, yy), r=0.1)
        fs.arrow(ax, (1.75 + (yy - 0.25) * 0.8, yy), (2.35 + (yy - 0.25) * 0.8, yy), color=fs.VEL, lw=1.2, ms=8)
    ax.text(1.9, 1.12, '광전자', fontsize=8, color=fs.NEG, ha='center')
    # 외부 회로
    ax.plot([0.62, 0.62, -0.6, -0.6], [-0.15, -0.5, -0.5, -1.9], color=fs.BLACK, lw=1.1)
    ax.plot([3.17, 3.17, 4.4, 4.4], [-0.15, -0.5, -0.5, -1.9], color=fs.BLACK, lw=1.1)
    ax.plot([-0.6, 1.5], [-1.9, -1.9], color=fs.BLACK, lw=1.1)
    ax.plot([2.3, 4.4], [-1.9, -1.9], color=fs.BLACK, lw=1.1)
    # 가변 전원(가로 배치): 왼쪽 판이 음극 쪽
    xb = 1.9
    ax.plot([1.5, xb - 0.08], [-1.9, -1.9], color=fs.BLACK, lw=1.1)
    ax.plot([xb + 0.08, 2.3], [-1.9, -1.9], color=fs.BLACK, lw=1.1)
    ax.plot([xb - 0.08, xb - 0.08], [-2.15, -1.65], color=fs.BLACK, lw=1.4)
    ax.plot([xb + 0.08, xb + 0.08], [-2.03, -1.77], color=fs.BLACK, lw=2.4)
    fs.arrow(ax, (xb - 0.35, -2.25), (xb + 0.35, -1.55), lw=0.9, ms=8)
    ax.text(xb, -2.45, r'가변 전원 $V$', fontsize=8.5, ha='center')
    # 전류계
    ax.add_patch(Circle((4.4, -1.2), 0.22, fc='white', ec=fs.BLACK, lw=1.1, zorder=4))
    ax.text(4.4, -1.2, 'A', ha='center', va='center', fontsize=9, zorder=5)
    ax.text(4.7, -1.2, '전류 $I$', fontsize=8.5, va='center')
    fs.save(fig, __file__, 'fig36_04')


# ---------------------------------------------------------------- I–V 곡선
def fig05():
    fig, ax = fs.plot_axes(4.2, 2.7)
    V = np.linspace(-2.6, 2.0, 600)

    def I(V, V0, Is):
        x = np.clip((V + V0) / (V0 + 0.4), 0, 1)
        return Is * x ** 2 * (3 - 2 * x)

    V1 = 1239.84 / 400 - 2.28
    V2 = 1239.84 / 300 - 2.28
    ax.plot(V, I(V, V1, 1.0), color=fs.VEL, lw=1.7, label=r'$\lambda = 400$ nm, 센 빛')
    ax.plot(V, I(V, V1, 0.5), color=fs.VEL, lw=1.4, ls='--', label=r'$\lambda = 400$ nm, 약한 빛')
    ax.plot(V, I(V, V2, 0.75), color=fs.FIELD, lw=1.5, label=r'$\lambda = 300$ nm')
    ax.axvline(0, color=fs.BLACK, lw=0.8)
    for v0, col in ((V1, fs.VEL), (V2, fs.FIELD)):
        ax.plot([-v0], [0], 'o', color=col, ms=4)
    ax.annotate(r'$-V_0 = -0.82$ V', xy=(-V1, 0), xytext=(-0.95, -0.27), fontsize=8.5, color=fs.VEL,
                arrowprops=dict(arrowstyle='->', color=fs.VEL, lw=0.8))
    ax.annotate(r'$-1.85$ V', xy=(-V2, 0), xytext=(-2.55, -0.27), fontsize=8.5, color=fs.FIELD,
                arrowprops=dict(arrowstyle='->', color=fs.FIELD, lw=0.8))
    ax.set_xlim(-2.6, 2.0); ax.set_ylim(-0.35, 1.25)
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    ax.set_yticks([])
    ax.set_xlabel('수집판의 전위 $V$ (음극 기준, V)'); ax.set_ylabel('광전류 $I$')
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    fs.save(fig, __file__, 'fig36_05')


# ---------------------------------------------------------------- K_max - f
def fig06():
    fig, ax = fs.plot_axes(4.2, 2.9)
    f = np.linspace(0, 13, 100)  # 10^14 Hz
    hh = h / eV * 1e14  # eV per 10^14 Hz
    for phi, col, name in ((2.28, fs.VEL, r'$\phi = 2.28$ eV'), (4.3, fs.FORCE, r'$\phi = 4.3$ eV')):
        f0 = phi / hh
        K = hh * f - phi
        ax.plot(f[f >= f0], K[f >= f0], color=col, lw=1.8, label=name)
        ax.plot(f[f <= f0], K[f <= f0], color=col, lw=1.0, ls=':')
        ax.plot([f0], [0], 'o', color=col, ms=4)
        ax.text(f0 + 0.15, -0.35, f'$f_0 = {f0:.2f}$', fontsize=8, color=col)
        ax.text(0.3, -phi - 0.3, r'$-\phi$', fontsize=9.5, color=col, va='center')
    fx = c / 400e-9 / 1e14
    ax.plot([fx], [hh * fx - 2.28], 's', color=fs.ACC, ms=4.5)
    ax.annotate('예제 36.3\n(400 nm, 0.82 eV)', xy=(fx, hh * fx - 2.28), xytext=(1.0, 1.9), fontsize=8, color=fs.ACC,
                arrowprops=dict(arrowstyle='->', color=fs.ACC, lw=0.8))
    ax.plot([9, 11, 11], [hh * 9 - 2.28, hh * 9 - 2.28, hh * 11 - 2.28], color=fs.GRAY, lw=0.8)
    ax.text(11.15, hh * 10 - 2.28, '기울기 $h$', fontsize=8.5, color=fs.GRAY, va='center')
    ax.legend(fontsize=8.5, frameon=False, loc='lower right')
    ax.axhline(0, color=fs.BLACK, lw=0.8)
    ax.set_xlim(0, 13); ax.set_ylim(-4.8, 3.2)
    ax.set_xlabel(r'진동수 $f$ ($10^{14}$ Hz)'); ax.set_ylabel(r'$K_{\max} = eV_0$ (eV)')
    fs.save(fig, __file__, 'fig36_06')


# ---------------------------------------------------------------- 콤프턴 산란 기하
def fig07():
    fig, ax = fs.canvas(4.6, 2.5, xlim=(-3.2, 3.6), ylim=(-1.7, 2.0))
    photon(ax, (-3.1, 0), (-0.25, 0), amp=0.12, nw=6, label=r'$\lambda,\ \ p = h/\lambda$', loff=(0, 0.38))
    electron(ax, (0, 0), r=0.16)
    ax.text(-0.55, -0.42, '정지한 전자', fontsize=8, ha='center')
    th, ph = np.radians(40), np.radians(-35)
    photon(ax, (0.2 * np.cos(th), 0.2 * np.sin(th)), (2.9 * np.cos(th), 2.9 * np.sin(th)), amp=0.12, nw=4.5)
    ax.text(2.25, 2.0, r"$\lambda',\ \ p' = h/\lambda'$", fontsize=10, color=LIGHT_C, ha='center')
    fs.arrow(ax, (0.22 * np.cos(ph), 0.22 * np.sin(ph)), (2.4 * np.cos(ph), 2.4 * np.sin(ph)), color=fs.NEG, lw=1.8)
    ax.text(2.25, -1.55, r'$\vec p_e,\ E_e$', fontsize=10, color=fs.NEG, ha='center')
    ax.plot([0, 3.3], [0, 0], ls=':', color=fs.GRAY, lw=0.9)
    fs.angle_arc(ax, (0, 0), 1.1, 0, 40, r'$\theta$', fontsize=11)
    fs.angle_arc(ax, (0, 0), 0.9, -35, 0, r'$\varphi$', fontsize=11)
    fs.save(fig, __file__, 'fig36_07')


# ---------------------------------------------------------------- 예제 36.4 운동량 벡터
def fig08():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.5), gridspec_kw={'width_ratios': [1, 1]})
    lam, lamp = 71.1, 73.53
    p, pp = 1 / lam * 100, 1 / lamp * 100  # 축척
    ang = np.degrees(np.arctan(lam / lamp))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    ax = axs[0]
    photon(ax, (-1.8, 0), (-0.15, 0), amp=0.08, nw=4)
    electron(ax, (0, 0), r=0.12)
    photon(ax, (0, 0.17), (0, 1.5), amp=0.08, nw=3)
    fs.arrow(ax, (0.12 * np.cos(np.radians(-ang)), 0.12 * np.sin(np.radians(-ang))),
             (1.5 * np.cos(np.radians(-ang)), 1.5 * np.sin(np.radians(-ang))), color=fs.NEG, lw=1.8)
    ax.plot([0, 1.6], [0, 0], ls=':', color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, (0, 0), 0.75, -ang, 0, f'{ang:.1f}°', fontsize=8.5, tr=1.05)
    ax.text(-1.0, 0.3, '71.1 pm', fontsize=8.5, color=LIGHT_C, ha='center')
    ax.text(0.15, 1.35, '73.5 pm', fontsize=8.5, color=LIGHT_C)
    ax.text(1.1, -1.3, '전자', fontsize=8.5, color=fs.NEG)
    ax.text(-0.5, -1.55, '(가) 진행 방향', fontsize=9, ha='center')
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.7, 1.7)
    ax = axs[1]
    fs.arrow(ax, (0, 0), (p, 0), color=LIGHT_C, lw=1.8, label=r'$\vec p$', lpos=0.5, loff=(0, -0.2))
    fs.arrow(ax, (0, 0), (0, pp), color=LIGHT_C, lw=1.8, label=r"$\vec p\,'$", lpos=0.5, loff=(-0.25, 0))
    fs.arrow(ax, (0, pp), (p, 0), color=fs.NEG, lw=1.8, label=r'$\vec p_e$', lpos=0.5, loff=(0.25, 0.15))
    ax.add_patch(Rectangle((0, 0), 0.1, 0.1, fc='none', ec=fs.BLACK, lw=0.6))
    ax.text(p / 2, -0.55, r"$\vec p = \vec p\,' + \vec p_e$", fontsize=9, ha='center')
    ax.text(p / 2, -0.95, '(나) 운동량 보존', fontsize=9, ha='center')
    ax.set_xlim(-0.5, 1.9); ax.set_ylim(-1.1, 1.6)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig36_08')


# ---------------------------------------------------------------- 데이비슨–거머
def fig09():
    fig, ax = fs.canvas(4.0, 2.7, xlim=(-1.6, 3.8), ylim=(-0.7, 3.0))
    d = 1.2
    xs = np.arange(-1.2, 3.7, d)
    for x in xs:
        ax.add_patch(Circle((x, 0), 0.13, fc='#95a5a6', ec=fs.BLACK, lw=0.7, zorder=3))
    ax.add_patch(Rectangle((-1.6, -0.7), 5.4, 0.55, fc='#ecf0f1', ec='none', zorder=0))
    ax.text(3.1, -0.45, '니켈 결정', fontsize=8.5, ha='center')
    phi = np.radians(50)
    A, B = (0.0, 0.0), (d, 0.0)
    for P in (A, B):
        fs.arrow(ax, (P[0], 2.7), (P[0], 0.18), color=fs.NEG, lw=1.3, ms=9)
        Q = (P[0] + 2.6 * np.sin(phi), 2.6 * np.cos(phi))
        fs.arrow(ax, (P[0] + 0.18 * np.sin(phi), 0.18 * np.cos(phi)), Q, color=fs.VEL, lw=1.3, ms=9)
    fs.angle_arc(ax, B, 0.8, 90 - 50, 90, r'$\varphi$', fontsize=11)
    # 경로차: B에서 A의 산란선에 내린 수선
    u = np.array([np.sin(phi), np.cos(phi)])
    foot = np.array(A) + np.dot(np.array(B) - np.array(A), u) * u
    ax.plot([B[0], foot[0]], [B[1], foot[1]], color=fs.FORCE, lw=0.9, ls='--')
    ax.plot([A[0], foot[0]], [A[1], foot[1]], color=fs.FORCE, lw=2.4, solid_capstyle='butt')
    ax.annotate(r'$d\sin\varphi$', xy=(foot[0] * 0.5, foot[1] * 0.5), xytext=(-1.45, 1.0), color=fs.FORCE, fontsize=10,
                arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.8))
    ax.annotate('', xy=(B[0], -0.3), xytext=(A[0], -0.3), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(d / 2, -0.52, r'$d$', fontsize=10, color=fs.GRAY, ha='center')
    ax.text(-1.5, 2.55, '입사 전자\n$54$ eV', fontsize=8.5, color=fs.NEG)
    ax.text(2.55, 2.5, '되튄 전자', fontsize=8.5, color=fs.VEL)
    fs.save(fig, __file__, 'fig36_09')


# ---------------------------------------------------------------- 하나씩 쌓이는 간섭무늬
def fig10():
    rng = np.random.default_rng(1)
    lam, d, a, L = 500e-9, 50e-6, 10e-6, 1.0
    y = np.linspace(-0.05, 0.05, 2001)
    beta = np.pi * a * y / (lam * L); ph = np.pi * d * y / (lam * L)
    P = np.cos(ph) ** 2 * np.sinc(beta / np.pi) ** 2
    P /= P.sum()
    fig, axs = plt.subplots(4, 1, figsize=(4.6, 3.4), sharex=True, gridspec_kw={'height_ratios': [1, 1, 1, 0.9]})
    for k, N in enumerate([30, 1000, 50000]):
        hits = rng.choice(y, size=N, p=P)
        ax = axs[k]
        vy = rng.uniform(0, 1, N)
        ax.scatter(hits * 100, vy, s=(4 if N <= 1000 else 0.15), color=fs.BLACK, lw=0, rasterized=True)
        ax.set_ylim(0, 1); ax.set_yticks([])
        ax.text(-5.25, 0.5, f'$N = {N}$', fontsize=8.5, ha='right', va='center')
        for s in ('top', 'right', 'left'):
            ax.spines[s].set_visible(True)
    ax = axs[3]
    ax.plot(y * 100, P / P.max(), color=fs.VEL, lw=1.2)
    ax.fill_between(y * 100, P / P.max(), color=fs.VEL, alpha=0.15)
    ax.set_yticks([]); ax.set_ylim(0, 1.1)
    ax.text(-5.25, 0.5, r'$P(y)$', fontsize=8.5, ha='right', va='center', color=fs.VEL)
    ax.set_xlim(-5, 5); ax.set_xlabel('스크린 위치 $y$ (cm)')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.subplots_adjust(hspace=0.12, left=0.16)
    fig.set_dpi(300)
    fs.save(fig, __file__, 'fig36_10')


# ---------------------------------------------------------------- 단일 슬릿과 불확정성
def fig11():
    fig, ax = fs.canvas(4.6, 2.6, xlim=(-2.8, 4.3), ylim=(-2.0, 2.0))
    a = 0.5
    ax.add_patch(Rectangle((-0.08, a / 2), 0.16, 1.7, fc='#7f8c8d', ec=fs.BLACK, lw=0.8))
    ax.add_patch(Rectangle((-0.08, -a / 2 - 1.7), 0.16, 1.7, fc='#7f8c8d', ec=fs.BLACK, lw=0.8))
    for yy in np.linspace(-0.9, 0.9, 7):
        pass
    for xx in (-2.3, -1.8, -1.3, -0.8):
        ax.plot([xx, xx], [-1.0, 1.0], color=fs.VEL, lw=0.9, alpha=0.7)
    fs.vec(ax, (-2.7, 1.35), (1.0, 0), color=fs.VEL, lw=1.6, label=r'$\vec p$', loff=(-0.5, 0.25))
    ax.annotate('', xy=(-0.25, a / 2), xytext=(-0.25, -a / 2), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=7))
    ax.text(-0.35, 0, r'$a$', fontsize=10, color=fs.GRAY, ha='right', va='center')
    th = np.radians(25)
    for s in (1, -1):
        ax.plot([0.1, 3.2], [0, s * 3.1 * np.tan(th)], ls='--', color=fs.GRAY, lw=0.8)
    # 회절 후 운동량
    o = np.array([0.4, 0.0])
    P = 1.5
    fs.vec(ax, tuple(o), (P * np.cos(th), P * np.sin(th)), color=fs.VEL, lw=1.6)
    ax.text(o[0] + P * np.cos(th) * 0.55 - 0.15, o[1] + P * np.sin(th) * 0.55 + 0.25, r'$\vec p$', color=fs.VEL, fontsize=10)
    ax.plot([o[0] + P * np.cos(th)] * 2, [0, P * np.sin(th)], color=fs.FORCE, lw=1.6)
    ax.text(o[0] + P * np.cos(th) + 0.1, P * np.sin(th) / 2, r'$p_y \approx p\sin\theta$', color=fs.FORCE, fontsize=9, va='center')
    fs.angle_arc(ax, tuple(o), 0.8, 0, 25, r'$\theta$', fontsize=10)
    ax.plot([o[0], o[0] + 1.6], [0, 0], ls=':', color=fs.GRAY, lw=0.8)
    # 스크린과 세기
    xs = 3.4
    ax.plot([xs, xs], [-1.9, 1.9], color=fs.BLACK, lw=1.2)
    yy = np.linspace(-1.9, 1.9, 400)
    bb = np.pi * yy / (3.1 * np.tan(th))
    I = np.sinc(bb / np.pi) ** 2
    ax.fill_betweenx(yy, xs, xs + 0.8 * I, color=fs.VEL, alpha=0.25)
    ax.plot(xs + 0.8 * I, yy, color=fs.VEL, lw=1)
    ax.text(xs + 0.45, -1.75, '스크린', fontsize=8, ha='center')
    ax.text(-1.6, -1.45, '슬릿 폭 $a$:\n$\\Delta y \\sim a$', fontsize=8.5, ha='center')
    ax.text(1.6, -1.55, r'$\sin\theta = \lambda/a$', fontsize=9, color=fs.GRAY, ha='center')
    fs.save(fig, __file__, 'fig36_12')


# ---------------------------------------------------------------- 가우스 파동 묶음
def fig12():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3), gridspec_kw={'width_ratios': [1.6, 1]})
    sx, k0 = 1.0, 8.0
    sk = 1 / (2 * sx)
    x = np.linspace(-5, 5, 1500)
    env = np.exp(-x ** 2 / (4 * sx ** 2))
    ax = axs[0]
    ax.plot(x, env * np.cos(k0 * x), color=fs.VEL, lw=1.0, label=r'$\mathrm{Re}\,\psi$')
    ax.plot(x, env, color=fs.FORCE, lw=1.3, ls='--', label=r'$\pm|\psi|$')
    ax.plot(x, -env, color=fs.FORCE, lw=1.3, ls='--')
    ax.annotate('', xy=(sx, -1.25), xytext=(-sx, -1.25), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(0, -1.5, r'$2\sigma_x$', ha='center', fontsize=9, color=fs.GRAY, va='center')
    ax.set_ylim(-1.7, 1.3); ax.set_xlim(-5, 5)
    ax.set_xlabel(r'$x$'); ax.set_yticks([]); ax.set_title('(가) 위치 공간', fontsize=9)
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    ax = axs[1]
    k = np.linspace(k0 - 2.5, k0 + 2.5, 400)
    phi2 = np.exp(-(k - k0) ** 2 / (2 * sk ** 2))
    ax.plot(k, phi2, color=fs.ACC, lw=1.5)
    ax.fill_between(k, phi2, color=fs.ACC, alpha=0.15)
    ax.annotate('', xy=(k0 + sk, 0.25), xytext=(k0 - sk, 0.25), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(k0, 0.12, r'$2\sigma_k$', ha='center', fontsize=9, color=fs.GRAY)
    ax.set_xticks([k0]); ax.set_xticklabels([r'$k_0$'])
    ax.set_yticks([]); ax.set_ylim(0, 1.15); ax.set_xlabel(r'$k$')
    ax.set_title(r'(나) 파수 분포 $|\phi(k)|^2$', fontsize=9)
    for a_ in axs:
        for s in ('top', 'right'):
            a_.spines[s].set_visible(False)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig36_11')


# ---------------------------------------------------------------- 수소 원자 크기 어림 E(r)
def fig13():
    fig, ax = fs.plot_axes(4.2, 2.8)
    C, ke2 = 0.0380998, 1.43996  # eV nm^2, eV nm
    r = np.linspace(0.012, 0.3, 600)
    K = C / r ** 2; U = -ke2 / r
    ax.plot(r, K, color=fs.ACC, lw=1.3, ls='--', label=r'$\hbar^2/2m_er^2$ (갇힌 운동)')
    ax.plot(r, U, color=fs.FORCE, lw=1.3, ls='--', label=r'$-ke^2/r$')
    ax.plot(r, K + U, color=fs.VEL, lw=1.9, label=r'$E(r)$')
    r0 = 2 * C / ke2
    ax.plot([r0], [C / r0 ** 2 - ke2 / r0], 'o', color=fs.VEL, ms=5)
    ax.annotate(r'$r_0 = 0.0529$ nm, $E = -13.6$ eV', xy=(r0, -13.6), xytext=(0.09, -24), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', color=fs.BLACK, lw=0.8))
    ax.axhline(0, color=fs.BLACK, lw=0.8)
    ax.set_xlim(0, 0.3); ax.set_ylim(-40, 40)
    ax.set_xlabel(r'$r$ (nm)'); ax.set_ylabel('에너지 (eV)')
    ax.legend(fontsize=8, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig36_13')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
        f()
