"""38장 원자와 분자 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse, FancyArrowPatch
from scipy.special import genlaguerre, factorial

RY = 13.605693  # eV
LEV = fs.BLACK
PD = fs.FIELD
LIGHT_C = fs.ORANGE


def clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def photon(ax, p, q, color=LIGHT_C, amp=0.06, nw=4, lw=1.2):
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p; L = np.hypot(*d); u = d / L; n = np.array([-u[1], u[0]])
    t = np.linspace(0, L * 0.85, 200)
    w = amp * np.sin(2 * np.pi * nw * t / (L * 0.85))
    pts = p + np.outer(t, u) + np.outer(w, n)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=4)
    ax.add_patch(FancyArrowPatch(p + u * L * 0.83, q, arrowstyle='-|>', mutation_scale=9, color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


def wl_color(nm):
    """가시광선 파장의 대략적인 색."""
    table = [(380, '#7a00c8'), (420, '#4b00ff'), (440, '#2c5bff'), (490, '#00b3d6'), (510, '#00c853'),
             (580, '#e0c000'), (600, '#ff8a00'), (650, '#e00000'), (750, '#b00000')]
    for (a, ca), (b, cb) in zip(table[:-1], table[1:]):
        if a <= nm <= b:
            return ca if nm - a < b - nm else cb
    return '#555555'


# ---------------------------------------------------------------- 보어 궤도의 정상파
def fig01():
    fig, ax = fs.canvas(2.6, 2.6, xlim=(-1.7, 1.7), ylim=(-1.7, 1.7))
    th = np.linspace(0, 2 * np.pi, 600)
    R, n = 1.1, 4
    ax.plot(R * np.cos(th), R * np.sin(th), ls='--', color=fs.GRAY, lw=0.9)
    r = R + 0.22 * np.cos(n * th)
    ax.plot(r * np.cos(th), r * np.sin(th), color=fs.VEL, lw=1.6)
    fs.charge(ax, (0, 0), +1, r=0.12, fontsize=9)
    ax.text(0, -0.32, '핵', fontsize=8.5, ha='center')
    ax.text(0, 1.55, r'$2\pi r = 4\lambda$ ($n = 4$)', ha='center', fontsize=9.5)
    fs.save(fig, __file__, 'fig38_01')


# ---------------------------------------------------------------- 수소 에너지 준위와 스펙트럼 계열
def fig02():
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    E = lambda n: -RY / n ** 2
    for n in range(1, 7):
        ax.plot([0, 10], [E(n), E(n)], color=LEV, lw=1.0)
        if n <= 4:
            ax.text(10.15, E(n), f'$n={n}$', fontsize=8, va='center')
        if n <= 3:
            ax.text(-0.15, E(n), f'{E(n):.2f}', fontsize=8, va='center', ha='right')
    ax.plot([0, 10], [0, 0], color=LEV, lw=1.0, ls='--')
    ax.text(10.15, 0, r'$n=\infty$', fontsize=8, va='center')
    ax.text(-0.15, 0, '0', fontsize=8, va='center', ha='right')

    def tr(x, ni, nf, col):
        ax.add_patch(FancyArrowPatch((x, E(ni)), (x, E(nf)), arrowstyle='-|>', mutation_scale=8, color=col, lw=1.1, shrinkA=0, shrinkB=0))
    for k, ni in enumerate(range(2, 7)):
        tr(0.5 + 0.35 * k, ni, 1, fs.FIELD)
    ax.text(2.2, -8.0, '라이먼 계열\n(자외선)', fontsize=8.5, color=fs.FIELD, ha='left', va='center')
    for k, ni in enumerate(range(3, 7)):
        lam = 1239.84 / (E(ni) - E(2))
        tr(3.8 + 0.4 * k, ni, 2, wl_color(lam))
    ax.text(4.4, -3.75, '발머 계열(가시광선)', fontsize=8.5, color=fs.FORCE, ha='center', va='top')
    ax.text(3.75, -2.3, r'H$\alpha$', fontsize=7.5, color=wl_color(656), ha='right')
    for k, ni in enumerate(range(4, 7)):
        tr(7.4 + 0.4 * k, ni, 3, fs.GRAY)
    ax.text(7.8, -1.75, '파셴 계열(적외선)', fontsize=8.5, color=fs.GRAY, ha='center', va='top')
    ax.set_xlim(-1.3, 11.2); ax.set_ylim(-14.6, 0.9)
    ax.set_xticks([])
    ax.set_ylabel('에너지 (eV)')
    for s in ('top', 'right', 'bottom'):
        ax.spines[s].set_visible(False)
    ax.set_yticks([])
    fs.save(fig, __file__, 'fig38_02')


# ---------------------------------------------------------------- 유효 퍼텐셜(원심력 장벽)
def fig03():
    fig, ax = fs.plot_axes(4.2, 2.7)
    r = np.linspace(0.05, 20, 1500)
    ax.plot(r, -2 * RY / r, color=fs.BLACK, lw=1.2, ls='--', label=r'$l = 0$ ($-ke^2/r$)')
    for l, col in ((0, fs.VEL), (1, fs.ACC), (2, fs.FORCE)):
        if l == 0:
            continue
        ax.plot(r, RY * (-2 / r + l * (l + 1) / r ** 2), color=col, lw=1.7, label=f'$l = {l}$')
    for n in (2, 3):
        ax.axhline(-RY / n ** 2, color=fs.GRAY, lw=0.7, ls=':')
        ax.text(19.8, -RY / n ** 2 - 0.2, f'$E_{n}$', fontsize=8.5, color=fs.GRAY, ha='right', va='top')
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    ax.set_xlim(0, 20); ax.set_ylim(-16, 8)
    ax.set_xlabel(r'$r/a_0$'); ax.set_ylabel(r'$U_{\mathrm{eff}}$ (eV)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    ax.text(5.5, 4.0, '원심력 장벽\n$l(l+1)\\hbar^2/2\\mu r^2$', fontsize=8.5, color=fs.FORCE)
    fs.save(fig, __file__, 'fig38_03')


# ---------------------------------------------------------------- 1s 지름 확률 밀도
def fig04():
    fig, ax = fs.plot_axes(4.0, 2.5)
    r = np.linspace(0, 6, 600)
    P = 4 * r ** 2 * np.exp(-2 * r)
    m = r <= 1
    ax.fill_between(r[m], P[m], color=PD, alpha=0.25)
    ax.plot(r, P, color=PD, lw=1.8)
    ax.axvline(1, color=fs.VEL, lw=0.9, ls='--')
    ax.axvline(1.5, color=fs.FORCE, lw=0.9, ls='--')
    ax.text(0.95, 0.64, '최빈 반지름 $a_0$', fontsize=8.5, color=fs.VEL, ha='right')
    ax.text(1.58, 0.58, r'$\langle r\rangle = 1.5a_0$', fontsize=8.5, color=fs.FORCE)
    ax.text(0.62, 0.06, '0.323', fontsize=8.5, color=PD, ha='center')
    ax.set_xlim(0, 6); ax.set_ylim(0, 0.7)
    ax.set_xlabel(r'$r/a_0$'); ax.set_ylabel(r'$a_0P(r)$')
    fs.save(fig, __file__, 'fig38_04')


# ---------------------------------------------------------------- 벡터 모형
def fig05():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 3.0))
    for ax, l in zip(axs, (1, 2)):
        ax.set_aspect('equal'); ax.axis('off')
        L = np.sqrt(l * (l + 1))
        th = np.linspace(-np.pi / 2, np.pi / 2, 200)
        ax.plot(L * np.cos(th), L * np.sin(th), ls=':', color=fs.GRAY, lw=0.9)
        ax.plot(-L * np.cos(th), L * np.sin(th), ls=':', color=fs.GRAY, lw=0.9)
        fs.arrow(ax, (0, -L - 0.4), (0, L + 0.55), lw=1.0, ms=9)
        ax.text(0.1, L + 0.5, '$z$', fontsize=10)
        for m in range(-l, l + 1):
            rx = np.sqrt(L ** 2 - m ** 2)
            ax.add_patch(Ellipse((0, m), 2 * rx, 0.28 * rx, fc='none', ec=fs.VEL, lw=0.7, ls='--', alpha=0.8))
            fs.arrow(ax, (0, 0), (rx, m), color=fs.VEL, lw=1.6, ms=9)
            ax.plot([0, rx], [m, m], color=fs.GRAY, lw=0.5)
            ax.text(-L - 0.25, m, f'$m_l = {m:+d}$'.replace('+0', '0'), fontsize=8, ha='right', va='center')
        mm = l
        ang = np.degrees(np.arccos(mm / L))
        fs.angle_arc(ax, (0, 0), 0.45 + 0.2 * l, 90 - ang, 90, r'$\theta$', fontsize=9, tr=0.7 + 0.3 * l)
        ax.text(0, -L - 0.75, f'$l = {l}$:  $L = \\sqrt{{{l * (l + 1)}}}\\,\\hbar$,  ' + r'$\theta_{\min}$' + f' = {ang:.1f}°', ha='center', fontsize=9)
        ax.set_xlim(-L - 1.4, L + 0.5); ax.set_ylim(-L - 0.95, L + 0.7)
    fig.tight_layout(w_pad=0.2)
    fs.save(fig, __file__, 'fig38_05')


# ---------------------------------------------------------------- 오비탈 단면
def fig06():
    fig, axs = plt.subplots(1, 4, figsize=(5.6, 1.8))
    specs = [('1s', 5, lambda x, z, r: np.exp(-r)),
             ('2s', 14, lambda x, z, r: (2 - r) * np.exp(-r / 2)),
             (r'2p$_z$', 14, lambda x, z, r: z * np.exp(-r / 2)),
             (r'3d$_{z^2}$', 22, lambda x, z, r: (3 * z ** 2 - r ** 2) * np.exp(-r / 3))]
    for ax, (name, ext, f) in zip(axs, specs):
        g = np.linspace(-ext, ext, 401)
        X, Z = np.meshgrid(g, g)
        R = np.hypot(X, Z)
        D = f(X, Z, R) ** 2
        D = (D / D.max()) ** 0.45
        ax.imshow(D, extent=(-ext, ext, -ext, ext), origin='lower', cmap='Purples', interpolation='bilinear')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(name, fontsize=9.5)
        ax.text(-ext * 0.92, -ext * 0.92, f'±{ext} $a_0$', fontsize=7, va='bottom', color=fs.GRAY)
        ax.text(ext * 0.08, ext * 0.78, '$z$', fontsize=8)
        ax.plot([0, 0], [ext * 0.6, ext * 0.95], color=fs.BLACK, lw=0.6)
    fig.tight_layout(w_pad=0.3)
    fig.set_dpi(220)
    fs.save(fig, __file__, 'fig38_06')


# ---------------------------------------------------------------- 지름 확률 분포
def Rnl(n, l, r):
    rho = 2 * r / n
    norm = np.sqrt((2 / n) ** 3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    return norm * np.exp(-rho / 2) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def fig07():
    fig, axs = plt.subplots(3, 1, figsize=(4.4, 3.4), sharex=True)
    r = np.linspace(0, 25, 2000)
    groups = [[(1, 0, '1s', fs.VEL)], [(2, 0, '2s', fs.VEL), (2, 1, '2p', fs.FORCE)],
              [(3, 0, '3s', fs.VEL), (3, 1, '3p', fs.FORCE), (3, 2, '3d', fs.ACC)]]
    for ax, grp in zip(axs, groups):
        for n, l, nm, col in grp:
            P = r ** 2 * Rnl(n, l, r) ** 2
            ax.plot(r, P, color=col, lw=1.5, label=nm)
            ra = 0.5 * (3 * n ** 2 - l * (l + 1))
            ax.plot([ra], [0], marker='^', color=col, ms=5, clip_on=False)
        ax.legend(fontsize=8, frameon=False, loc='upper right')
        ax.set_yticks([]); clean(ax)
        ax.set_ylim(0, None)
    axs[1].set_ylabel(r'$P(r) = r^2\lvert R_{nl}\rvert^2$'.replace(r'\lvert', '|').replace(r'\rvert', '|'))
    axs[-1].set_xlabel(r'$r/a_0$'); axs[-1].set_xlim(0, 25)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, __file__, 'fig38_07')


# ---------------------------------------------------------------- 제이만 갈라짐
def fig08():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.3, 7.6), ylim=(-0.7, 3.9))
    ax.plot([0.3, 2.0], [3.0, 3.0], color=LEV, lw=1.6)
    ax.plot([0.3, 2.0], [0.0, 0.0], color=LEV, lw=1.6)
    ax.text(1.15, 3.2, '$l = 1$', ha='center', fontsize=9)
    ax.text(1.15, -0.3, '$l = 0$', ha='center', fontsize=9)
    ax.add_patch(FancyArrowPatch((1.15, 3.0), (1.15, 0.0), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(1.15, -0.6, '$B = 0$', ha='center', fontsize=9.5)
    d = 0.6
    for m in (1, 0, -1):
        y = 3.0 + m * d
        ax.plot([2.0, 2.6], [3.0, y], color=fs.GRAY, lw=0.6, ls=':')
        ax.plot([2.6, 5.6], [y, y], color=LEV, lw=1.6)
        ax.text(5.7, y, f'$m_l = {m:+d}$'.replace('+0', '0'), fontsize=8.5, va='center')
    ax.plot([2.6, 5.6], [0, 0], color=LEV, lw=1.6)
    for k, m in enumerate((1, 0, -1)):
        x = 3.4 + 0.7 * k
        ax.add_patch(FancyArrowPatch((x, 3.0 + m * d), (x, 0.0), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.2, shrinkA=0, shrinkB=0))
    ax.annotate('', xy=(6.95, 3.6), xytext=(6.95, 3.0), arrowprops=dict(arrowstyle='<|-|>', color=fs.VEL, lw=0.8, mutation_scale=7))
    ax.text(7.05, 3.3, r'$\mu_BB$', fontsize=9, color=fs.VEL, va='center')
    ax.text(4.1, -0.6, r'$B \neq 0$: 선 3개', ha='center', fontsize=9.5)
    fs.save(fig, __file__, 'fig38_08')


# ---------------------------------------------------------------- 슈테른–게를라흐
def fig09():
    fig, ax = fs.canvas(5.4, 2.4, xlim=(-0.4, 9.6), ylim=(-2.1, 2.3))
    ax.add_patch(Rectangle((0, -0.5), 1.0, 1.0, fc='#e6b0aa', ec=fs.BLACK, lw=1.0))
    ax.text(0.5, -0.75, '오븐', fontsize=8.5, ha='center', va='top')
    for x in (1.6, 2.1):
        ax.plot([x, x], [0.08, 0.6], color=fs.BLACK, lw=2); ax.plot([x, x], [-0.6, -0.08], color=fs.BLACK, lw=2)
    ax.text(1.85, -0.75, '슬릿', fontsize=8.5, ha='center', va='top')
    # 자석: 위 N극(뾰족), 아래 S극(오목)
    ax.add_patch(Polygon([(3.0, 1.6), (5.6, 1.6), (5.6, 0.75), (4.45, 0.3), (4.15, 0.3), (3.0, 0.75)], fc='#c0392b', ec=fs.BLACK, lw=1.0, alpha=0.85))
    ax.add_patch(Polygon([(3.0, -1.6), (5.6, -1.6), (5.6, -0.45), (4.3, -0.75), (3.0, -0.45)], fc='#2471a3', ec=fs.BLACK, lw=1.0, alpha=0.85))
    ax.text(3.3, 1.2, 'N', color='white', fontsize=10, fontweight='bold')
    ax.text(3.3, -1.3, 'S', color='white', fontsize=10, fontweight='bold')
    ax.text(4.3, -1.75, r'불균일한 자기장 ($\partial B_z/\partial z \neq 0$)', fontsize=8.5, ha='center', va='top')
    # 빔
    xs = np.linspace(1.0, 3.0, 10)
    ax.plot([1.0, 3.0], [0, 0], color=fs.ORANGE, lw=1.6)
    x = np.linspace(3.0, 5.6, 100)
    for s in (1, -1):
        y = s * 0.09 * ((x - 3.0) / 2.6) ** 2 * 2.6
        ax.plot(x, y, color=fs.ORANGE, lw=1.6)
        y_end = y[-1]; slope = s * 0.09 * 2 * 1.0
        ax.plot([5.6, 8.0], [y_end, y_end + slope * 2.4], color=fs.ORANGE, lw=1.6)
    # 스크린
    ax.add_patch(Rectangle((8.0, -1.4), 0.12, 2.8, fc='#bdc3c7', ec=fs.BLACK, lw=0.8))
    ax.text(8.06, -1.5, '검출판', fontsize=8.5, ha='center', va='top')
    ye = 0.09 * 2.6 + 0.18 * 2.4
    for s in (1, -1):
        ax.add_patch(Ellipse((8.06, s * ye), 0.28, 0.2, fc=fs.ORANGE, ec='none'))
    ax.text(8.35, ye, r'$m_s = +\frac{1}{2}$', fontsize=8.5, va='center')
    ax.text(8.35, -ye, r'$m_s = -\frac{1}{2}$', fontsize=8.5, va='center')
    ax.text(8.5, 1.5, '고전적 예상:\n연속된 띠', fontsize=7.5, color=fs.GRAY, ha='left', va='bottom')
    ax.add_patch(Rectangle((9.25, -ye), 0.12, 2 * ye, fc=fs.GRAY, alpha=0.4, ec='none'))
    ax.text(0.5, 0.7, '은 원자', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig38_09')


# ---------------------------------------------------------------- X선 준위
def fig10():
    fig, ax = fs.canvas(3.4, 2.5, xlim=(-0.5, 5.2), ylim=(-0.6, 3.9))
    ys = {'K ($n=1$)': 0.0, 'L ($n=2$)': 2.4, 'M ($n=3$)': 3.2}
    for name, y in ys.items():
        ax.plot([0, 3.6], [y, y], color=LEV, lw=1.4)
        ax.text(3.7, y, name, fontsize=9, va='center')
    for x in (0.6, 1.2, 2.4, 3.0):
        fs.dot(ax, (x, 2.4), r=0.08, color=fs.NEG)
    fs.dot(ax, (1.8, 2.4), r=0.08, color=fs.NEG)
    fs.dot(ax, (0.9, 0.0), r=0.08, color=fs.NEG)
    ax.add_patch(Circle((2.1, 0.0), 0.1, fc='white', ec=fs.NEG, lw=1.2, zorder=6))
    ax.text(2.1, -0.38, '빈자리', fontsize=8, ha='center')
    ax.add_patch(FancyArrowPatch((1.8, 2.3), (2.03, 0.12), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.3, shrinkA=0, shrinkB=0))
    ax.add_patch(FancyArrowPatch((2.7, 3.15), (2.17, 0.12), arrowstyle='-|>', mutation_scale=9, color=fs.FIELD, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(1.55, 1.2, r'K$\alpha$', color=fs.FORCE, fontsize=10, ha='right')
    ax.text(2.6, 1.2, r'K$\beta$', color=fs.FIELD, fontsize=10)
    fs.save(fig, __file__, 'fig38_10')


# ---------------------------------------------------------------- X선 스펙트럼
def fig11():
    fig, ax = fs.plot_axes(4.4, 2.7)
    lam = np.linspace(0.02, 0.25, 2000)
    lka, lkb = 0.1541, 0.1392
    for V, col in ((35, fs.VEL), (25, fs.ACC)):
        lmin = 1.23984 / V
        I = np.where(lam > lmin, (1 / lmin - 1 / lam) / lam ** 2, 0) * 1e-3
        line = (V - 8.98) ** 1.6 * 0.02
        I = I + line * (np.exp(-((lam - lka) / 0.0012) ** 2) + 0.2 * np.exp(-((lam - lkb) / 0.0012) ** 2))
        ax.plot(lam, I, color=col, lw=1.5, label=f'{V} kV')
        ax.annotate(f'$\\lambda_{{\\min}} = {lmin:.4f}$ nm', xy=(lmin, 0), xytext=((0.055, 7.2) if V == 35 else (0.07, 6.0)),
                    fontsize=8, color=col, ha='left', arrowprops=dict(arrowstyle='->', color=col, lw=0.7))
    ax.text(lka + 0.005, 4.4, r'K$\alpha$ (0.154 nm)', fontsize=8.5, ha='left')
    ax.text(lkb - 0.004, 2.0, r'K$\beta$', fontsize=8.5, ha='right')
    ax.set_xlim(0, 0.25); ax.set_ylim(0, 8)
    ax.set_yticks([])
    ax.set_xlabel(r'파장 $\lambda$ (nm)'); ax.set_ylabel('세기 (임의 단위)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig38_12')


# ---------------------------------------------------------------- 모즐리 그림
def fig12():
    fig, ax = fs.plot_axes(4.0, 2.7)
    h = 4.135667696e-15  # eV s
    Z = np.linspace(15, 50, 100)
    f = 10.2 * (Z - 1) ** 2 / h
    ax.plot(Z, np.sqrt(f) / 1e9, color=fs.VEL, lw=1.4, label=r'$E = 10.2\ \mathrm{eV}\,(Z - 1)^2$')
    data = [('Ti', 22, 4.511), ('Cr', 24, 5.415), ('Fe', 26, 6.404), ('Ni', 28, 7.478), ('Cu', 29, 8.048),
            ('Zn', 30, 8.639), ('Mo', 42, 17.479), ('Ag', 47, 22.163)]
    for nm, z, E in data:
        y = np.sqrt(E * 1e3 / h) / 1e9
        ax.plot(z, y, 'o', color=fs.FORCE, ms=4.5)
        if nm in ('Cr', 'Ni', 'Zn'):
            ax.text(z + 0.6, y - 0.12, nm, fontsize=8, ha='left')
        else:
            ax.text(z - 0.6, y + 0.1, nm, fontsize=8, ha='right')
    ax.plot([], [], 'o', color=fs.FORCE, ms=4.5, label=r'측정값(K$\alpha_1$)')
    ax.set_xlim(15, 50); ax.set_ylim(0.8, 2.5)
    ax.set_xlabel('원자번호 $Z$'); ax.set_ylabel(r'$\sqrt{f}$ ($10^9\ \mathrm{Hz}^{1/2}$)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper left')
    fs.save(fig, __file__, 'fig38_11')


# ---------------------------------------------------------------- 흡수, 자발 방출, 유도 방출
def fig13():
    fig, axs = plt.subplots(1, 3, figsize=(5.6, 2.0))
    titles = ['(가) 흡수', '(나) 자발 방출', '(다) 유도 방출']
    for k, (ax, t) in enumerate(zip(axs, titles)):
        ax.set_xlim(-1.6, 1.8); ax.set_ylim(-0.6, 1.7); ax.set_aspect('equal'); ax.axis('off')
        for y, nm in ((0, '$E_1$'), (1.2, '$E_2$')):
            ax.plot([-0.5, 0.5], [y, y], color=LEV, lw=1.4)
            ax.text(-0.6, y, nm, fontsize=9, ha='right', va='center')
        ax.text(0.15, -0.5, t, fontsize=9, ha='center')
        if k == 0:
            photon(ax, (-1.5, 0.6), (-0.15, 0.6))
            ax.add_patch(FancyArrowPatch((0.1, 0.0), (0.1, 1.2), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.3, shrinkA=0, shrinkB=0))
            fs.dot(ax, (0.1, 1.2), r=0.08, color=fs.NEG)
            ax.add_patch(Circle((0.1, 0.0), 0.08, fc='white', ec=fs.NEG, lw=0.9, zorder=6))
        elif k == 1:
            ax.add_patch(FancyArrowPatch((0.0, 1.2), (0.0, 0.0), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.3, shrinkA=0, shrinkB=0))
            photon(ax, (0.25, 0.6), (1.3, 1.45))
            fs.dot(ax, (0.0, 0.0), r=0.08, color=fs.NEG)
            ax.add_patch(Circle((0.0, 1.2), 0.08, fc='white', ec=fs.NEG, lw=0.9, zorder=6))
            ax.text(1.35, 1.0, '방향\n무작위', fontsize=7.5, color=fs.GRAY)
        else:
            photon(ax, (-1.5, 0.6), (-0.15, 0.6))
            ax.add_patch(FancyArrowPatch((0.0, 1.2), (0.0, 0.0), arrowstyle='-|>', mutation_scale=9, color=fs.FORCE, lw=1.3, shrinkA=0, shrinkB=0))
            photon(ax, (0.2, 0.75), (1.6, 0.75))
            photon(ax, (0.2, 0.45), (1.6, 0.45))
            fs.dot(ax, (0.0, 0.0), r=0.08, color=fs.NEG)
            ax.add_patch(Circle((0.0, 1.2), 0.08, fc='white', ec=fs.NEG, lw=0.9, zorder=6))
    fig.tight_layout(w_pad=0.1)
    fs.save(fig, __file__, 'fig38_13')


# ---------------------------------------------------------------- 4준위 레이저
def fig14():
    fig, ax = fs.canvas(4.4, 2.8, xlim=(-1.2, 6.4), ylim=(-0.6, 4.4))
    lv = {0: 0.0, 1: 0.9, 2: 3.0, 3: 3.8}
    names = {0: '$E_0$ (바닥)', 1: '$E_1$ (레이저 아래 준위)', 2: '$E_2$ (준안정)', 3: '$E_3$ (펌핑 준위)'}
    for k, y in lv.items():
        ax.plot([0, 3.0], [y, y], color=LEV, lw=1.4)
        ax.text(3.1, y, names[k], fontsize=8.5, va='center')
    ax.add_patch(Rectangle((0, 3.65), 3.0, 0.3, fc='#e8e8e8', ec='none', zorder=0))
    ax.add_patch(FancyArrowPatch((0.4, 0.0), (0.4, 3.8), arrowstyle='-|>', mutation_scale=12, color=fs.VEL, lw=2.4, shrinkA=0, shrinkB=0))
    ax.text(0.3, 1.9, '펌핑', fontsize=9, color=fs.VEL, ha='right')
    ax.add_patch(FancyArrowPatch((1.2, 3.8), (1.2, 3.0), arrowstyle='-|>', mutation_scale=9, color=fs.GRAY, lw=1.1, ls='--', shrinkA=0, shrinkB=0))
    ax.text(1.32, 3.4, '빠름', fontsize=8, color=fs.GRAY)
    ax.add_patch(FancyArrowPatch((1.9, 3.0), (1.9, 0.9), arrowstyle='-|>', mutation_scale=12, color=fs.FORCE, lw=2.4, shrinkA=0, shrinkB=0))
    ax.text(2.05, 1.95, '레이저 빛\n(유도 방출)', fontsize=8.5, color=fs.FORCE)
    ax.add_patch(FancyArrowPatch((1.2, 0.9), (1.2, 0.0), arrowstyle='-|>', mutation_scale=9, color=fs.GRAY, lw=1.1, ls='--', shrinkA=0, shrinkB=0))
    ax.text(1.32, 0.45, '빠름', fontsize=8, color=fs.GRAY)
    # 원자 수 막대
    for k, n in ((0, 1.0), (1, 0.08), (2, 0.55), (3, 0.04)):
        ax.add_patch(Rectangle((-1.1, lv[k] - 0.1), n * 0.9, 0.2, fc=fs.ACC, ec='none', alpha=0.8))
    ax.text(-0.65, -0.45, '원자 수', fontsize=8, ha='center', color=fs.ACC)
    fs.save(fig, __file__, 'fig38_14')


# ---------------------------------------------------------------- 회전 준위(CO)
def fig15():
    fig, axs = plt.subplots(2, 1, figsize=(4.4, 3.3), gridspec_kw={'height_ratios': [3, 1]})
    ax = axs[0]
    for l in range(6):
        E = l * (l + 1)
        ax.plot([0, 7.5], [E, E], color=LEV, lw=1.1)
        ax.text(7.6, E, f'$l = {l}$', fontsize=8, va='center')
    for l in range(5):
        x = 1.0 + 1.2 * l
        ax.add_patch(FancyArrowPatch((x, l * (l + 1)), (x, (l + 1) * (l + 2)), arrowstyle='-|>', mutation_scale=8, color=fs.FORCE, lw=1.1, shrinkA=0, shrinkB=0))
        ax.text(x + 0.1, (l * (l + 1) + (l + 1) * (l + 2)) / 2, f'{(l + 1) * 115.5:.0f}', fontsize=7, color=fs.FORCE, va='center')
    ax.set_xlim(0, 8.6); ax.set_ylim(-1, 32)
    ax.set_xticks([]); ax.set_yticks([0, 2, 6, 12, 20, 30])
    ax.set_ylabel(r'$E_l$ ($\hbar^2/2I$ 단위)', fontsize=9)
    clean(ax); ax.spines['bottom'].set_visible(False)
    ax = axs[1]
    for l in range(5):
        f = (l + 1) * 115.5
        ax.plot([f, f], [0, 1], color=fs.FORCE, lw=2)
    ax.annotate('', xy=(346.5, 1.25), xytext=(231, 1.25), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=7))
    ax.text(288.75, 1.4, '115.5 GHz', fontsize=8, color=fs.GRAY, ha='center')
    ax.set_xlim(0, 650); ax.set_ylim(0, 1.8); ax.set_yticks([])
    ax.set_xlabel('흡수 진동수 $f$ (GHz)')
    clean(ax); ax.spines['left'].set_visible(False)
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, __file__, 'fig38_15')


# ---------------------------------------------------------------- 분자 퍼텐셜(H2, 모스 모형)
def fig16():
    De, r0, a, hw = 4.75, 0.0741, 19.4, 0.546
    U = lambda r: De * (1 - np.exp(-a * (r - r0))) ** 2 - De
    fig, ax = fs.plot_axes(4.4, 3.0)
    ax.grid(False)
    r = np.linspace(0.035, 0.40, 800)
    ax.plot(r, U(r), color=fs.BLACK, lw=1.7, label='퍼텐셜 에너지 $U(r)$')
    k = 2 * De * a ** 2
    ax.plot(r, 0.5 * k * (r - r0) ** 2 - De, color=fs.GRAY, lw=1.0, ls='--', label='조화 근사')
    v = 0
    while True:
        Ev = hw * (v + 0.5) - (hw * (v + 0.5)) ** 2 / (4 * De) - De
        if Ev > -0.05 or v > 13:
            break
        # 되돌이점
        s = np.sqrt((Ev + De) / De)
        r1 = r0 - np.log(1 + s) / a; r2 = r0 - np.log(1 - s) / a
        ax.plot([r1, r2], [Ev, Ev], color=fs.VEL, lw=0.9)
        v += 1
    E0 = hw * 0.5 - (hw * 0.5) ** 2 / (4 * De) - De
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    ax.annotate('', xy=(0.30, 0), xytext=(0.30, E0), arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=0.9, mutation_scale=8))
    ax.text(0.305, E0 / 2, f'결합 에너지\n$\\approx {-E0:.1f}$ eV', fontsize=8.5, color=fs.FORCE, va='center')
    ax.text(0.095, E0, '$v = 0$', fontsize=8, color=fs.VEL, va='center')
    ax.axvline(r0, color=fs.GRAY, lw=0.6, ls=':')
    ax.text(r0 + 0.004, 1.6, '$r_0$', fontsize=9)
    ax.text(0.16, -3.6, '진동 준위: 위로 갈수록\n간격이 좁아짐', fontsize=8, color=fs.VEL)
    ax.set_xlim(0.03, 0.40); ax.set_ylim(-5.2, 2.0)
    ax.set_xlabel('원자 사이 거리 $r$ (nm)'); ax.set_ylabel('에너지 (eV)')
    ax.legend(fontsize=8, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig38_16')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16):
        f()
