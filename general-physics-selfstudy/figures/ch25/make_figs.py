"""25장 전류, 저항, 직류 회로 그림 생성 스크립트.  python3 figures/ch25/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Ellipse, FancyArrowPatch, Wedge, Arc

sd, elm = fs.schem()
BB = dict(fc='white', ec='none', pad=0.5)
CUR = fs.VEL      # 전류 화살표 색


# ---------- 회로 도우미 ----------
def circuit(ax):
    return sd.Drawing(canvas=ax)


def finish(ax, d, pad=0.5):
    d.draw(show=False)
    ax.axis('off'); ax.set_aspect('equal')
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - pad, x1 + pad); ax.set_ylim(y0 - pad, y1 + pad)


def mid(e):
    return (np.array(e.start) + np.array(e.end)) / 2


def bat(p, q):
    """p→q 방향의 전지, q 쪽이 + 극(schemdraw BatteryCell은 시작 쪽이 +이므로 뒤집는다)."""
    return elm.BatteryCell().at(p).to(q).reverse()


def pm(ax, e, side, fontsize=10):
    """bat()으로 그린 전지의 + (끝 쪽), − (시작 쪽) 표시."""
    s, t = np.array(e.start), np.array(e.end)
    u = (t - s) / np.linalg.norm(t - s); c = (s + t) / 2
    ax.text(*(c + 0.42 * u + np.array(side)), '+', ha='center', va='center', fontsize=fontsize)
    ax.text(*(c - 0.42 * u + np.array(side)), '−', ha='center', va='center', fontsize=fontsize)


def T(ax, p, s, **kw):
    kw.setdefault('fontsize', 10); kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    ax.text(p[0], p[1], s, **kw)


def cur(ax, p, q, label=None, loff=(0.3, 0), color=CUR, **kw):
    fs.arrow(ax, p, q, color=color, lw=1.4, ms=10, zorder=8)
    if label:
        m = (np.array(p) + np.array(q)) / 2 + np.array(loff)
        T(ax, m, label, color=color, **kw)


def meter(ax, c, letter, r=0.42):
    """계기(전류계 A, 전압계 V, 검류계 G)를 도선 위에 원과 글자로 그린다."""
    ax.add_patch(Circle(c, r, fc='white', ec=fs.BLACK, lw=1.4, zorder=5))
    T(ax, c, letter, fontsize=10, zorder=6)


def loop_arrow(ax, c, r=0.6, cw=True, label=None):
    """고리 방향 표시(원호 화살표)."""
    th1, th2 = (60, 330) if cw else (210, 120 + 360)
    t = np.radians(np.linspace(th1, th2, 60))
    if cw:
        t = t[::-1]
    xs, ys = c[0] + r * np.cos(t), c[1] + r * np.sin(t)
    ax.plot(xs, ys, color=fs.GRAY, lw=0.9)
    ax.add_patch(FancyArrowPatch((xs[-3], ys[-3]), (xs[-1], ys[-1]), arrowstyle='-|>', mutation_scale=9, color=fs.GRAY, lw=0))
    if label:
        T(ax, c, label, fontsize=8.5, color=fs.GRAY)


# ---------------------------------------------------------------- 25.1
def fig01():
    """전류밀도와 표류 속도: 시간 dt 동안 단면을 지나는 운반자."""
    fig, ax = fs.canvas(4.8, 2.2, xlim=(-2.9, 3.9), ylim=(-1.35, 1.25))
    fs.cylinder(ax, (0, 0), 0.8, 5.2, fc='#dddddd', alpha=0.4, vertical=False, ry=0.28)
    x0, x1 = -0.2, 1.3
    ax.add_patch(Rectangle((x0, -0.8), x1 - x0, 1.6, fc=fs.SURF, alpha=0.45, ec='none', zorder=1))
    ax.add_patch(Ellipse((x1, 0), 0.56, 1.6, fc=fs.SURF, alpha=0.8, ec=fs.BLACK, lw=1.0, zorder=2))
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 50)
    ax.plot(x0 + 0.28 * np.cos(th), 0.8 * np.sin(th), color=fs.BLACK, lw=0.8, ls='--')
    ax.plot(x0 - 0.28 * np.cos(th), 0.8 * np.sin(th), color=fs.BLACK, lw=0.8, ls='--')
    rng = np.random.default_rng(5)
    pts = np.c_[rng.uniform(-2.4, 2.4, 26), rng.uniform(-0.6, 0.6, 26)]
    for p in pts:
        ax.add_patch(Circle(p, 0.07, fc=fs.POS, ec='none', zorder=4))
    for p in pts[:6]:
        fs.arrow(ax, p, p + np.array([0.45, 0]), color=fs.VEL, lw=1.0, ms=6)
    T(ax, (x1, 1.05), '단면 $A$', fontsize=9)
    fs.dim(ax, (x0, -0.85), (x1, -0.85), '$v_d\\,dt$', off=-0.2, color=fs.BLACK)
    fs.arrow(ax, (2.85, 0), (3.7, 0), color=fs.BLACK, lw=1.4)
    T(ax, (3.3, 0.3), '$\\vec{J}$, $I$', fontsize=10)
    fs.arrow(ax, (-2.6, 1.05), (-1.9, 1.05), color=fs.VEL, lw=1.2, ms=8)
    T(ax, (-1.6, 1.05), '$\\vec{v}_d$', color=fs.VEL, fontsize=10)
    fs.save(fig, __file__, 'fig25_01')


# ---------------------------------------------------------------- 25.2
def fig02():
    """균일한 도선의 저항."""
    fig, ax = fs.canvas(4.4, 1.9, xlim=(-2.9, 2.9), ylim=(-1.2, 1.1))
    fs.cylinder(ax, (0, 0), 0.5, 4.4, fc='#d9c7a7', alpha=0.6, vertical=False, ry=0.18)
    for y in (-0.25, 0.0, 0.25):
        fs.arrow(ax, (-1.6, y), (1.4, y), color=fs.FIELD, lw=0.9, ms=7)
    T(ax, (1.65, 0.0), '$\\vec{E}$', color=fs.FIELD, fontsize=10)
    ax.plot([-2.2, -2.75], [0, 0], color=fs.BLACK, lw=1.2); ax.plot([2.2, 2.75], [0, 0], color=fs.BLACK, lw=1.2)
    T(ax, (-2.75, 0.3), '$+$', fontsize=11); T(ax, (2.75, 0.3), '$-$', fontsize=11)
    cur(ax, (-2.75, -0.2), (-2.3, -0.2), '$I$', loff=(0, -0.22))
    fs.dim(ax, (-2.2, -0.55), (2.2, -0.55), '$L$', off=-0.2, color=fs.BLACK)
    T(ax, (2.2, 0.75), '단면적 $A$', fontsize=9)
    T(ax, (0, 0.85), '$V$ (양끝의 전위차)', fontsize=9)
    fs.save(fig, __file__, 'fig25_02')


def fig03():
    """I–V 곡선: 옴성 저항, 백열전구 필라멘트, 다이오드."""
    fig, axs = plt.subplots(1, 3, figsize=(5.4, 1.9))
    V = np.linspace(-1, 1, 300)
    Id = np.where(V > 0, 0.02 * (np.exp(V / 0.17) - 1), -0.004)
    curves = [V, 1.8 * V / (1 + 1.6 * np.abs(V)), np.where(Id > 1.1, np.nan, Id)]
    titles = ['(가) 옴성 저항', '(나) 필라멘트', '(다) 다이오드']
    for ax, I, ti in zip(axs, curves, titles):
        ax.axhline(0, color=fs.GRAY, lw=0.7); ax.axvline(0, color=fs.GRAY, lw=0.7)
        ax.plot(V, I, color=fs.VEL, lw=1.8)
        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.1, 1.1)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.text(1.0, -0.2, '$V$', fontsize=9, ha='right'); ax.text(0.06, 1.0, '$I$', fontsize=9, va='top')
        ax.set_title(ti, fontsize=9, y=-0.2)
    fig.tight_layout(w_pad=0.8)
    fs.save(fig, __file__, 'fig25_03')


def fig04():
    """예제 25.2: 동심 원통 사이의 지름 방향 전류(단면)."""
    fig, ax = fs.canvas(2.8, 2.6, xlim=(-1.55, 1.55), ylim=(-1.45, 1.45))
    a, b, r, dr = 0.4, 1.25, 0.8, 0.12
    ax.add_patch(Circle((0, 0), b + 0.1, fc='#bbbbbb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, 0), b, fc='#efe3cb', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Wedge((0, 0), r + dr / 2, 0, 360, width=dr, fc=fs.ORANGE, alpha=0.6, ec='none'))
    ax.add_patch(Circle((0, 0), a, fc='#bbbbbb', ec=fs.BLACK, lw=1.0, zorder=3))
    for k in range(8):
        ang = 2 * np.pi * (k + 0.5) / 8
        u = np.array([np.cos(ang), np.sin(ang)])
        fs.arrow(ax, (a + 0.05) * u, (b - 0.07) * u, color=CUR, lw=1.0, ms=7)
    ax.plot([0, a], [0, 0], color=fs.BLACK, lw=0.8, zorder=4); T(ax, (0.2, 0.12), '$a$', fontsize=9, zorder=5)
    ax.plot([0, -b * np.cos(np.radians(20))], [0, -b * np.sin(np.radians(20))], color=fs.BLACK, lw=0.8)
    T(ax, (-1.0, -0.12), '$b$', fontsize=9)
    T(ax, (0.62, 0.78), '$r$', fontsize=9, color=fs.ORANGE)
    T(ax, (1.05, -1.25), '$\\rho$', fontsize=10)
    fs.save(fig, __file__, 'fig25_04')


# ---------------------------------------------------------------- 25.3
def fig05():
    """드루드 모형: 충돌 사이의 포물선 운동과 표류."""
    rng = np.random.default_rng(11)
    n = 26
    ang = rng.uniform(0, 2 * np.pi, n); tau = rng.exponential(1.0, n)
    fig, ax = fs.canvas(4.6, 2.3)
    for acc, col, lab in ((0.0, fs.GRAY, '$\\vec{E} = 0$'), (-0.3, fs.VEL, '$\\vec{E}$ 있음')):
        p = np.zeros(2); P = [p.copy()]; C = [p.copy()]
        for k in range(n):
            v0 = np.array([np.cos(ang[k]), np.sin(ang[k])])
            t = np.linspace(0, tau[k], 15)
            seg = p + np.outer(t, v0) + 0.5 * np.outer(t ** 2, [acc, 0])
            P.extend(seg[1:]); p = seg[-1].copy(); C.append(p.copy())
        P = np.array(P); C = np.array(C)
        ax.plot(P[:, 0], P[:, 1], color=col, lw=1.0, ls='-' if acc else '--')
        ax.plot(C[1:-1, 0], C[1:-1, 1], 'o', ms=2.2, color=col)
        ax.plot(*C[-1], 'o', ms=5, color=col)
    ax.plot(0, 0, 'o', ms=5, color=fs.BLACK)
    T(ax, (0.0, -0.45), '출발', fontsize=8.5)
    ax.set_aspect('equal')
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    fs.arrow(ax, (x1 - 3.0, y0 - 0.6), (x1 - 0.6, y0 - 0.6), color=fs.FIELD, lw=1.3)
    T(ax, (x1 - 0.2, y0 - 0.6), '$\\vec{E}$', color=fs.FIELD)
    ax.plot([], [], color=fs.GRAY, ls='--', label='$\\vec{E} = 0$')
    ax.plot([], [], color=fs.VEL, label='$\\vec{E}$ 있음 (전자)')
    ax.legend(fontsize=8.5, frameon=False, loc='upper left', bbox_to_anchor=(0.0, 1.08))
    ax.set_ylim(y0 - 0.9, y1 + 0.6)
    fs.save(fig, __file__, 'fig25_05')


# ---------------------------------------------------------------- 25.4
def fig06():
    """기전력과 내부 저항, 단자 전압."""
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    d = circuit(ax)
    d += (b := bat((0, 0), (0, 2.0)))
    d += (r := elm.Resistor().at((0, 2.0)).to((0, 4.0)))
    d += elm.Line().at((0, 4.0)).to((4.0, 4.0))
    d += (R := elm.Resistor().at((4.0, 4.0)).to((4.0, 0)))
    d += elm.Line().at((4.0, 0)).to((0, 0))
    finish(ax, d)
    pm(ax, b, (0.45, 0))
    T(ax, mid(b) + (-0.6, 0), '$\\mathcal{E}$', ha='right')
    T(ax, mid(r) + (-0.6, 0), '$r$', ha='right')
    T(ax, mid(R) + (0.6, 0), '$R$', ha='left')
    ax.add_patch(Rectangle((-1.2, -0.35), 2.4, 4.7, fc='none', ec=fs.GRAY, lw=0.9, ls='--'))
    T(ax, (0.0, -0.65), '실제 전원', fontsize=8.5, color=fs.GRAY)
    for p in ((1.2, 4.0), (1.2, 0)):
        ax.add_patch(Circle(p, 0.1, fc='white', ec=fs.BLACK, zorder=9))
    T(ax, (1.45, 4.35), '$a$'); T(ax, (1.45, -0.35), '$b$')
    cur(ax, (2.2, 4.0), (3.1, 4.0), '$I$', loff=(0, 0.35))
    ax.set_xlim(-1.9, 5.3); ax.set_ylim(-1.0, 4.8)
    fs.save(fig, __file__, 'fig25_06')


def fig07():
    """예제 25.5: 외부 저항의 일률 P(R)와 효율."""
    emf, r = 12.0, 2.0
    R = np.linspace(0.01, 16, 400)
    P = emf ** 2 * R / (R + r) ** 2
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.plot(R, P, color=fs.FORCE, lw=1.8)
    ax.plot([2, 4], [18, 16], 'o', color=fs.FORCE, ms=5)
    ax.annotate('$R = r$: 18 W, 효율 50%', xy=(2, 18), xytext=(4.5, 19.3), fontsize=8.5,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.annotate('$R = 4\\ \\Omega$: 16 W, 효율 67%', xy=(4, 16), xytext=(6.5, 13.0), fontsize=8.5,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.set_xlim(0, 16); ax.set_ylim(0, 21)
    ax.set_xlabel('외부 저항 $R$ ($\\Omega$)'); ax.set_ylabel('$P$ (W)')
    fs.save(fig, __file__, 'fig25_07')


# ---------------------------------------------------------------- 25.5
def fig08():
    """예제 25.6: 두 고리 회로."""
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    d = circuit(ax)
    d += (e1 := bat((0, 0), (0, 3)))
    d += (r1 := elm.Resistor().at((0, 3)).to((4, 3)))
    d += (r2 := elm.Resistor().at((4, 3)).to((8, 3)))
    d += elm.Dot().at((4, 3))
    d += (r3 := elm.Resistor().at((4, 3)).to((4, 0)))
    d += elm.Dot().at((4, 0))
    d += (e2 := bat((8, 0), (8, 3)))
    d += elm.Line().at((0, 0)).to((8, 0))
    finish(ax, d)
    pm(ax, e1, (0.45, 0)); pm(ax, e2, (-0.45, 0))
    T(ax, mid(e1) + (-0.55, 0), '$\\mathcal{E}_1$', ha='right')
    T(ax, mid(e2) + (0.55, 0), '$\\mathcal{E}_2$', ha='left')
    T(ax, mid(r1) + (0, 0.55), '$R_1$'); T(ax, mid(r2) + (0, 0.55), '$R_2$')
    T(ax, mid(r3) + (-0.55, 0), '$R_3$', ha='right')
    cur(ax, (0, 0.2), (0, 0.75), '$I_1$', loff=(-0.35, 0), ha='right')
    cur(ax, (8, 0.2), (8, 0.75), '$I_2$', loff=(0.35, 0), ha='left')
    cur(ax, (4, 0.95), (4, 0.35), '$I_3$', loff=(0.35, 0), ha='left')
    loop_arrow(ax, (2.0, 1.45), r=0.6, cw=True, label='1')
    loop_arrow(ax, (6.0, 1.45), r=0.6, cw=False, label='2')
    fs.save(fig, __file__, 'fig25_08')


def fig09():
    """전류계와 전압계의 연결."""
    fig, ax = plt.subplots(figsize=(4.0, 2.4))
    d = circuit(ax)
    d += (b := bat((0, 0), (0, 3)))
    d += elm.Line().at((0, 3)).to((3, 3))
    d += (R1 := elm.Resistor().at((3, 3)).to((6, 3)))
    d += elm.Dot().at((6, 3))
    d += (R2 := elm.Resistor().at((6, 3)).to((6, 0)))
    d += elm.Dot().at((6, 0))
    d += elm.Line().at((6, 0)).to((0, 0))
    d += elm.Line().at((6, 3)).to((8, 3))
    d += elm.Line().at((8, 3)).to((8, 0))
    d += elm.Line().at((8, 0)).to((6, 0))
    finish(ax, d)
    meter(ax, (1.5, 3), 'A'); meter(ax, (8, 1.5), 'V')
    pm(ax, b, (0.45, 0))
    T(ax, mid(R1) + (0, 0.55), '$R_1$'); T(ax, mid(R2) + (-0.55, 0), '$R_2$', ha='right')
    T(ax, (1.5, 2.25), '전류계(직렬)', fontsize=8.5, color=fs.GRAY)
    T(ax, (8.6, 1.5), '전압계(병렬)', fontsize=8.5, color=fs.GRAY, ha='left')
    fs.save(fig, __file__, 'fig25_09')


def fig10():
    """휘트스톤 브리지."""
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    A, B, C, D = (0, 2.2), (0, -2.2), (-2.2, 0), (2.2, 0)
    d = circuit(ax)
    d += (r1 := elm.Resistor().at(A).to(C))
    d += (r2 := elm.Resistor().at(C).to(B))
    d += (r3 := elm.Resistor().at(A).to(D))
    d += (r4 := elm.Resistor().at(D).to(B))
    d += elm.Line().at(C).to((-0.4, 0))
    d += elm.Line().at((0.4, 0)).to(D)
    for p in (A, B, C, D):
        d += elm.Dot().at(p)
    d += elm.Line().at(A).to((0, 3.0))
    d += elm.Line().at((0, 3.0)).to((-3.4, 3.0))
    d += (e := bat((-3.4, -3.0), (-3.4, 3.0)))
    d += elm.Line().at((-3.4, -3.0)).to((0, -3.0))
    d += elm.Line().at((0, -3.0)).to(B)
    finish(ax, d, pad=0.3)
    meter(ax, (0, 0), 'G', r=0.4)
    pm(ax, e, (0.4, 0))
    for p, s, off in ((A, '$A$', (0.35, 0.15)), (B, '$B$', (0.35, -0.15)), (C, '$C$', (-0.3, -0.3)), (D, '$D$', (0.3, -0.3))):
        T(ax, np.array(p) + off, s)
    for r, s, off in ((r1, '$R_1$', (-0.45, 0.45)), (r2, '$R_2$', (-0.45, -0.45)), (r3, '$R_3$', (0.45, 0.45)), (r4, '$R_4$', (0.45, -0.45))):
        T(ax, mid(r) + off, s)
    fs.save(fig, __file__, 'fig25_10')


# ---------------------------------------------------------------- 25.6
def fig11():
    """RC 충전 회로."""
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    d = circuit(ax)
    d += (b := bat((0, 0), (0, 3)))
    d += (S := elm.Switch().at((0, 3)).to((2.5, 3)))
    d += (R := elm.Resistor().at((2.5, 3)).to((5.5, 3)))
    d += (C := elm.Capacitor().at((5.5, 3)).to((5.5, 0)))
    d += elm.Line().at((5.5, 0)).to((0, 0))
    finish(ax, d)
    pm(ax, b, (0.45, 0))
    T(ax, mid(b) + (-0.55, 0), '$\\mathcal{E}$', ha='right')
    T(ax, mid(S) + (0, 0.6), '$S$ ($t = 0$에 닫음)', fontsize=8.5)
    T(ax, mid(R) + (0, 0.55), '$R$')
    T(ax, mid(C) + (0.55, 0), '$C$', ha='left')
    T(ax, mid(C) + (-0.4, 0.3), '$+q$', fontsize=8.5, ha='right', color=fs.POS)
    T(ax, mid(C) + (-0.4, -0.3), '$-q$', fontsize=8.5, ha='right', color=fs.NEG)
    cur(ax, (3.1, 2.4), (4.4, 2.4), '$I$', loff=(0, -0.3))
    fs.save(fig, __file__, 'fig25_11')


def fig12():
    """예제 25.8: RC 충전의 q(t), I(t)."""
    tau, Q, I0 = 2.0, 10.0, 5.0     # s, μC, μA
    t = np.linspace(0, 12, 400)
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.3))
    ax = axs[0]
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.plot(t, Q * (1 - np.exp(-t / tau)), color=fs.VEL, lw=1.8)
    ax.axhline(Q, color=fs.GRAY, lw=0.8, ls='--')
    ax.plot([tau, tau], [0, Q * 0.632], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot(tau, Q * 0.632, 'o', ms=4, color=fs.VEL)
    ax.text(tau + 0.3, Q * 0.632 - 1.0, '$t = \\tau$: 63.2%', fontsize=8.5)
    t9 = tau * np.log(10)
    ax.plot(t9, 9.0, 'o', ms=4, color=fs.FORCE)
    ax.annotate('$V_C = 9.0$ V\n($t = 4.6$ s)', xy=(t9, 9.0), xytext=(6.5, 2.4), fontsize=8.5,
                arrowprops=dict(arrowstyle='-', color=fs.GRAY, lw=0.6))
    ax.text(9.0, Q + 0.4, '$C\\mathcal{E}$', fontsize=9)
    ax.set_xlim(0, 12); ax.set_ylim(0, 11.5)
    ax.set_xlabel('$t$ (s)'); ax.set_ylabel('$q$ ($\\mu$C)')
    ax.set_title('(가) 전하', fontsize=9)
    ax = axs[1]
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.plot(t, I0 * np.exp(-t / tau), color=fs.FORCE, lw=1.8)
    ax.plot([tau, tau], [0, I0 / np.e], color=fs.GRAY, lw=0.7, ls=':')
    ax.plot(tau, I0 / np.e, 'o', ms=4, color=fs.FORCE)
    ax.text(tau + 0.3, I0 / np.e + 0.2, '$I_0/e$', fontsize=8.5)
    ax.text(0.4, I0 + 0.1, '$I_0 = \\mathcal{E}/R$', fontsize=8.5)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.9)
    ax.set_xlabel('$t$ (s)'); ax.set_ylabel('$I$ ($\\mu$A)')
    ax.set_title('(나) 전류', fontsize=9)
    fig.tight_layout(w_pad=1.0)
    fs.save(fig, __file__, 'fig25_12')


# ---------------------------------------------------------------- 연습문제
def fig13():
    """연습문제 13: 전압계의 부하 효과."""
    fig, ax = plt.subplots(figsize=(3.6, 2.4))
    d = circuit(ax)
    d += (b := bat((0, 0), (0, 4)))
    d += elm.Line().at((0, 4)).to((3, 4))
    d += (Ra := elm.Resistor().at((3, 4)).to((3, 2)))
    d += elm.Dot().at((3, 2))
    d += (Rb := elm.Resistor().at((3, 2)).to((3, 0)))
    d += elm.Dot().at((3, 0))
    d += elm.Line().at((3, 0)).to((0, 0))
    d += elm.Line().at((3, 2)).to((5, 2))
    d += elm.Line().at((5, 2)).to((5, 0))
    d += elm.Line().at((5, 0)).to((3, 0))
    finish(ax, d)
    pm(ax, b, (0.45, 0))
    T(ax, mid(b) + (-0.55, 0), '$12\\ \\mathrm{V}$', ha='right')
    T(ax, mid(Ra) + (-0.5, 0), '$10\\ \\mathrm{k}\\Omega$', ha='right', fontsize=9)
    T(ax, mid(Rb) + (-0.5, 0), '$10\\ \\mathrm{k}\\Omega$', ha='right', fontsize=9)
    meter(ax, (5, 1), 'V')
    T(ax, (5.6, 1), '$R_V = 100\\ \\mathrm{k}\\Omega$', ha='left', fontsize=9)
    fs.save(fig, __file__, 'fig25_13')


def fig14():
    """연습문제 14: 무한 사다리 회로."""
    fig, ax = plt.subplots(figsize=(4.8, 1.8))
    d = circuit(ax)
    x = 0
    for k in range(3):
        d += elm.Resistor().at((x, 2)).to((x + 2.5, 2))
        d += elm.Dot().at((x + 2.5, 2))
        d += elm.Resistor().at((x + 2.5, 2)).to((x + 2.5, 0))
        d += elm.Dot().at((x + 2.5, 0))
        d += elm.Line().at((x, 0)).to((x + 2.5, 0))
        x += 2.5
    d += elm.Line().at((x, 2)).to((x + 0.8, 2))
    d += elm.Line().at((x, 0)).to((x + 0.8, 0))
    finish(ax, d, pad=0.4)
    for p, s in (((0, 2), '$a$'), ((0, 0), '$b$')):
        ax.add_patch(Circle(p, 0.1, fc='white', ec=fs.BLACK, zorder=9))
        T(ax, (p[0] - 0.35, p[1]), s)
    T(ax, (x + 1.3, 1.0), '$\\cdots$', fontsize=14)
    for k in range(3):
        T(ax, (1.25 + 2.5 * k, 2.55), '$R$', fontsize=9)
        T(ax, (2.5 + 2.5 * k + 0.5, 1.0), '$R$', fontsize=9, ha='left')
    ax.set_xlim(-0.8, x + 1.8)
    fs.save(fig, __file__, 'fig25_14')


def fig15():
    """연습문제 17: 누설 저항이 있는 축전기의 충전."""
    fig, ax = plt.subplots(figsize=(3.8, 2.2))
    d = circuit(ax)
    d += (b := bat((0, 0), (0, 3)))
    d += (R1 := elm.Resistor().at((0, 3)).to((3, 3)))
    d += elm.Dot().at((3, 3))
    d += (C := elm.Capacitor().at((3, 3)).to((3, 0)))
    d += elm.Dot().at((3, 0))
    d += elm.Line().at((3, 3)).to((5.5, 3))
    d += (R2 := elm.Resistor().at((5.5, 3)).to((5.5, 0)))
    d += elm.Line().at((5.5, 0)).to((0, 0))
    finish(ax, d)
    pm(ax, b, (0.45, 0))
    T(ax, mid(b) + (-0.55, 0), '$\\mathcal{E}$', ha='right')
    T(ax, mid(R1) + (0, 0.55), '$R_1$')
    T(ax, mid(C) + (0.55, 0), '$C$', ha='left')
    T(ax, mid(R2) + (0.55, 0), '$R_2$', ha='left')
    fs.save(fig, __file__, 'fig25_15')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15):
        f()
