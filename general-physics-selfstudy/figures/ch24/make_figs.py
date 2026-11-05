"""24장 축전기와 유전체 그림 생성 스크립트.  python3 figures/ch24/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Ellipse, FancyArrowPatch, Wedge

sd, elm = fs.schem()
BB = dict(fc='white', ec='none', pad=0.6)


# ---------- 회로 도우미: schemdraw를 matplotlib 축에 그린다 ----------
def circuit(ax):
    return sd.Drawing(canvas=ax)


def finish(ax, d, pad=0.6):
    d.draw(show=False)
    ax.axis('off'); ax.set_aspect('equal')
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - pad, x1 + pad); ax.set_ylim(y0 - pad, y1 + pad)


def mid(e):
    return (np.array(e.start) + np.array(e.end)) / 2


def bat_up():
    """위쪽이 + 극인 전지(schemdraw의 BatteryCell은 그리는 방향의 시작 쪽이 +이므로 뒤집는다)."""
    return elm.BatteryCell().up().reverse()


def plus(ax, e, side, fontsize=10):
    """bat_up()으로 그린 전지의 위쪽에 +, 아래쪽에 −를 쓴다. side는 글자를 놓을 수직 방향 벡터."""
    t, s = np.array(e.start), np.array(e.end)
    u = (t - s) / np.linalg.norm(t - s)
    c = (s + t) / 2
    ax.text(*(c - 0.45 * u + np.array(side)), '+', ha='center', va='center', fontsize=fontsize)
    ax.text(*(c + 0.45 * u + np.array(side)), '−', ha='center', va='center', fontsize=fontsize)


def T(ax, p, s, **kw):
    kw.setdefault('fontsize', 10)
    kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    ax.text(p[0], p[1], s, **kw)


# ---------------------------------------------------------------- 24.1
def fig01():
    """평행판 축전기: 균일한 장, 가장자리 장, 가우스 면."""
    fig, ax = fs.canvas(4.6, 2.6, xlim=(-1.2, 5.6), ylim=(-1.25, 1.55))
    L, h, th = 4.4, 0.6, 0.09
    ax.add_patch(Rectangle((0, h), L, th, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    ax.add_patch(Rectangle((0, -h - th), L, th, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    for x in np.linspace(0.2, L - 0.2, 12):
        T(ax, (x, h - 0.1), '+', color=fs.POS, fontsize=8)
        T(ax, (x, -h + 0.1), '−', color=fs.NEG, fontsize=8)
    for x in np.linspace(0.45, L - 0.45, 7):
        fs.arrow(ax, (x, h - 0.2), (x, -h + 0.2), color=fs.FIELD, lw=1.0, ms=8)
    # 가장자리 장(정성적)
    for sgn, x0 in ((-1, 0.0), (1, L)):
        for k, r in enumerate((0.25, 0.45)):
            t = np.linspace(-np.pi / 2, np.pi / 2, 50)
            xs = x0 + sgn * r * 1.2 * np.cos(t)
            ys = h * np.sin(-t) * (1 + 0.15 * k)
            ys = np.clip(ys, -h, h)
            ax.plot(xs, ys, color=fs.FIELD, lw=0.8, ls='-')
            i = 25
            ax.add_patch(FancyArrowPatch((xs[i - 2], ys[i - 2]), (xs[i + 2], ys[i + 2]), arrowstyle='-|>', mutation_scale=7, color=fs.FIELD, lw=0))
    # 가우스 면(필박스)
    ax.add_patch(Rectangle((1.55, h - 0.3), 0.75, 0.75, fc=fs.SURF, alpha=0.45, ec=fs.BLACK, lw=0.9, ls='--', zorder=4))
    T(ax, (1.92, 1.32), '가우스 면', fontsize=8.5)
    T(ax, (-0.85, h + 0.1), '$+Q$', color=fs.POS)
    T(ax, (-0.85, -h - 0.1), '$-Q$', color=fs.NEG)
    T(ax, (3.6, 0.0), r'$\vec{E}$', color=fs.FIELD, bbox=BB)
    fs.dim(ax, (L + 0.95, h), (L + 0.95, -h), '$d$', off=0.0, color=fs.BLACK)
    T(ax, (2.2, -1.05), '넓이 $A$', fontsize=9)
    fs.save(fig, __file__, 'fig24_01')


def fig02():
    """원통형(동축) 축전기와 구형 축전기."""
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]
    ax.set_xlim(-2.6, 2.7); ax.set_ylim(-1.75, 1.35); ax.set_aspect('equal'); ax.axis('off')
    Lc = 3.6
    fs.cylinder(ax, (0, 0), 1.0, Lc, fc='#cccccc', alpha=0.35, vertical=False, ry=0.3)
    fs.cylinder(ax, (0, 0), 0.62, Lc, fc=fs.SURF, alpha=0.45, vertical=False, ry=0.19, ec=fs.ORANGE)
    fs.cylinder(ax, (0, 0), 0.25, Lc, fc='#f2b8b0', alpha=0.9, vertical=False, ry=0.08)
    xe = Lc / 2
    fs.arrow(ax, (xe, 0), (xe, 0.25), color=fs.BLACK, lw=0.8, ms=6)
    fs.arrow(ax, (xe, 0), (xe + 0.0, -0.62), color=fs.ORANGE, lw=0.8, ms=6)
    fs.arrow(ax, (xe, 0), (xe, 1.0), color=fs.BLACK, lw=0.8, ms=6)
    T(ax, (xe + 0.32, 0.55), '$b$', fontsize=10)
    T(ax, (xe + 0.24, 0.12), '$a$', fontsize=10)
    T(ax, (xe + 0.3, -0.38), '$r$', fontsize=10, color=fs.ORANGE)
    for x in (-1.0, 0.0):
        fs.arrow(ax, (x, 0.27), (x, 0.95), color=fs.FIELD, lw=1.0, ms=7)
        fs.arrow(ax, (x, -0.27), (x, -0.95), color=fs.FIELD, lw=1.0, ms=7)
    fs.dim(ax, (-Lc / 2, -1.05), (Lc / 2, -1.05), '$L$', off=-0.2, color=fs.BLACK)
    T(ax, (0.9, 0.0), '$+Q$', color=fs.POS, fontsize=9, zorder=8)
    T(ax, (0.9, 0.82), '$-Q$', color=fs.NEG, fontsize=9, zorder=8)
    ax.set_title('(가) 원통형(동축)', fontsize=9, y=-0.12)
    ax = axs[1]
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.75, 1.35); ax.set_aspect('equal'); ax.axis('off')
    a, b = 0.45, 1.25
    ax.add_patch(Circle((0, 0), b + 0.12, fc='#cccccc', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), b, fc='white', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), 0.85, fc=fs.SURF, alpha=0.4, ec=fs.ORANGE, lw=1.0, ls='--'))
    ax.add_patch(Circle((0, 0), a, fc='#f2b8b0', ec=fs.BLACK, lw=1.0, zorder=3))
    for k in range(8):
        ang = 2 * np.pi * (k + 0.5) / 8
        u = np.array([np.cos(ang), np.sin(ang)])
        fs.arrow(ax, (a + 0.05) * u, (b - 0.08) * u, color=fs.FIELD, lw=1.0, ms=7)
        T(ax, 0.75 * a * u, '+', color=fs.POS, fontsize=7, zorder=5)
        T(ax, (b - 0.0) * u + 0.0, '', fontsize=7)
    for k in range(12):
        ang = 2 * np.pi * k / 12
        T(ax, (b - 0.1) * np.array([np.cos(ang), np.sin(ang)]), '−', color=fs.NEG, fontsize=7)
    ax.plot([0, 0], [0, a], color=fs.BLACK, lw=0.8, zorder=6)
    T(ax, (0.13, 0.22), '$a$', fontsize=9, zorder=6)
    ax.plot([0, b * np.cos(np.radians(200))], [0, b * np.sin(np.radians(200))], color=fs.BLACK, lw=0.8)
    T(ax, (-0.9, -0.15), '$b$', fontsize=9)
    T(ax, (0.62, -0.5), '$r$', fontsize=9, color=fs.ORANGE)
    ax.set_title('(나) 구형(단면)', fontsize=9, y=-0.12)
    fig.tight_layout(w_pad=0.3)
    fs.save(fig, __file__, 'fig24_02')


# ---------------------------------------------------------------- 24.2
def fig03():
    """병렬과 직렬 연결."""
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    ax = axs[0]
    d = circuit(ax)
    d += (b := bat_up())
    d += elm.Line().right()
    d += elm.Dot()
    d.push(); d += (c1 := elm.Capacitor().down()); d += elm.Dot(); d.pop()
    d += elm.Line().right()
    d += (c2 := elm.Capacitor().down())
    d += elm.Line().left()
    d += elm.Line().left()
    finish(ax, d)
    plus(ax, b, (-0.35, 0))
    T(ax, mid(b) + (-0.85, 0), '$V$')
    for c, n in ((c1, 1), (c2, 2)):
        T(ax, mid(c) + (0.55, 0.3), f'$+Q_{n}$', color=fs.POS, fontsize=9, ha='left')
        T(ax, mid(c) + (0.55, -0.3), f'$-Q_{n}$', color=fs.NEG, fontsize=9, ha='left')
        T(ax, mid(c) + (-0.55, 0), f'$C_{n}$', fontsize=10)
    ax.set_title('(가) 병렬: 같은 $V$', fontsize=9, y=-0.1)
    ax = axs[1]
    d = circuit(ax)
    d += (b := bat_up())
    d += (c1 := elm.Capacitor().right())
    d += (c2 := elm.Capacitor().right())
    d += elm.Line().down()
    d += elm.Line().left().tox(b.start)
    finish(ax, d)
    plus(ax, b, (-0.35, 0))
    T(ax, mid(b) + (-0.85, 0), '$V$')
    for c, n in ((c1, 1), (c2, 2)):
        m = mid(c)
        T(ax, m + (-0.42, 0.55), '$+Q$', color=fs.POS, fontsize=8.5, ha='right')
        T(ax, m + (0.42, 0.55), '$-Q$', color=fs.NEG, fontsize=8.5, ha='left')
        T(ax, m + (0, -0.62), f'$C_{n}$', fontsize=10)
    m1, m2 = mid(c1), mid(c2)
    ax.add_patch(Rectangle((m1[0] + 0.12, m1[1] - 0.3), m2[0] - m1[0] - 0.24, 0.6, fc='none', ec=fs.GRAY, lw=0.9, ls='--'))
    T(ax, ((m1[0] + m2[0]) / 2, m1[1] - 0.62), '알짜 전하 0', fontsize=8, color=fs.GRAY)
    ax.set_title('(나) 직렬: 같은 $Q$', fontsize=9, y=-0.1)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig24_03')


def series_parallel(ax, V, Cs, Cp1, Cp2):
    """전지 – 직렬 축전기 – 병렬 두 축전기 회로."""
    d = circuit(ax)
    d += (b := bat_up())
    d += elm.Line().right(1.5)
    d += (c1 := elm.Capacitor().right())
    d += elm.Line().right(1.0)
    d += elm.Dot()
    d.push(); d += (c2 := elm.Capacitor().down()); d += elm.Dot(); d.pop()
    d += elm.Line().right(2.5)
    d += (c3 := elm.Capacitor().down())
    d += elm.Line().left(2.5)
    d += elm.Line().left().tox(b.start)
    finish(ax, d, pad=0.3)
    plus(ax, b, (-0.35, 0))
    T(ax, mid(b) + (-0.95, 0), V, fontsize=10, ha='right')
    T(ax, mid(c1) + (0, 0.65), Cs[0], fontsize=10)
    T(ax, mid(c1) + (0, -0.6), Cs[1], fontsize=9, color=fs.GRAY)
    for c, (n, v) in ((c2, Cp1), (c3, Cp2)):
        T(ax, mid(c) + (0.45, 0.18), n, fontsize=10, ha='left')
        T(ax, mid(c) + (0.45, -0.32), v, fontsize=9, ha='left', color=fs.GRAY)


def fig04():
    fig, ax = plt.subplots(figsize=(4.2, 2.3))
    series_parallel(ax, '$12\\ \\mathrm{V}$', ('$C_1$', '$12\\ \\mu\\mathrm{F}$'),
                    ('$C_2$', '$4.0\\ \\mu\\mathrm{F}$'), ('$C_3$', '$8.0\\ \\mu\\mathrm{F}$'))
    fs.save(fig, __file__, 'fig24_04')


# ---------------------------------------------------------------- 24.3
def fig05():
    """충전하는 데 드는 일: v–q 그래프의 넓이."""
    fig, ax = plt.subplots(figsize=(3.6, 2.5))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    Q, C = 1.0, 1.0
    q = np.linspace(0, Q, 50)
    ax.fill_between(q, q / C, color=fs.VEL, alpha=0.15, lw=0)
    ax.plot(q, q / C, color=fs.VEL, lw=1.8)
    q0, dq = 0.55, 0.06
    ax.add_patch(Rectangle((q0, 0), dq, q0 / C, fc=fs.VEL, alpha=0.55, ec='none'))
    ax.plot([0, Q], [Q / C, Q / C], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot([Q, Q], [0, Q / C], color=fs.GRAY, lw=0.7, ls=':')
    ax.set_xticks([q0, Q]); ax.set_xticklabels(['$q$', '$Q$'])
    ax.set_yticks([Q / C]); ax.set_yticklabels(['$V = Q/C$'])
    ax.set_xlim(0, 1.25); ax.set_ylim(0, 1.25)
    ax.set_xlabel('전하 $q$'); ax.set_ylabel('전위차 $v = q/C$')
    ax.annotate(r'$dW = v\,dq$', xy=(q0 + dq / 2, 0.35), xytext=(0.12, 0.75), fontsize=9,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.text(0.72, 0.22, r'넓이 $= \dfrac{Q^2}{2C}$', fontsize=9.5)
    fs.save(fig, __file__, 'fig24_05')


def fig06():
    """예제 24.4: 충전된 C1을 빈 C2에 연결."""
    fig, ax = plt.subplots(figsize=(3.6, 2.2))
    d = circuit(ax)
    d += (c1 := elm.Capacitor().down())
    d += elm.Line().right(1.2)
    d += elm.Line().right(1.8)
    d += (c2 := elm.Capacitor().up())
    d += (s := elm.Switch().left())
    finish(ax, d, pad=0.3)
    T(ax, mid(c1) + (-0.5, 0.0), '$C_1$', ha='right')
    T(ax, mid(c1) + (0.35, 0.32), '$+$', color=fs.POS, fontsize=10)
    T(ax, mid(c1) + (0.35, -0.32), '$-$', color=fs.NEG, fontsize=10)
    T(ax, mid(c1) + (-0.5, -0.55), '$100\\ \\mathrm{V}$', ha='right', fontsize=9, color=fs.GRAY)
    T(ax, mid(c2) + (0.5, 0.0), '$C_2$', ha='left')
    T(ax, mid(c2) + (0.5, -0.55), '처음 0', ha='left', fontsize=9, color=fs.GRAY)
    T(ax, mid(s) + (0, 0.55), '$S$')
    fs.save(fig, __file__, 'fig24_06')


# ---------------------------------------------------------------- 24.4
def fig07():
    """★ 유전체 판이 빨려 들어가는 힘과 가장자리 장."""
    fig, ax = fs.canvas(4.6, 2.3, xlim=(-1.9, 4.9), ylim=(-1.2, 1.3))
    L, h, th = 4.0, 0.55, 0.08
    for y in (h, -h - th):
        ax.add_patch(Rectangle((0, y), L, th, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    x = 2.3
    ax.add_patch(Rectangle((-1.5, -h + 0.06), x + 1.5, 2 * h - 0.12, fc='#cfe3c8', ec=fs.BLACK, lw=1.0, zorder=2))
    T(ax, (-0.85, 0.0), '$\\kappa$', fontsize=11)
    for xx in np.linspace(0.35, L - 0.3, 7):
        fs.arrow(ax, (xx, h - 0.02), (xx, -h + 0.02), color=fs.FIELD, lw=0.9, ms=7, zorder=4)
    # 왼쪽 가장자리 장: 판 끝에서 휘어져 나와 유전체를 지난다
    for r in (0.25, 0.45, 0.65):
        t = np.linspace(-np.pi / 2, np.pi / 2, 60)
        xs = -r * 1.1 * np.cos(t); ys = -h * np.sin(t)
        ax.plot(xs, ys, color=fs.FIELD, lw=0.8, zorder=4)
        ax.add_patch(FancyArrowPatch((xs[28], ys[28]), (xs[32], ys[32]), arrowstyle='-|>', mutation_scale=7, color=fs.FIELD, lw=0, zorder=4))
    fs.arrow(ax, (-0.3, -0.85), (0.8, -0.85), color=fs.FORCE, lw=1.8)
    T(ax, (1.05, -0.85), '$\\vec{F}$', color=fs.FORCE)
    fs.dim(ax, (0, h + th), (x, h + th), '$x$', off=0.22, color=fs.BLACK)
    fs.dim(ax, (0, h + th), (L, h + th), '$L$', off=0.55, color=fs.GRAY)
    fs.dim(ax, (L + 0.35, h), (L + 0.35, -h), '$d$', off=0.0, color=fs.BLACK)
    fs.save(fig, __file__, 'fig24_07')


def fig08():
    """예제 24.7: 두께 t인 유전체 판이 일부 채운 축전기."""
    fig, ax = fs.canvas(4.0, 2.6, xlim=(-0.9, 5.2), ylim=(-1.4, 1.25))
    L, h, th, t = 4.0, 0.95, 0.08, 0.7
    for y in (h, -h - th):
        ax.add_patch(Rectangle((0, y), L, th, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    for xx in np.linspace(0.25, L - 0.25, 10):
        T(ax, (xx, h - 0.09), '+', color=fs.POS, fontsize=7)
        T(ax, (xx, -h + 0.09), '−', color=fs.NEG, fontsize=7)
    yb = -0.15
    ax.add_patch(Rectangle((0, yb - t / 2), L, t, fc='#cfe3c8', ec=fs.BLACK, lw=0.9, zorder=1))
    kap = 3.0
    for xx in np.linspace(0.45, L - 0.45, 5):
        fs.arrow(ax, (xx, h - 0.2), (xx, yb + t / 2 + 0.02), color=fs.FIELD, lw=1.2, ms=8)
        fs.arrow(ax, (xx, yb + 0.1), (xx, yb + 0.1 - 0.55 / kap), color=fs.FIELD, lw=1.2, ms=6)
        fs.arrow(ax, (xx, yb - t / 2 - 0.02), (xx, -h + 0.2), color=fs.FIELD, lw=1.2, ms=8)
    T(ax, (L + 0.15, h - 0.25), '$E_0$', color=fs.FIELD, ha='left', fontsize=10)
    T(ax, (L + 0.15, yb), '$E_0/\\kappa$', color=fs.FIELD, ha='left', fontsize=10)
    T(ax, (L + 0.15, -h + 0.18), '$E_0$', color=fs.FIELD, ha='left', fontsize=10)
    fs.dim(ax, (-0.6, h), (-0.6, -h), '$d$', off=0.0, color=fs.BLACK)
    ax.add_patch(FancyArrowPatch((0.2, yb + t / 2), (0.2, yb - t / 2), arrowstyle='<|-|>', mutation_scale=7, color=fs.BLACK, lw=0.8))
    T(ax, (0.3, yb), '$t$', fontsize=10, ha='left')
    T(ax, (2.0, -1.3), '넓이 $A$', fontsize=9)
    fs.save(fig, __file__, 'fig24_08')


def fig09():
    """★ 두 유전체 경계에서 전기력선이 꺾이는 각."""
    fig, ax = fs.canvas(3.4, 2.7, xlim=(-1.9, 1.9), ylim=(-1.6, 1.4))
    ax.add_patch(Rectangle((-1.9, -1.6), 3.8, 1.6, fc='#cfe3c8', ec='none', zorder=0))
    ax.plot([-1.9, 1.9], [0, 0], color=fs.BLACK, lw=1.0)
    ax.plot([0, 0], [-1.5, 1.3], color=fs.GRAY, lw=0.8, ls='--')
    k1, k2, th1 = 1.0, 3.0, np.radians(25)
    th2 = np.arctan(np.tan(th1) * k2 / k1)
    for off in (-0.35, 0.0, 0.35):
        p0 = np.array([off - 1.3 * np.tan(th1), 1.3]); p1 = np.array([off, 0.0])
        p2 = p1 + 1.5 * np.array([np.sin(th2), -np.cos(th2)])
        for a_, b_ in ((p0, p1), (p1, p2)):
            ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=fs.FIELD, lw=1.1)
            m = a_ + 0.55 * (b_ - a_)
            ax.add_patch(FancyArrowPatch(a_ + 0.5 * (b_ - a_), m, arrowstyle='-|>', mutation_scale=8, color=fs.FIELD, lw=0))
    fs.angle_arc(ax, (0, 0), 0.55, 90, 90 + np.degrees(th1), r'$\theta_1$', fontsize=10, tr=0.8)
    fs.angle_arc(ax, (0, 0), 0.45, -90, -90 + np.degrees(th2), r'$\theta_2$', fontsize=10, tr=0.7)
    T(ax, (1.35, 0.85), '$\\kappa_1$', fontsize=11)
    T(ax, (-1.35, -0.85), '$\\kappa_2 > \\kappa_1$', fontsize=10)
    fs.save(fig, __file__, 'fig24_09')


# ---------------------------------------------------------------- 24.5
def dip(ax, c, ang=0.0, L=0.42, W=0.2):
    """작은 쌍극자 분자: 왼쪽 −(파랑), 오른쪽 +(빨강)."""
    u = np.array([np.cos(ang), np.sin(ang)])
    ax.add_patch(Ellipse(c, L, W, angle=np.degrees(ang), fc='#f4f4f4', ec=fs.GRAY, lw=0.6))
    T(ax, c - 0.11 * u, '−', color=fs.NEG, fontsize=7)
    T(ax, c + 0.11 * u, '+', color=fs.POS, fontsize=7)


def fig10():
    """분자의 분극: 유도 쌍극자와 영구 쌍극자의 정렬."""
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    ax = axs[0]
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.axis('off')
    # E = 0
    ax.add_patch(Circle((0.9, 0.1), 0.55, fc=fs.NEG, alpha=0.25, ec='none'))
    ax.add_patch(Circle((0.9, 0.1), 0.08, fc=fs.POS, ec='none'))
    T(ax, (0.9, -0.85), '$\\vec{E} = 0$', fontsize=9)
    # E ≠ 0: 전자 구름이 장의 반대쪽으로 밀린다
    ax.add_patch(Ellipse((2.85, 0.1), 1.2, 1.05, fc=fs.NEG, alpha=0.25, ec='none'))
    ax.add_patch(Circle((3.12, 0.1), 0.08, fc=fs.POS, ec='none'))
    fs.arrow(ax, (2.55, 0.1), (3.2, 0.1), color=fs.BLACK, lw=1.3, ms=8)
    T(ax, (2.85, 0.32), '$\\vec{p}$', fontsize=10)
    fs.arrow(ax, (2.1, -0.85), (3.7, -0.85), color=fs.FIELD, lw=1.2, ms=8)
    T(ax, (3.95, -0.85), '$\\vec{E}$', color=fs.FIELD, fontsize=10)
    ax.set_title('(가) 유도 쌍극자', fontsize=9, y=-0.12)
    ax = axs[1]
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(3)
    pts = [(x, y) for x in (0.35, 0.95, 1.55) for y in (0.75, 0.15, -0.45)]
    for p in pts:
        dip(ax, p, rng.uniform(0, 2 * np.pi))
    T(ax, (0.95, -1.0), '$\\vec{E} = 0$', fontsize=9)
    for p in pts:
        dip(ax, (p[0] + 2.0, p[1]), rng.normal(0, 0.45))
    fs.arrow(ax, (2.1, -1.0), (3.7, -1.0), color=fs.FIELD, lw=1.2, ms=8)
    T(ax, (3.95, -1.0), '$\\vec{E}$', color=fs.FIELD, fontsize=10)
    ax.set_title('(나) 극성 분자의 부분 정렬', fontsize=9, y=-0.12)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig24_10')


def fig11():
    """속박 전하: 유전체 표면에 드러난 전하가 자유 전하를 일부 가린다."""
    fig, ax = fs.canvas(4.4, 2.8, xlim=(-1.0, 5.2), ylim=(-1.75, 1.9))
    H = 1.5
    ax.add_patch(Rectangle((-0.15, -H), 0.12, 2 * H, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((4.23, -H), 0.12, 2 * H, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    for y in np.linspace(-H + 0.15, H - 0.15, 9):
        T(ax, (0.1, y), '+', color=fs.POS, fontsize=9)
        T(ax, (4.1, y), '−', color=fs.NEG, fontsize=9)
    ax.add_patch(Rectangle((0.45, -H + 0.05), 3.3, 2 * H - 0.1, fc='#e3efdf', ec=fs.BLACK, lw=0.9))
    for x in np.linspace(0.85, 3.35, 5):
        for y in np.linspace(-1.05, 1.05, 5):
            dip(ax, (x, y), 0.0, L=0.46, W=0.22)
    for y in np.linspace(-H + 0.25, H - 0.25, 6):
        T(ax, (0.55, y), '−', color=fs.NEG, fontsize=9, fontweight='bold')
        T(ax, (3.65, y), '+', color=fs.POS, fontsize=9, fontweight='bold')
    T(ax, (0.1, H + 0.22), '$+\\sigma_f$', color=fs.POS, fontsize=9.5)
    T(ax, (4.1, H + 0.22), '$-\\sigma_f$', color=fs.NEG, fontsize=9.5)
    T(ax, (0.65, H + 0.22), '$-\\sigma_b$', color=fs.NEG, fontsize=9.5, ha='left')
    T(ax, (3.55, H + 0.22), '$+\\sigma_b$', color=fs.POS, fontsize=9.5, ha='right')
    fs.arrow(ax, (1.2, -1.62), (3.0, -1.62), color=fs.FIELD, lw=1.3, ms=8)
    T(ax, (3.15, -1.62), '$\\vec{E} = \\vec{E}_0/\\kappa$', color=fs.FIELD, fontsize=9.5, ha='left')
    fs.save(fig, __file__, 'fig24_11')


def fig12():
    """🐍 κ(x)가 선형으로 변하는 축전기 속 E(x)."""
    eps0 = 8.8541878128e-12
    A, d, V, k1, k2 = 0.010, 1.0e-3, 100.0, 2.0, 6.0
    C = eps0 * A * (k2 - k1) / (d * np.log(k2 / k1))
    D = C * V / A
    x = np.linspace(0, d, 200)
    kap = k1 + (k2 - k1) * x / d
    E = D / (kap * eps0)
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.plot(x * 1e3, E / 1e5, color=fs.FIELD, lw=1.8, label='$E(x)$')
    ax.set_xlabel('$x$ (mm)'); ax.set_ylabel(r'$E$ ($10^5$ V/m)', color=fs.FIELD)
    ax.set_ylim(0, 2.0); ax.set_xlim(0, 1)
    ax2 = ax.twinx()
    ax2.plot(x * 1e3, kap, color=fs.GRAY, lw=1.3, ls='--')
    ax2.set_ylabel(r'$\kappa(x)$', color=fs.GRAY); ax2.set_ylim(0, 7)
    ax2.spines['top'].set_visible(False)
    ax.text(0.03, 1.87, r'$E(0) = 1.82\times10^5$', fontsize=8.5, color=fs.FIELD)
    ax.text(0.55, 0.42, r'$E(d) = 0.607\times10^5$', fontsize=8.5, color=fs.FIELD)
    ax2.text(0.62, 5.2, r'$\kappa(x)$', fontsize=9, color=fs.GRAY)
    fs.save(fig, __file__, 'fig24_12')


# ---------------------------------------------------------------- 연습문제
def fig13():
    fig, ax = plt.subplots(figsize=(4.2, 2.3))
    series_parallel(ax, '$30\\ \\mathrm{V}$', ('$C_3$', '$3.0\\ \\mu\\mathrm{F}$'),
                    ('$C_1$', '$2.0\\ \\mu\\mathrm{F}$'), ('$C_2$', '$4.0\\ \\mu\\mathrm{F}$'))
    fs.save(fig, __file__, 'fig24_13')


def fig14():
    """연습문제 11: 넓이 절반을 유전체로 채운 평행판."""
    fig, ax = fs.canvas(3.8, 2.2, xlim=(-0.5, 4.6), ylim=(-1.15, 1.2))
    L, h, th = 4.0, 0.65, 0.08
    for y in (h, -h - th):
        ax.add_patch(Rectangle((0, y), L, th, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    ax.add_patch(Rectangle((0, -h), L / 2, 2 * h, fc='#cfe3c8', ec='none', zorder=0))
    ax.plot([L / 2, L / 2], [-h, h], color=fs.BLACK, lw=0.8, ls='--')
    for xx in np.linspace(0.1, L / 2 - 0.1, 10):
        T(ax, (xx, h - 0.12), '+', color=fs.POS, fontsize=7)
        T(ax, (xx, -h + 0.12), '−', color=fs.NEG, fontsize=7)
    for xx in np.linspace(L / 2 + 0.5, L - 0.5, 2):
        T(ax, (xx, h - 0.12), '+', color=fs.POS, fontsize=7)
        T(ax, (xx, -h + 0.12), '−', color=fs.NEG, fontsize=7)
    for xx in (0.5, 1.0, 1.5, 2.5, 3.0, 3.5):
        fs.arrow(ax, (xx, h - 0.22), (xx, -h + 0.22), color=fs.FIELD, lw=1.0, ms=7)
    T(ax, (1.0, -0.0), '$\\kappa = 5.0$', fontsize=9.5, bbox=dict(fc='#cfe3c8', ec='none', pad=0.5))
    T(ax, (3.0, -0.0), '공기', fontsize=9.5, bbox=BB)
    fs.save(fig, __file__, 'fig24_14')


def fig15():
    """연습문제 15: 아래쪽 반구만 유전체로 채운 구형 축전기."""
    fig, ax = fs.canvas(2.8, 2.6, xlim=(-1.55, 1.55), ylim=(-1.5, 1.4))
    a, b = 0.45, 1.2
    ax.add_patch(Circle((0, 0), b + 0.1, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), b, fc='white', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Wedge((0, 0), b, 180, 360, width=b - a, fc='#cfe3c8', ec='none'))
    ax.plot([-b, b], [0, 0], color=fs.BLACK, lw=0.7, ls='--')
    ax.add_patch(Circle((0, 0), a, fc='#f2b8b0', ec=fs.BLACK, lw=1.0, zorder=3))
    for k in range(8):
        ang = 2 * np.pi * (k + 0.5) / 8
        u = np.array([np.cos(ang), np.sin(ang)])
        fs.arrow(ax, (a + 0.04) * u, (b - 0.06) * u, color=fs.FIELD, lw=1.0, ms=7)
    for k in range(4):
        ang = np.pi * (k + 0.5) / 4
        T(ax, 0.72 * a * np.array([np.cos(ang), np.sin(ang)]), '+', color=fs.POS, fontsize=7, zorder=5)
    for k in range(10):
        ang = np.pi + np.pi * (k + 0.5) / 10
        T(ax, 0.76 * a * np.array([np.cos(ang), np.sin(ang)]), '+', color=fs.POS, fontsize=6, zorder=5)
    T(ax, (0.95, -0.95), '$\\kappa$', fontsize=11)
    ax.plot([0, -a * np.cos(np.radians(30))], [0, a * np.sin(np.radians(30))], color=fs.BLACK, lw=0.7, zorder=6)
    T(ax, (-0.95, 0.85), '$b$', fontsize=10)
    ax.plot([0, -b * np.cos(np.radians(45))], [0, b * np.sin(np.radians(45))], color=fs.BLACK, lw=0.7)
    T(ax, (-0.13, 0.3), '$a$', fontsize=9, zorder=6)
    fs.save(fig, __file__, 'fig24_15')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15):
        f()
