"""21장 전하와 전기장 그림. python3 figures/ch21/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch, Arc, Ellipse, FancyBboxPatch

k = 8.99e9


def sign(ax, p, q, fs_=11, zorder=7):
    """작은 + / − 기호(점전하 원 없이)."""
    ax.text(p[0], p[1], '+' if q > 0 else '−', color=fs.POS if q > 0 else fs.NEG, ha='center', va='center',
            fontsize=fs_, fontweight='bold', zorder=zorder)


def styled(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def ground_symbol(ax, p, w=0.3):
    x, y = p
    for i, ww in enumerate([w, w * 0.65, w * 0.3]):
        ax.plot([x - ww / 2, x + ww / 2], [y - i * 0.08, y - i * 0.08], color=fs.BLACK, lw=1.1)


# ---------------------------------------------------------------- 21.1 유도 대전
def fig01():
    fig, ax = fs.canvas(5.5, 2.0, xlim=(-0.1, 11.2), ylim=(-1.45, 1.75))
    Rs = 0.72
    for i in range(3):
        ox = i * 3.75
        c = (ox + 2.3, 0.45)
        ax.add_patch(Circle(c, Rs, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
        ax.plot([c[0], c[0]], [c[1] - Rs, -0.75], color=fs.GRAY, lw=2.5, zorder=2)   # 절연 받침대
        ax.plot([c[0] - 0.3, c[0] + 0.3], [-0.75, -0.75], color=fs.GRAY, lw=2.5, zorder=2)
        if i < 2:   # 음으로 대전된 막대
            ax.add_patch(Rectangle((ox + 0.0, 0.32), 1.0, 0.26, fc='#d9d9d9', ec=fs.BLACK, lw=0.9, zorder=3))
            for xx in np.linspace(ox + 0.15, ox + 0.85, 4):
                sign(ax, (xx, 0.45), -1, fs_=9)
        if i == 0:
            for a in (150, 180, 210):
                t = np.radians(a); sign(ax, (c[0] + 0.52 * np.cos(t), c[1] + 0.52 * np.sin(t)), +1, 10)
            for a in (-30, 0, 30):
                t = np.radians(a); sign(ax, (c[0] + 0.52 * np.cos(t), c[1] + 0.52 * np.sin(t)), -1, 10)
        elif i == 1:
            for a in (150, 180, 210):
                t = np.radians(a); sign(ax, (c[0] + 0.52 * np.cos(t), c[1] + 0.52 * np.sin(t)), +1, 10)
            ax.plot([c[0] + Rs, c[0] + 1.2, c[0] + 1.2], [c[1], c[1], -0.85], color=fs.BLACK, lw=1.0, zorder=2)
            ground_symbol(ax, (c[0] + 1.2, -0.85))
            fs.arrow(ax, (c[0] + 1.35, 0.1), (c[0] + 1.35, -0.55), color=fs.NEG, lw=1.0, ms=8)
            ax.text(c[0] + 1.42, -0.2, '전자', fontsize=8, color=fs.NEG, ha='left', va='center')
        else:
            for a in range(0, 360, 60):
                t = np.radians(a + 30); sign(ax, (c[0] + 0.5 * np.cos(t), c[1] + 0.5 * np.sin(t)), +1, 10)
        ax.text(ox + 1.65, -1.3, ['(가) 막대를 가까이', '(나) 먼 쪽을 접지', '(다) 접지를 끊고 막대 제거'][i],
                fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig21_01')


# ---------------------------------------------------------------- 💡 종잇조각의 분극
def fig02():
    fig, ax = fs.canvas(4.0, 1.7, xlim=(-0.2, 6.2), ylim=(-1.05, 1.2))
    ax.add_patch(Rectangle((0, -0.45), 1.3, 0.9, fc='#d9d9d9', ec=fs.BLACK, lw=1.0))
    for yy in (-0.25, 0.05, 0.3):
        for xx in (0.95, 1.15):
            sign(ax, (xx, yy), -1, 9)
    ax.text(0.5, 0.75, '대전된 자', fontsize=9, ha='center')
    c = (3.0, 0.0)
    ax.add_patch(Ellipse(c, 1.5, 0.6, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    sign(ax, (2.5, 0), +1, 12); sign(ax, (3.5, 0), -1, 12)
    ax.text(3.0, 0.55, '분극된 분자', fontsize=9, ha='center')
    fs.arrow(ax, (2.45, -0.45), (1.55, -0.45), color=fs.FORCE, lw=2.0, ms=11)
    ax.text(2.0, -0.82, '큰 인력', fontsize=8.5, color=fs.FORCE, ha='center')
    fs.arrow(ax, (3.55, -0.45), (4.05, -0.45), color=fs.FORCE, lw=1.2, ms=9)
    ax.text(3.85, -0.82, '작은 척력', fontsize=8.5, color=fs.FORCE, ha='center')
    ax.text(4.5, 0.15, '→ 알짜 힘은\n   자 쪽(인력)', fontsize=9, ha='left', va='center')
    fs.save(fig, __file__, 'fig21_02')


# ---------------------------------------------------------------- 쿨롱 법칙의 방향
def fig03():
    fig, ax = fs.canvas(4.6, 2.3, xlim=(-1.6, 5.4), ylim=(-1.6, 2.0))
    for row, (q2, title) in enumerate([(+1, '(가) 같은 부호: 척력'), (-1, '(나) 다른 부호: 인력')]):
        y = 1.15 - row * 2.0
        p1, p2 = (0.4, y), (3.4, y)
        ax.plot([p1[0], p2[0]], [y, y], color=fs.GRAY, lw=0.6, ls=':')
        fs.charge(ax, p1, +1, r=0.17); fs.charge(ax, p2, q2, r=0.17)
        ax.text(p1[0], y + 0.35, '$q_1$', fontsize=10, ha='center')
        ax.text(p2[0], y + 0.35, '$q_2$', fontsize=10, ha='center')
        fs.arrow(ax, (1.2, y - 0.3), (1.9, y - 0.3), color=fs.BLACK, lw=1.0, ms=8)
        ax.text(1.55, y - 0.52, r'$\hat r_{12}$', fontsize=9.5, ha='center')
        if q2 > 0:
            fs.arrow(ax, (p2[0] + 0.2, y), (p2[0] + 1.2, y), color=fs.FORCE, label=r'$\vec F_{12}$', lpos=1, loff=(0.3, 0.0))
            fs.arrow(ax, (p1[0] - 0.2, y), (p1[0] - 1.2, y), color=fs.FORCE, label=r'$\vec F_{21}$', lpos=0.5,
                     loff=(0.0, 0.3))
        else:
            fs.arrow(ax, (p2[0] - 0.2, y), (p2[0] - 1.2, y), color=fs.FORCE, label=r'$\vec F_{12}$', lpos=0.5,
                     loff=(0.0, 0.3))
            fs.arrow(ax, (p1[0] + 0.2, y), (p1[0] + 1.2, y), color=fs.FORCE, label=r'$\vec F_{21}$', lpos=0.5,
                     loff=(0.0, 0.3))
        ax.text(-1.55, y + 0.62, title, fontsize=9, ha='left')
    fs.save(fig, __file__, 'fig21_03')


# ---------------------------------------------------------------- 예제 21.2
def fig04():
    fig, ax = fs.canvas(3.6, 3.3, xlim=(-1.0, 5.0), ylim=(-0.9, 6.6))
    s = 10.0          # 위치: 1 m → 10 단위
    fsc = 4.0         # 힘: 1 N → 4 단위
    q1, q2, q3 = (0, 0), (0.30 * s, 0), (0, 0.40 * s)
    fs.arrow(ax, (-0.6, 0), (4.6, 0), color=fs.GRAY, lw=0.7, ms=8); ax.text(4.65, 0, '$x$', va='center', fontsize=10)
    fs.arrow(ax, (0, -0.6), (0, 6.3), color=fs.GRAY, lw=0.7, ms=8); ax.text(0.15, 6.3, '$y$', fontsize=10)
    ax.plot([q2[0], q3[0]], [q2[1], q3[1]], color=fs.GRAY, lw=0.6, ls='--')
    fs.charge(ax, q1, +1, r=0.22); fs.charge(ax, q2, -1, r=0.22); fs.charge(ax, q3, +1, r=0.22)
    ax.text(-0.35, -0.45, r'$q_1=+2.0\ \mu\mathrm{C}$', fontsize=8.5, ha='left', va='top')
    ax.text(3.0, -0.45, r'$q_2=-3.0\ \mu\mathrm{C}$', fontsize=8.5, ha='center', va='top')
    ax.text(-0.35, 4.0, r'$q_3=+4.0\ \mu\mathrm{C}$', fontsize=8.5, ha='right', va='center')
    ax.text(2.45, 1.25, '0.50 m', fontsize=8.5, color=fs.GRAY, rotation=-53, ha='center', va='center')
    ax.text(1.5, 0.22, '0.30 m', fontsize=8.5, color=fs.GRAY, ha='center')
    ax.text(-0.2, 2.0, '0.40 m', fontsize=8.5, color=fs.GRAY, ha='right', rotation=90, va='center')
    F13 = np.array([0, 0.449]); F23 = np.array([0.259, -0.345]); F3 = F13 + F23
    fs.vec(ax, q3, F13 * fsc, color=fs.FORCE, label=r'$\vec F_{13}$', lpos=1, loff=(-0.35, 0.1))
    fs.vec(ax, q3, F23 * fsc, color=fs.FORCE, label=r'$\vec F_{23}$', lpos=1, loff=(0.4, -0.15))
    fs.vec(ax, q3, F3 * fsc, color=fs.FORCE, lw=2.3, label=r'$\vec F_3$', lpos=1, loff=(0.1, 0.35))
    ax.plot([q3[0] + F13[0] * fsc, q3[0] + F3[0] * fsc], [q3[1] + F13[1] * fsc, q3[1] + F3[1] * fsc],
            color=fs.FORCE, lw=0.7, ls=':')
    ax.plot([q3[0] + F23[0] * fsc, q3[0] + F3[0] * fsc], [q3[1] + F23[1] * fsc, q3[1] + F3[1] * fsc],
            color=fs.FORCE, lw=0.7, ls=':')
    fs.angle_arc(ax, q3, 0.8, 0, np.degrees(np.arctan2(F3[1], F3[0])))
    ax.text(1.75, 4.15, '21.9°', fontsize=8.5, ha='left', va='center')
    ax.plot([q3[0], q3[0] + 1.6], [q3[1], q3[1]], color=fs.GRAY, lw=0.5)
    fs.save(fig, __file__, 'fig21_04')


# ---------------------------------------------------------------- 점전하의 전기력선
def fig05():
    fig, axs = plt.subplots(1, 2, figsize=(4.6, 2.3))
    for ax, q, t in zip(axs, (+1, -1), ('(가) 양전하', '(나) 음전하')):
        ax.set_aspect('equal'); ax.axis('off')
        fs.field_lines(ax, [(0, 0, q)], (-2, 2), (-2, 2), per_unit=12)
        fs.charge(ax, (0, 0), q, r=0.2)
        ax.set_title(t, fontsize=9.5)
    fig.tight_layout()
    fs.save(fig, __file__, 'fig21_05')


# ---------------------------------------------------------------- 쌍극자와 같은 부호 두 전하
def fig06():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.7))
    for ax, q2, t in zip(axs, (-1, +1), ('(가) 전기 쌍극자 ($+q$, $-q$)', '(나) 같은 부호 두 전하 ($+q$, $+q$)')):
        ax.set_aspect('equal'); ax.axis('off')
        fs.field_lines(ax, [(0, 0.5, 1), (0, -0.5, q2)], (-2.2, 2.2), (-2.2, 2.2), per_unit=12, start_angle=7.5)
        fs.charge(ax, (0, 0.5), +1, r=0.17); fs.charge(ax, (0, -0.5), q2, r=0.17)
        ax.set_title(t, fontsize=9)
    fs.arrow(axs[0], (0.55, -0.35), (0.55, 0.35), color=fs.BLACK, lw=1.6, ms=10)
    axs[0].text(0.72, 0, r'$\vec p$', fontsize=11, va='center',
                bbox=dict(fc='white', ec='none', pad=0.5))
    fig.tight_layout()
    fs.save(fig, __file__, 'fig21_06')


# ---------------------------------------------------------------- 쌍극자 장의 기하
def fig07():
    fig, ax = fs.canvas(4.2, 3.2, xlim=(-1.6, 4.6), ylim=(-1.6, 3.6))
    pp, pm = np.array([0, 0.5]), np.array([0, -0.5])
    ax.plot([0, 0], [-1.4, 3.2], color=fs.GRAY, lw=0.7, ls='-.')
    ax.text(-0.2, 3.3, '$z$', fontsize=10, ha='right')
    fs.charge(ax, pp, +1, r=0.17); fs.charge(ax, pm, -1, r=0.17)
    ax.text(-0.3, 0.5, '$+q$', fontsize=10, ha='right', va='center')
    ax.text(-0.3, -0.5, '$-q$', fontsize=10, ha='right', va='center')
    fs.dim(ax, (-0.85, -0.5), (-0.85, 0.5), '$d$', off=0.0, color=fs.BLACK)
    # 축 위의 점
    P = np.array([0, 2.4])
    fs.dot(ax, P, r=0.05)
    ax.text(-0.15, 2.4, '축 위의 점 $(z)$', fontsize=9, ha='right', va='center')
    fs.vec(ax, P, (0, 0.85), color=fs.FIELD, lw=1.4, label=r'$\vec E_+$', lpos=1, loff=(0.3, -0.1))
    fs.vec(ax, (0.12, 2.4), (0, -0.45), color=fs.FIELD, lw=1.4, ls='--')
    ax.text(0.27, 2.05, r'$\vec E_-$', fontsize=10, color=fs.FIELD)
    # 수직 이등분선 위의 점
    Q = np.array([3.0, 0.0])
    ax.plot([-0.1, 4.3], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    ax.plot([pp[0], Q[0]], [pp[1], Q[1]], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([pm[0], Q[0]], [pm[1], Q[1]], color=fs.GRAY, lw=0.7, ls='--')
    fs.dot(ax, Q, r=0.05)
    ax.text(0.9, -0.05, '$r$', fontsize=10, ha='center', va='top')
    ax.text(1.35, 0.55, r'$\sqrt{r^2 + d^2/4}$', fontsize=9, ha='center', rotation=-9)
    L = 1.1
    up = (Q - pp) / np.linalg.norm(Q - pp) * L; um = (pm - Q) / np.linalg.norm(pm - Q) * L
    fs.vec(ax, Q, up, color=fs.FIELD, lw=1.3, label=r'$\vec E_+$', lpos=1, loff=(0.25, -0.05))
    fs.vec(ax, Q, um, color=fs.FIELD, lw=1.3, ls='--', label=r'$\vec E_-$', lpos=1, loff=(-0.1, -0.25))
    fs.vec(ax, Q, up + um, color=fs.FIELD, lw=2.2, label=r'$\vec E$', lpos=1, loff=(0.25, -0.05))
    fs.vec(ax, (-0.05, -0.38), (0, 0.76), color=fs.BLACK, lw=1.5, ms=9)
    ax.text(0.12, 0.05, r'$\vec p$', fontsize=10)
    fs.save(fig, __file__, 'fig21_07')


# ---------------------------------------------------------------- 막대의 수직 이등분선
def fig08():
    fig, ax = fs.canvas(4.4, 2.9, xlim=(-3.2, 3.4), ylim=(-0.8, 4.1))
    L2 = 2.6
    ax.add_patch(Rectangle((-L2, -0.08), 2 * L2, 0.16, fc='#f3c9c2', ec=fs.BLACK, lw=0.9, zorder=3))
    for xx in np.linspace(-2.4, 2.4, 13):
        sign(ax, (xx, -0.28), +1, 7)
    P = np.array([0, 2.5]); x0 = 1.5
    for xe, ls, lab in [(x0, '-', r'$d\vec E$'), (-x0, '--', r"$d\vec E'$")]:
        ax.add_patch(Rectangle((xe - 0.13, -0.08), 0.26, 0.16, fc=fs.POS, ec='none', zorder=4))
        ax.plot([xe, P[0]], [0, P[1]], color=fs.GRAY, lw=0.7, ls='--')
        u = (P - np.array([xe, 0])); u = u / np.linalg.norm(u) * 1.25
        fs.vec(ax, P, u, color=fs.FIELD, lw=1.5, ls=ls, label=lab, lpos=1, loff=(0.3 * np.sign(-xe), 0.12))
    u = (P - np.array([x0, 0])); u = u / np.linalg.norm(u) * 1.25
    ax.plot([P[0] + u[0], P[0] + u[0]], [P[1], P[1] + u[1]], color=fs.FIELD, lw=0.6, ls=':')
    fs.vec(ax, (P[0] - 0.05, P[1]), (0, 2 * u[1]), color=fs.FIELD, lw=2.2)
    ax.text(0.12, P[1] + 2 * u[1] - 0.05, r'$y$ 성분만 남음', fontsize=8.5, color=fs.FIELD, va='center')
    fs.dot(ax, P, r=0.05)
    ax.text(0.15, 2.3, '$P\\,(0, y)$', fontsize=9.5, va='top')
    ax.text(x0, 0.25, r'$dq=\lambda\,dx$', fontsize=9, ha='center', va='bottom')
    ax.text(1.0, 1.4, r'$\sqrt{x^2+y^2}$', fontsize=9, ha='left', va='center')
    ax.plot([0, 0], [0, 2.45], color=fs.GRAY, lw=0.6, ls=':')
    ax.text(-0.12, 1.2, '$y$', fontsize=10, ha='right')
    fs.dim(ax, (0, -0.5), (x0, -0.5), '$x$', off=0.0, color=fs.BLACK)
    ax.text(-L2, -0.6, '$-L/2$', fontsize=9, ha='center', va='top')
    ax.text(L2, -0.6, '$L/2$', fontsize=9, ha='center', va='top')
    fs.save(fig, __file__, 'fig21_08')


# ---------------------------------------------------------------- 예제 21.4 그래프
def fig09():
    fig, ax = fs.plot_axes(4.2, 2.9)
    Q, L = 5.0e-9, 1.0; lam = Q / L
    y = np.logspace(-2, 1, 400)
    ax.loglog(y, k * Q / (y * np.sqrt(y ** 2 + L ** 2 / 4)), color=fs.FIELD, lw=2.0, label='정확한 값')
    ax.loglog(y, 2 * k * lam / y, color=fs.VEL, lw=1.2, ls='--', label=r'무한 직선 $2k\lambda/y$')
    ax.loglog(y, k * Q / y ** 2, color=fs.FORCE, lw=1.2, ls='--', label=r'점전하 $kQ/y^2$')
    for yy in (0.05, 0.5, 2.0):
        ax.plot(yy, k * Q / (yy * np.sqrt(yy ** 2 + L ** 2 / 4)), 'ko', ms=4, zorder=5)
    ax.axvline(L / 2, color=fs.GRAY, lw=0.7, ls=':')
    ax.text(0.53, 3e4, '$y=L/2$', fontsize=8.5, color=fs.GRAY)
    ax.set_xlim(0.01, 10); ax.set_ylim(0.3, 1e5)
    ax.set_xlabel('$y$ (m)'); ax.set_ylabel('$E$ (N/C)')
    ax.legend(fontsize=8.5, frameon=False, loc='lower left')
    fs.save(fig, __file__, 'fig21_09')


# ---------------------------------------------------------------- 고리 축 위의 장
def fig10():
    fig, ax = fs.canvas(4.4, 2.8, xlim=(-1.2, 5.2), ylim=(-1.9, 2.2))
    Rr = 1.35
    ax.add_patch(Ellipse((0, 0), 0.7, 2 * Rr, fc='none', ec=fs.POS, lw=2.0))
    ax.plot([-0.9, 4.9], [0, 0], color=fs.GRAY, lw=0.7, ls='-.')
    ax.text(4.95, -0.05, '$z$', fontsize=10, va='center')
    P = np.array([3.2, 0])
    top, bot = np.array([0, Rr]), np.array([0, -Rr])
    for e, ls, lab in [(top, '-', r'$d\vec E$'), (bot, '--', r"$d\vec E'$")]:
        ax.add_patch(Circle(e, 0.1, fc=fs.POS, ec='none', zorder=5))
        ax.plot([e[0], P[0]], [e[1], P[1]], color=fs.GRAY, lw=0.7, ls='--')
        u = (P - e) / np.linalg.norm(P - e) * 1.3
        fs.vec(ax, P, u, color=fs.FIELD, lw=1.5, ls=ls, label=lab, lpos=1, loff=(0.25, 0.15 * np.sign(u[1])))
    u = (P - top) / np.linalg.norm(P - top) * 1.3
    ax.plot([P[0] + u[0], P[0] + u[0]], [0, u[1]], color=fs.FIELD, lw=0.6, ls=':')
    fs.dot(ax, P, r=0.05)
    ax.text(P[0] - 0.05, 0.15, '$P$', fontsize=10, ha='right', va='bottom')
    fs.angle_arc(ax, P, 0.6, 180 - np.degrees(np.arctan2(Rr, P[0])), 180, r'$\theta$', fontsize=9.5)
    ax.text(0.15, Rr + 0.2, '$dq$', fontsize=10, ha='left')
    ax.text(0.15, -Rr - 0.25, "$dq'$", fontsize=10, ha='left', va='top')
    ax.plot([0, 0], [0, Rr], color=fs.BLACK, lw=0.8)
    ax.text(-0.12, Rr / 2, '$R$', fontsize=10, ha='right')
    fs.dim(ax, (0, -0.5), (P[0], -0.5), '$z$', off=0.0, color=fs.BLACK)
    ax.text(1.75, 1.05, r'$\sqrt{z^2+R^2}$', fontsize=9, ha='center', va='bottom')
    fs.save(fig, __file__, 'fig21_10')


# ---------------------------------------------------------------- 예제 21.5 그래프
def fig11():
    fig, ax = fs.plot_axes(4.0, 2.6)
    Rr, Q = 0.050, 20e-9
    z = np.linspace(-0.15, 0.15, 600)
    E = k * Q * z / (z ** 2 + Rr ** 2) ** 1.5
    ax.plot(z * 100, E / 1e4, color=fs.FIELD, lw=1.8)
    zm = Rr / np.sqrt(2); Em = k * Q * zm / (zm ** 2 + Rr ** 2) ** 1.5
    for sgn in (1, -1):
        ax.plot(sgn * zm * 100, sgn * Em / 1e4, 'ko', ms=4)
        ax.plot([sgn * zm * 100] * 2, [0, sgn * Em / 1e4], color=fs.GRAY, lw=0.7, ls=':')
    ax.annotate(r'$z=R/\sqrt{2}=3.54$ cm' + '\n' + r'$E_{\max}=2.77\times10^4$ N/C', xy=(zm * 100, Em / 1e4),
                xytext=(4.5, -1.6), fontsize=8.5, va='center', arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.axhline(0, color=fs.BLACK, lw=0.7)
    ax.set_xlim(-15, 15); ax.set_ylim(-3.2, 3.2)
    ax.set_xlabel('$z$ (cm)'); ax.set_ylabel(r'$E_z$ ($10^4$ N/C)')
    fs.save(fig, __file__, 'fig21_11')


# ---------------------------------------------------------------- 원판을 고리로 나누기
def fig12():
    fig, ax = fs.canvas(4.2, 2.7, xlim=(-1.3, 5.0), ylim=(-1.9, 2.0))
    Rd = 1.5; ex = 0.28
    ax.add_patch(Ellipse((0, 0), 2 * Rd * ex, 2 * Rd, fc='#f3c9c2', ec=fs.BLACK, lw=1.0))
    r1, r2 = 0.85, 1.05
    th = np.linspace(0, 2 * np.pi, 200)
    ring = np.r_[np.c_[r2 * ex * np.cos(th), r2 * np.sin(th)], np.c_[r1 * ex * np.cos(th[::-1]), r1 * np.sin(th[::-1])]]
    ax.add_patch(Polygon(ring, closed=True, fc=fs.POS, alpha=0.75, ec='none'))
    ax.plot([-1.0, 4.7], [0, 0], color=fs.GRAY, lw=0.7, ls='-.')
    ax.text(4.75, -0.05, '$z$', fontsize=10, va='center')
    P = np.array([3.4, 0]); fs.dot(ax, P, r=0.05)
    ax.text(P[0], 0.15, '$P$', fontsize=10, ha='center', va='bottom')
    fs.vec(ax, P, (1.0, 0), color=fs.FIELD, lw=1.6, label=r'$dE_z$', lpos=1, loff=(0.0, 0.25))
    ax.plot([0, 0], [0, Rd], color=fs.BLACK, lw=0.8)
    ax.text(0.1, 1.25, '$R$', fontsize=10, ha='left', va='center')
    ax.plot([0, 0.0], [0, -r1], color=fs.BLACK, lw=0.8)
    ax.text(0.1, -0.45, '$r$', fontsize=10, ha='left', va='center')
    ax.annotate(r'고리: $dq=\sigma\,2\pi r\,dr$', xy=(r2 * ex * np.cos(-0.6), r2 * np.sin(-0.6) - 0.05),
                xytext=(1.4, -1.65), fontsize=9, arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.annotate('$dr$', xy=(-0.05, 0.95), xytext=(-0.95, 0.9), fontsize=10, va='center',
                arrowprops=dict(arrowstyle='->', lw=0.7))
    fs.dim(ax, (0, -1.15), (P[0], -1.15), '$z$', off=0.0, color=fs.BLACK)
    fs.save(fig, __file__, 'fig21_12')


# ---------------------------------------------------------------- 원판 장의 극한
def fig13():
    fig, ax = fs.plot_axes(4.2, 2.7)
    x = np.logspace(-2, np.log10(30), 400)
    ax.semilogx(x, 1 - x / np.sqrt(x ** 2 + 1), color=fs.FIELD, lw=2.0, label='원판 (정확)')
    ax.axhline(1, color=fs.VEL, lw=1.2, ls='--', label=r'무한 평면 $\sigma/2\varepsilon_0$')
    xx = x[x > 0.4]
    ax.semilogx(xx, 1 / (2 * xx ** 2), color=fs.FORCE, lw=1.2, ls='--', label=r'점전하 $kQ/z^2$')
    for z, lab, dx in [(0.1, '90%', 1.25), (0.5, '55%', 1.25), (10, '0.50%', 0.9)]:
        v = 1 - z / np.sqrt(z ** 2 + 1)
        ax.plot(z, v, 'ko', ms=4, zorder=5)
        ax.text(z * dx, v + 0.06, lab, fontsize=8.5, ha='left' if dx > 1 else 'center')
    ax.set_ylim(0, 1.15); ax.set_xlim(0.01, 30)
    ax.set_xlabel('$z/R$'); ax.set_ylabel(r'$E\,/\,(\sigma/2\varepsilon_0)$')
    ax.legend(fontsize=8.5, frameon=False, loc='center left', bbox_to_anchor=(0.0, 0.42))
    fs.save(fig, __file__, 'fig21_14')


# ---------------------------------------------------------------- 평행판 중첩
def fig14():
    fig, ax = fs.canvas(4.6, 2.6, xlim=(-3.4, 3.4), ylim=(-1.75, 1.95))
    for x0, q in [(-1.0, +1), (1.0, -1)]:
        ax.add_patch(Rectangle((x0 - 0.06, -1.5), 0.12, 3.0, fc=fs.POS if q > 0 else fs.NEG, ec='none', alpha=0.85))
        ax.text(x0, 1.7, '$+\\sigma$' if q > 0 else '$-\\sigma$', fontsize=10, ha='center')
    rows = [(0.95, r'$\vec E_+$', '-'), (0.35, r'$\vec E_-$', '--')]
    regions = [(-2.25, -1, -1), (0.0, +1, +1), (2.25, +1, -1)]   # (중심, E+ 방향, E- 방향)
    for xc, dp, dm in regions:
        for (y, lab, ls), d in zip(rows, (dp, dm)):
            fs.arrow(ax, (xc - 0.4 * d, y), (xc + 0.4 * d, y), color=fs.FIELD, lw=1.3, ls=ls, ms=9)
        if xc == 0:
            fs.arrow(ax, (-0.65, -0.55), (0.65, -0.55), color=fs.FIELD, lw=2.6, ms=13)
            ax.text(0, -0.95, r'$E=\sigma/\varepsilon_0$', fontsize=9.5, ha='center', color=fs.FIELD)
        else:
            ax.text(xc, -0.55, '$E=0$', fontsize=9.5, ha='center', va='center', color=fs.FIELD)
    ax.text(-3.35, 0.95, r'$\vec E_+$', fontsize=9.5, color=fs.FIELD, va='center')
    ax.text(-3.35, 0.35, r'$\vec E_-$', fontsize=9.5, color=fs.FIELD, va='center')
    ax.text(-3.35, -0.55, '합', fontsize=9.5, va='center')
    ax.plot([-3.4, 3.4], [-0.2, -0.2], color=fs.GRAY, lw=0.5)
    fs.save(fig, __file__, 'fig21_13')


# ---------------------------------------------------------------- 예제 21.7 전자 편향
def fig15():
    fig, ax = fs.canvas(4.6, 2.7, xlim=(-1.4, 5.8), ylim=(-1.95, 1.75))
    Lp = 3.0
    ax.add_patch(Rectangle((0, 1.0), Lp, 0.12, fc=fs.NEG, ec='none'))
    ax.add_patch(Rectangle((0, -1.12), Lp, 0.12, fc=fs.POS, ec='none'))
    for xx in np.linspace(0.3, 2.7, 5):
        sign(ax, (xx, 1.3), -1, 9); sign(ax, (xx, -1.32), +1, 9)
        fs.arrow(ax, (xx, -0.9), (xx, -0.35), color=fs.FIELD, lw=1.0, ms=8)
    ax.text(-0.1, -0.62, r'$\vec E$', fontsize=10, color=fs.FIELD, ha='right', va='center')
    y0, dy = 0.4, 0.75          # 처짐을 과장해 그림
    x = np.linspace(0, Lp, 100); yy = y0 - dy * (x / Lp) ** 2
    ax.plot(np.r_[-1.2, x], np.r_[y0, yy], color=fs.VEL, lw=1.5)
    slope = -2 * dy / Lp
    x2 = np.linspace(Lp, 5.6, 20); ax.plot(x2, y0 - dy + slope * (x2 - Lp), color=fs.VEL, lw=1.5, ls='-')
    ax.plot([Lp, 5.6], [y0 - dy, y0 - dy], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, (Lp, y0 - dy), 1.3, np.degrees(np.arctan(slope)), 0, '7.5°', fontsize=8.5, tr=1.75)
    ax.add_patch(Circle((-0.9, y0), 0.09, fc=fs.NEG, ec='none', zorder=6))
    fs.vec(ax, (-0.9, y0 + 0.25), (0.8, 0), color=fs.VEL, lw=1.4, label=r'$v_0$', lpos=0.5, loff=(0, 0.2))
    xm = 1.6; ym = y0 - dy * (xm / Lp) ** 2
    ax.add_patch(Circle((xm, ym), 0.09, fc=fs.NEG, ec='none', zorder=6))
    fs.vec(ax, (xm, ym - 0.1), (0, -0.55), color=fs.FORCE, lw=1.5)
    ax.text(xm - 0.12, ym - 0.4, r'$\vec F=-e\vec E$', fontsize=9.5, color=fs.FORCE, ha='right', va='center',
            bbox=dict(fc='white', ec='none', pad=0.3))
    ax.plot([Lp + 0.15, Lp + 0.45], [y0, y0], color=fs.GRAY, lw=0.5)
    ax.annotate('', xy=(Lp + 0.3, y0 - dy), xytext=(Lp + 0.3, y0),
                arrowprops=dict(arrowstyle='<|-|>', color=fs.BLACK, lw=0.8, mutation_scale=7))
    ax.text(Lp + 0.42, y0 - dy / 2 + 0.05, '$y$ = 2.0 mm', fontsize=8.5, va='center')
    fs.dim(ax, (0, -1.6), (Lp, -1.6), '3.0 cm', off=-0.0, color=fs.BLACK)
    fs.save(fig, __file__, 'fig21_15')


# ---------------------------------------------------------------- 균일한 장 속 쌍극자
def fig16():
    fig, ax = fs.canvas(4.0, 2.7, xlim=(-2.6, 2.9), ylim=(-1.75, 1.95))
    for y in np.linspace(-1.5, 1.5, 6):
        fs.arrow(ax, (-2.5, y), (2.6, y), color=fs.FIELD, lw=0.7, ms=8, zorder=1)
    ax.text(2.65, 1.5, r'$\vec E$', fontsize=11, color=fs.FIELD, va='center')
    th = np.radians(35); hd = 1.0
    u = np.array([np.cos(th), np.sin(th)])
    pp, pm = hd * u, -hd * u
    ax.plot([pm[0], pp[0]], [pm[1], pp[1]], color=fs.BLACK, lw=1.2, zorder=4)
    fs.charge(ax, pp, +1, r=0.15); fs.charge(ax, pm, -1, r=0.15)
    fs.vec(ax, pp + (0.17, 0), (1.0, 0), color=fs.FORCE, lw=1.8, label=r'$q\vec E$', lpos=1, loff=(0.05, 0.25))
    fs.vec(ax, pm - (0.17, 0), (-1.0, 0), color=fs.FORCE, lw=1.8, label=r'$-q\vec E$', lpos=1, loff=(-0.05, 0.25))
    fs.vec(ax, (0, 0) - 0.45 * u - (0.25 * u[1], -0.25 * u[0]), 0.9 * u, color=fs.BLACK, lw=1.6, ms=10)
    ax.text(0.3, -0.45, r'$\vec p$', fontsize=11)
    ax.plot([0, 1.3], [0, 0], color=fs.GRAY, lw=0.6, ls='--', zorder=3)
    fs.angle_arc(ax, (0, 0), 0.55, 0, 35, r'$\theta$', fontsize=10)
    ax.add_patch(Arc((0, 0), 2.9, 2.9, theta1=60, theta2=100, color=fs.ACC, lw=1.4))
    t = np.radians(60)
    ax.add_patch(FancyArrowPatch((1.45 * np.cos(t + 0.05), 1.45 * np.sin(t + 0.05)), (1.45 * np.cos(t), 1.45 * np.sin(t)),
                                 arrowstyle='-|>', mutation_scale=10, color=fs.ACC, lw=0))
    fs.cross_in(ax, (-0.55, 1.45), r=0.1, color=fs.ACC)
    ax.text(-0.75, 1.45, r'$\vec\tau=\vec p\times\vec E$', fontsize=9, color=fs.ACC, ha='right', va='center',
            bbox=dict(fc='white', ec='none', pad=0.5))
    fs.save(fig, __file__, 'fig21_16')


# ---------------------------------------------------------------- 연습문제 9 반원
def fig17():
    fig, ax = fs.canvas(3.0, 1.9, xlim=(-1.9, 1.9), ylim=(-0.45, 1.75))
    Rr = 1.4
    t = np.linspace(0, np.pi, 200)
    ax.plot(Rr * np.cos(t), Rr * np.sin(t), color=fs.POS, lw=2.4)
    ax.plot([-1.8, 1.8], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    fs.dot(ax, (0, 0), r=0.04); ax.text(0, -0.12, 'O', fontsize=9.5, ha='center', va='top')
    a = np.radians(55)
    e = Rr * np.array([np.cos(a), np.sin(a)])
    ax.plot([0, e[0]], [0, e[1]], color=fs.BLACK, lw=0.8)
    ax.text(e[0] / 2 - 0.15, e[1] / 2 + 0.05, '$R$', fontsize=10, ha='right')
    ax.add_patch(Arc((0, 0), 2 * Rr, 2 * Rr, theta1=52, theta2=58, color=fs.BLACK, lw=4))
    ax.text(e[0] + 0.12, e[1] + 0.1, r'$dq=\lambda R\,d\theta$', fontsize=9, ha='left')
    fs.angle_arc(ax, (0, 0), 0.4, 0, 55, r'$\theta$', fontsize=10)
    ax.text(-1.55, 1.3, '$Q$', fontsize=10, color=fs.POS)
    fs.save(fig, __file__, 'fig21_17')


# ---------------------------------------------------------------- 연습문제 10 막대 연장선
def fig18():
    fig, ax = fs.canvas(4.0, 1.2, xlim=(-0.4, 6.4), ylim=(-0.9, 0.8))
    Lr = 3.2
    ax.add_patch(Rectangle((0, -0.08), Lr, 0.16, fc='#f3c9c2', ec=fs.BLACK, lw=0.9))
    ax.add_patch(Rectangle((1.8, -0.08), 0.22, 0.16, fc=fs.POS, ec='none'))
    ax.text(1.91, 0.18, '$dx$', fontsize=9, ha='center', va='bottom')
    ax.plot([-0.3, 6.2], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    P = (Lr + 1.6, 0); fs.dot(ax, P, r=0.05)
    ax.text(P[0], 0.15, '$P$', fontsize=10, ha='center', va='bottom')
    fs.dim(ax, (0, -0.35), (Lr, -0.35), '$L$', off=0.0, color=fs.BLACK)
    fs.dim(ax, (Lr, -0.35), (P[0], -0.35), '$a$', off=0.0, color=fs.BLACK)
    ax.text(0, 0.18, '$x=0$', fontsize=9, ha='center', va='bottom')
    ax.text(Lr / 2 - 0.9, 0.18, '$Q$', fontsize=10, color=fs.POS, ha='center', va='bottom')
    fs.save(fig, __file__, 'fig21_18')


if __name__ == '__main__':
    names = sys.argv[1:] or [f'fig{i:02d}' for i in range(1, 19)]
    for n in names:
        globals()[n]()
