"""3장 직선 운동 그림. 실행: python3 figures/ch03/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt

g = 9.8


def style(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def numline(ax, x0, x1, y, ticks=(), origin=0.0, show_o=True):
    fs.arrow(ax, (x0, y), (x1, y), lw=1.1, ms=10)
    ax.text(x1 + 0.1, y, r'$x$', va='center', fontsize=11)
    for t in ticks:
        ax.plot([t, t], [y - 0.07, y + 0.07], color=fs.BLACK, lw=0.8)
    ax.plot([origin, origin], [y - 0.13, y + 0.13], color=fs.BLACK, lw=1.3)
    if show_o:
        ax.text(origin, y - 0.3, 'O', ha='center', fontsize=10)


# ---------- 그림 3.1 위치와 변위 ----------
def fig01():
    fig, ax = fs.canvas(4.6, 1.9, xlim=(-2.6, 8.6), ylim=(-0.6, 3.4))
    for y, (xa, xb) in ((2.2, (1.5, 6.0)), (0.5, (5.0, 2.0))):
        numline(ax, -2.4, 8.2, y, ticks=range(-2, 9))
        col = fs.BLACK
        fs.dot(ax, (xa, y), r=0.11, color=fs.GRAY)
        fs.dot(ax, (xb, y), r=0.11, color=fs.BLACK)
        ax.text(xa, y - 0.32, r'$x_1$', ha='center', fontsize=10)
        ax.text(xb, y - 0.32, r'$x_2$', ha='center', fontsize=10)
        fs.arrow(ax, (xa, y + 0.38), (xb, y + 0.38), color=col, lw=1.5)
        sign = '> 0' if xb > xa else '< 0'
        ax.text((xa + xb) / 2, y + 0.68, r'$\Delta x = x_2 - x_1 %s$' % sign, ha='center', fontsize=10)
    ax.text(-2.5, 2.95, '(가)', fontsize=9); ax.text(-2.5, 1.25, '(나)', fontsize=9)
    fs.save(fig, __file__, 'fig03_01')


# ---------- 그림 3.2 할선과 접선 ----------
def fig02():
    fig, ax = fs.plot_axes(4.0, 2.9)
    t = np.linspace(0, 3.0, 300)
    ax.plot(t, t ** 2, color=fs.BLACK, lw=1.6)
    t0 = 1.0
    for dt, al in ((1.5, 0.35), (0.8, 0.6), (0.3, 0.9)):
        t1 = t0 + dt
        s = (t1 ** 2 - t0 ** 2) / dt
        tt = np.array([0.3, 3.0])
        ax.plot(tt, t0 ** 2 + s * (tt - t0), color=fs.ORANGE, lw=1.0, alpha=al)
        ax.plot(t1, t1 ** 2, 'o', color=fs.ORANGE, ms=4, alpha=al)
    # 가장 큰 할선의 Δt, Δx
    t1 = 2.5
    ax.plot([t0, t1], [t0 ** 2, t0 ** 2], color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([t1, t1], [t0 ** 2, t1 ** 2], color=fs.GRAY, lw=0.8, ls='--')
    ax.text((t0 + t1) / 2, 0.55, r'$\Delta t$', ha='center', fontsize=10, color=fs.GRAY)
    ax.text(t1 + 0.07, 3.5, r'$\Delta x$', fontsize=10, color=fs.GRAY)
    tt = np.array([0.25, 2.6])
    ax.plot(tt, 1 + 2 * (tt - 1), color=fs.VEL, lw=1.6)
    ax.plot(t0, 1, 'o', color=fs.BLACK, ms=5, zorder=5)
    ax.text(0.95, 1.5, 'P', fontsize=10)
    ax.text(2.62, 4.2, '접선: 기울기 $= v$', color=fs.VEL, fontsize=9, ha='left')
    ax.text(1.65, 7.1, '할선: 기울기 $= v_{\\mathrm{avg}}$', color=fs.ORANGE, fontsize=9)
    ax.annotate('', xy=(2.15, 5.5), xytext=(1.85, 6.85),
                arrowprops=dict(arrowstyle='->', color=fs.ORANGE, lw=0.8))
    ax.set_xlim(0, 3.6); ax.set_ylim(-0.3, 9)
    ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$x$')
    ax.set_xticks([1, 2, 3]); ax.set_yticks([0, 3, 6, 9])
    fs.save(fig, __file__, 'fig03_02')


# ---------- 그림 3.3 예제 3.2의 x-t, v-t ----------
def fig03():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.2, 3.4), sharex=True)
    t = np.linspace(0, 3, 300)
    x = 2 * t ** 3 - 9 * t ** 2 + 12 * t
    v = 6 * t ** 2 - 18 * t + 12
    for ax in (a1, a2):
        style(ax)
        for tc in (1, 2):
            ax.axvline(tc, color=fs.GRAY, lw=0.8, ls='--')
    a1.plot(t, x, color=fs.BLACK)
    for tc, xc in ((0, 0), (1, 5), (2, 4), (3, 9)):
        a1.plot(tc, xc, 'o', color=fs.BLACK, ms=4)
        a1.text(tc + (0.07 if tc < 3 else -0.07), xc + 0.6, f'{xc:g} m', fontsize=8,
                ha='left' if tc < 3 else 'right')
    a1.set_ylabel(r'$x$ (m)'); a1.set_ylim(-0.5, 10.5)
    a2.plot(t, v, color=fs.VEL)
    a2.axhline(0, color=fs.BLACK, lw=0.8)
    a2.fill_between(t, v, 0, where=v < 0, color=fs.VEL, alpha=0.15)
    a2.text(1.5, 1.6, '$v<0$\n(되돌아감)', ha='center', fontsize=8, color=fs.VEL)
    a2.set_ylabel(r'$v$ (m/s)'); a2.set_xlabel(r'$t$ (s)')
    a2.set_xticks([0, 1, 2, 3]); a2.set_ylim(-3, 14)
    fig.align_ylabels()
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, __file__, 'fig03_03')


# ---------- 그림 3.4 예제 3.2의 경로 ----------
def fig04():
    fig, ax = fs.canvas(4.6, 1.6, xlim=(-0.8, 10.6), ylim=(-0.75, 2.3))
    numline(ax, -0.6, 10.2, 0, ticks=range(0, 10), show_o=False)
    for k in (0, 5, 4, 9):
        ax.text(k, -0.55, str(k), ha='center', fontsize=8)
    segs = [((0, 5), 1.8, r'$0\to1$ s: $+5.0$ m'), ((5, 4), 1.15, r'$1\to2$ s: $-1.0$ m'),
            ((4, 9), 0.5, r'$2\to3$ s: $+5.0$ m')]
    for (a, b), y, s in segs:
        fs.arrow(ax, (a, y), (b, y), color=fs.VEL, lw=1.5)
        ax.plot([a, a], [0, y], color=fs.GRAY, lw=0.5, ls=':')
        if b > a:
            ax.text(b + 0.2, y, s, va='center', fontsize=8.5, color=fs.VEL)
        else:
            ax.text(b - 0.2, y, s, va='center', ha='right', fontsize=8.5, color=fs.VEL)
    ax.plot([9, 9], [0, 0.5], color=fs.GRAY, lw=0.5, ls=':')
    fs.save(fig, __file__, 'fig03_04')


# ---------- 그림 3.5 v와 a의 부호와 속력 변화 ----------
def fig05():
    fig, ax = fs.canvas(4.8, 2.4, xlim=(0, 9.6), ylim=(-0.6, 4.4))
    cases = [((0.2, 2.6), +1, +1, '속력 증가'), ((5.0, 2.6), +1, -1, '속력 감소'),
             ((0.2, 0.2), -1, -1, '속력 증가'), ((5.0, 0.2), -1, +1, '속력 감소')]
    for (x0, y0), sv, sa, txt in cases:
        cx = x0 + 2.2
        fs.ground(ax, x0, x0 + 4.4, y0, depth=0.12)
        fs.block(ax, (cx, y0 + 0.3), 0.7, 0.6)
        fs.vec(ax, (cx + sv * 0.38, y0 + 0.45), (sv * 1.2, 0), color=fs.VEL, lw=1.7)
        ax.text(cx + sv * 1.75, y0 + 0.62, r'$\vec v$', color=fs.VEL, fontsize=10, ha='center')
        fs.vec(ax, (cx, y0 + 1.0), (sa * 1.0, 0), color=fs.ACC, lw=1.7)
        ax.text(cx + sa * 1.3, y0 + 1.15, r'$\vec a$', color=fs.ACC, fontsize=10, ha='center')
        sgn = lambda s: '+' if s > 0 else '-'
        ax.text(cx, y0 + 1.6, f'$v{sgn(sv)}$, $a{sgn(sa)}$: {txt}', ha='center', fontsize=9,
                fontweight='bold' if '증가' in txt else 'normal')
    fs.arrow(ax, (4.3, -0.4), (5.3, -0.4), lw=1.0, ms=8)
    ax.text(5.4, -0.4, r'$+x$ 방향', fontsize=8, va='center')
    fs.save(fig, __file__, 'fig03_05')


# ---------- 그림 3.6 등가속도 v-t 그래프의 넓이 ----------
def fig06():
    fig, ax = fs.plot_axes(3.8, 2.7)
    v0, a, T = 2.0, 1.0, 4.0
    t = np.linspace(0, T, 50)
    ax.plot([0, 5], [v0, v0 + 5 * a], color=fs.VEL, lw=1.6)
    ax.fill_between([0, T], [0, 0], [v0, v0], color=fs.VEL, alpha=0.18, lw=0)
    ax.fill_between(t, v0, v0 + a * t, color=fs.ACC, alpha=0.22, lw=0)
    ax.plot([T, T], [0, v0 + a * T], color=fs.GRAY, lw=0.8, ls='--')
    ax.text(T / 2, v0 / 2, r'$v_0t$', ha='center', va='center', fontsize=11)
    ax.text(T * 0.66, v0 + 1.0, r'$\frac{1}{2}at^2$', ha='center', va='center', fontsize=11)
    ax.plot([T, T], [v0, v0 + a * T], color=fs.ACC, lw=0)
    ax.annotate('', xy=(T + 0.12, v0 + a * T), xytext=(T + 0.12, v0),
                arrowprops=dict(arrowstyle='<->', color=fs.ACC, lw=0.9))
    ax.text(T + 0.2, v0 + a * T / 2, r'$at$', color=fs.ACC, fontsize=10, va='center')
    ax.text(2.0, 4.9, '기울기 $= a$', color=fs.VEL, fontsize=9, ha='right')
    ax.set_xticks([0, T]); ax.set_xticklabels(['0', r'$t$'])
    ax.set_yticks([0, v0, v0 + a * T]); ax.set_yticklabels(['0', r'$v_0$', r'$v$'])
    ax.set_xlim(0, 5); ax.set_ylim(0, 7.2)
    ax.set_xlabel('시간'); ax.set_ylabel('속도')
    fs.save(fig, __file__, 'fig03_06')


# ---------- 그림 3.7 예제 3.3 정지거리 ----------
def fig07():
    fig, ax = fs.plot_axes(4.2, 2.7)
    for v0, col, lab in ((100 / 3.6, fs.VEL, '100 km/h'), (50 / 3.6, fs.ORANGE, '50 km/h')):
        tb = v0 / 7.0
        ts = [0, 1.0, 1.0 + tb]
        vs = [v0, v0, 0]
        ax.plot(ts, vs, color=col, lw=1.6, label=lab)
        ax.fill_between([0, 1.0], [v0, v0], color=col, alpha=0.15, lw=0)
        ax.fill_between([1.0, 1.0 + tb], [v0, 0], color=col, alpha=0.30, lw=0)
    ax.axvline(1.0, color=fs.GRAY, lw=0.8, ls='--')
    ax.text(0.5, 21, '반응\n27.8 m', ha='center', fontsize=8, color=fs.VEL)
    ax.text(0.5, 6, '13.9 m', ha='center', fontsize=8, color='#a0521a')
    ax.text(3.3, 7.5, '제동\n55.1 m', ha='center', fontsize=8, color=fs.VEL)
    ax.text(1.55, 4.0, '13.8 m', ha='center', fontsize=8, color='#a0521a')
    ax.legend(fontsize=8, loc='upper right', frameon=False)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    ax.set_xlim(0, 5.5); ax.set_ylim(0, 31)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    fs.save(fig, __file__, 'fig03_07')


# ---------- 그림 3.8 예제 3.4 y-t ----------
def fig08():
    fig, ax = fs.plot_axes(4.2, 2.8)
    y = lambda t: 30 + 15 * t - 4.9 * t ** 2
    tf = (15 + np.sqrt(225 + 4 * 4.9 * 30)) / 9.8
    tn = (15 - np.sqrt(225 + 4 * 4.9 * 30)) / 9.8
    t = np.linspace(0, tf, 200)
    ax.plot(t, y(t), color=fs.BLACK, lw=1.6)
    t2 = np.linspace(tn, 0, 60)
    ax.plot(t2, y(t2), color=fs.GRAY, lw=1.0, ls='--')
    ax.axhline(0, color=fs.BLACK, lw=0.8)
    tm = 15 / 9.8
    ax.plot([tm], [y(tm)], 'o', color=fs.BLACK, ms=4)
    ax.text(tm, y(tm) + 2.2, r'최고점 $(1.53\ \mathrm{s},\ 41.5\ \mathrm{m})$', ha='center', fontsize=8)
    ax.plot([0], [30], 'o', color=fs.BLACK, ms=4)
    ax.text(0.1, 26.5, '던진 점 (옥상, 30.0 m)', fontsize=8)
    ax.plot([tf], [0], 'o', color=fs.BLACK, ms=4)
    ax.text(tf, -2.0, r'$4.44\ \mathrm{s}$', ha='center', va='top', fontsize=8)
    ax.plot([tn], [0], 'o', color=fs.GRAY, ms=4)
    ax.text(tn, -2.0, r'$-1.38\ \mathrm{s}$', ha='center', va='top', fontsize=8, color=fs.GRAY)
    ax.annotate('땅에 닿을 때 기울기\n$v = -28.5$ m/s', xy=(4.3, 4.5), xytext=(2.75, 9), fontsize=8,
                color=fs.VEL, ha='center', arrowprops=dict(arrowstyle='->', color=fs.VEL, lw=0.8))
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$y$ (m)')
    ax.set_xlim(-1.8, 5.0); ax.set_ylim(-9, 48)
    fs.save(fig, __file__, 'fig03_08')


# ---------- 그림 3.9 예제 3.5 모터보트 ----------
def fig09():
    fig, axs = plt.subplots(1, 3, figsize=(5.6, 1.95))
    v0, k = 10.0, 0.5
    t = np.linspace(0, 10, 300)
    v = v0 * np.exp(-k * t); x = v0 / k * (1 - np.exp(-k * t))
    t1 = np.log(10) / k
    for ax in axs:
        style(ax)
    a1, a2, a3 = axs
    a1.plot(t, v, color=fs.VEL)
    a1.plot(t1, 1.0, 'o', color=fs.VEL, ms=3.5)
    a1.text(t1 + 0.4, 1.8, '(4.6 s, 1.0 m/s)', fontsize=7.5)
    a1.set_xlabel(r'$t$ (s)'); a1.set_ylabel(r'$v$ (m/s)'); a1.set_ylim(0, 10.5)
    a2.plot(t, x, color=fs.BLACK)
    a2.axhline(v0 / k, color=fs.GRAY, ls='--', lw=0.9)
    a2.text(9.8, 13, r'$v_0/k = 20$ m', ha='right', fontsize=7.5, color=fs.GRAY)
    a2.plot(t1, 18, 'o', color=fs.BLACK, ms=3.5)
    a2.set_xlabel(r'$t$ (s)'); a2.set_ylabel(r'$x$ (m)'); a2.set_ylim(0, 23)
    xx = np.linspace(0, 20, 50)
    a3.plot(xx, v0 - k * xx, color=fs.VEL)
    a3.text(10.5, 6.5, r'$v = v_0 - kx$', fontsize=8, color=fs.VEL)
    a3.set_xlabel(r'$x$ (m)'); a3.set_ylabel(r'$v$ (m/s)'); a3.set_ylim(0, 10.5); a3.set_xlim(0, 21)
    for ax, s in zip(axs, ('(가)', '(나)', '(다)')):
        ax.set_title(s, fontsize=8, loc='left')
        ax.tick_params(labelsize=8)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'fig03_09')


# ---------- 그림 3.10 예제 3.6 위상 공간 ----------
def fig10():
    fig, ax = fs.canvas(3.0, 2.7, xlim=(-1.6, 1.75), ylim=(-1.45, 1.55))
    fs.arrow(ax, (-1.45, 0), (1.5, 0), lw=0.9, ms=9)
    fs.arrow(ax, (0, -1.35), (0, 1.4), lw=0.9, ms=9)
    ax.text(1.55, -0.13, r'$x/A$', fontsize=10)
    ax.text(0.07, 1.42, r'$v/\omega A$', fontsize=10)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(th), np.sin(th), color=fs.VEL, lw=1.6)
    # 시계 방향 진행: (1,0)에서 출발해 v<0
    for th0 in (-np.pi / 4, -3 * np.pi / 4, 3 * np.pi / 4, np.pi / 4):
        p = np.array([np.cos(th0), np.sin(th0)]); d = np.array([np.sin(th0), -np.cos(th0)])
        fs.arrow(ax, p - 0.04 * d, p + 0.06 * d, color=fs.VEL, ms=11, lw=0)
    fs.dot(ax, (1, 0), r=0.05)
    ax.text(1.05, 0.12, '출발\n$(A, 0)$', fontsize=8, va='bottom')
    fs.dot(ax, (0, -1), r=0.05)
    ax.text(0.1, -1.17, r'$|v| = \omega A$', fontsize=8.5)
    ax.text(1.07, -0.08, '1', fontsize=8, ha='left', va='top')
    ax.text(-1.07, -0.08, '−1', fontsize=8, ha='right', va='top')
    fs.save(fig, __file__, 'fig03_10')


# ---------- 그림 3.11 x-t 그래프의 오목·볼록 ----------
def fig11():
    fig, axs = plt.subplots(1, 2, figsize=(4.6, 2.0))
    t = np.linspace(0, 2, 200)
    curves = [(lambda t: 0.5 * t ** 2 + 0.2, lambda t: t, r'$a > 0$ (위로 오목, $\cup$)'),
              (lambda t: 2.2 - 0.5 * (2 - t) ** 2, lambda t: (2 - t), r'$a < 0$ (위로 볼록, $\cap$)')]
    for ax, (f, df, title) in zip(axs, curves):
        ax.plot(t, f(t), color=fs.BLACK, lw=1.5)
        for t0 in (0.4, 1.0, 1.6):
            tt = np.array([t0 - 0.3, t0 + 0.3])
            ax.plot(tt, f(t0) + df(t0) * (tt - t0), color=fs.VEL, lw=1.3)
            ax.plot(t0, f(t0), 'o', color=fs.VEL, ms=3)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel(r'$t$', labelpad=1); ax.set_ylabel(r'$x$', labelpad=1)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
        ax.set_xlim(0, 2.1); ax.set_ylim(0, 2.4)
    axs[0].text(1.0, 2.0, '기울기 증가', fontsize=8, color=fs.VEL, ha='center')
    axs[1].text(1.15, 0.45, '기울기 감소', fontsize=8, color=fs.VEL, ha='center')
    fig.tight_layout(w_pad=1.5)
    fs.save(fig, __file__, 'fig03_11')


# ---------- 예제 3.7 데이터 ----------
T37 = np.array([0, 4, 10, 13, 14])
V37 = np.array([0, 12, 12, 0, -4])


def v37(t):
    return np.interp(t, [0, 4, 10, 14], [0, 12, 12, -4])


def fig12():
    fig, ax = fs.plot_axes(4.4, 2.7)
    t = np.linspace(0, 14, 600)
    v = v37(t)
    ax.plot(t, v, color=fs.VEL, lw=1.7)
    ax.axhline(0, color=fs.BLACK, lw=0.9)
    ax.fill_between(t, v, 0, where=v >= 0, color=fs.VEL, alpha=0.18, lw=0, interpolate=True)
    ax.fill_between(t, v, 0, where=v < 0, color=fs.FORCE, alpha=0.25, lw=0, interpolate=True)
    for tc in (4, 10, 13):
        ax.plot([tc, tc], [0, v37(tc)], color=fs.GRAY, lw=0.7, ls='--')
    for x, y, s in ((2.7, 4.0, '24 m'), (7, 6, '72 m'), (11.2, 4.0, '18 m')):
        ax.text(x, y, s, ha='center', fontsize=9)
    ax.annotate('$-2.0$ m', xy=(13.6, -1.0), xytext=(11.4, -3.6), fontsize=9, color=fs.FORCE,
                arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.8))
    ax.set_xticks([0, 4, 10, 13, 14]); ax.set_yticks([-4, 0, 4, 8, 12])
    ax.set_xlim(0, 14.6); ax.set_ylim(-5.5, 14)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    fs.save(fig, __file__, 'fig03_12')


def fig13():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.2))
    for ax in (a1, a2):
        style(ax)
    ta = [0, 4, 4, 10, 10, 14]; aa = [3, 3, 0, 0, -4, -4]
    a1.plot(ta, aa, color=fs.ACC, lw=1.6)
    a1.axhline(0, color=fs.BLACK, lw=0.8)
    a1.set_xlabel(r'$t$ (s)'); a1.set_ylabel(r'$a$ (m/s$^2$)')
    a1.set_xticks([0, 4, 10, 14]); a1.set_ylim(-5, 4.5); a1.set_yticks([-4, 0, 3])
    t = np.linspace(0, 14, 1401)
    v = v37(t)
    x = np.concatenate([[0], np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(t))])
    a2.plot(t, x, color=fs.BLACK, lw=1.6)
    a2.plot(13, x[1300], 'o', color=fs.BLACK, ms=3.5)
    a2.text(12.8, x[1300] + 6, '114 m\n($t$ = 13 s)', ha='right', fontsize=8, va='bottom')
    a2.plot(14, x[-1], 'o', color=fs.GRAY, ms=3.5)
    a2.text(13.6, x[-1] - 22, '112 m', ha='center', fontsize=8, color=fs.GRAY)
    a2.set_xlabel(r'$t$ (s)'); a2.set_ylabel(r'$x$ (m)')
    a2.set_xticks([0, 4, 10, 14]); a2.set_ylim(0, 140)
    a1.set_title('(가)', fontsize=8, loc='left'); a2.set_title('(나)', fontsize=8, loc='left')
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig03_13')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
        f()
