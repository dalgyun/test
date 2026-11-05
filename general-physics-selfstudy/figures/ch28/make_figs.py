"""28장 전자기 유도와 인덕턴스 — 그림 생성 스크립트.
python3 figures/ch28/make_figs.py  (FIG_PREVIEW=<폴더> 를 주면 PNG 미리보기도 저장)
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon, Ellipse, Wedge

F = fs.FIELD
sd, elm = fs.schem()


# ---------- 도우미 ----------
def tip(ax, p, d, color=F, ms=10, zorder=5):
    """점 p에서 방향 d로 향하는 화살촉만."""
    p = np.asarray(p, float); d = np.asarray(d, float); d = d / (np.hypot(*d) + 1e-12)
    ax.add_patch(FancyArrowPatch(p - d * 0.02, p + d * 0.02, arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=zorder))


def circ_arrow(ax, c, r, th0, th1, color=F, lw=1.0, ms=10, arrow_at=(), ls='-', zorder=3):
    th = np.radians(np.linspace(th0, th1, 200))
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color=color, lw=lw, ls=ls, zorder=zorder)
    sgn = 1 if th1 > th0 else -1
    for a in arrow_at:
        a = np.radians(a)
        tip(ax, (c[0] + r * np.cos(a), c[1] + r * np.sin(a)), sgn * np.array([-np.sin(a), np.cos(a)]),
            color=color, ms=ms, zorder=zorder + 1)


def ring(ax, c, rx, ry, color=fs.BLACK, lw=1.6, sense=+1, arrows=(), ms=11, zorder=3, near='bottom'):
    """비스듬히 본 고리. 점 (c + (rx cos φ, ry sin φ)). sense=+1이면 φ가 증가하는 방향으로 전류.
    near='bottom'이면 아래 절반이 앞쪽(실선), 'left'면 왼쪽 절반이 앞쪽."""
    ph = np.linspace(0, 2 * np.pi, 300)
    x = c[0] + rx * np.cos(ph); y = c[1] + ry * np.sin(ph)
    front = (np.sin(ph) < 0) if near == 'bottom' else (np.cos(ph) < 0)
    xb, yb = x.copy(), y.copy(); xb[front] = np.nan; yb[front] = np.nan
    xf, yf = x.copy(), y.copy(); xf[~front] = np.nan; yf[~front] = np.nan
    ax.plot(xb, yb, color=color, lw=lw * 0.7, ls='--', zorder=zorder - 1)
    ax.plot(xf, yf, color=color, lw=lw, zorder=zorder + 1)
    for a in arrows:
        a = np.radians(a)
        p = (c[0] + rx * np.cos(a), c[1] + ry * np.sin(a))
        tip(ax, p, sense * np.array([-rx * np.sin(a), ry * np.cos(a)]), color=color, ms=ms, zorder=zorder + 2)


def zigzag(ax, p, q, n=6, w=0.12, color=fs.BLACK, lw=1.3):
    fs.spring(ax, p, q, coils=n // 2 if n > 2 else 2, width=w, color=color, lw=lw, lead=0.12)


def magnet(ax, x0, y0, w, h, left='S', right='N'):
    """가로로 놓인 막대자석(왼쪽 절반/오른쪽 절반 색 구분)."""
    cols = {'N': '#d9534f', 'S': '#5b8bd0'}
    ax.add_patch(Rectangle((x0, y0 - h / 2), w / 2, h, fc=cols[left], ec=fs.BLACK, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((x0 + w / 2, y0 - h / 2), w / 2, h, fc=cols[right], ec=fs.BLACK, lw=1.0, zorder=4))
    ax.text(x0 + w / 4, y0, left, color='white', ha='center', va='center', fontsize=11, fontweight='bold', zorder=5)
    ax.text(x0 + 3 * w / 4, y0, right, color='white', ha='center', va='center', fontsize=11, fontweight='bold', zorder=5)


def graph_ax(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# ---------- 그림 28.1 자기 선속 ----------
def fig01():
    fig, ax = fs.canvas(3.4, 2.8, xlim=(-1.9, 2.1), ylim=(-1.2, 2.2))
    th = np.radians(35)
    ax.add_patch(Ellipse((0, 0), 2.6, 0.8, fc=fs.SURF, alpha=0.45, ec=fs.BLACK, lw=1.2, zorder=1))
    ax.text(-1.05, -0.45, r'넓이 $A$', fontsize=9, ha='center', va='top')
    d = np.array([np.sin(th), np.cos(th)])
    for x0 in np.linspace(-1.1, 1.1, 5):
        p = np.array([x0, 0.0]) - d * 0.75
        q = np.array([x0, 0.0]) + d * 1.8
        ax.plot([p[0], q[0]], [p[1], q[1]], color=F, lw=1.0, zorder=0 if True else 2)
        tip(ax, q - d * 0.25, d, color=F, ms=9)
    ax.text(2.0, 1.75, r'$\vec{B}$', fontsize=12, color=F)
    fs.arrow(ax, (0, 0), (0, 1.5), color=fs.BLACK, lw=1.8, zorder=6)
    ax.text(-0.12, 1.5, r'$\hat{n}$', fontsize=12, ha='right', va='center')
    fs.angle_arc(ax, (0, 0), 0.75, 90 - np.degrees(th), 90, r'$\theta$', fontsize=11, tr=0.95)
    fs.dot(ax, (0, 0), r=0.04)
    fs.save(fig, __file__, 'fig28_01')


# ---------- 그림 28.3 렌츠 법칙: 자석과 코일 ----------
def fig02():
    fig, axs = plt.subplots(2, 1, figsize=(4.4, 3.4))
    for ax, approach in [(axs[0], True), (axs[1], False)]:
        ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.0, 1.0); ax.set_aspect('equal'); ax.axis('off')
        magnet(ax, -2.4, 0, 1.5, 0.45, left='S', right='N')
        vx = 0.6 if approach else -0.6
        fs.arrow(ax, (-1.65, 0.48), (-1.65 + vx, 0.48), color=fs.VEL, lw=1.8)
        ax.text(-1.65 + vx / 2, 0.68, r'$\vec{v}$', fontsize=11, color=fs.VEL, ha='center')
        cx = 0.9
        # 자석의 자기장(오른쪽)
        fs.arrow(ax, (-0.85, -0.05), (2.3, -0.05), color=F, lw=1.0, ms=9)
        ax.text(2.35, -0.05, r'자석의 $\vec{B}$', fontsize=9, color=F, va='center')
        # 유도 자기장: 접근하면 왼쪽(자석 쪽), 멀어지면 오른쪽
        s = -1 if approach else 1
        fs.arrow(ax, (cx - s * 0.45, 0.22), (cx + s * 0.45, 0.22), color=fs.ORANGE, lw=1.8, ms=10, zorder=8)
        ax.text(cx + s * 0.5 + (-0.05 if approach else 0.05), 0.33, r'유도 $\vec{B}$', fontsize=9,
                color=fs.ORANGE, ha='right' if approach else 'left')
        # 고리: 축이 x 방향. 점 (y,w)=(cos φ, sin φ) → 종이 (cx - rx sin φ, ry cos φ). 왼쪽 절반이 앞.
        rx, ry = 0.28, 0.8
        ph = np.linspace(0, 2 * np.pi, 300)
        X = cx - rx * np.sin(ph); Y = ry * np.cos(ph)
        front = np.sin(ph) > 0
        Xb, Yb = X.copy(), Y.copy(); Xb[front] = np.nan
        Xf, Yf = X.copy(), Y.copy(); Xf[~front] = np.nan
        ax.plot(Xb, Yb, color=fs.BLACK, lw=1.1, ls='--', zorder=2)
        ax.plot(Xf, Yf, color=fs.BLACK, lw=2.0, zorder=6)
        # μ_ind = s x̂ ↔ (y,w) 평면에서 s=+1이면 φ 증가 방향 전류
        for a in (60, 120):
            a = np.radians(a)
            dpdphi = np.array([-rx * np.cos(a), -ry * np.sin(a)])
            tip(ax, (cx - rx * np.sin(a), ry * np.cos(a)), s * dpdphi, color=fs.BLACK, ms=12, zorder=7)
        ax.text(cx - 0.35, -0.75, r'$I$', fontsize=11, ha='right')
        pole = 'N' if approach else 'S'
        ax.text(cx - 0.55, 0.62, pole, fontsize=11, fontweight='bold',
                color='#d9534f' if pole == 'N' else '#5b8bd0', ha='center')
        title = '(가) 다가갈 때: 선속 증가 → 밀어냄' if approach else '(나) 멀어질 때: 선속 감소 → 끌어당김'
        ax.text(0, -0.98, title, fontsize=9, ha='center')
    fig.subplots_adjust(hspace=0.12)
    fs.save(fig, __file__, 'fig28_03')


# ---------- 그림 28.4 구리관 속 자석과 와전류 ----------
def fig03():
    fig, ax = fs.canvas(2.6, 3.3, xlim=(-1.4, 1.6), ylim=(-2.1, 2.0))
    r, ry = 0.75, 0.2
    ax.add_patch(Rectangle((-r, -1.9), 2 * r, 3.7, fc='#f0d9c4', alpha=0.55, ec='none', zorder=0))
    ax.plot([-r, -r], [-1.9, 1.8], color='#a0522d', lw=1.3); ax.plot([r, r], [-1.9, 1.8], color='#a0522d', lw=1.3)
    ax.add_patch(Ellipse((0, 1.8), 2 * r, 2 * ry, fc='#f6e7da', ec='#a0522d', lw=1.1, zorder=1))
    # 자석 (N이 아래)
    ax.add_patch(Rectangle((-0.22, 0.0), 0.44, 0.4, fc='#5b8bd0', ec=fs.BLACK, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((-0.22, -0.4), 0.44, 0.4, fc='#d9534f', ec=fs.BLACK, lw=1.0, zorder=4))
    ax.text(0, 0.2, 'S', color='white', ha='center', va='center', fontsize=10, fontweight='bold', zorder=5)
    ax.text(0, -0.2, 'N', color='white', ha='center', va='center', fontsize=10, fontweight='bold', zorder=5)
    fs.arrow(ax, (1.05, 0.35), (1.05, -0.35), color=fs.VEL, lw=1.8)
    ax.text(1.18, 0.0, r'$\vec{v}$', fontsize=11, color=fs.VEL, va='center')
    # 와전류: 아래 고리는 위에서 볼 때 반시계(위로 향하는 자기 모멘트), 위 고리는 시계
    ring(ax, (0, -1.05), r, ry, color=fs.ORANGE, lw=1.6, sense=+1, arrows=(-90, 90), ms=10, zorder=5)
    ring(ax, (0, 1.05), r, ry, color=fs.ORANGE, lw=1.6, sense=-1, arrows=(-90, 90), ms=10, zorder=5)
    ax.text(-1.35, -1.05, '와전류', fontsize=9, color=fs.ORANGE, ha='left', va='center', rotation=90)
    ax.text(-1.35, 1.05, '와전류', fontsize=9, color=fs.ORANGE, ha='left', va='center', rotation=90)
    ax.text(0, -2.05, '구리관', fontsize=9, ha='center', color='#a0522d')
    fs.save(fig, __file__, 'fig28_04')


# ---------- 그림 28.5 미끄러지는 막대 ----------
def fig04():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.8, 5.2), ylim=(-1.6, 1.65))
    yt, yb, xr = 1.0, -1.0, 3.1
    fs.field_grid(ax, (0.15, 5.1), (-0.95, 1.5), kind='in', step=0.48, r=0.07)
    ax.plot([0, 5.0], [yt, yt], color=fs.BLACK, lw=1.8, zorder=3)
    ax.plot([0, 5.0], [yb, yb], color=fs.BLACK, lw=1.8, zorder=3)
    ax.plot([0, 0], [yt, 0.45], color=fs.BLACK, lw=1.8, zorder=3)
    ax.plot([0, 0], [-0.45, yb], color=fs.BLACK, lw=1.8, zorder=3)
    zigzag(ax, (0, 0.45), (0, -0.45), n=8, w=0.13)
    ax.add_patch(Rectangle((-0.2, -0.45), 0.4, 0.9, fc='white', ec='none', zorder=2))
    ax.text(-0.25, 0, r'$R$', fontsize=11, ha='right', va='center')
    ax.add_patch(Rectangle((xr - 0.07, yb - 0.12), 0.14, yt - yb + 0.24, fc='#b0b7c0', ec=fs.BLACK, lw=1.0, zorder=7))
    fs.arrow(ax, (xr + 0.15, 0.25), (xr + 1.0, 0.25), color=fs.VEL, lw=2.0, zorder=8)
    ax.text(xr + 0.6, 0.42, r'$\vec{v}$', fontsize=11, color=fs.VEL, ha='center', zorder=8)
    fs.arrow(ax, (xr - 0.15, -0.3), (xr - 1.0, -0.3), color=fs.FORCE, lw=2.0, zorder=8)
    ax.text(xr - 0.6, -0.12, r'$\vec{F}_B$', fontsize=11, color=fs.FORCE, ha='center', zorder=8)
    # 유도 전류: 반시계 (막대에서 위로)
    tip(ax, (xr, 0.65), (0, 1), color=fs.ORANGE, ms=13, zorder=9)
    tip(ax, (1.6, yt), (-1, 0), color=fs.ORANGE, ms=13, zorder=9)
    tip(ax, (1.6, yb), (1, 0), color=fs.ORANGE, ms=13, zorder=9)
    ax.text(xr + 0.15, 0.75, r'$I$', fontsize=11, color=fs.ORANGE)
    ax.annotate('', xy=(xr + 0.25, yt), xytext=(xr + 0.25, yb), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(xr + 0.33, -0.65, r'$L$', fontsize=11, color=fs.GRAY)
    ax.annotate('', xy=(xr, -1.35), xytext=(0, -1.35), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(xr / 2, -1.45, r'$x$', fontsize=11, color=fs.GRAY, ha='center', va='top')
    ax.text(5.15, 1.45, r'$\vec{B}$ (⊗)', fontsize=10, color=F, ha='right', va='bottom')
    fs.save(fig, __file__, 'fig28_05')


# ---------- 그림 28.6 예제 28.2: v(t), x(t) ----------
def fig05():
    tau, v0 = 0.50, 2.0
    t = np.linspace(0, 2.5, 300)
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    for a in axs: graph_ax(a)
    axs[0].plot(t, v0 * np.exp(-t / tau), color=fs.VEL, lw=1.8)
    axs[0].plot([0, tau], [v0, 0], color=fs.GRAY, lw=0.8, ls='--')
    axs[0].axvline(tau, color=fs.GRAY, lw=0.6, ls=':')
    axs[0].text(tau + 0.05, 1.3, r'$\tau = 0.50$ s', fontsize=8.5, color=fs.GRAY)
    axs[0].set_xlabel(r'$t$ (s)'); axs[0].set_ylabel(r'$v$ (m/s)'); axs[0].set_ylim(0, 2.2); axs[0].set_xlim(0, 2.5)
    axs[0].set_title('(가) 속력', fontsize=9)
    axs[1].plot(t, v0 * tau * (1 - np.exp(-t / tau)), color=fs.BLACK, lw=1.8)
    axs[1].axhline(v0 * tau, color=fs.FORCE, lw=0.9, ls='--')
    axs[1].text(2.45, 0.93, r'$x_\infty = v_0\tau = 1.0$ m', fontsize=8.5, color=fs.FORCE, ha='right', va='top')
    axs[1].set_xlabel(r'$t$ (s)'); axs[1].set_ylabel(r'$x$ (m)'); axs[1].set_ylim(0, 1.15); axs[1].set_xlim(0, 2.5)
    axs[1].set_title('(나) 간 거리', fontsize=9)
    fig.subplots_adjust(wspace=0.35)
    fs.save(fig, __file__, 'fig28_06')


# ---------- 그림 28.7 교류 발전기 (위에서 본 모습) ----------
def fig06():
    fig, ax = fs.canvas(3.6, 2.6, xlim=(-2.3, 2.3), ylim=(-1.55, 1.6))
    for x0, lab, col in [(-2.25, 'N', '#d9534f'), (1.55, 'S', '#5b8bd0')]:
        ax.add_patch(Rectangle((x0, -1.1), 0.7, 2.2, fc=col, ec=fs.BLACK, lw=1.0, zorder=1))
        ax.text(x0 + 0.35, 0, lab, color='white', fontsize=13, fontweight='bold', ha='center', va='center')
    for y in (-0.8, -0.4, 0.4, 0.8):
        fs.arrow(ax, (-1.5, y), (1.5, y), color=F, lw=0.9, ms=9, zorder=1)
    ax.text(1.45, 0.98, r'$\vec{B}$', fontsize=11, color=F, ha='right')
    th = np.radians(50)   # 법선과 B 사이 각
    n = np.array([np.cos(th), np.sin(th)])
    t = np.array([-n[1], n[0]])
    half = 0.85
    ax.plot([-t[0] * half, t[0] * half], [-t[1] * half, t[1] * half], color=fs.BLACK, lw=3.2, zorder=4,
            solid_capstyle='round')
    fs.dot_out(ax, t * half, r=0.09); fs.cross_in(ax, -t * half, r=0.09)
    fs.arrow(ax, (0, 0), n * 1.1, color=fs.BLACK, lw=1.6, zorder=6)
    ax.text(*(n * 1.25 + np.array([0.05, 0.0])), r'$\hat{n}$', fontsize=12, ha='center', va='center')
    ax.plot([0, 1.0], [0, 0], color=fs.GRAY, lw=0.7, ls='--', zorder=5)
    fs.angle_arc(ax, (0, 0), 0.5, 0, np.degrees(th), r'$\theta=\omega t$', fontsize=9.5, tr=0.82)
    circ_arrow(ax, (0, 0), 1.25, 115, 150, color=fs.BLACK, lw=1.0, arrow_at=[150], ms=9)
    ax.text(-0.85, 1.2, r'$\omega$', fontsize=11)
    ax.add_patch(Circle((0, 0), 0.06, color=fs.BLACK, zorder=7))
    ax.text(0, -1.5, '회전축은 지면에 수직(⊙ 쪽 변과 ⊗ 쪽 변이 코일의 두 긴 변)', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig28_07')


# ---------- 그림 28.8 발전기의 선속과 기전력 ----------
def fig07():
    x = np.linspace(0, 4 * np.pi, 600)
    fig, ax = fs.plot_axes(4.2, 2.4)
    ax.plot(x, np.cos(x), color=F, lw=1.6, label=r'선속 $\Phi_B/BA = \cos\omega t$')
    ax.plot(x, np.sin(x), color=fs.FORCE, lw=1.8, label=r'기전력 $\mathcal{E}/\mathcal{E}_{\max} = \sin\omega t$')
    ax.set_xticks(np.arange(0, 4.01 * np.pi, np.pi / 2))
    ax.set_xticklabels(['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$',
                        r'$\frac{5\pi}{2}$', r'$3\pi$', r'$\frac{7\pi}{2}$', r'$4\pi$'])
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    ax.set_xlabel(r'$\omega t$'); ax.set_ylim(-1.25, 1.6); ax.set_xlim(0, 4 * np.pi)
    ax.plot([np.pi / 2], [1], 'o', color=fs.FORCE, ms=4); ax.plot([np.pi / 2], [0], 'o', color=F, ms=4)
    ax.legend(fontsize=8, loc='upper right', frameon=False, ncol=2)
    fs.save(fig, __file__, 'fig28_08')


# ---------- 그림 28.9 솔레노이드 안팎의 유도 전기장 ----------
def fig08():
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.5), gridspec_kw={'width_ratios': [1, 1.25]})
    ax = axs[0]; ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.0, 2.0); ax.set_aspect('equal'); ax.axis('off')
    R = 1.0
    ax.add_patch(Circle((0, 0), R, fc='#f3eef7', ec=fs.BLACK, lw=1.2, zorder=0))
    for x in np.arange(-0.6, 0.61, 0.4):
        for y in np.arange(-0.6, 0.61, 0.4):
            if x * x + y * y < 0.75:
                fs.dot_out(ax, (x, y), r=0.07, color=F)
    for r in (0.5, 1.5):
        circ_arrow(ax, (0, 0), r, 360, 0, color=fs.ORANGE, lw=1.3, arrow_at=[45, 225] if r > 1 else [140, 320], ms=10)
    ax.text(1.12, 1.42, r'$\vec{E}$', fontsize=11, color=fs.ORANGE)
    fs.arrow(ax, (0, 0), (R * np.cos(np.radians(-60)), R * np.sin(np.radians(-60))), color=fs.BLACK, lw=0.8, ms=7)
    ax.text(0.15, -0.6, r'$R$', fontsize=10)
    ax.text(0, -1.95, r'$\vec{B}$(⊙)가 증가', fontsize=9, ha='center', color=F)
    ax = axs[1]; graph_ax(ax)
    Rm, dB = 0.05, 0.10
    r = np.linspace(0, 0.15, 400)
    E = np.where(r < Rm, r / 2 * dB, Rm ** 2 / (2 * np.maximum(r, 1e-9)) * dB) * 1e3
    ax.plot(r * 100, E, color=fs.ORANGE, lw=1.8)
    ax.axvline(5, color=fs.GRAY, lw=0.7, ls=':')
    for rr in (2, 10):
        e = (rr / 100 / 2 * dB if rr < 5 else Rm ** 2 / (2 * rr / 100) * dB) * 1e3
        ax.plot(rr, e, 'o', color=fs.BLACK, ms=4)
        ax.text(rr + 0.4, e + 0.12, '1.0' if rr == 2 else '1.25', fontsize=8.5)
    ax.text(5.3, 2.55, r'$r = R$', fontsize=8.5, color=fs.GRAY)
    ax.set_xlabel(r'$r$ (cm)'); ax.set_ylabel(r'$E$ (mV/m)')
    ax.set_xlim(0, 15); ax.set_ylim(0, 2.9)
    fig.subplots_adjust(wspace=0.2)
    fs.save(fig, __file__, 'fig28_09')


# ---------- 그림 28.2 솔레노이드 안의 작은 코일 (예제 28.1) ----------
def fig09():
    fig, ax = fs.canvas(4.2, 2.2, xlim=(-2.6, 2.6), ylim=(-1.35, 1.35))
    a = 1.0
    for x in np.arange(-2.3, 2.35, 0.3):
        fs.dot_out(ax, (x, a), r=0.1); fs.cross_in(ax, (x, -a), r=0.1)
    for y in (-0.7, 0.7):
        fs.arrow(ax, (-2.45, y), (2.45, y), color=F, lw=1.0, ms=9)
    ax.text(2.5, 0.72, r'$\vec{B}$', fontsize=11, color=F, va='center')
    # 작은 코일 (지름 2.0 cm ↔ 솔레노이드보다 작음)
    for x in np.linspace(-0.3, 0.3, 6):
        ax.add_patch(Ellipse((x, 0), 0.14, 0.9, fc='none', ec=fs.ORANGE, lw=1.4, zorder=4))
    fs.arrow(ax, (-1.2, 0), (1.2, 0), color=F, lw=1.0, ms=9, zorder=2)
    ax.text(0.45, -0.38, r'$N = 100$', fontsize=9, color=fs.ORANGE)
    ax.text(0.45, 0.25, '작은 코일', fontsize=8.5, color=fs.ORANGE)
    ax.text(-2.55, 1.25, r'솔레노이드: $n$, 전류 $I(t)$', fontsize=9, va='bottom')
    fs.save(fig, __file__, 'fig28_02')


# ---------- 그림 28.10 직사각형 단면의 토로이드 ----------
def fig10():
    fig, ax = fs.canvas(3.8, 2.2, xlim=(-2.9, 2.9), ylim=(-1.0, 1.4))
    a, b, h = 1.2, 2.4, 1.0
    ax.plot([0, 0], [-0.9, 1.3], color=fs.GRAY, lw=0.8, ls='-.')
    for s in (-1, 1):
        x0 = s * a if s > 0 else -b
        ax.add_patch(Rectangle((x0, -h / 2), b - a, h, fc='#f3eef7', ec=fs.BLACK, lw=1.2))
    fs.cross_in(ax, (1.8, 0.0), r=0.12, color=F); fs.dot_out(ax, (-1.8, 0.0), r=0.12, color=F)
    r, dr = 1.75, 0.18
    ax.add_patch(Rectangle((r, -h / 2), dr, h, fc=F, alpha=0.35, ec=F, lw=0.8))
    ax.annotate('', xy=(a, -0.75), xytext=(0, -0.75), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(a / 2, -0.82, r'$a$', fontsize=10, color=fs.GRAY, ha='center', va='top')
    ax.annotate('', xy=(b, 0.85), xytext=(0, 0.85), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(b / 2, 0.9, r'$b$', fontsize=10, color=fs.GRAY, ha='center', va='bottom')
    ax.annotate('', xy=(b + 0.2, h / 2), xytext=(b + 0.2, -h / 2), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(b + 0.28, 0, r'$h$', fontsize=10, color=fs.GRAY, va='center')
    ax.text(r + dr / 2, -h / 2 - 0.05, r'$dr$', fontsize=9, color=F, ha='center', va='top')
    ax.text(-1.8, -0.75, r'$\vec{B}$ (나옴)', fontsize=8.5, color=F, ha='center', va='top')
    fs.save(fig, __file__, 'fig28_10')


# ---------- 그림 28.11 RL 회로 ----------
def fig11():
    fig, ax = plt.subplots(figsize=(3.2, 2.2))
    d = sd.Drawing(canvas=ax)
    d += (bat := elm.BatteryCell().up().reverse().label(r'$\mathcal{E}$', loc='bottom', ofst=0.3))
    d += (sw := elm.Switch().right().label(r'$S$', loc='top'))
    d += (res := elm.Resistor().right().label(r'$R$', loc='top'))
    d += (ind := elm.Inductor2(loops=4).down().label(r'$L$', loc='bottom', ofst=0.25))
    d += elm.Line().left().tox(bat.start)
    d.draw(show=False)
    ax.axis('off'); ax.set_aspect('equal')
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - 0.4, x1 + 0.4); ax.set_ylim(y0 - 0.5, y1 + 0.3)
    yb = bat.start[1]
    fs.arrow(ax, (4.6, yb + 0.35), (3.0, yb + 0.35), color=fs.ORANGE, lw=1.3, ms=10)
    ax.text(3.8, yb + 0.5, r'$I$', fontsize=11, color=fs.ORANGE, ha='center')
    ax.text(bat.end[0] - 0.3, bat.end[1] - 0.45, '+', fontsize=10, ha='right')
    fs.save(fig, __file__, 'fig28_11')


# ---------- 그림 28.12 RL 회로의 전류 ----------
def fig12():
    tau, Iinf = 5.0, 2.0
    t = np.linspace(0, 30, 400)
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.4))
    for a in axs: graph_ax(a)
    ax = axs[0]
    ax.plot(t, Iinf * (1 - np.exp(-t / tau)), color=fs.ORANGE, lw=1.8)
    ax.axhline(Iinf, color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([0, tau], [0, Iinf], color=fs.GRAY, lw=0.8, ls=':')
    for tt, lab, dy in [(tau, r'$\tau_L$: 63%', -0.3), (tau * np.log(10), '11.5 ms: 90%', -0.35)]:
        ii = Iinf * (1 - np.exp(-tt / tau))
        ax.plot(tt, ii, 'o', color=fs.BLACK, ms=3.5)
        ax.text(tt + 0.8, ii + dy, lab, fontsize=8.5)
    ax.text(29, Iinf + 0.05, r'$\mathcal{E}/R = 2.0$ A', fontsize=8.5, ha='right', va='bottom', color=fs.GRAY)
    ax.set_xlabel(r'$t$ (ms)'); ax.set_ylabel(r'$I$ (A)'); ax.set_ylim(0, 2.5); ax.set_xlim(0, 30)
    ax.set_title('(가) 스위치를 닫은 뒤 성장', fontsize=9)
    ax = axs[1]
    ax.plot(t, Iinf * np.exp(-t / tau), color=fs.ORANGE, lw=1.8)
    ax.plot([0, tau], [Iinf, 0], color=fs.GRAY, lw=0.8, ls=':')
    ax.plot(tau, Iinf * np.exp(-1), 'o', color=fs.BLACK, ms=3.5)
    ax.text(tau + 0.8, Iinf * np.exp(-1) + 0.05, r'$\tau_L$: 37%', fontsize=8.5)
    ax.set_xlabel(r'$t$ (ms)'); ax.set_ylabel(r'$I$ (A)'); ax.set_ylim(0, 2.5); ax.set_xlim(0, 30)
    ax.set_title(r'(나) 전지를 뺀 뒤 감소 ($I_0 = 2.0$ A)', fontsize=9)
    fig.subplots_adjust(wspace=0.32)
    fs.save(fig, __file__, 'fig28_12')


# ---------- 그림 28.13 RL 회로의 에너지 흐름 (예제 28.6) ----------
def fig13():
    E, R, L = 12.0, 6.0, 0.030
    tau = L / R
    t = np.linspace(0, 6 * tau, 400)
    I = E / R * (1 - np.exp(-t / tau)); dI = E / L * np.exp(-t / tau)
    fig, ax = fs.plot_axes(4.2, 2.6)
    tm = t * 1e3
    ax.plot(tm, E * I, color=fs.BLACK, lw=1.8, label=r'전지 $\mathcal{E}I$')
    ax.plot(tm, I ** 2 * R, color=fs.FORCE, lw=1.6, ls='--', label=r'저항 $I^2R$')
    ax.plot(tm, L * I * dI, color=fs.VEL, lw=1.6, ls='-.', label=r'인덕터 $LI\,dI/dt$')
    ax.axvline(5, color=fs.GRAY, lw=0.7, ls=':')
    It = E / R * (1 - np.exp(-1))
    for v, c in [(E * It, fs.BLACK), (It ** 2 * R, fs.FORCE), (It * E * np.exp(-1), fs.VEL)]:
        ax.plot(5, v, 'o', color=c, ms=3.5)
        ax.text(5.6, v, f'{v:.1f} W', fontsize=8.5, color=c, va='center')
    ax.set_xlabel(r'$t$ (ms)'); ax.set_ylabel('일률 (W)')
    ax.set_xlim(0, 30); ax.set_ylim(0, 26)
    ax.legend(fontsize=8.5, loc='center right', frameon=False)
    fs.save(fig, __file__, 'fig28_13')


# ---------- 그림 28.14 동축 케이블 (예제 28.7) ----------
def fig14():
    fig, ax = fs.canvas(2.7, 2.6, xlim=(-1.55, 1.55), ylim=(-1.5, 1.5))
    a, b = 0.4, 1.3
    ax.add_patch(Circle((0, 0), b + 0.08, fc='#dfe6ee', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), b, fc='white', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), a, fc='#dfe6ee', ec=fs.BLACK, lw=1.0))
    r, dr = 0.85, 0.1
    ax.add_patch(Wedge((0, 0), r + dr, 0, 360, width=dr, fc=F, alpha=0.3, ec=F, lw=0.6))
    circ_arrow(ax, (0, 0), 0.62, 0, 360, color=F, lw=0.9, arrow_at=[100], ms=9)
    ax.text(-0.62, 0.45, r'$\vec{B}$', fontsize=10, color=F)
    fs.dot_out(ax, (0, 0), r=0.09)
    for t, lab in [(90, r'$a$'), (210, r'$b$')]:
        rr = a if lab == r'$a$' else b
        tt = np.radians(t)
        fs.arrow(ax, (0, 0), (rr * np.cos(tt), rr * np.sin(tt)), color=fs.BLACK, lw=0.7, ms=7)
    ax.text(0.1, 0.25, r'$a$', fontsize=10)
    ax.text(-0.6, -0.15, r'$b$', fontsize=10)
    ax.text(0.68, -0.72, r'$r$', fontsize=9, color=F)
    ax.text(0.95, 0.7, r'$dr$', fontsize=9, color=F)
    fs.save(fig, __file__, 'fig28_14')


# ---------- 그림 28.15 떨어지는 막대 (🐍 실습) ----------
def fig15():
    fig, ax = fs.canvas(2.8, 3.0, xlim=(-1.4, 1.9), ylim=(-1.75, 1.75))
    xl, xr = -0.9, 0.9
    fs.field_grid(ax, (-0.85, 0.85), (-1.15, 1.6), kind='in', step=0.42, r=0.065)
    ax.plot([xl, xl], [-1.3, 1.7], color=fs.BLACK, lw=1.8); ax.plot([xr, xr], [-1.3, 1.7], color=fs.BLACK, lw=1.8)
    ax.plot([xl, -0.35], [-1.3, -1.3], color=fs.BLACK, lw=1.8); ax.plot([0.35, xr], [-1.3, -1.3], color=fs.BLACK, lw=1.8)
    zigzag(ax, (-0.35, -1.3), (0.35, -1.3), n=8, w=0.12)
    ax.text(0, -1.5, r'$R$', fontsize=11, ha='center', va='top')
    yr = 0.65
    ax.add_patch(Rectangle((xl - 0.12, yr - 0.07), xr - xl + 0.24, 0.14, fc='#b0b7c0', ec=fs.BLACK, lw=1.0, zorder=7))
    fs.arrow(ax, (1.3, yr + 0.3), (1.3, yr - 0.45), color=fs.VEL, lw=1.8)
    ax.text(1.42, yr - 0.1, r'$\vec{v}$', fontsize=11, color=fs.VEL)
    fs.arrow(ax, (0.25, yr - 0.08), (0.25, yr - 0.75), color=fs.FORCE, lw=1.8, zorder=8)
    ax.text(0.33, yr - 0.6, r'$m\vec{g}$', fontsize=10, color=fs.FORCE)
    fs.arrow(ax, (-0.25, yr + 0.08), (-0.25, yr + 0.6), color=fs.FORCE, lw=1.8, zorder=8)
    ax.text(-0.33, yr + 0.5, r'$\vec{F}_B$', fontsize=10, color=fs.FORCE, ha='right')
    ax.annotate('', xy=(xr, 1.62), xytext=(xl, 1.62), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(0, 1.68, r'$L$', fontsize=10, color=fs.GRAY, ha='center', va='bottom')
    ax.text(1.0, -0.6, r'$\vec{B}$(⊗)', fontsize=9, color=F)
    fs.save(fig, __file__, 'fig28_15')


# ---------- 그림 28.16 연습문제 7 ----------
def fig16():
    fig, ax = fs.canvas(3.2, 2.4, xlim=(-0.8, 3.7), ylim=(-1.55, 1.6))
    ax.plot([0, 0], [-1.5, 1.5], color=fs.BLACK, lw=2.2)
    fs.arrow(ax, (-0.3, -0.35), (-0.3, 0.35), color=fs.BLACK, lw=1.2)
    ax.text(-0.42, 0, r'$I$', fontsize=11, ha='right', va='center')
    x, aa, bb = 1.1, 1.4, 2.0
    ax.add_patch(Rectangle((x, -bb / 2), aa, bb, fc='none', ec=fs.BLACK, lw=1.8))
    fs.arrow(ax, (x + aa + 0.15, 0), (x + aa + 0.85, 0), color=fs.VEL, lw=1.8)
    ax.text(x + aa + 0.5, 0.15, r'$\vec{v}$', fontsize=11, color=fs.VEL, ha='center')
    ax.annotate('', xy=(x, -1.25), xytext=(0, -1.25), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(x / 2, -1.32, r'$x$', fontsize=10, color=fs.GRAY, ha='center', va='top')
    ax.annotate('', xy=(x + aa, -1.25), xytext=(x, -1.25), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(x + aa / 2, -1.32, r'$a$', fontsize=10, color=fs.GRAY, ha='center', va='top')
    ax.annotate('', xy=(x - 0.2, bb / 2), xytext=(x - 0.2, -bb / 2), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.text(x - 0.28, 0, r'$b$', fontsize=10, color=fs.GRAY, ha='right', va='center')
    fs.save(fig, __file__, 'fig28_16')


# ---------- 그림 28.17 연습문제 10 ----------
def fig17():
    fig, ax = fs.canvas(3.8, 2.0, xlim=(-0.3, 5.2), ylim=(-1.1, 1.3))
    xb = 2.6
    ax.add_patch(Rectangle((xb, -1.0), 2.5, 2.2, fc='#f3eef7', ec='none'))
    ax.plot([xb, xb], [-1.0, 1.2], color=fs.GRAY, lw=0.9, ls='--')
    fs.field_grid(ax, (xb, 5.1), (-1.0, 1.2), kind='in', step=0.44, r=0.07)
    s = 1.2
    x0 = 1.9
    ax.add_patch(Rectangle((x0, -s / 2), s, s, fc='none', ec=fs.BLACK, lw=2.0, zorder=8))
    fs.arrow(ax, (0.3, 0), (1.1, 0), color=fs.VEL, lw=1.8)
    ax.text(0.7, 0.15, r'$\vec{v}$', fontsize=11, color=fs.VEL, ha='center')
    ax.annotate('', xy=(x0, s / 2 + 0.2), xytext=(x0 + s, s / 2 + 0.2), arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8))
    ax.add_patch(Rectangle((x0 + 0.1, s / 2 + 0.27), s - 0.2, 0.25, fc='white', ec='none', zorder=9))
    ax.text(x0 + s / 2, s / 2 + 0.28, '0.10 m', fontsize=8.5, color=fs.GRAY, ha='center', va='bottom', zorder=10)
    ax.text(5.1, 1.22, r'$\vec{B}$ (⊗)', fontsize=10, color=F, ha='right', va='bottom')
    fs.save(fig, __file__, 'fig28_17')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10,
              fig11, fig12, fig13, fig14, fig15, fig16, fig17]:
        f()
