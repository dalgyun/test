"""39장 고체와 반도체 그림. python3 figures/ch39/make_figs.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools'))
import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch

kB = 8.617333e-5          # eV/K
CB = '#d6e4f5'            # 전도띠 채움(빈 띠)
VBF = '#8fb3de'           # 전자로 찬 띠
EL = fs.NEG               # 전자(파랑)
HO = fs.POS               # 양공(빨강)


# ---------------------------------------------------------------- 공통 도우미
def P3(x, y, z, k=0.42, ang=30):
    """비스듬한 투영: x 오른쪽, y 깊이(오른쪽 위), z 위."""
    a = np.radians(ang)
    return np.array([x + k * y * np.cos(a), z + k * y * np.sin(a)])


def cube_edges(ax, o=(0, 0), s=1.0, k=0.42):
    V = {}
    for i in (0, 1):
        for j in (0, 1):
            for l in (0, 1):
                V[(i, j, l)] = P3(i, j, l, k) * s + o
    hidden = (0, 1, 0)   # 뒤쪽 아래 왼쪽 꼭짓점
    for a in V:
        for b in V:
            if sum(abs(np.array(a) - np.array(b))) == 1 and a < b:
                ls = '--' if hidden in (a, b) else '-'
                ax.plot([V[a][0], V[b][0]], [V[a][1], V[b][1]], color=fs.BLACK, lw=0.8, ls=ls, zorder=1)


def atom(ax, p, r, color, z=3):
    ax.add_patch(Circle(p, r, fc=color, ec=fs.BLACK, lw=0.6, zorder=z))
    ax.add_patch(Circle((p[0] - r * 0.3, p[1] + r * 0.3), r * 0.3, fc='white', ec='none', alpha=0.5, zorder=z + 0.1))


def electron(ax, p, r=0.07):
    ax.add_patch(Circle(p, r, fc=EL, ec='none', zorder=8))


def hole(ax, p, r=0.07):
    ax.add_patch(Circle(p, r, fc='white', ec=HO, lw=1.1, zorder=8))


# ---------------------------------------------------------------- 그림 39.1 단위 세포
def fig01():
    fig, axs = plt.subplots(1, 3, figsize=(5.5, 2.25))
    k = 0.42
    corners = [(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)]
    face = [(.5, .5, 0), (.5, .5, 1), (.5, 0, .5), (.5, 1, .5), (0, .5, .5), (1, .5, .5)]
    inner = [(.25, .25, .25), (.75, .75, .25), (.75, .25, .75), (.25, .75, .75)]
    titles = ['체심 입방(bcc)\n단위 세포당 2개', '면심 입방(fcc)\n단위 세포당 4개', '다이아몬드 구조\n단위 세포당 8개']
    for n, ax in enumerate(axs):
        ax.set_xlim(-0.35, 1.6); ax.set_ylim(-0.25, 1.45); ax.set_aspect('equal'); ax.axis('off')
        cube_edges(ax, k=k)
        atoms = [(c, '#9aa9b8', 0.085) for c in corners]
        if n == 0:
            atoms.append(((.5, .5, .5), fs.FORCE, 0.1))
        else:
            atoms += [(f, fs.ACC, 0.085) for f in face]
        if n == 2:
            atoms += [(q, fs.ORANGE, 0.075) for q in inner]
            sites = corners + face
            for q in inner:
                for s in sites:
                    if abs(np.linalg.norm(np.subtract(q, s)) - np.sqrt(3) / 4) < 1e-6:
                        a, b = P3(*q, k), P3(*s, k)
                        ax.plot([a[0], b[0]], [a[1], b[1]], color=fs.ORANGE, lw=1.6, zorder=2)
        atoms.sort(key=lambda t: -t[0][1])           # 뒤쪽(y 큰 것)부터
        for i, (c, col, r) in enumerate(atoms):
            atom(ax, P3(*c, k), r, col, z=3 + i * 0.01)
        ax.text(0.7, -0.2, titles[n], ha='center', va='top', fontsize=9)
    fs.dim(axs[0], P3(0, 0, 0, k), P3(0, 0, 1, k), r'$a$', off=0.13, fontsize=10)
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, __file__, 'fig39_01')


# ---------------------------------------------------------------- 그림 39.2 상태 세기
def fig02():
    fig, ax = fs.canvas(3.0, 2.9, xlim=(-0.6, 9.6), ylim=(-0.9, 9.4))
    R = 7.3
    for nx in range(1, 10):
        for ny in range(1, 10):
            inside = nx ** 2 + ny ** 2 <= R ** 2
            ax.add_patch(Circle((nx, ny), 0.16, fc=fs.VEL if inside else 'white', ec=fs.VEL, lw=0.8, zorder=3))
    th = np.linspace(0, np.pi / 2, 200)
    ax.fill(np.r_[0, R * np.cos(th)], np.r_[0, R * np.sin(th)], color=fs.SURF, alpha=0.35, zorder=1)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.ORANGE, lw=1.4, zorder=2)
    fs.arrow(ax, (0, 0), (9.4, 0), lw=1.0, ms=9); fs.arrow(ax, (0, 0), (0, 9.3), lw=1.0, ms=9)
    ax.text(9.45, -0.45, r'$n_x$', fontsize=11, ha='center')
    ax.text(0.5, 9.1, r'$n_y$', fontsize=11, ha='center')
    a = np.radians(62)
    fs.arrow(ax, (0, 0), (R * np.cos(a), R * np.sin(a)), color=fs.ORANGE, lw=1.1, ms=9)
    ax.text(R * np.cos(a) * 0.5 - 0.65, R * np.sin(a) * 0.5 + 0.35, r'$R$', color=fs.ORANGE, fontsize=12)
    for i in (1, 5, 9):
        ax.text(i, -0.5, str(i), ha='center', va='top', fontsize=8, color=fs.GRAY)
        if i < 9:
            ax.text(-0.25, i, str(i), ha='right', va='center', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig39_02')


# ---------------------------------------------------------------- 그림 39.3 페르미-디랙 분포와 g(E)f(E)
def fig03():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.4), gridspec_kw={'width_ratios': [1.05, 1]})
    for a in (a1, a2):
        a.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    dE = np.linspace(-0.6, 0.6, 1201)
    for T, c in ((0, fs.BLACK), (300, fs.VEL), (1000, fs.ACC), (3000, fs.FORCE)):
        if T == 0:
            f = (dE < 0).astype(float)
            a1.plot(dE, f, color=c, lw=1.2, label=r'$T = 0$')
        else:
            f = 1 / (np.exp(dE / (kB * T)) + 1)
            a1.plot(dE, f, color=c, label=fr'$T = {T}$ K')
    a1.plot(0, 0.5, 'o', color=fs.BLACK, ms=3.5, zorder=5)
    a1.text(0.04, 0.53, r'$f = \frac{1}{2}$', fontsize=9)
    a1.set_xlabel(r'$E - E_F$ (eV)', fontsize=9); a1.set_ylabel(r'$f(E)$', fontsize=10)
    a1.set_xlim(-0.6, 0.6); a1.set_ylim(-0.03, 1.08)
    a1.legend(fontsize=7.5, loc='lower left', frameon=False)
    a1.tick_params(labelsize=8)
    a1.set_title('(가) 페르미–디랙 분포', fontsize=9)
    # (나) 상태 밀도와 채워진 상태
    EF = 7.0
    E = np.linspace(0, 9, 900)
    g = np.sqrt(E)
    kT = 0.05 * EF
    f = 1 / (np.exp((E - EF) / kT) + 1)
    a2.plot(E, g, color=fs.BLACK, lw=1.2, label=r'$g(E) \propto \sqrt{E}$')
    a2.fill_between(E, 0, g * (E <= EF), color=fs.VEL, alpha=0.18, lw=0, label=r'$T = 0$에서 찬 상태')
    a2.plot(E, g * f, color=fs.FORCE, lw=1.2, label=r'$g(E)f(E)$, $T > 0$')
    a2.axvline(EF, color=fs.GRAY, lw=0.8, ls='--')
    a2.text(EF + 0.1, 0.25, r'$E_F$', fontsize=10)
    a2.set_xlabel(r'$E$ (eV)', fontsize=9); a2.set_ylabel('상태 밀도 (상대값)', fontsize=8)
    a2.set_xlim(0, 9); a2.set_ylim(0, 3.4); a2.set_yticks([])
    a2.legend(fontsize=7, loc='upper left', frameon=False)
    a2.tick_params(labelsize=8)
    a2.set_title(r'(나) 구리 ($E_F = 7.0$ eV)', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig39_03')


# ---------------------------------------------------------------- 그림 39.4 준위가 띠로 갈라짐
def levels(Ecen, t, N):
    k = np.arange(1, N + 1)
    return Ecen - 2 * t * np.cos(k * np.pi / (N + 1))


def fig04():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.8), gridspec_kw={'width_ratios': [1, 1.35]})
    # (가) 원자 수에 따른 준위
    a1.axis('off'); a1.set_xlim(-0.3, 4.3); a1.set_ylim(-0.4, 4.3)
    E_up, E_lo = 3.0, 1.0
    for i, (N, lab) in enumerate(((1, '1개'), (2, '2개'), (6, '6개'), (60, r'$N$개'))):
        x0 = i * 1.05
        for Ec, t in ((E_up, 0.32), (E_lo, 0.08)):
            for E in levels(Ec, t, N):
                a1.plot([x0, x0 + 0.75], [E, E], color=fs.VEL, lw=1.0 if N < 60 else 0.5)
        a1.text(x0 + 0.37, 0.3, lab, ha='center', fontsize=8.5)
    a1.text(-0.25, E_up, '바깥\n준위', fontsize=7.5, ha='right', va='center')
    a1.text(-0.25, E_lo, '안쪽\n준위', fontsize=7.5, ha='right', va='center')
    a1.text(2.05, -0.2, '원자 수', ha='center', fontsize=8.5)
    a1.text(2.05, 4.2, '(가) 원자 수와 준위', ha='center', fontsize=9)
    # (나) 원자 사이 거리에 따른 띠
    r = np.linspace(0.85, 3.2, 400)
    r0 = 1.0
    N = 24
    for Ec, t0, lam in ((3.0, 0.45, 0.45), (1.0, 0.18, 0.22)):
        t = t0 * np.exp(-(r - r0) / lam)
        Ls = np.array([levels(Ec, tt, N) for tt in t])
        a2.fill_between(r, Ls.min(1), Ls.max(1), color=fs.VEL, alpha=0.18, lw=0)
        for j in range(0, N, 3):
            a2.plot(r, Ls[:, j], color=fs.VEL, lw=0.5)
        a2.plot(r, Ls[:, 0], color=fs.VEL, lw=0.9); a2.plot(r, Ls[:, -1], color=fs.VEL, lw=0.9)
    ra = 1.25
    a2.axvline(ra, color=fs.GRAY, ls='--', lw=0.8)
    a2.text(ra, -0.05, r'$a$', ha='center', va='top', fontsize=10)
    tu = 0.45 * np.exp(-(ra - r0) / 0.45); tl = 0.18 * np.exp(-(ra - r0) / 0.22)
    top_lo = 1.0 + 2 * tl; bot_up = 3.0 - 2 * tu
    fs.arrow(a2, (ra + 0.08, top_lo), (ra + 0.08, bot_up), style='<|-|>', color=fs.FORCE, lw=0.9, ms=7)
    a2.text(ra + 0.14, (top_lo + bot_up) / 2, r'$E_g$', color=fs.FORCE, fontsize=10, va='center')
    a2.text(2.9, 3.12, '바깥 껍질', fontsize=7.5, ha='center', va='bottom')
    a2.text(2.9, 1.12, '안쪽 껍질', fontsize=7.5, ha='center', va='bottom')
    a2.set_xlim(0.85, 3.2); a2.set_ylim(0, 4.3)
    a2.set_xticks([]); a2.set_yticks([])
    for s in ('top', 'right'):
        a2.spines[s].set_visible(False)
    a2.set_xlabel('원자 사이 거리 $r$', fontsize=9); a2.set_ylabel('에너지', fontsize=9)
    a2.set_title('(나) 원자 사이 거리와 띠', fontsize=9)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig39_04')


# ---------------------------------------------------------------- 그림 39.5 브래그 조건의 정상파
def fig05():
    fig, axs = plt.subplots(3, 1, figsize=(4.4, 3.2), sharex=True, gridspec_kw={'height_ratios': [1, 1, 1]})
    x = np.linspace(-0.5, 4.5, 1000)
    ions = np.arange(0, 5)
    U = np.zeros_like(x)
    for xi in ions:
        U -= 1 / np.sqrt((x - xi) ** 2 + 0.02)
    U = (U - U.max()) / (U.max() - U.min())
    axs[0].plot(x, U, color=fs.BLACK, lw=1.0)
    axs[0].set_ylim(-1.1, 0.45)
    axs[0].set_ylabel(r'$U(x)$', fontsize=9)
    c = np.cos(np.pi * x) ** 2; s = np.sin(np.pi * x) ** 2
    axs[1].fill_between(x, 0, c, color=fs.VEL, alpha=0.25, lw=0); axs[1].plot(x, c, color=fs.VEL)
    axs[1].axhline(0.5, color=fs.GRAY, ls=':', lw=0.9)
    axs[1].set_ylabel(r'$\cos^2\frac{\pi x}{a}$', fontsize=9)
    axs[1].text(4.55, 0.95, '양이온 위에 몰림\n(에너지 낮음)', fontsize=7.5, va='top', ha='left')
    axs[2].fill_between(x, 0, s, color=fs.FORCE, alpha=0.2, lw=0); axs[2].plot(x, s, color=fs.FORCE)
    axs[2].axhline(0.5, color=fs.GRAY, ls=':', lw=0.9)
    axs[2].set_ylabel(r'$\sin^2\frac{\pi x}{a}$', fontsize=9)
    axs[2].text(4.55, 0.95, '양이온 사이에 몰림\n(에너지 높음)', fontsize=7.5, va='top', ha='left')
    axs[1].text(4.55, 0.42, '점선: 진행파\n$|e^{ikx}|^2$', fontsize=7.5, va='top', ha='left', color=fs.GRAY)
    for a in axs:
        for xi in ions:
            a.axvline(xi, color=fs.GRAY, lw=0.4)
        a.set_yticks([]); a.set_xlim(-0.5, 4.5)
        for sp in ('top', 'right'):
            a.spines[sp].set_visible(False)
    for a in axs[1:]:
        a.set_ylim(0, 1.1)
    for xi in ions:
        axs[0].add_patch(Circle((xi, 0.25), 0.09, fc=fs.POS, ec='none', transform=axs[0].transData, zorder=5))
    axs[2].set_xticks(ions)
    axs[2].set_xticklabels(['0', r'$a$', r'$2a$', r'$3a$', r'$4a$'], fontsize=9)
    axs[2].set_xlabel(r'$x$', fontsize=10)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, __file__, 'fig39_05')


# ---------------------------------------------------------------- 그림 39.6 크로니히-페니 (본문 코드)
def fig06():
    P = 3 * np.pi / 2
    x = np.linspace(1e-6, 4 * np.pi, 200001)
    f = np.cos(x) + P * np.sin(x) / x
    E = (x / np.pi) ** 2
    allowed = np.abs(f) <= 1
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.7), gridspec_kw={'width_ratios': [1.25, 1]})
    for a in (a1, a2):
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    a1.axhspan(-1, 1, color=fs.ACC, alpha=0.12, lw=0)
    a1.plot(x / np.pi, f, color=fs.BLACK, lw=1.1)
    a1.plot(x / np.pi, np.where(allowed, f, np.nan), color=fs.ACC, lw=2.4)
    a1.axhline(1, color=fs.ACC, lw=0.7, ls='--'); a1.axhline(-1, color=fs.ACC, lw=0.7, ls='--')
    a1.set_xlim(0, 3.2); a1.set_ylim(-1.8, 5.5)
    a1.set_xlabel(r'$\alpha a/\pi$', fontsize=9)
    a1.set_ylabel(r'$\cos\alpha a + P\,\sin\alpha a/\alpha a$', fontsize=8.5)
    a1.text(1.6, 4.6, r'$P = 3\pi/2$', fontsize=9)
    a1.text(0.08, -0.5, '허용 띠', fontsize=8, color=fs.ACC, va='center')
    a1.tick_params(labelsize=8)
    a1.set_title('(가) 허용 조건 $|\\cdots| \\leq 1$', fontsize=9)
    ka = np.arccos(np.clip(f, -1, 1)) / np.pi
    q = np.linspace(0, 1, 200)
    for e in (q ** 2, (2 - q) ** 2, (2 + q) ** 2):
        a2.plot(q, e, '--', color=fs.GRAY, lw=0.8)
    seg = np.split(np.arange(x.size), np.flatnonzero(np.diff(allowed.astype(int))) + 1)
    for idx in seg:
        if allowed[idx[0]]:
            a2.plot(ka[idx], E[idx], color=fs.VEL, lw=1.8)
    edges = E[np.flatnonzero(np.diff(allowed.astype(int)))]
    for lo, hi in ((edges[1], edges[2]), (edges[3], edges[4])):
        a2.axhspan(lo, hi, color=fs.FORCE, alpha=0.12, lw=0)
    a2.text(0.5, (edges[1] + edges[2]) / 2, '띠 간격', fontsize=8, color=fs.FORCE, ha='center', va='center')
    a2.text(0.5, (edges[3] + edges[4]) / 2, '띠 간격', fontsize=8, color=fs.FORCE, ha='center', va='center')
    a2.set_xlim(0, 1); a2.set_ylim(0, 10)
    a2.set_xlabel(r'$ka/\pi$', fontsize=9); a2.set_ylabel(r'$E/E_1$', fontsize=9)
    a2.tick_params(labelsize=8)
    a2.set_title('(나) 띠 구조 $E$–$k$', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig39_06')


# ---------------------------------------------------------------- 그림 39.7 도체·부도체·반도체
def band(ax, x, y0, y1, w=1.3, fill=0.0, fc=CB):
    ax.add_patch(Rectangle((x, y0), w, y1 - y0, fc=fc, ec=fs.BLACK, lw=0.9, zorder=2))
    if fill > 0:
        ax.add_patch(Rectangle((x, y0), w, (y1 - y0) * fill, fc=VBF, ec='none', zorder=3))
        ax.add_patch(Rectangle((x, y0), w, y1 - y0, fc='none', ec=fs.BLACK, lw=0.9, zorder=4))


def fig07():
    fig, ax = fs.canvas(5.3, 2.9, xlim=(-0.4, 6.4), ylim=(-0.75, 3.75))
    # 도체
    band(ax, 0, 0.0, 0.9, fill=1.0)
    band(ax, 0, 1.45, 3.3, fill=0.45)
    ax.plot([-0.15, 1.45], [1.45 + 1.85 * 0.45] * 2, color=fs.FORCE, ls='--', lw=1.0, zorder=5)
    ax.text(1.5, 1.45 + 1.85 * 0.45, r'$E_F$', color=fs.FORCE, va='center', fontsize=10)
    ax.text(0.65, 2.75, '부분적으로\n찬 띠', ha='center', va='center', fontsize=8)
    # 부도체
    band(ax, 2.35, 0.0, 1.1, fill=1.0)
    band(ax, 2.35, 2.75, 3.3)
    fs.arrow(ax, (3.0, 1.12), (3.0, 2.73), style='<|-|>', lw=0.9, ms=7)
    ax.text(3.08, 1.93, '$E_g$ 큼\n(다이아몬드\n5.5 eV)', fontsize=7.5, va='center')
    ax.text(2.95, 3.03, '전도띠', ha='center', va='center', fontsize=8)
    ax.text(2.95, 0.55, '원자가띠', ha='center', va='center', fontsize=8, color='white')
    # 반도체
    band(ax, 4.7, 0.0, 1.6, fill=1.0)
    band(ax, 4.7, 2.15, 3.3)
    fs.arrow(ax, (5.35, 1.62), (5.35, 2.13), style='<|-|>', lw=0.9, ms=6)
    ax.text(5.45, 1.88, '$E_g$ 작음 (Si 1.12 eV)', fontsize=7.5, va='center')
    for xe in (4.95, 5.4, 5.75):
        electron(ax, (xe, 2.27))
    for xh in (5.05, 5.55):
        ax.add_patch(Circle((xh, 1.48), 0.07, fc=CB, ec=HO, lw=1.1, zorder=8))
    ax.text(5.35, 3.03, '전도띠', ha='center', va='center', fontsize=8)
    ax.text(5.35, 0.75, '원자가띠', ha='center', va='center', fontsize=8, color='white')
    for x, t in ((0.65, '도체(금속)'), (3.0, '부도체'), (5.35, '반도체')):
        ax.text(x, -0.3, t, ha='center', va='center', fontsize=10)
    ax.text(0.65, 0.45, '찬 띠', ha='center', va='center', fontsize=8, color='white')
    fs.arrow(ax, (-0.35, 0), (-0.35, 3.6), lw=0.9, ms=8)
    ax.text(-0.3, 3.68, '$E$', fontsize=10, va='bottom')
    # 범례
    ax.add_patch(Rectangle((1.2, -0.68), 0.25, 0.16, fc=VBF, ec=fs.BLACK, lw=0.6))
    ax.text(1.5, -0.6, '전자로 찬 상태', fontsize=7.5, va='center')
    ax.add_patch(Rectangle((3.15, -0.68), 0.25, 0.16, fc=CB, ec=fs.BLACK, lw=0.6))
    ax.text(3.45, -0.6, '빈 상태', fontsize=7.5, va='center')
    electron(ax, (4.45, -0.6)); ax.text(4.55, -0.6, '전자', fontsize=7.5, va='center')
    ax.add_patch(Circle((5.1, -0.6), 0.07, fc='white', ec=HO, lw=1.1)); ax.text(5.2, -0.6, '양공', fontsize=7.5, va='center')
    fs.save(fig, __file__, 'fig39_07')


# ---------------------------------------------------------------- 그림 39.8 도핑의 결합 그림
def lattice_panel(ax, center_label, center_color, kind):
    ax.set_xlim(-0.6, 4.6); ax.set_ylim(-0.6, 4.9); ax.set_aspect('equal'); ax.axis('off')
    for i in range(5):
        for j in range(5):
            if i < 4:
                for d in (-0.06, 0.06):
                    ax.plot([i + 0.2, i + 0.8], [j + d, j + d], color=fs.GRAY, lw=0.8, zorder=1)
            if j < 4:
                for d in (-0.06, 0.06):
                    ax.plot([i + d, i + d], [j + 0.2, j + 0.8], color=fs.GRAY, lw=0.8, zorder=1)
    for i in range(5):
        for j in range(5):
            if (i, j) == (2, 2):
                continue
            ax.add_patch(Circle((i, j), 0.21, fc='#dfe6ee', ec=fs.BLACK, lw=0.7, zorder=3))
            ax.text(i, j, 'Si', fontsize=6.5, ha='center', va='center', zorder=4)
    ax.add_patch(Circle((2, 2), 0.25, fc=center_color, ec=fs.BLACK, lw=0.8, zorder=3))
    ax.text(2, 2, center_label, fontsize=7.5, ha='center', va='center', color='white', zorder=4, fontweight='bold')
    if kind == 'n':
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(2 + 1.45 * np.cos(th), 2 + 1.45 * np.sin(th), color=EL, lw=0.9, ls='--', zorder=2)
        pe = (2 + 1.45 * np.cos(0.42), 2 + 1.45 * np.sin(0.42))
        electron(ax, pe, r=0.1)
        ax.annotate('여분의 전자', xy=pe, xytext=(3.3, 4.6), fontsize=8, color=EL, ha='center',
                    arrowprops=dict(arrowstyle='-', lw=0.6, color=EL))
    else:
        # 오른쪽 결합 하나에 전자가 하나 빠짐(양공)
        ax.add_patch(Rectangle((2.2, 1.9), 0.6, 0.2, fc='white', ec='none', zorder=1.5))
        ax.plot([2.2, 2.8], [1.94, 1.94], color=fs.GRAY, lw=0.8, zorder=1.6)
        hole(ax, (2.5, 2.08), r=0.09)
        ax.text(2.6, 2.45, '양공', fontsize=8, color=HO, ha='left')


def fig08():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.75))
    lattice_panel(a1, 'P', fs.ORANGE, 'n')
    lattice_panel(a2, 'B', fs.ACC, 'p')
    a1.set_title('(가) n형: 인(15족)', fontsize=9)
    a2.set_title('(나) p형: 붕소(13족)', fontsize=9)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig39_08')


# ---------------------------------------------------------------- 그림 39.9 주개·받개 준위
def fig09():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.5))
    for a, kind in ((a1, 'n'), (a2, 'p')):
        a.set_xlim(-0.3, 4.3); a.set_ylim(-0.75, 3.8); a.axis('off')
        a.add_patch(Rectangle((0, 2.4), 4, 1.2, fc=CB, ec='none'))
        a.add_patch(Rectangle((0, -0.6), 4, 1.2, fc=VBF, ec='none'))
        a.plot([0, 4], [2.4, 2.4], color=fs.BLACK, lw=1.1); a.plot([0, 4], [0.6, 0.6], color=fs.BLACK, lw=1.1)
        a.text(4.05, 2.4, r'$E_c$', va='center', fontsize=10); a.text(4.05, 0.6, r'$E_v$', va='center', fontsize=10)
        a.text(0.1, 3.3, '전도띠', fontsize=8, va='center'); a.text(0.1, -0.35, '원자가띠', fontsize=8, va='center', color='white')
        xs = [0.6, 1.4, 2.2, 3.0]
        if kind == 'n':
            yd = 2.1
            for i, x in enumerate(xs):
                a.plot([x - 0.22, x + 0.22], [yd, yd], color=fs.ORANGE, lw=2.0)
                a.text(x, yd - 0.22, '+', color=fs.ORANGE, ha='center', va='center', fontsize=9, fontweight='bold')
                electron(a, (x + 0.15 * (i % 2), 2.75 + 0.18 * (i % 3)), r=0.08)
                fs.arrow(a, (x - 0.15, yd + 0.05), (x - 0.15, 2.62), color=EL, lw=0.8, ms=6)
            a.text(3.45, yd, r'$E_d$', color=fs.ORANGE, fontsize=9, va='center')
            a.text(2.0, 1.5, '주개 준위: $E_c$ 아래 수십 meV', fontsize=8, ha='center', color=fs.ORANGE)
            a.set_title('(가) n형: 주개가 전자를 내준다', fontsize=9)
        else:
            ya = 0.9
            for i, x in enumerate(xs):
                a.plot([x - 0.22, x + 0.22], [ya, ya], color=fs.ACC, lw=2.0)
                a.text(x, ya + 0.22, '−', color=fs.ACC, ha='center', va='center', fontsize=10, fontweight='bold')
                a.add_patch(Circle((x + 0.15 * (i % 2), 0.25 - 0.18 * (i % 3)), 0.08, fc='white', ec=HO, lw=1.2, zorder=8))
                fs.arrow(a, (x - 0.15, 0.4), (x - 0.15, ya - 0.05), color=EL, lw=0.8, ms=6)
            a.text(3.45, ya, r'$E_a$', color=fs.ACC, fontsize=9, va='center')
            a.text(2.0, 1.45, '받개 준위: $E_v$ 위 수십 meV', fontsize=8, ha='center', color=fs.ACC)
            a.set_title('(나) p형: 받개가 전자를 받는다', fontsize=9)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'fig39_09')


# ---------------------------------------------------------------- p-n 접합 수치(예제 39.5)
e, eps0 = 1.602176634e-19, 8.8541878128e-12
eps = 11.7 * eps0
NA = ND = 1.0e22
ni = 1.0e16
kT = 0.025852
Vbi = kT * np.log(NA * ND / ni ** 2)


def pn_profile(V):
    W = np.sqrt(2 * eps * V / e * (1 / NA + 1 / ND))
    xn = W * NA / (NA + ND); xp = W * ND / (NA + ND)
    x = np.linspace(-2.2 * xp, 2.2 * xn, 2001)
    rho = np.where((x > -xp) & (x < 0), -e * NA, 0) + np.where((x >= 0) & (x < xn), e * ND, 0)
    Ef = np.where((x > -xp) & (x < 0), -e * NA / eps * (x + xp), 0) + np.where((x >= 0) & (x < xn), e * ND / eps * (x - xn), 0)
    Vx = np.where(x <= -xp, 0, np.where(x < 0, e * NA / (2 * eps) * (x + xp) ** 2,
                  np.where(x < xn, V - e * ND / (2 * eps) * (x - xn) ** 2, V)))
    return x, rho, Ef, Vx, xp, xn


def fig10():
    fig, ax = fs.canvas(5.0, 1.9, xlim=(-3.2, 3.2), ylim=(-0.95, 1.25))
    ax.add_patch(Rectangle((-3, -0.6), 3, 1.4, fc='#fbe3e0', ec='none'))
    ax.add_patch(Rectangle((0, -0.6), 3, 1.4, fc='#dfe8f6', ec='none'))
    ax.add_patch(Rectangle((-0.9, -0.6), 1.8, 1.4, fc='white', ec='none', alpha=0.75))
    ax.add_patch(Rectangle((-3, -0.6), 6, 1.4, fc='none', ec=fs.BLACK, lw=1.0))
    ax.plot([0, 0], [-0.6, 0.8], color=fs.BLACK, lw=0.6, ls=':')
    ax.plot([-0.9, -0.9], [-0.6, 0.8], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([0.9, 0.9], [-0.6, 0.8], color=fs.GRAY, lw=0.7, ls='--')
    rng = np.random.default_rng(2)
    for _ in range(14):
        hole(ax, (rng.uniform(-2.85, -1.05), rng.uniform(-0.45, 0.65)), r=0.07)
        electron(ax, (rng.uniform(1.05, 2.85), rng.uniform(-0.45, 0.65)), r=0.07)
    for xi in (-0.7, -0.25):
        for yi in (-0.35, 0.1, 0.55):
            ax.add_patch(Circle((xi, yi), 0.12, fc='white', ec=fs.NEG, lw=0.9, zorder=6))
            ax.text(xi, yi - 0.01, '−', color=fs.NEG, ha='center', va='center', fontsize=9, zorder=7)
    for xi in (0.25, 0.7):
        for yi in (-0.35, 0.1, 0.55):
            ax.add_patch(Circle((xi, yi), 0.12, fc='white', ec=fs.POS, lw=0.9, zorder=6))
            ax.text(xi, yi - 0.01, '+', color=fs.POS, ha='center', va='center', fontsize=9, zorder=7)
    fs.arrow(ax, (0.75, 0.97), (-0.75, 0.97), color=fs.FIELD, lw=1.3, ms=10)
    ax.text(0, 1.13, r'$\vec E$ (n → p)', color=fs.FIELD, fontsize=9, ha='center')
    ax.text(-2.0, 1.0, 'p형', fontsize=11, ha='center'); ax.text(2.0, 1.0, 'n형', fontsize=11, ha='center')
    ax.text(0, -0.82, '공핍층', fontsize=9, ha='center')
    ax.text(-1.95, -0.82, '양공(다수 운반자)', fontsize=8, ha='center', color=HO)
    ax.text(1.95, -0.82, '전자(다수 운반자)', fontsize=8, ha='center', color=EL)
    ax.text(-0.9, 0.86, r'$-x_p$', fontsize=8, ha='center'); ax.text(0.9, 0.86, r'$x_n$', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig39_10')


def fig11():
    x, rho, Ef, Vx, xp, xn = pn_profile(Vbi)
    xu = x * 1e6
    fig, axs = plt.subplots(3, 1, figsize=(4.2, 3.4), sharex=True)
    axs[0].fill_between(xu, 0, rho / e * 1e-6 / 1e16, step='mid', color=fs.FIELD, alpha=0.25, lw=0)
    axs[0].plot(xu, rho / e * 1e-6 / 1e16, color=fs.FIELD, lw=1.2)
    axs[0].set_ylabel(r'$\rho/e$' '\n' r'($10^{16}$ cm$^{-3}$)', fontsize=8)
    axs[0].text(-0.11, -0.55, r'$-eN_A$', fontsize=8.5, ha='center'); axs[0].text(0.11, 0.35, r'$+eN_D$', fontsize=8.5, ha='center')
    axs[0].set_ylim(-1.4, 1.4)
    axs[1].plot(xu, Ef / 1e6, color=fs.FIELD, lw=1.2)
    axs[1].set_ylabel(r'$E$ ($10^6$ V/m)', fontsize=8)
    Em = e * ND * xn / eps
    axs[1].annotate(fr'$-|E_{{\max}}| = -{Em/1e6:.1f}\times10^6$ V/m', xy=(0, -Em / 1e6), xytext=(0.17, -2.9),
                    fontsize=7.5, arrowprops=dict(arrowstyle='-', lw=0.6))
    axs[1].set_ylim(-3.8, 0.6)
    axs[2].plot(xu, Vx, color=fs.BLACK, lw=1.2)
    axs[2].set_ylabel(r'$V$ (V)', fontsize=8)
    axs[2].text(0.32, Vbi - 0.18, fr'$V_{{bi}} = {Vbi:.2f}$ V', fontsize=8)
    axs[2].set_ylim(-0.1, 0.85)
    for a in axs:
        a.axhline(0, color=fs.GRAY, lw=0.5)
        a.axvspan(-xp * 1e6, xn * 1e6, color=fs.SURF, alpha=0.25, lw=0)
        a.grid(True, lw=0.3, color='#dddddd'); a.tick_params(labelsize=7.5)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    axs[2].set_xlabel(r'$x$ ($\mu$m)   (p쪽 $x<0$, n쪽 $x>0$)', fontsize=8)
    axs[2].set_xlim(xu[0], xu[-1])
    fig.align_ylabels(axs)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, __file__, 'fig39_11')


# ---------------------------------------------------------------- 그림 39.12 띠 굽음
def fig12():
    Eg = 1.12
    dF = kT * np.log(ND / ni)           # n쪽 E_F - E_i (= p쪽 E_i - E_F)
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.6), sharey=True)
    for a, Vapp, title in ((axs[0], 0.0, '(가) 평형'), (axs[1], 0.40, '(나) 순방향 $V$ = 0.40 V')):
        x, rho, Ef, Vx, xp, xn = pn_profile(Vbi - Vapp)
        xu = x * 1e6
        Ec_p = Eg / 2 + dF               # p쪽 E_c (n쪽 E_F를 0 기준으로 잡지 않고 p쪽 E_Fp = 0)
        Ec = Ec_p - Vx
        Ev = Ec - Eg
        a.fill_between(xu, Ec, Ec + 0.5, color=CB, lw=0); a.fill_between(xu, Ev - 0.5, Ev, color=VBF, lw=0, alpha=0.8)
        a.plot(xu, Ec, color=fs.BLACK, lw=1.2); a.plot(xu, Ev, color=fs.BLACK, lw=1.2)
        EFp = 0.0; EFn = Vapp
        if Vapp == 0:
            a.plot(xu, np.zeros_like(xu), '--', color=fs.FORCE, lw=1.0)
            a.text(xu[0] + 0.02, 0.06, r'$E_F$', color=fs.FORCE, fontsize=9)
        else:
            m = xu < xn * 1e6; a.plot(xu[m], np.full(m.sum(), EFp), '--', color=fs.FORCE, lw=1.0)
            m = xu > -xp * 1e6; a.plot(xu[m], np.full(m.sum(), EFn), '--', color=fs.ACC, lw=1.0)
            a.text(xu[0] + 0.02, 0.06, r'$E_{Fp}$', color=fs.FORCE, fontsize=9)
            a.text(xu[-1] - 0.01, EFn - 0.15, r'$E_{Fn}$', color=fs.ACC, fontsize=9, ha='right')
            xa = xu[0] * 0.45
            fs.arrow(a, (xa, EFp), (xa, EFn), style='<|-|>', lw=0.8, ms=6, color=fs.BLACK)
            a.text(xa + 0.015, EFn / 2, r'$eV$', fontsize=9, va='center')
        top_p, top_n = Ec[0], Ec[-1]
        xb = xu[-1] * 0.45
        a.plot([xu[0] * 0.2, xu[-1]], [top_p, top_p], color=fs.GRAY, lw=0.6, ls=':')
        fs.arrow(a, (xb, top_n), (xb, top_p), style='<|-|>', color=fs.VEL, lw=0.9, ms=6)
        lab = r'$eV_{bi}$' if Vapp == 0 else r'$e(V_{bi}-V)$'
        a.text(xb - 0.015, (top_p + top_n) / 2, lab, color=fs.VEL, fontsize=9, va='center', ha='right')
        a.text(xu[0] + 0.02, Ec_p + 0.08, r'$E_c$', fontsize=9); a.text(xu[0] + 0.02, Ec_p - Eg - 0.2, r'$E_v$', fontsize=9)
        a.scatter(xu[-1] * np.linspace(0.62, 0.95, 5), Ec[-1] + 0.12 + 0 * np.arange(5), s=12, color=EL, zorder=6)
        a.scatter(xu[0] * np.linspace(0.3, 0.62, 5), Ev[0] - 0.12 + 0 * np.arange(5), s=12, facecolors='white',
                  edgecolors=HO, linewidths=1.0, zorder=6)
        a.set_title(title, fontsize=9)
        a.set_xlim(xu[0], xu[-1]); a.set_xticks([])
        a.text(xu[0] * 0.6, -1.95, 'p', fontsize=10, ha='center'); a.text(xu[-1] * 0.6, -1.95, 'n', fontsize=10, ha='center')
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    axs[0].set_ylabel('전자 에너지 (eV)', fontsize=8.5)
    axs[0].set_ylim(-2.1, 1.4)
    axs[0].tick_params(labelsize=7.5)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'fig39_12')


# ---------------------------------------------------------------- 그림 39.13 다이오드 I-V
def fig13():
    Is = 1e-14
    V = np.linspace(-0.3, 0.75, 1000)
    I = Is * (np.exp(V / kT) - 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.5))
    for a in (a1, a2):
        a.grid(True, lw=0.4, color='#d0d0d0'); a.tick_params(labelsize=8)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    a1.plot(V, I * 1e3, color=fs.VEL)
    a1.axhline(0, color=fs.BLACK, lw=0.6); a1.axvline(0, color=fs.BLACK, lw=0.6)
    a1.set_xlim(-0.3, 0.75); a1.set_ylim(-1, 12)
    a1.set_xlabel(r'$V$ (V)', fontsize=9); a1.set_ylabel(r'$I$ (mA)', fontsize=9)
    a1.text(-0.28, 1.0, '역방향:\n$I \\approx -I_s$', fontsize=7.5)
    a1.text(0.2, 8, '순방향', fontsize=8)
    a1.set_title('(가) 선형 눈금', fontsize=9)
    Vp = np.linspace(0.0, 0.75, 500)
    a2.semilogy(Vp, Is * (np.exp(Vp / kT) - 1) + 1e-30, color=fs.VEL)
    a2.set_xlim(0.1, 0.75); a2.set_ylim(1e-12, 1e-1)
    a2.set_xlabel(r'$V$ (V)', fontsize=9); a2.set_ylabel(r'$I$ (A)', fontsize=9)
    v1 = 0.40; v2 = v1 + kT * np.log(10)
    i1 = Is * np.exp(v1 / kT); i2 = Is * np.exp(v2 / kT)
    a2.plot([v1, v2, v2], [i1, i1, i2], color=fs.FORCE, lw=0.9)
    a2.text((v1 + v2) / 2, i1 / 4, '59.5 mV', fontsize=7.5, ha='center', color=fs.FORCE, va='top')
    a2.text(v2 + 0.01, np.sqrt(i1 * i2), '×10', fontsize=7.5, color=fs.FORCE, va='center')
    a2.set_title('(나) 로그 눈금(순방향)', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig39_13')


# ---------------------------------------------------------------- 그림 39.14 트랜지스터
def fig14():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.5), gridspec_kw={'width_ratios': [1, 1.15]})
    # (가) BJT
    a1.set_xlim(-0.2, 4.4); a1.set_ylim(-1.0, 2.6); a1.set_aspect('equal'); a1.axis('off')
    a1.add_patch(Rectangle((0, 0), 1.7, 1.4, fc='#dfe8f6', ec=fs.BLACK, lw=1.0))
    a1.add_patch(Rectangle((1.7, 0), 0.5, 1.4, fc='#fbe3e0', ec=fs.BLACK, lw=1.0))
    a1.add_patch(Rectangle((2.2, 0), 1.9, 1.4, fc='#dfe8f6', ec=fs.BLACK, lw=1.0))
    a1.text(0.85, 1.15, 'n', ha='center', fontsize=10); a1.text(1.95, 1.15, 'p', ha='center', fontsize=10); a1.text(3.15, 1.15, 'n', ha='center', fontsize=10)
    a1.text(0.85, -0.25, '이미터 E', ha='center', va='top', fontsize=8)
    a1.text(1.95, 1.65, '베이스 B', ha='center', va='bottom', fontsize=8)
    a1.text(3.15, -0.25, '컬렉터 C', ha='center', va='top', fontsize=8)
    a1.plot([1.95, 1.95], [1.4, 1.62], color=fs.BLACK, lw=1.0)
    for y in (0.35, 0.65, 0.95):
        fs.arrow(a1, (0.6, y), (3.8, y), color=EL, lw=1.0, ms=8)
    fs.arrow(a1, (1.85, 0.55), (1.85, 1.38), color=EL, lw=0.8, ms=6, ls=':')
    a1.text(0.08, 0.65, '전자', fontsize=7.5, color=EL, ha='left', va='center')
    a1.text(1.62, -0.75, '순방향', fontsize=7.5, ha='right', color=fs.ACC)
    a1.text(2.28, -0.75, '역방향', fontsize=7.5, ha='left', color=fs.FORCE)
    a1.plot([1.7, 1.7], [-0.62, 0], color=fs.ACC, lw=0.7, ls='--'); a1.plot([2.2, 2.2], [-0.62, 0], color=fs.FORCE, lw=0.7, ls='--')
    a1.text(3.15, 1.65, r'$I_C = \beta I_B$', fontsize=8.5, ha='center', va='bottom')
    a1.set_title('(가) n-p-n 쌍극 접합 트랜지스터', fontsize=8.5)
    # (나) n채널 MOSFET (켜짐)
    a2.set_xlim(-0.3, 5.3); a2.set_ylim(-0.9, 3.0); a2.set_aspect('equal'); a2.axis('off')
    a2.add_patch(Rectangle((0, 0), 5, 1.6, fc='#fbe3e0', ec=fs.BLACK, lw=1.0))
    a2.text(2.5, 0.25, 'p형 기판', ha='center', fontsize=8.5)
    for x0, lab in ((0.2, '소스'), (3.6, '드레인')):
        a2.add_patch(Rectangle((x0, 0.9), 1.2, 0.7, fc='#dfe8f6', ec=fs.BLACK, lw=0.9))
        a2.text(x0 + 0.6, 1.2, 'n', ha='center', va='center', fontsize=9)
        a2.add_patch(Rectangle((x0 + 0.3, 1.6), 0.6, 0.25, fc='#b0b0b0', ec=fs.BLACK, lw=0.7))
        a2.plot([x0 + 0.6, x0 + 0.6], [1.85, 2.05], color=fs.BLACK, lw=1.0)
        a2.text(x0 + 0.6, 2.08, lab, ha='center', va='bottom', fontsize=8)
    a2.add_patch(Rectangle((1.4, 1.6), 2.2, 0.18, fc='#f6efc8', ec=fs.BLACK, lw=0.8))
    a2.add_patch(Rectangle((1.5, 1.78), 2.0, 0.35, fc='#b0b0b0', ec=fs.BLACK, lw=0.9))
    a2.plot([2.5, 2.5], [2.13, 2.5], color=fs.BLACK, lw=1.0)
    a2.text(2.5, 2.55, r'게이트 $V_G > 0$', ha='center', va='bottom', fontsize=8)
    for k in range(6):
        electron(a2, (1.55 + 0.38 * k, 1.5), r=0.06)
    for k in range(5):
        a2.text(1.7 + 0.42 * k, 1.97, '+', ha='center', va='center', fontsize=7, color=fs.POS)
    a2.annotate('산화막', xy=(3.55, 1.69), xytext=(4.25, 2.75), fontsize=7.5, arrowprops=dict(arrowstyle='-', lw=0.5))
    a2.annotate('반전층(전자 채널)', xy=(2.5, 1.45), xytext=(2.5, -0.55), fontsize=7.5, ha='center', color=EL,
                arrowprops=dict(arrowstyle='-', lw=0.5, color=EL))
    a2.set_title('(나) n채널 MOSFET (켜짐)', fontsize=8.5)
    fig.tight_layout(w_pad=0.4)
    fs.save(fig, __file__, 'fig39_14')


# ---------------------------------------------------------------- 그림 39.15 직접·간접 띠
def fig15():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.5), sharey=True)
    k = np.linspace(-1, 1, 300)
    for a, kind in zip(axs, ('direct', 'indirect')):
        Ev = -0.9 * k ** 2
        Ec = 1.2 + 0.9 * k ** 2 if kind == 'direct' else 1.0 + 0.9 * (np.abs(k) - 0.62) ** 2
        a.plot(k, Ec, color=fs.VEL, lw=1.5); a.plot(k, Ev, color=fs.FORCE, lw=1.5)
        a.axvline(0, color=fs.GRAY, lw=0.5)
        a.text(-0.95, 1.62 if kind == 'direct' else 1.55, '전도띠', fontsize=8, color=fs.VEL)
        a.text(-0.95, -0.55, '원자가띠', fontsize=8, color=fs.FORCE)
        electron(a, (0 if kind == 'direct' else 0.62, Ec.min() + 0.06), r=0.035)
        a.add_patch(Circle((0, 0.06), 0.035, fc='white', ec=HO, lw=1.1, zorder=8))
        if kind == 'direct':
            fs.arrow(a, (0, Ec.min()), (0, 0.02), color=fs.ORANGE, lw=1.4, ms=9)
            fs.wave(a, 0.12, 0.62, y0=0.6, amp=0.06, wavelength=0.12, color=fs.ORANGE, lw=1.0)
            a.text(0.65, 0.6, r'광자 $\hbar\omega \approx E_g$', fontsize=8, color=fs.ORANGE, va='center')
            a.set_title('(가) 직접 띠 간격 (GaAs, GaN)', fontsize=9)
        else:
            fs.arrow(a, (0.62, Ec.min()), (0.04, 0.03), color=fs.ORANGE, lw=1.2, ms=8, ls='--')
            a.text(0.5, 0.42, '포논이\n운동량 보탬', fontsize=7.5, color=fs.ORANGE, ha='left')
            a.annotate('', xy=(0.62, 1.7), xytext=(0, 1.7), arrowprops=dict(arrowstyle='<|-|>', lw=0.7))
            a.text(0.31, 1.76, r'$\Delta k$', fontsize=8, ha='center', va='bottom')
            a.set_title('(나) 간접 띠 간격 (Si, Ge)', fontsize=9)
        a.set_xlim(-1, 1); a.set_ylim(-0.95, 2.1)
        a.set_xticks([0]); a.set_xticklabels(['0'], fontsize=8); a.set_yticks([])
        a.set_xlabel(r'파수 $k$', fontsize=9)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    axs[0].set_ylabel(r'$E$', fontsize=10)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'fig39_15')


# ---------------------------------------------------------------- 그림 39.16 태양전지 J-V (본문 코드)
def fig16():
    kT_e = 0.025852
    J_L, J_s = 35e-3, 1e-12
    V = np.linspace(0, 0.7, 7001)
    J = J_L - J_s * (np.exp(V / kT_e) - 1)
    Pw = J * V
    i = np.argmax(Pw)
    Voc = kT_e * np.log(J_L / J_s + 1)
    fig, ax = fs.plot_axes(4.2, 2.7)
    ax.plot(V, J * 1e3, color=fs.VEL, label=r'$J$ (mA/cm$^2$)')
    ax.add_patch(Rectangle((0, 0), V[i], J[i] * 1e3, fc=fs.SURF, alpha=0.35, ec=fs.ORANGE, lw=0.8))
    ax.plot(V[i], J[i] * 1e3, 'o', color=fs.ORANGE, ms=5, zorder=5)
    ax.annotate(f'최대 출력점\n({V[i]:.3f} V, {J[i]*1e3:.1f} mA/cm²)', xy=(V[i], J[i] * 1e3), xytext=(0.2, 25),
                fontsize=7.5, arrowprops=dict(arrowstyle='->', lw=0.6))
    ax.set_xlabel(r'$V$ (V)', fontsize=9); ax.set_ylabel(r'$J$ (mA/cm$^2$)', fontsize=9, color=fs.VEL)
    ax.set_xlim(0, 0.7); ax.set_ylim(0, 40)
    ax.text(Voc, 1.2, r'$V_{oc}$' f'\n{Voc:.3f} V', fontsize=7.5, ha='center')
    ax.text(0.01, 36.2, r'$J_{sc} = 35$', fontsize=7.5)
    ax.tick_params(labelsize=8)
    a2 = ax.twinx()
    a2.plot(V, Pw * 1e3, color=fs.FORCE, ls='--', lw=1.1)
    a2.set_ylim(0, 20); a2.set_ylabel(r'$P = JV$ (mW/cm$^2$)', fontsize=9, color=fs.FORCE)
    a2.tick_params(labelsize=8)
    a2.spines['top'].set_visible(False)
    a2.text(0.18, 7.6, r'$P$', color=fs.FORCE, fontsize=9)
    fs.save(fig, __file__, 'fig39_16')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14,
              fig15, fig16):
        f()
