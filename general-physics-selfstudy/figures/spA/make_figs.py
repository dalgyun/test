"""특집 A 양자정보와 양자컴퓨터 그림. python3 figures/spA/make_figs.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools'))
import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, FancyBboxPatch, FancyArrowPatch, Polygon


def style(a):
    a.grid(True, lw=0.4, color='#d0d0d0'); a.tick_params(labelsize=8)
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)


# ---------------------------------------------------------------- 블로흐 구면 투영 도우미
EL, AZ = np.radians(18), np.radians(32)
RIGHT = np.array([-np.sin(AZ), np.cos(AZ), 0.0])
UP = np.array([-np.sin(EL) * np.cos(AZ), -np.sin(EL) * np.sin(AZ), np.cos(EL)])
VIEW = np.array([np.cos(EL) * np.cos(AZ), np.cos(EL) * np.sin(AZ), np.sin(EL)])


def pr(v):
    v = np.asarray(v, float)
    return np.array([v @ RIGHT, v @ UP])


def curve3d(ax, pts, color=fs.BLACK, lw=0.9, dash_back=True, **kw):
    pts = np.asarray(pts)
    front = pts @ VIEW >= -1e-9
    P = np.array([pr(p) for p in pts])
    if not dash_back:
        ax.plot(P[:, 0], P[:, 1], color=color, lw=lw, **kw); return
    for mask, ls in ((front, '-'), (~front, '--')):
        Q = np.where(mask[:, None], P, np.nan)
        ax.plot(Q[:, 0], Q[:, 1], color=color, lw=lw, ls=ls, **kw)


def bloch_base(ax):
    ax.add_patch(Circle((0, 0), 1, fc='#eef3fa', ec=fs.BLACK, lw=1.0, zorder=0))
    t = np.linspace(0, 2 * np.pi, 300)
    curve3d(ax, np.c_[np.cos(t), np.sin(t), 0 * t], color=fs.GRAY, lw=0.8)
    curve3d(ax, np.c_[np.sin(t), 0 * t, np.cos(t)], color=fs.GRAY, lw=0.5)
    for v, lab, off in (((1.35, 0, 0), '$x$', (-0.1, 0.06)), ((0, 1.35, 0), '$y$', (0.08, 0)),
                        ((0, 0, 1.3), '$z$', (0.07, 0.03))):
        q = pr(v)
        fs.arrow(ax, (0, 0), tuple(q), lw=0.7, ms=7, color=fs.GRAY)
        ax.text(q[0] + off[0], q[1] + off[1], lab, fontsize=10, color=fs.GRAY, ha='center', va='center')
    for v in ((0, 0, -1), (-1, 0, 0), (0, -1, 0)):
        q = pr(v); ax.plot([0, q[0]], [0, q[1]], color=fs.GRAY, lw=0.5, ls=':')


# ---------------------------------------------------------------- 그림 A.1 블로흐 구면
def fig01():
    fig, ax = fs.canvas(3.4, 3.3, xlim=(-1.55, 1.6), ylim=(-1.45, 1.6))
    bloch_base(ax)
    states = [((0, 0, 1), r'$|0\rangle$', (-0.2, 0.12)), ((0, 0, -1), r'$|1\rangle$', (0.2, -0.1)),
              ((1, 0, 0), r'$|+\rangle$', (0.2, -0.1)), ((-1, 0, 0), r'$|-\rangle$', (-0.05, -0.16)),
              ((0, 1, 0), r'$|{+i}\rangle$', (0.05, 0.2))]
    for v, lab, off in states:
        q = pr(v)
        ax.plot(*q, 'o', color=fs.VEL, ms=4.5, zorder=6)
        ax.text(q[0] + off[0], q[1] + off[1], lab, fontsize=10, color=fs.VEL, ha='center', va='center')
    th, ph = np.radians(50), np.radians(110)
    r = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    q = pr(r)
    fs.arrow(ax, (0, 0), tuple(q), color=fs.FORCE, lw=1.6, ms=10)
    ax.text(q[0] + 0.1, q[1] + 0.1, r'$|\psi\rangle$', color=fs.FORCE, fontsize=11)
    foot = np.array([r[0], r[1], 0])
    pf = pr(foot)
    ax.plot([q[0], pf[0]], [q[1], pf[1]], color=fs.FORCE, lw=0.6, ls=':')
    ax.plot([0, pf[0]], [0, pf[1]], color=fs.FORCE, lw=0.6, ls=':')
    t = np.linspace(0, th, 50)
    arc = np.array([[0.35 * np.sin(a) * np.cos(ph), 0.35 * np.sin(a) * np.sin(ph), 0.35 * np.cos(a)] for a in t])
    curve3d(ax, arc, color=fs.BLACK, lw=0.9, dash_back=False)
    m = pr(arc[25] * 1.45); ax.text(m[0], m[1], r'$\theta$', fontsize=10, ha='center', va='center')
    t = np.linspace(0, ph, 50)
    arc = np.c_[0.45 * np.cos(t), 0.45 * np.sin(t), 0 * t]
    curve3d(ax, arc, color=fs.BLACK, lw=0.9, dash_back=False)
    m = pr(arc[25] * 1.4); ax.text(m[0], m[1] - 0.04, r'$\varphi$', fontsize=10, ha='center', va='center')
    fs.save(fig, __file__, 'figSA_01')


# ---------------------------------------------------------------- 그림 A.2 중첩과 혼합
def fig02():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.3), sharey=True)
    labs = ['0', '1', '+', '−']
    cols = [fs.VEL, fs.VEL, fs.ACC, fs.ACC]
    for a, P, title in ((axs[0], [0.5, 0.5, 1.0, 0.0], r'(가) 중첩 $|+\rangle$'),
                        (axs[1], [0.5, 0.5, 0.5, 0.5], '(나) 50:50 혼합(동전 던지기)')):
        style(a); a.grid(False, axis='x')
        a.bar([0, 1, 2.6, 3.6], P, color=cols, width=0.7)
        for x, p in zip([0, 1, 2.6, 3.6], P):
            a.text(x, p + 0.03, f'{p:g}', ha='center', fontsize=8)
        a.set_xticks([0, 1, 2.6, 3.6]); a.set_xticklabels(labs, fontsize=9)
        a.text(0.5, -0.27, '$Z$ 기저', ha='center', fontsize=8.5, color=fs.VEL, transform=a.transData)
        a.text(3.1, -0.27, '$X$ 기저', ha='center', fontsize=8.5, color=fs.ACC, transform=a.transData)
        a.set_ylim(0, 1.15); a.set_xlim(-0.6, 4.2)
        a.set_title(title, fontsize=9)
    axs[0].set_ylabel('측정 확률', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'figSA_02')


# ---------------------------------------------------------------- 그림 A.3 벨 실험
def detector(ax, c, setting_labels, name, flip=False):
    s = -1 if flip else 1
    ax.add_patch(FancyBboxPatch((c[0] - 0.45, c[1] - 0.45), 0.9, 0.9, boxstyle='round,pad=0.02,rounding_size=0.1',
                                fc='#eef3fa', ec=fs.BLACK, lw=1.0))
    ax.text(c[0], c[1] + 0.68, name, ha='center', fontsize=9)
    # 설정 손잡이
    for k, (lab, ang) in enumerate(zip(setting_labels, (55, 0))):
        pass
    ax.add_patch(Circle(c, 0.22, fc='white', ec=fs.BLACK, lw=0.8))
    a = np.radians(50)
    ax.plot([c[0], c[0] + 0.2 * np.cos(a)], [c[1], c[1] + 0.2 * np.sin(a)], color=fs.FORCE, lw=1.4)
    ax.text(c[0], c[1] - 0.62, f'설정 {setting_labels[0]} 또는 {setting_labels[1]}', ha='center', fontsize=7.5)
    for dy, lab in ((0.25, '+1'), (-0.25, '−1')):
        p = (c[0] + s * 0.75, c[1] + dy)
        ax.add_patch(Circle(p, 0.09, fc='#f5d76e', ec=fs.BLACK, lw=0.6))
        ax.text(p[0] + s * 0.2, p[1], lab, fontsize=7.5, ha='left' if s > 0 else 'right', va='center')
        ax.plot([c[0] + s * 0.45, p[0] - s * 0.09], [c[1], p[1]], color=fs.GRAY, lw=0.6)


def fig03():
    fig, ax = fs.canvas(5.3, 2.3, xlim=(-3.6, 3.6), ylim=(-1.4, 1.35))
    ax.add_patch(Circle((0, 0), 0.32, fc=fs.SURF, ec=fs.BLACK, lw=1.0))
    ax.text(0, 0, '원천', ha='center', va='center', fontsize=8)
    ax.text(0, 0.55, r'$|\Phi^+\rangle$ 쌍', ha='center', fontsize=9)
    fs.wave(ax, -1.95, -0.4, y0=0, amp=0.06, wavelength=0.18, color=fs.ORANGE, lw=1.0)
    fs.wave(ax, 0.4, 1.95, y0=0, amp=0.06, wavelength=0.18, color=fs.ORANGE, lw=1.0)
    fs.arrow(ax, (-1.6, 0.0), (-1.98, 0.0), color=fs.ORANGE, lw=0, ms=9)
    fs.arrow(ax, (1.6, 0.0), (1.98, 0.0), color=fs.ORANGE, lw=0, ms=9)
    detector(ax, (-2.45, 0), ("$a$", "$a'$"), '앨리스', flip=True)
    detector(ax, (2.45, 0), ("$b$", "$b'$"), '밥')
    ax.annotate('', xy=(2.3, -1.05), xytext=(-2.3, -1.05),
                arrowprops=dict(arrowstyle='<|-|>', lw=0.8, ls='--', color=fs.GRAY))
    ax.text(0, -1.3, '나중에 결과를 모아 $E(a, b) = \\langle AB\\rangle$ 계산', ha='center', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'figSA_03')


# ---------------------------------------------------------------- 그림 A.4 CHSH 각도와 S
def fig04():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.4, 2.6), gridspec_kw={'width_ratios': [1, 1.35]})
    a1.set_aspect('equal'); a1.axis('off'); a1.set_xlim(-1.45, 1.45); a1.set_ylim(-1.35, 1.45)
    a1.add_patch(Circle((0, 0), 1, fc='none', ec=fs.GRAY, lw=0.8))
    a1.text(1.3, 0.1, '$x$', fontsize=9, color=fs.GRAY); a1.text(0.06, 1.3, '$z$', fontsize=9, color=fs.GRAY)
    a1.plot([-1.25, 1.25], [0, 0], color=fs.GRAY, lw=0.5); a1.plot([0, 0], [-1.2, 1.25], color=fs.GRAY, lw=0.5)
    # 블로흐 x-z 평면: z축에서 x쪽으로 각 theta
    for th, lab, c in ((0, '$a$', fs.FORCE), (np.pi / 2, "$a'$", fs.FORCE), (np.pi / 4, '$b$', fs.VEL),
                       (-np.pi / 4, "$b'$", fs.VEL)):
        q = (np.sin(th), np.cos(th))
        fs.arrow(a1, (0, 0), q, color=c, lw=1.5, ms=9)
        a1.text(1.18 * q[0] + (0.08 if th == 0 else 0), 1.18 * q[1], lab, color=c, fontsize=11, ha='center', va='center')
    fs.angle_arc(a1, (0, 0), 0.35, 45, 90, '45°', fontsize=7.5, tr=0.55)
    a1.set_title('(가) 측정 방향(블로흐 $x$-$z$ 평면)', fontsize=8.5)
    style(a2)
    phi = np.linspace(-90, 180, 500)
    S = 2 * (np.cos(np.radians(phi)) + np.sin(np.radians(phi)))
    a2.axhspan(-2, 2, color=fs.GRAY, alpha=0.15, lw=0)
    a2.plot(phi, S, color=fs.VEL)
    a2.axhline(2 * np.sqrt(2), color=fs.FORCE, lw=0.8, ls='--')
    a2.text(-85, 2 * np.sqrt(2) + 0.12, r'$2\sqrt{2}$', color=fs.FORCE, fontsize=9)
    a2.text(-45, -1.05, '국소적 숨은 변수\n$|S| \\leq 2$', fontsize=7.5, ha='center', va='top', color='#555555')
    a2.plot(45, 2 * np.sqrt(2), 'o', color=fs.FORCE, ms=4)
    a2.set_xlim(-90, 180); a2.set_ylim(-3.2, 3.4); a2.set_xticks([-90, -45, 0, 45, 90, 135, 180])
    a2.set_xlabel(r"$b = \phi$, $b' = -\phi$ (도)", fontsize=8.5); a2.set_ylabel('$S$', fontsize=9)
    a2.set_title(r"(나) $a = 0$, $a'$ = 90°일 때 $S(\phi)$", fontsize=8.5)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'figSA_04')


# ---------------------------------------------------------------- 양자 회로 도우미
def wire(ax, y, x0, x1, classical=False):
    if classical:
        ax.plot([x0, x1], [y + 0.04, y + 0.04], color=fs.BLACK, lw=0.8)
        ax.plot([x0, x1], [y - 0.04, y - 0.04], color=fs.BLACK, lw=0.8)
    else:
        ax.plot([x0, x1], [y, y], color=fs.BLACK, lw=1.0, zorder=1)


def gate(ax, x, y, lab, fc='#dfe8f6', w=0.5):
    ax.add_patch(Rectangle((x - w / 2, y - 0.25), w, 0.5, fc=fc, ec=fs.BLACK, lw=1.0, zorder=3))
    ax.text(x, y, lab, ha='center', va='center', fontsize=11, zorder=4)


def cnot(ax, x, yc, yt):
    ax.plot([x, x], [yc, yt + (0.17 if yt < yc else -0.17)], color=fs.BLACK, lw=1.0, zorder=2)
    ax.add_patch(Circle((x, yc), 0.07, color=fs.BLACK, zorder=4))
    ax.add_patch(Circle((x, yt), 0.17, fc='white', ec=fs.BLACK, lw=1.0, zorder=4))
    ax.plot([x - 0.17, x + 0.17], [yt, yt], color=fs.BLACK, lw=1.0, zorder=5)
    ax.plot([x, x], [yt - 0.17, yt + 0.17], color=fs.BLACK, lw=1.0, zorder=5)


def meter(ax, x, y):
    ax.add_patch(Rectangle((x - 0.27, y - 0.25), 0.54, 0.5, fc='white', ec=fs.BLACK, lw=1.0, zorder=3))
    ax.add_patch(Arc((x, y - 0.1), 0.36, 0.36, theta1=0, theta2=180, lw=0.9, zorder=4))
    ax.plot([x, x + 0.14], [y - 0.1, y + 0.13], color=fs.BLACK, lw=0.9, zorder=4)


# ---------------------------------------------------------------- 그림 A.5 벨 상태 회로
def fig05():
    fig, ax = fs.canvas(5.0, 1.9, xlim=(-0.9, 7.0), ylim=(-0.75, 2.05))
    yA, yB = 1.0, 0.0
    wire(ax, yA, 0, 6.3); wire(ax, yB, 0, 6.3)
    ax.text(-0.1, yA, r'A: $|0\rangle$', ha='right', va='center', fontsize=10)
    ax.text(-0.1, yB, r'B: $|0\rangle$', ha='right', va='center', fontsize=10)
    gate(ax, 1.2, yA, 'H')
    cnot(ax, 3.0, yA, yB)
    meter(ax, 5.9, yA); meter(ax, 5.9, yB)
    for x in (0.5, 2.1, 4.1):
        ax.plot([x, x], [-0.25, 1.4], color=fs.GRAY, lw=0.6, ls=':')
    ax.text(0.5, 1.55, r'$|00\rangle$', ha='center', fontsize=9, color=fs.VEL)
    ax.text(2.1, 1.55, r'$\frac{|00\rangle + |10\rangle}{\sqrt{2}}$', ha='center', fontsize=10, color=fs.VEL)
    ax.text(4.1, 1.55, r'$\frac{|00\rangle + |11\rangle}{\sqrt{2}} = |\Phi^+\rangle$', ha='center', fontsize=10, color=fs.VEL)
    ax.text(3.0, -0.55, '제어 ●, 표적 ⊕', ha='center', fontsize=8, color=fs.GRAY)
    ax.text(5.9, -0.55, '측정', ha='center', fontsize=8, color=fs.GRAY)
    fs.arrow(ax, (0.2, -0.55), (1.6, -0.55), lw=0.8, ms=7, color=fs.GRAY)
    ax.text(0.9, -0.42, '시간', ha='center', va='bottom', fontsize=7.5, color=fs.GRAY)
    fs.save(fig, __file__, 'figSA_05')


# ---------------------------------------------------------------- 그림 A.6 양자 순간이동 회로
def fig06():
    fig, ax = fs.canvas(5.4, 2.4, xlim=(-1.2, 8.3), ylim=(-0.85, 2.85))
    y1, y2, y3 = 2.0, 1.0, 0.0
    wire(ax, y1, 0, 5.1); wire(ax, y2, 0, 5.1); wire(ax, y3, 0, 7.6)
    ax.text(-0.1, y1, r'$|\psi\rangle$', ha='right', va='center', fontsize=11)
    ax.text(-0.1, y2, r'$|0\rangle$', ha='right', va='center', fontsize=11)
    ax.text(-0.1, y3, r'$|0\rangle$', ha='right', va='center', fontsize=11)
    ax.text(-0.75, 1.5, '앨리스', ha='center', va='center', fontsize=8, rotation=90, color=fs.FORCE)
    ax.text(-0.75, 0.0, '밥', ha='center', va='center', fontsize=8, rotation=90, color=fs.VEL)
    gate(ax, 0.7, y2, 'H'); cnot(ax, 1.5, y2, y3)
    ax.add_patch(Rectangle((0.3, -0.4), 1.6, 1.75, fc='none', ec=fs.ACC, lw=0.8, ls='--'))
    ax.text(1.1, -0.65, '벨 쌍 준비', ha='center', fontsize=8, color=fs.ACC)
    cnot(ax, 2.7, y1, y2); gate(ax, 3.5, y1, 'H')
    meter(ax, 4.6, y1); meter(ax, 4.6, y2)
    ax.add_patch(Rectangle((2.3, 0.6), 2.75, 1.85, fc='none', ec=fs.FORCE, lw=0.8, ls='--'))
    ax.text(3.65, 2.62, '벨 측정', ha='center', fontsize=8, color=fs.FORCE)
    # 고전 통신
    wire(ax, y2, 4.87, 5.9, classical=True); wire(ax, y1, 4.87, 6.9, classical=True)
    for x, y in ((5.9, y2), (6.9, y1)):
        ax.plot([x - 0.04, x - 0.04], [y, y3 + 0.25], color=fs.BLACK, lw=0.8)
        ax.plot([x + 0.04, x + 0.04], [y, y3 + 0.25], color=fs.BLACK, lw=0.8)
        ax.add_patch(Circle((x, y), 0.05, color=fs.BLACK, zorder=5))
    gate(ax, 5.9, y3, 'X', fc='#fbe5dc'); gate(ax, 6.9, y3, 'Z', fc='#fbe5dc')
    ax.text(5.05, y2 + 0.2, '$m_2$', fontsize=8.5); ax.text(5.05, y1 + 0.2, '$m_1$', fontsize=8.5)
    ax.text(7.7, y3, r'$|\psi\rangle$', ha='left', va='center', fontsize=11, color=fs.VEL)
    ax.text(6.4, -0.65, '2비트 고전 통신에 따라 보정', ha='center', fontsize=8, color='#555555')
    fs.save(fig, __file__, 'figSA_06')


# ---------------------------------------------------------------- 그림 A.7 LC와 트랜스몬 준위 (본문 코드)
def transmon_levels(EJ_over_EC, ng=0.0, N=30, k=4):
    n = np.arange(-N, N + 1)
    Hm = np.diag(4.0 * (n - ng) ** 2)
    Hm -= EJ_over_EC / 2 * (np.eye(2 * N + 1, k=1) + np.eye(2 * N + 1, k=-1))
    return np.linalg.eigvalsh(Hm)[:k]


def fig07():
    r = 50.0
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.8), sharey=True)
    phi = np.linspace(-np.pi, np.pi, 400)
    hw = np.sqrt(8 * r)
    # (가) LC: 조화 퍼텐셜 E_J phi^2/2 (바닥 -E_J에 맞춤)
    U_h = -r + r * phi ** 2 / 2
    E_h = -r + hw * (np.arange(4) + 0.5)
    U_c = -r * np.cos(phi)
    E_t = transmon_levels(r)
    for a, U, E, title in ((axs[0], U_h, E_h, '(가) LC 회로: 등간격'), (axs[1], U_c, E_t, '(나) 트랜스몬: 비등간격')):
        a.plot(phi, U, color=fs.BLACK, lw=1.3)
        for i, e in enumerate(E):
            if a is axs[0]:
                w = np.sqrt(2 * (e + r) / r)
            else:
                w = np.arccos(np.clip(-e / r, -1, 1))
            a.plot([-w, w], [e, e], color=fs.VEL, lw=1.3)
            a.text(w + 0.08, e, f'$|{i}\\rangle$', fontsize=8, va='center', color=fs.VEL)
        for i in range(2):
            d = E[i + 1] - E[i]
            x = -2.75 + 0.0 * i
            a.annotate('', xy=(x + 0.35 * i, E[i + 1]), xytext=(x + 0.35 * i, E[i]),
                       arrowprops=dict(arrowstyle='<|-|>', lw=0.7, color=fs.FORCE, mutation_scale=7))
            a.text(x + 0.35 * i - 0.08, (E[i] + E[i + 1]) / 2, f'{d:.1f}', fontsize=7, color=fs.FORCE, ha='right', va='center')
        a.set_xlim(-np.pi, np.pi); a.set_ylim(-55, 40)
        a.set_xticks([-np.pi, 0, np.pi]); a.set_xticklabels([r'$-\pi$', '0', r'$\pi$'], fontsize=8)
        a.set_xlabel(r'위상차 $\varphi$', fontsize=9)
        a.set_title(title, fontsize=9)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
        a.tick_params(labelsize=8)
    axs[0].set_ylabel(r'에너지 ($E_C$ 단위)', fontsize=9)
    axs[0].text(0, 33, r'$\frac{E_J}{2}\varphi^2 - E_J$', ha='center', fontsize=9)
    axs[1].text(0, 33, r'$-E_J\cos\varphi$', ha='center', fontsize=9)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'figSA_07')


# ---------------------------------------------------------------- 그림 A.8 기울어진 빨래판 퍼텐셜
def fig08():
    i = 0.3
    phi = np.linspace(-3.0, 10.5, 800)
    U = -np.cos(phi) - i * phi
    fig, ax = fs.plot_axes(4.4, 2.6)
    ax.grid(False)
    ax.plot(phi, U, color=fs.BLACK, lw=1.4)
    pm = np.arcsin(i)                       # 우물 바닥
    pM = np.pi - np.arcsin(i)               # 장벽 꼭대기
    Um, UM = -np.cos(pm) - i * pm, -np.cos(pM) - i * pM
    for e in (Um + 0.2, Um + 0.55):
        xs = phi[(phi > pm - 3) & (phi < pM)]
        inside = xs[(-np.cos(xs) - i * xs) <= e]
        ax.plot([inside.min(), inside.max()], [e, e], color=fs.VEL, lw=1.2)
    e = Um + 0.2
    ax.add_patch(Circle((pm, e), 0.1, fc=fs.FORCE, ec='none', zorder=5))
    xs = phi[(phi > pM) & (phi < pM + 4)]
    xr = xs[(-np.cos(xs) - i * xs) <= e].min()
    ax.annotate('', xy=(xr + 0.4, e), xytext=(pm + 0.3, e),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, ls='--', color=fs.FORCE))
    ax.text(xr + 0.5, e + 0.1, '거시적 양자\n터널링', fontsize=8, color=fs.FORCE, ha='left', va='bottom')
    ax.annotate('', xy=(pM + 0.7, UM - 0.1), xytext=(pm - 0.6, Um + 0.75),
                arrowprops=dict(arrowstyle='-|>', lw=0.8, color=fs.GRAY, connectionstyle='arc3,rad=-0.45'))
    ax.text(pm - 0.3, UM + 0.75, '열적 넘음(고온)', fontsize=7.5, color=fs.GRAY, ha='center')
    ax.text(pm, Um - 0.15, '우물에 갇힘\n(전압 0)', fontsize=7.5, ha='center', va='top')
    ax.text(8.2, -1.3, '탈출 후 굴러 내려감\n(전압 발생)', fontsize=7.5, ha='center')
    ax.text(-2.8, -1.05, r'$U = -E_J\cos\varphi - \frac{\hbar I}{2e}\varphi$', fontsize=9, ha='left')
    ax.set_xlim(-3.0, 10.5); ax.set_ylim(-4.3, 2.0)
    ax.set_xlabel(r'위상차 $\varphi$', fontsize=9); ax.set_ylabel(r'$U(\varphi)$', fontsize=9)
    ax.set_yticks([]); ax.set_xticks([])
    fs.save(fig, __file__, 'figSA_08')


# ---------------------------------------------------------------- 그림 A.9 그로버 알고리즘 (본문 코드)
def grover(n, marked, iters):
    N = 2 ** n
    s = np.ones(N) / np.sqrt(N)
    psi = s.copy()
    for _ in range(iters):
        psi[marked] *= -1
        psi = 2 * s * (s @ psi) - psi
    return np.abs(psi[marked]) ** 2


def fig09():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.4, 2.6), gridspec_kw={'width_ratios': [1, 1.25]})
    a1.set_aspect('equal'); a1.axis('off'); a1.set_xlim(-0.55, 1.35); a1.set_ylim(-0.45, 1.3)
    N = 16; th = np.arcsin(1 / np.sqrt(N))
    fs.arrow(a1, (0, 0), (1.2, 0), lw=0.8, ms=7, color=fs.GRAY); fs.arrow(a1, (0, 0), (0, 1.2), lw=0.8, ms=7, color=fs.GRAY)
    a1.text(1.22, -0.1, r"$|s'\rangle$", fontsize=8.5, color=fs.GRAY)
    a1.text(0.06, 1.22, r'$|w\rangle$ (답)', fontsize=8.5, color=fs.GRAY)
    a1.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=90, color='#cccccc', lw=0.6))
    for k, c in ((0, fs.VEL), (1, fs.ACC), (2, fs.ORANGE), (3, fs.FORCE)):
        ang = (2 * k + 1) * th
        fs.arrow(a1, (0, 0), (np.cos(ang), np.sin(ang)), color=c, lw=1.3, ms=8)
        a1.text(1.08 * np.cos(ang), 1.08 * np.sin(ang), f'$k={k}$', fontsize=7.5, color=c,
                ha='left' if ang < np.pi / 2 else 'right', va='center')
    fs.angle_arc(a1, (0, 0), 0.3, 0, np.degrees(th), r'$\theta$', fontsize=8, tr=0.42)
    # 오라클 반사 (s' 축에 대한 반사) 표시
    a1.plot([np.cos(th), np.cos(th)], [np.sin(th), -np.sin(th)], color=fs.GRAY, lw=0.6, ls=':')
    a1.plot(np.cos(th), -np.sin(th), 'o', color=fs.GRAY, ms=3)
    a1.text(np.cos(th) - 0.05, -np.sin(th) - 0.12, '오라클 뒤', fontsize=7, color=fs.GRAY, ha='center', va='top')
    a1.set_title(f'(가) 매 반복 $2\\theta$ 회전 ($N = {N}$)', fontsize=8.5)
    style(a2)
    ks = np.arange(0, 13)
    P = [grover(4, 3, k) for k in ks]
    kk = np.linspace(0, 12, 400)
    a2.plot(kk, np.sin((2 * kk + 1) * th) ** 2, color=fs.GRAY, lw=0.8, ls='--', label=r'$\sin^2((2k+1)\theta)$')
    a2.plot(ks, P, 'o', color=fs.VEL, ms=4, label='시뮬레이션', zorder=5)
    a2.plot(3, P[3], 'o', color=fs.FORCE, ms=6, zorder=6)
    a2.text(3.4, P[3] - 0.06, f'$k = 3$: {P[3]:.4f}', fontsize=7.5, color=fs.FORCE)
    a2.set_xlim(-0.3, 12.3); a2.set_ylim(0, 1.32)
    a2.set_xlabel('반복 횟수 $k$', fontsize=9); a2.set_ylabel('성공 확률', fontsize=9)
    a2.legend(fontsize=7, loc='upper center', frameon=False, ncol=2)
    a2.set_title(f'(나) $N = 16$', fontsize=8.5)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'figSA_09')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09):
        f()
