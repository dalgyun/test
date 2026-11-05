"""13장 중력 — 그림 생성 스크립트.

    python3 figures/ch13/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Ellipse, Arc, Wedge, FancyArrowPatch

EARTH = '#cfe0f0'


# ---------- 이 장 전용 도우미 ----------
def hdim(ax, x0, x1, y, text, color=fs.GRAY, fontsize=9, above=True):
    ax.annotate('', (x0, y), (x1, y), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.8,
                                                       mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (0.04 if above else -0.04), text, fontsize=fontsize, color=color,
            ha='center', va='bottom' if above else 'top')


def seg_label(ax, p, q, text, off=0.15, color=fs.BLACK, fontsize=10):
    """선분 p–q의 가운데에서 왼쪽 법선 방향으로 off만큼 떨어진 곳에 글자."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    u = (q - p) / np.linalg.norm(q - p); n = np.array([-u[1], u[0]])
    m = (p + q) / 2 + n * off
    ax.text(m[0], m[1], text, fontsize=fontsize, color=color, ha='center', va='center')


def curve_arrow(ax, pts, color=fs.BLACK, lw=1.2, ms=10, ls='-', zorder=5):
    pts = np.asarray(pts, float)
    ax.plot(pts[:-2, 0], pts[:-2, 1], color=color, lw=lw, ls=ls, zorder=zorder)
    ax.add_patch(FancyArrowPatch(pts[-4], pts[-1], arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=zorder))


# ---------- 그림 13.1 두 입자 사이의 중력 ----------
def fig01():
    fig, ax = fs.canvas(4.2, 1.5, xlim=(-0.8, 5.8), ylim=(-0.9, 1.0))
    p1, p2 = np.array([0.0, 0.0]), np.array([5.0, 0.0])
    ax.add_patch(Circle(p1, 0.28, fc='#9fb6cd', ec=fs.BLACK, lw=1.0, zorder=5))
    ax.add_patch(Circle(p2, 0.2, fc='#9fb6cd', ec=fs.BLACK, lw=1.0, zorder=5))
    ax.text(p1[0], p1[1] - 0.5, r'$m_1$', fontsize=11, ha='center')
    ax.text(p2[0], p2[1] - 0.5, r'$m_2$', fontsize=11, ha='center')
    fs.arrow(ax, p1 + [0.28, 0], p1 + [1.4, 0], color=fs.FORCE, lw=1.8)
    ax.text(1.0, 0.3, r'$\vec F_{21}$', fontsize=11, color=fs.FORCE, ha='center')
    fs.arrow(ax, p2 - [0.2, 0], p2 - [1.32, 0], color=fs.FORCE, lw=1.8)
    ax.text(4.1, 0.3, r'$\vec F_{12}$', fontsize=11, color=fs.FORCE, ha='center')
    fs.arrow(ax, p2 + [0.2, 0], p2 + [0.75, 0], color=fs.BLACK, lw=1.2, ms=9)
    ax.text(5.5, 0.3, r'$\hat r_{12}$', fontsize=11, ha='center')
    hdim(ax, 0, 5.0, -0.75, r'$r$', above=True)
    fs.save(fig, __file__, 'fig13_01')


