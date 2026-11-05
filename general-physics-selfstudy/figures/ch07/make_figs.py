import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
"""7장 일과 운동에너지 그림."""
import numpy as np
from matplotlib.patches import Polygon, Circle, Arc, Rectangle, FancyArrowPatch

F = __file__
D2R = np.pi / 180


def wsub(ax, p, main, sub, color=fs.BLACK, fontsize=10):
    """수식 기호에 한글 아래첨자를 붙인다(mathtext는 한글을 못 쓰므로 글자 두 개로 나눈다)."""
    t = ax.text(p[0], p[1], main, color=color, fontsize=fontsize, ha='right', va='baseline')
    ax.text(p[0], p[1] - 0.012 * fontsize * 0, sub, color=color, fontsize=fontsize * 0.7, ha='left', va='top')
    return t


def u(ang):
    """각 ang(도) 방향 단위벡터."""
    return np.array([np.cos(ang * D2R), np.sin(ang * D2R)])


# ---------------------------------------------------------------- 그림 7.1 일의 정의
def fig01():
    fig, ax = fs.canvas(4.4, 2.2, xlim=(-0.3, 5.6), ylim=(-0.85, 2.2))
    fs.ground(ax, -0.3, 5.6, 0)
    c0 = np.array([1.0, 0.35])
    c1 = np.array([4.4, 0.35])
    fs.block(ax, c0, 0.9, 0.7)
    ax.add_patch(Rectangle((c1[0] - 0.45, 0), 0.9, 0.7, fc='none', ec=fs.GRAY, ls='--', lw=1.0))
    phi = 35
    Fv = 1.9 * u(phi)
    fs.vec(ax, c0, Fv, color=fs.FORCE, lw=2)
    fs.label(ax, c0 + Fv + (0.15, 0.12), r'$\vec{F}$', color=fs.FORCE, fontsize=12)
    # 성분
    ax.plot([c0[0] + Fv[0]] * 2, [c0[1], c0[1] + Fv[1]], color=fs.FORCE, ls=':', lw=0.9)
    fs.arrow(ax, c0, (c0[0] + Fv[0], c0[1]), color=fs.FORCE, lw=1.1, ls='--', ms=9)
    fs.label(ax, (c0[0] + Fv[0] + 0.55, c0[1] - 0.02), r'$F\cos\phi$', color=fs.FORCE, fontsize=10)
    fs.angle_arc(ax, c0, 0.6, 0, phi, r'$\phi$', tr=0.8)
    # 변위
    fs.arrow(ax, (c0[0], -0.5), (c1[0], -0.5), lw=1.6)
    fs.label(ax, ((c0[0] + c1[0]) / 2, -0.72), r'$\Delta\vec{r}$', fontsize=12)
    for x in (c0[0], c1[0]):
        ax.plot([x, x], [-0.38, -0.6], color=fs.BLACK, lw=0.7)
    fs.label(ax, (c1[0], 1.0), '나중', fontsize=9, color=fs.GRAY)
    fs.label(ax, (c0[0] - 0.05, 1.0), '처음', fontsize=9, color=fs.GRAY)
    fs.save(fig, F, 'fig07_01')


# ---------------------------------------------------------------- 그림 7.2 일의 부호
def fig02():
    fig, ax = fs.canvas(5.4, 1.9, xlim=(-0.2, 9.4), ylim=(-1.05, 1.95))
    cases = [(40, r'$0\leq\phi<90^{\circ}$', r'$W>0$'),
             (90, r'$\phi=90^{\circ}$', r'$W=0$'),
             (140, r'$90^{\circ}<\phi\leq180^{\circ}$', r'$W<0$')]
    for k, (phi, t1, t2) in enumerate(cases):
        o = np.array([0.9 + 3.15 * k, 0.0])
        fs.arrow(ax, o, o + (1.8, 0), lw=1.6)
        fs.label(ax, o + (1.95, -0.22), r'$\Delta\vec{r}$', fontsize=11)
        Fv = 1.5 * u(phi)
        fs.vec(ax, o, Fv, color=fs.FORCE, lw=1.8)
        fs.label(ax, o + Fv * 1.13 + (0.12, 0.05), r'$\vec{F}$', color=fs.FORCE, fontsize=11)
        if phi == 90:
            ax.plot([o[0] + 0.18, o[0] + 0.18, o[0]], [0, 0.18, 0.18], color=fs.BLACK, lw=0.8)
        else:
            fs.angle_arc(ax, o, 0.42, 0, phi, r'$\phi$', tr=0.62)
        fs.dot(ax, o, r=0.06)
        fs.label(ax, o + (0.9, -0.55), t1, fontsize=9.5)
        fs.label(ax, o + (0.9, -0.88), t2, fontsize=10.5)
    fs.save(fig, F, 'fig07_02')


