"""37장 양자역학 입문 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyArrowPatch
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal
from scipy.special import eval_hermite, factorial

C = 0.0380998          # hbar^2/(2 m_e), eV nm^2
POT = '#555555'        # 퍼텐셜 곡선
WF = fs.VEL            # 파동함수
PD = fs.FIELD          # 확률 밀도
LEV = fs.GRAY          # 에너지 준위


def clean(ax, grid=False):
    if grid:
        ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def hatch_wall(ax, x0, x1, y0, y1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc='#e5e5e5', ec='none', hatch='///', lw=0, zorder=0))


# ---------------------------------------------------------------- 예제 37.1
def fig01():
    fig, ax = fs.plot_axes(4.0, 2.4)
    x = np.linspace(-3.5, 3.5, 800)
    psi = np.exp(-np.abs(x))
    P = psi ** 2
    m = np.abs(x) < 1
    ax.fill_between(x[m], P[m], color=PD, alpha=0.2)
    ax.plot(x, psi, color=WF, lw=1.3, ls='--', label=r'$\psi\sqrt{a}$')
    ax.plot(x, P, color=PD, lw=1.8, label=r'$a\lvert\psi\rvert^2$'.replace(r'\lvert', '|').replace(r'\rvert', '|'))
    ax.text(0, 0.12, '넓이 0.865', ha='center', fontsize=8.5, color=PD)
    for s in (-1, 1):
        ax.axvline(s, color=fs.GRAY, lw=0.8, ls=':')
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(0, 1.1)
    ax.set_xlabel(r'$x/a$')
    ax.legend(fontsize=9, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig37_01')


# ---------------------------------------------------------------- 허용 영역과 금지 영역
def fig02():
    N = 3000
    x = np.linspace(-3, 12, N); dx = x[1] - x[0]
    U = 20 * (1 - np.exp(-0.5 * x)) ** 2          # 단위: hbar^2/2m = 1
    E, V = eigh_tridiagonal(2 / dx ** 2 + U, -np.ones(N - 1) / dx ** 2, select='i', select_range=(4, 4))
    E = E[0]; psi = V[:, 0]
    psi = psi / np.max(np.abs(psi))
    if psi[np.argmax(np.abs(psi))] < 0:
        psi = -psi
    tp = x[np.where(np.diff(np.sign(U - E)))[0]]
    fig, ax = fs.plot_axes(4.6, 2.7)
    ax.grid(False)
    ax.plot(x, U, color=POT, lw=1.6, label=r'$U(x)$')
    ax.axhline(E, color=LEV, lw=0.9, ls='--')
    ax.plot(x, E + 4.0 * psi, color=WF, lw=1.5, label=r'$\psi(x)$')
    for t in tp:
        ax.axvline(t, color=fs.FORCE, lw=0.8, ls=':')
    ax.axvspan(-3, tp[0], color='#f6e3e1', zorder=0)
    ax.axvspan(tp[1], 12, color='#f6e3e1', zorder=0)
    ax.text((tp[0] + tp[1]) / 2, 23.2, '허용 영역 ($E > U$)\n진동', ha='center', fontsize=8.5)
    ax.text(tp[1] + 0.25, 23.2, '금지 영역\n지수 감소', ha='left', fontsize=8.5, color=fs.FORCE)
    ax.text(-2.85, 23.2, '금지\n영역', ha='left', fontsize=8.5, color=fs.FORCE)
    ax.text(11.8, E + 0.5, r'$E$', fontsize=10, color=LEV, ha='right', va='bottom')
    ax.set_xlim(-3, 12); ax.set_ylim(0, 26)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(r'$x$'); ax.set_ylabel('에너지')
    ax.legend(fontsize=8.5, frameon=False, loc='lower right')
    fs.save(fig, __file__, 'fig37_02')


# ---------------------------------------------------------------- 무한 우물
def fig03():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 3.0), sharey=True)
    x = np.linspace(0, 1, 400)
    for ax, kind in zip(axs, ('psi', 'P')):
        hatch_wall(ax, -0.15, 0, 0, 11.5); hatch_wall(ax, 1, 1.15, 0, 11.5)
        ax.plot([0, 0], [0, 11.5], color=fs.BLACK, lw=1.4); ax.plot([1, 1], [0, 11.5], color=fs.BLACK, lw=1.4)
        ax.plot([0, 1], [0, 0], color=fs.BLACK, lw=1.0)
        for n in (1, 2, 3):
            En = n ** 2
            ax.plot([0, 1], [En, En], color=LEV, lw=0.8, ls='--')
            if kind == 'psi':
                y = np.sqrt(2) * np.sin(n * np.pi * x)
                ax.plot(x, En + 0.9 * y, color=WF, lw=1.5)
                ax.text(1.2, En, f'$n={n}$', fontsize=9, va='center')
            else:
                y = 2 * np.sin(n * np.pi * x) ** 2
                ax.fill_between(x, En, En + 0.9 * y, color=PD, alpha=0.2)
                ax.plot(x, En + 0.9 * y, color=PD, lw=1.5)
                ax.text(1.2, En, ['$E_1$', '$4E_1$', '$9E_1$'][n - 1], fontsize=9.5, va='center')
        ax.set_xlim(-0.15, 1.6); ax.set_ylim(-0.3, 11.5)
        ax.set_xticks([0, 1]); ax.set_xticklabels(['0', r'$L$'])
        ax.set_yticks([])
        for s in ('top', 'right', 'left'):
            ax.spines[s].set_visible(False)
    axs[0].set_title(r'(가) 파동함수 $\psi_n$', fontsize=9.5)
    axs[1].set_title(r'(나) 확률 밀도 $|\psi_n|^2$', fontsize=9.5)
    axs[0].set_ylabel('에너지')
    axs[0].spines['left'].set_visible(True)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig37_03')


# ---------------------------------------------------------------- 대응 원리
def fig04():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.2), sharey=True)
    x = np.linspace(0, 1, 2000)
    for ax, n in zip(axs, (1, 20)):
        P = 2 * np.sin(n * np.pi * x) ** 2
        ax.fill_between(x, P, color=PD, alpha=0.15)
        ax.plot(x, P, color=PD, lw=1.0 if n > 1 else 1.6)
        ax.axhline(1, color=fs.FORCE, ls='--', lw=1.2)
        ax.set_xlim(0, 1); ax.set_ylim(0, 2.3)
        ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', r'$L/2$', r'$L$'])
        ax.set_title(f'$n = {n}$', fontsize=9.5)
        clean(ax)
    axs[0].set_ylabel(r'$L\,|\psi_n|^2$')
    axs[0].text(0.02, 1.07, '고전 $1/L$', fontsize=8, color=fs.FORCE)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'fig37_04')


# ---------------------------------------------------------------- 예제 37.3
def fig05():
    fig, ax = fs.plot_axes(3.8, 2.3)
    ax.grid(False)
    x = np.linspace(0, 1, 600)
    P = 2 * np.sin(np.pi * x) ** 2
    m = (x > 1 / 3) & (x < 2 / 3)
    ax.fill_between(x[m], P[m], color=PD, alpha=0.25)
    ax.plot(x, P, color=PD, lw=1.7)
    ax.axhline(1, color=fs.FORCE, ls='--', lw=1.0)
    ax.text(0.5, 0.55, '$P = 0.609$', ha='center', fontsize=9.5, color=PD)
    ax.text(0.02, 1.07, '고전 $1/L$', fontsize=8, color=fs.FORCE)
    for v in (1 / 3, 2 / 3):
        ax.axvline(v, color=fs.GRAY, lw=0.8, ls=':')
    ax.set_xlim(0, 1); ax.set_ylim(0, 2.2)
    ax.set_xticks([0, 1 / 3, 0.5, 2 / 3, 1]); ax.set_xticklabels(['0', r'$L/3$', r'$L/2$', r'$2L/3$', r'$L$'])
    ax.set_ylabel(r'$L\,|\psi_1|^2$')
    fs.save(fig, __file__, 'fig37_05')


# ---------------------------------------------------------------- 유한 우물(예제 37.4)
def finite_well_states(L, U0):
    z0 = L / 2 * np.sqrt(U0 / C)
    sols = []
    f_even = lambda z: z * np.tan(z) - np.sqrt(z0 ** 2 - z ** 2)
    f_odd = lambda z: -z / np.tan(z) - np.sqrt(z0 ** 2 - z ** 2)
    k = 0
    while k * np.pi / 2 < z0:
        a, b = k * np.pi / 2 + 1e-9, min((k + 1) * np.pi / 2 - 1e-9, z0)
        f = f_even if k % 2 == 0 else f_odd
        try:
            sols.append((brentq(f, a, b), 'even' if k % 2 == 0 else 'odd'))
        except ValueError:
            pass
        k += 1
    return z0, sols


def fig06():
    L, U0 = 1.0, 1.0
    z0, sols = finite_well_states(L, U0)
    fig, ax = fs.plot_axes(4.4, 2.9)
    ax.grid(False)
    x = np.linspace(-1.5, 1.5, 1200)
    ax.plot([-1.5, -0.5, -0.5, 0.5, 0.5, 1.5], [U0, U0, 0, 0, U0, U0], color=POT, lw=1.6)
    for z, kind in sols:
        k = 2 * z / L; E = C * k ** 2; kap = np.sqrt((U0 - E) / C)
        if kind == 'even':
            inside = np.cos(k * x); edge = np.cos(k * L / 2)
            out = edge * np.exp(-kap * (np.abs(x) - L / 2))
        else:
            inside = np.sin(k * x); edge = np.sin(k * L / 2)
            out = np.sign(x) * edge * np.exp(-kap * (np.abs(x) - L / 2))
        psi = np.where(np.abs(x) < L / 2, inside, out)
        psi /= np.max(np.abs(psi))
        ax.plot([-1.5, 1.5], [E, E], color=LEV, lw=0.8, ls='--')
        ax.plot(x, E + 0.2 * psi, color=WF, lw=1.5)
        ax.text(1.52, E, f'{E:.3f} eV', fontsize=8.5, va='center')
    Einf = C * (np.pi / L) ** 2
    ax.plot([-0.5, 0.5], [Einf, Einf], color=fs.FORCE, lw=1.0, ls=':')
    ax.text(0.55, Einf, f'같은 폭 무한 우물의 $E_1$\n({Einf:.3f} eV)', fontsize=7.5, color=fs.FORCE, va='center')
    ax.annotate('', xy=(0.5, 0.1), xytext=(0.72, 0.1), arrowprops=dict(arrowstyle='<|-|>', color=fs.ORANGE, lw=0.8, mutation_scale=7))
    ax.text(0.75, 0.05, r'$\delta = 0.22$ nm', fontsize=8, color=fs.ORANGE)
    ax.text(-1.45, U0 + 0.04, r'$U_0 = 1.0$ eV', fontsize=8.5)
    ax.set_xlim(-1.5, 2.15); ax.set_ylim(-0.08, 1.2)
    ax.set_xlabel(r'$x$ (nm)'); ax.set_ylabel('에너지 (eV)')
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    fs.save(fig, __file__, 'fig37_07')


# ---------------------------------------------------------------- 그래프 풀이
def fig07():
    z0, sols = finite_well_states(1.0, 1.0)
    fig, ax = fs.plot_axes(4.2, 2.8)
    z = np.linspace(0.001, 3.3, 3000)
    zt = z * np.tan(z); zc = -z / np.tan(z)
    zt[np.abs(np.cos(z)) < 0.03] = np.nan
    zc[np.abs(np.sin(z)) < 0.03] = np.nan
    zt[zt < 0] = np.nan; zc[zc < 0] = np.nan
    ax.plot(z, zt, color=fs.VEL, lw=1.6, label=r'$z\tan z$ (짝)')
    ax.plot(z, zc, color=fs.ACC, lw=1.6, label=r'$-z\cot z$ (홀)')
    zz = np.linspace(0, z0, 400)
    ax.plot(zz, np.sqrt(z0 ** 2 - zz ** 2), color=fs.FORCE, lw=1.6, label=r'$\sqrt{z_0^2 - z^2}$')
    for zs, kind in sols:
        ax.plot(zs, np.sqrt(z0 ** 2 - zs ** 2), 'o', color=fs.BLACK, ms=5, zorder=6)
        ax.text(zs + 0.06, np.sqrt(z0 ** 2 - zs ** 2) + 0.12, f'$z = {zs:.2f}$', fontsize=8.5)
    for v in (np.pi / 2, np.pi):
        ax.axvline(v, color=fs.GRAY, lw=0.7, ls=':')
    ax.set_xticks([0, 1, np.pi / 2, 2, z0, 3, np.pi])
    ax.set_xticklabels(['0', '1', r'$\pi/2$', '2', r'$z_0$', '3', r'$\pi$'])
    ax.set_xlim(0, 3.3); ax.set_ylim(0, 4)
    ax.set_xlabel(r'$z = kL/2$')
    ax.legend(fontsize=8, frameon=False, loc='upper left')
    fs.save(fig, __file__, 'fig37_06')


# ---------------------------------------------------------------- 장벽 터널링 파동함수
def barrier_solution(E, U0, a):
    """x<0 입사+반사, 0<x<a 장벽, x>a 투과. (k, kappa, r, A, B, t) 반환."""
    k = np.sqrt(E / C); kap = np.sqrt((U0 - E) / C)
    # 미지수 r, A, B, t: psi = e^{ikx} + r e^{-ikx}; A e^{kx}+B e^{-kx}; t e^{ikx}
    M = np.array([[-1, 1, 1, 0],
                  [1j * k, kap, -kap, 0],
                  [0, np.exp(kap * a), np.exp(-kap * a), -np.exp(1j * k * a)],
                  [0, kap * np.exp(kap * a), -kap * np.exp(-kap * a), -1j * k * np.exp(1j * k * a)]], dtype=complex)
    rhs = np.array([1, 1j * k, 0, 0], dtype=complex)
    r, A, B, t = np.linalg.solve(M, rhs)
    return k, kap, r, A, B, t


def fig08():
    E, U0, a = 2.0, 4.0, 0.30
    k, kap, r, A, B, t = barrier_solution(E, U0, a)
    x = np.linspace(-1.2, 1.5, 2000)
    psi = np.where(x < 0, np.exp(1j * k * x) + r * np.exp(-1j * k * x),
                   np.where(x < a, A * np.exp(kap * x) + B * np.exp(-kap * x), t * np.exp(1j * k * x)))
    fig, ax = fs.plot_axes(4.6, 2.7)
    ax.grid(False)
    ax.add_patch(Rectangle((0, 0), a, 4.6, fc='#ececec', ec='none', zorder=0))
    sc = 0.55
    base = 0.6
    ax.plot(x, base + sc * psi.real, color=WF, lw=1.0, label=r'$\mathrm{Re}\,\psi$')
    ax.plot(x, base + sc * np.abs(psi) ** 2, color=PD, lw=1.7, label=r'$|\psi|^2$')
    ax.axhline(base, color=fs.BLACK, lw=0.6)
    ax.text(-1.15, 3.15, '입사 + 반사', fontsize=8.5)
    ax.text(0.5, 1.15, '투과파', fontsize=8.5)
    ax.text(a / 2, 4.3, '장벽', fontsize=8.5, ha='center')
    ax.text(a / 2, 3.95, r'$U_0 = 4.0$ eV', fontsize=8, ha='center')
    ax.annotate('', xy=(a, 4.75), xytext=(0, 4.75), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=7))
    ax.text(a / 2, 4.95, r'$L = 0.30$ nm', fontsize=8, ha='center', color=fs.GRAY)
    ax.set_xlim(-1.2, 1.5); ax.set_ylim(-0.1, 5.2)
    ax.set_yticks([]); ax.set_xlabel(r'$x$ (nm)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig37_08')
    return abs(t) ** 2


# ---------------------------------------------------------------- 투과 확률 vs 두께
def fig09():
    E, U0 = 1.0, 5.0
    kap = np.sqrt((U0 - E) / C)
    L = np.linspace(0.02, 1.2, 400)
    Tex = 1 / (1 + U0 ** 2 * np.sinh(kap * L) ** 2 / (4 * E * (U0 - E)))
    Tap = 16 * E / U0 * (1 - E / U0) * np.exp(-2 * kap * L)
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.semilogy(L, Tex, color=fs.VEL, lw=1.8, label='정확한 식')
    ax.semilogy(L, Tap, color=fs.FORCE, lw=1.2, ls='--', label=r'근사 $16\frac{E}{U_0}(1-\frac{E}{U_0})e^{-2\kappa L}$')
    for LL, txt in ((0.5, r'$9.1\times10^{-5}$'), (1.0, r'$3.2\times10^{-9}$')):
        Tv = 16 * E / U0 * (1 - E / U0) * np.exp(-2 * kap * LL)
        ax.plot(LL, Tv, 'o', color=fs.BLACK, ms=4)
        ax.text(LL + 0.04, Tv * 2.5, txt, fontsize=8.5)
    ax.set_xlim(0, 1.2); ax.set_ylim(1e-11, 2)
    ax.set_xlabel(r'장벽 두께 $L$ (nm)'); ax.set_ylabel(r'투과 확률 $T$')
    ax.legend(fontsize=8, frameon=False, loc='lower left')
    fs.save(fig, __file__, 'fig37_09')


# ---------------------------------------------------------------- STM
def fig10():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-2.6, 3.4), ylim=(-1.3, 2.4))
    # 시료 표면의 원자
    xs = np.arange(-2.4, 2.6, 0.5)
    for x in xs:
        ax.add_patch(Circle((x, -0.25), 0.25, fc='#d5dbdf', ec=fs.BLACK, lw=0.7, zorder=2))
    ax.add_patch(Rectangle((-2.6, -1.3), 5.2, 0.85, fc='#d5dbdf', ec='none', zorder=1))
    ax.add_patch(Circle((1.0, 0.18), 0.22, fc='#f5b7b1', ec=fs.BLACK, lw=0.7, zorder=2))
    # 탐침
    tip = np.array([0.0, 0.62])
    ax.add_patch(Polygon([(tip[0], tip[1]), (-0.6, 2.3), (0.6, 2.3)], fc='#aab7b8', ec=fs.BLACK, lw=0.9, zorder=3))
    ax.add_patch(Circle(tip + (0, 0.1), 0.12, fc='#aab7b8', ec=fs.BLACK, lw=0.7, zorder=3))
    ax.annotate('', xy=(-0.35, 0.0), xytext=(-0.35, 0.6), arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=0.9, mutation_scale=8))
    ax.text(-0.45, 0.3, r'$d$', fontsize=11, color=fs.FORCE, ha='right', va='center')
    for dx in (-0.05, 0.05):
        ax.annotate('', xy=(dx, 0.02), xytext=(dx, 0.58), arrowprops=dict(arrowstyle='->', color=fs.VEL, lw=0.8))
    ax.text(-2.55, 0.25, r'터널 전류 $I \propto e^{-2\kappa d}$', fontsize=8.5, color=fs.VEL)
    ax.text(0.8, 1.9, '탐침', fontsize=9)
    ax.text(-2.5, -1.1, '시료 표면', fontsize=8.5)
    # 주사 경로
    ax.plot(np.linspace(-2.3, 2.5, 200), 0.72 + 0.05 * np.cos(2 * np.pi * np.linspace(-2.3, 2.5, 200) / 0.5)
            + 0.33 * np.exp(-((np.linspace(-2.3, 2.5, 200) - 1.0) / 0.3) ** 2), ls='--', color=fs.ACC, lw=1.0)
    ax.text(2.55, 0.85, '탐침 높이\n(전류 일정)', fontsize=8, color=fs.ACC, va='center')
    fs.arrow(ax, (-1.9, 1.9), (-1.0, 1.9), color=fs.BLACK, lw=1.0, ms=8)
    ax.text(-1.45, 2.1, '주사 방향', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig37_11')


# ---------------------------------------------------------------- 전계 방출 삼각 장벽
def fig11():
    phi, F = 4.5, 5.0     # eV, V/nm
    w = phi / F
    fig, ax = fs.plot_axes(4.2, 2.6)
    ax.grid(False)
    ax.add_patch(Rectangle((-0.6, -1.5), 0.6, 1.5, fc='#d5dbdf', ec='none'))
    ax.text(-0.3, -1.2, '금속', ha='center', fontsize=9)
    x = np.linspace(0, 1.5, 300)
    ax.plot([-0.6, 0], [0, 0], color=fs.VEL, lw=1.2)
    ax.text(-0.57, -0.35, '페르미 준위', fontsize=8, color=fs.VEL)
    ax.plot([0, 0], [-1.5, phi], color=POT, lw=1.6)
    ax.plot(x, phi - F * x, color=POT, lw=1.6, label=r'$U(x)$')
    ax.plot(x, phi + 0 * x, color=POT, lw=0.8, ls=':')
    ax.text(1.0, phi + 0.15, '전기장이 없을 때', fontsize=8, color=fs.GRAY)
    xx = np.linspace(0, w, 100)
    ax.fill_between(xx, 0, phi - F * xx, color=fs.FORCE, alpha=0.15)
    ax.annotate('', xy=(w, -0.35), xytext=(0, -0.35), arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=0.8, mutation_scale=7))
    ax.text(w / 2, -0.75, f'장벽 폭 $\\phi/e\\mathcal{{E}} = {w:.2f}$ nm', fontsize=8.5, color=fs.FORCE, ha='center')
    ax.annotate('', xy=(0.05, phi), xytext=(0.05, 0), arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(0.1, phi / 2 + 0.5, r'$\phi$', fontsize=11)
    fs.arrow(ax, (-0.35, 0.0), (1.3, 0.0), color=fs.NEG, lw=1.2, ms=9, ls='--')
    ax.text(1.32, 0.0, '터널링', fontsize=8.5, color=fs.NEG, va='center')
    ax.set_xlim(-0.6, 1.6); ax.set_ylim(-1.5, 5.4)
    ax.set_xlabel(r'표면에서의 거리 $x$ (nm)'); ax.set_ylabel('에너지 (eV)')
    ax.set_yticks([0, phi]); ax.set_yticklabels(['$E$', r'$E + \phi$'])
    fs.save(fig, __file__, 'fig37_10')


# ---------------------------------------------------------------- 조화 진동자
def ho_psi(n, x):
    return (1 / np.sqrt(2 ** n * factorial(n) * np.sqrt(np.pi))) * eval_hermite(n, x) * np.exp(-x ** 2 / 2)


def fig12():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 3.0), gridspec_kw={'width_ratios': [1.35, 1]})
    ax = axs[0]
    x = np.linspace(-4.2, 4.2, 800)
    ax.plot(x, x ** 2 / 2, color=POT, lw=1.6)
    for n in range(5):
        E = n + 0.5
        xt = np.sqrt(2 * E)
        ax.plot([-xt, xt], [E, E], color=LEV, lw=0.8, ls='--')
        ax.plot(x, E + 0.55 * ho_psi(n, x) / 0.75, color=WF, lw=1.3)
        ax.text(4.3, E, f'$n={n}$', fontsize=8.5, va='center')
    ax.annotate('', xy=(-3.6, 1.5), xytext=(-3.6, 0.5), arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=0.8, mutation_scale=7))
    ax.text(-3.7, 1.0, r'$\hbar\omega$', fontsize=9.5, color=fs.FORCE, ha='right', va='center')
    ax.set_xlim(-4.6, 5.0); ax.set_ylim(0, 5.6)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5]); ax.set_yticklabels(['1/2', '3/2', '5/2', '7/2', '9/2'])
    ax.set_ylabel(r'$E/\hbar\omega$'); ax.set_xlabel(r'$x/b$')
    ax.set_title(r'(가) 준위와 파동함수', fontsize=9.5)
    clean(ax)
    ax = axs[1]
    P = ho_psi(0, x) ** 2
    ax.plot(x, P, color=PD, lw=1.7)
    for m in (x < -1, x > 1):
        ax.fill_between(x[m], P[m], color=fs.FORCE, alpha=0.3)
    for v in (-1, 1):
        ax.axvline(v, color=fs.GRAY, lw=0.8, ls=':')
    ax.text(2.0, 0.22, '합 0.157', fontsize=8.5, color=fs.FORCE, ha='center')
    ax.annotate('', xy=(1.4, 0.05), xytext=(2.0, 0.19), arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.7))
    ax.set_xlim(-3, 3); ax.set_ylim(0, 0.65)
    ax.set_xticks([-1, 0, 1]); ax.set_xticklabels([r'$-b$', '0', r'$b$'])
    ax.set_yticks([]); ax.set_xlabel(r'$x$')
    ax.set_title(r'(나) $|\psi_0|^2$와 금지 영역', fontsize=9.5)
    clean(ax)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'fig37_12')


# ---------------------------------------------------------------- 연습문제 14: 중첩 상태
def fig13():
    fig, ax = fs.plot_axes(4.2, 2.5)
    x = np.linspace(0, 1, 500)
    p1 = np.sqrt(2) * np.sin(np.pi * x); p2 = np.sqrt(2) * np.sin(2 * np.pi * x)
    cols = (fs.VEL, fs.GRAY, fs.FORCE)
    for ph, col, lab in ((0, cols[0], r'$\omega_{21}t = 0$'), (np.pi / 2, cols[1], r'$\pi/2$'), (np.pi, cols[2], r'$\pi$')):
        P = 0.5 * (p1 ** 2 + p2 ** 2) + p1 * p2 * np.cos(ph)
        ax.plot(x, P, color=col, lw=1.6, ls='--' if ph == np.pi / 2 else '-', label=lab)
        xm = 0.5 - 16 / (9 * np.pi ** 2) * np.cos(ph)
        ax.plot([xm], [0.05], marker='^', color=col, ms=7)
    ax.set_xlim(0, 1); ax.set_ylim(0, 3.6)
    ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', r'$L/2$', r'$L$'])
    ax.set_ylabel(r'$L\,|\Psi|^2$')
    ax.legend(fontsize=8.5, frameon=False, loc='upper center', ncol=3)
    fs.save(fig, __file__, 'fig37_13')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
        f()