# ---------- 그림 13.2 세 질량의 중력(예제 13.2) ----------
def fig02():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-1.0, 6.2), ylim=(-1.0, 5.0))
    ax.plot([-0.6, 6.0], [0, 0], color=fs.GRAY, lw=0.7); ax.plot([0, 0], [-0.6, 4.8], color=fs.GRAY, lw=0.7)
    ax.text(6.0, -0.35, r'$x$', fontsize=10, color=fs.GRAY); ax.text(-0.35, 4.7, r'$y$', fontsize=10, color=fs.GRAY)
    for p, m, rr in [((0, 0), '1.0 kg', 0.2), ((5, 0), '2.0 kg', 0.25), ((0, 4), '3.0 kg', 0.3)]:
        ax.add_patch(Circle(p, rr, fc='#9fb6cd', ec=fs.BLACK, lw=1.0, zorder=5))
    ax.text(-0.25, -0.45, '1.0 kg', fontsize=8, ha='right')
    ax.text(5.0, -0.6, '2.0 kg', fontsize=8, ha='center')
    ax.text(0.45, 4.05, '3.0 kg', fontsize=8, ha='left')
    k = 0.25          # 1e-10 N → 그림 단위
    F1, F2 = 5.34 * k, 12.5 * k
    fs.arrow(ax, (0, 0), (F1, 0), color=fs.FORCE, lw=1.6, zorder=6)
    ax.text(F1 + 0.35, 0.25, r'$\vec F_1$', fontsize=11, color=fs.FORCE, ha='center')
    fs.arrow(ax, (0, 0), (0, F2), color=fs.FORCE, lw=1.6, zorder=6)
    ax.text(-0.38, F2 / 2, r'$\vec F_2$', fontsize=11, color=fs.FORCE, ha='center')
    ax.plot([F1, F1], [0, F2], ls=':', color=fs.FORCE, lw=0.8); ax.plot([0, F1], [F2, F2], ls=':', color=fs.FORCE, lw=0.8)
    fs.arrow(ax, (0, 0), (F1, F2), color=fs.FORCE, lw=2.2, zorder=7)
    ax.text(F1 + 0.2, F2 + 0.15, r'$\vec F_{\mathrm{net}}$', fontsize=11, color=fs.FORCE)
    fs.angle_arc(ax, (0, 0), 0.75, 0, 66.9, r'$66.9^\circ$', fontsize=8, tr=1.25)
    hdim(ax, 0, 5.0, -0.85, r'$0.50\ \mathrm{m}$', above=False)
    ax.annotate('', (-0.7, 0), (-0.7, 4.0), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(-0.8, 2.6, r'$0.40\ \mathrm{m}$', fontsize=9, color=fs.GRAY, rotation=90, ha='right', va='center')
    fs.save(fig, __file__, 'fig13_02')


# ---------- 그림 13.3 껍질 정리의 기하 ----------
def fig03():
    fig, ax = fs.canvas(4.6, 3.0, xlim=(-2.3, 5.6), ylim=(-2.55, 2.6))
    R = 2.0; rP = 4.8
    th, dth = np.radians(55), np.radians(10)
    # 띠(고리) 단면
    for sgn in (1, -1):
        ax.add_patch(Wedge((0, 0), R + 0.06, np.degrees(sgn * th) - (0 if sgn > 0 else np.degrees(dth)),
                           np.degrees(sgn * th) + (np.degrees(dth) if sgn > 0 else 0), width=0.12,
                           fc=fs.SURF, ec='none', zorder=2))
    ax.add_patch(Circle((0, 0), R, fc='none', ec=fs.BLACK, lw=1.3, zorder=3))
    # 고리 (비스듬히 본 원)
    xm = R * np.cos(th + dth / 2); ym = R * np.sin(th + dth / 2)
    fs.ellipse3d(ax, (xm, 0), 0.22, ym, color=fs.ORANGE, lw=1.0)
    ax.plot([-R - 0.2, rP + 0.4], [0, 0], color=fs.GRAY, lw=0.7, ls='-.')
    O = np.array([0, 0]); P = np.array([rP, 0]); T = R * np.array([np.cos(th), np.sin(th)])
    fs.dot(ax, O); fs.dot(ax, P, r=0.07, color=fs.VEL)
    ax.text(-0.1, -0.3, r'$O$', fontsize=11, ha='center')
    ax.text(rP + 0.05, -0.32, r'$P$', fontsize=11, ha='center', color=fs.VEL)
    ax.plot([0, T[0]], [0, T[1]], color=fs.BLACK, lw=1.0)
    seg_label(ax, O, T, r'$R$', off=0.22)
    ax.plot([T[0], P[0]], [T[1], P[1]], color=fs.VEL, lw=1.0)
    seg_label(ax, T, P, r'$s$', off=0.2, color=fs.VEL)
    fs.angle_arc(ax, (0, 0), 0.55, 0, 55, r'$\theta$', fontsize=11, tr=0.8)
    hdim(ax, 0, rP, -2.35, r'$r$', above=True)
    ax.annotate(r'$R\,d\theta$', (R * np.cos(th + dth) + 0.05, R * np.sin(th + dth) + 0.05), (0.2, 2.45),
                fontsize=10, arrowprops=dict(arrowstyle='-', lw=0.6))
    ax.annotate('질량 $dM$인 고리\n(반지름 $R\\sin\\theta$)', (xm + 0.2, -0.9), (2.6, 1.7), fontsize=8.5, color=fs.ORANGE,
                ha='center', arrowprops=dict(arrowstyle='-', lw=0.6, color=fs.ORANGE))
    fs.save(fig, __file__, 'fig13_03')


# ---------- 그림 13.4 껍질 안쪽에서 힘이 상쇄되는 이유 ----------
def fig04():
    fig, ax = fs.canvas(3.4, 2.9, xlim=(-2.4, 2.4), ylim=(-2.2, 2.3))
    R = 2.0
    ax.add_patch(Circle((0, 0), R, fc='none', ec=fs.BLACK, lw=1.3))
    P = np.array([-0.9, -0.35])
    d = np.array([np.cos(np.radians(200)), np.sin(np.radians(200))])
    half = np.radians(9)

    def hit(u):   # P + t u 가 원과 만나는 점 (t>0)
        b = P @ u; c = P @ P - R ** 2
        return P + (-b + np.sqrt(b * b - c)) * u
    for sgn, col, lab in [(1, fs.FORCE, 1), (-1, fs.VEL, 2)]:
        a0 = np.arctan2(sgn * d[1], sgn * d[0])
        u1 = np.array([np.cos(a0 - half), np.sin(a0 - half)]); u2 = np.array([np.cos(a0 + half), np.sin(a0 + half)])
        h1, h2 = hit(u1), hit(u2)
        ax.add_patch(Polygon([P, h1, h2], closed=True, fc=fs.SURF, alpha=0.55, ec=fs.GRAY, lw=0.6))
        ang1, ang2 = np.degrees(np.arctan2(h1[1], h1[0])), np.degrees(np.arctan2(h2[1], h2[0]))
        lo, hi = sorted([ang1, ang2])
        if hi - lo > 180:
            lo, hi = hi, lo + 360
        ax.add_patch(Arc((0, 0), 2 * R, 2 * R, theta1=lo, theta2=hi, color=fs.ORANGE, lw=4))
        mid = (h1 + h2) / 2
        s = np.linalg.norm(mid - P)
        ax.text(*(mid + (mid / np.linalg.norm(mid)) * 0.3), rf'$dm_{lab}$', fontsize=10, ha='center', va='center')
        seg_label(ax, P, mid, rf'$s_{lab}$', off=0.28 * sgn, fontsize=10)
    fs.dot(ax, P, r=0.06, color=fs.VEL)
    ax.text(P[0] + 0.1, P[1] - 0.28, r'$P$', fontsize=11, color=fs.VEL)
    fs.save(fig, __file__, 'fig13_04')


# ---------- 그림 13.5 균일한 공의 중력장 ----------
def fig05():
    fig, ax = fs.plot_axes(4.0, 2.5)
    x = np.linspace(0, 4, 500)
    g = np.where(x <= 1, x, 1 / np.maximum(x, 1e-9) ** 2)
    ax.plot(x, g, color=fs.FIELD, lw=1.9)
    ax.axvline(1, color=fs.GRAY, lw=0.8, ls=':')
    ax.text(0.75, 0.25, r'$g = \dfrac{GM}{R^3}r$', fontsize=10, ha='center', color=fs.FIELD)
    ax.text(2.2, 0.45, r'$g = \dfrac{GM}{r^2}$', fontsize=10, ha='center', color=fs.FIELD)
    ax.text(0.5, 0.06, '공 안', fontsize=9, ha='center'); ax.text(2.5, 0.06, '공 밖', fontsize=9, ha='center')
    ax.set_xlim(0, 4); ax.set_ylim(0, 1.15)
    ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', r'$R$', r'$2R$', r'$3R$', r'$4R$'])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(['0', '', '', '', r'$g_0$'])
    ax.set_xlabel(r'중심에서의 거리 $r$'); ax.set_ylabel(r'중력장의 크기 $g(r)$')
    fs.save(fig, __file__, 'fig13_05')


# ---------- 그림 13.6 지구를 관통하는 터널(예제 13.3) ----------
def fig06():
    fig, ax = fs.canvas(3.6, 2.7, xlim=(-2.6, 2.6), ylim=(-2.1, 2.1))
    R = 1.9
    ax.add_patch(Circle((0, 0), R, fc=EARTH, ec=fs.BLACK, lw=1.2))
    ax.add_patch(Rectangle((-R, -0.08), 2 * R, 0.16, fc='white', ec=fs.BLACK, lw=0.8))
    fs.dot(ax, (0, 0), r=0.04)
    x = 1.1
    ax.add_patch(Circle((x, 0), 0.1, fc=fs.VEL, ec='none', zorder=6))
    fs.arrow(ax, (x, 0.25), (x - 0.9, 0.25), color=fs.FORCE, lw=1.6)
    ax.text(x - 0.45, 0.55, r'$F_x = -m\dfrac{g_0}{R}x$', color=fs.FORCE, fontsize=9.5, ha='center')
    ax.annotate('', (x, -0.35), (0, -0.35), arrowprops=dict(arrowstyle='-|>', color=fs.BLACK, lw=0.8, mutation_scale=8))
    ax.text(x / 2, -0.62, r'$x$', fontsize=11, ha='center')
    ax.text(0, -0.25, '0', fontsize=8, ha='center', va='top')
    ax.text(-R - 0.08, 0, r'$-R$', fontsize=10, ha='right', va='center')
    ax.text(R + 0.08, 0, r'$R$', fontsize=10, ha='left', va='center')
    fs.save(fig, __file__, 'fig13_06')


# ---------- 그림 13.7 중력 퍼텐셜 에너지와 속박 ----------
def fig07():
    fig, ax = fs.plot_axes(4.4, 2.8)
    r = np.linspace(0.6, 6, 400)
    ax.plot(r, -1 / r, color=fs.BLACK, lw=1.8)
    ax.axhline(0, color=fs.BLACK, lw=0.8)
    E1 = -0.3; rmax = -1 / E1
    ax.plot([1, rmax], [E1, E1], color=fs.VEL, lw=1.6)
    ax.plot([rmax, rmax], [E1, -1 / rmax], ls=':', color=fs.VEL, lw=0.9)
    ax.plot(rmax, E1, 'o', color=fs.VEL, ms=4)
    ax.text(1.15, E1 + 0.06, r'$E < 0$: 속박 상태', color=fs.VEL, fontsize=9)
    ax.annotate('되돌아오는 점', (rmax, E1), (rmax + 0.6, E1 - 0.3), fontsize=8.5, color=fs.VEL,
                arrowprops=dict(arrowstyle='->', lw=0.7, color=fs.VEL))
    E2 = 0.15
    ax.plot([1, 6], [E2, E2], color=fs.FORCE, lw=1.6)
    ax.text(3.4, E2 + 0.06, r'$E > 0$: 무한히 멀리 달아남', color=fs.FORCE, fontsize=9)
    ax.axvline(1, color=fs.GRAY, lw=0.8, ls='--')
    ax.text(1.05, -1.25, '지표', fontsize=8.5, color=fs.GRAY)
    ax.text(2.0, -0.82, r'$U(r) = -\dfrac{GMm}{r}$', fontsize=10)
    ax.set_xlim(0.5, 6); ax.set_ylim(-1.4, 0.4)
    ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_xticklabels([r'$R$', r'$2R$', r'$3R$', r'$4R$', r'$5R$', r'$6R$'])
    ax.set_yticks([-1, 0]); ax.set_yticklabels([r'$-\dfrac{GMm}{R}$', '0'])
    ax.set_xlabel(r'$r$'); ax.set_ylabel('에너지')
    fs.save(fig, __file__, 'fig13_07')


# ---------- 그림 13.8 타원의 기하 ----------
def fig08():
    fig, ax = fs.canvas(4.6, 3.2, xlim=(-3.1, 3.1), ylim=(-3.0, 2.4))
    a, e = 2.4, 0.6; b = a * np.sqrt(1 - e ** 2); c = a * e
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(a * np.cos(t), b * np.sin(t), color=fs.VEL, lw=1.6)
    ax.plot([-a, a], [0, 0], color=fs.GRAY, lw=0.6, ls='-.'); ax.plot([0, 0], [-b, b], color=fs.GRAY, lw=0.6, ls='-.')
    ax.add_patch(Circle((c, 0), 0.13, fc=fs.ORANGE, ec='none', zorder=6))
    ax.text(c + 0.05, 0.22, '태양', fontsize=8, ha='center')
    fs.dot(ax, (-c, 0), r=0.05, color=fs.GRAY)
    ax.text(-c, -0.15, '빈 초점', fontsize=8, ha='center', va='top', color=fs.GRAY)
    fs.dot(ax, (0, 0), r=0.035)
    # 행성 P
    tp = np.radians(115); P = np.array([a * np.cos(tp), b * np.sin(tp)])
    ax.add_patch(Circle(P, 0.09, fc=fs.VEL, ec='none', zorder=6))
    ax.plot([c, P[0]], [0, P[1]], color=fs.BLACK, lw=0.9)
    ax.plot([-c, P[0]], [0, P[1]], color=fs.BLACK, lw=0.9, ls='--')
    seg_label(ax, (c, 0), P, r'$r_1$', off=-0.2, fontsize=10)
    seg_label(ax, (-c, 0), P, r'$r_2$', off=0.2, fontsize=10)
    ax.text(P[0] - 0.05, P[1] + 0.25, r'$r_1 + r_2 = 2a$', fontsize=9, ha='center')
    # 치수
    hdim(ax, -a, 0, -0.75, r'$a$')
    ax.annotate('', (0.0, 0), (0.0, -b), arrowprops=dict(arrowstyle='<|-|>', color=fs.GRAY, lw=0.8, mutation_scale=8))
    ax.text(0.08, -b * 0.55, r'$b$', fontsize=9, color=fs.GRAY, ha='left')
    hdim(ax, 0, c, -0.33, r'$ea$', above=False)
    hdim(ax, c, a, -2.15, r'$r_p = a(1-e)$', above=False)
    hdim(ax, -a, c, -2.55, r'$r_a = a(1+e)$', above=False)
    for xx, yb in ((-a, -2.6), (a, -2.2), (c, -2.6)):
        ax.plot([xx, xx], [-0.05, yb], color=fs.GRAY, lw=0.4)
    ax.text(a + 0.05, -0.15, '근일점', fontsize=8, ha='left', va='top')
    ax.text(-a - 0.05, -0.15, '원일점', fontsize=8, ha='right', va='top')
    fs.save(fig, __file__, 'fig13_08')


# ---------- 그림 13.9 케플러 제2법칙 ----------
def kepler_pos(M, e, a=1.0):
    E = M.copy()
    for _ in range(50):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return np.c_[a * (np.cos(E) - e), a * np.sqrt(1 - e ** 2) * np.sin(E)]   # 초점이 원점


def fig09():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-1.75, 0.75), ylim=(-0.95, 0.95))
    e = 0.6
    M = np.linspace(0, 2 * np.pi, 600)
    orb = kepler_pos(M, e)
    ax.plot(orb[:, 0], orb[:, 1], color=fs.VEL, lw=1.4)
    dM = 0.45
    for Mc in (0.0, np.pi):
        arc = kepler_pos(np.linspace(Mc - dM / 2, Mc + dM / 2, 80), e)
        ax.add_patch(Polygon(np.r_[[[0, 0]], arc], closed=True, fc=fs.SURF, alpha=0.75, ec=fs.ORANGE, lw=0.8))
        for p in (arc[0], arc[-1]):
            ax.add_patch(Circle(p, 0.025, fc=fs.VEL, ec='none', zorder=6))
    ax.add_patch(Circle((0, 0), 0.06, fc=fs.ORANGE, ec='none', zorder=7))
    ax.text(0.0, -0.13, '태양', fontsize=8, ha='center', va='top')
    ax.text(0.47, 0.0, r'$\Delta A$', fontsize=10, ha='center', va='center')
    ax.text(-1.15, 0.0, r'$\Delta A$', fontsize=10, ha='center', va='center')
    # 진행 방향 화살표
    pr = kepler_pos(np.array([0.9, 0.95]), e)
    ax.add_patch(FancyArrowPatch(pr[0], pr[1], arrowstyle='-|>', mutation_scale=10, color=fs.VEL, lw=0))
    ax.text(0.42, 0.42, '근일점 근처:\n빠르다', fontsize=8, ha='left', color=fs.VEL)
    ax.text(-1.6, 0.62, '원일점 근처:\n느리다', fontsize=8, ha='left', color=fs.VEL)
    fs.save(fig, __file__, 'fig13_09')