# ---------------------------------------------------------------- 그림 7.3 예제 7.1 빗면 FBD
def fig03():
    th = 30
    fig, ax = fs.canvas(4.4, 2.9, xlim=(-0.3, 6.3), ylim=(-0.4, 4.0))
    fs.incline(ax, (0, 0), 6.0, th, show_angle=False)
    fs.angle_arc(ax, (0, 0), 0.7, 0, th, r'$30^{\circ}$', tr=1.1, fontsize=9)
    t, n = u(th), u(th + 90)
    s0 = 2.2                                # 상자 위치(빗면을 따라)
    h = 0.6
    c = s0 * t + n * h / 2
    fs.block(ax, c, 0.9, h, angle=th)
    fs.label(ax, c - t * 0.22 + n * 0.08, r'$m$', fontsize=11, zorder=9)
    # 힘
    fs.vec(ax, c + t * 0.45, t * 1.35, color=fs.FORCE, lw=2)
    fs.label(ax, c + t * 1.95 + n * 0.12, r'$\vec{F}$', color=fs.FORCE)
    fs.vec(ax, c, (0, -1.25), color=fs.FORCE, lw=2)
    fs.label(ax, c + (0.38, -1.15), r'$m\vec{g}$', color=fs.FORCE)
    fs.vec(ax, c + n * h / 2, n * 0.95, color=fs.FORCE, lw=2)
    fs.label(ax, c + n * (h / 2 + 1.12), r'$\vec{N}$', color=fs.FORCE)
    fs.vec(ax, c - t * 0.45 - n * 0.2, -t * 0.7, color=fs.FORCE, lw=2)
    fs.label(ax, c - t * 1.3 - n * 0.05, r'$\vec{f}_k$', color=fs.FORCE)
    # 중력과 변위의 각 120°
    fs.angle_arc(ax, c, 0.42, -90, th, r'$120^{\circ}$', tr=0.62, fontsize=9)
    # 변위 d
    p0 = s0 * t + n * (h + 0.95)
    fs.arrow(ax, p0 - t * 0.1 + n * 0.0 + t * 0.6, p0 + t * 2.0 + t * 0.6, lw=1.4)
    fs.label(ax, p0 + t * 1.2 + n * 0.5, r'$d=5.0\ \mathrm{m}$', fontsize=10)
    fs.save(fig, F, 'fig07_03')


# ---------------------------------------------------------------- 그림 7.4 예제 7.2 벡터
def fig04():
    fig, ax = fs.plot_axes(3.6, 3.2)
    A, B = np.array([1.0, 2.0]), np.array([4.0, -2.0])
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(-2.8, 4.8); ax.set_aspect('equal')
    ax.axhline(0, color=fs.BLACK, lw=0.8); ax.axvline(0, color=fs.BLACK, lw=0.8)
    ax.set_xlabel(r'$x$ (m)'); ax.set_ylabel(r'$y$ (m)')
    fs.arrow(ax, A, B, lw=1.8)
    fs.label(ax, (A + B) / 2 + (0.5, 0.2), r'$\Delta\vec{r}$', fontsize=12)
    Fd = np.array([3.0, 4.0]) * 0.5
    fs.vec(ax, A, Fd, color=fs.FORCE, lw=2)
    fs.label(ax, A + Fd + (0.15, 0.25), r'$\vec{F}=(3.0\hat{i}+4.0\hat{j})\ \mathrm{N}$', color=fs.FORCE,
             fontsize=9, ha='center')
    a1 = np.degrees(np.arctan2(-4, 3)); a2 = np.degrees(np.arctan2(4, 3))
    fs.angle_arc(ax, A, 0.55, a1, a2, r'$106^{\circ}$', fontsize=9, tr=0.95)
    fs.dot(ax, A, r=0.07); fs.dot(ax, B, r=0.07)
    fs.label(ax, A + (-0.12, 0.42), r'$(1.0,\,2.0)$', fontsize=9, ha='right', bbox=dict(fc='white', ec='none', pad=0.5))
    fs.label(ax, B + (0.0, -0.4), r'$(4.0,\,-2.0)$', fontsize=9)
    fs.save(fig, F, 'fig07_04')


