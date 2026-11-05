"""11장 토크, 각운동량, 굴림 운동 — 그림 생성 스크립트.

    python3 figures/ch11/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Polygon, Rectangle, Ellipse

ANG = fs.ORANGE      # 각운동량
TORQ = fs.FIELD      # 토크 벡터(힘과 구별)


# ---------- 이 장 전용 도우미 ----------
def curve_arrow(ax, pts, color=fs.BLACK, lw=1.2, ms=10, zorder=5):
    """점열을 따라가는 곡선 화살표(끝에 화살촉)."""
    pts = np.asarray(pts, float)
    ax.plot(pts[:-2, 0], pts[:-2, 1], color=color, lw=lw, zorder=zorder)
    ax.add_patch(FancyArrowPatch(pts[-4], pts[-1], arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=zorder))


def curl(ax, c, r, th1, th2, color=fs.BLACK, lw=1.2, ry=None, ms=10):
    """중심 c, 반지름 r인 원(또는 ry를 주면 타원) 호를 th1→th2(도) 방향으로 도는 화살표."""
    th = np.radians(np.linspace(th1, th2, 60))
    ry = r if ry is None else ry
    curve_arrow(ax, np.c_[c[0] + r * np.cos(th), c[1] + ry * np.sin(th)], color=color, lw=lw, ms=ms)


def right_angle(ax, p, u, v, s=0.15, color=fs.BLACK, lw=0.8):
    """점 p에서 단위벡터 u, v 방향 사이의 직각 표시."""
    p, u, v = map(lambda a: np.asarray(a, float), (p, u, v))
    q = [p + s * u, p + s * u + s * v, p + s * v]
    ax.plot([q[0][0], q[1][0], q[2][0]], [q[0][1], q[1][1], q[2][1]], color=color, lw=lw)


def unit(a):
    a = np.asarray(a, float)
    return a / np.linalg.norm(a)


def proj(x, y, z, k=0.45, ang=35):
    """사투영: x 오른쪽, z 위, y는 오른쪽 위 비스듬히(지면 안쪽)."""
    a = np.radians(ang)
    return np.array([x + k * y * np.cos(a), z + k * y * np.sin(a)])


# ---------- 그림 11.1 토크의 기하 ----------
def fig01():
    fig, ax = fs.canvas(4.6, 3.1, xlim=(-0.8, 5.0), ylim=(-1.0, 3.4))
    O = np.array([0.0, 0.0])
    al, phi = np.radians(18), np.radians(60)
    ur = np.array([np.cos(al), np.sin(al)])
    P = O + 3.0 * ur
    uF = np.array([np.cos(al + phi), np.sin(al + phi)])
    Fl = 1.7
    # 작용선
    a, b = P - 2.2 * uF, P + 1.9 * uF
    ax.plot([a[0], b[0]], [a[1], b[1]], ls='--', color=fs.GRAY, lw=0.9)
    ax.text(*(P + 1.95 * uF + np.array([0.05, 0.12])), '작용선', fontsize=9, color=fs.GRAY, ha='center')
    # r의 연장선
    e = P + 1.1 * ur
    ax.plot([P[0], e[0]], [P[1], e[1]], ls=':', color=fs.BLACK, lw=0.9)
    # 지레팔
    foot = P - (P - O) @ uF * uF
    ax.plot([O[0], foot[0]], [O[1], foot[1]], color=fs.ORANGE, lw=1.6)
    right_angle(ax, foot, unit(O - foot), unit(P - foot), s=0.17)
    mid = (O + foot) / 2
    ax.text(mid[0] + 0.1, mid[1] - 0.4, r'$r_\perp = r\sin\phi$', color=fs.ORANGE, fontsize=11, ha='center')
    # 벡터
    fs.arrow(ax, O, P, color=fs.BLACK, lw=1.8)
    ax.text(*(O + 1.7 * ur + np.array([0.12, -0.3])), r'$\vec r$', fontsize=13)
    fs.arrow(ax, P, P + Fl * uF, color=fs.FORCE, lw=2.0)
    ax.text(*(P + Fl * uF + np.array([0.3, -0.25])), r'$\vec F$', fontsize=13, color=fs.FORCE)
    # 성분 F_perp
    up = np.array([-ur[1], ur[0]])
    Fperp = Fl * np.sin(phi) * up
    Fpar = Fl * np.cos(phi) * ur
    fs.arrow(ax, P, P + Fperp, color=fs.FORCE, lw=1.1, ls='--', ms=9)
    ax.text(*(P + Fperp + np.array([-0.55, -0.05])), r'$F_\perp$', fontsize=11, color=fs.FORCE)
    ax.plot([P[0] + Fperp[0], P[0] + Fl * uF[0]], [P[1] + Fperp[1], P[1] + Fl * uF[1]], ls=':', color=fs.FORCE, lw=0.8)
    ax.plot([P[0] + Fpar[0], P[0] + Fl * uF[0]], [P[1] + Fpar[1], P[1] + Fl * uF[1]], ls=':', color=fs.FORCE, lw=0.8)
    # 각 phi
    fs.angle_arc(ax, P, 0.45, np.degrees(al), np.degrees(al + phi), r'$\phi$', fontsize=11, tr=0.65)
    # O와 회전 방향
    fs.dot(ax, O, r=0.06)
    ax.text(0.05, -0.38, r'$O$', fontsize=12, ha='center')
    curl(ax, O, 0.4, 100, 250, color=TORQ, lw=1.1)
    ax.text(-0.62, 0.0, r'$\tau$', color=TORQ, fontsize=12, ha='center')
    fs.dot(ax, P, r=0.05)
    fs.save(fig, __file__, 'fig11_01')


# ---------- 그림 11.2 오른손 규칙 ----------
def fig02():
    fig, ax = fs.canvas(3.9, 2.9, xlim=(-0.9, 4.3), ylim=(-0.9, 2.6))
    O = proj(0, 0, 0)
    # xy 평면
    sq = [proj(-0.6, -0.9, 0), proj(3.2, -0.9, 0), proj(3.2, 2.6, 0), proj(-0.6, 2.6, 0)]
    ax.add_patch(Polygon(sq, closed=True, fc='#eef2f7', ec=fs.GRAY, lw=0.6, zorder=0))
    r = proj(2.4, 0, 0); F = proj(0.7, 2.0, 0)
    rp = r - O; Fp = F - O
    # 평행사변형(|τ|=넓이)
    ax.add_patch(Polygon([O, r, r + Fp, F], closed=True, fc=fs.SURF, alpha=0.45, ec='none', zorder=1))
    ax.plot([r[0], r[0] + Fp[0]], [r[1], r[1] + Fp[1]], ls=':', color=fs.GRAY, lw=0.8)
    ax.plot([F[0], F[0] + rp[0]], [F[1], F[1] + rp[1]], ls=':', color=fs.GRAY, lw=0.8)
    fs.arrow(ax, O, r, color=fs.BLACK, lw=1.8)
    ax.text(r[0] - 0.1, r[1] - 0.25, r'$\vec r$', fontsize=13)
    fs.arrow(ax, O, F, color=fs.FORCE, lw=1.8)
    ax.text(F[0] - 0.3, F[1] + 0.05, r'$\vec F$', fontsize=13, color=fs.FORCE)
    T = proj(0, 0, 2.2)
    fs.arrow(ax, O, T, color=TORQ, lw=2.0)
    ax.text(T[0] + 0.25, T[1] - 0.2, r'$\vec\tau = \vec r\times\vec F$', fontsize=12, color=TORQ, ha='left')
    # r에서 F 쪽으로 감기
    th = np.linspace(0.15, 1.25, 50)
    pts = np.array([proj(0.75 * np.cos(t) * 1.0, 0.75 * np.sin(t) * 1.6, 0) for t in th])
    curve_arrow(ax, pts, color=fs.BLACK, lw=1.0, ms=9)
    # 감는 방향 원(축 둘레)
    c = proj(0, 0, 1.5)
    th = np.radians(np.linspace(200, 520, 80))
    pts = np.c_[c[0] + 0.32 * np.cos(th), c[1] + 0.11 * np.sin(th)]
    curve_arrow(ax, pts, color=TORQ, lw=1.0, ms=8)
    fs.dot(ax, O, r=0.05)
    ax.text(O[0] - 0.22, O[1] - 0.18, r'$O$', fontsize=12)
    ax.text(1.6, -0.75, r'$\vec r$와 $\vec F$가 놓인 평면', fontsize=9, color=fs.GRAY, ha='center')
    fs.save(fig, __file__, 'fig11_02')


# ---------- 그림 11.3 무거운 도르래 애트우드 기계 ----------
def fig03():
    fig, ax = fs.canvas(5.4, 3.2, xlim=(-1.6, 8.2), ylim=(-0.4, 5.4))
    # (가) 장치
    C = np.array([0.0, 4.1]); R = 0.55
    fs.ceiling(ax, -0.8, 0.8, 5.1)
    ax.plot([0, 0], [5.1, C[1]], color=fs.BLACK, lw=1.4)
    fs.pulley(ax, C, r=R)
    ax.text(C[0] + R + 0.2, C[1] + 0.35, r'$M,\ R$', fontsize=10, ha='left', va='center')
    y1, y2 = 1.9, 1.0
    ax.plot([-R, -R], [C[1], y1 + 0.35], color=fs.BLACK, lw=1.1)
    ax.plot([R, R], [C[1], y2 + 0.35], color=fs.BLACK, lw=1.1)
    fs.block(ax, (-R, y1), w=0.6, h=0.7, text=r'$m_1$')
    fs.block(ax, (R, y2), w=0.6, h=0.7, text=r'$m_2$')
    fs.arrow(ax, (-R - 0.6, y1 - 0.3), (-R - 0.6, y1 + 0.4), color=fs.ACC, lw=1.5)
    ax.text(-R - 0.85, y1 + 0.05, r'$a$', color=fs.ACC, fontsize=12, ha='center')
    fs.arrow(ax, (R + 0.6, y2 + 0.4), (R + 0.6, y2 - 0.3), color=fs.ACC, lw=1.5)
    ax.text(R + 0.85, y2 + 0.05, r'$a$', color=fs.ACC, fontsize=12, ha='center')
    curl(ax, C, R + 0.32, 150, 30, color=fs.ACC, lw=1.2)
    ax.text(C[0] - 0.95, C[1] + 0.55, r'$\alpha$', color=fs.ACC, fontsize=12)
    ax.text(0, -0.3, '(가) 장치', fontsize=10, ha='center')
    # (나) 자유물체도
    x1, xp, x2 = 3.2, 5.2, 7.2
    # m1
    fs.block(ax, (x1, 2.0), w=0.6, h=0.7, text=r'$m_1$')
    fs.arrow(ax, (x1, 2.35), (x1, 3.35), color=fs.FORCE, label=r'$\vec T_1$', loff=(0.3, -0.1))
    fs.arrow(ax, (x1, 1.65), (x1, 0.85), color=fs.FORCE, label=r'$m_1\vec g$', loff=(0.45, 0.15))
    # 도르래
    Cp = np.array([xp, 3.4])
    fs.pulley(ax, Cp, r=R)
    fs.arrow(ax, (xp - R, Cp[1]), (xp - R, Cp[1] - 1.05), color=fs.FORCE, label=r'$\vec T_1$', loff=(-0.35, 0.2))
    fs.arrow(ax, (xp + R, Cp[1]), (xp + R, Cp[1] - 1.15), color=fs.FORCE, label=r'$\vec T_2$', loff=(0.38, 0.2))
    fs.arrow(ax, Cp, Cp + np.array([0, 1.7]), color=fs.FORCE, lw=1.3, label='축의 힘', loff=(0.72, -0.3), zorder=6)
    fs.arrow(ax, Cp, Cp + np.array([0, -0.7]), color=fs.FORCE, lw=1.3, label=r'$M\vec g$', loff=(0.0, -0.28), zorder=6)
    # m2
    fs.block(ax, (x2, 1.6), w=0.6, h=0.7, text=r'$m_2$')
    fs.arrow(ax, (x2, 1.95), (x2, 3.05), color=fs.FORCE, label=r'$\vec T_2$', loff=(0.32, -0.1))
    fs.arrow(ax, (x2, 1.25), (x2, 0.1), color=fs.FORCE, label=r'$m_2\vec g$', loff=(0.45, 0.2))
    ax.text(xp, -0.3, '(나) 자유물체도', fontsize=10, ha='center')
    fs.save(fig, __file__, 'fig11_03')


# ---------- 그림 11.4 쓰러지는 막대 ----------
def fig04():
    fig, ax = fs.canvas(4.2, 2.3, xlim=(-0.8, 5.0), ylim=(-1.9, 1.3))
    L = 4.0
    ax.add_patch(Rectangle((0, -0.08), L, 0.16, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    # 축
    ax.add_patch(Polygon([(-0.25, -0.75), (0.25, -0.75), (0, 0)], closed=True, fc='#dddddd', ec=fs.BLACK, lw=1.0, zorder=2))
    fs.ground(ax, -0.5, 0.5, y=-0.75, depth=0.12)
    ax.add_patch(Circle((0, 0), 0.07, fc='white', ec=fs.BLACK, lw=1.0, zorder=6))
    fs.arrow(ax, (0, 0.1), (0, 0.85), color=fs.FORCE, label=r'$\vec N$', loff=(-0.3, -0.1))
    fs.arrow(ax, (L / 2, 0), (L / 2, -1.1), color=fs.FORCE, label=r'$M\vec g$', loff=(-0.4, 0.15))
    fs.dot(ax, (L / 2, 0), r=0.06, color=fs.BLACK, zorder=7)
    fs.arrow(ax, (L / 2 + 0.25, -0.15), (L / 2 + 0.25, -0.15 - 0.6), color=fs.ACC, lw=1.4)
    ax.text(L / 2 + 0.75, -0.55, r'$a_{\mathrm{cm}} = \frac{3}{4}g$', color=fs.ACC, fontsize=10)
    fs.arrow(ax, (L, -0.1), (L, -0.1 - 1.2), color=fs.ACC, lw=1.6)
    ax.text(L + 0.1, -1.55, r'끝: $\frac{3}{2}g$', color=fs.ACC, fontsize=10, ha='center')
    curl(ax, (0, 0), 0.95, -12, -70, color=fs.ACC, lw=1.1)
    ax.text(0.95, -0.85, r'$\alpha$', color=fs.ACC, fontsize=12)
    fs.dim(ax, (0, 0.1), (L / 2, 0.1), r'$L/2$', off=0.35)
    fs.dim(ax, (L / 2, 0.1), (L, 0.1), r'$L/2$', off=0.35)
    ax.text(-0.6, -0.25, '축', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig11_04')


# ---------- 그림 11.5 굴림 운동의 속도 분포 ----------
def fig05():
    fig, ax = fs.canvas(5.6, 1.9, xlim=(-1.3, 10.6), ylim=(-0.95, 2.6))
    R, v = 1.0, 0.8
    pts = {'top': (0, R), 'front': (R, 0), 'bot': (0, -R), 'back': (-R, 0)}
    centers = [0.0, 4.4, 8.8]
    titles = ['병진', '회전(질량중심 기준)', '굴림 = 병진 + 회전']
    for k, cx in enumerate(centers):
        c = np.array([cx, 1.0])
        ax.add_patch(Circle(c, R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2))
        fs.ground(ax, cx - 1.3, cx + 1.3, y=0.0, depth=0.12)
        fs.dot(ax, c, r=0.05)
        ax.text(cx, -0.65, titles[k], fontsize=9, ha='center')
        for key, d in pts.items():
            p = c + np.array(d)
            if k == 0:
                vel = np.array([v, 0])
            elif k == 1:
                vel = v * np.array([d[1], -d[0]]) / R     # 시계 방향 회전
            else:
                vel = np.array([v, 0]) + v * np.array([d[1], -d[0]]) / R
            if np.linalg.norm(vel) > 1e-6:
                fs.vec(ax, p, vel, color=fs.VEL, lw=1.4, ms=9)
            fs.dot(ax, p, r=0.04)
        if k == 0:
            fs.vec(ax, c, (v, 0), color=fs.VEL, lw=1.4, ms=9)
            ax.text(cx + 0.55, 1.18, r'$v_{\mathrm{cm}}$', color=fs.VEL, fontsize=9, ha='center')
        if k == 1:
            curl(ax, c, 0.42, 130, -40, color=fs.BLACK, lw=0.9, ms=8)
            ax.text(cx + 0.05, 2.3, r'$R\omega = v_{\mathrm{cm}}$', color=fs.VEL, fontsize=9, ha='center')
        if k == 2:
            fs.vec(ax, c, (v, 0), color=fs.VEL, lw=1.4, ms=9)
            ax.text(cx + 1.05, 2.25, r'$2v_{\mathrm{cm}}$', color=fs.VEL, fontsize=9)
            ax.text(cx + 0.55, 1.18, r'$v_{\mathrm{cm}}$', color=fs.VEL, fontsize=9, ha='center')
            P = c + np.array([0, -R])
            for d in [(0, R), (R, 0), (-R, 0), (0, 0)]:
                q = c + np.array(d)
                ax.plot([P[0], q[0]], [P[1], q[1]], ls=':', color=fs.GRAY, lw=0.9, zorder=3)
            ax.text(cx + 0.18, 0.16, r'$P$', fontsize=10)
            ax.text(cx - 0.3, 0.2, '0', fontsize=8, color=fs.VEL)
    ax.text(2.2, 1.0, '+', fontsize=16, ha='center', va='center')
    ax.text(6.6, 1.0, '=', fontsize=16, ha='center', va='center')
    fs.save(fig, __file__, 'fig11_05')


# ---------- 그림 11.6 빗면을 굴러 내려가는 물체 ----------
def fig06():
    fig, ax = fs.canvas(4.2, 2.8, xlim=(-0.3, 6.0), ylim=(-0.4, 3.9))
    th = 30.0
    t = np.radians(th)
    fs.incline(ax, (0, 0), length=6.4, angle=th)
    ud = -np.array([np.cos(t), np.sin(t)])     # 빗면 아래 방향
    n = np.array([-np.sin(t), np.cos(t)])
    R = 0.65
    Pc = np.array([np.cos(t), np.sin(t)]) * 3.6
    C = Pc + R * n
    ax.add_patch(Circle(C, R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=3))
    fs.dot(ax, C, r=0.05)
    fs.arrow(ax, C, C + np.array([0, -1.45]), color=fs.FORCE, label=r'$M\vec g$', loff=(0.35, 0.1), zorder=7)
    fs.arrow(ax, Pc, Pc + 1.75 * n, color=fs.FORCE, label=r'$\vec N$', loff=(-0.2, 0.15), zorder=7, lpos=1.0)
    fs.arrow(ax, Pc, Pc - 0.85 * ud, color=fs.FORCE, label=r'$\vec f$', loff=(0.05, 0.25), zorder=7)
    fs.dot(ax, Pc, r=0.04)
    a0 = C + 0.15 * n + (R + 0.15) * ud
    fs.arrow(ax, a0, a0 + 0.95 * ud, color=fs.ACC, lw=1.5)
    ax.text(*(a0 + 0.55 * ud + 0.3 * n), r'$a_{\mathrm{cm}}$', color=fs.ACC, fontsize=11, ha='center')
    curl(ax, C, R + 0.2, 15, 100, color=fs.ACC, lw=1.1)
    ax.text(C[0] + 0.85, C[1] + 0.85, r'$\alpha$', color=fs.ACC, fontsize=11)
    fs.save(fig, __file__, 'fig11_06')


# ---------- 그림 11.7 볼링공: 미끄럼에서 굴림으로 ----------
def fig07():
    fig, ax = fs.plot_axes(4.2, 2.7)
    g, mu, v0 = 9.8, 0.20, 8.0
    t1 = 2 * v0 / (7 * mu * g)
    v1 = 5 / 7 * v0
    t = np.linspace(0, 2.0, 400)
    v = np.where(t < t1, v0 - mu * g * t, v1)
    Rw = np.where(t < t1, 2.5 * mu * g * t, v1)
    ax.plot(t, v, color=fs.VEL, lw=1.8, label=r'질량중심 속력 $v$')
    ax.plot(t, Rw, color=fs.ORANGE, lw=1.8, ls='--', label=r'$R\omega$')
    ax.axvline(t1, color=fs.GRAY, lw=0.8, ls=':')
    ax.fill_between(t, v, Rw, where=t < t1, color=fs.SURF, alpha=0.35, lw=0)
    ax.text(0.45, 4.0, '미끄러짐\n($v > R\\omega$)', fontsize=9, ha='center')
    ax.text(1.6, 6.15, '굴림 ($v = R\\omega$)', fontsize=9, ha='center')
    ax.annotate(rf'$t_1 = {t1:.2f}$ s', (t1, 0.4), (t1 + 0.12, 1.0), fontsize=9)
    ax.annotate(rf'$\frac{{5}}{{7}}v_0 = {v1:.2f}$ m/s', (t1, v1), (1.25, 4.3), fontsize=9,
                arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.set_xlim(0, 2.0); ax.set_ylim(0, 8.6)
    ax.set_xlabel(r'시간 $t$ (s)'); ax.set_ylabel('속력 (m/s)')
    ax.legend(loc='upper right', fontsize=8.5, frameon=False)
    fs.save(fig, __file__, 'fig11_07')


# ---------- 그림 11.8 직선 운동하는 입자의 각운동량 ----------
def fig08():
    from matplotlib.patches import Arc
    fig, ax = fs.canvas(4.4, 2.4, xlim=(-1.3, 6.2), ylim=(-0.75, 2.9))
    O = np.array([0.0, 0.0]); d = 1.8
    ax.plot([-1.0, 6.0], [d, d], ls='--', color=fs.GRAY, lw=0.9)
    ax.text(-1.0, d + 0.2, '운동 경로', fontsize=9, color=fs.GRAY, ha='left')
    for x, show in [(1.2, True), (3.6, False)]:
        P = np.array([x, d])
        fs.arrow(ax, O, P, color=fs.BLACK, lw=1.4 if show else 1.0)
        fs.vec(ax, P, (1.1, 0), color=fs.VEL, lw=1.8)
        ax.add_patch(Circle(P, 0.1, fc=fs.VEL, ec='none', zorder=7))
        ax.text(P[0] + 1.15, P[1] + 0.25, r'$\vec p$', color=fs.VEL, fontsize=12)
        if show:
            ax.text(0.35, 1.05, r'$\vec r$', fontsize=12)
            a = np.degrees(np.arctan2(d, x))
            ext = P + 0.75 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
            ax.plot([P[0], ext[0]], [P[1], ext[1]], ls=':', color=fs.BLACK, lw=0.9)
            ax.add_patch(Arc(P, 0.9, 0.9, theta1=0, theta2=a, lw=0.9))
            ax.text(P[0] + 0.55, P[1] + 0.3, r'$\phi$', fontsize=11)
        else:
            ax.text(2.25, 1.25, r"$\vec r\,'$", fontsize=12)
    # r_perp
    fs.arrow(ax, (O[0] - 0.55, 0), (O[0] - 0.55, d), color=fs.ORANGE, lw=1.0, style='<|-|>', ms=8)
    ax.plot([O[0] - 0.7, O[0]], [0, 0], color=fs.ORANGE, lw=0.6)
    ax.text(-0.95, d / 2, r'$r_\perp$', color=fs.ORANGE, fontsize=12, ha='center')
    fs.dot(ax, O, r=0.06)
    ax.text(0.0, -0.32, r'$O$', fontsize=12, ha='center')
    fs.cross_in(ax, (2.3, -0.45), r=0.1, color=ANG)
    ax.text(2.5, -0.45, r'$\vec\ell = \vec r\times\vec p$ (지면 안쪽, 일정)', fontsize=9, color=ANG, ha='left', va='center')
    fs.save(fig, __file__, 'fig11_08')


# ---------- 그림 11.9 막대에 박히는 총알 ----------
def fig09():
    fig, ax = fs.canvas(5.0, 2.8, xlim=(-2.0, 8.0), ylim=(-4.0, 0.7))
    L = 3.0
    for cx in (0.0, 4.6):
        fs.ceiling(ax, cx - 0.5, cx + 0.5, 0.4)
        ax.plot([cx, cx], [0.4, 0.0], color=fs.BLACK, lw=1.2)
    # (가) 충돌 직전
    ax.add_patch(Rectangle((-0.08, -L), 0.16, L, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    ax.add_patch(Circle((0, 0), 0.07, fc='white', ec=fs.BLACK, zorder=6))
    ax.add_patch(Circle((-1.4, -L + 0.08), 0.09, fc=fs.BLACK, zorder=6))
    fs.vec(ax, (-1.3, -L + 0.08), (0.75, 0), color=fs.VEL, lw=1.6)
    ax.text(-1.4, -L + 0.4, r'$m,\ v$', fontsize=11, color=fs.VEL, ha='center')
    fs.dim(ax, (0.08, 0), (0.08, -L), r'$L$', off=-0.35)
    ax.text(0.3, -1.5, r'$M$', fontsize=11)
    ax.text(-0.3, -3.8, '(가) 충돌 직전', fontsize=10, ha='center')
    # (나) 최대로 올라간 순간
    cx = 4.6
    ax.plot([cx, cx], [0, -L], ls='--', color=fs.GRAY, lw=0.9)
    th = np.radians(101)
    tip = np.array([cx + L * np.sin(th), -L * np.cos(th)])
    u = (tip - np.array([cx, 0])) / L; nn = np.array([-u[1], u[0]]) * 0.08
    ax.add_patch(Polygon([np.array([cx, 0]) + nn, tip + nn, tip - nn, np.array([cx, 0]) - nn], closed=True,
                         fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    ax.add_patch(Circle(tip, 0.09, fc=fs.BLACK, zorder=6))
    ax.add_patch(Circle((cx, 0), 0.07, fc='white', ec=fs.BLACK, zorder=6))
    fs.angle_arc(ax, (cx, 0), 0.8, -90, -90 + 101, r'$\theta$', fontsize=12, tr=1.1)
    ax.plot([cx, cx + 2.6], [0, 0], ls=':', color=fs.GRAY, lw=0.8)
    ax.text(cx + 1.2, -3.8, '(나) 가장 높이 올라간 순간', fontsize=10, ha='center')
    fs.save(fig, __file__, 'fig11_09')


# ---------- 그림 11.10 자이로스코프의 세차운동 ----------
def fig10():
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.9), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]
    ax.set_xlim(-1.3, 4.2); ax.set_ylim(-2.2, 2.6); ax.set_aspect('equal'); ax.axis('off')
    O = proj(0, 0, 0)
    # 받침대
    ax.add_patch(Rectangle((-0.12, -1.7), 0.24, 1.7, fc='#dddddd', ec=fs.BLACK, lw=1.0, zorder=1))
    fs.ground(ax, -0.8, 0.8, y=-1.7, depth=0.12)
    r = 2.0
    C = proj(r, 0, 0)
    ax.plot([O[0], C[0] + 0.5], [O[1], C[1]], color=fs.BLACK, lw=2.2, zorder=3)
    # 바퀴(yz 평면의 원 → 사투영)
    th = np.linspace(0, 2 * np.pi, 200)
    Rw = 0.9
    wheel = np.array([proj(r, Rw * np.cos(t), Rw * np.sin(t)) for t in th])
    ax.fill(wheel[:, 0], wheel[:, 1], fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2)
    fs.dot(ax, C, r=0.06)
    fs.dot(ax, O, r=0.06)
    ax.text(O[0] - 0.35, O[1] + 0.15, r'$O$', fontsize=12)
    # 스핀
    sp = np.array([proj(r, 1.15 * np.cos(t), 1.15 * np.sin(t)) for t in np.linspace(1.9, 3.6, 40)])
    curve_arrow(ax, sp, color=fs.BLACK, lw=0.9, ms=8)
    ax.text(*(proj(r, -1.35, 1.0)), r'$\omega$', fontsize=11)
    # L
    fs.arrow(ax, C, proj(r + 1.6, 0, 0), color=ANG, lw=2.0)
    ax.text(*(proj(r + 1.65, 0, 0) + np.array([-0.15, 0.22])), r'$\vec L$', color=ANG, fontsize=12)
    # 중력
    fs.arrow(ax, C, C + np.array([0, -1.5]), color=fs.FORCE, lw=1.6, zorder=6)
    ax.text(C[0] + 0.2, C[1] - 1.45, r'$M\vec g$', color=fs.FORCE, fontsize=11)
    fs.arrow(ax, O, O + np.array([0, 1.2]), color=fs.FORCE, lw=1.4, zorder=6)
    ax.text(O[0] + 0.12, O[1] + 1.15, r'$\vec N$', color=fs.FORCE, fontsize=11)
    # r_cm
    fs.dim(ax, O, C, r'$r$', off=-0.28)
    # 토크 (+y, 지면 안쪽 비스듬히)
    fs.arrow(ax, O, proj(0, 2.6, 0), color=TORQ, lw=1.8)
    ax.text(*(proj(0, 2.6, 0) + np.array([0.12, 0.1])), r'$\vec\tau$', color=TORQ, fontsize=12)
    # 세차
    pre = np.array([proj(0.55 * np.cos(t), 0.55 * np.sin(t), 2.0) for t in np.linspace(-1.9, 1.3, 60)])
    ax.plot([O[0], O[0]], [O[1] + 1.25, O[1] + 2.35], color=fs.BLACK, lw=0.8, ls=':')
    curve_arrow(ax, pre, color=fs.ACC, lw=1.1, ms=8)
    ax.text(*(proj(0.0, 0, 2.15) + np.array([-0.45, 0.25])), r'$\Omega$', color=fs.ACC, fontsize=12)
    ax.text(1.6, -2.15, '(가) 옆에서 본 모습', fontsize=9, ha='center')
    # (나) 위에서 본 벡터 그림
    ax = axs[1]
    ax.set_xlim(-0.5, 3.2); ax.set_ylim(-1.0, 2.6); ax.set_aspect('equal'); ax.axis('off')
    O2 = np.array([0, 0]); Lm = 2.4; dphi = np.radians(22)
    fs.arrow(ax, O2, (Lm, 0), color=ANG, lw=2.0)
    ax.text(Lm * 0.6, -0.3, r'$\vec L(t)$', color=ANG, fontsize=11, ha='center')
    L2 = Lm * np.array([np.cos(dphi), np.sin(dphi)])
    fs.arrow(ax, O2, L2, color=ANG, lw=1.4, ls='--')
    ax.text(L2[0] * 0.5 - 0.35, L2[1] * 0.5 + 0.2, r'$\vec L(t + dt)$', color=ANG, fontsize=10, ha='center')
    fs.arrow(ax, (Lm, 0), L2, color=TORQ, lw=1.5, ms=9)
    ax.text(Lm + 0.25, 0.45, r'$d\vec L = \vec\tau\,dt$', color=TORQ, fontsize=10, ha='left')
    fs.angle_arc(ax, O2, 0.9, 0, np.degrees(dphi), r'$d\phi$', fontsize=10, tr=1.25)
    fs.dot(ax, O2, r=0.05)
    ax.text(-0.25, -0.2, r'$O$', fontsize=11)
    ax.text(1.3, 1.6, '세차', fontsize=9, color=fs.ACC)
    th = np.radians(np.linspace(5, 50, 40))
    curve_arrow(ax, np.c_[1.85 * np.cos(th), 1.85 * np.sin(th)], color=fs.ACC, lw=1.0, ms=8)
    ax.text(1.35, -0.85, '(나) 위에서 본 모습', fontsize=9, ha='center')
    fig.tight_layout(w_pad=0.2)
    fs.save(fig, __file__, 'fig11_10')


# ---------- 그림 11.11 실패(연습문제 8) ----------
def fig11():
    fig, ax = fs.canvas(3.6, 2.6, xlim=(-1.7, 3.6), ylim=(-0.35, 3.0))
    R, r = 1.2, 0.55
    C = np.array([0.0, R])
    fs.ground(ax, -1.6, 3.4, y=0.0)
    ax.add_patch(Circle(C, R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, zorder=2))
    ax.add_patch(Circle(C, r, fc='#c9d6e3', ec=fs.BLACK, lw=1.0, zorder=3))
    fs.dot(ax, C, r=0.05)
    th = np.radians(30)
    u = np.array([np.cos(th), np.sin(th)])
    nrm = np.array([np.sin(th), -np.cos(th)])
    Tp = C + r * nrm
    end = Tp + 2.6 * u
    ax.plot([Tp[0], end[0]], [Tp[1], end[1]], color=fs.BLACK, lw=1.0, zorder=4)
    fs.arrow(ax, end - 0.9 * u, end + 0.15 * u, color=fs.FORCE, lw=1.8, zorder=6)
    ax.text(*(end + np.array([-0.15, 0.3])), r'$\vec T$', color=fs.FORCE, fontsize=12)
    hx = Tp + 1.4 * u
    ax.plot([hx[0], hx[0] + 0.9], [hx[1], hx[1]], ls=':', color=fs.GRAY, lw=0.8)
    fs.angle_arc(ax, hx, 0.6, 0, 30, r'$\theta$', fontsize=11, tr=0.85)
    # 반지름 표시
    pR = C + R * np.array([np.cos(np.radians(135)), np.sin(np.radians(135))])
    ax.plot([C[0], pR[0]], [C[1], pR[1]], color=fs.BLACK, lw=0.8)
    ax.text((C[0] + pR[0]) / 2 - 0.15, (C[1] + pR[1]) / 2 + 0.12, r'$R$', fontsize=11)
    pr = C + r * np.array([np.cos(np.radians(70)), np.sin(np.radians(70))])
    ax.plot([C[0], pr[0]], [C[1], pr[1]], color=fs.BLACK, lw=0.8)
    ax.text(pr[0] + 0.1, pr[1] - 0.05, r'$r$', fontsize=11)
    fs.dot(ax, (0, 0), r=0.05)
    ax.text(-0.25, 0.15, r'$P$', fontsize=11)
    fs.save(fig, __file__, 'fig11_11')


# ---------- 그림 11.12 기울어진 아령의 회전(연습문제 15) ----------
def fig12():
    fig, ax = fs.canvas(2.8, 3.0, xlim=(-1.6, 1.8), ylim=(-1.9, 2.1))
    al = np.radians(30); l = 1.4
    ax.plot([0, 0], [-1.8, 1.8], color=fs.GRAY, lw=0.9, ls='-.')
    ax.text(0.12, 1.85, r'$z$', fontsize=11)
    fs.arrow(ax, (0, 1.05), (0, 1.75), color=fs.ACC, lw=2.0)
    ax.text(-0.35, 1.45, r'$\vec\omega$', color=fs.ACC, fontsize=12)
    p = l * np.array([np.sin(al), np.cos(al)])
    ax.plot([-p[0], p[0]], [-p[1], p[1]], color=fs.BLACK, lw=1.6, zorder=3)
    for s in (1, -1):
        ax.add_patch(Circle(s * p, 0.13, fc=fs.VEL, ec='none', zorder=5))
    ax.text(p[0] + 0.2, p[1], r'$m$', fontsize=11)
    ax.text(-p[0] - 0.42, -p[1], r'$m$', fontsize=11)
    fs.angle_arc(ax, (0, 0), 0.55, 90 - 30, 90, r'$\alpha$', fontsize=11, tr=0.8)
    fs.dim(ax, (0, 0), p, r'$l$', off=-0.22)
    fs.dot(ax, (0, 0), r=0.05)
    th = np.radians(np.linspace(200, 520, 80))
    curve_arrow(ax, np.c_[0.45 * np.cos(th), -1.45 + 0.12 * np.sin(th)], color=fs.ACC, lw=0.9, ms=8)
    fs.save(fig, __file__, 'fig11_12')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12):
        f()