# ---------- 그림 13.10 같은 근일점에서 출발한 궤도들 ----------
def fig10():
    fig, ax = fs.canvas(4.6, 3.2, xlim=(-3.1, 2.4), ylim=(-2.0, 2.0))
    cols = [fs.BLACK, fs.VEL, fs.ACC, fs.FORCE]
    for f, col in zip([1.0, 1.2, np.sqrt(2), 1.6], cols):
        e = f ** 2 - 1; p = 1 + e
        if e < 1:
            phi = np.linspace(-np.pi, np.pi, 600)
        else:
            lim = np.arccos(-1 / e) - 1e-3
            phi = np.linspace(-lim, lim, 600)
        r = p / (1 + e * np.cos(phi))
        x, y = r * np.cos(phi), r * np.sin(phi)
        m = (x > -3.4) & (np.abs(y) < 2.3)
        ax.plot(np.where(m, x, np.nan), np.where(m, y, np.nan), color=col, lw=1.5)
    ax.add_patch(Circle((0, 0), 0.08, fc=fs.ORANGE, ec='none', zorder=7))
    ax.text(0.1, -0.2, '태양', fontsize=8)
    fs.dot(ax, (1, 0), r=0.04)
    fs.arrow(ax, (1, 0), (1, 0.5), color=fs.BLACK, lw=1.2, ms=8)
    ax.text(1.08, 0.3, r'$v_0$', fontsize=9, ha='left')
    ax.text(0.0, -0.55, r'$e = 0$ 원', fontsize=8.5, color=cols[0], ha='center')
    ax.text(-1.55, -0.35, r'$e = 0.44$ 타원', fontsize=8.5, color=cols[1], ha='center')
    for f, col, lab in [(np.sqrt(2), cols[2], r'$e = 1$ 포물선'), (1.6, cols[3], r'$e = 1.56$ 쌍곡선')]:
        e = f ** 2 - 1; p = 1 + e
        phi = np.linspace(0, np.arccos(-1 / e) - 1e-3 if e > 1.01 else np.pi - 1e-3, 4000)
        r = p / (1 + e * np.cos(phi)); y = r * np.sin(phi); k = np.argmin(np.abs(y - 1.75))
        xk = r[k] * np.cos(phi[k])
        if e > 1.01:
            ax.text(xk + 0.08, -1.75, lab, fontsize=8.5, color=col, ha='left', va='center')
        else:
            ax.text(xk - 0.08, 1.75, lab, fontsize=8.5, color=col, ha='right', va='center')
    fs.save(fig, __file__, 'fig13_10')