# ---------------------------------------------------------------- 그림 7.5 리만 합
def fig05():
    fig, ax = fs.plot_axes(4.0, 2.6)
    f = lambda x: 1.2 + 1.6 * np.exp(-((x - 2.4) / 1.3) ** 2) + 0.15 * x
    xi, xf = 0.8, 4.6
    edges = np.linspace(xi, xf, 11)
    for k, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        m = (a + b) / 2
        fc = fs.SURF if k == 6 else fs.LIGHT
        ax.add_patch(Rectangle((a, 0), b - a, f(m), fc=fc, ec=fs.VEL, lw=0.6, zorder=1))
    x = np.linspace(0, 5.4, 300)
    ax.plot(x, f(x), color=fs.FORCE, lw=1.8, zorder=3)
    ax.set_xlim(0, 5.4); ax.set_ylim(0, 3.6)
    ax.set_xticks([xi, xf]); ax.set_xticklabels([r'$x_i$', r'$x_f$'])
    ax.set_yticks([])
    ax.set_xlabel(r'$x$', loc='right'); ax.set_ylabel(r'$F(x)$')
    a, b = edges[6], edges[7]; m = (a + b) / 2
    ax.annotate('', xy=(a, -0.25), xytext=(b, -0.25), annotation_clip=False,
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(m, -0.5, r'$\Delta x$', ha='center', va='center', fontsize=10, clip_on=False)
    ax.annotate(r'$F(x_j)$', xy=(m, f(m)), xytext=(m + 0.75, f(m) + 0.45), fontsize=10, color=fs.FORCE,
                arrowprops=dict(arrowstyle='-', color=fs.FORCE, lw=0.6))
    ax.text(2.2, 0.7, r'$W\approx\sum F(x_j)\,\Delta x$', ha='center', fontsize=10, bbox=dict(fc='white', ec='none', pad=1.5), zorder=5)
    ax.grid(False)
    fs.save(fig, F, 'fig07_05')


# ---------------------------------------------------------------- 그림 7.6 예제 7.3
def fig06():
    fig, ax = fs.plot_axes(4.0, 2.8)
    f = lambda x: 6 * x ** 2 - 4 * x
    x = np.linspace(0, 3.2, 400)
    xn = np.linspace(0, 2 / 3, 100); xp = np.linspace(2 / 3, 3, 300)
    ax.fill_between(xp, f(xp), color=fs.VEL, alpha=0.18, lw=0)
    ax.fill_between(xn, f(xn), color=fs.FORCE, alpha=0.35, lw=0)
    ax.plot(x, f(x), color=fs.FORCE, lw=1.8)
    ax.axhline(0, color=fs.BLACK, lw=0.8)
    ax.axvline(3, color=fs.GRAY, lw=0.8, ls='--')
    ax.set_xlim(0, 3.25); ax.set_ylim(-5, 50)
    ax.set_xlabel(r'$x$ (m)'); ax.set_ylabel(r'$F$ (N)')
    ax.text(2.15, 12, r'$+36.3\ \mathrm{J}$', ha='center', fontsize=10, color=fs.VEL)
    ax.annotate(r'$-0.30\ \mathrm{J}$', xy=(0.35, -0.6), xytext=(0.55, 12), fontsize=10, color=fs.FORCE,
                ha='center', arrowprops=dict(arrowstyle='-', color=fs.FORCE, lw=0.7))
    ax.text(1.0, 38, r'$F(x)=6x^2-4x$', fontsize=10, color=fs.FORCE)
    ax.text(2.95, 45, r'$x=3.0$', fontsize=9, ha='right', color=fs.GRAY)
    ax.annotate(r'$x=\frac{2}{3}\ \mathrm{m}$', xy=(2 / 3, 0), xytext=(1.05, 5.5), fontsize=9.5,
                arrowprops=dict(arrowstyle='-', color=fs.BLACK, lw=0.6))
    fs.save(fig, F, 'fig07_06')


# ---------------------------------------------------------------- 그림 7.7 예제 7.4 경로
def fig07():
    fig, ax = fs.plot_axes(3.3, 3.2)
    g = np.linspace(0.1, 1.1, 6)
    X, Y = np.meshgrid(g, g)
    ax.quiver(X, Y, 2 * Y, X, color=fs.FORCE, alpha=0.35, scale=22, width=0.006, zorder=1)
    t = np.linspace(0, np.pi / 2, 100)
    ax.plot(np.cos(t), np.sin(t), color=fs.VEL, lw=2, label='(가) 사분원')
    ax.plot([1, 0], [0, 1], color=fs.ACC, lw=2, label='(나) 직선')
    ax.plot([1, 1, 0], [0, 1, 1], color=fs.ORANGE, lw=1.6, ls='--', label='꺾은선(🐍 실습)'.replace('🐍 ', ''))
    for (p, q, c) in [((np.cos(0.8), np.sin(0.8)), (np.cos(0.84), np.sin(0.84)), fs.VEL),
                      ((0.5, 0.5), (0.47, 0.53), fs.ACC), ((1, 0.5), (1, 0.53), fs.ORANGE), ((0.5, 1), (0.47, 1), fs.ORANGE)]:
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=11, color=c, lw=0, zorder=4))
    ax.plot([1, 0], [0, 1], 'o', color=fs.BLACK, ms=4, zorder=5)
    ax.text(1.03, -0.1, r'$(R,0)$', fontsize=9.5, ha='center')
    ax.text(-0.05, 1.1, r'$(0,R)$', fontsize=9.5, ha='center')
    ax.set_xlim(-0.15, 1.3); ax.set_ylim(-0.2, 1.3); ax.set_aspect('equal')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['0', r'$R$']); ax.set_yticks([0, 1]); ax.set_yticklabels(['0', r'$R$'])
    ax.set_xlabel(r'$x$'); ax.set_ylabel(r'$y$')
    ax.legend(loc='lower left', fontsize=8, framealpha=0.95)
    fs.save(fig, F, 'fig07_07')


