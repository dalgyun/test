"""33장 간섭 그림."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Arc

RAY = fs.ORANGE
GLASS = '#dbe7f3'
WAVE = fs.VEL


def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def arc2(ax, center, r, a1, a2, text=None, **kw):
    diff = (a2 - a1) % 360
    if diff > 180:
        a1, diff = a2, 360 - diff
    fs.angle_arc(ax, center, r, a1, a1 + diff, text, **kw)


def darrow(ax, p, q, text=None, tpos=None, color=fs.GRAY, fontsize=10, **kw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>', mutation_scale=7, color=color, lw=0.7))
    if text:
        tp = tpos if tpos is not None else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        fs.label(ax, tp, text, fontsize=fontsize, color=color, **kw)


# ---------- 그림 33.1 하위헌스 원리 ----------
def fig01():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.0, 2.5))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    # (가) 평면파
    ax = axs[0]; ax.set_xlim(-0.4, 3.0); ax.set_ylim(-1.5, 1.5)
    R = 0.9
    ys = np.linspace(-1.2, 1.2, 7)
    ax.plot([0, 0], [-1.35, 1.35], color=WAVE, lw=1.6)
    for y in ys:
        fs.dot(ax, (0, y), r=0.035, color=WAVE)
        ax.add_patch(Arc((0, y), 2 * R, 2 * R, theta1=-90, theta2=90, color=WAVE, lw=0.7, ls='--'))
    ax.plot([R, R], [-1.35, 1.35], color=WAVE, lw=1.6)
    fs.arrow(ax, (1.25, 0.3), (2.1, 0.3), color=fs.BLACK, lw=1.2)
    fs.label(ax, (0, -1.5), r'$t$', fontsize=10)
    fs.label(ax, (R, -1.5), r'$t + \Delta t$', fontsize=10)
    darrow(ax, (0, 1.05), (R, 1.05), r'$v\Delta t$', tpos=(R / 2 + 0.05, 1.3), fontsize=9)
    ax.set_title('(가) 평면파', fontsize=9)
    # (나) 구면파
    ax = axs[1]; ax.set_xlim(-0.5, 2.9); ax.set_ylim(-1.5, 1.5)
    S = np.array([-0.4, 0.0]); r0 = 1.0; R = 0.6
    th = np.linspace(-55, 55, 7)
    ax.add_patch(Arc(S, 2 * r0, 2 * r0, theta1=-65, theta2=65, color=WAVE, lw=1.6))
    ax.add_patch(Arc(S, 2 * (r0 + R), 2 * (r0 + R), theta1=-60, theta2=60, color=WAVE, lw=1.6))
    for t in np.radians(th):
        c = S + r0 * np.array([np.cos(t), np.sin(t)])
        fs.dot(ax, c, r=0.035, color=WAVE)
        ax.add_patch(Arc(c, 2 * R, 2 * R, theta1=np.degrees(t) - 90, theta2=np.degrees(t) + 90, color=WAVE,
                         lw=0.7, ls='--'))
    fs.dot(ax, S, r=0.05)
    fs.label(ax, (S[0], S[1] - 0.22), '파원', fontsize=8)
    ax.set_title('(나) 구면파', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig33_01')


# ---------- 그림 33.2 하위헌스 원리로 본 굴절 ----------
def fig02():
    fig, ax = fs.canvas(4.2, 3.2, xlim=(-0.6, 3.4), ylim=(-1.9, 1.6))
    v1, v2 = 1.0, 0.62
    th1 = np.radians(50)
    AC = 2.4
    A = np.array([0.0, 0.0]); C = np.array([AC, 0.0])
    # 입사 파면 AB (경계면과 θ1): B는 C에서 진행 방향 반대쪽으로 v1 t
    k1 = np.array([np.sin(th1), -np.cos(th1)])          # 진행 방향
    v1t = AC * np.sin(th1)
    B = C - v1t * k1
    v2t = v1t * v2 / v1
    th2 = np.arcsin(v2t / AC)
    k2 = np.array([np.sin(th2), -np.cos(th2)])
    Dp = A + v2t * k2
    ax.add_patch(Rectangle((-0.6, -1.9), 4.0, 1.9, fc=GLASS, ec='none', zorder=0))
    ax.plot([-0.6, 3.4], [0, 0], color=fs.BLACK, lw=1.1)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=WAVE, lw=1.8)
    ax.plot([C[0], Dp[0]], [C[1], Dp[1]], color=WAVE, lw=1.8)
    ax.add_patch(Arc(A, 2 * v2t, 2 * v2t, theta1=200, theta2=360, color=WAVE, lw=0.8, ls='--'))
    # 광선
    for P0 in (A, B):
        fs.ray(ax, [P0 - 0.8 * k1, P0], color=RAY, lw=1.0)
    fs.ray(ax, [B, C], color=RAY, lw=1.0, )
    fs.ray(ax, [A, Dp], color=RAY, lw=1.0)
    ax.plot([A[0], C[0]], [A[1], C[1]], color=fs.BLACK, lw=1.1)
    ax.plot([A[0], Dp[0]], [A[1], Dp[1]], color=fs.GRAY, lw=0.6)
    for P, s, off in ((A, r'$A$', (-0.15, 0.15)), (B, r'$B$', (0.05, 0.2)), (C, r'$C$', (0.15, 0.15)),
                      (Dp, r'$D$', (-0.05, -0.22))):
        fs.dot(ax, P, r=0.04); fs.label(ax, (P[0] + off[0], P[1] + off[1]), s, fontsize=11)
    m = (B + C) / 2
    fs.label(ax, (m[0] + 0.32, m[1] + 0.12), r'$v_1t$', fontsize=10, color=RAY)
    m = (A + Dp) / 2
    fs.label(ax, (m[0] - 0.3, m[1] - 0.05), r'$v_2t$', fontsize=10, color=RAY)
    ang = lambda v: np.degrees(np.arctan2(v[1], v[0]))
    arc2(ax, A, 0.5, 0, ang(B - A), r'$\theta_1$', tr=0.7, fontsize=10)
    arc2(ax, C, 0.5, 180, ang(Dp - C), r'$\theta_2$', tr=0.72, fontsize=10)
    fs.label(ax, (3.0, 1.3), '매질 1 ($v_1$)', fontsize=8.5)
    fs.label(ax, (3.0, -1.65), '매질 2 ($v_2$)', fontsize=8.5)
    fs.save(fig, __file__, 'fig33_02')


# ---------- 그림 33.3 플라스틱 판이 만드는 위상차 (예제 33.1) ----------
def fig03():
    fig, ax = fs.canvas(5.4, 2.0, xlim=(-0.6, 4.1), ylim=(-0.75, 0.95))
    lam = 0.55; L = 2.60; n = 1.60
    x0 = 0.4
    x = np.linspace(-0.4, x0 + L + 0.5, 3000)
    # 위: 공기
    y1 = 0.48 + 0.16 * np.sin(2 * np.pi * x / lam)
    # 아래: 판 안에서 파장 lam/n
    ph = np.where(x < x0, 2 * np.pi * x / lam,
                  np.where(x < x0 + L, 2 * np.pi * x0 / lam + 2 * np.pi * n * (x - x0) / lam,
                           2 * np.pi * x0 / lam + 2 * np.pi * n * L / lam + 2 * np.pi * (x - x0 - L) / lam))
    y2 = -0.35 + 0.16 * np.sin(ph)
    ax.add_patch(Rectangle((x0, -0.62), L, 0.54, fc=GLASS, ec=fs.BLACK, lw=0.9))
    ax.plot(x, y1, color=WAVE, lw=1.1)
    ax.plot(x, y2, color=WAVE, lw=1.1)
    for xx in (x0, x0 + L):
        ax.plot([xx, xx], [-0.65, 0.75], color=fs.GRAY, lw=0.6, ls=':')
    darrow(ax, (x0, 0.82), (x0 + L, 0.82), r'$L = 2.60\ \mu\mathrm{m}$', tpos=(x0 + L / 2, 0.82), fontsize=9,
           va='bottom')
    fs.label(ax, (-0.5, 0.68), '공기', fontsize=8.5, ha='left', va='bottom')
    fs.label(ax, (x0 + L / 2, -0.7), '$n = 1.60$', fontsize=9)
    fs.label(ax, (3.72, 0.48), '4.73파장', fontsize=8, color=fs.GRAY)
    fs.label(ax, (3.72, -0.35), '7.56파장', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig33_03')


# ---------- 그림 33.4 영의 이중 슬릿 장치 ----------
def fig04():
    fig, ax = fs.canvas(5.2, 2.6, xlim=(-0.4, 6.6), ylim=(-1.75, 1.75))
    # 광원, 단일 슬릿, 이중 슬릿, 스크린
    fs.dot(ax, (0, 0), r=0.08, color=fs.ORANGE)
    fs.label(ax, (0, -0.35), '광원', fontsize=8)
    def barrier(x, gaps, h=1.5, w=0.06):
        edges = [-h] + [g for c in sorted(gaps) for g in (c - 0.045, c + 0.045)] + [h]
        for a, b in zip(edges[0::2], edges[1::2]):
            ax.add_patch(Rectangle((x - w / 2, a), w, b - a, fc=fs.BLACK, ec='none'))
    barrier(0.8, [0.0])
    d = 0.5
    barrier(2.0, [d / 2, -d / 2])
    # 파면
    for r in np.arange(0.25, 1.2, 0.3):
        ax.add_patch(Arc((0.8, 0), 2 * r, 2 * r, theta1=-50, theta2=50, color=WAVE, lw=0.6))
    for c in (d / 2, -d / 2):
        for r in np.arange(0.25, 3.8, 0.3):
            ax.add_patch(Arc((2.0, c), 2 * r, 2 * r, theta1=-40, theta2=40, color=WAVE, lw=0.4, alpha=0.6))
    # 스크린과 무늬
    xs = 5.6
    ax.add_patch(Rectangle((xs, -1.55), 0.08, 3.1, fc='#cccccc', ec=fs.BLACK, lw=0.8))
    y = np.linspace(-1.55, 1.55, 400)
    Lr = xs - 2.0; lam = 0.09
    I = np.cos(np.pi * d * (y / np.hypot(Lr, y)) / lam) ** 2
    for yi, Ii in zip(y[:-1], I[:-1]):
        ax.add_patch(Rectangle((xs + 0.25, yi), 0.3, y[1] - y[0], fc=str(1 - 0.9 * Ii), ec='none'))
    ax.add_patch(Rectangle((xs + 0.25, -1.55), 0.3, 3.1, fc='none', ec=fs.BLACK, lw=0.6))
    fs.label(ax, (0.8, 1.65), '단일 슬릿', fontsize=8)
    fs.label(ax, (2.0, 1.65), '이중 슬릿', fontsize=8)
    fs.label(ax, (xs, 1.68), '스크린', fontsize=8)
    darrow(ax, (2.0, -1.65), (xs, -1.65), r'$L$', tpos=((2.0 + xs) / 2, -1.5), fontsize=10)
    darrow(ax, (1.72, -d / 2), (1.72, d / 2), r'$d$', tpos=(1.55, 0), fontsize=10)
    fs.save(fig, __file__, 'fig33_04')


# ---------- 그림 33.5 경로차 d sin(theta) ----------
def fig05():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.4, 2.7), gridspec_kw=dict(width_ratios=[1.0, 1.25]))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
    # (가) 전체 배치
    ax = axs[0]; ax.set_xlim(-0.4, 4.2); ax.set_ylim(-1.0, 2.6)
    d = 0.6; Lr = 3.6
    S1 = np.array([0, d / 2]); S2 = np.array([0, -d / 2])
    th = np.radians(25)
    P = np.array([Lr, Lr * np.tan(th)])
    ax.plot([Lr, Lr], [-0.9, 2.4], color=fs.BLACK, lw=1.2)
    for a, b in ((-0.9, -d / 2 - 0.05), (-d / 2 + 0.05, d / 2 - 0.05), (d / 2 + 0.05, 1.2)):
        ax.add_patch(Rectangle((-0.04, a), 0.08, b - a, fc=fs.BLACK, ec='none'))
    ax.plot([0, Lr], [0, 0], color=fs.GRAY, lw=0.6, ls='--')
    ax.plot([0, P[0]], [0, P[1]], color=fs.GRAY, lw=0.6, ls='--')
    fs.ray(ax, [S1, P], color=RAY, lw=1.0, arrows=False); fs.ray(ax, [S2, P], color=RAY, lw=1.0, arrows=False)
    arc2(ax, (0, 0), 1.2, 0, 25, r'$\theta$', tr=1.4, fontsize=10)
    fs.dot(ax, P, r=0.05); fs.label(ax, (P[0] + 0.2, P[1]), r'$P$', fontsize=11)
    fs.label(ax, (1.6, 1.25), r'$r_1$', fontsize=10, color=RAY)
    fs.label(ax, (2.0, 0.55), r'$r_2$', fontsize=10, color=RAY)
    darrow(ax, (Lr + 0.18, 0), (Lr + 0.18, P[1]), r'$y$', tpos=(Lr + 0.38, P[1] / 2))
    darrow(ax, (0, -0.75), (Lr, -0.75), r'$L$', tpos=(Lr / 2, -0.93))
    fs.label(ax, (-0.25, d / 2), r'$S_1$', fontsize=9); fs.label(ax, (-0.25, -d / 2), r'$S_2$', fontsize=9)
    ax.set_title('(가) $L \\gg d$이면 두 광선은 거의 평행', fontsize=9)
    # (나) 슬릿 근처 확대
    ax = axs[1]; ax.set_xlim(-0.9, 3.3); ax.set_ylim(-1.5, 2.1)
    d = 1.6
    S1 = np.array([0, d / 2]); S2 = np.array([0, -d / 2])
    u = np.array([np.cos(th), np.sin(th)])
    for a, b in ((-1.45, -d / 2 - 0.08), (-d / 2 + 0.08, d / 2 - 0.08), (d / 2 + 0.08, 2.0)):
        ax.add_patch(Rectangle((-0.06, a), 0.12, b - a, fc=fs.BLACK, ec='none'))
    for S in (S1, S2):
        fs.ray(ax, [S, S + 3.1 * u], color=RAY, lw=1.3)
    # S1에서 S2 광선에 내린 수선의 발
    foot = S2 + np.dot(S1 - S2, u) * u
    ax.plot([S1[0], foot[0]], [S1[1], foot[1]], color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([S2[0], foot[0]], [S2[1], foot[1]], color=fs.FORCE, lw=3.0, solid_capstyle='butt', zorder=5)
    fs.label(ax, (1.75, -1.2), r'$\Delta r = d\sin\theta$', fontsize=10, color=fs.FORCE)
    darrow(ax, (-0.35, -d / 2), (-0.35, d / 2), r'$d$', tpos=(-0.55, 0))
    # theta at S2 between screen-normal (가로) and ray; also at S1 between slit plane and perpendicular
    ax.plot([0, 1.6], [-d / 2, -d / 2], color=fs.GRAY, lw=0.6, ls=':')
    arc2(ax, S2, 0.9, 0, 25, r'$\theta$', tr=1.1, fontsize=10)
    arc2(ax, S1, 0.55, -90, -90 + 25, r'$\theta$', tr=0.75, fontsize=10)
    fs.label(ax, (0.3, d / 2 + 0.2), r'$S_1$', fontsize=9); fs.label(ax, (0.3, -d / 2 - 0.25), r'$S_2$', fontsize=9)
    ax.set_title('(나) 슬릿 근처 확대', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig33_05')


# ---------- 그림 33.6 페이저 합 ----------
def fig06():
    fig, ax = fs.canvas(3.4, 2.0, xlim=(-0.3, 2.4), ylim=(-0.3, 1.15))
    phi = np.radians(60)
    O = np.array([0, 0]); A = np.array([1.0, 0]); B = A + np.array([np.cos(phi), np.sin(phi)])
    fs.arrow(ax, O, A, color=fs.VEL, lw=1.6, ms=10)
    fs.arrow(ax, A, B, color=fs.VEL, lw=1.6, ms=10)
    fs.arrow(ax, O, B, color=fs.FORCE, lw=1.8, ms=11)
    ax.plot([A[0], A[0] + 0.7], [0, 0], color=fs.GRAY, lw=0.6, ls='--')
    arc2(ax, A, 0.35, 0, 60, r'$\phi$', tr=0.5, fontsize=10)
    arc2(ax, O, 0.55, 0, 30, r'$\phi/2$', tr=0.85, fontsize=9)
    fs.label(ax, (0.5, -0.15), r'$E_0$', fontsize=10, color=fs.VEL)
    fs.label(ax, (1.6, 0.55), r'$E_0$', fontsize=10, color=fs.VEL)
    fs.label(ax, (0.55, 0.65), r'$2E_0\cos\frac{\phi}{2}$', fontsize=10, color=fs.FORCE, ha='right')
    fs.save(fig, __file__, 'fig33_06')


# ---------- 그림 33.7 이중 슬릿 세기 분포 (예제 33.2, 33.4) ----------
def fig07():
    fig, ax = fs.plot_axes(4.4, 2.5)
    dy = 2.5   # mm
    y = np.linspace(-7.5, 7.5, 2001)
    I = np.cos(np.pi * y / dy) ** 2
    ax.plot(y, 4 * I, color=fs.VEL, lw=1.5)
    ax.axhline(2, color=fs.GRAY, lw=0.9, ls='--')
    ax.text(7.7, 2.0, r'평균 $2I_0$', fontsize=8.5, color=fs.GRAY, ha='left', va='center', clip_on=False)
    ax.axhline(1, xmin=0, xmax=0, color='none')
    # 반치폭
    ax.annotate('', xy=(-dy / 4, 2), xytext=(dy / 4, 2),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.FORCE, lw=0.9, mutation_scale=8))
    ax.text(0, 1.8, '반치폭', fontsize=8, color=fs.FORCE, ha='center', va='top')
    ax.annotate('', xy=(0, 4.35), xytext=(dy, 4.35),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=8))
    ax.text(dy / 2, 4.45, r'$\Delta y = 2.5$ mm', fontsize=8.5, ha='center', va='bottom')
    ax.set_xlim(-7.5, 7.5); ax.set_ylim(0, 5.0)
    ax.set_yticks([0, 1, 2, 3, 4]); ax.set_yticklabels(['0', r'$I_0$', r'$2I_0$', r'$3I_0$', r'$4I_0$'])
    ax.set_xlabel(r'스크린 위의 위치 $y$ (mm)', fontsize=9)
    ax.set_ylabel(r'세기 $I$', fontsize=9)
    fs.save(fig, __file__, 'fig33_07')


# ---------- 그림 33.8 박막의 두 반사광 ----------
def fig08():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.4, 2.6))
    cases = [('(가) 공기 속 비누막', 1.00, 1.33, 1.00, ('$\\pi$ 변화', '변화 없음')),
             ('(나) 유리 위 MgF$_2$ 코팅', 1.00, 1.38, 1.52, ('$\\pi$ 변화', '$\\pi$ 변화'))]
    for ax, (title, n1, n2, n3, ph) in zip(axs, cases):
        ax.set_xlim(-0.2, 3.2); ax.set_ylim(-1.45, 1.65); ax.set_aspect('equal'); ax.axis('off')
        Lt = 0.75
        ax.add_patch(Rectangle((-0.2, -Lt), 3.4, Lt, fc='#e9f1f8', ec='none'))
        ax.add_patch(Rectangle((-0.2, -1.45), 3.4, 1.45 - Lt, fc='#cfdcea' if n3 > 1 else 'white', ec='none'))
        ax.plot([-0.2, 3.2], [0, 0], color=fs.BLACK, lw=1.0)
        ax.plot([-0.2, 3.2], [-Lt, -Lt], color=fs.BLACK, lw=1.0)
        th = np.radians(14)
        thi = np.arcsin(np.sin(th) / n2)
        P0 = np.array([0.8, 0.0])
        inc = P0 + 1.4 * np.array([-np.sin(th), np.cos(th)])
        P1 = P0 + np.array([Lt * np.tan(thi), -Lt])
        P2 = P1 + np.array([Lt * np.tan(thi), Lt])
        r1 = P0 + 1.4 * np.array([np.sin(th), np.cos(th)])
        r2 = P2 + 1.4 * np.array([np.sin(th), np.cos(th)])
        fs.ray(ax, [inc, P0, r1], color=RAY, lw=1.3)
        fs.ray(ax, [P0, P1, P2, r2], color=RAY, lw=1.0)
        fs.ray(ax, [P1, P1 + 0.65 * np.array([np.sin(th), -np.cos(th)])], color=RAY, lw=0.7, ls='-')
        fs.label(ax, (r1[0] - 0.12, r1[1] + 0.12), '1', fontsize=9)
        fs.label(ax, (r2[0] + 0.05, r2[1] + 0.12), '2', fontsize=9)
        fs.label(ax, (2.75, 0.3), f'$n_1 = {n1:.2f}$', fontsize=8.5)
        fs.label(ax, (2.75, -Lt / 2), f'$n_2 = {n2:.2f}$', fontsize=8.5)
        fs.label(ax, (2.75, -1.1), f'$n_3 = {n3:.2f}$', fontsize=8.5)
        fs.label(ax, (P0[0] - 0.5, 0.18), ph[0], fontsize=8, color=fs.FORCE)
        fs.label(ax, (P1[0] - 0.75, -Lt - 0.25), ph[1], fontsize=8, color=fs.FORCE)
        ax.add_patch(FancyArrowPatch((0.1, 0), (0.1, -Lt), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
        fs.label(ax, (0.25, -Lt / 2), r'$L$', fontsize=10, color=fs.GRAY)
        ax.set_title(title, fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig33_08')


# ---------- 그림 33.9 공기 쐐기 ----------
def fig09():
    fig, axs = fs.plt.subplots(2, 1, figsize=(4.8, 2.9), gridspec_kw=dict(height_ratios=[1.75, 1]))
    ax = axs[0]
    ax.set_xlim(-0.3, 5.4); ax.set_ylim(-0.8, 1.15); ax.axis('off')
    ell = 5.0; Dw = 0.32; tg = 0.18
    ax.add_patch(Polygon([(0, 0), (ell, 0), (ell, -tg), (0, -tg)], fc=GLASS, ec=fs.BLACK, lw=0.9))
    ax.add_patch(Polygon([(0, 0), (ell, Dw), (ell, Dw + tg), (0, tg)], fc=GLASS, ec=fs.BLACK, lw=0.9))
    ax.add_patch(Circle((ell - Dw / 2, Dw / 2), Dw / 2, fc=fs.GRAY, ec=fs.BLACK, lw=0.7))
    x = 3.0; t = Dw * x / ell
    ax.plot([x, x], [0, t], color=fs.FORCE, lw=1.4)
    fs.label(ax, (x + 0.15, t / 2 - 0.0), r'$t$', fontsize=10, color=fs.FORCE)
    for xx in np.linspace(0.6, 4.2, 5):
        fs.arrow(ax, (xx, 1.05), (xx, 0.45), color=RAY, lw=1.0, ms=8)
    ax.add_patch(FancyArrowPatch((0, -0.38), (x, -0.38), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (x / 2, -0.5), r'$x$', fontsize=10, color=fs.GRAY)
    fs.label(ax, (ell + 0.25, Dw / 2), r'$D$', fontsize=10)
    ax.add_patch(FancyArrowPatch((0, -0.62), (ell, -0.62), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (ell / 2, -0.74), r'$\ell$', fontsize=10, color=fs.GRAY)
    ax.set_title('(가) 옆에서 본 모습 (두께는 크게 과장)', fontsize=9)
    # (나) 위에서 본 무늬: 반사광 어두운 무늬 2t = m lambda
    ax = axs[1]
    ax.set_xlim(-0.3, 5.4); ax.set_ylim(-0.1, 0.75); ax.axis('off')
    xs = np.linspace(0, ell, 1000)
    lam_eff = 0.56   # 무늬 간격 lambda*ell/(2D)를 그림 단위로
    I = np.sin(np.pi * xs / lam_eff) ** 2      # x=0에서 어두움
    for xa, xb, Ii in zip(xs[:-1], xs[1:], I[:-1]):
        ax.add_patch(Rectangle((xa, 0.05), xb - xa, 0.4, fc=str(0.1 + 0.85 * Ii), ec='none'))
    ax.add_patch(Rectangle((0, 0.05), ell, 0.4, fc='none', ec=fs.BLACK, lw=0.6))
    darrow(ax, (lam_eff * 2, 0.55), (lam_eff * 3, 0.55), r'$\Delta x$', tpos=(lam_eff * 2.5, 0.68), fontsize=9)
    ax.set_title('(나) 위에서 본 반사광 무늬', fontsize=9, pad=2)
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, __file__, 'fig33_09')


# ---------- 그림 33.10 뉴턴 고리 ----------
def fig10():
    fig, axs = fs.plt.subplots(1, 2, figsize=(5.0, 2.4), gridspec_kw=dict(width_ratios=[1.4, 1]))
    ax = axs[0]
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-0.5, 2.0); ax.set_aspect('equal'); ax.axis('off')
    R = 4.0
    ax.add_patch(Rectangle((-2.2, -0.35), 4.4, 0.35, fc=GLASS, ec=fs.BLACK, lw=0.9))
    xx = np.linspace(-1.9, 1.9, 200)
    yy = R - np.sqrt(R ** 2 - xx ** 2)
    ax.fill_between(xx, yy, 1.1, color=GLASS, lw=0)
    ax.plot(xx, yy, color=fs.BLACK, lw=0.9); ax.plot([-1.9, 1.9], [1.1, 1.1], color=fs.BLACK, lw=0.9)
    ax.plot([-1.9, -1.9], [yy[0], 1.1], color=fs.BLACK, lw=0.9); ax.plot([1.9, 1.9], [yy[-1], 1.1], color=fs.BLACK, lw=0.9)
    r = 1.3; t = R - np.sqrt(R ** 2 - r ** 2)
    ax.plot([r, r], [0, t], color=fs.FORCE, lw=1.4)
    fs.label(ax, (r + 0.18, t / 2 + 0.02), r'$t$', fontsize=10, color=fs.FORCE)
    ax.add_patch(FancyArrowPatch((0, -0.2), (r, -0.2), arrowstyle='<|-|>', mutation_scale=7, color=fs.GRAY, lw=0.7))
    fs.label(ax, (r / 2, -0.43), r'$r$', fontsize=10, color=fs.GRAY)
    ax.plot([0, 0], [0, 1.9], color=fs.GRAY, lw=0.6, ls='-.')
    fs.label(ax, (0.25, 1.65), r'$R$ (곡률 반지름)', fontsize=8.5, ha='left', color=fs.GRAY)
    for x0 in (-1.2, -0.5, 0.5):
        fs.arrow(ax, (x0, 1.95), (x0, 1.25), color=RAY, lw=1.0, ms=8)
    ax.set_title('(가) 옆에서 본 모습 (곡률은 과장)', fontsize=9)
    ax = axs[1]
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect('equal'); ax.axis('off')
    n = 600
    g = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(g, g)
    rr2 = X ** 2 + Y ** 2
    I = np.sin(np.pi * rr2 / 0.09) ** 2       # 어두운 고리 r_m^2 = m*0.09 (sqrt(m) 간격)
    I[rr2 > 1] = np.nan
    ax.imshow(I, extent=(-1, 1, -1, 1), cmap='gray', vmin=-0.1, vmax=1.05, origin='lower')
    ax.set_title('(나) 위에서 본 고리 무늬', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig33_10')


# ---------- 그림 33.11 마이컬슨 간섭계 ----------
def fig11():
    fig, ax = fs.canvas(4.0, 3.3, xlim=(-2.4, 3.2), ylim=(-2.1, 2.5))
    BS = np.array([0.0, 0.0])
    # 빔 분할기
    ax.plot([-0.35, 0.35], [-0.35, 0.35], color=fs.VEL, lw=3.0, alpha=0.6)
    fs.label(ax, (0.55, -0.35), '빔 분할기', fontsize=8, ha='left')
    # 거울
    M1x, M2y = 2.6, 2.0
    ax.add_patch(Rectangle((M1x, -0.5), 0.1, 1.0, fc=fs.GRAY, ec=fs.BLACK))
    ax.add_patch(Rectangle((-0.5, M2y), 1.0, 0.1, fc=fs.GRAY, ec=fs.BLACK))
    fs.label(ax, (M1x + 0.35, 0.55), r'$M_1$', fontsize=11)
    fs.label(ax, (0.75, M2y + 0.2), r'$M_2$', fontsize=11)
    # 광원
    ax.add_patch(Rectangle((-2.3, -0.2), 0.45, 0.4, fc=fs.ORANGE, ec=fs.BLACK, lw=0.8))
    fs.label(ax, (-2.08, -0.42), '광원', fontsize=8)
    off = 0.06
    fs.ray(ax, [(-1.85, 0), BS], color=RAY, lw=1.3)
    fs.ray(ax, [(0, off), (M1x, off)], color=RAY, lw=1.1)
    fs.ray(ax, [(M1x, -off), (0, -off)], color=RAY, lw=1.1)
    fs.ray(ax, [(-off, 0), (-off, M2y)], color=fs.FORCE, lw=1.1)
    fs.ray(ax, [(off, M2y), (off, 0)], color=fs.FORCE, lw=1.1)
    fs.ray(ax, [(0.0, -0.05), (0.0, -1.6)], color=fs.FIELD, lw=1.4)
    ax.add_patch(Rectangle((-0.35, -1.95), 0.7, 0.3, fc='#555555', ec=fs.BLACK))
    fs.label(ax, (0.55, -1.8), '검출기(스크린)', fontsize=8, ha='left')
    darrow(ax, (0, -0.75), (M1x, -0.75), r'$d_1$', tpos=(M1x / 2, -0.95))
    darrow(ax, (-0.75, 0), (-0.75, M2y), r'$d_2$', tpos=(-0.95, M2y / 2))
    fs.arrow(ax, (M1x + 0.25, -0.75), (M1x + 0.65, -0.75), color=fs.GRAY, lw=0.9, style='<|-|>', ms=7)
    fs.label(ax, (M1x + 0.45, -0.95), '이동', fontsize=8, color=fs.GRAY)
    fs.save(fig, __file__, 'fig33_11')


# ---------- 그림 33.12 로이드 거울 (연습문제 13) ----------
def fig12():
    fig, ax = fs.canvas(4.8, 2.4, xlim=(-0.5, 6.2), ylim=(-1.4, 2.0))
    a = 0.8
    S = np.array([0.0, a]); Sp = np.array([0.0, -a])
    ax.add_patch(Rectangle((0.6, -0.12), 4.0, 0.12, fc='#d8dde3', ec=fs.BLACK, lw=0.9))
    ax.plot([0, 5.8], [0, 0], color=fs.GRAY, lw=0.5, ls=':')
    Xs = 5.8
    ax.plot([Xs, Xs], [-0.2, 1.9], color=fs.BLACK, lw=1.3)
    P = np.array([Xs, 1.3])
    # 반사점: S'에서 P로 가는 직선이 y = 0과 만나는 점
    t = (0 - Sp[1]) / (P[1] - Sp[1]); Q = Sp + t * (P - Sp)
    fs.ray(ax, [S, P], color=RAY, lw=1.2)
    fs.ray(ax, [S, Q, P], color=fs.VEL, lw=1.2)
    ax.plot([Sp[0], Q[0]], [Sp[1], Q[1]], color=fs.VEL, lw=0.8, ls='--')
    fs.dot(ax, S, r=0.06); fs.label(ax, (-0.25, a), r'$S$', fontsize=11)
    ax.add_patch(Circle(Sp, 0.06, fc='white', ec=fs.BLACK, zorder=6)); fs.label(ax, (-0.25, -a), r"$S'$", fontsize=11)
    darrow(ax, (-0.15, 0), (-0.15, a), None)
    fs.label(ax, (0.12, a / 2), r'$a$', fontsize=10, color=fs.GRAY)
    darrow(ax, (-0.15, 0), (-0.15, -a), None)
    fs.label(ax, (0.12, -a / 2), r'$a$', fontsize=10, color=fs.GRAY)
    fs.dot(ax, P, r=0.05); fs.label(ax, (Xs + 0.2, P[1]), r'$P$', fontsize=11)
    fs.label(ax, (2.6, -0.35), '거울', fontsize=8.5)
    fs.label(ax, (Xs, 1.95), '스크린', fontsize=8.5, va='bottom')
    darrow(ax, (0, -1.2), (Xs, -1.2), r'$L$', tpos=(Xs / 2, -1.05))
    fs.save(fig, __file__, 'fig33_12')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12]:
        f()
