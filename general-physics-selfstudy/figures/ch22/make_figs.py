"""22장 가우스 법칙 그림. python3 figures/ch22/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch, Arc, Ellipse

k = 8.99e9
CA = np.cos(np.radians(35)) * 0.5
SA = np.sin(np.radians(35)) * 0.5


def P3(x, y, z):
    """사선 투영: x 오른쪽, y 깊이(오른쪽 위로 비스듬히), z 위쪽."""
    return np.array([x + CA * y, z + SA * y])


def sign(ax, p, q, size=10, zorder=7):
    ax.text(p[0], p[1], '+' if q > 0 else '−', color=fs.POS if q > 0 else fs.NEG, ha='center', va='center',
            fontsize=size, fontweight='bold', zorder=zorder)


def styled(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def blob(cx, cy, r0, amps=((3, 0.12, 0.3), (2, 0.08, 1.0)), n=400):
    """울퉁불퉁한 닫힌 곡선(단면). 점 배열과 극좌표 함수를 돌려준다."""
    t = np.linspace(0, 2 * np.pi, n)

    def rf(tt):
        r = r0 * np.ones_like(tt)
        for m, a, ph in amps:
            r = r + r0 * a * np.cos(m * tt + ph)
        return r
    r = rf(t)
    return np.c_[cx + r * np.cos(t), cy + r * np.sin(t)], rf


def outward(cx, cy, rf, t, eps=1e-4):
    """극좌표 곡선 위 매개변수 t인 점과 바깥 법선."""
    def pt(tt):
        r = rf(np.array([tt]))[0]
        return np.array([cx + r * np.cos(tt), cy + r * np.sin(tt)])
    p = pt(t); tan = pt(t + eps) - pt(t - eps)
    n = np.array([tan[1], -tan[0]]); n /= np.linalg.norm(n)
    return p, n


def cube(ax, o, a, fc='none', alpha=0.15, lw=1.1, hidden=True, faces=None):
    """원점 o=(x,y,z), 한 변 a인 정육면체(사선 투영)."""
    x, y, z = o
    V = {(i, j, l): P3(x + i * a, y + j * a, z + l * a) for i in (0, 1) for j in (0, 1) for l in (0, 1)}
    edges = [((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 0, 1)), ((1, 0, 1), (0, 0, 1)), ((0, 0, 1), (0, 0, 0)),
             ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (1, 1, 1)), ((1, 1, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1)),
             ((0, 1, 1), (1, 1, 1))]
    back = [((0, 0, 0), (0, 1, 0)), ((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1))]
    for p, q in edges:
        ax.plot(*zip(V[p], V[q]), color=fs.BLACK, lw=lw, zorder=4)
    for p, q in back:
        ax.plot(*zip(V[p], V[q]), color=fs.GRAY, lw=0.8, ls='--' if hidden else '-', zorder=2)
    if faces:
        for face, col in faces:
            ax.add_patch(Polygon([V[c] for c in face], closed=True, fc=col, alpha=0.45, ec='none', zorder=1))
    return V


# ---------------------------------------------------------------- 22.1 평평한 면의 선속
def fig01():
    fig, ax = fs.canvas(3.8, 2.6, xlim=(-2.6, 2.9), ylim=(-1.75, 1.95))
    th = np.radians(35); s = 1.0
    n = np.array([np.cos(th), 0, np.sin(th)])
    u = np.array([-np.sin(th), 0, np.cos(th)]) * s; w = np.array([0, 1, 0]) * s
    corners = [P3(*(c1 * u + c2 * w)) for c1, c2 in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    for y in np.linspace(-1.4, 1.4, 6):
        fs.arrow(ax, (-2.5, y), (2.6, y), color=fs.FIELD, lw=0.8, ms=8, zorder=1)
    ax.add_patch(Polygon(corners, closed=True, fc=fs.SURF, alpha=0.75, ec=fs.BLACK, lw=1.1, zorder=3))
    o = P3(0, 0, 0)
    nn = P3(*n) - o
    fs.arrow(ax, o, o + 1.5 * nn, color=fs.BLACK, lw=1.6, ms=10, zorder=6)
    ax.text(*(o + 1.62 * nn + [0.1, 0.05]), r'$\hat n$', fontsize=11, zorder=6)
    ax.plot([0, 1.3], [0, 0], color=fs.BLACK, lw=0.8, ls='--', zorder=5)
    fs.angle_arc(ax, (0, 0), 0.75, 0, np.degrees(np.arctan2(nn[1], nn[0])), r'$\theta$', fontsize=10)
    ax.text(2.65, 1.4, r'$\vec E$', fontsize=11, color=fs.FIELD, va='center')
    ax.text(*(np.array(corners[0]) + [-0.25, -0.1]), '넓이 $A$', fontsize=9, ha='right', va='top', zorder=6,
            bbox=dict(fc='white', ec='none', pad=0.3))
    ax.text(-2.5, 1.75, r'$\vec A = A\hat n$', fontsize=10)
    fs.save(fig, __file__, 'fig22_01')


def fig02():
    fig, ax = fs.canvas(5.4, 2.0, xlim=(-0.3, 11.4), ylim=(-1.75, 1.95))
    for i, (deg, txt) in enumerate([(0, r'$\theta = 0$: $\Phi_E = EA$'), (60, r'$\theta$: $\Phi_E = EA\cos\theta$'),
                                    (90, r'$\theta = 90$°: $\Phi_E = 0$')]):
        cx = 1.9 + i * 3.8
        for y in np.linspace(-1.2, 1.2, 9):
            fs.arrow(ax, (cx - 1.7, y), (cx + 1.7, y), color=fs.FIELD, lw=0.7, ms=7, zorder=1)
        th = np.radians(deg)
        n = np.array([np.cos(th), np.sin(th)]); t = np.array([-np.sin(th), np.cos(th)])
        L = 1.05
        p, q = np.array([cx, 0]) - L * t, np.array([cx, 0]) + L * t
        ax.plot([p[0], q[0]], [p[1], q[1]], color=fs.BLACK, lw=3.2, solid_capstyle='butt', zorder=3)
        fs.arrow(ax, (cx, 0), (cx + 0.8 * n[0], 0.8 * n[1]), color=fs.BLACK, lw=1.4, ms=9, zorder=5)
        ax.text(cx + 0.95 * n[0] + 0.12, 0.95 * n[1] + 0.05, r'$\hat n$', fontsize=10, zorder=5)
        ax.text(cx, -1.6, txt, fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig22_02')


# ---------------------------------------------------------------- 닫힌 곡면의 바깥 법선
def fig03():
    fig, ax = fs.canvas(3.8, 2.7, xlim=(-2.7, 2.9), ylim=(-1.95, 2.0))
    for y in np.linspace(-1.6, 1.6, 7):
        fs.arrow(ax, (-2.6, y), (2.7, y), color=fs.FIELD, lw=0.7, ms=7, zorder=1)
    ax.text(2.72, 1.6, r'$\vec E$', fontsize=11, color=fs.FIELD, va='center')
    pts, rf = blob(0, 0, 1.2, amps=((3, 0.08, 0.4), (2, 0.06, 1.2)))
    ax.add_patch(Polygon(pts, closed=True, fc=fs.SURF, alpha=0.45, ec=fs.BLACK, lw=1.3, zorder=2))
    for t, txt, col, off in [(0.15, r'나감: $\vec E\cdot d\vec A > 0$', fs.FORCE, (0.1, -0.45)),
                             (np.pi + 0.25, r'들어옴: $\vec E\cdot d\vec A < 0$', fs.VEL, (-0.1, 0.62)),
                             (np.pi / 2 + 0.1, r'스침: $\vec E\cdot d\vec A = 0$', fs.GRAY, (0.0, 0.55))]:
        p, n = outward(0, 0, rf, t)
        fs.arrow(ax, p, p + 0.75 * n, color=fs.BLACK, lw=1.5, ms=10, zorder=6)
        ax.plot(*p, 'ko', ms=3, zorder=6)
        ax.text(p[0] + 0.75 * n[0] + off[0], p[1] + 0.75 * n[1] + off[1], txt, fontsize=8.5, color=col,
                ha='center', va='center', bbox=dict(fc='white', ec='none', pad=0.4), zorder=7)
    ax.text(0.05, -0.3, '닫힌 곡면 $S$', fontsize=9, ha='center', zorder=6)
    ax.text(0.05, -0.75, r'$d\vec A$는 바깥쪽', fontsize=8.5, ha='center', zorder=6)
    fs.save(fig, __file__, 'fig22_03')


# ---------------------------------------------------------------- 균일한 장 속 정육면체
def fig04():
    fig, ax = fs.canvas(4.0, 2.4, xlim=(-2.3, 3.6), ylim=(-0.9, 2.3))
    a = 1.6
    V = cube(ax, (0, 0, 0), a, faces=[([(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)], fs.VEL),
                                     ([(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)], fs.FORCE)])
    for z in (0.35, 1.25):
        for yy in (0.4, 1.2):
            p0 = P3(-1.2, yy, z); p1 = P3(a + 1.2, yy, z)
            fs.arrow(ax, p0, p1, color=fs.FIELD, lw=0.9, ms=8, zorder=5)
    ax.text(-2.2, 1.95, '왼쪽 면: $-EA$', fontsize=9, color=fs.VEL)
    ax.text(3.55, -0.25, '오른쪽 면: $+EA$', fontsize=9, color=fs.FORCE, ha='right')
    ax.text(0.6, -0.75, '나머지 네 면: 0  →  총 선속 0', fontsize=9, ha='center')
    ax.text(*(P3(a + 1.25, 1.2, 1.25) + [0.1, 0]), r'$\vec E$', fontsize=10, color=fs.FIELD, va='center')
    fs.save(fig, __file__, 'fig22_04')


# ---------------------------------------------------------------- 예제 22.1
def fig05():
    fig, ax = fs.canvas(4.0, 2.7, xlim=(-1.0, 4.4), ylim=(-0.8, 2.9))
    a = 1.8
    o = P3(0, 0, 0)
    fs.arrow(ax, o, P3(a + 1.9, 0, 0), color=fs.GRAY, lw=0.8, ms=8); ax.text(*(P3(a + 2.0, 0, 0) + [0, -0.05]), '$x$', fontsize=10, va='center')
    fs.arrow(ax, o, P3(0, a + 0.9, 0), color=fs.GRAY, lw=0.8, ms=8); ax.text(*(P3(0, a + 1.0, 0)), '$y$', fontsize=10)
    fs.arrow(ax, o, P3(0, 0, a + 0.6), color=fs.GRAY, lw=0.8, ms=8); ax.text(*(P3(0, 0, a + 0.7) + [-0.1, 0]), '$z$', fontsize=10, ha='right')
    cube(ax, (0, 0, 0), a, faces=[([(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)], fs.FORCE)])
    sc = 0.33
    for xx in (0.0, a / 3, 2 * a / 3, a):
        for z in (a * 0.3, a * 0.75):
            p = P3(xx, 0, z)
            L = sc * xx
            if L > 0.01:
                fs.arrow(ax, p, p + [L, 0], color=fs.FIELD, lw=1.3, ms=8, zorder=6)
            else:
                ax.plot(*p, 'o', color=fs.FIELD, ms=3, zorder=6)
    ax.text(*(P3(0, 0, 0) + [-0.1, -0.45]), '$x=0$: $E=0$', fontsize=8.5, ha='center', va='top')
    ax.text(*(P3(a, 0, 0) + [0.25, -0.45]), '$x=a$: $E_x=ba$', fontsize=8.5, ha='center', va='top')
    ax.text(*(P3(a, 0, a) + [-0.6, 0.15]), r'$\vec E = bx\,\hat i$', fontsize=10, color=fs.FIELD)
    ax.text(a / 2, -0.12, '$a$', fontsize=10, ha='center', va='top')
    fs.save(fig, __file__, 'fig22_05')


# ---------------------------------------------------------------- 예제 22.2
def fig06():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-0.6, 5.4), ylim=(-1.9, 1.9))
    d, R = 3.2, 1.6
    fs.charge(ax, (0, 0), +1, r=0.15); ax.text(0, -0.32, '$q$', fontsize=10, ha='center', va='top')
    ax.plot([-0.3, 4.8], [0, 0], color=fs.GRAY, lw=0.6, ls='-.')
    ax.add_patch(Ellipse((d, 0), 0.5, 2 * R, fc=fs.SURF, alpha=0.6, ec=fs.BLACK, lw=1.1, zorder=2))
    ax.plot([0, d], [0, R], color=fs.GRAY, lw=0.6, ls=':'); ax.plot([0, d], [0, -R], color=fs.GRAY, lw=0.6, ls=':')
    r = 0.95
    ax.add_patch(Ellipse((d, 0), 0.5 * r / R, 2 * r, fc='none', ec=fs.FORCE, lw=2.2, zorder=3))
    P = np.array([d, r])
    ax.plot([0, P[0]], [0, P[1]], color=fs.BLACK, lw=0.8, ls='--')
    u = P / np.linalg.norm(P)
    fs.vec(ax, P, 1.25 * u, color=fs.FIELD, lw=1.5, label=r'$\vec E$', lpos=1, loff=(0.2, 0.12), zorder=6)
    fs.vec(ax, P, (1.25, 0), color=fs.BLACK, lw=1.3, label=r'$\hat n$', lpos=1, loff=(0.2, -0.05), zorder=6)
    fs.angle_arc(ax, P, 0.85, 0, np.degrees(np.arctan2(u[1], u[0])))
    ax.text(P[0] + 0.95, P[1] + 0.09, r'$\theta$', fontsize=9.5, va='center')
    ax.text(1.45, 0.62, r'$\sqrt{r^2+d^2}$', fontsize=9, ha='center', rotation=0)
    fs.dim(ax, (0, -1.3), (d, -1.3), '$d$', off=0.0, color=fs.BLACK)
    ax.annotate('', xy=(d - 0.35, r), xytext=(d - 0.35, 0),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(d - 0.45, r / 2, '$r$', fontsize=10, ha='right', va='center')
    ax.text(d + 0.35, -R + 0.1, '$R$', fontsize=10)
    ax.annotate('고리(폭 $dr$)', xy=(d + 0.12, -0.75), xytext=(d + 0.55, -0.6), fontsize=8.5, color=fs.FORCE,
                ha='left', va='center', arrowprops=dict(arrowstyle='->', color=fs.FORCE, lw=0.7))
    fs.save(fig, __file__, 'fig22_06')


# ---------------------------------------------------------------- 가우스 법칙: 여러 닫힌 곡면
def fig07():
    fig, ax = fs.canvas(4.8, 3.2, xlim=(-3.2, 3.2), ylim=(-2.15, 2.15))
    fs.field_lines(ax, [(-1.0, 0, 1), (1.0, 0, -1)], (-3.2, 3.2), (-2.15, 2.15), per_unit=14, lw=0.7)
    fs.charge(ax, (-1.0, 0), +1, r=0.16); fs.charge(ax, (1.0, 0), -1, r=0.16)
    surfs = [((-1.0, 0.0, 0.55), ((3, 0.12, 0.3),), fs.FORCE, '-', '$S_1$', (-1.2, 0.75)),
             ((1.0, 0.0, 0.55), ((3, 0.12, 1.3),), fs.VEL, '-', '$S_2$', (1.2, 0.75)),
             ((0.0, 0.0, 1.75), ((2, 0.18, 0.0), (3, 0.05, 0.5)), fs.ACC, '--', '$S_3$', (0, 1.25)),
             ((-2.35, 1.3, 0.45), ((3, 0.12, 0.0),), fs.ORANGE, '-', '$S_4$', (-2.35, 1.95))]
    for (cx, cy, r0), amps, col, ls, lab, lp in surfs:
        pts, _ = blob(cx, cy, r0, amps=amps)
        if lab == '$S_3$':
            pts[:, 1] = pts[:, 1] * 0.7
        ax.plot(pts[:, 0], pts[:, 1], color=col, lw=1.8, ls=ls, zorder=3)
        ax.text(*lp, lab, fontsize=10.5, color=col, ha='center', va='center', zorder=8,
                bbox=dict(fc='white', ec='none', pad=0.3))
    ax.text(-3.1, -1.95, r'$\Phi_1 = +q/\varepsilon_0$,  $\Phi_2 = -q/\varepsilon_0$,  $\Phi_3 = 0$,  $\Phi_4 = 0$',
            fontsize=9, ha='left', bbox=dict(fc='white', ec='none', pad=0.5), zorder=8)
    fs.save(fig, __file__, 'fig22_07')


# ---------------------------------------------------------------- 입체각
def fig08():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-0.4, 5.3), ylim=(-1.05, 2.2))
    fs.charge(ax, (0, 0), +1, r=0.13); ax.text(0.0, -0.28, '$q$', fontsize=10, ha='center', va='top')
    a1, a2 = np.radians(16), np.radians(30)
    r = 3.6
    # 기울어진 면 조각 dA: 반지름 r 근처, 법선이 r̂와 각 α를 이룸
    m = np.radians(23); alpha = np.radians(40)
    c = r * np.array([np.cos(m), np.sin(m)])
    nvec = np.array([np.cos(m - alpha), np.sin(m - alpha)])
    tvec = np.array([-nvec[1], nvec[0]])
    # 조각의 양 끝: 원점에서 각 a1, a2인 반직선과의 교점
    def hit(a):
        d = np.array([np.cos(a), np.sin(a)])
        s = np.dot(c, nvec) / np.dot(d, nvec)
        return s * d
    e1, e2 = hit(a1), hit(a2)
    for e in (e1, e2):
        ax.plot([0, e[0] * 1.12], [0, e[1] * 1.12], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([e1[0], e2[0]], [e1[1], e2[1]], color=fs.BLACK, lw=3.0, solid_capstyle='butt', zorder=4)
    rr = np.linalg.norm(c)
    t = np.linspace(a1, a2, 50)
    ax.plot(rr * np.cos(t), rr * np.sin(t), color=fs.ACC, lw=2.2, zorder=3)
    t2 = np.linspace(0.0, np.radians(50), 100)
    ax.plot(rr * np.cos(t2), rr * np.sin(t2), color=fs.ACC, lw=0.6, ls=':')
    ax.plot(1.0 * np.cos(t), 1.0 * np.sin(t), color=fs.FIELD, lw=2.4)
    ax.plot(1.0 * np.cos(t2), 1.0 * np.sin(t2), color=fs.FIELD, lw=0.6, ls=':')
    mid = (e1 + e2) / 2
    fs.arrow(ax, mid, mid + 0.9 * nvec, color=fs.BLACK, lw=1.4, ms=9, zorder=6)
    ax.text(*(mid + 1.0 * nvec + [0.12, -0.05]), r'$\hat n$', fontsize=10)
    rh = mid / np.linalg.norm(mid)
    ax.plot([mid[0], mid[0] + 0.9 * rh[0]], [mid[1], mid[1] + 0.9 * rh[1]], color=fs.GRAY, lw=0.8)
    ax.text(*(mid + 0.95 * rh + [0.05, 0.12]), r'$\hat r$', fontsize=10)
    ax.text(*(mid + [0.15, -0.35]), '$dA$', fontsize=10)
    ax.text(rr * np.cos(a2) - 0.15, rr * np.sin(a2) + 0.15, r'$dA\cos\alpha$', fontsize=9, color=fs.ACC, ha='right')
    ax.text(1.05 * np.cos(a2) - 0.05, 1.05 * np.sin(a2) + 0.1, r'$d\Omega$', fontsize=10, color=fs.FIELD, ha='right')
    ax.text(0.7, -0.3, '반지름 1', fontsize=8, color=fs.FIELD, ha='center', va='top')
    ax.text(rr + 0.05, 0.45, '반지름 $r$', fontsize=8, color=fs.ACC, ha='left', va='center')
    ax.text(3.7, -0.55, r'$d\Omega = \dfrac{dA\cos\alpha}{r^2} = \dfrac{\hat r\cdot d\vec A}{r^2}$', fontsize=9.5,
            ha='center', va='center')
    fs.save(fig, __file__, 'fig22_08')


# ---------------------------------------------------------------- 밖에 있는 전하
def fig09():
    fig, ax = fs.canvas(4.2, 2.3, xlim=(-0.5, 5.6), ylim=(-1.5, 1.8))
    fs.charge(ax, (0, 0), +1, r=0.13); ax.text(0, -0.28, '$q$', fontsize=10, ha='center', va='top')
    pts, rf = blob(3.4, 0.0, 1.25, amps=((3, 0.07, 0.4), (2, 0.06, 1.2)))
    ax.add_patch(Polygon(pts, closed=True, fc=fs.SURF, alpha=0.45, ec=fs.BLACK, lw=1.2, zorder=2))
    a1, a2 = np.radians(6), np.radians(14)
    for a in (a1, a2):
        ax.plot([0, 5.4 * np.cos(a)], [0, 5.4 * np.sin(a)], color=fs.GRAY, lw=0.7, ls='--', zorder=3)
    # 곡면과 반직선의 교점
    def crossings(a):
        d = np.array([np.cos(a), np.sin(a)])
        s = np.linspace(0.5, 5.5, 4000)
        P = s[:, None] * d
        inside = np.array([np.hypot(*(p - [3.4, 0])) < rf(np.array([np.arctan2(p[1], p[0] - 3.4)]))[0] for p in P])
        idx = np.where(np.diff(inside.astype(int)) != 0)[0]
        return P[idx]
    c1, c2 = crossings(a1), crossings(a2)
    for k_, (lab, col, sgn) in enumerate([('들어감: $d\\Phi<0$', fs.VEL, -1), ('나옴: $d\\Phi>0$', fs.FORCE, 1)]):
        p, q = c1[k_], c2[k_]
        ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=3.0, zorder=5)
        mid = (p + q) / 2
        tt = np.arctan2(mid[1], mid[0] - 3.4)
        _, n = outward(3.4, 0.0, rf, tt)
        fs.arrow(ax, mid, mid + 0.6 * n, color=fs.BLACK, lw=1.2, ms=8, zorder=6)
        ax.text(mid[0] + 0.6 * n[0] + 0.05 * sgn, mid[1] + 0.6 * n[1] + 0.35, lab, fontsize=8.5, color=col,
                ha='center', zorder=7, bbox=dict(fc='white', ec='none', pad=0.3))
    ax.text(1.3, 0.02, r'같은 $d\Omega$', fontsize=8.5, ha='center', va='top')
    fs.save(fig, __file__, 'fig22_09')


# ---------------------------------------------------------------- 예제 22.3 구형 가우스 면
def fig10():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-2.3, 2.5), ylim=(-2.2, 2.3))
    R = 1.5
    fs.sphere(ax, (0, 0), R)
    fs.charge(ax, (0, 0), +1, r=0.15)
    ax.text(0.2, -0.22, '$q$', fontsize=10)
    for a in range(20, 360, 45):
        if a == 110:
            continue
        t = np.radians(a)
        p = R * np.array([np.cos(t), np.sin(t)])
        fs.arrow(ax, p, 1.45 * p, color=fs.FIELD, lw=1.2, ms=8, zorder=5)
    t = np.radians(65); p = R * np.array([np.cos(t), np.sin(t)])
    ax.plot([0, p[0]], [0, p[1]], color=fs.BLACK, lw=0.8)
    ax.text(p[0] / 2 - 0.15, p[1] / 2 + 0.05, '$r$', fontsize=10, ha='right')
    ax.text(1.55 * np.cos(np.radians(20)) + 0.1, 1.55 * np.sin(np.radians(20)) + 0.12, r'$\vec E$', fontsize=10,
            color=fs.FIELD)
    t = np.radians(110); p = R * np.array([np.cos(t), np.sin(t)])
    fs.arrow(ax, p, p + 0.55 * p / R, color=fs.BLACK, lw=1.5, ms=9, zorder=6)
    ax.text(p[0] + 0.62 * p[0] / R - 0.1, p[1] + 0.62 * p[1] / R + 0.05, r'$d\vec A$', fontsize=10, ha='right')
    ax.text(-1.25, -2.05, '가우스 면(구면)', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig22_10')


# ---------------------------------------------------------------- 정전기 평형의 도체
def fig11():
    fig, ax = fs.canvas(3.8, 2.6, xlim=(-2.6, 2.9), ylim=(-1.85, 1.95))
    pts, rf = blob(0, 0, 1.35, amps=((2, 0.18, 0.0), (3, 0.06, 0.8)))
    ax.add_patch(Polygon(pts, closed=True, fc='#d9dee5', ec=fs.BLACK, lw=1.4, zorder=2))
    ins = np.c_[pts[:, 0] * 0.83, pts[:, 1] * 0.83]
    ax.plot(ins[:, 0], ins[:, 1], color=fs.ACC, lw=1.4, ls='--', zorder=3)
    for t in np.linspace(0, 2 * np.pi, 18, endpoint=False):
        p, n = outward(0, 0, rf, t)
        sign(ax, p - 0.1 * n, +1, size=8)
        if int(round(t / (2 * np.pi / 18))) % 2 == 0:
            fs.arrow(ax, p + 0.05 * n, p + 0.5 * n, color=fs.FIELD, lw=1.0, ms=7, zorder=5)
    ax.text(0, 0.15, r'도체 속 $\vec E = 0$', fontsize=9.5, ha='center')
    ax.text(0, -0.3, r'$q_{\mathrm{in}} = 0$', fontsize=9.5, ha='center', color=fs.ACC)
    ax.annotate('가우스 면\n(표면 바로 안쪽)', xy=(ins[60, 0], ins[60, 1]), xytext=(1.9, 1.55), fontsize=8.5,
                color=fs.ACC, ha='center', arrowprops=dict(arrowstyle='->', color=fs.ACC, lw=0.7))
    ax.text(-2.5, -1.7, '표면에 수직인 $\\vec E$', fontsize=8.5, color=fs.FIELD)
    fs.save(fig, __file__, 'fig22_11')


# ---------------------------------------------------------------- 도체 표면의 필박스
def fig12():
    fig, ax = fs.canvas(3.8, 2.6, xlim=(-2.6, 2.8), ylim=(-1.75, 1.95))
    ax.add_patch(Polygon([(-2.5, 0), (2.0, 0), (2.7, 0.35), (-1.8, 0.35), (-1.8, -1.6), (-2.5, -1.6)],
                         closed=True, fc='none', ec='none'))
    ax.add_patch(Polygon([(-2.5, -1.6), (2.0, -1.6), (2.0, 0), (-2.5, 0)], closed=True, fc='#d9dee5', ec='none', zorder=0))
    ax.add_patch(Polygon([(-2.5, 0), (2.0, 0), (2.7, 0.45), (-1.8, 0.45)], closed=True, fc='#c3cad4', ec=fs.BLACK,
                         lw=0.8, zorder=0))
    ax.plot([2.0, 2.0, 2.7, 2.7], [-1.6, 0, 0.45, -1.15], color=fs.BLACK, lw=0.8, zorder=0)
    for x in np.linspace(-2.2, 2.3, 9):
        sign(ax, (x + 0.15, 0.22), +1, size=8, zorder=1)
    fs.cylinder(ax, (0.1, 0.22), 0.55, 1.6, ry=0.16)
    for x in (-0.3, 0.1, 0.5):
        fs.arrow(ax, (x, 1.1), (x, 1.85), color=fs.FIELD, lw=1.2, ms=8, zorder=6)
    ax.text(0.75, 1.6, r'$\vec E$ (표면에 수직)', fontsize=9, color=fs.FIELD, ha='left')
    ax.text(-0.75, 1.05, '넓이 $A$', fontsize=9, ha='right')
    ax.text(-1.0, -1.15, r'도체 속: $\vec E = 0$', fontsize=9, ha='center')
    ax.text(2.75, 0.2, r'$\sigma$', fontsize=11, color=fs.POS, ha='left')
    ax.annotate('필박스(가우스 면)', xy=(0.65, -0.3), xytext=(1.1, -1.15), fontsize=8.5, ha='left',
                arrowprops=dict(arrowstyle='->', lw=0.7))
    fs.save(fig, __file__, 'fig22_12')


# ---------------------------------------------------------------- 공동이 있는 도체
def fig13():
    fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.6))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.9, 2.0)
    # (가) 빈 공동
    ax = axs[0]
    pts, rf = blob(0, 0, 1.5, amps=((2, 0.12, 0.2), (3, 0.05, 1.0)))
    ax.add_patch(Polygon(pts, closed=True, fc='#d9dee5', ec=fs.BLACK, lw=1.3, zorder=1))
    cav, rc = blob(-0.15, 0.05, 0.6, amps=((3, 0.12, 0.5),))
    ax.add_patch(Polygon(cav, closed=True, fc='white', ec=fs.BLACK, lw=1.1, zorder=2))
    g, _ = blob(-0.15, 0.05, 0.9, amps=((3, 0.08, 0.5),))
    ax.plot(g[:, 0], g[:, 1], color=fs.ACC, lw=1.2, ls='--', zorder=3)
    for t in np.linspace(0, 2 * np.pi, 14, endpoint=False):
        p, n = outward(0, 0, rf, t)
        sign(ax, p - 0.12 * n, +1 if np.cos(t) > 0 else -1, size=8)
    fs.arrow(ax, (-1.95, -1.7), (-1.5, -1.7), color=fs.FIELD, lw=1.0, ms=7)
    ax.text(-1.45, -1.7, r'바깥 장 $\vec E$', fontsize=8, color=fs.FIELD, va='center')
    ax.text(-0.15, 0.05, '$E=0$', fontsize=9, ha='center', va='center', zorder=4)
    ax.set_title('(가) 빈 공동: 장이 없음', fontsize=9)
    # (나) 공동 속 전하
    ax = axs[1]
    ax.add_patch(Circle((0, 0), 1.6, fc='#d9dee5', ec=fs.BLACK, lw=1.3, zorder=1))
    cc = np.array([-0.15, 0.1]); rcav = 0.75
    ax.add_patch(Circle(cc, rcav, fc='white', ec=fs.BLACK, lw=1.1, zorder=2))
    qpos = cc + [0.32, 0.15]
    fs.charge(ax, qpos, +1, r=0.12)
    ax.text(qpos[0], qpos[1] - 0.24, '$q$', fontsize=9.5, ha='center', va='top', zorder=8)
    # 공동 벽의 -q: 전하에 가까운 쪽에 더 촘촘히
    ang = np.arctan2(*(qpos - cc)[::-1])
    for t in ang + np.sign(np.linspace(-1, 1, 11)) * np.pi * np.abs(np.linspace(-1, 1, 11)) ** 1.6:
        p = cc + (rcav + 0.12) * np.array([np.cos(t), np.sin(t)])
        sign(ax, p, -1, size=8)
    for t in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        sign(ax, 1.47 * np.array([np.cos(t), np.sin(t)]), +1, size=8)
    g = 1.18
    ax.add_patch(Circle((0, 0), g, fc='none', ec=fs.ACC, lw=1.2, ls='--', zorder=3))
    ax.text(0.0, -1.85, '벽: $-q$,  바깥 표면: $Q+q$', fontsize=8.5, ha='center')
    ax.set_title('(나) 공동 속 전하 $q$', fontsize=9)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig22_13')


# ---------------------------------------------------------------- 예제 22.4 구조
def fig14():
    fig, ax = fs.canvas(3.4, 3.2, xlim=(-2.3, 2.6), ylim=(-2.3, 2.3))
    a, b = 1.0, 1.5
    ax.add_patch(Circle((0, 0), b, fc='#d9dee5', ec=fs.BLACK, lw=1.2, zorder=1))
    ax.add_patch(Circle((0, 0), a, fc='white', ec=fs.BLACK, lw=1.1, zorder=2))
    fs.charge(ax, (0, 0), +1, r=0.12)
    for t in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        sign(ax, (a + 0.1) * np.array([np.cos(t), np.sin(t)]), -1, size=8)
    for t in np.linspace(0, 2 * np.pi, 4, endpoint=False) + 0.4:
        sign(ax, (b - 0.1) * np.array([np.cos(t), np.sin(t)]), +1, size=8)
    for r, lab, ang in [(0.5, '0.050 m', 200), (1.2, '0.12 m', 235), (2.0, '0.20 m', 300)]:
        ax.add_patch(Circle((0, 0), r, fc='none', ec=fs.ACC, lw=1.2, ls='--', zorder=4))
        t = np.radians(ang)
        ax.text((r + 0.08) * np.cos(t), (r + 0.08) * np.sin(t), lab, fontsize=8, color=fs.ACC,
                ha='center', va='center', bbox=dict(fc='white', ec='none', pad=0.2), zorder=6)
    ax.plot([0, a * np.cos(np.radians(60))], [0, a * np.sin(np.radians(60))], color=fs.BLACK, lw=0.7, zorder=5)
    ax.text(0.25, 0.6, '$a$', fontsize=10, zorder=6)
    ax.plot([0, b * np.cos(np.radians(12))], [0, b * np.sin(np.radians(12))], color=fs.BLACK, lw=0.7, zorder=5)
    ax.text(1.3, 0.12, '$b$', fontsize=10, zorder=6, va='bottom')
    ax.text(-2.25, 2.1, '중심 $q=+5.0$ nC\n안쪽 표면 $-5.0$ nC\n바깥 표면 $+2.0$ nC', fontsize=8, ha='left', va='top',
            linespacing=1.4)
    fs.save(fig, __file__, 'fig22_14')


def fig15():
    fig, ax = fs.plot_axes(4.0, 2.6)
    q, Qo, a, b = 5e-9, 2e-9, 0.10, 0.15
    r1 = np.linspace(0.035, a, 200); r3 = np.linspace(b, 0.30, 200)
    ax.plot(r1, k * q / r1 ** 2 / 1e3, color=fs.FIELD, lw=1.8)
    ax.plot([a, a, b, b], [k * q / a ** 2 / 1e3, 0, 0, k * Qo / b ** 2 / 1e3], color=fs.FIELD, lw=1.8)
    ax.plot(r3, k * Qo / r3 ** 2 / 1e3, color=fs.FIELD, lw=1.8)
    ax.axvspan(a, b, color='#d9dee5', alpha=0.7, lw=0)
    ax.text((a + b) / 2, 22, '도체', fontsize=9, ha='center')
    for r, txt, off in [(0.05, '18', (0.006, 0)), (0.12, '0', (0, 1.2)), (0.20, '0.45', (0, 1.5))]:
        E = k * (q if r < a else (0 if r < b else Qo)) / r ** 2 / 1e3
        ax.plot(r, E, 'ko', ms=4, zorder=5)
        ax.text(r + off[0], E + off[1], txt, fontsize=8.5, ha='left' if off[0] else 'center')
    ax.set_xlim(0, 0.30); ax.set_ylim(0, 26)
    ax.set_xlabel('$r$ (m)'); ax.set_ylabel(r'$E$ ($10^3$ N/C)')
    fs.save(fig, __file__, 'fig22_15')


# ---------------------------------------------------------------- 예제 22.5 균일한 구
def fig16():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-2.3, 2.6), ylim=(-2.25, 2.2))
    R = 1.2
    ax.add_patch(Circle((0, 0), R, fc='#f3c9c2', ec=fs.BLACK, lw=1.2, zorder=1))
    ax.text(-0.45, 0.75, r'$\rho$ 균일', fontsize=9, ha='center', zorder=6)
    for r, col, lab, ang in [(0.7, fs.ACC, r'$r<R$', 250), (1.85, fs.VEL, r'$r>R$', 215)]:
        ax.add_patch(Circle((0, 0), r, fc='none', ec=col, lw=1.4, ls='--', zorder=4))
        t = np.radians(ang)
        ax.text((r + 0.02) * np.cos(t), (r + 0.02) * np.sin(t), lab, fontsize=9, color=col, ha='center',
                va='center', bbox=dict(fc='white', ec='none', pad=0.2), zorder=6)
    ax.plot([0, R * np.cos(np.radians(40))], [0, R * np.sin(np.radians(40))], color=fs.BLACK, lw=0.8, zorder=5)
    ax.text(0.62, 0.32, '$R$', fontsize=10, zorder=6)
    ax.annotate(r'$q_{\mathrm{in}} = Q\,r^3/R^3$', xy=(0.7 * np.cos(np.radians(-30)), 0.7 * np.sin(np.radians(-30))),
                xytext=(1.0, -2.05), fontsize=8.5, color=fs.ACC, ha='left', va='center',
                arrowprops=dict(arrowstyle='->', color=fs.ACC, lw=0.7))
    ax.text(1.45, 1.8, r'$q_{\mathrm{in}} = Q$', fontsize=9, color=fs.VEL, ha='left')
    fs.save(fig, __file__, 'fig22_16')


def fig17():
    fig, ax = fs.plot_axes(4.0, 2.6)
    x1 = np.linspace(0, 1, 100); x2 = np.linspace(1, 3, 200)
    ax.plot(x1, x1, color=fs.FIELD, lw=1.8, label=r'균일한 구: $\propto r$ (안), $1/r^2$ (밖)')
    ax.plot(x1, x1 ** 2, color=fs.ORANGE, lw=1.8, ls='--', label=r'$\rho\propto r$: $\propto r^2$ (안)')
    ax.plot(x2, 1 / x2 ** 2, color=fs.FIELD, lw=1.8)
    ax.axvline(1, color=fs.GRAY, lw=0.7, ls=':')
    ax.set_xlim(0, 3); ax.set_ylim(0, 1.15)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(['0', '$R$', '$2R$', '$3R$'])
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', '', r'$kQ/R^2$'])
    ax.set_xlabel('$r$'); ax.set_ylabel('$E$')
    ax.legend(fontsize=8.5, frameon=False, loc='upper right')
    fs.save(fig, __file__, 'fig22_17')


# ---------------------------------------------------------------- 무한 선전하
def fig18():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-2.2, 2.6), ylim=(-2.1, 2.2))
    ax.plot([0, 0], [-2.05, 2.1], color=fs.POS, lw=2.4, zorder=2)
    for y in np.linspace(-1.9, 1.9, 13):
        sign(ax, (-0.15, y), +1, size=7, zorder=2)
    r, h = 0.95, 2.4
    fs.cylinder(ax, (0, 0), r, h, ry=0.28)
    for y in (-0.7, 0.0, 0.7):
        fs.arrow(ax, (r, y), (r + 0.75, y), color=fs.FIELD, lw=1.3, ms=8, zorder=6)
        fs.arrow(ax, (-r, y), (-r - 0.75, y), color=fs.FIELD, lw=1.3, ms=8, zorder=6)
    fs.arrow(ax, (0.25, h / 2), (0.85, h / 2 + 0.05), color=fs.FIELD, lw=1.0, ms=7, zorder=6)
    ax.text(1.0, h / 2 + 0.35, '윗면: $\\vec E$가 면과 나란\n→ 선속 0', fontsize=8, ha='left', va='center')
    ax.plot([0, r], [-0.35, -0.35], color=fs.BLACK, lw=0.8, zorder=5)
    ax.text(r / 2, -0.32, '$r$', fontsize=10, ha='center', va='bottom', zorder=6)
    fs.dim(ax, (-r - 0.05, -h / 2), (-r - 0.05, h / 2), '$L$', off=0.45, color=fs.BLACK)
    ax.text(0.15, -1.95, r'$\lambda$', fontsize=11, color=fs.POS)
    ax.text(r + 0.8, -0.35, r'$\vec E$', fontsize=10, color=fs.FIELD, ha='left')
    fs.save(fig, __file__, 'fig22_18')


# ---------------------------------------------------------------- 동축 케이블
def fig19():
    fig = plt.figure(figsize=(5.4, 2.5))
    ax = fig.add_axes([0.0, 0.02, 0.44, 0.96]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.1)
    a, b, c = 0.45, 1.3, 1.65
    ax.add_patch(Circle((0, 0), c, fc='#d9dee5', ec=fs.BLACK, lw=1.2))
    ax.add_patch(Circle((0, 0), b, fc='white', ec=fs.BLACK, lw=1.1))
    ax.add_patch(Circle((0, 0), a, fc='#d9dee5', ec=fs.BLACK, lw=1.1))
    for t in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        sign(ax, (a - 0.12) * np.array([np.cos(t), np.sin(t)]), +1, size=7)
        sign(ax, (b + 0.1) * np.array([np.cos(t + 0.2), np.sin(t + 0.2)]), -1, size=7)
    for t in np.linspace(0, 2 * np.pi, 8, endpoint=False) + 0.4:
        fs.arrow(ax, 0.55 * np.array([np.cos(t), np.sin(t)]), 1.15 * np.array([np.cos(t), np.sin(t)]),
                 color=fs.FIELD, lw=0.9, ms=7)
    for r in (0.85, 1.9):
        ax.add_patch(Circle((0, 0), r, fc='none', ec=fs.ACC, lw=1.1, ls='--'))
    for r, lab, ang in [(a, '$a$', 90), (b, '$b$', 120), (c, '$c$', 150)]:
        t = np.radians(ang)
        ax.plot([0, r * np.cos(t)], [0, r * np.sin(t)], color=fs.BLACK, lw=0.6)
        ax.text((r + 0.0) * np.cos(t) + 0.02, (r + 0.0) * np.sin(t) + 0.15, lab, fontsize=9, ha='center',
                bbox=dict(fc='white', ec='none', pad=0.1))
    ax.text(0, -2.05, r'$+\lambda$ (안), $-\lambda$ (바깥 도체 안쪽 면)', fontsize=8, ha='center')
    ax2 = fig.add_axes([0.55, 0.2, 0.43, 0.72]); styled(ax2)
    r = np.linspace(a, b, 100)
    ax2.plot([0, a], [0, 0], color=fs.FIELD, lw=1.8)
    ax2.plot(r, a / r, color=fs.FIELD, lw=1.8)
    ax2.plot([b, b, 2.4], [a / b, 0, 0], color=fs.FIELD, lw=1.8)
    for lo, hi in [(0, a), (b, c)]:
        ax2.axvspan(lo, hi, color='#d9dee5', alpha=0.8, lw=0)
    ax2.set_xticks([a, b, c]); ax2.set_xticklabels(['$a$', '$b$', '$c$'])
    ax2.set_yticks([]); ax2.set_xlim(0, 2.4); ax2.set_ylim(0, 1.15)
    ax2.text(0.85, 0.75, r'$\dfrac{\lambda}{2\pi\varepsilon_0 r}$', fontsize=10, color=fs.FIELD)
    ax2.set_xlabel('$r$'); ax2.set_ylabel('$E$')
    fs.save(fig, __file__, 'fig22_19')


# ---------------------------------------------------------------- 무한 평면
def fig20():
    fig, ax = fs.canvas(3.8, 2.6, xlim=(-2.6, 2.8), ylim=(-1.8, 1.95))
    # 평면(비스듬히 본 세로 판)
    ax.add_patch(Polygon([(-0.55, -1.7), (0.35, -1.1), (0.35, 1.85), (-0.55, 1.25)], closed=True, fc='#f3c9c2',
                         ec=fs.BLACK, lw=0.9, alpha=0.8, zorder=1))
    for y in np.linspace(-1.3, 1.4, 7):
        for x in (-0.35, 0.1):
            sign(ax, (x, y + 0.3 * (x + 0.55)), +1, size=7, zorder=2)
    fs.cylinder(ax, (0, 0.05), 0.5, 2.6, vertical=False, ry=0.2)
    for x0, d in [(1.3, 1), (-1.3, -1)]:
        for y in (-0.2, 0.3):
            fs.arrow(ax, (x0, y), (x0 + 0.85 * d, y), color=fs.FIELD, lw=1.2, ms=8, zorder=6)
    ax.text(2.2, 0.75, r'$\vec E$', fontsize=10, color=fs.FIELD, ha='center')
    ax.text(-2.2, 0.75, r'$\vec E$', fontsize=10, color=fs.FIELD, ha='center')
    ax.text(1.35, -0.75, '밑면 넓이 $A$', fontsize=8.5, ha='center')
    ax.text(0.45, 1.65, r'$\sigma$', fontsize=11, color=fs.POS)
    ax.text(0.9, 1.25, '옆면: 선속 0', fontsize=8.5, ha='left')
    fs.save(fig, __file__, 'fig22_20')


# ---------------------------------------------------------------- 예제 22.8 (나) 두꺼운 판
def fig21():
    fig = plt.figure(figsize=(5.4, 2.4))
    ax = fig.add_axes([0.0, 0.05, 0.45, 0.9]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.6, 1.8)
    d = 0.9
    ax.add_patch(Rectangle((-d, -1.4), 2 * d, 2.9, fc='#f3c9c2', ec='none', zorder=0))
    ax.plot([-d, -d], [-1.4, 1.5], color=fs.BLACK, lw=0.8); ax.plot([d, d], [-1.4, 1.5], color=fs.BLACK, lw=0.8)
    rng = np.random.default_rng(5)
    for _ in range(18):
        sign(ax, (rng.uniform(-d + 0.1, d - 0.1), rng.uniform(-1.3, 1.4)), +1, size=7, zorder=1)
    x0 = 0.55
    fs.cylinder(ax, (0, 0.0), 0.45, 2 * x0, vertical=False, ry=0.15)
    for s_ in (1, -1):
        fs.arrow(ax, (s_ * x0, 0), (s_ * (x0 + 0.9), 0), color=fs.FIELD, lw=1.4, ms=9, zorder=6)
    ax.text(x0 + 0.5, -0.35, r'$E(x_0)$', fontsize=9, color=fs.FIELD, ha='center', va='top')
    ax.text(-d, -1.55, '$-d$', fontsize=9, ha='center', va='top'); ax.text(d, -1.55, '$d$', fontsize=9, ha='center', va='top')
    ax.text(x0, 0.55, '$x_0$', fontsize=9, ha='center'); ax.text(-x0, 0.55, '$-x_0$', fontsize=9, ha='center')
    ax.text(0, 1.6, r'밀도 $\rho$', fontsize=9, ha='center')
    ax2 = fig.add_axes([0.62, 0.18, 0.37, 0.74]); styled(ax2)
    x = np.linspace(-3, 3, 600)
    E = np.where(np.abs(x) < 1, x, np.sign(x))
    ax2.plot(x, E, color=fs.FIELD, lw=1.8)
    ax2.axhline(0, color=fs.BLACK, lw=0.7); ax2.axvspan(-1, 1, color='#f3c9c2', alpha=0.6, lw=0)
    ax2.set_xticks([-1, 0, 1]); ax2.set_xticklabels(['$-d$', '0', '$d$'])
    ax2.set_yticks([-1, 0, 1]); ax2.set_yticklabels([r'$-\rho d/\varepsilon_0$', '0', r'$\rho d/\varepsilon_0$'])
    ax2.set_xlabel('$x$'); ax2.set_ylabel('$E_x$'); ax2.set_ylim(-1.3, 1.3)
    fs.save(fig, __file__, 'fig22_21')


# ---------------------------------------------------------------- p-n 접합
def fig22():
    e, eps = 1.602e-19, 11.7 * 8.854e-12
    N, xn = 1.0e22, 0.20e-6
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.0, 3.3), sharex=True)
    for ax in (a1, a2):
        styled(ax)
    x = np.linspace(-0.4, 0.4, 801)
    rho = np.where((x > -0.2) & (x < 0), -1.0, np.where((x > 0) & (x < 0.2), 1.0, 0.0))
    a1.fill_between(x, 0, rho, where=rho < 0, color=fs.NEG, alpha=0.5, lw=0, step='mid')
    a1.fill_between(x, 0, rho, where=rho > 0, color=fs.POS, alpha=0.5, lw=0, step='mid')
    a1.plot(x, rho, color=fs.BLACK, lw=1.0)
    a1.set_yticks([-1, 0, 1]); a1.set_yticklabels([r'$-eN_A$', '0', r'$+eN_D$'])
    a1.set_ylabel(r'$\rho$'); a1.set_ylim(-1.4, 1.4)
    a1.text(-0.33, 0.6, 'p 쪽', fontsize=9, ha='center'); a1.text(0.33, -0.9, 'n 쪽', fontsize=9, ha='center')
    xm = x * 1e-6
    E = np.where((x >= -0.2) & (x <= 0), -e * N / eps * (xm + xn),
                 np.where((x > 0) & (x <= 0.2), -e * N / eps * (xn - xm), 0.0))
    a2.plot(x, E / 1e6, color=fs.FIELD, lw=1.8)
    a2.axhline(0, color=fs.BLACK, lw=0.7)
    a2.text(0.02, -3.1, r'$E_{\max}=-3.1\times10^6$ V/m', fontsize=8.5, va='center')
    a2.set_ylabel(r'$E$ ($10^6$ V/m)'); a2.set_ylim(-3.8, 0.8)
    a2.set_xlabel(r'$x$ ($\mu$m)')
    a2.set_xticks([-0.4, -0.2, 0, 0.2, 0.4]); a2.set_xticklabels(['−0.4', r'$-x_p$', '0', r'$x_n$', '0.4'])
    fig.tight_layout(h_pad=0.4)
    fs.save(fig, __file__, 'fig22_22')


# ---------------------------------------------------------------- 언쇼 정리
def fig23():
    fig, ax = fs.canvas(2.6, 2.5, xlim=(-1.6, 1.6), ylim=(-1.8, 1.6))
    ax.add_patch(Circle((0, 0), 0.75, fc=fs.SURF, alpha=0.35, ec=fs.BLACK, lw=1.0, ls='--'))
    fs.dot(ax, (0, 0), r=0.05); ax.text(0.1, 0.1, '$P$', fontsize=10)
    for t in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        u = np.array([np.cos(t), np.sin(t)])
        fs.arrow(ax, 1.35 * u, 0.85 * u, color=fs.FIELD, lw=1.2, ms=8)
    ax.text(0, -1.65, r'모두 안쪽이면 $\oint\vec E\cdot d\vec A < 0$', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig22_23')


# ---------------------------------------------------------------- 연습문제 11 공동이 있는 구
def fig24():
    fig, ax = fs.canvas(3.0, 2.6, xlim=(-1.9, 2.1), ylim=(-1.7, 1.75))
    R = 1.6
    ax.add_patch(Circle((0, 0), R, fc='#f3c9c2', ec=fs.BLACK, lw=1.2))
    cc = np.array([0.8, 0.3]); rc = 0.6
    ax.add_patch(Circle(cc, rc, fc='white', ec=fs.BLACK, lw=1.1))
    fs.dot(ax, (0, 0), r=0.04); fs.dot(ax, cc, r=0.04)
    fs.arrow(ax, (0, 0), cc, color=fs.BLACK, lw=1.4, ms=9)
    ax.text(0.35, -0.05, r'$\vec d$', fontsize=11, ha='center')
    P = cc + np.array([0.1, 0.38])
    fs.dot(ax, P, r=0.04)
    fs.arrow(ax, (0, 0), P, color=fs.GRAY, lw=0.9, ms=7)
    fs.arrow(ax, cc, P, color=fs.GRAY, lw=0.9, ms=7)
    ax.text(0.3, 0.55, r'$\vec r$', fontsize=10, color=fs.GRAY)
    ax.text(P[0] + 0.12, P[1] - 0.15, r"$\vec r^{\,\prime}$", fontsize=10, color=fs.GRAY)
    ax.text(-0.9, -0.9, r'$\rho$', fontsize=12)
    ax.text(cc[0] + 0.05, cc[1] - 0.35, '공동', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig22_24')


if __name__ == '__main__':
    names = sys.argv[1:] or [f'fig{i:02d}' for i in range(1, 25)]
    for n in names:
        globals()[n]()