# ---------------------------------------------------------------- 그림 7.8 용수철의 세 상태
def fig08():
    fig, ax = fs.canvas(4.4, 3.5, xlim=(-0.4, 5.6), ylim=(-0.55, 6.3))
    x0 = 2.8                    # 자연 길이일 때 블록 왼쪽 면
    rows = [(4.6, 0.0, '(가) 자연 길이: $x=0$, $F_x=0$'),
            (2.3, 0.9, '(나) 늘어남: $x>0$, $F_x<0$'),
            (0.0, -0.8, '(다) 압축: $x<0$, $F_x>0$')]
    for y, dx, txt in rows:
        fs.ground(ax, 0, 5.4, y, n=26)
        fs.wall(ax, y, y + 1.2, 0)
        xb = x0 + dx
        fs.spring(ax, (0, y + 0.3), (xb, y + 0.3), coils=9, width=0.14)
        fs.block(ax, (xb + 0.35, y + 0.3), 0.7, 0.6)
        if dx != 0:
            sgn = -np.sign(dx)
            fs.arrow(ax, (xb + 0.35, y + 0.78), (xb + 0.35 + sgn * 0.9, y + 0.78), color=fs.FORCE, lw=2, zorder=8)
            fs.label(ax, (xb + 0.35 + sgn * 1.3, y + 0.78), r'$F_x$', color=fs.FORCE, fontsize=10)
            ax.plot([xb + 0.35, xb + 0.35], [y + 0.6, y + 0.78], color=fs.FORCE, lw=0.8)
            ax.annotate('', xy=(xb, y + 1.12), xytext=(x0, y + 1.12),
                        arrowprops=dict(arrowstyle='->', color=fs.BLACK, lw=1.0, shrinkA=0, shrinkB=0))
            ax.plot([xb, xb], [y + 0.62, y + 1.2], color=fs.BLACK, lw=0.6, ls=':')
            fs.label(ax, (xb - sgn * 0.0 + (0.18 if dx > 0 else -0.18), y + 1.12), r'$x$', fontsize=10)
        fs.label(ax, (0.25, y + 1.55), txt, fontsize=9, ha='left')
    ax.plot([x0, x0], [-0.3, 6.0], color=fs.GRAY, ls='--', lw=0.8, zorder=0)
    fs.label(ax, (x0 + 0.08, -0.42), r'$x=0$', fontsize=9, color=fs.GRAY, ha='left')
    fs.save(fig, F, 'fig07_08')


