"""6장 뉴턴 법칙의 응용 그림. 실행: python3 figures/ch06/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Arc

g = 9.8


def style(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def force(ax, c, d, label=None, color=fs.FORCE, start=0.0, lw=1.8, fontsize=10, loff=(0, 0), ha='center',
          ms=11, ls='-'):
    """점 c에서 방향 d로 힘 화살표. start>0이면 c에서 그만큼 떨어진 곳에서 시작."""
    c = np.asarray(c, float); d = np.asarray(d, float)
    u = d / np.hypot(*d)
    p = c + u * start
    fs.arrow(ax, tuple(p), tuple(p + d), color=color, lw=lw, ms=ms, ls=ls)
    if label:
        q = p + d + u * 0.22 + np.array(loff)
        ax.text(q[0], q[1], label, color=color, fontsize=fontsize, ha=ha, va='center')


def rope(ax, p, q, lw=1.1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=fs.BLACK, lw=lw, zorder=2)


# ---------- 그림 6.1 미는 힘과 마찰력 ----------
def fig01():
    fig, ax = fs.plot_axes(4.2, 2.6)
    m, mus, muk = 10.0, 0.40, 0.30
    fsmax, fk = mus * m * g, muk * m * g
    ax.plot([0, fsmax], [0, fsmax], color=fs.FORCE, lw=1.8)
    ax.plot([fsmax, fsmax], [fsmax, fk], color=fs.FORCE, lw=1.0, ls=':')
    ax.plot([fsmax, 70], [fk, fk], color=fs.FORCE, lw=1.8)
    ax.axhline(fsmax, color=fs.GRAY, lw=0.7, ls='--')
    ax.text(2, fsmax + 1.0, r'$f_{s,\max} = \mu_sN = 39.2$ N', fontsize=8.5, color=fs.GRAY, va='bottom')
    ax.text(48, fk - 1.5, r'$f_k = \mu_kN = 29.4$ N', fontsize=8.5, color=fs.FORCE, va='top', ha='center')
    ax.text(14, 22, '정지마찰\n$f_s = F$', fontsize=8.5, color=fs.FORCE, ha='center')
    ax.text(fsmax + 1, 12, '미끄러지기\n시작', fontsize=8, color=fs.BLACK, ha='left')
    ax.annotate('', xy=(fsmax, 0.5), xytext=(fsmax + 0.8, 11), arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.set_xlim(0, 70); ax.set_ylim(0, 50)
    ax.set_xlabel(r'수평으로 미는 힘 $F$ (N)'); ax.set_ylabel(r'마찰력 $f$ (N)')
    fs.save(fig, __file__, 'fig06_01')


def incline_with_block(ax, th_deg, L, s_pos, bw=0.9, bh=0.6, label=None):
    th = np.radians(th_deg)
    u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    top = np.array(fs.incline(ax, origin=(0, 0), length=L, angle=th_deg, show_angle=False))
    c = u * s_pos + n * (bh / 2)
    fs.block(ax, tuple(c), bw, bh, angle=th_deg, text=label, fontsize=9)
    return c, u, n, top


# ---------- 그림 6.2 예제 6.1 임계각 ----------
def fig02():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-0.2, 6.0), ylim=(-0.4, 3.4))
    th = np.degrees(np.arctan(0.5))
    c, u, n, top = incline_with_block(ax, th, 6.0, 3.3, bw=1.0, bh=0.65)
    fs.angle_arc(ax, (0, 0), 0.9, 0, th, None)
    ax.text(1.05, 0.22, r'$\theta_c = 26.6^\circ$', fontsize=9, va='center')
    sc = 1.5
    force(ax, c, (0, -sc), r'$m\vec g$', loff=(0.3, 0.1))
    force(ax, c, n * sc * np.cos(np.radians(th)), r'$\vec N$', start=0.33, loff=(-0.1, 0))
    fpt = c - n * 0.325 + u * 0.0
    force(ax, fpt, u * sc * np.sin(np.radians(th)), r'$\vec f_s$', start=0.5, loff=(0.0, 0.25))
    ax.text(3.6, -0.3, r'$f_s = mg\sin\theta_c = \mu_sN$', fontsize=8.5, ha='left', color=fs.FORCE)
    fs.save(fig, __file__, 'fig06_02')


# ---------- 그림 6.3 예제 6.2 비스듬히 끄는 상자 ----------
def fig03():
    fig = plt.figure(figsize=(5.4, 2.4))
    ax = fig.add_axes([0.0, 0.0, 0.45, 1.0]); ax.axis('off'); ax.set_aspect('equal')
    ax.set_xlim(-1.6, 2.8); ax.set_ylim(-1.7, 2.3)
    fs.ground(ax, -1.5, 2.7, 0, depth=0.15, n=25)
    c = np.array([0.4, 0.4])
    fs.block(ax, tuple(c), 1.1, 0.8, text='20 kg', fontsize=8)
    th = np.radians(26.6)
    sc = 1.4 / 196.0   # N당 길이: mg = 196 N, T = 87.7 N, N = 157 N, f_k = 78.4 N
    force(ax, c + (0.55, 0.0), 87.7 * sc * np.array([np.cos(th), np.sin(th)]), r'$\vec T$', loff=(0.05, 0.1))
    ax.plot([c[0] + 0.55, c[0] + 1.9], [c[1], c[1]], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, tuple(c + (0.55, 0)), 0.75, 0, 26.6, r'$\theta$', fontsize=9, tr=0.98)
    force(ax, c, (0, 157 * sc), r'$\vec N$', start=0.4, loff=(0.25, -0.15))
    force(ax, c, (0, -196 * sc), r'$m\vec g$', start=0.4, loff=(0.4, 0.2))
    force(ax, (c[0] - 0.55, 0.06), (-78.4 * sc, 0), r'$\vec f_k$', loff=(0, 0.25))
    fs.vec(ax, (-1.2, 1.7), (0.8, 0), color=fs.VEL, lw=1.4, ms=9)
    ax.text(-0.3, 1.7, '등속', fontsize=8, color=fs.VEL, va='center')
    ax.text(-1.55, 2.15, '(가)', fontsize=9)
    ax2 = fig.add_axes([0.58, 0.2, 0.4, 0.72]); style(ax2)
    t = np.linspace(0, 70, 300); mk = 0.5
    T = mk * 20 * g / (np.cos(np.radians(t)) + mk * np.sin(np.radians(t)))
    ax2.plot(t, T, color=fs.FORCE)
    ax2.plot(26.6, 87.7, 'o', color=fs.FORCE, ms=4)
    ax2.text(26.6, 82, '$(26.6^\\circ, 87.7$ N$)$', fontsize=7.5, ha='center', va='top')
    ax2.set_xlim(0, 70); ax2.set_ylim(75, 125)
    ax2.set_xlabel(r'$\theta$ (°)', labelpad=1); ax2.set_ylabel(r'$T$ (N)', labelpad=1)
    ax2.tick_params(labelsize=8)
    ax2.set_title('(나)', fontsize=9, loc='left')
    fs.save(fig, __file__, 'fig06_03')


# ---------- 그림 6.4 끌림힘과 선형 끌림의 v(t) ----------
def fig04():
    fig = plt.figure(figsize=(5.0, 2.3))
    ax = fig.add_axes([0.0, 0.0, 0.3, 1.0]); ax.axis('off'); ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.4); ax.set_ylim(-2.2, 1.9)
    ax.add_patch(Circle((0, 0), 0.3, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=4))
    force(ax, (0, 0), (0, -1.5), r'$m\vec g$', start=0.3, loff=(0.4, 0.2))
    force(ax, (0, 0), (0, 1.0), r'$\vec D$', start=0.3, loff=(0.3, -0.15))
    fs.vec(ax, (0.75, 0.4), (0, -1.1), color=fs.VEL, lw=1.5, ms=9)
    ax.text(0.95, -0.2, r'$\vec v$', color=fs.VEL, fontsize=10)
    ax.text(-1.15, 1.6, '(가)', fontsize=9)
    ax2 = fig.add_axes([0.42, 0.2, 0.56, 0.72]); style(ax2)
    x = np.linspace(0, 5, 300)
    ax2.plot(x, 1 - np.exp(-x), color=fs.VEL, lw=1.6)
    ax2.axhline(1, color=fs.GRAY, ls='--', lw=0.8)
    ax2.plot([1, 1], [0, 1 - np.exp(-1)], color=fs.GRAY, lw=0.7, ls=':')
    ax2.plot(1, 1 - np.exp(-1), 'o', color=fs.VEL, ms=3.5)
    ax2.text(1.1, 0.58, r'$t = \tau$: $0.63\,v_T$', fontsize=8)
    ax2.plot([0, 1], [0, 1], color=fs.GRAY, lw=0.7, ls='--')
    ax2.text(1.1, 1.02, r'← 처음 기울기 $g$', fontsize=7.5, color=fs.GRAY, ha='left', va='bottom')
    ax2.set_xlabel(r'$t/\tau$', labelpad=1); ax2.set_ylabel(r'$v/v_T$', labelpad=1)
    ax2.set_xlim(0, 5); ax2.set_ylim(0, 1.18)
    ax2.tick_params(labelsize=8)
    ax2.set_title('(나)', fontsize=9, loc='left')
    fs.save(fig, __file__, 'fig06_04')


# ---------- 그림 6.5 예제 6.3 스카이다이버 ----------
def fig05():
    fig, ax = fs.plot_axes(4.2, 2.6)
    m, C, A, rho = 80, 1.0, 0.70, 1.2
    vT = np.sqrt(2 * m * g / (C * rho * A))
    t = np.linspace(0, 15, 400)
    ax.plot(t, vT * np.tanh(g * t / vT), color=fs.VEL, lw=1.7, label='이차 끌림')
    t2 = np.linspace(0, 6.6, 50)
    ax.plot(t2, g * t2, color=fs.GRAY, lw=1.0, ls='--', label='끌림 없음 ($v = gt$)')
    ax.axhline(vT, color=fs.BLACK, lw=0.8, ls=':')
    ax.text(14.8, vT + 1.2, r'$v_T = 43.2$ m/s', fontsize=8.5, ha='right', va='bottom')
    t90 = np.arctanh(0.9) * vT / g
    ax.plot(t90, 0.9 * vT, 'o', color=fs.VEL, ms=4)
    ax.plot([t90, t90], [0, 0.9 * vT], color=fs.VEL, lw=0.6, ls=':')
    ax.text(t90 + 0.3, 0.9 * vT - 3, '6.5 s, $0.9\\,v_T$', fontsize=8, va='top')
    ax.set_xlim(0, 15); ax.set_ylim(0, 66)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    ax.legend(fontsize=8, loc='lower right', frameon=False)
    fs.save(fig, __file__, 'fig06_05')


# ---------- 그림 6.6 낙하산 시뮬레이션(🐍) ----------
def fig06():
    m, rho = 80.0, 1.2
    def CA(t):
        s = np.clip((t - 20.0) / 3.0, 0, 1)
        return 0.70 + s * (30.0 - 0.70)
    dt = 0.001; n = 60000
    t = np.arange(n) * dt; v = np.zeros(n)
    for i in range(n - 1):
        v[i + 1] = v[i] + (g - 0.5 * rho * CA(t[i]) * v[i] ** 2 / m) * dt
    fig, ax = fs.plot_axes(4.2, 2.5)
    ax.plot(t, v, color=fs.VEL, lw=1.6)
    ax.axvspan(20, 23, color=fs.ORANGE, alpha=0.15, lw=0)
    ax.text(21.5, 47, '낙하산\n펴짐', fontsize=8, ha='center', va='bottom', color='#a0521a')
    ax.text(10, 45, '43.2 m/s', fontsize=8, ha='center', va='bottom')
    ax.text(45, 9, '6.60 m/s', fontsize=8, ha='center', va='bottom')
    ax.set_xlim(0, 60); ax.set_ylim(0, 56)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    fs.save(fig, __file__, 'fig06_06')


# ---------- 그림 6.7 예제 6.5 경사진 커브 ----------
def fig07():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    th = np.radians(10)
    u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    for ax, case in zip(axs, ('가', '나')):
        ax.axis('off'); ax.set_aspect('equal'); ax.set_xlim(-2.3, 2.6); ax.set_ylim(-1.9, 2.2)
        p0 = -2.1 * u; p1 = 2.3 * u
        ax.add_patch(Polygon([tuple(p0), tuple(p1), (p1[0], -0.75), (p0[0], -0.75)], fc='#e6e6e6', ec='none'))
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=fs.BLACK, lw=1.3)
        ax.plot([0.6, 1.8], [0.6 * np.tan(th) * 0 + 0.106, 0.106], color=fs.GRAY, lw=0.5, ls=':')
        c = n * 0.3
        fs.block(ax, tuple(c), 0.75, 0.6, angle=10, text='차', fontsize=8)
        if case == '가':
            N = 1.1 / np.cos(th)
            force(ax, c, n * N, r'$\vec N$', start=0.3, loff=(-0.05, 0.0))
            force(ax, c, (0, -1.1), r'$m\vec g$', loff=(0.4, 0.15))
            ax.set_title('(가) 설계 속력: 마찰 없음', fontsize=8.5)
        else:
            mu = 0.6
            N = 1.1 / (np.cos(th) - mu * np.sin(th))
            force(ax, c, n * N, r'$\vec N$', start=0.3, loff=(-0.05, 0.0))
            force(ax, c, (0, -1.1), r'$m\vec g$', loff=(0.4, 0.15))
            fpt = c - n * 0.3
            force(ax, fpt, -u * mu * N, None, start=0.38)
            ax.text(-1.25, 0.25, r'$f = \mu_sN$', color=fs.FORCE, fontsize=8.5, ha='center')
            ax.set_title('(나) 최대 속력: 마찰력은 안쪽 아래로', fontsize=8.5)
        fs.vec(ax, (1.2, 1.3), (-1.1, 0), color=fs.ACC, lw=1.6, ms=9)
        ax.text(0.65, 1.55, r'$a = v^2/r$', color=fs.ACC, fontsize=8.5, ha='center')
        ax.text(-2.2, 1.85, '← 곡선의 중심', fontsize=7.5, color=fs.GRAY)
        fs.angle_arc(ax, tuple(p0), 0.6, 0, 10, None)
        ax.plot([p0[0], p0[0] + 0.9], [p0[1], p0[1]], color=fs.GRAY, lw=0.6)
        ax.text(p0[0] + 0.7, p0[1] - 0.15, r'$\theta$', fontsize=9, va='top')
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig06_07')


# ---------- 그림 6.8 수직 원운동 ----------
def fig08():
    fig, ax = fs.canvas(3.2, 3.3, xlim=(-2.1, 2.4), ylim=(-2.9, 2.3))
    R = 1.5
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.BLACK, lw=2.2)
    fs.dot(ax, (0, 0), r=0.04)
    ax.plot([0, R * np.cos(np.radians(200))], [0, R * np.sin(np.radians(200))], color=fs.GRAY, lw=0.7)
    ax.text(-0.8, -0.05, r'$R$', fontsize=9, color=fs.GRAY)
    yt, yb = R - 0.15, -R + 0.15
    for y in (yt, yb):
        ax.add_patch(Circle((0, y), 0.13, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=5))
    force(ax, (-0.12, yt), (0, -0.55), start=0.13)
    ax.text(-0.3, yt - 0.6, r'$\vec N$', color=fs.FORCE, fontsize=9, ha='right')
    force(ax, (0.12, yt), (0, -0.75), start=0.13)
    ax.text(0.3, yt - 0.75, r'$m\vec g$', color=fs.FORCE, fontsize=9, ha='left')
    ax.text(0, R + 0.2, '꼭대기: $N + mg = mv^2/R$', fontsize=8, ha='center', va='bottom')
    force(ax, (-0.12, yb), (0, 1.05), start=0.13)
    ax.text(-0.3, yb + 0.95, r'$\vec N$', color=fs.FORCE, fontsize=9, ha='right')
    force(ax, (0.12, yb), (0, -0.75), start=0.13)
    ax.text(0.3, yb - 0.8, r'$m\vec g$', color=fs.FORCE, fontsize=9, ha='left')
    ax.text(0, -R - 0.95, '바닥: $N - mg = mv^2/R$', fontsize=8, ha='center', va='top')
    fs.vec(ax, (1.0, R - 0.25), (0, -0.55), color=fs.ACC, lw=1.4, ms=8)
    ax.text(1.15, R - 0.55, r'$\vec a$', color=fs.ACC, fontsize=9)
    fs.vec(ax, (1.0, -R + 0.25), (0, 0.55), color=fs.ACC, lw=1.4, ms=8)
    ax.text(1.15, -R + 0.5, r'$\vec a$', color=fs.ACC, fontsize=9)
    fs.save(fig, __file__, 'fig06_08')


# ---------- 그림 6.9 원뿔 진자 ----------
def fig09():
    fig, ax = fs.canvas(3.4, 3.1, xlim=(-2.0, 2.6), ylim=(-0.5, 3.6))
    L = 2.8; th = np.radians(30)
    O = np.array([0, 3.2]); r = L * np.sin(th); h = L * np.cos(th)
    fs.ceiling(ax, -0.8, 0.8, O[1])
    C = O - (0, h)
    fs.ellipse3d(ax, tuple(C), r, 0.28 * r, color=fs.GRAY, lw=0.9)
    B = C + (r, 0)
    rope(ax, O, B, lw=1.2)
    ax.plot([O[0], C[0]], [O[1], C[1] - 0.2], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([C[0], B[0]], [C[1], B[1]], color=fs.GRAY, lw=0.7, ls=':')
    fs.angle_arc(ax, tuple(O), 0.6, -90, -90 + 30, r'$\theta$', fontsize=9, tr=0.85)
    m = (O + B) / 2
    ax.text(m[0] - 0.2, m[1] - 0.05, r'$L$', fontsize=10, ha='right')
    ax.text((C[0] + B[0]) / 2, C[1] + 0.1, r'$L\sin\theta$', fontsize=8.5, ha='center', va='bottom')
    ax.add_patch(Circle(tuple(B), 0.13, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=5))
    d = (O - B) / L
    force(ax, B, d * 1.25, r'$\vec T$', start=0.13, loff=(0.2, 0.0))
    force(ax, B, (0, -1.08), r'$m\vec g$', start=0.13, loff=(0.4, 0.15))
    fs.vec(ax, (B[0] - 0.2, B[1] - 0.25), (-0.7, 0), color=fs.ACC, lw=1.5, ms=9)
    ax.text(B[0] - 0.6, B[1] - 0.48, r'$\vec a$', color=fs.ACC, fontsize=10, ha='center')
    fs.save(fig, __file__, 'fig06_09')


# ---------- 그림 6.10 예제 6.6 가속하는 열차 안의 진자 ----------
def fig10():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.6))
    a = 2.0; th = np.arctan(a / g); L = 2.0
    for ax, case in zip(axs, ('가', '나')):
        ax.axis('off'); ax.set_aspect('equal'); ax.set_xlim(-1.9, 2.0); ax.set_ylim(-3.6, 0.6)
        fs.ceiling(ax, -1.2, 1.2, 0.2)
        O = np.array([0, 0.2]); B = O + L * np.array([-np.sin(th), -np.cos(th)])
        ax.plot([0, 0], [0.2, -2.0], color=fs.GRAY, lw=0.6, ls='--')
        rope(ax, O, B, lw=1.2)
        fs.angle_arc(ax, tuple(O), 0.9, -90 - np.degrees(th), -90, None)
        ax.text(-0.12, -0.95, r'$\theta$', fontsize=9, ha='center')
        ax.add_patch(Circle(tuple(B), 0.12, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=5))
        sc = 1.4 / g
        T = np.array([np.sin(th), np.cos(th)]) * np.hypot(a, g) * sc
        force(ax, B, T, r'$\vec T$', start=0.12, loff=(0.25, -0.05))
        force(ax, B, (0, -g * sc), r'$m\vec g$', start=0.12, loff=(0.35, 0.2))
        if case == '가':
            fs.vec(ax, (0.6, -1.8), (0.9, 0), color=fs.ACC, lw=1.6, ms=9)
            ax.text(1.05, -1.6, r'$\vec a$', color=fs.ACC, fontsize=10, ha='center')
            ax.set_title('(가) 지면 기준틀', fontsize=8.5)
        else:
            force(ax, B, (-a * sc, 0), r'$-m\vec A$', start=0.12, loff=(-0.25, 0.25), ls='--', lw=1.4, fontsize=9, ms=8)
            ge = np.array([-a, -g]) * sc
            fs.vec(ax, (1.3, -0.9), tuple(ge), color=fs.FIELD, lw=1.5, ms=9)
            ax.text(1.15, -2.45, r'$\vec g_{\mathrm{eff}}$', color=fs.FIELD, fontsize=9, ha='center', va='top')
            ax.set_title('(나) 열차 기준틀', fontsize=8.5)
        fs.vec(ax, (0.35, -3.35), (0.6, 0), color=fs.GRAY, lw=1.0, ms=8)
        ax.text(0.65, -3.5, '열차의 가속 방향', fontsize=7, color=fs.GRAY, ha='center', va='top')
    fig.tight_layout(w_pad=0.3)
    fs.save(fig, __file__, 'fig06_10')


# ---------- 그림 6.11 예제 6.7 지구 자전과 겉보기 중력 ----------
def fig11():
    fig, ax = fs.canvas(3.8, 3.2, xlim=(-1.8, 3.1), ylim=(-1.75, 2.0))
    R = 1.4
    ax.add_patch(Circle((0, 0), R, fc='#e7eef6', ec=fs.BLACK, lw=1.2))
    ax.plot([0, 0], [-1.7, 1.75], color=fs.BLACK, lw=0.9, ls='-.')
    ax.add_patch(Arc((0, 1.6), 0.5, 0.16, theta1=200, theta2=520 - 180, color=fs.BLACK, lw=0.8))
    fs.arrow(ax, (0.2, 1.56), (0.26, 1.6), ms=7, lw=0.8)
    ax.text(0.3, 1.75, r'$\vec\omega$', fontsize=10)
    ax.plot([-R, R], [0, 0], color=fs.GRAY, lw=0.6, ls='--')
    ax.text(-R + 0.05, 0.08, '적도', fontsize=7.5, color=fs.GRAY)
    lam = np.radians(37.5)
    P = R * np.array([np.cos(lam), np.sin(lam)])
    ax.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=0.9)
    fs.angle_arc(ax, (0, 0), 0.4, 0, 37.5, r'$\lambda$', fontsize=9, tr=0.55)
    ax.plot([0, P[0]], [P[1], P[1]], color=fs.GRAY, lw=0.8, ls=':')
    ax.text(P[0] / 2, P[1] + 0.06, r'$R\cos\lambda$', fontsize=8, ha='center', va='bottom', color=fs.GRAY)
    fs.dot(ax, P, r=0.04)
    gdir = -P / R
    gl = 1.0
    fs.vec(ax, tuple(P), tuple(gdir * gl), color=fs.FIELD, lw=1.5, ms=9)
    q = P + gdir * gl * 0.55 - np.array([-gdir[1], gdir[0]]) * 0.2
    ax.text(q[0], q[1], r'$\vec g$', color=fs.FIELD, fontsize=10, ha='center', va='center')
    fs.vec(ax, tuple(P), (0.55, 0), color=fs.ACC, lw=1.5, ms=9)
    ax.text(P[0] + 0.6, P[1] + 0.12, r'$\omega^2R\cos\lambda$', color=fs.ACC, fontsize=8.5)
    ax.text(P[0] + 0.6, P[1] - 0.12, '(원심 가속도)', color=fs.ACC, fontsize=7, va='top')
    # 연추 방향(과장): g + 원심
    ge = gdir * gl + np.array([0.4, 0])
    fs.vec(ax, tuple(P), tuple(ge), color=fs.BLACK, lw=1.0, ms=8, ls='--')
    ax.annotate('연추 방향\n(기울기 과장)', xy=tuple(P + ge * 0.85), xytext=(1.6, -0.45), fontsize=7, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', lw=0.5, color=fs.BLACK))
    fs.save(fig, __file__, 'fig06_11')


# ---------- 그림 6.12 예제 6.8 움직도르래가 있는 계 ----------
def fig12():
    fig, ax = fs.canvas(5.2, 2.9, xlim=(-0.2, 9.4), ylim=(-0.3, 4.9))
    ty = 3.0
    ax.add_patch(Rectangle((0.0, ty - 0.2), 3.2, 0.2, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((0.2, 0.0), 0.18, ty - 0.2, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((2.8, 0.0), 0.18, ty - 0.2, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    fs.ground(ax, -0.1, 3.4, 0, depth=0.15, n=20)
    fs.block(ax, (1.2, ty + 0.3), 1.0, 0.6, text='A', fontsize=9)
    r1 = 0.22; P1 = np.array([3.4, ty + 0.3 - r1])
    ax.plot([3.2, P1[0]], [ty - 0.1, P1[1]], color=fs.BLACK, lw=1.1)
    r2 = 0.32; P2 = np.array([P1[0] + r1 + r2, 1.35])
    rope(ax, (1.7, ty + 0.3), (P1[0], ty + 0.3))
    rope(ax, (P1[0] + r1, P1[1]), (P1[0] + r1, P2[1]))
    rope(ax, (P2[0] + r2, P2[1]), (P2[0] + r2, 4.4))
    fs.ceiling(ax, P2[0] + r2 - 0.45, P2[0] + r2 + 0.45, 4.4)
    fs.pulley(ax, tuple(P1), r=r1)
    fs.pulley(ax, tuple(P2), r=r2)
    rope(ax, P2, (P2[0], 0.75))
    fs.block(ax, (P2[0], 0.45), 0.6, 0.6, text='B', fontsize=9)
    ax.text(P2[0] + r2 + 0.1, P2[1] - 0.05, '움직\n도르래', fontsize=7, va='center')
    fs.vec(ax, (0.7, ty + 0.85), (0.8, 0), color=fs.ACC, lw=1.4, ms=8)
    ax.text(1.6, ty + 0.85, r'$a_A$', color=fs.ACC, fontsize=9, va='center')
    fs.vec(ax, (P2[0] + 0.55, 0.75), (0, -0.55), color=fs.ACC, lw=1.4, ms=8)
    ax.text(P2[0] + 0.65, 0.45, r'$a_B$', color=fs.ACC, fontsize=9, ha='left', va='center')
    # 자유물체도
    cA = np.array([6.3, 3.6])
    fs.block(ax, tuple(cA), 0.8, 0.5, text='A', fontsize=9)
    force(ax, cA, (1.0, 0), r'$T$', start=0.4, loff=(0.1, 0.22))
    ax.text(cA[0], cA[1] - 0.5, '(연직 힘 $N$, $m_Ag$는\n서로 상쇄)', fontsize=7, ha='center', va='top')
    cB = np.array([8.4, 1.6])
    ax.add_patch(Circle(tuple(cB + (0, 0.45)), 0.22, fc='#dfe6ee', ec=fs.BLACK, lw=1.0, zorder=4))
    rope(ax, cB + (0, 0.45), cB)
    fs.block(ax, tuple(cB - (0, 0.15)), 0.5, 0.5, text='B', fontsize=8)
    sc = 1.0 / 21.4
    force(ax, cB + (-0.22, 0.45), (0, 10.7 * sc * 1.5), r'$T$', loff=(-0.05, 0.05), fontsize=9)
    force(ax, cB + (0.22, 0.45), (0, 10.7 * sc * 1.5), r'$T$', loff=(0.05, 0.05), fontsize=9)
    force(ax, cB - (0, 0.4), (0, -29.4 * sc * 1.5), r'$m_Bg$', loff=(0.45, 0.2), fontsize=9)
    ax.text(7.3, 4.6, '자유물체도', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig06_12')


# ---------- 그림 6.13 연습문제 14: 쐐기 기준틀 ----------
def fig13():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-1.7, 6.0), ylim=(-0.4, 3.9))
    fs.ground(ax, -1.6, 5.9, 0, depth=0.15, n=40)
    th = np.radians(30); W = 4.5; H = W * np.tan(th)
    ax.add_patch(Polygon([(0, 0), (W, 0), (0, H)], fc='#f2f2f2', ec=fs.BLACK, lw=1.2, zorder=1))
    ax.text(0.5, 0.45, '$M$', fontsize=11)
    fs.angle_arc(ax, (W, 0), 0.7, 150, 180, r'$\theta$', fontsize=10, tr=0.95)
    u = np.array([np.cos(th), -np.sin(th)]); n = np.array([np.sin(th), np.cos(th)])
    c = np.array([0, H]) + u * 2.0 + n * 0.3
    fs.block(ax, tuple(c), 0.8, 0.6, angle=-30, text='$m$', fontsize=10)
    fs.vec(ax, (-0.2, 1.0), (-1.1, 0), color=fs.ACC, lw=1.6, ms=9)
    ax.text(-0.75, 1.25, r'$A$', color=fs.ACC, fontsize=10, ha='center')
    ax.text(-1.6, 3.6, '마찰 없는 쐐기와 블록', fontsize=8)
    fs.save(fig, __file__, 'fig06_13')


# ---------- 그림 6.14 연습문제 17: 회전하는 막대의 구슬 ----------
def fig14():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-1.7, 2.6), ylim=(-1.0, 2.8))
    phi = np.radians(35)
    e = np.array([np.cos(phi), np.sin(phi)]); t = np.array([-np.sin(phi), np.cos(phi)])
    ax.plot([-1.2 * e[0], 2.9 * e[0]], [-1.2 * e[1], 2.9 * e[1]], color=fs.GRAY, lw=3.5, solid_capstyle='round', zorder=1)
    fs.dot(ax, (0, 0), r=0.06)
    ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=45, theta2=150, color=fs.BLACK, lw=0.9))
    a1 = np.radians(150); a0 = np.radians(142)
    fs.arrow(ax, (0.45 * np.cos(a0), 0.45 * np.sin(a0)), (0.45 * np.cos(a1), 0.45 * np.sin(a1)), ms=8, lw=0.9)
    ax.text(-0.3, 0.55, r'$\omega$', fontsize=10)
    r = 1.6; B = r * e
    ax.add_patch(Circle(tuple(B), 0.12, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=5))
    ax.text(r / 2 * e[0] + 0.1, r / 2 * e[1] - 0.2, r'$r$', fontsize=10)
    fs.vec(ax, tuple(B - t * 0.25), tuple(e * 0.5), color=fs.VEL, lw=1.3, ms=8)
    q = B - t * 0.25 + e * 0.5
    ax.text(q[0] + 0.05, q[1] - 0.2, r"$\vec v\,'$", color=fs.VEL, fontsize=9)
    ax.text(-1.6, 2.55, '위에서 본 그림(회전 기준틀)', fontsize=7.5)
    fs.save(fig, __file__, 'fig06_14')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
        f()
