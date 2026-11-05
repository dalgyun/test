"""2장 측정, 단위, 불확도 — 그림 생성 스크립트.

    python3 figures/ch02/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, Ellipse, FancyArrowPatch

S = __file__


def clean(ax, grid=True):
    if grid:
        ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# ---------- 그림 2.1 키블 저울의 두 모드 ----------
def fig01():
    fig, ax = fs.canvas(5.2, 2.9, xlim=(-0.2, 8.6), ylim=(-0.55, 4.3))

    def panel(cx, mode):
        # 영구자석(가운데 기둥)과 바깥 고리 — 단면 대신 비스듬히 본 모습
        ax.add_patch(Rectangle((cx - 0.32, 0.0), 0.64, 1.3, fc='#d5d8dc', ec=fs.BLACK, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((cx - 1.55, 0.0), 0.3, 1.3, fc='#d5d8dc', ec=fs.BLACK, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((cx + 1.25, 0.0), 0.3, 1.3, fc='#d5d8dc', ec=fs.BLACK, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((cx - 1.55, -0.25), 3.1, 0.25, fc='#d5d8dc', ec=fs.BLACK, lw=1.0, zorder=2))
        ax.text(cx, -0.42, '영구자석', fontsize=8.5, ha='center', va='center')
        # 지름 방향 자기장
        for y in (0.35, 0.95):
            for sgn in (-1, 1):
                fs.arrow(ax, (cx + sgn * 0.36, y), (cx + sgn * 1.2, y), color=fs.FIELD, lw=1.0, ms=8, zorder=3)
        ax.text(cx + 0.6, 1.1, r'$\vec{B}$', color=fs.FIELD, fontsize=10, ha='center', va='bottom')
        # 코일(틈 속의 도선 고리)
        yc = 0.65
        ax.add_patch(Ellipse((cx, yc), 1.95, 0.42, fc='none', ec=fs.ORANGE, lw=2.4, zorder=4))
        # 코일과 접시를 잇는 막대
        top = 2.75
        ax.plot([cx, cx], [yc + 0.21, top], color=fs.BLACK, lw=1.0, zorder=1)
        ax.plot([cx - 0.95, cx - 0.95, cx], [yc, 1.85, 1.85], color=fs.BLACK, lw=0.7, zorder=1)
        ax.plot([cx + 0.95, cx + 0.95, cx], [yc, 1.85, 1.85], color=fs.BLACK, lw=0.7, zorder=1)
        ax.plot([cx - 0.55, cx + 0.55], [top, top], color=fs.BLACK, lw=1.6)
        ax.text(cx - 1.62, yc + 0.02, '코일', fontsize=8.5, color=fs.ORANGE, ha='right', va='center')
        if mode == 'weigh':
            ax.add_patch(Rectangle((cx - 0.3, top), 0.6, 0.42, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=4))
            ax.text(cx, top + 0.21, '$m$', fontsize=10, ha='center', va='center', zorder=5)
            fs.arrow(ax, (cx + 0.45, top + 0.2), (cx + 0.45, top - 0.55), color=fs.FORCE, lw=1.6)
            ax.text(cx + 0.55, top - 0.35, '$mg$', color=fs.FORCE, fontsize=10, ha='left', va='center')
            fs.arrow(ax, (cx + 1.0, 1.45), (cx + 1.0, 2.2), color=fs.FORCE, lw=1.6)
            ax.text(cx + 1.1, 2.0, '$BLI$', color=fs.FORCE, fontsize=10, ha='left', va='center')
            ax.text(cx - 1.1, 1.45, '전류 $I$', fontsize=9, ha='right', va='center')
            ax.text(cx, 3.95, '(가) 무게 측정 모드', fontsize=9.5, ha='center', va='center')
            ax.text(cx, 3.55, '$mg = BLI$', fontsize=10, ha='center', va='center')
        else:
            fs.arrow(ax, (cx + 1.0, 1.45), (cx + 1.0, 2.2), color=fs.VEL, lw=1.6)
            ax.text(cx + 1.1, 2.0, r'$\vec{v}$', color=fs.VEL, fontsize=11, ha='left', va='center')
            # 전압계
            vx, vy = cx - 1.45, 2.35
            ax.add_patch(Circle((vx, vy), 0.24, fc='white', ec=fs.BLACK, lw=1.0, zorder=4))
            ax.text(vx, vy, 'V', fontsize=9, ha='center', va='center', zorder=5)
            ax.plot([vx, vx], [vy - 0.24, 1.45], color=fs.BLACK, lw=0.7)
            ax.plot([vx, cx - 1.0], [1.45, 1.45], color=fs.BLACK, lw=0.7)
            ax.text(vx + 0.32, vy + 0.05, r'$\mathcal{E}$', fontsize=10, ha='left', va='center')
            ax.text(cx, 3.95, '(나) 이동 모드', fontsize=9.5, ha='center', va='center')
            ax.text(cx, 3.55, r'$\mathcal{E} = BLv$', fontsize=10, ha='center', va='center')

    panel(2.0, 'weigh')
    panel(6.4, 'move')
    ax.plot([4.2, 4.2], [-0.4, 4.2], color=fs.GRAY, lw=0.6, ls=':')
    fs.save(fig, S, 'fig02_01')


# ---------- 그림 2.2 단진자 ----------
def fig02():
    fig, ax = fs.canvas(2.4, 2.6, xlim=(-1.4, 1.6), ylim=(-2.7, 0.35))
    fs.ceiling(ax, -0.8, 0.8, 0.0)
    th = np.radians(25); l = 2.2
    b = np.array([l * np.sin(th), -l * np.cos(th)])
    ax.plot([0, 0], [0, -l - 0.1], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([0, b[0]], [0, b[1]], color=fs.BLACK, lw=1.2)
    ax.add_patch(Circle(b, 0.14, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=5))
    ax.text(b[0] + 0.2, b[1] + 0.05, '$m$', fontsize=11, ha='left', va='center')
    fs.angle_arc(ax, (0, 0), 0.75, -90, -90 + 25, r'$\theta_0$', tr=1.0)
    ax.text(b[0] / 2 + 0.13, b[1] / 2 + 0.05, r'$\ell$', fontsize=12, ha='left', va='center')
    fs.arrow(ax, (-0.9, -1.2), (-0.9, -1.95), color=fs.ACC, lw=1.4)
    ax.text(-0.98, -1.55, r'$\vec{g}$', color=fs.ACC, fontsize=11, ha='right', va='center')
    fs.save(fig, S, 'fig02_02')


# ---------- 그림 2.3 정확도와 정밀도 ----------
def fig03():
    fig, axs = plt.subplots(1, 4, figsize=(5.4, 1.75))
    rng = np.random.default_rng(7)
    cases = [((0, 0), 0.12, '정확하고\n정밀함'), ((0.55, 0.45), 0.12, '정밀하지만\n부정확함'),
             ((0, 0), 0.42, '정확하지만\n정밀하지 않음'), ((0.45, -0.4), 0.42, '정확하지도\n정밀하지도 않음')]
    for ax, (c, sd, title) in zip(axs, cases):
        for r, fc in ((1.2, '#f2f2f2'), (0.9, '#e1e5ea'), (0.6, '#f2f2f2'), (0.3, '#e1e5ea')):
            ax.add_patch(Circle((0, 0), r, fc=fc, ec=fs.GRAY, lw=0.6))
        ax.plot([0], [0], '+', color=fs.BLACK, ms=6, mew=0.8)
        p = np.array(c) + sd * rng.standard_normal((9, 2))
        ax.plot(p[:, 0], p[:, 1], 'o', ms=3.4, color=fs.FORCE, mec='white', mew=0.4, zorder=5)
        ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(title, fontsize=8.5)
    fig.subplots_adjust(wspace=0.08, left=0.01, right=0.99, bottom=0.02, top=0.78)
    fs.save(fig, S, 'fig02_03')


# ---------- 그림 2.4 정규분포와 균일분포 ----------
def fig04():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
    x = np.linspace(-3.6, 3.6, 500)
    g = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    a1.fill_between(x, g, where=abs(x) <= 2, color=fs.VEL, alpha=0.15, lw=0)
    a1.fill_between(x, g, where=abs(x) <= 1, color=fs.VEL, alpha=0.3, lw=0)
    a1.plot(x, g, color=fs.VEL, lw=1.6)
    a1.annotate('', xy=(-1, 0.30), xytext=(1, 0.30), arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8))
    a1.text(0, 0.315, '68%', fontsize=8.5, ha='center', va='bottom')
    a1.annotate('', xy=(-2, 0.075), xytext=(2, 0.075), arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8))
    a1.text(2.1, 0.075, '95%', fontsize=8.5, ha='left', va='center')
    a1.set_xticks([-2, -1, 0, 1, 2])
    a1.set_xticklabels([r'$-2\sigma$', r'$-\sigma$', r'$\mu$', r'$+\sigma$', r'$+2\sigma$'], fontsize=8.5)
    a1.set_yticks([]); a1.set_ylim(0, 0.45); a1.set_xlim(-3.6, 3.6)
    a1.set_title('(가) 정규분포', fontsize=9)
    clean(a1, grid=False)
    # 균일분포
    a = 1.0
    a2.add_patch(Rectangle((-a, 0), 2 * a, 0.5, fc=fs.ORANGE, alpha=0.25, ec=fs.ORANGE, lw=1.4))
    a2.plot([-1.6, -a], [0, 0], color=fs.ORANGE, lw=1.4); a2.plot([a, 1.6], [0, 0], color=fs.ORANGE, lw=1.4)
    s3 = a / np.sqrt(3)
    for v in (-s3, s3):
        a2.plot([v, v], [0, 0.5], color=fs.BLACK, lw=0.9, ls='--')
    a2.annotate('', xy=(-s3, 0.3), xytext=(s3, 0.3), arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8))
    a2.text(0, 0.32, r'$\pm a/\sqrt{3}$', fontsize=8.5, ha='center', va='bottom')
    a2.set_xticks([-a, 0, a]); a2.set_xticklabels([r'$-a$', r'$x_{\mathrm{읽음}}$', r'$+a$'], fontsize=8.5)
    a2.set_xticklabels([r'$-a$', '읽은 값', r'$+a$'], fontsize=8.5)
    a2.set_yticks([]); a2.set_ylim(0, 0.72); a2.set_xlim(-1.6, 1.6)
    a2.set_title('(나) 균일분포', fontsize=9)
    clean(a2, grid=False)
    fig.tight_layout(w_pad=1.5)
    fs.save(fig, S, 'fig02_04')


# ---------- 그림 2.5 예제 2.4 반복 측정 ----------
def fig05():
    d = np.array([2.01, 2.03, 1.99, 2.02, 2.00, 2.04, 1.98, 2.01, 2.02, 2.00])
    m, s = d.mean(), d.std(ddof=1); sm = s / np.sqrt(len(d))
    fig, ax = plt.subplots(figsize=(4.4, 2.2))
    clean(ax, grid=False)
    vals, counts = np.unique(np.round(d, 2), return_counts=True)
    for v, c in zip(vals, counts):
        for k in range(c):
            ax.plot(v, 0.5 + k, 'o', ms=8, color=fs.VEL, mec='white', zorder=5)
    ax.axvspan(m - s, m + s, color=fs.ORANGE, alpha=0.15, lw=0)
    ax.axvspan(m - sm, m + sm, color=fs.FORCE, alpha=0.25, lw=0)
    ax.axvline(m, color=fs.BLACK, lw=1.2)
    ax.annotate('', xy=(m - s, 3.2), xytext=(m + s, 3.2), arrowprops=dict(arrowstyle='<->', color=fs.ORANGE, lw=1.0))
    ax.text(m + s + 0.002, 3.2, r'$\bar{T}\pm s$ (한 번 측정의 흩어짐)', fontsize=8, color=fs.ORANGE, ha='left', va='center')
    ax.annotate('', xy=(m - sm, 2.6), xytext=(m + sm, 2.6), arrowprops=dict(arrowstyle='<->', color=fs.FORCE, lw=1.0))
    ax.text(m + s + 0.002, 2.6, r'$\bar{T}\pm s_{\bar{T}}$ (평균의 불확도)', fontsize=8, color=fs.FORCE, ha='left', va='center')
    ax.text(m, 3.75, r'$\bar{T} = 2.010\ \mathrm{s}$', fontsize=8.5, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.5))
    ax.set_xlim(1.97, 2.09); ax.set_ylim(0, 4.0)
    ax.set_yticks([0, 1, 2]); ax.set_ylabel('횟수')
    ax.set_xticks([1.98, 2.00, 2.02, 2.04]); ax.set_xticklabels(['1.98', '2.00', '2.02', '2.04'])
    ax.set_xlabel('$T$ (s)')
    fs.save(fig, S, 'fig02_05')


# ---------- 그림 2.6 한 변수의 불확도 전파 ----------
def fig06():
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    clean(ax, grid=False)
    f = lambda x: 0.25 * x ** 2 + 0.3
    x = np.linspace(0.3, 4.2, 200)
    ax.plot(x, f(x), color=fs.BLACK, lw=1.6)
    x0, dx = 2.6, 0.5
    fp = 0.5 * x0
    xt = np.linspace(1.6, 3.6, 2)
    ax.plot(xt, f(x0) + fp * (xt - x0), color=fs.VEL, lw=1.1, ls='--')
    ax.axvspan(x0 - dx, x0 + dx, ymax=0.06, color=fs.ORANGE, alpha=0.5, lw=0)
    for xv in (x0 - dx, x0 + dx):
        ax.plot([xv, xv], [0, f(x0) + fp * (xv - x0)], color=fs.ORANGE, lw=0.8, ls=':')
        ax.plot([0, xv], [f(x0) + fp * (xv - x0)] * 2, color=fs.FORCE, lw=0.8, ls=':')
    ax.plot([x0, x0], [0, f(x0)], color=fs.GRAY, lw=0.7)
    ax.plot([0, x0], [f(x0), f(x0)], color=fs.GRAY, lw=0.7)
    ax.plot([x0], [f(x0)], 'o', color=fs.BLACK, ms=4)
    lo, hi = f(x0) - fp * dx, f(x0) + fp * dx
    ax.add_patch(Rectangle((0, lo), 0.1, hi - lo, fc=fs.FORCE, alpha=0.5, ec='none'))
    ax.annotate('', xy=(x0 - dx, 0.18), xytext=(x0 + dx, 0.18), arrowprops=dict(arrowstyle='<->', color=fs.ORANGE, lw=0.9))
    ax.text(x0, 0.28, r'$2\,\delta x$', color=fs.ORANGE, fontsize=9, ha='center', va='bottom')
    ax.annotate('', xy=(0.25, lo), xytext=(0.25, hi), arrowprops=dict(arrowstyle='<->', color=fs.FORCE, lw=0.9))
    ax.text(0.33, f(x0) + 0.05, r'$2\,\delta f = 2|f^{\prime}(x)|\,\delta x$', color=fs.FORCE, fontsize=9, ha='left', va='center')
    ax.text(3.45, 2.55, '접선(기울기 $f^{\\prime}$)', color=fs.VEL, fontsize=8.5, ha='left', va='center')
    ax.text(4.15, f(4.15) + 0.05, '$f(x)$', fontsize=10, ha='right', va='bottom')
    ax.set_xticks([x0]); ax.set_xticklabels(['$x$'])
    ax.set_yticks([f(x0)]); ax.set_yticklabels(['$f(x)$'])
    ax.set_xlim(0, 4.9); ax.set_ylim(0, 4.9)
    fs.save(fig, S, 'fig02_06')


# ---------- 그림 2.7 몬테카를로 불확도 전파 ----------
def fig07():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    for ax, sT, ttl, rngx in ((axs[0], 0.005, r'(가) $\sigma_T = 0.005\ \mathrm{s}$', (9.55, 10.05)),
                              (axs[1], 0.2, r'(나) $\sigma_T = 0.2\ \mathrm{s}$', (3, 22))):
        rng = np.random.default_rng(1)
        N = 1_000_000
        L = rng.normal(1.000, 0.002, N)
        T = rng.normal(2.007, sT, N)
        g = 4 * np.pi ** 2 * L / T ** 2
        g0 = 4 * np.pi ** 2 * 1.000 / 2.007 ** 2
        sg = g0 * np.sqrt((0.002 / 1.000) ** 2 + (2 * sT / 2.007) ** 2)
        ax.hist(g, bins=np.linspace(*rngx, 90), density=True, color=fs.VEL, alpha=0.45, lw=0)
        xx = np.linspace(*rngx, 400)
        ax.plot(xx, np.exp(-(xx - g0) ** 2 / (2 * sg ** 2)) / (sg * np.sqrt(2 * np.pi)), color=fs.FORCE, lw=1.4)
        ax.set_xlim(*rngx); ax.set_yticks([])
        ax.set_title(ttl, fontsize=9)
        ax.set_xlabel(r'$g$ (m/s$^2$)')
        clean(ax, grid=False)
    axs[0].text(0.03, 0.95, '몬테카를로', color=fs.VEL, fontsize=8.5, transform=axs[0].transAxes, va='top')
    axs[0].text(0.03, 0.82, '전파 공식', color=fs.FORCE, fontsize=8.5, transform=axs[0].transAxes, va='top')
    fig.tight_layout(w_pad=1.2)
    fs.save(fig, S, 'fig02_07')


# ---------- 그림 2.8 선형화: T 대 ℓ, T² 대 ℓ ----------
L_DATA = np.array([0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
T_DATA = np.array([0.899, 1.101, 1.268, 1.420, 1.553, 1.680, 1.793, 1.904, 2.009])


def fig08():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.3))
    for a in (a1, a2):
        clean(a)
    b, a0 = np.polyfit(L_DATA, T_DATA ** 2, 1)
    ll = np.linspace(0, 1.05, 200)
    a1.plot(L_DATA, T_DATA, 'o', color=fs.VEL, ms=4)
    a1.plot(ll, np.sqrt(np.clip(a0 + b * ll, 0, None)), color=fs.GRAY, lw=1.0, ls='--')
    a1.set_xlabel(r'$\ell$ (m)'); a1.set_ylabel(r'$T$ (s)')
    a1.set_xlim(0, 1.05); a1.set_ylim(0, 2.2)
    a1.set_title(r'(가) $T$ 대 $\ell$: 곡선', fontsize=9)
    a2.plot(L_DATA, T_DATA ** 2, 'o', color=fs.VEL, ms=4)
    a2.plot(ll, a0 + b * ll, color=fs.FORCE, lw=1.2)
    a2.set_xlabel(r'$\ell$ (m)'); a2.set_ylabel(r'$T^2$ (s$^2$)')
    a2.set_xlim(0, 1.05); a2.set_ylim(0, 4.5)
    a2.set_title(r'(나) $T^2$ 대 $\ell$: 직선', fontsize=9)
    a2.text(0.05, 3.9, r'기울기 $b = 4\pi^2/g$' + '\n' + rf'$= {b:.3f}\ \mathrm{{s^2/m}}$', fontsize=8.5, color=fs.FORCE, va='top')
    fig.tight_layout(w_pad=1.5)
    fs.save(fig, S, 'fig02_08')


# ---------- 그림 2.9 로그–로그 그래프 ----------
def fig09():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.4))
    x = np.linspace(0.01, 3, 300)
    xs = np.logspace(-1, 1, 100)
    ns = [(0.5, fs.ACC), (1.0, fs.GRAY), (1.5, fs.VEL), (2.0, fs.FORCE)]
    for n, c in ns:
        a1.plot(x, x ** n, color=c, lw=1.4)
        a2.loglog(xs, xs ** n, color=c, lw=1.4, label=rf'$n = {n:g}$')
    clean(a1); clean(a2)
    a1.set_xlim(0, 3); a1.set_ylim(0, 6)
    a1.set_xlabel('$x$'); a1.set_ylabel('$y$', rotation=0)
    a1.set_title(r'(가) 보통 눈금: $y = x^n$', fontsize=9)
    a2.set_xlim(0.1, 10); a2.set_ylim(0.01, 100)
    a2.set_xlabel('$x$'); a2.set_title('(나) 로그–로그 눈금', fontsize=9)
    a2.legend(fontsize=7.5, frameon=False, loc='upper left')
    a2.grid(True, which='major', lw=0.4, color='#d0d0d0')
    fig.tight_layout(w_pad=1.5)
    fs.save(fig, S, 'fig02_09')


# ---------- 그림 2.10 최소제곱법과 잔차 ----------
def fig10():
    xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    ys = np.array([1.9, 2.45, 3.6, 3.75, 4.9, 5.25])
    b, a = np.polyfit(xs, ys, 1)
    fig, ax = plt.subplots(figsize=(3.8, 2.6))
    clean(ax, grid=False)
    xx = np.linspace(0, 7, 2)
    ax.plot(xx, a + b * xx, color=fs.FORCE, lw=1.3)
    for xi, yi in zip(xs, ys):
        ax.plot([xi, xi], [yi, a + b * xi], color=fs.ORANGE, lw=1.6)
    ax.plot(xs, ys, 'o', color=fs.VEL, ms=5, zorder=5)
    xm, ym = xs.mean(), ys.mean()
    ax.plot([xm], [ym], 's', color=fs.BLACK, ms=5, zorder=6)
    ax.annotate(r'$(\bar{x}, \bar{y})$', xy=(xm, ym), xytext=(xm - 1.3, ym + 1.0), fontsize=9,
                arrowprops=dict(arrowstyle='-', lw=0.6, color=fs.BLACK), ha='center')
    i = 2
    ax.annotate('잔차\n' + r'$y_i - (a + bx_i)$', xy=(xs[i], (ys[i] + a + b * xs[i]) / 2), xytext=(xs[i] + 1.2, ys[i] - 1.2),
                fontsize=8.5, color=fs.ORANGE, ha='left', va='center', arrowprops=dict(arrowstyle='-', lw=0.6, color=fs.ORANGE))
    ax.text(6.9, a + b * 6.9 + 0.12, '$y = a + bx$', color=fs.FORCE, fontsize=10, ha='right', va='bottom')
    ax.set_xlim(0, 7); ax.set_ylim(0, 6.3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$x$'); ax.set_ylabel('$y$', rotation=0)
    fs.save(fig, S, 'fig02_10')


# ---------- 그림 2.11 잔차 그래프 ----------
def fig11():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 1.9), sharey=True)
    x = np.linspace(1, 10, 12)
    rng = np.random.default_rng(3)
    r1 = rng.normal(0, 1, len(x))
    r2 = -0.32 * (x - 5.5) ** 2 + 2.2 + rng.normal(0, 0.25, len(x))
    for ax, r, t in ((axs[0], r1, '(가) 무작위로 흩어짐: 좋은 맞춤'), (axs[1], r2, '(나) 체계적인 곡선: 모형이 틀림')):
        clean(ax, grid=False)
        ax.axhline(0, color=fs.GRAY, lw=0.8)
        ax.errorbar(x, r, yerr=1.0, fmt='o', ms=3.5, color=fs.VEL, elinewidth=0.8, capsize=2)
        ax.set_title(t, fontsize=8.5)
        ax.set_xticks([]); ax.set_xlabel('$x$')
    axs[0].set_ylabel('잔차')
    axs[0].set_yticks([0])
    fig.tight_layout(w_pad=1.2)
    fs.save(fig, S, 'fig02_11')


# ---------- 그림 2.12 예제 2.7 용수철 상수 ----------
def fig12():
    x = np.array([0.0196, 0.0405, 0.0590, 0.0801])
    F = np.array([0.490, 0.980, 1.470, 1.960])
    N = len(x); D = N * np.sum(x ** 2) - np.sum(x) ** 2
    k = (N * np.sum(x * F) - np.sum(x) * np.sum(F)) / D
    a = (np.sum(x ** 2) * np.sum(F) - np.sum(x) * np.sum(x * F)) / D
    r = F - a - k * x
    s = np.sqrt(np.sum(r ** 2) / (N - 2))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(3.8, 3.3), sharex=True, gridspec_kw=dict(height_ratios=[2.2, 1]))
    clean(a1); clean(a2)
    xx = np.linspace(0, 0.09, 2)
    a1.plot(xx, a + k * xx, color=fs.FORCE, lw=1.2)
    a1.plot(x, F, 'o', color=fs.VEL, ms=5, zorder=5)
    a1.set_ylabel('$F$ (N)'); a1.set_ylim(0, 2.3)
    a1.text(0.003, 2.05, rf'$k = {k:.1f}\ \mathrm{{N/m}}$, $a = {a:.3f}\ \mathrm{{N}}$', color=fs.FORCE, fontsize=9, va='center')
    a2.axhline(0, color=fs.GRAY, lw=0.8)
    a2.axhspan(-s, s, color=fs.ORANGE, alpha=0.15, lw=0)
    a2.plot(x, r, 'o', color=fs.VEL, ms=5)
    a2.text(0.086, s, r'$\pm s$', fontsize=8.5, color=fs.ORANGE, ha='right', va='bottom')
    a2.set_ylabel('잔차 (N)'); a2.set_ylim(-0.04, 0.04)
    a2.set_xlabel('$x$ (m)'); a2.set_xlim(0, 0.09)
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, S, 'fig02_12')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12):
        f()