# ---------------------------------------------------------------- 그림 7.9 용수철의 F-x 그래프
def fig09():
    fig, ax = fs.plot_axes(4.0, 3.0)
    k = 1.0
    xi, xf = 0.8, 2.0
    x = np.linspace(-0.3, 2.4, 100)
    ax.plot(x, k * x, color=fs.VEL, lw=1.6, ls='--')
    ax.plot(x, -k * x, color=fs.FORCE, lw=1.8)
    xs = np.linspace(xi, xf, 50)
    ax.fill_between(xs, -k * xs, color=fs.FORCE, alpha=0.25, lw=0)
    ax.fill_between(xs, k * xs, color=fs.VEL, alpha=0.15, lw=0)
    ax.axhline(0, color=fs.BLACK, lw=0.8); ax.axvline(0, color=fs.BLACK, lw=0.8)
    for xx in (xi, xf):
        ax.plot([xx, xx], [-k * xx, k * xx], color=fs.GRAY, lw=0.6, ls=':')
    ax.set_xticks([xi, xf]); ax.set_xticklabels([r'$x_i$', r'$x_f$'])
    ax.set_yticks([])
    ax.set_xlim(-0.3, 2.5); ax.set_ylim(-2.5, 2.5)
    ax.set_xlabel(r'$x$', loc='right'); ax.set_ylabel(r'$F$')
    ax.text(0.62, 1.0, r'손의 힘 $kx$', color=fs.VEL, fontsize=9.5, ha='right')
    ax.text(0.62, -1.1, r'용수철 힘 $F_x=-kx$', color=fs.FORCE, fontsize=9.5, ha='right')
    wsub(ax, (1.45, 0.5), r'$W$', '손', color=fs.VEL, fontsize=11)
    ax.text(1.42, -0.62, r'$W_s<0$', color=fs.FORCE, fontsize=10, ha='center')
    ax.text(-0.25, 2.1, r'두 넓이의 크기 $=\frac{1}{2}kx_f^2-\frac{1}{2}kx_i^2$', fontsize=9)
    ax.grid(False)
    fs.save(fig, F, 'fig07_09')