# ---------- 그림 13.11 원궤도의 에너지 ----------
def fig11():
    fig, ax = fs.plot_axes(4.0, 2.6)
    x = np.linspace(1, 6, 300)
    ax.plot(x, 1 / (2 * x), color=fs.VEL, lw=1.7)
    ax.plot(x, -1 / x, color=fs.BLACK, lw=1.7)
    ax.plot(x, -1 / (2 * x), color=fs.FORCE, lw=1.7, ls='--')
    ax.text(2.1, 0.33, r'$K = \dfrac{GMm}{2r}$', color=fs.VEL, fontsize=9.5)
    ax.text(2.3, -0.72, r'$U = -\dfrac{GMm}{r}$', color=fs.BLACK, fontsize=9.5)
    ax.text(1.05, -0.11, r'$E = -GMm/2r$', color=fs.FORCE, fontsize=9, va='center')
    ax.axhline(0, color=fs.BLACK, lw=0.7)
    ax.set_xlim(1, 6); ax.set_ylim(-1.05, 0.65)
    ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_xticklabels([r'$R$', r'$2R$', r'$3R$', r'$4R$', r'$5R$', r'$6R$'])
    ax.set_yticks([-1, -0.5, 0, 0.5]); ax.set_yticklabels([r'$-\dfrac{GMm}{R}$', '', '0', ''])
    ax.set_xlabel(r'궤도 반지름 $r$'); ax.set_ylabel('에너지')
    fs.save(fig, __file__, 'fig13_11')


