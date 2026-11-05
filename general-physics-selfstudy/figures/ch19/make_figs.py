"""19장 기체 분자 운동론 그림. python3 figures/ch19/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch, Arc, Ellipse

kB = 1.380649e-23
NA = 6.02214076e23
R = 8.314


def mb(v, M, T):
    """맥스웰–볼츠만 속력 분포 P(v), M은 kg/mol"""
    m = M / NA
    a = m / (2 * kB * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v ** 2 * np.exp(-a * v ** 2)


# ---------------------------------------------------------------- 19.1 판데르발스 등온선
def fig01():
    fig, ax = fs.plot_axes(4.2, 2.9)
    v = np.linspace(0.42, 5, 600)
    for Tr, c in [(0.9, fs.VEL), (1.0, fs.FIELD), (1.2, fs.ACC), (1.5, fs.FORCE)]:
        p = 8 * Tr / (3 * v - 1) - 3 / v ** 2
        ax.plot(v, p, color=c, lw=1.4, label=rf'$T/T_c={Tr}$')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    ax.plot([1], [1], 'o', color=fs.BLACK, ms=5, zorder=5)
    ax.annotate('임계점', xy=(1, 1), xytext=(1.6, 1.75), fontsize=10,
                arrowprops=dict(arrowstyle='->', color=fs.BLACK, lw=0.8))
    ax.set_xlim(0, 5.2); ax.set_ylim(0, 2.4)
    ax.set_xlabel(r'$V/V_c$'); ax.set_ylabel(r'$p/p_c$')
    fs.save(fig, __file__, 'fig19_01')


# ---------------------------------------------------------------- 19.2 벽과 충돌하는 분자
def fig02():
    fig, ax = fs.canvas(5.5, 2.9, xlim=(-0.3, 9.6), ylim=(-0.6, 4.6))
    # (가) 정육면체 (사선 투영)
    L = 3.0; ox, oy = 0.9, 0.6
    F = np.array([[0, 0], [L, 0], [L, L], [0, L]])
    B = F + [ox, oy]
    # 오른쪽 벽(x = L) 강조
    ax.add_patch(Polygon([F[1], B[1], B[2], F[2]], closed=True, fc=fs.SURF, alpha=0.5, ec='none', zorder=1))
    ax.add_patch(Polygon(F, closed=True, fc='none', ec=fs.BLACK, lw=1.1, zorder=3))
    for i in (1, 2):
        ax.plot([F[i][0], B[i][0]], [F[i][1], B[i][1]], color=fs.BLACK, lw=1.1, zorder=3)
    ax.plot([F[3][0], B[3][0]], [F[3][1], B[3][1]], color=fs.BLACK, lw=1.1, zorder=3)
    ax.plot([B[3][0], B[2][0]], [B[3][1], B[2][1]], color=fs.BLACK, lw=1.1, zorder=3)
    ax.plot([B[2][0], B[1][0]], [B[2][1], B[1][1]], color=fs.BLACK, lw=1.1, zorder=3)
    ax.plot([F[0][0], B[0][0]], [F[0][1], B[0][1]], color=fs.GRAY, lw=0.8, ls='--', zorder=2)
    ax.plot([B[0][0], B[1][0]], [B[0][1], B[1][1]], color=fs.GRAY, lw=0.8, ls='--', zorder=2)
    ax.plot([B[0][0], B[3][0]], [B[0][1], B[3][1]], color=fs.GRAY, lw=0.8, ls='--', zorder=2)
    ax.text(L + ox + 0.1, L / 2 + oy / 2 + 0.3, '벽\n넓이 $L^2$', fontsize=9, ha='left', va='center')
    # 분자의 왕복 경로 (x 방향 성분만 강조)
    y0 = 1.6
    ax.plot([0.05, L - 0.12], [y0, y0], color=fs.VEL, lw=0.9, ls='--', zorder=4)
    fs.arrow(ax, (0.9, y0 + 0.12), (2.1, y0 + 0.12), color=fs.VEL, lw=1.2, ms=9)
    fs.arrow(ax, (2.1, y0 - 0.12), (0.9, y0 - 0.12), color=fs.VEL, lw=1.2, ms=9)
    ax.add_patch(Circle((L - 0.12, y0), 0.11, fc=fs.VEL, ec='none', zorder=6))
    ax.text(1.5, y0 + 0.42, r'왕복 시간 $\Delta t = 2L/v_x$', fontsize=9, ha='center', color=fs.VEL)
    # 축과 치수
    fs.arrow(ax, (0, -0.35), (L + 0.6, -0.35), color=fs.BLACK, lw=0.9, ms=8)
    ax.text(L + 0.7, -0.35, '$x$', fontsize=10, va='center')
    ax.text(0, -0.55, '0', fontsize=9, ha='center', va='top')
    ax.text(L, -0.55, '$L$', fontsize=9, ha='center', va='top')
    ax.plot([L, L], [-0.42, -0.28], color=fs.BLACK, lw=0.9)
    ax.text(-0.25, 4.35, '(가)', fontsize=10)
    # (나) 충돌 확대
    wx = 8.6
    fs.wall(ax, 0.3, 4.0, x=wx, side='right')
    hit = (wx - 0.12, 2.15)
    ax.add_patch(Circle(hit, 0.12, fc=fs.VEL, ec='none', zorder=6))
    vin = np.array([1.5, 0.9]); vout = np.array([-1.5, 0.9])
    fs.arrow(ax, hit - vin, hit - vin * 0.08, color=fs.VEL, lw=1.5, ms=10)
    fs.arrow(ax, hit, hit + vout, color=fs.VEL, lw=1.5, ms=10)
    ax.text(hit[0] - vin[0] - 0.1, hit[1] - vin[1] - 0.05, '충돌 전\n' + r'$p_x = mv_x$', fontsize=9, ha='right',
            va='center', color=fs.VEL)
    ax.text(hit[0] + vout[0] - 0.1, hit[1] + vout[1] + 0.05, '충돌 후\n' + r'$p_x = -mv_x$', fontsize=9, ha='right',
            va='center', color=fs.VEL)
    ax.text(6.2, 0.3, r'$\Delta p_x = -2mv_x$' + '\n' + r'(벽은 $+2mv_x$를 받음)', fontsize=9, ha='center',
            va='center')
    fs.arrow(ax, (wx + 0.05, 3.5), (wx + 0.75, 3.5), color=fs.FORCE, lw=1.6, ms=10)
    ax.text(wx + 0.4, 3.75, r'$\vec F$', fontsize=10, color=fs.FORCE, ha='center')
    ax.text(5.2, 4.35, '(나)', fontsize=10)
    fs.save(fig, __file__, 'fig19_02')


# ---------------------------------------------------------------- 19.4 속도 공간의 구 껍질
def fig03():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-2.4, 2.6), ylim=(-2.3, 2.4))
    v, dv = 1.5, 0.3
    th = np.linspace(0, 2 * np.pi, 300)
    xo, yo = (v + dv) * np.cos(th), (v + dv) * np.sin(th)
    xi, yi = v * np.cos(th[::-1]), v * np.sin(th[::-1])
    ax.add_patch(Polygon(np.c_[np.r_[xo, xi], np.r_[yo, yi]], closed=True, fc=fs.SURF, alpha=0.6, ec='none'))
    ax.plot(v * np.cos(th), v * np.sin(th), color=fs.BLACK, lw=0.9)
    ax.plot((v + dv) * np.cos(th), (v + dv) * np.sin(th), color=fs.BLACK, lw=0.9)
    fs.arrow(ax, (-2.2, 0), (2.4, 0), color=fs.BLACK, lw=0.8, ms=8)
    fs.arrow(ax, (0, -2.1), (0, 2.25), color=fs.BLACK, lw=0.8, ms=8)
    ax.text(2.45, -0.18, '$v_x$', fontsize=10)
    ax.text(0.12, 2.2, '$v_y$', fontsize=10)
    a = np.radians(35)
    fs.arrow(ax, (0, 0), (v * np.cos(a), v * np.sin(a)), color=fs.VEL, lw=1.4, ms=10)
    ax.text(0.55 * v * np.cos(a) - 0.15, 0.55 * v * np.sin(a) + 0.15, r'$\vec v$', color=fs.VEL, fontsize=11,
            ha='center')
    b = np.radians(-40)
    p1 = np.array([v * np.cos(b), v * np.sin(b)]); p2 = np.array([(v + dv) * np.cos(b), (v + dv) * np.sin(b)])
    ax.add_patch(FancyArrowPatch(p1 - (p2 - p1) * 1.2, p1, arrowstyle='-|>', mutation_scale=7, color=fs.BLACK, lw=0.7))
    ax.add_patch(FancyArrowPatch(p2 + (p2 - p1) * 1.2, p2, arrowstyle='-|>', mutation_scale=7, color=fs.BLACK, lw=0.7))
    ax.text(p2[0] + 0.35, p2[1] - 0.25, '$dv$', fontsize=10)
    ax.text(-0.75, -0.55, '$v$', fontsize=10)
    ax.plot([0, v * np.cos(np.radians(215))], [0, v * np.sin(np.radians(215))], color=fs.GRAY, lw=0.7, ls='--')
    ax.text(-1.95, 1.75, r'부피 $4\pi v^2\,dv$', fontsize=10, ha='left')
    fs.save(fig, __file__, 'fig19_03')


# ---------------------------------------------------------------- 19.4 두 인자의 경쟁
def fig04():
    fig, ax = fs.plot_axes(4.0, 2.6)
    x = np.linspace(0, 3, 400)
    ax.plot(x, x ** 2, color=fs.ORANGE, ls='--', lw=1.2, label=r'$v^2$ 인자 ($\propto x^2$)')
    ax.plot(x, np.exp(-x ** 2), color=fs.ACC, ls='--', lw=1.2, label=r'볼츠만 인자 $e^{-x^2}$')
    ax.plot(x, 4 / np.sqrt(np.pi) * x ** 2 * np.exp(-x ** 2), color=fs.VEL, lw=1.8,
            label=r'곱: $\frac{4}{\sqrt{\pi}}x^2e^{-x^2}$')
    ax.set_ylim(0, 1.25); ax.set_xlim(0, 3)
    ax.set_xlabel(r'$x = v/v_p$'); ax.set_ylabel('상대적 크기')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig19_04')


# ---------------------------------------------------------------- 예제 19.3 산소 분포
def fig06():
    fig, ax = fs.plot_axes(4.4, 2.8)
    M, T = 0.0320, 300
    v = np.linspace(0, 1400, 700)
    P = mb(v, M, T) * 1e3
    vp = np.sqrt(2 * R * T / M); vb = np.sqrt(8 * R * T / (np.pi * M)); vr = np.sqrt(3 * R * T / M)
    ax.plot(v, P, color=fs.VEL, lw=1.8)
    tail = v >= 2 * vp
    ax.fill_between(v[tail], 0, P[tail], color=fs.FORCE, alpha=0.35, lw=0)
    ax.annotate(r'$v>2v_p$: 약 4.6%', xy=(860, 0.12), xytext=(930, 0.75), fontsize=9, color=fs.FORCE,
                arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.8))
    for val, ytop, txt, ha, dx in [(vp, 2.25, r'$v_p=395$', 'right', -8), (vb, 2.62, r'$\bar v=446$', 'center', 0),
                                   (vr, 2.25, r'$v_{\mathrm{rms}}=484$', 'left', 8)]:
        ax.plot([val, val], [0, ytop], color=fs.BLACK, lw=0.8, ls='--')
        ax.text(val + dx, ytop + 0.03, txt, fontsize=8.5, ha=ha, va='bottom')
    ax.set_xlim(0, 1400); ax.set_ylim(0, 2.95)
    ax.set_xlabel('속력 $v$ (m/s)'); ax.set_ylabel(r'$P(v)$ ($10^{-3}$ s/m)')
    ax.text(1380, 2.6, r'$\mathrm{O_2}$, 300 K', fontsize=9.5, ha='right')
    fs.save(fig, __file__, 'fig19_06')


# ---------------------------------------------------------------- 온도·질량에 따른 분포
def fig05():
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.5))
    for ax in axs:
        ax.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    v = np.linspace(0, 2000, 800)
    for T, c in [(100, fs.VEL), (300, fs.ACC), (1000, fs.FORCE)]:
        axs[0].plot(v, mb(v, 0.0280, T) * 1e3, color=c, lw=1.5, label=f'{T} K')
    axs[0].set_xlabel('$v$ (m/s)'); axs[0].set_ylabel(r'$P(v)$ ($10^{-3}$ s/m)')
    axs[0].legend(fontsize=8.5, frameon=False); axs[0].set_title(r'(가) $\mathrm{N_2}$, 온도별', fontsize=9.5)
    axs[0].set_xlim(0, 2000); axs[0].set_ylim(0, 3.8)
    v = np.linspace(0, 4500, 900)
    for M, lab, c in [(0.0440, r'$\mathrm{CO_2}$', fs.FIELD), (0.0280, r'$\mathrm{N_2}$', fs.ACC),
                      (0.00400, 'He', fs.ORANGE), (0.00202, r'$\mathrm{H_2}$', fs.VEL)]:
        axs[1].plot(v, mb(v, M, 300) * 1e3, color=c, lw=1.5, label=lab)
    axs[1].set_xlabel('$v$ (m/s)'); axs[1].legend(fontsize=8.5, frameon=False)
    axs[1].set_title('(나) 300 K, 기체별', fontsize=9.5); axs[1].set_xlim(0, 4500); axs[1].set_ylim(0, 2.7)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig19_05')


# ---------------------------------------------------------------- 이원자 분자의 자유도
def fig07():
    fig, ax = fs.canvas(4.4, 2.9, xlim=(-2.6, 3.0), ylim=(-1.75, 2.0))
    # 축: x(결합 방향) 가로, z 세로, y 비스듬히
    fs.arrow(ax, (-2.3, 0), (2.5, 0), color=fs.GRAY, lw=0.8, ms=8)
    fs.arrow(ax, (0, -1.5), (0, 1.75), color=fs.GRAY, lw=0.8, ms=8)
    fs.arrow(ax, (0.75, 0.6), (-1.75, -1.4), color=fs.GRAY, lw=0.8, ms=8)
    ax.text(-1.95, -1.45, '$y$', fontsize=10)
    ax.text(2.55, -0.05, '$x$', fontsize=10, va='center')
    ax.text(0.1, 1.78, '$z$', fontsize=10)
    # 분자 (두 원자 + 결합 용수철)
    fs.spring(ax, (-0.95, 0), (0.95, 0), coils=5, width=0.1, lw=1.0)
    for x0 in (-1.2, 1.2):
        ax.add_patch(Circle((x0, 0), 0.32, fc='#9fb8d6', ec=fs.BLACK, lw=1.0, zorder=5))
    # z축 둘레 회전
    ax.add_patch(Arc((0, 1.05), 1.0, 0.32, theta1=200, theta2=520, color=fs.ACC, lw=1.3))
    ax.add_patch(FancyArrowPatch((0.32, 0.93), (0.45, 0.99), arrowstyle='-|>', mutation_scale=9, color=fs.ACC, lw=0))
    ax.text(0.6, 1.25, 'z축 둘레 회전', fontsize=9, color=fs.ACC)
    # y축 둘레 회전
    cy = (-1.25, -1.0)
    ax.add_patch(Arc(cy, 0.75, 0.26, angle=128.7, theta1=200, theta2=520, color=fs.ACC, lw=1.3))
    ax.text(-1.55, -0.55, 'y축 둘레 회전', fontsize=9, color=fs.ACC, ha='right')
    # x축 둘레 회전 (무시)
    ax.add_patch(Ellipse((2.05, 0), 0.22, 0.6, fc='none', ec=fs.GRAY, lw=1.0, ls='--'))
    ax.text(2.2, 0.42, 'x축 둘레 회전\n(관성모멘트 ≈ 0,\n들뜨지 않음)', fontsize=8, color=fs.GRAY, ha='left', va='bottom')
    ax.annotate('진동\n(상온에서 얼어 있음)', xy=(0.5, -0.1), xytext=(0.75, -1.05), fontsize=8, color=fs.FORCE,
                ha='left', va='center', arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.7))
    ax.text(-2.55, 1.75, '병진 3 + 회전 2 = 5', fontsize=10, ha='left')
    fs.save(fig, __file__, 'fig19_07')


# ---------------------------------------------------------------- 수소의 C_V (개략)
def fig08():
    fig, ax = fs.plot_axes(4.2, 2.7)

    def ein(th, T):
        x = th / T
        return x ** 2 * np.exp(-x) / (1 - np.exp(-x)) ** 2
    T = np.logspace(np.log10(10), np.log10(10000), 600)
    cv = 1.5 + ein(250.0, T) + ein(6300.0, T)
    ax.semilogx(T, cv, color=fs.VEL, lw=1.8)
    for y, s in [(1.5, r'$\frac{3}{2}$ (병진)'), (2.5, r'$\frac{5}{2}$ (+회전)'), (3.5, r'$\frac{7}{2}$ (+진동)')]:
        ax.axhline(y, color=fs.GRAY, lw=0.7, ls='--')
        ax.text(11, y + 0.06, s, fontsize=9, va='bottom')
    ax.axvline(300, color=fs.FORCE, lw=0.8, ls=':')
    ax.text(310, 0.6, '상온', fontsize=9, color=fs.FORCE)
    ax.set_ylim(0.5, 4.0); ax.set_xlim(10, 10000)
    ax.set_xlabel('온도 $T$ (K)'); ax.set_ylabel(r'$C_V/R$')
    fs.save(fig, __file__, 'fig19_08')


# ---------------------------------------------------------------- 등온선과 단열선
def fig09():
    fig, ax = fs.plot_axes(3.8, 2.8)
    V = np.linspace(0.38, 2.0, 400)
    ax.plot(V, 1 / V, color=fs.VEL, lw=1.6, label=r'등온선 $pV=$일정')
    ax.plot(V, V ** -1.4, color=fs.FORCE, lw=1.6, label=r'단열선 $pV^{1.4}=$일정')
    ax.plot([1], [1], 'ko', ms=4)
    ax.text(1.04, 1.06, '출발점', fontsize=9)
    for p, c in [(2.0, fs.VEL), (2 ** 1.4, fs.FORCE)]:
        ax.plot([0.5], [p], 'o', color=c, ms=4)
        ax.plot([0, 0.5], [p, p], color=c, lw=0.7, ls=':')
    ax.plot([0.5, 0.5], [0, 2 ** 1.4], color=fs.GRAY, lw=0.7, ls=':')
    ax.text(0.53, 2 ** 1.4 + 0.05, r'$2.64p_0$', fontsize=9, color=fs.FORCE, va='bottom')
    ax.set_xticks([0.5, 1, 1.5, 2]); ax.set_xticklabels([r'$V_0/2$', r'$V_0$', r'$1.5V_0$', r'$2V_0$'])
    ax.set_yticks([0, 1, 2, 3]); ax.set_yticklabels(['0', r'$p_0$', r'$2p_0$', r'$3p_0$'])
    ax.set_xlim(0, 2.05); ax.set_ylim(0, 3.6)
    ax.set_xlabel('$V$'); ax.set_ylabel('$p$')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig19_09')


# ---------------------------------------------------------------- 지그재그 경로
def fig10():
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-0.3, 8.0), ylim=(-0.3, 5.0))
    rng = np.random.default_rng(7)
    # 배경 분자
    for _ in range(45):
        ax.add_patch(Circle((rng.uniform(0, 7.7), rng.uniform(0, 4.7)), 0.07, fc='#c9d3de', ec='none', zorder=1))
    for seed in range(100):
        r2 = np.random.default_rng(seed)
        p = np.array([1.2, 1.4]); pts = [p.copy()]
        for _ in range(14):
            a = r2.uniform(0, 2 * np.pi); s_ = r2.exponential(0.8) + 0.25
            p = p + s_ * np.array([np.cos(a), np.sin(a)]); pts.append(p.copy())
        P_ = np.array(pts)
        if P_[:, 0].min() > 0.2 and P_[:, 0].max() < 7.5 and P_[:, 1].min() > 0.2 and P_[:, 1].max() < 4.5 \
                and np.linalg.norm(P_[-1] - P_[0]) > 3.0:
            break
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=fs.VEL, lw=1.2, zorder=3)
    for q in pts[1:-1]:
        ax.add_patch(Circle(q, 0.09, fc=fs.ORANGE, ec='none', zorder=4))
    ax.add_patch(Circle(pts[0], 0.12, fc=fs.VEL, ec='none', zorder=5))
    ax.add_patch(Circle(pts[-1], 0.12, fc=fs.VEL, ec='none', zorder=5))
    ax.text(pts[0][0] - 0.2, pts[0][1] + 0.05, '출발', fontsize=9, ha='right', va='center')
    ax.text(pts[-1][0] + 0.15, pts[-1][1] + 0.3, '도착', fontsize=9, ha='center')
    fs.arrow(ax, pts[0], pts[-1], color=fs.BLACK, lw=1.0, ls='--', ms=9, zorder=2)
    # 한 구간에 자유 경로 표시
    i = int(np.argmax(np.linalg.norm(np.diff(pts, axis=0), axis=1)))
    m = (pts[i] + pts[i + 1]) / 2
    d = pts[i + 1] - pts[i]; nrm = np.array([-d[1], d[0]]) / np.linalg.norm(d)
    ax.text(m[0] + 0.45 * nrm[0], m[1] + 0.45 * nrm[1], '자유 경로', fontsize=9, color=fs.VEL, ha='center', va='center')
    ax.text(7.9, 0.05, '● 충돌 지점', fontsize=8.5, color=fs.ORANGE, ha='right', va='bottom')
    fs.save(fig, __file__, 'fig19_10')
    return pts


# ---------------------------------------------------------------- 충돌 원통
def fig11():
    fig, ax = fs.canvas(5.0, 2.3, xlim=(-0.6, 7.6), ylim=(-1.7, 1.75))
    d = 0.75
    Lc = 5.2
    fs.cylinder(ax, (0.6 + Lc / 2, 0), d, Lc, vertical=False, ry=0.28)
    ax.plot([-0.4, 6.6], [0, 0], color=fs.GRAY, lw=0.7, ls='-.', zorder=2)
    # 움직이는 분자 (지름 d → 반지름 d/2)
    ax.add_patch(Circle((0.6, 0), d / 2, fc=fs.VEL, ec='none', zorder=6))
    fs.arrow(ax, (0.6 + d / 2 + 0.05, 0), (1.9, 0), color=fs.VEL, lw=1.6, ms=10, zorder=7)
    ax.text(1.3, 0.2, r'$\vec v$', color=fs.VEL, fontsize=11)
    # 다른 분자들 (중심이 원통 안: 충돌, 밖: 비켜감)
    inside = [(2.3, 0.4), (3.6, -0.5), (4.9, 0.15)]
    outside = [(2.9, 1.2), (4.2, -1.25), (5.5, 1.05), (1.6, -1.15)]
    for c in inside:
        ax.add_patch(Circle(c, d / 2, fc=fs.ORANGE, ec=fs.BLACK, lw=0.6, alpha=0.9, zorder=5))
        ax.plot(*c, 'k.', ms=3, zorder=6)
    for c in outside:
        ax.add_patch(Circle(c, d / 2, fc='#d5dbe2', ec=fs.GRAY, lw=0.6, zorder=5))
        ax.plot(*c, '.', color=fs.GRAY, ms=3, zorder=6)
    # 반지름 d 치수 (원통 오른쪽 끝 바깥)
    xr = 0.6 + Lc
    ax.plot([xr + 0.3, xr + 0.75], [d, d], color=fs.BLACK, lw=0.5)
    ax.annotate('', xy=(xr + 0.6, d), xytext=(xr + 0.6, 0),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(xr + 0.75, d / 2, '$d$', fontsize=10, ha='left', va='center')
    fs.dim(ax, (0.6, -d - 0.25), (0.6 + Lc, -d - 0.25), r'$v\,\Delta t$', off=-0.08, color=fs.BLACK)
    ax.text(xr + 0.6, -0.75, '단면적\n' + r'$\pi d^2$', fontsize=9, ha='center', va='top')
    fs.save(fig, __file__, 'fig19_11')


# ---------------------------------------------------------------- 확산
def fig12():
    fig, ax = fs.plot_axes(4.2, 2.6)
    x = np.linspace(-12, 12, 600)
    for Dt, lab, c in [(1, '$t_1$', fs.VEL), (4, '$4t_1$', fs.ACC), (16, '$16t_1$', fs.FORCE)]:
        n = np.exp(-x ** 2 / (4 * Dt)) / np.sqrt(4 * np.pi * Dt)
        ax.plot(x, n, color=c, lw=1.6, label=f'$t=${lab}')
        s = np.sqrt(2 * Dt)
        h = np.exp(-0.5) / np.sqrt(4 * np.pi * Dt)
        ax.annotate('', xy=(s, h), xytext=(-s, h),
                    arrowprops=dict(arrowstyle='<|-|>', color=c, lw=0.8, mutation_scale=7))
    ax.text(0, 0.21, r'$\pm\sqrt{\langle x^2\rangle}=\pm\sqrt{2Dt}$', fontsize=9, ha='center')
    ax.set_xlim(-12, 12); ax.set_ylim(0, 0.3)
    ax.set_xlabel(r'$x/\sqrt{Dt_1}$'); ax.set_ylabel(r'$n/N$ (임의 단위)')
    ax.set_yticks([])
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig19_12')


# ---------------------------------------------------------------- 막 투과의 농도 분포
def fig13():
    fig, ax = fs.plot_axes(4.2, 2.6)
    ax.grid(False)
    h = 1.0; C1, C2, K = 1.0, 0.35, 2.0
    ax.axvspan(0, h, color=fs.SURF, alpha=0.45, lw=0)
    ax.plot([-1.2, 0], [C1, C1], color=fs.VEL, lw=1.8)
    ax.plot([0, h], [K * C1, K * C2], color=fs.FORCE, lw=1.8)
    ax.plot([h, 2.2], [C2, C2], color=fs.VEL, lw=1.8)
    ax.plot([0, 0], [C1, K * C1], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot([h, h], [C2, K * C2], color=fs.GRAY, lw=0.7, ls=':')
    ax.text(-0.6, C1 + 0.08, '$C_1$', fontsize=10, ha='center', color=fs.VEL)
    ax.text(1.6, C2 + 0.08, '$C_2$', fontsize=10, ha='center', color=fs.VEL)
    ax.text(0.05, K * C1 + 0.05, '$KC_1$', fontsize=10, ha='left', va='bottom', color=fs.FORCE)
    ax.text(h + 0.05, K * C2 + 0.05, '$KC_2$', fontsize=10, ha='left', va='bottom', color=fs.FORCE)
    ax.text(h / 2, 2.35, '막(지질)', fontsize=9, ha='center')
    ax.text(-0.6, 2.35, '바깥(물)', fontsize=9, ha='center')
    ax.text(1.6, 2.35, '안쪽(물)', fontsize=9, ha='center')
    fs.arrow(ax, (0.2, 0.3), (0.8, 0.3), color=fs.ACC, lw=1.5, ms=10)
    ax.text(0.5, 0.42, '흐름 $J$', fontsize=9, color=fs.ACC, ha='center')
    ax.annotate('', xy=(h, 0.08), xytext=(0, 0.08),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(h / 2, 0.14, '$h$', fontsize=10, ha='center')
    ax.set_xlim(-1.2, 2.2); ax.set_ylim(0, 2.6)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('위치 $x$'); ax.set_ylabel('약물 농도')
    fs.save(fig, __file__, 'fig19_13')


# ---------------------------------------------------------------- 분출 (연습문제 15)
def fig14():
    fig, ax = fs.canvas(4.0, 3.1, xlim=(-3.6, 1.6), ylim=(-2.1, 2.2))
    # 벽 (x = 0), 구멍은 y ∈ [-0.5, 0.5]
    a = 0.5
    for y0, y1 in [(-2.0, -a), (a, 2.1)]:
        ax.add_patch(Rectangle((0, y0), 0.22, y1 - y0, fc='#cfcfcf', ec=fs.BLACK, lw=1.0, zorder=3))
    ax.text(0.5, 0, '구멍\n넓이 $A$', fontsize=9, ha='left', va='center')
    ax.text(-3.5, 1.95, '기체', fontsize=10)
    ax.text(0.55, 1.75, '진공', fontsize=10)
    th = np.radians(35); L = 2.2
    u = np.array([np.cos(th), np.sin(th)])     # 분자의 진행 방향 (벽 쪽으로)
    P = [(-L * u[0], -a - L * u[1]), (0, -a), (0, a), (-L * u[0], a - L * u[1])]
    ax.add_patch(Polygon(P, closed=True, fc=fs.SURF, alpha=0.55, ec=fs.BLACK, lw=0.9, zorder=2))
    for yy in (-0.25, 0.25):
        fs.arrow(ax, (-L * u[0] * 0.9, yy - L * u[1] * 0.9), (-L * u[0] * 0.25, yy - L * u[1] * 0.25),
                 color=fs.VEL, lw=1.2, ms=9)
    ax.text(-0.95, -1.72, r'기울어진 길이 $v\,dt$', fontsize=9, ha='center', va='center', rotation=35)
    # 법선과 각
    ax.plot([-1.8, 0], [a, a], color=fs.GRAY, lw=0.7, ls='--')
    fs.angle_arc(ax, (0, a), 1.15, 180, 180 + 35, r'$\theta$', fontsize=10)
    fs.arrow(ax, (0.22, -1.25), (1.1, -1.25), color=fs.BLACK, lw=1.1, ms=9)
    ax.text(1.15, -1.25, r'$\hat n$', fontsize=10, va='center')
    # 높이 v dt cosθ
    ax.annotate('', xy=(-L * u[0], 1.55), xytext=(0, 1.55),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=7))
    ax.plot([-L * u[0], -L * u[0]], [a - L * u[1] + 0.05, 1.62], color=fs.GRAY, lw=0.5)
    ax.text(-L * u[0] / 2, 1.7, r'$v\,dt\cos\theta$', fontsize=9, ha='center', color=fs.GRAY)
    fs.save(fig, __file__, 'fig19_14')


if __name__ == '__main__':
    names = sys.argv[1:] or [f'fig{i:02d}' for i in range(1, 15)]
    for n in names:
        globals()[n]()