# ---------------------------------------------------------------- 그림 7.10 예제 7.5
def fig10():
    fig, ax = fs.canvas(4.4, 2.3, xlim=(-0.2, 6.0), ylim=(-0.5, 2.8))
    L0 = 2.0                                     # 자연 길이(그림 단위)
    xw = 5.8
    for y, xb, comp, txt in [(1.6, 0.9, 0.0, '충돌 직전'), (0.0, None, 0.7, '최대 압축 순간 ($v=0$)')]:
        fs.ground(ax, -0.2, xw, y, n=30)
        fs.wall(ax, y, y + 0.9, xw, side='right')
        xs = xw - L0 + comp                        # 용수철 왼쪽 끝
        fs.spring(ax, (xs, y + 0.3), (xw, y + 0.3), coils=8, width=0.13)
        if xb is None:
            xb = xs - 0.35
        fs.block(ax, (xb, y + 0.3), 0.7, 0.6, text=r'$m$', fontsize=10)
        fs.label(ax, (0.9, y + 1.0) if y > 0 else (1.3, y + 1.0), txt, fontsize=9)
        if y > 0:
            fs.arrow(ax, (xb + 0.45, y + 0.3), (xb + 1.45, y + 0.3), color=fs.VEL, lw=2)
            fs.label(ax, (xb + 1.15, y + 0.6), r'$v=2.0\ \mathrm{m/s}$', color=fs.VEL, fontsize=9.5)
    ax.plot([xw - L0] * 2, [-0.1, 2.6], color=fs.GRAY, ls='--', lw=0.8, zorder=0)
    ax.annotate('', xy=(xw - L0, 0.82), xytext=(xw - L0 + 0.7, 0.82),
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.9, shrinkA=0, shrinkB=0))
    fs.label(ax, (xw - L0 + 0.35, 1.02), r'$d$', fontsize=11)
    fs.label(ax, (2.85, -0.32), r'$k=200\ \mathrm{N/m}$,  $m=0.50\ \mathrm{kg}$', fontsize=9)
    fs.save(fig, F, 'fig07_10')


# ---------------------------------------------------------------- 그림 7.11 예제 7.7 속력-시간
def fig11():
    m, P, k = 1200.0, 6.0e4, 0.5 * 0.30 * 1.2 * 2.2
    vmax = (P / k) ** (1 / 3)
    t = np.linspace(0, 60, 600)
    v0 = np.sqrt(2 * P * t / m)
    # 저항이 있을 때: t(v) = ∫ m v dv / (P - k v^3)  (사다리꼴 누적 적분)
    vs = np.linspace(0, vmax * 0.9995, 20001)
    g = m * vs / (P - k * vs ** 3)
    ts = np.concatenate([[0], np.cumsum((g[1:] + g[:-1]) / 2 * np.diff(vs))])
    sel = ts <= 60
    fig, ax = fs.plot_axes(4.2, 2.8)
    ax.plot(t, v0, color=fs.VEL, lw=1.6, ls='--', label=r'저항 없음: $v=\sqrt{2Pt/m}$')
    ax.plot(ts[sel], vs[sel], color=fs.VEL, lw=2, label=r'저항 $kv^2$ 있음')
    ax.axhline(vmax, color=fs.GRAY, lw=1, ls=':')
    ax.text(1.5, vmax + 2.0, r'$v_{\max}=(P/k)^{1/3}=53\ \mathrm{m/s}$', fontsize=9, color=fs.GRAY)
    v1 = 100 / 3.6
    t1 = np.interp(v1, vs, ts)
    ax.axhline(v1, color=fs.ORANGE, lw=0.8, ls=':')
    ax.plot([m * v1 ** 2 / (2 * P)], [v1], 'o', color=fs.ORANGE, ms=4, zorder=5)
    ax.text(9.5, v1 - 4.8, r'$100\ \mathrm{km/h}$, $t=7.7\ \mathrm{s}$', fontsize=8.5, color=fs.ORANGE)
    ax.set_xlim(0, 60); ax.set_ylim(0, 75)
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'$v$ (m/s)')
    ax.legend(loc='lower right', fontsize=8.5)
    fs.save(fig, F, 'fig07_11')