# ---------- 그림 13.12 호만 전이 궤도(예제 13.8) ----------
def fig12():
    fig, ax = fs.canvas(4.8, 3.1, xlim=(-50, 13), ylim=(-46, 46))
    RE, r1, r2 = 6.378, 6.678, 42.164        # 1000 km 단위
    a = (r1 + r2) / 2; e = (r2 - r1) / (r2 + r1)
    ax.add_patch(Circle((0, 0), RE, fc=EARTH, ec=fs.BLACK, lw=0.8, zorder=2))
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(r1 * np.cos(t), r1 * np.sin(t), color=fs.GRAY, lw=1.0, zorder=3)
    ax.plot(r2 * np.cos(t), r2 * np.sin(t), color=fs.GRAY, lw=1.0)
    phi = np.linspace(0, np.pi, 300)
    r = a * (1 - e ** 2) / (1 + e * np.cos(phi))
    ax.plot(r * np.cos(phi), r * np.sin(phi), color=fs.VEL, lw=1.8)
    phi = np.linspace(np.pi, 2 * np.pi, 300)
    r = a * (1 - e ** 2) / (1 + e * np.cos(phi))
    ax.plot(r * np.cos(phi), r * np.sin(phi), color=fs.VEL, lw=0.9, ls=':')
    fs.arrow(ax, (r1, 0), (r1, 14), color=fs.FORCE, lw=1.8, ms=10, zorder=7)
    ax.text(r1 + 1.0, 10, r'$\Delta v_1$', color=fs.FORCE, fontsize=10, ha='left')
    fs.arrow(ax, (-r2, 0), (-r2, -10), color=fs.FORCE, lw=1.8, ms=10, zorder=7)
    ax.text(-r2 - 1.5, -7, r'$\Delta v_2$', color=fs.FORCE, fontsize=10, ha='right')
    fs.dot(ax, (r1, 0), r=0.7, color=fs.BLACK); fs.dot(ax, (-r2, 0), r=0.7, color=fs.BLACK)
    ax.text(r1 + 1, -4.5, '근지점', fontsize=8, ha='left')
    ax.text(-r2 - 1, 3.5, '원지점', fontsize=8, ha='right')
    ax.text(-14, 23, '전이 궤도', fontsize=8.5, color=fs.VEL, ha='center')
    ax.text(25, 37, '정지 궤도\n' + r'$r_2 = 42\,164$ km', fontsize=8, color=fs.GRAY, ha='left')
    ax.annotate('처음 원궤도\n' + r'$r_1 = 6678$ km', (-r1 * 0.7, -r1 * 0.7), (-18, -28), fontsize=8,
                color=fs.GRAY, ha='center', arrowprops=dict(arrowstyle='-', lw=0.6, color=fs.GRAY))
    curve_arrow(ax, np.c_[30 * np.cos(np.linspace(0.6, 1.0, 30)), 30 * np.sin(np.linspace(0.6, 1.0, 30))],
                color=fs.GRAY, lw=0.8, ms=8)
    ax.set_xlim(-50, 46)
    fs.save(fig, __file__, 'fig13_12')


