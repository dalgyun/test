"""특집 B 파이썬 계산물리 입문 그림. 본문 코드를 그대로 따라 계산한다. python3 figures/spB/make_figs.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools'))
import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit, brentq


def style(a):
    a.grid(True, lw=0.4, color='#d0d0d0'); a.tick_params(labelsize=8)
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)


# ---------------------------------------------------------------- 그림 B.1 유한차분 오차
def fig01():
    f, df_exact, x0 = np.sin, np.cos(1.0), 1.0
    h = np.logspace(-13, -0.5, 400)
    fwd = np.abs((f(x0 + h) - f(x0)) / h - df_exact)
    cen = np.abs((f(x0 + h) - f(x0 - h)) / (2 * h) - df_exact)
    fig, ax = fs.plot_axes(4.4, 2.8)
    ax.loglog(h, fwd, color=fs.VEL, lw=1.0, label='전방차분')
    ax.loglog(h, cen, color=fs.FORCE, lw=1.0, label='중심차분')
    ht = np.array([1e-1, 1e-2, 1e-3, 1e-5, 1e-8, 1e-11])
    ax.loglog(ht, np.abs((f(x0 + ht) - f(x0)) / ht - df_exact), 'o', color=fs.VEL, ms=4)
    ax.loglog(ht, np.abs((f(x0 + ht) - f(x0 - ht)) / (2 * ht) - df_exact), 's', color=fs.FORCE, ms=4)
    hh = np.logspace(-6, -0.5, 10)
    ax.loglog(hh, hh / 2 * np.sin(1), '--', color=fs.VEL, lw=0.7)
    ax.loglog(hh[3:], hh[3:] ** 2 / 6 * np.cos(1), '--', color=fs.FORCE, lw=0.7)
    hr = np.logspace(-13, -6, 10)
    ax.loglog(hr, 2.2e-16 / hr, ':', color=fs.GRAY, lw=0.9)
    ax.text(3e-5, 1e-3, r'$\propto h$', color=fs.VEL, fontsize=9)
    ax.text(2e-3, 1.5e-8, r'$\propto h^2$', color=fs.FORCE, fontsize=9)
    ax.text(3e-12, 2e-3, r'반올림 $\propto \epsilon/h$', color=fs.GRAY, fontsize=8)
    ax.set_xlim(1e-13, 0.4); ax.set_ylim(1e-13, 1)
    ax.set_xlabel('간격 $h$', fontsize=9); ax.set_ylabel("수치 도함수의 오차", fontsize=9)
    ax.legend(fontsize=8, loc='lower left', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'figSB_01')


# ---------------------------------------------------------------- 그림 B.2 사다리꼴과 심프슨
def trapezoid(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x); h = (b - a) / n
    return h * (y[0] / 2 + y[1:-1].sum() + y[-1] / 2)


def simpson(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x); h = (b - a) / n
    return h / 3 * (y[0] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum() + y[-1])


def fig02():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.6), gridspec_kw={'width_ratios': [1.1, 1]})
    style(a1); style(a2)
    x = np.linspace(0, np.pi, 300)
    g = lambda t: np.sin(t) + 0.35 * np.sin(3 * t)        # 차이가 잘 보이도록 고른 예시 함수
    a1.plot(x, g(x), color=fs.BLACK, lw=1.4, label='$f(x)$')
    n = 4; xi = np.linspace(0, np.pi, n + 1)
    a1.fill_between(xi, 0, g(xi), color=fs.VEL, alpha=0.15, lw=0)
    a1.plot(xi, g(xi), '-o', color=fs.VEL, lw=1.0, ms=3.5, label='사다리꼴(직선)')
    for k in range(0, n, 2):
        xs = xi[k:k + 3]; c = np.polyfit(xs, g(xs), 2)
        xx = np.linspace(xs[0], xs[-1], 100)
        a1.plot(xx, np.polyval(c, xx), '--', color=fs.FORCE, lw=1.2, label='심프슨(포물선)' if k == 0 else None)
    a1.set_xticks(xi); a1.set_xticklabels(['$x_0$', '$x_1$', '$x_2$', '$x_3$', '$x_4$'], fontsize=8)
    a1.set_ylim(0, 1.5); a1.legend(fontsize=7, loc='upper right', frameon=False)
    a1.set_title('(가) $n = 4$ 조각의 근사', fontsize=9)
    ns = np.array([4, 8, 16, 32, 64, 128])
    eT = [abs(trapezoid(np.sin, 0, np.pi, k) - 2) for k in ns]
    eS = [abs(simpson(np.sin, 0, np.pi, k) - 2) for k in ns]
    a2.loglog(ns, eT, 'o-', color=fs.VEL, ms=4, label=r'사다리꼴 $\propto n^{-2}$')
    a2.loglog(ns, eS, 's-', color=fs.FORCE, ms=4, label=r'심프슨 $\propto n^{-4}$')
    a2.set_xlabel('조각 수 $n$', fontsize=9); a2.set_ylabel('오차', fontsize=9)
    a2.set_xticks(ns); a2.set_xticklabels([str(k) for k in ns], fontsize=8); a2.minorticks_off()
    a2.legend(fontsize=7.5, loc='lower left', frameon=False)
    a2.set_title(r'(나) $\int_0^\pi \sin x\,dx$의 오차', fontsize=9)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'figSB_02')


# ---------------------------------------------------------------- 예제 B.2 코드(궤적 기록판)
w = 2 * np.pi


def acc(x):
    return -w ** 2 * x


def run(method, dt=0.01, T=10.0, record=False):
    x, v = 1.0, 0.0
    xs, vs = [x], [v]
    for _ in range(int(round(T / dt))):
        if method == 'euler':
            x, v = x + v * dt, v + acc(x) * dt
        elif method == 'cromer':
            v = v + acc(x) * dt
            x = x + v * dt
        elif method == 'rk4':
            k1x, k1v = v, acc(x)
            k2x, k2v = v + k1v * dt / 2, acc(x + k1x * dt / 2)
            k3x, k3v = v + k2v * dt / 2, acc(x + k2x * dt / 2)
            k4x, k4v = v + k3v * dt, acc(x + k3x * dt)
            x = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
            v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if record:
            xs.append(x); vs.append(v)
    return (np.array(xs), np.array(vs)) if record else (x, v)


NAMES = {'euler': '오일러', 'cromer': '오일러–크로머', 'rk4': 'RK4'}
COLS = {'euler': fs.FORCE, 'cromer': fs.ACC, 'rk4': fs.VEL}


# ---------------------------------------------------------------- 그림 B.3 세 방법의 위상 공간과 에너지
def fig03():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.7), gridspec_kw={'width_ratios': [1, 1.25]})
    style(a1); style(a2)
    t = np.arange(1001) * 0.01
    for m in ('euler', 'cromer', 'rk4'):
        xs, vs = run(m, record=True)
        a1.plot(xs, vs / w, color=COLS[m], lw=0.6 if m == 'euler' else 1.2, label=NAMES[m])
        E = 0.5 * vs ** 2 + 0.5 * w ** 2 * xs ** 2
        a2.semilogy(t, E / E[0], color=COLS[m], lw=1.0, label=NAMES[m])
    a1.set_xlim(-8, 8); a1.set_ylim(-8, 8); a1.set_aspect('equal')
    a1.set_xlabel('$x$', fontsize=9); a1.set_ylabel(r'$v/\omega$', fontsize=9)
    a1.set_title('(가) 위상 공간 궤적(10 s)', fontsize=9)
    a1.legend(fontsize=6.5, loc='upper right', frameon=True, framealpha=0.92, edgecolor='none')
    a2.set_ylim(0.8, 80); a2.set_xlim(0, 10)
    a2.set_xlabel('$t$ (s)', fontsize=9); a2.set_ylabel(r'$E/E_0$', fontsize=9)
    a2.axhline(51.4, color=fs.FORCE, lw=0.5, ls=':')
    a2.text(0.3, 55, r'$(1 + \omega^2\Delta t^2)^{1000} \approx 51.4$', fontsize=7.5, color=fs.FORCE)
    a2.set_title(r'(나) 에너지 ($\Delta t = 0.01$ s)', fontsize=9)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'figSB_03')
    # 오일러-크로머의 진동 폭 확인용 출력(본문 '최대 약 3%')
    xs, vs = run('cromer', record=True)
    E = 0.5 * vs ** 2 + 0.5 * w ** 2 * xs ** 2
    return np.max(np.abs(E / E[0] - 1))


# ---------------------------------------------------------------- 그림 B.4 수렴 차수 (연습 B.3)
def fig04():
    dts = 0.01 / 2.0 ** np.arange(5)
    fig, ax = fs.plot_axes(4.2, 2.7)
    errs = {}
    for m in ('euler', 'cromer', 'rk4'):
        err = np.array([abs(run(m, dt, T=10.25)[0] - np.cos(2 * np.pi * 10.25)) for dt in dts])
        errs[m] = err
        ax.loglog(dts, err, 'o-', color=COLS[m], ms=4, label=NAMES[m])
    for m, k, lab, dy in (('cromer', 1, '기울기 1', 0.35), ('rk4', 4, '기울기 4', 0.2)):
        e0 = errs[m][-1]
        ax.loglog(dts, e0 * (dts / dts[-1]) ** k * dy, ':', color=fs.GRAY, lw=0.9)
        ax.text(dts[1], e0 * (dts[1] / dts[-1]) ** k * dy * 0.35, lab, fontsize=8, color=fs.GRAY, ha='center', va='top')
    ax.set_xticks(dts); ax.set_xticklabels(['0.01', '0.005', '0.0025', '0.00125', '0.000625'], fontsize=7.5)
    ax.minorticks_off()
    ax.set_xlabel(r'시간 간격 $\Delta t$ (s)', fontsize=9); ax.set_ylabel(r'$t = 10.25$ s의 위치 오차', fontsize=9)
    ax.legend(fontsize=8, loc='center left', bbox_to_anchor=(0.0, 0.42), frameon=False)
    ax.tick_params(axis='y', labelsize=8)
    fs.save(fig, __file__, 'figSB_04')
    return errs


# ---------------------------------------------------------------- 그림 B.5 큰 진폭 진자 (예제 B.3)
def fig05():
    g, L = 9.8, 1.0

    def pendulum(t, y):
        th, om = y
        return [om, -g / L * np.sin(th)]

    def cross_up(t, y):
        return y[0]
    cross_up.direction = 1
    th0 = np.radians(120)
    t = np.linspace(0, 8, 2001)
    sol = solve_ivp(pendulum, [0, 8], [th0, 0.0], t_eval=t, rtol=1e-10, atol=1e-12, events=cross_up)
    T = np.mean(np.diff(sol.t_events[0])) if len(sol.t_events[0]) > 1 else None
    T = 2.7555 if T is None else T
    fig, ax = fs.plot_axes(4.4, 2.5)
    ax.plot(t, np.degrees(sol.y[0]), color=fs.VEL, lw=1.5, label=r'수치해 ($\theta_0$ = 120°)')
    ax.plot(t, 120 * np.cos(2 * np.pi * t / T), '--', color=fs.GRAY, lw=1.0, label='같은 진폭·주기의 사인 곡선')
    T0 = 2 * np.pi * np.sqrt(L / g)
    ax.annotate('', xy=(T, -138), xytext=(0, -138), arrowprops=dict(arrowstyle='<|-|>', lw=0.8))
    ax.text(T / 2, -132, f'$T = {T:.4f}$ s', fontsize=8, ha='center', va='bottom')
    ax.set_xlim(0, 8); ax.set_ylim(-150, 175); ax.set_yticks([-120, -60, 0, 60, 120])
    ax.set_xlabel('$t$ (s)', fontsize=9); ax.set_ylabel(r'$\theta$ (도)', fontsize=9)
    ax.legend(fontsize=7.5, loc='upper center', frameon=False, ncol=2)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'figSB_05')
    return T, T0


# ---------------------------------------------------------------- 그림 B.6 몬테카를로 π
def fig06():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.4, 2.6), gridspec_kw={'width_ratios': [1, 1.3]})
    rng = np.random.default_rng(seed=42)
    N = 1000
    x, y = rng.random(N), rng.random(N)
    inside = x ** 2 + y ** 2 < 1
    a1.plot(x[inside], y[inside], '.', color=fs.VEL, ms=2.5)
    a1.plot(x[~inside], y[~inside], '.', color=fs.FORCE, ms=2.5)
    t = np.linspace(0, np.pi / 2, 100); a1.plot(np.cos(t), np.sin(t), color=fs.BLACK, lw=1.0)
    a1.set_aspect('equal'); a1.set_xlim(0, 1); a1.set_ylim(0, 1)
    a1.set_xticks([0, 1]); a1.set_yticks([0, 1]); a1.tick_params(labelsize=8)
    a1.set_title(f'(가) $N = {N}$: $\\pi \\approx {4*inside.mean():.3f}$', fontsize=9)
    style(a2)
    rng = np.random.default_rng(seed=42)
    Ns = np.unique(np.logspace(1, 7, 25).astype(int))
    err = []
    for n in Ns:
        xx, yy = rng.random(n), rng.random(n)
        err.append(abs(4 * np.mean(xx ** 2 + yy ** 2 < 1) - np.pi))
    p = np.pi / 4
    a2.loglog(Ns, err, 'o', color=fs.VEL, ms=3.5, label='실제 오차')
    a2.loglog(Ns, 4 * np.sqrt(p * (1 - p) / Ns), color=fs.FORCE, label=r'$4\sqrt{p(1-p)/N}$')
    a2.set_xlabel('점의 수 $N$', fontsize=9); a2.set_ylabel('추정값의 오차', fontsize=9)
    a2.legend(fontsize=7.5, loc='lower left', frameon=False)
    a2.set_title(r'(나) 오차 $\propto 1/\sqrt{N}$', fontsize=9)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'figSB_06')


# ---------------------------------------------------------------- 그림 B.7 무작위 행보 (본문 코드)
def fig07():
    rng = np.random.default_rng(seed=0)
    walkers, steps = 5000, 1000
    jumps = rng.choice([-1, 1], size=(walkers, steps))
    x = np.cumsum(jumps, axis=1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.6), gridspec_kw={'width_ratios': [1.3, 1]})
    style(a1); style(a2)
    n = np.arange(1, steps + 1)
    for i in range(15):
        a1.plot(n, x[i], lw=0.6, color=plt.cm.viridis(i / 15), alpha=0.85)
    a1.plot(n, np.sqrt(n), color=fs.FORCE, lw=1.4, label=r'$\pm\sqrt{n}$')
    a1.plot(n, -np.sqrt(n), color=fs.FORCE, lw=1.4)
    a1.plot(n, np.sqrt(np.mean(x ** 2, axis=0)), '--', color=fs.BLACK, lw=1.0, label=r'$x_{\mathrm{rms}}$ (5000명)')
    a1.set_xlim(0, 1000); a1.set_ylim(-95, 95)
    a1.set_xlabel('단계 수 $n$', fontsize=9); a1.set_ylabel('위치 $x$', fontsize=9)
    a1.legend(fontsize=7.5, loc='upper left', frameon=False)
    a1.set_title('(가) 보행자 15명의 경로', fontsize=9)
    a2.hist(x[:, -1], bins=np.arange(-121, 122, 6), density=True, color=fs.VEL, alpha=0.5, label='$n = 1000$')
    xx = np.linspace(-120, 120, 200)
    a2.plot(xx, np.exp(-xx ** 2 / 2000) / np.sqrt(2000 * np.pi), color=fs.FORCE, label='가우스(분산 1000)')
    a2.set_xlabel('$x$', fontsize=9); a2.set_yticks([])
    a2.legend(fontsize=7, loc='upper left', frameon=False)
    a2.set_ylim(0, 0.019)
    a2.set_title('(나) $n = 1000$의 분포', fontsize=9)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'figSB_07')


# ---------------------------------------------------------------- 그림 B.8 맞춤 (예제 B.4, B.5)
def fig08():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.6))
    style(a1); style(a2)
    rng = np.random.default_rng(seed=3)
    F = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    x = F / 25.0 + rng.normal(0, 0.002, F.size)
    b, a = np.polyfit(F, x, 1)
    a1.errorbar(F, x * 1e3, yerr=2, fmt='o', color=fs.VEL, ms=4, capsize=2, lw=0.8)
    FF = np.linspace(0, 3.2, 10)
    a1.plot(FF, (a + b * FF) * 1e3, color=fs.FORCE, label=f'맞춤: $k = 1/b = {1/b:.2f}$ N/m')
    a1.plot(FF, FF / 25 * 1e3, ':', color=fs.GRAY, label='참값 $k = 25$ N/m')
    a1.set_xlim(0, 3.2); a1.set_ylim(0, 135)
    a1.set_xlabel('$F$ (N)', fontsize=9); a1.set_ylabel('$x$ (mm)', fontsize=9)
    a1.legend(fontsize=7, loc='upper left', frameon=False)
    a1.set_title('(가) 예제 B.4: 직선 맞춤', fontsize=9)
    rng = np.random.default_rng(seed=5)
    t = np.linspace(0, 8, 17); sig = 0.05
    V = 5.0 * np.exp(-t / 2.0) + rng.normal(0, sig, t.size)
    model = lambda t, V0, tau: V0 * np.exp(-t / tau)
    p, cov = curve_fit(model, t, V, p0=[4, 1], sigma=np.full(t.size, sig), absolute_sigma=True)
    a2.errorbar(t, V, yerr=sig, fmt='o', color=fs.VEL, ms=3.5, capsize=2, lw=0.8)
    tt = np.linspace(0, 8, 200)
    a2.plot(tt, model(tt, *p), color=fs.FORCE, label=f'$V_0 = {p[0]:.3f}$ V, $\\tau = {p[1]:.3f}$ s')
    a2.plot(tt, model(tt, 5.0, 2.0), ':', color=fs.GRAY, label='참값')
    a2.set_xlim(0, 8.2); a2.set_ylim(-0.2, 5.5)
    a2.set_xlabel('$t$ (s)', fontsize=9); a2.set_ylabel('$V$ (V)', fontsize=9)
    a2.legend(fontsize=7, loc='upper right', frameon=False)
    a2.set_title('(나) 예제 B.5: curve_fit', fontsize=9)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'figSB_08')
    return 1 / b, p


# ---------------------------------------------------------------- 그림 B.9 유한 우물 근 찾기 (예제 B.6)
def fig09():
    z0 = 4.0
    g = lambda z: z * np.tan(z) - np.sqrt(z0 ** 2 - z ** 2)
    roots = []
    for n in range(int(z0 / np.pi) + 1):
        lo, hi = n * np.pi + 1e-9, min(n * np.pi + np.pi / 2 - 1e-9, z0)
        if lo < hi and g(lo) * g(hi) < 0:
            roots.append(brentq(g, lo, hi))
    fig, ax = fs.plot_axes(4.2, 2.7)
    z = np.linspace(0, z0, 2000)
    zt = z * np.tan(z)
    zt[np.abs(np.cos(z)) < 0.02] = np.nan          # tan이 발산하는 점은 끊어 그린다
    ax.plot(z, zt, color=fs.VEL, label=r'$z\tan z$')
    ax.plot(z, np.sqrt(z0 ** 2 - z ** 2), color=fs.FORCE, label=r'$\sqrt{z_0^2 - z^2}$')
    for r in roots:
        ax.plot(r, np.sqrt(z0 ** 2 - r ** 2), 'o', color=fs.BLACK, ms=5, zorder=5)
        ax.annotate(f'$z = {r:.4f}$', xy=(r, np.sqrt(z0 ** 2 - r ** 2)), xytext=(r + 0.15, np.sqrt(z0 ** 2 - r ** 2) + 1.2) if r < 2 else (r - 1.0, np.sqrt(z0 ** 2 - r ** 2) - 1.6),
                    fontsize=8, arrowprops=dict(arrowstyle='-', lw=0.5))
    ax.axvline(np.pi / 2, color=fs.GRAY, lw=0.6, ls=':'); ax.text(np.pi / 2 + 0.05, -3.5, r'$\pi/2$', fontsize=8, color=fs.GRAY)
    ax.set_xlim(0, z0); ax.set_ylim(-4, 8)
    ax.set_xlabel('$z$', fontsize=9)
    ax.legend(fontsize=8, loc='upper right', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'figSB_09')
    return roots


# ---------------------------------------------------------------- 그림 B.10 경사하강법 (본문 코드)
def fig10():
    def grad(p):
        x, y = p
        return np.array([2 * x, 20 * y])
    fig, ax = fs.plot_axes(4.4, 2.8)
    ax.grid(False)
    X, Y = np.meshgrid(np.linspace(-2.5, 2.5, 300), np.linspace(-1.6, 1.6, 300))
    ax.contour(X, Y, X ** 2 + 10 * Y ** 2, levels=[0.25, 1, 2.5, 5, 9, 14], colors='#bbbbbb', linewidths=0.6)
    for eta, c, nstep in ((0.01, fs.VEL, 100), (0.09, fs.ACC, 100), (0.11, fs.FORCE, 3)):
        p = np.array([2.0, 1.0]); path = [p]
        for _ in range(nstep):
            p = p - eta * grad(p); path.append(p)
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], '-o', color=c, ms=2.2, lw=0.9, label=f'$\\eta = {eta}$' + (' (발산)' if eta > 0.1 else ''))
    ax.plot(2, 1, 'o', color=fs.BLACK, ms=4); ax.text(2.05, 1.12, '출발 (2, 1)', fontsize=7.5)
    ax.set_xlim(-0.6, 2.6); ax.set_ylim(-1.85, 1.6); ax.set_aspect('equal')
    ax.set_xlabel('$x$', fontsize=9); ax.set_ylabel('$y$', fontsize=9)
    ax.legend(fontsize=7.5, loc='upper left', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'figSB_10')


if __name__ == '__main__':
    fig01(); fig02()
    ec = fig03(); errs = fig04()
    T, T0 = fig05()
    fig06(); fig07()
    k, p = fig08()
    roots = fig09(); fig10()
    print('RK4 오차 비:', np.round(errs['rk4'][:-1] / errs['rk4'][1:], 1), '오일러-크로머:', np.round(errs['cromer'][:-1] / errs['cromer'][1:], 2))
    print(f'검산: 오일러-크로머 에너지 최대 변화 {ec:.3f}, 진자 T = {T:.4f} s, k = {k:.2f}, '
          f'V0, tau = {p[0]:.3f}, {p[1]:.3f}, 근 = {np.round(roots, 4)}')