# ---------------------------------------------------------------- 그림 7.12 연습문제 14 사슬
def fig12():
    fig, ax = fs.canvas(3.6, 2.3, xlim=(-0.3, 4.6), ylim=(-1.9, 1.0))
    ax.add_patch(Rectangle((0, -0.25), 3.2, 0.25, fc='#eeeeee', ec=fs.BLACK, lw=1.2))
    ax.plot([0.25, 0.25], [-0.25, -1.8], color=fs.BLACK, lw=1.2)
    ax.plot([2.95, 2.95], [-0.25, -1.8], color=fs.BLACK, lw=1.2)
    # 사슬: 탁자 위 0.8~3.2, 그리고 아래로 1.2
    xs = np.arange(0.9, 3.2, 0.12)
    for x in xs:
        ax.add_patch(Circle((x, 0.06), 0.05, fc='none', ec=fs.GRAY, lw=1.0))
    ys = np.arange(-0.06, -1.2, -0.12)
    for y in ys:
        ax.add_patch(Circle((3.26, y), 0.05, fc='none', ec=fs.GRAY, lw=1.0))
    ax.annotate('', xy=(3.55, 0.0), xytext=(3.55, -1.17),
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8, shrinkA=0, shrinkB=0))
    fs.label(ax, (3.95, -0.6), r'$L/3$', fontsize=10)
    ax.annotate('', xy=(0.85, 0.35), xytext=(3.2, 0.35),
                arrowprops=dict(arrowstyle='<->', color=fs.BLACK, lw=0.8, shrinkA=0, shrinkB=0))
    fs.label(ax, (2.0, 0.6), r'$2L/3$', fontsize=10)
    fs.label(ax, (1.6, -0.8), '마찰 없는 탁자', fontsize=9, color=fs.GRAY)
    fs.save(fig, F, 'fig07_12')


# ---------------------------------------------------------------- 그림 7.13 연습문제 15 반구형 그릇
def fig13():
    R = 2.0
    fig, ax = fs.canvas(3.6, 2.6, xlim=(-2.6, 2.9), ylim=(-2.5, 0.7))
    th = np.linspace(np.pi, 2 * np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.BLACK, lw=1.6)
    for a in np.linspace(np.pi + 0.08, 2 * np.pi - 0.08, 22):
        p = R * np.array([np.cos(a), np.sin(a)])
        ax.plot([p[0], p[0] * 1.07], [p[1], p[1] * 1.07 - 0.04], color=fs.BLACK, lw=0.6)
    ax.plot([-R - 0.2, R + 0.2], [0, 0], color=fs.GRAY, ls='--', lw=0.8)
    O = np.array([0, 0]); fs.dot(ax, O, r=0.05); fs.label(ax, (0, 0.2), '중심', fontsize=8.5)
    phi = 38
    pos = R * np.array([np.cos(phi * D2R), -np.sin(phi * D2R)])
    ax.plot([0, pos[0]], [0, pos[1]], color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, O, 0.6, -phi, 0, r'$\varphi$', tr=0.85)
    fs.label(ax, pos * 0.5 + (-0.12, -0.17), r'$R$', fontsize=10)
    ax.add_patch(Circle(pos, 0.11, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=6))
    inward = -pos / R
    tang = np.array([-np.sin(phi * D2R), -np.cos(phi * D2R)])       # 운동 방향(아래쪽)
    perp = np.array([-inward[1], inward[0]])
    fs.vec(ax, pos, inward * 0.75, color=fs.FORCE, lw=1.8)
    fs.label(ax, pos + inward * 0.55 - perp * 0.25, r'$\vec{N}$', color=fs.FORCE, fontsize=10)
    fs.vec(ax, pos, (0, -0.8), color=fs.FORCE, lw=1.8)
    fs.label(ax, pos + (0.3, -0.75), r'$m\vec{g}$', color=fs.FORCE, fontsize=10)
    fs.vec(ax, pos, -tang * 0.6, color=fs.FORCE, lw=1.8)
    fs.label(ax, pos - tang * 0.75 + (0.25, 0.0), r'$\vec{f}_k$', color=fs.FORCE, fontsize=10)
    fs.vec(ax, pos + inward * 0.28, tang * 0.65, color=fs.VEL, lw=1.6)
    fs.label(ax, pos + inward * 0.28 + tang * 0.85, r'$\vec{v}$', color=fs.VEL, fontsize=10)
    ax.add_patch(Circle((R, 0), 0.1, fc='white', ec=fs.GRAY, ls='--', lw=0.9, zorder=5))
    fs.label(ax, (R + 0.25, 0.32), '출발', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, F, 'fig07_13')


for f_ in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
    f_()
