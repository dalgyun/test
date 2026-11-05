"""17장 소리 그림. 실행: python3 figures/ch17/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch

F = __file__


def dline(ax, p, q, color=fs.GRAY, lw=0.8, ls='--', zorder=1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=zorder)


def darrow(ax, p, q, text=None, color=fs.BLACK, off=(0, 0.12), fontsize=10, ms=8, lw=0.8, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=ms, color=color, lw=lw, zorder=5))
    if text:
        m = ((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1])
        ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color, **kw)


def clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


# ---------------------------------------------------------------- 17.1 변위파와 압력파
def fig01():
    fig, axs = plt.subplots(3, 1, figsize=(4.8, 3.5), sharex=True, gridspec_kw=dict(height_ratios=[1.0, 1, 1]))
    lam = 1.0
    k = 2 * np.pi / lam
    X = 2 * lam
    ax = axs[0]
    xe = np.arange(0.0, X + 1e-9, 0.03125)
    for xi in xe:
        si = 0.06 * np.cos(k * xi)
        ax.plot([xi + si, xi + si], [0, 1], color=fs.BLACK, lw=0.8)
    for xc, lab in ((0.25, '압축'), (0.75, '희박'), (1.25, '압축'), (1.75, '희박')):
        ax.text(xc, 1.08, lab, ha='center', va='bottom', fontsize=8, color=fs.FORCE if lab == '압축' else fs.VEL)
    ax.set_ylim(0, 1.45); ax.set_yticks([])
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    x = np.linspace(0, X, 600)
    axs[1].plot(x, np.cos(k * x), color=fs.BLACK, lw=1.5)
    axs[1].set_ylabel('$s$', fontsize=10, rotation=0, labelpad=8)
    axs[1].set_yticks([-1, 0, 1]); axs[1].set_yticklabels(['$-s_m$', '0', '$s_m$'])
    axs[2].plot(x, np.sin(k * x), color=fs.FORCE, lw=1.5)
    axs[2].set_ylabel(r'$\Delta p$', fontsize=10, rotation=0, labelpad=8)
    axs[2].set_yticks([-1, 0, 1]); axs[2].set_yticklabels([r'$-\Delta p_m$', '0', r'$\Delta p_m$'])
    for ax in axs[1:]:
        ax.axhline(0, color=fs.GRAY, lw=0.5); ax.set_ylim(-1.3, 1.3); clean(ax)
        ax.grid(True, axis='x', lw=0.4, color='#d0d0d0')
    for ax in axs:
        for xc in (0.25, 1.25):
            ax.axvline(xc, color=fs.FORCE, lw=0.7, ls=':')
        for xc in (0.75, 1.75):
            ax.axvline(xc, color=fs.VEL, lw=0.7, ls=':')
    axs[2].set_xticks([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])
    axs[2].set_xticklabels(['0', '', r'$\lambda/2$', '', r'$\lambda$', '', r'$3\lambda/2$', '', r'$2\lambda$'])
    axs[2].set_xlabel('$x$ (한 순간, $t=0$)', fontsize=9)
    axs[2].set_xlim(0, X)
    fig.align_ylabels(axs)
    fig.tight_layout(h_pad=0.3)
    fs.save(fig, F, 'fig17_01')


# ---------------------------------------------------------------- 17.1 공기층에 작용하는 힘
def fig02():
    fig, ax = fs.canvas(4.6, 2.4, xlim=(-0.3, 7.6), ylim=(-1.05, 2.75))
    # 관
    ax.plot([0, 7.2], [0, 0], color=fs.BLACK, lw=1.1); ax.plot([0, 7.2], [1.8, 1.8], color=fs.BLACK, lw=1.1)
    # 평형 위치의 층
    xa, xb = 2.4, 4.2
    ax.add_patch(Rectangle((xa, 0), xb - xa, 1.8, fc='none', ec=fs.GRAY, lw=0.9, ls='--', zorder=4))
    # 움직인 층
    sa, sb = 0.55, 0.85
    ax.add_patch(Rectangle((xa + sa, 0), xb - xa + sb - sa, 1.8, fc='#dbe7f3', ec=fs.BLACK, lw=1.2))
    ax.text(xa - 0.08, -0.12, '$x$', ha='center', va='top', fontsize=10)
    ax.text(xb, -0.12, r'$x+\Delta x$', ha='center', va='top', fontsize=10)
    fs.arrow(ax, (xa, 2.0), (xa + sa, 2.0), color=fs.BLACK, lw=1.0, ms=7)
    ax.text(xa + sa / 2, 2.12, '$s(x)$', ha='center', va='bottom', fontsize=9)
    fs.arrow(ax, (xb, 2.0), (xb + sb, 2.0), color=fs.BLACK, lw=1.0, ms=7)
    ax.text(xb + sb / 2 + 0.1, 2.12, r'$s(x+\Delta x)$', ha='center', va='bottom', fontsize=9)
    fs.arrow(ax, (xa + sa - 1.3, 0.9), (xa + sa, 0.9), color=fs.FORCE, lw=1.6)
    ax.text(xa + sa - 1.35, 1.2, r'$[p_0+\Delta p(x)]A$', color=fs.FORCE, fontsize=8.5, ha='center')
    fs.arrow(ax, (xb + sb + 1.3, 0.9), (xb + sb, 0.9), color=fs.FORCE, lw=1.6)
    ax.text(xb + sb + 1.25, 1.2, r'$[p_0+\Delta p(x+\Delta x)]A$', color=fs.FORCE, fontsize=8.5, ha='center')
    ax.text(3.75, 0.5, '질량\n' + r'$\rho A\Delta x$', ha='center', va='center', fontsize=8.5)
    ax.text(0.1, -0.85, '단면적 $A$인 관 속의 공기층 (점선: 평형 위치)', fontsize=8, color=fs.GRAY)
    fs.save(fig, F, 'fig17_02')


# ---------------------------------------------------------------- 17.2 점 음원
def fig03():
    fig, ax = fs.canvas(3.6, 2.6, xlim=(-0.4, 4.6), ylim=(-1.7, 1.9))
    S = (0, 0)
    for r, lab in ((1.2, '$r$'), (2.4, '$2r$')):
        t = np.linspace(-0.62, 0.62, 100)
        ax.plot(r * np.cos(t), r * np.sin(t), color=fs.VEL, lw=1.3)
    for a in np.linspace(-0.55, 0.55, 7):
        ax.plot([0.15 * np.cos(a), 3.5 * np.cos(a)], [0.15 * np.sin(a), 3.5 * np.sin(a)], color=fs.GRAY, lw=0.5, ls=':')
    # 같은 원뿔이 자르는 넓이
    a0 = 0.18
    for r, c in ((1.2, fs.ORANGE), (2.4, fs.ORANGE)):
        t = np.linspace(-a0, a0, 40)
        ax.plot(r * np.cos(t), r * np.sin(t), color=c, lw=4.5, alpha=0.7, solid_capstyle='butt')
    ax.plot([0, 3.0 * np.cos(a0)], [0, 3.0 * np.sin(a0)], color=fs.ORANGE, lw=0.7)
    ax.plot([0, 3.0 * np.cos(a0)], [0, -3.0 * np.sin(a0)], color=fs.ORANGE, lw=0.7)
    ax.add_patch(Circle(S, 0.12, fc=fs.FORCE, ec='none', zorder=6))
    ax.text(-0.15, 0.25, r'$P_s$', fontsize=10, ha='center')
    ax.text(1.2 * np.cos(0.62) - 0.05, 1.2 * np.sin(0.62) + 0.12, r'$r$', fontsize=10, ha='center')
    ax.text(2.4 * np.cos(0.62), 2.4 * np.sin(0.62) + 0.12, r'$2r$', fontsize=10, ha='center')
    ax.annotate('넓이 $a$', (1.2, 0.12), (1.3, 0.95), fontsize=8, color=fs.ORANGE, arrowprops=dict(arrowstyle='-', color=fs.ORANGE, lw=0.6))
    ax.annotate('넓이 $4a$', (2.4, 0.3), (2.85, 1.05), fontsize=8, color=fs.ORANGE, arrowprops=dict(arrowstyle='-', color=fs.ORANGE, lw=0.6))
    ax.text(2.0, -1.55, r'세기 $I=P_s/(4\pi r^2)$: 거리 2배 → 1/4', fontsize=8, ha='center')
    fs.save(fig, F, 'fig17_03')


# ---------------------------------------------------------------- 17.3 관의 정상파
def fig04():
    fig, ax = fs.canvas(5.0, 3.5, xlim=(-0.6, 10.4), ylim=(-1.2, 7.5))
    L = 4.0
    x = np.linspace(0, L, 300)
    rows = (5.6, 3.4, 1.2)
    for col, (x0, closed) in enumerate(((0.0, False), (5.8, True))):
        for i, y0 in enumerate(rows):
            n = i + 1 if not closed else 2 * i + 1
            if closed:
                env = np.sin(n * np.pi * x / (2 * L)); lam = {1: '4L', 3: '4L/3', 5: '4L/5'}[n]
                fr = r'$f_{%d}=%sv/4L$' % (n, '' if n == 1 else str(n))
            else:
                env = np.cos(n * np.pi * x / L); lam = {1: '2L', 2: 'L', 3: '2L/3'}[n]
                fr = r'$f_{%d}=%sv/2L$' % (n, '' if n == 1 else str(n))
            h = 0.6
            ax.fill_between(x0 + x, y0 - h * np.abs(env), y0 + h * np.abs(env), color='#dbe7f3', lw=0)
            ax.plot(x0 + x, y0 + h * env, color=fs.VEL, lw=1.3)
            ax.plot(x0 + x, y0 - h * env, color=fs.VEL, lw=1.0, ls='--')
            ax.plot([x0, x0 + L], [y0 + 0.8, y0 + 0.8], color=fs.BLACK, lw=1.1)
            ax.plot([x0, x0 + L], [y0 - 0.8, y0 - 0.8], color=fs.BLACK, lw=1.1)
            if closed:
                ax.add_patch(Rectangle((x0 - 0.15, y0 - 0.8), 0.15, 1.6, fc=fs.GRAY, ec=fs.BLACK, lw=0.8))
            ax.text(x0 + L / 2, y0 - 0.88, f'$n={n}$,  ' + rf'$\lambda_{n}={lam}$,  ' + fr, ha='center', va='top', fontsize=8)
    ax.text(2.0, 7.25, '(가) 양 끝이 열린 관', ha='center', fontsize=9)
    ax.text(7.8, 7.25, '(나) 한쪽 끝이 닫힌 관', ha='center', fontsize=9)
    ax.text(7.8, -0.5, '닫힌 끝: 변위 마디·압력 배', fontsize=7.5, ha='center', va='center', color=fs.GRAY)
    ax.text(7.8, -0.95, '열린 끝: 변위 배·압력 마디', fontsize=7.5, ha='center', va='center', color=fs.GRAY)
    ax.text(2.0, -0.5, '열린 끝: 변위 배·압력 마디', fontsize=7.5, ha='center', va='center', color=fs.GRAY)
    fs.save(fig, F, 'fig17_04')


# ---------------------------------------------------------------- 17.4 맥놀이
def fig05():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 2.9), sharex=True)
    f1, f2 = 10.0, 12.0
    t = np.linspace(0, 1.0, 4000)
    s1 = np.cos(2 * np.pi * f1 * t); s2 = np.cos(2 * np.pi * f2 * t)
    a1.plot(t, s1, color=fs.VEL, lw=1.0, label=r'$s_1$ ($f_1=10$ Hz)')
    a1.plot(t, s2, color=fs.ORANGE, lw=1.0, ls='--', label=r'$s_2$ ($f_2=12$ Hz)')
    a1.legend(fontsize=7, ncol=2, loc='lower left', bbox_to_anchor=(0, 0.98), frameon=False, borderaxespad=0)
    env = 2 * np.cos(np.pi * (f1 - f2) * t)
    a2.plot(t, s1 + s2, color=fs.BLACK, lw=1.1)
    a2.plot(t, env, color=fs.FORCE, lw=1.0, ls='--'); a2.plot(t, -env, color=fs.FORCE, lw=1.0, ls='--')
    a2.text(0.26, 2.2, r'포락선 $\pm2s_m\cos(\Delta\omega\,t/2)$', fontsize=8, color=fs.FORCE, va='bottom')
    a2.annotate('', xy=(0.5, -2.6), xytext=(0.0, -2.6), arrowprops=dict(arrowstyle='<|-|>', lw=0.8, mutation_scale=7))
    a2.text(0.25, -2.7, r'$1/f_{\mathrm{beat}}=0.5$ s', fontsize=8, ha='center', va='top')
    a1.set_ylim(-1.3, 1.3); a2.set_ylim(-3.4, 2.9)
    a1.set_ylabel('$s/s_m$', fontsize=9); a2.set_ylabel(r'$(s_1+s_2)/s_m$', fontsize=9)
    a2.set_xlabel('$t$ (s)', fontsize=9); a2.set_xlim(0, 1)
    for a in (a1, a2):
        a.axhline(0, color=fs.GRAY, lw=0.4); clean(a)
    fig.align_ylabels([a1, a2])
    fig.tight_layout(h_pad=0.6)
    fs.save(fig, F, 'fig17_05')


# ---------------------------------------------------------------- 17.5 움직이는 음원의 파면
def fig06():
    fig, ax = fs.canvas(4.8, 3.4, xlim=(-4.6, 4.9), ylim=(-3.75, 3.4))
    v, vs, T = 1.0, 0.5, 0.8
    tnow = 4 * T
    t = np.linspace(0, 2 * np.pi, 300)
    for j in range(4):
        te = j * T
        cx = -0.8 + vs * te
        r = v * (tnow - te)
        ax.plot(cx + r * np.cos(t), r * np.sin(t), color=fs.VEL, lw=1.0)
        ax.plot([cx], [0], '.', color=fs.GRAY, ms=3)
    S = -0.8 + vs * tnow
    ax.add_patch(Circle((S, 0), 0.13, fc=fs.FORCE, ec='none', zorder=6))
    fs.arrow(ax, (S + 0.15, 0.3), (S + 0.85, 0.3), color=fs.FORCE, lw=1.3, ms=8)
    ax.text(S + 0.5, 0.45, '$v_S$', color=fs.FORCE, fontsize=9, ha='center', va='bottom')
    # 앞뒤 파면 간격
    front = [(-0.8 + vs * j * T) + v * (tnow - j * T) for j in range(4)]
    back = [(-0.8 + vs * j * T) - v * (tnow - j * T) for j in range(4)]
    darrow(ax, (front[3], -0.35), (front[2], -0.35), None, ms=6)
    ax.text((front[2] + front[3]) / 2, -0.5, r"$\lambda'=(v-v_S)T$", fontsize=8, ha='center', va='top',
            bbox=dict(fc='white', ec='none', pad=0.3))
    darrow(ax, (back[3], -0.35), (back[2], -0.35), None, ms=6)
    ax.text((back[2] + back[3]) / 2, -0.5, r"$(v+v_S)T$", fontsize=8, ha='center', va='top',
            bbox=dict(fc='white', ec='none', pad=0.3))
    # 관찰자
    for xo, lab in ((4.3, '높게 들림'), (-4.25, '낮게 들림')):
        ax.add_patch(Circle((xo, 0), 0.12, fc=fs.ACC, ec='none'))
        ax.text(xo, 0.25, lab, fontsize=8, ha='center', va='bottom', color=fs.ACC)
    ax.text(0.2, -3.6, '음원이 지나온 자리(회색 점)에서 낸 파면들', fontsize=8, color=fs.GRAY, ha='center')
    fs.save(fig, F, 'fig17_06')


# ---------------------------------------------------------------- 🐍 지나가는 음원의 도플러 곡선
def fig07():
    v, f0, vs, d = 343.0, 1000.0, 30.0, 20.0
    obs = np.array([0.0, d])
    te = np.linspace(-10, 10, 4001)
    src = np.stack([vs * te, np.zeros_like(te)], 1)
    r = obs - src
    dist = np.linalg.norm(r, axis=1)
    tr = te + dist / v
    cos_th = r[:, 0] / dist
    f = f0 / (1 - vs * cos_th / v)
    fig, ax = fs.plot_axes(4.4, 2.6)
    ax.plot(tr, f, color=fs.VEL, lw=1.6, label='$d=20$ m')
    d2 = 5.0
    r2 = np.array([0.0, d2]) - src; dist2 = np.linalg.norm(r2, axis=1)
    ax.plot(te + dist2 / v, f0 / (1 - vs * r2[:, 0] / dist2 / v), color=fs.ORANGE, lw=1.2, ls='--', label='$d=5$ m')
    ax.axhline(f0 * v / (v - vs), color=fs.GRAY, lw=0.7, ls=':')
    ax.axhline(f0 * v / (v + vs), color=fs.GRAY, lw=0.7, ls=':')
    ax.axhline(f0, color=fs.GRAY, lw=0.5)
    ax.text(-4.9, 1096 + 6, '1096 Hz (다가올 때)', fontsize=8, color=fs.GRAY, va='bottom')
    ax.text(4.9, 920 - 6, '920 Hz (멀어질 때)', fontsize=8, color=fs.GRAY, va='top', ha='right')
    ax.set_xlim(-5, 5); ax.set_ylim(880, 1140)
    ax.set_xlabel('소리가 도착한 시각 (s) (최근접 통과 = 0)', fontsize=8.5)
    ax.set_ylabel('들리는 진동수 (Hz)', fontsize=8.5)
    ax.tick_params(labelsize=8)
    ax.legend(fontsize=8, frameon=False, loc='center left', bbox_to_anchor=(0.0, 0.42))
    fs.save(fig, F, 'fig17_07')


# ---------------------------------------------------------------- 예제 17.7 도플러 혈류
def fig08():
    fig, ax = fs.canvas(4.0, 2.7, xlim=(-0.3, 6.3), ylim=(-1.3, 3.1))
    # 혈관
    ax.add_patch(Rectangle((0, -0.5), 6.0, 1.0, fc='#f6dcdc', ec='none'))
    ax.plot([0, 6], [0.5, 0.5], color=fs.FORCE, lw=1.1); ax.plot([0, 6], [-0.5, -0.5], color=fs.FORCE, lw=1.1)
    for xc in (1.0, 2.2, 4.6):
        ax.add_patch(Circle((xc, 0.05 * (xc % 2)), 0.13, fc=fs.FORCE, ec='none', alpha=0.8))
    fs.arrow(ax, (4.1, -0.15), (5.4, -0.15), color=fs.VEL, lw=1.6)
    ax.text(5.5, -0.15, '$u$', color=fs.VEL, fontsize=10, va='center')
    # 탐촉자와 빔: 빔이 혈류 방향과 60°
    th = np.radians(60)
    P = np.array([3.0, 0.0])
    d = np.array([-np.cos(th), np.sin(th)])        # P에서 탐촉자 쪽
    Q = P + 2.2 * d
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=fs.ORANGE, lw=1.4, ls='--')
    nrm = np.array([d[1], -d[0]])
    pr = np.array([Q + 0.3 * nrm, Q - 0.3 * nrm, Q - 0.3 * nrm + 0.55 * d, Q + 0.3 * nrm + 0.55 * d])
    ax.add_patch(Polygon(pr, closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1))
    ax.text(Q[0] + 0.4, Q[1] + 0.05, '탐촉자', fontsize=8, va='center')
    ax.plot([P[0] - 0.9, P[0] + 1.2], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, P, 0.55, 120, 180, r'$\theta=60$°', fontsize=8, tr=1.05)
    ax.text(3.0, -1.0, '혈관', fontsize=8, ha='center', color=fs.FORCE)
    ax.text(0.0, 2.85, r'빔 방향 성분 $u\cos\theta$만 도플러 이동을 만든다', fontsize=8, va='center')
    fs.save(fig, F, 'fig17_08')


# ---------------------------------------------------------------- 17.6 마하 원뿔
def fig09():
    fig, ax = fs.canvas(4.6, 3.1, xlim=(-3.8, 7.7), ylim=(-3.75, 3.8))
    v, vs = 1.0, 2.0                       # 마하 2.0 (예제 17.8)
    tnow = 3.5
    Sx = vs * tnow
    t = np.linspace(0, 2 * np.pi, 300)
    for te in (0.0, 0.875, 1.75, 2.625):
        r = v * (tnow - te)
        cx = vs * te
        ax.plot(cx + r * np.cos(t), r * np.sin(t), color=fs.VEL, lw=1.0)
        ax.plot([cx], [0], '.', color=fs.GRAY, ms=3)
    th = np.arcsin(v / vs)
    Lc = 8.4
    for sg in (1, -1):
        ax.plot([Sx, Sx - Lc * np.cos(th)], [0, sg * Lc * np.sin(th)], color=fs.FORCE, lw=1.5)
    ax.add_patch(Polygon([(Sx, 0), (Sx - 0.35, 0.12), (Sx - 0.35, -0.12)], closed=True, fc=fs.BLACK))
    # 기하: t=0에서 낸 파면
    r0 = v * tnow
    tp = (r0 * np.cos(np.pi / 2 + th), r0 * np.sin(np.pi / 2 + th))   # 접점 방향: 원뿔에 수직
    nvec = np.array([np.sin(th), np.cos(th)])
    T = np.array([0, 0]) + r0 * nvec
    ax.plot([0, T[0]], [0, T[1]], color=fs.BLACK, lw=1.0)
    ax.text(T[0] / 2 - 0.3, T[1] / 2 + 0.05, '$vt$', fontsize=10)
    ax.plot([0, Sx], [0, 0], color=fs.BLACK, lw=1.0)
    ax.text(Sx / 2, -0.2, '$v_St$', fontsize=10, ha='center', va='top', bbox=dict(fc='white', ec='none', pad=0.3))
    fs.angle_arc(ax, (Sx, 0), 0.9, 180 - np.degrees(th), 180, r'$\theta$', fontsize=10, tr=1.15)
    # 직각 표시
    u1 = -nvec * 0.22; u2 = np.array([np.cos(th), -np.sin(th)]) * 0.22
    ax.plot([T[0] + u1[0], T[0] + u1[0] + u2[0], T[0] + u2[0]], [T[1] + u1[1], T[1] + u1[1] + u2[1], T[1] + u2[1]], color=fs.BLACK, lw=0.7)
    fs.dot(ax, (0, 0), r=0.05)
    ax.text(0, 0.15, '$t$ 전의 위치', fontsize=7.5, ha='center', va='bottom', color=fs.GRAY)
    ax.text(Sx + 0.1, 0.25, '음원', fontsize=8)
    ax.text(3.3, 2.75, '마하 원뿔', color=fs.FORCE, fontsize=8, ha='center')
    fs.save(fig, F, 'fig17_09')


# ---------------------------------------------------------------- 연습문제 16 소닉 붐
def fig10():
    fig, ax = fs.canvas(4.6, 2.2, xlim=(-1.0, 9.6), ylim=(-0.9, 3.6))
    h = 2.6
    th = np.radians(30)
    xp = 2.0 + h / np.tan(th)              # 비행기 위치(원뿔이 관찰자 O에 닿는 순간)
    O = (2.0, 0.0)
    fs.ground(ax, -0.8, 9.4, y=0.0)
    ax.plot([xp, xp - (h + 0.6) / np.tan(th)], [h, -0.6 + 0.0 * h], color=fs.FORCE, lw=1.4)
    ax.add_patch(Polygon([(xp + 0.25, h), (xp - 0.35, h + 0.12), (xp - 0.35, h - 0.12)], closed=True, fc=fs.BLACK))
    fs.arrow(ax, (xp + 0.35, h), (xp + 1.2, h), color=fs.VEL, lw=1.3)
    ax.text(xp + 0.8, h + 0.15, '$v_S$', color=fs.VEL, fontsize=9, ha='center', va='bottom')
    ax.plot([-0.8, xp], [h, h], color=fs.GRAY, lw=0.7, ls=':')
    ax.add_patch(Circle(O, 0.12, fc=fs.ACC, ec='none', zorder=6))
    ax.text(O[0], -0.25, '관찰자', fontsize=8, ha='center', va='top')
    ax.plot([O[0], O[0]], [0, h], color=fs.GRAY, lw=0.8, ls='--')
    darrow(ax, (O[0] - 0.35, 0), (O[0] - 0.35, h), '$h$', off=(-0.25, 0))
    darrow(ax, (O[0], h + 0.45), (xp, h + 0.45), '$x$', off=(0, 0.2))
    fs.angle_arc(ax, (xp, h), 1.1, 180, 180 + 30, r'$\theta$', fontsize=10, tr=1.4)
    ax.text(4.0, 0.55, '마하 원뿔', color=fs.FORCE, fontsize=8, rotation=0)
    fs.save(fig, F, 'fig17_10')


for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10):
    f()