# ---------- 그림 13.13 등가 원리 ----------
def fig13():
    fig, ax = fs.canvas(4.4, 2.8, xlim=(-0.4, 7.4), ylim=(-1.6, 3.6))
    for cx in (0.3, 4.3):
        ax.add_patch(Rectangle((cx, 0), 2.6, 3.0, fc='#f6f6f6', ec=fs.BLACK, lw=1.3, zorder=1))
        # 사람(단순)
        px = cx + 0.7
        ax.add_patch(Circle((px, 1.9), 0.18, fc='white', ec=fs.BLACK, lw=1.0, zorder=3))
        ax.plot([px, px], [1.72, 0.9], color=fs.BLACK, lw=1.2)
        ax.plot([px, px - 0.25], [0.9, 0.0], color=fs.BLACK, lw=1.2); ax.plot([px, px + 0.25], [0.9, 0.0], color=fs.BLACK, lw=1.2)
        ax.plot([px, px + 0.6], [1.5, 1.6], color=fs.BLACK, lw=1.2)
        ax.add_patch(Circle((cx + 1.8, 1.5), 0.12, fc=fs.VEL, ec='none', zorder=4))
        ax.add_patch(Circle((cx + 1.8, 0.8), 0.12, fc=fs.VEL, ec='none', alpha=0.35, zorder=4))
        fs.arrow(ax, (cx + 2.2, 1.6), (cx + 2.2, 0.8), color=fs.ACC, lw=1.4, ms=9)
        ax.text(cx + 2.33, 1.2, r'$g$', color=fs.ACC, fontsize=10, ha='left')
    # (가) 지구 위
    fs.ground(ax, -0.1, 3.3, y=0.0)
    fs.arrow(ax, (-0.15, 2.8), (-0.15, 1.8), color=fs.FIELD, lw=1.4, ms=9)
    ax.text(-0.05, 3.0, r'$\vec g$', color=fs.FIELD, fontsize=10, ha='center')
    ax.text(1.6, -1.1, '(가) 중력장 속에 정지', fontsize=9, ha='center')
    # (나) 로켓
    cx = 4.3
    ax.add_patch(Polygon([(cx + 0.6, 0), (cx + 2.0, 0), (cx + 1.6, -0.55), (cx + 1.0, -0.55)], closed=True,
                         fc='#dddddd', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Polygon([(cx + 1.0, -0.55), (cx + 1.6, -0.55), (cx + 1.3, -0.95)], closed=True, fc=fs.ORANGE, ec='none'))
    ax.add_patch(Polygon([(cx, 3.0), (cx + 2.6, 3.0), (cx + 1.3, 3.55)], closed=True, fc='#dddddd', ec=fs.BLACK, lw=1.0))
    fs.arrow(ax, (cx + 2.95, 1.0), (cx + 2.95, 2.0), color=fs.ACC, lw=1.6, ms=9)
    ax.text(cx + 3.05, 1.5, r'$a = g$', color=fs.ACC, fontsize=9.5, ha='left')
    ax.text(5.6, -1.1, '(나) 중력 없는 곳에서 가속', fontsize=9, ha='center')
    ax.set_xlim(-0.5, 8.0)
    fs.save(fig, __file__, 'fig13_13')


# ---------- 그림 13.14 중심을 지나지 않는 터널(연습문제 9) ----------
def fig14():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-2.3, 2.3), ylim=(-2.2, 2.2))
    R = 2.0; b = 0.9
    ax.add_patch(Circle((0, 0), R, fc=EARTH, ec=fs.BLACK, lw=1.2))
    xc = np.sqrt(R ** 2 - b ** 2)
    ax.add_patch(Rectangle((-xc, -b - 0.07), 2 * xc, 0.14, fc='white', ec=fs.BLACK, lw=0.8))
    O = np.array([0, 0]); M = np.array([0, -b]); x = 1.0; Q = np.array([x, -b])
    fs.dot(ax, O, r=0.04); ax.text(-0.1, 0.15, r'$O$', fontsize=10)
    ax.plot([0, 0], [0, -b], ls='--', color=fs.BLACK, lw=0.8)
    ax.text(-0.12, -b / 2, r'$b$', fontsize=10, ha='right', va='center')
    ax.plot([0, Q[0]], [0, Q[1]], color=fs.BLACK, lw=0.9)
    seg_label(ax, O, Q, r'$r$', off=-0.2)
    ax.add_patch(Circle(Q, 0.09, fc=fs.VEL, ec='none', zorder=6))
    u = -Q / np.linalg.norm(Q)
    fs.arrow(ax, Q, Q + 0.75 * u, color=fs.FORCE, lw=1.6, zorder=7)
    ax.text(*(Q + 0.5 * u + np.array([0.22, 0.2])), r'$\vec F$', color=fs.FORCE, fontsize=10, ha='center')
    fs.arrow(ax, Q + np.array([0, -0.22]), Q + np.array([-0.75 * abs(u[0]), -0.22]), color=fs.FORCE, lw=1.2, ls='--', ms=8)
    ax.text(Q[0] - 0.3, -b - 0.5, r'$F_x$', color=fs.FORCE, fontsize=10, ha='center')
    ax.annotate('', (x, -b - 0.75), (0, -b - 0.75), arrowprops=dict(arrowstyle='-|>', lw=0.8, mutation_scale=8))
    ax.text(x / 2, -b - 0.95, r'$x$', fontsize=10, ha='center')
    fs.save(fig, __file__, 'fig13_14')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
        f()
