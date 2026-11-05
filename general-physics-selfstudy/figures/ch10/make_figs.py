import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
"""10장 회전 운동학과 관성모멘트 그림."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Ellipse, Arc, Wedge

F = __file__
D2R = np.pi / 180
AX = dict(color=fs.BLACK, lw=1.0, ls='-.')      # 회전축


def u(ang):
    return np.array([np.cos(ang * D2R), np.sin(ang * D2R)])


def dimline(ax, p, q, text, off=(0, 0), color=fs.BLACK, fontsize=9.5, **kw):
    ax.annotate('', xy=p, xytext=q, arrowprops=dict(arrowstyle='<->', color=color, lw=0.8, shrinkA=0, shrinkB=0))
    m = (np.asarray(p) + np.asarray(q)) / 2 + np.asarray(off)
    ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color, **kw)


def ccw_arrow(ax, c, r, th1, th2, color=fs.BLACK, lw=1.2):
    """중심 c, 반지름 r인 호를 th1→th2(도, 반시계)로 그리고 끝에 화살촉."""
    ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=th1, theta2=th2, color=color, lw=lw))
    e = np.asarray(c) + r * u(th2)
    d = u(th2 + 90)
    ax.add_patch(FancyArrowPatch(e - d * 0.02, e + d * 0.06, arrowstyle='-|>', mutation_scale=10, color=color, lw=0))


# ---------------------------------------------------------------- 그림 10.1 각위치와 호의 길이
def fig01():
    fig, ax = fs.canvas(3.2, 2.8, xlim=(-1.7, 2.3), ylim=(-1.6, 1.9))
    R = 1.4
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.3))
    fs.arrow(ax, (-1.7, 0), (2.2, 0), lw=0.8, ms=8); ax.text(2.2, -0.2, r'$x$', fontsize=10)
    th = 55
    r = 1.0
    ax.plot([0, R * np.cos(th * D2R)], [0, R * np.sin(th * D2R)], color=fs.FORCE, lw=2)
    ax.text(*(u(th) * (R + 0.25)), '기준선', fontsize=8.5, color=fs.FORCE, ha='center')
    ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=0, theta2=th, color=fs.VEL, lw=2.2))
    ax.text(*(u(th / 2) * (r + 0.18)), r'$s$', fontsize=11, color=fs.VEL, ha='center', va='center')
    fs.angle_arc(ax, (0, 0), 0.35, 0, th, r'$\theta$', tr=0.55)
    ax.plot(*u(th) * r, 'o', color=fs.VEL, ms=4)
    ax.text(0.62, -0.18, r'$r$', fontsize=10)
    ax.plot([0, r], [0, 0], color=fs.BLACK, lw=1.4)
    fs.dot_out(ax, (0, 0), r=0.08)
    ax.text(-0.5, -0.95, '회전축(⊙)', fontsize=8.5, color=fs.GRAY)
    ccw_arrow(ax, (0, 0), R + 0.15, 100, 150)
    fs.save(fig, F, 'fig10_01')


# ---------------------------------------------------------------- 그림 10.2 예제 10.1의 ω(t), α(t)
def fig02():
    t = np.linspace(0, 3.5, 300)
    w = 8 * t - 3 * t ** 2
    al = 8 - 6 * t
    fig, axs = plt.subplots(2, 1, figsize=(3.8, 3.3), sharex=True)
    for ax in axs:
        ax.grid(True, lw=0.4, color='#d0d0d0')
        for s_ in ('top', 'right'):
            ax.spines[s_].set_visible(False)
        ax.axhline(0, color=fs.BLACK, lw=0.7)
        ax.axvline(4 / 3, color=fs.GRAY, lw=0.7, ls=':'); ax.axvline(8 / 3, color=fs.GRAY, lw=0.7, ls=':')
    axs[0].plot(t, w, color=fs.VEL, lw=2)
    axs[0].plot(4 / 3, 16 / 3, 'o', color=fs.VEL, ms=4)
    axs[0].text(4 / 3 + 0.08, 16 / 3 + 0.2, r'최대 $5.33\ \mathrm{rad/s}$', fontsize=8.5, color=fs.VEL)
    axs[0].plot(8 / 3, 0, 'o', color=fs.FORCE, ms=4)
    axs[0].text(8 / 3 + 0.08, 0.7, '순간 정지', fontsize=8.5, color=fs.FORCE)
    axs[0].set_ylabel(r'$\omega$ (rad/s)'); axs[0].set_ylim(-14, 8)
    axs[1].plot(t, al, color=fs.ACC, lw=2)
    axs[1].set_ylabel(r'$\alpha$ (rad/s$^2$)'); axs[1].set_ylim(-14, 10)
    axs[1].set_xlabel(r'$t$ (s)'); axs[1].set_xlim(0, 3.5)
    axs[1].set_xticks([0, 1, 4 / 3, 2, 8 / 3, 3]); axs[1].set_xticklabels(['0', '1', r'$\frac{4}{3}$', '2', r'$\frac{8}{3}$', '3'])
    fig.align_ylabels(axs)
    fs.save(fig, F, 'fig10_02')


# ---------------------------------------------------------------- 그림 10.3 각속도 벡터와 v = ω × r
def fig03():
    fig, ax = fs.canvas(3.4, 3.1, xlim=(-1.9, 2.3), ylim=(-0.4, 3.3))
    O = np.array([0.0, 0.0]); C = np.array([0.0, 1.3])
    rx, ry = 1.4, 0.38
    ax.plot([0, 0], [-0.3, 3.2], **AX)
    fs.ellipse3d(ax, C, rx, ry, color=fs.GRAY, lw=1.0)
    t = -35 * D2R
    P = C + np.array([rx * np.cos(t), ry * np.sin(t)])
    fs.arrow(ax, (0, 2.2), (0, 3.1), color=fs.FIELD, lw=2.2)
    ax.text(0.15, 3.05, r'$\vec{\omega}$', fontsize=12, color=fs.FIELD)
    ax.add_patch(Arc((0, 2.45), 0.7, 0.2, theta1=200, theta2=340, color=fs.FIELD, lw=1.0))
    ax.add_patch(FancyArrowPatch((0.31, 2.405), (0.34, 2.42), arrowstyle='-|>', mutation_scale=8, color=fs.FIELD, lw=0))
    fs.arrow(ax, O, P, color=fs.BLACK, lw=1.6)
    ax.text(*(P * 0.5 + np.array([0.15, -0.15])), r'$\vec{r}$', fontsize=11)
    ax.plot([C[0], P[0]], [C[1], P[1]], color=fs.BLACK, lw=1.0, ls='--')
    ax.text(*((C + P) / 2 + np.array([-0.05, 0.17])), r'$r_\perp=r\sin\phi$', fontsize=9, ha='center')
    ang_r = np.degrees(np.arctan2(P[1], P[0]))
    fs.angle_arc(ax, O, 0.42, ang_r, 90, r'$\phi$', tr=0.6)
    vdir = np.array([-rx * np.sin(t), ry * np.cos(t)]); vdir /= np.linalg.norm(vdir)
    fs.vec(ax, P, vdir * 0.9, color=fs.VEL, lw=1.8)
    ax.text(*(P + vdir * 1.0 + np.array([0.1, 0.12])), r'$\vec{v}=\vec{\omega}\times\vec{r}$', fontsize=9.5,
            color=fs.VEL, ha='left')
    ax.plot(*P, 'o', color=fs.BLACK, ms=4)
    fs.dot(ax, O, r=0.04); ax.text(-0.2, -0.15, 'O', fontsize=9)
    ax.text(-1.85, 3.0, '회전축', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, F, 'fig10_03')


# ---------------------------------------------------------------- 그림 10.4 접선 가속도와 지름 가속도
def fig04():
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.7))
    R = 1.0
    th = 35
    for k, ax in enumerate(axs):
        ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.2, 2.3); ax.set_ylim(-1.45, 2.0)
        ax.add_patch(Circle((0, 0), R, fc='none', ec=fs.GRAY, lw=1.0, ls='--'))
        fs.dot(ax, (0, 0), r=0.035)
        P = R * u(th)
        ax.plot([0, P[0]], [0, P[1]], color=fs.GRAY, lw=0.8)
        ax.plot(*P, 'o', color=fs.BLACK, ms=5, zorder=7)
        if k == 0:
            fs.angle_arc(ax, (0, 0), 0.3, 0, th, r'$\theta$', tr=0.47, fontsize=9)
            ax.plot([0, 1.3], [0, 0], color=fs.GRAY, lw=0.6)
        if k == 0:
            fs.vec(ax, P, u(th) * 0.6, color=fs.BLACK, lw=1.5)
            ax.text(*(P + u(th) * 0.78), r'$\hat{r}$', fontsize=12, ha='center', va='center')
            fs.vec(ax, P, u(th + 90) * 0.6, color=fs.BLACK, lw=1.5)
            ax.text(*(P + u(th + 90) * 0.78), r'$\hat{\theta}$', fontsize=12, ha='center', va='center')
            ax.text(0.55, -1.35, r'(가) 단위벡터 $\hat{r}$, $\hat{\theta}$', fontsize=9, ha='center')
        else:
            at, ar = 0.55, 0.8
            fs.vec(ax, P, u(th + 90) * at, color=fs.ACC, lw=1.4)
            ax.text(*(P + u(th + 90) * (at + 0.12) + u(th) * 0.35), r'$a_t=r\alpha$', fontsize=9, color=fs.ACC,
                    ha='center')
            fs.vec(ax, P, -u(th) * ar, color=fs.ACC, lw=1.4)
            ax.text(*(P + np.array([0.05, -0.68])), r'$a_r=\omega^2r$', fontsize=9, color=fs.ACC,
                    ha='center')
            A = u(th + 90) * at - u(th) * ar
            fs.vec(ax, P, A, color=fs.ACC, lw=2.2)
            ax.plot([P[0] + u(th + 90)[0] * at, P[0] + A[0]], [P[1] + u(th + 90)[1] * at, P[1] + A[1]],
                    color=fs.ACC, lw=0.6, ls=':')
            ax.plot([P[0] - u(th)[0] * ar, P[0] + A[0]], [P[1] - u(th)[1] * ar, P[1] + A[1]], color=fs.ACC, lw=0.6,
                    ls=':')
            ax.text(*(P + A + np.array([-0.12, 0.15])), r'$\vec{a}$', fontsize=12, color=fs.ACC, ha='center')
            ax.text(0.55, -1.35, '(나) 가속도의 두 성분', fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, F, 'fig10_04')


# ---------------------------------------------------------------- 그림 10.5 회전하는 고리의 반쪽(플라이휠)
def fig05():
    R = 1.5
    fig, ax = fs.canvas(3.4, 2.3, xlim=(-2.2, 2.2), ylim=(-1.0, 2.0))
    th = np.linspace(0, np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.BLACK, lw=4, solid_capstyle='butt', alpha=0.35)
    ax.plot(R * np.cos(th), R * np.sin(th), color=fs.BLACK, lw=1.0)
    th2 = np.linspace(np.pi, 2 * np.pi, 100)
    ax.plot(R * np.cos(th2), R * np.sin(th2), color=fs.GRAY, lw=0.8, ls=':')
    ax.plot([-2.0, 2.0], [0, 0], color=fs.GRAY, lw=0.6, ls='--')
    fs.dot(ax, (0, 0), r=0.04)
    for x in (-R, R):
        fs.arrow(ax, (x, 0), (x, -0.75), color=fs.FORCE, lw=1.8)
        ax.text(x + (0.2 if x > 0 else -0.2), -0.55, r'$T$', fontsize=11, color=fs.FORCE, ha='center')
    a, da = 60, 12
    ax.plot(R * np.cos(np.linspace(a, a + da, 20) * D2R), R * np.sin(np.linspace(a, a + da, 20) * D2R),
            color=fs.ORANGE, lw=5, solid_capstyle='butt')
    m = a + da / 2
    fs.vec(ax, R * u(m), -u(m) * 0.7, color=fs.ACC, lw=1.6)
    ax.text(*(R * u(m) - u(m) * 0.95 + np.array([0.45, 0.0])), r'$\omega^2R\,dm$', fontsize=9, color=fs.ACC)
    ax.plot([0, R * np.cos(m * D2R) * 0.55], [0, R * np.sin(m * D2R) * 0.55], color=fs.GRAY, lw=0.6)
    fs.angle_arc(ax, (0, 0), 0.4, 0, m, r'$\theta$', tr=0.58, fontsize=9)
    ax.text(*(R * u(a + da + 8) + np.array([0.0, 0.18])), r'$dm=\rho AR\,d\theta$', fontsize=9, color=fs.ORANGE)
    ax.text(-1.2, 1.6, r'$\omega$', fontsize=11)
    ccw_arrow(ax, (0, 0), R + 0.3, 105, 140)
    fs.save(fig, F, 'fig10_05')


# ---------------------------------------------------------------- 그림 10.6 가는 막대의 질량 요소
def fig06():
    fig, axs = plt.subplots(2, 1, figsize=(3.8, 2.6))
    L = 3.0
    for k, ax in enumerate(axs):
        ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.0, 3.4 if k else 2.0); ax.set_ylim(-0.75, 0.75)
        x0 = -L / 2 if k == 0 else 0.0
        ax.add_patch(Rectangle((x0, -0.07), L, 0.14, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
        xa = 0.0
        ax.plot([xa, xa], [-0.6, 0.6], **AX)
        xe = 0.9 if k == 0 else 1.9
        ax.add_patch(Rectangle((xe, -0.07), 0.15, 0.14, fc=fs.SURF, ec=fs.BLACK, lw=0.8, zorder=3))
        ax.annotate('', xy=(xa, 0.28), xytext=(xe, 0.28), arrowprops=dict(arrowstyle='<->', lw=0.8, shrinkA=0, shrinkB=0))
        ax.text((xa + xe) / 2, 0.45, r'$x$', fontsize=10, ha='center')
        ax.text(xe + 0.08, -0.32, r'$dm=\frac{M}{L}dx$', fontsize=9, ha='center')
        if k == 0:
            ax.text(-1.5, -0.62, r'$-\frac{L}{2}$', fontsize=9, ha='center'); ax.text(1.5, -0.62, r'$\frac{L}{2}$', fontsize=9, ha='center')
            ax.text(-1.95, 0.45, '(가) 중심축', fontsize=9)
        else:
            ax.text(-0.15, -0.3, '0', fontsize=9, ha='center'); ax.text(3.0, -0.3, r'$L$', fontsize=9, ha='center')
            ax.text(-1.95, 0.45, '(나) 끝을 지나는 축', fontsize=9)
    fig.subplots_adjust(hspace=0.15)
    fs.save(fig, F, 'fig10_06')


# ---------------------------------------------------------------- 그림 10.7 원판을 고리로 나누기
def fig07():
    R = 1.4
    fig, ax = fs.canvas(2.8, 2.6, xlim=(-1.6, 1.9), ylim=(-1.6, 1.6))
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.3))
    r, dr = 0.85, 0.16
    ax.add_patch(Wedge((0, 0), r + dr, 0, 360, width=dr, fc=fs.SURF, ec=fs.BLACK, lw=0.7))
    fs.dot_out(ax, (0, 0), r=0.07)
    fs.arrow(ax, (0, 0), r * u(-35), lw=1.0, ms=8)
    ax.text(*(r * u(-35) * 0.5 + np.array([0.05, -0.18])), r'$r$', fontsize=10)
    p = (r + dr / 2) * u(30)
    ax.annotate(r'$dr$', xy=p, xytext=p + np.array([0.75, 0.55]), fontsize=10,
                arrowprops=dict(arrowstyle='-', lw=0.6))
    ax.plot([0, R * np.cos(150 * D2R)], [0, R * np.sin(150 * D2R)], color=fs.GRAY, lw=0.8)
    ax.text(*(1.22 * u(150) + np.array([0.0, 0.15])), r'$R$', fontsize=10, color=fs.GRAY, ha='center')
    ax.text(0.2, 1.48, r'$dm=\sigma\,2\pi r\,dr$', fontsize=9)
    fs.save(fig, F, 'fig10_07')


# ---------------------------------------------------------------- 그림 10.8 구 껍질을 띠로 나누기
def fig08():
    R = 1.4
    fig, ax = fs.canvas(3.0, 3.0, xlim=(-1.8, 2.1), ylim=(-1.75, 1.9))
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.3, alpha=0.6))
    ax.plot([0, 0], [-1.7, 1.85], **AX)
    th, dth = 50, 9
    for a in (th, th + dth):
        fs.ellipse3d(ax, (0, R * np.cos(a * D2R)), R * np.sin(a * D2R), 0.22 * R * np.sin(a * D2R), color=fs.BLACK, lw=0.7)
    y1, y2 = R * np.cos(th * D2R), R * np.cos((th + dth) * D2R)
    tt = np.linspace(np.pi, 2 * np.pi, 80)
    xs1 = R * np.sin(th * D2R) * np.cos(tt); ys1 = y1 + 0.22 * R * np.sin(th * D2R) * np.sin(tt)
    xs2 = R * np.sin((th + dth) * D2R) * np.cos(tt[::-1]); ys2 = y2 + 0.22 * R * np.sin((th + dth) * D2R) * np.sin(tt[::-1])
    ax.add_patch(Polygon(np.c_[np.r_[xs1, xs2], np.r_[ys1, ys2]], closed=True, fc=fs.SURF, ec='none', alpha=0.9))
    P = R * u(90 - th)
    ax.plot([0, P[0]], [0, P[1]], color=fs.GRAY, lw=0.9)
    fs.angle_arc(ax, (0, 0), 0.45, 90 - th, 90, r'$\theta$', tr=0.65, fontsize=9)
    ax.text(*(P * 0.55 + np.array([0.12, -0.08])), r'$R$', fontsize=10, color=fs.GRAY)
    ax.annotate('', xy=(0, y1 + 0.05), xytext=(P[0], y1 + 0.05), arrowprops=dict(arrowstyle='<->', lw=0.7, shrinkA=0, shrinkB=0))
    ax.text(P[0] / 2, y1 + 0.45, r'$R\sin\theta$', fontsize=9, ha='center')
    Q = R * u(90 - th - dth / 2)
    ax.annotate(r'폭 $R\,d\theta$', xy=Q, xytext=Q + np.array([0.45, 0.25]), fontsize=9,
                arrowprops=dict(arrowstyle='-', lw=0.6))
    fs.save(fig, F, 'fig10_08')


# ---------------------------------------------------------------- 그림 10.9 속이 찬 공: 원판과 껍질
def fig09():
    R = 1.3
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.5))
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.6, 2.2); ax.set_ylim(-1.75, 1.75)
    ax = axs[0]
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, alpha=0.7))
    ax.plot([0, 0], [-1.6, 1.7], **AX)
    ax.text(0.08, 1.6, r'$z$', fontsize=10)
    z, dz = 0.6, 0.12
    rz = np.sqrt(R ** 2 - z ** 2)
    ax.add_patch(Ellipse((0, z), 2 * rz, 0.4 * rz, fc=fs.SURF, ec=fs.BLACK, lw=0.8, zorder=3))
    ax.add_patch(Rectangle((-rz, z - dz), 2 * rz, dz, fc=fs.SURF, ec='none', zorder=2))
    ax.plot([-rz, -rz], [z - dz, z], color=fs.BLACK, lw=0.8); ax.plot([rz, rz], [z - dz, z], color=fs.BLACK, lw=0.8)
    ax.add_patch(Arc((0, z - dz), 2 * rz, 0.4 * rz, theta1=180, theta2=360, color=fs.BLACK, lw=0.8))
    ax.annotate('', xy=(0, z + 0.02), xytext=(rz, z + 0.02), arrowprops=dict(arrowstyle='<->', lw=0.7, shrinkA=0, shrinkB=0), zorder=5)
    ax.text(rz / 2 + 0.45, z + 0.5, r'$\sqrt{R^2-z^2}$', fontsize=8.5, ha='center')
    ax.annotate('', xy=(-1.45, 0), xytext=(-1.45, z), arrowprops=dict(arrowstyle='<->', lw=0.7, shrinkA=0, shrinkB=0))
    ax.plot([-1.5, 0], [0, 0], color=fs.GRAY, lw=0.5, ls=':'); ax.plot([-1.5, -rz], [z, z], color=fs.GRAY, lw=0.5, ls=':')
    ax.text(-1.55, z / 2, r'$z$', fontsize=9.5, ha='right', va='center')
    ax.annotate(r'$dz$', xy=(rz + 0.02, z - dz / 2), xytext=(rz + 0.45, z - 0.35), fontsize=9,
                arrowprops=dict(arrowstyle='-', lw=0.6))
    ax.text(0.3, -1.7, '(가) 원판으로 나누기', fontsize=9, ha='center')
    ax = axs[1]
    ax.add_patch(Circle((0, 0), R, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2))
    r, dr = 0.8, 0.15
    ax.add_patch(Wedge((0, 0), r + dr, 0, 360, width=dr, fc=fs.SURF, ec=fs.BLACK, lw=0.7))
    fs.dot(ax, (0, 0), r=0.04)
    fs.arrow(ax, (0, 0), r * u(-40), lw=1.0, ms=8)
    ax.text(*(r * u(-40) * 0.5 + np.array([0.05, -0.2])), r'$r$', fontsize=10)
    p = (r + dr / 2) * u(35)
    ax.annotate(r'$dr$', xy=p, xytext=p + np.array([0.7, 0.5]), fontsize=10, arrowprops=dict(arrowstyle='-', lw=0.6))
    ax.text(0.3, -1.7, '(나) 구 껍질로 나누기', fontsize=9, ha='center')
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, F, 'fig10_09')


# ---------------------------------------------------------------- 그림 10.10 평행축 정리
def fig10():
    fig, ax = fs.canvas(3.6, 2.8, xlim=(-2.2, 2.6), ylim=(-1.6, 2.1))
    t = np.linspace(0, 2 * np.pi, 200)
    rr = 1.25 + 0.18 * np.cos(3 * t) + 0.1 * np.sin(2 * t)
    ax.add_patch(Polygon(np.c_[1.25 * rr * np.cos(t), 0.95 * rr * np.sin(t)], closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2))
    fs.arrow(ax, (-2.1, 0), (2.5, 0), lw=0.7, ms=7); ax.text(2.5, -0.2, r'$x$', fontsize=10)
    fs.arrow(ax, (0, -1.5), (0, 2.0), lw=0.7, ms=7); ax.text(0.1, 1.95, r'$y$', fontsize=10)
    cm = np.array([0.0, 0.0]); P = np.array([1.1, 0.7]); dm = np.array([-0.7, 0.55])
    fs.dot_out(ax, cm, r=0.09)
    fs.dot_out(ax, P, r=0.09)
    ax.text(0.15, -0.25, 'cm', fontsize=9)
    ax.text(P[0] + 0.15, P[1] + 0.15, r'$(a,b)$', fontsize=9.5)
    ax.plot([cm[0], P[0]], [cm[1], P[1]], color=fs.FORCE, lw=1.4)
    ax.text(0.65, 0.2, r'$d$', fontsize=11, color=fs.FORCE)
    ax.add_patch(Rectangle(dm - 0.06, 0.12, 0.12, fc=fs.ORANGE, ec=fs.BLACK, lw=0.6, zorder=6))
    ax.text(dm[0] - 0.1, dm[1] + 0.22, r'$dm\ (x,y)$', fontsize=9.5, ha='center')
    ax.plot([cm[0], dm[0]], [cm[1], dm[1]], color=fs.GRAY, lw=0.9, ls='--')
    ax.plot([P[0], dm[0]], [P[1], dm[1]], color=fs.VEL, lw=0.9, ls='--')
    ax.text(-2.15, -1.5, '두 축 모두 종이면에 수직(⊙)', fontsize=8, color=fs.GRAY)
    fs.save(fig, F, 'fig10_10')


# ---------------------------------------------------------------- 그림 10.11 수직축 정리
def fig11():
    fig, ax = fs.canvas(3.4, 2.6, xlim=(-2.2, 2.5), ylim=(-1.3, 2.0))
    ex, ey = np.array([-0.7, -0.45]), np.array([1.0, 0.0])
    plate = [ex * a + ey * b for a, b in ((-1.0, -1.1), (1.0, -1.1), (1.0, 1.4), (-1.0, 1.4))]
    ax.add_patch(Polygon(plate, closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2, alpha=0.9))
    for d, t_ in ((ex * 1.9, r'$x$'), (ey * 2.1, r'$y$'), (np.array([0, 1.8]), r'$z$')):
        fs.arrow(ax, (0, 0), d, lw=1.0, ms=8)
        ax.text(*(d * 1.08 + np.array([0.0, 0.05])), t_, fontsize=11, ha='center', va='center')
    p = ex * 0.7 + ey * 1.2
    ax.add_patch(Circle(p, 0.06, fc=fs.ORANGE, ec=fs.BLACK, lw=0.6, zorder=6))
    ax.text(*(p + np.array([0.15, -0.2])), r'$dm$', fontsize=9.5)
    ax.plot(*zip(p, ey * 1.2), color=fs.GRAY, lw=0.7, ls=':')
    ax.plot(*zip(p, ex * 0.7), color=fs.GRAY, lw=0.7, ls=':')
    ax.plot(*zip((0, 0), p), color=fs.VEL, lw=1.0)
    ax.annotate(r'$\sqrt{x^2+y^2}$', xy=p * 0.55, xytext=(1.25, -0.85), fontsize=8.5, color=fs.VEL,
                arrowprops=dict(arrowstyle='-', color=fs.VEL, lw=0.6))
    ax.text(-2.1, 1.75, r'$I_z=I_x+I_y$', fontsize=10)
    fs.save(fig, F, 'fig10_11')


# ---------------------------------------------------------------- 그림 10.12 여러 물체의 관성모멘트
def fig12():
    fig, axs = plt.subplots(2, 3, figsize=(5.4, 3.4))
    for ax in axs.flat:
        ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.55, 1.25)
    # 막대 중심
    ax = axs[0, 0]
    ax.add_patch(Rectangle((-1.0, -0.06), 2.0, 0.12, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    ax.plot([0, 0], [-0.7, 0.7], **AX)
    ax.text(0, -1.0, '막대(중심)', fontsize=8.5, ha='center'); ax.text(0, -1.4, r'$\frac{1}{12}ML^2$', fontsize=10, ha='center')
    ax = axs[0, 1]
    ax.add_patch(Rectangle((-1.0, -0.06), 2.0, 0.12, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    ax.plot([-1.0, -1.0], [-0.7, 0.7], **AX)
    ax.text(0, -1.0, '막대(끝)', fontsize=8.5, ha='center'); ax.text(0, -1.4, r'$\frac{1}{3}ML^2$', fontsize=10, ha='center')
    ax = axs[0, 2]
    ax.add_patch(Ellipse((0, 0), 2.0, 0.6, fc='none', ec=fs.BLACK, lw=2.2))
    ax.plot([0, 0], [-0.8, 0.9], **AX)
    ax.text(0, -1.0, '얇은 고리', fontsize=8.5, ha='center'); ax.text(0, -1.4, r'$MR^2$', fontsize=10, ha='center')
    ax = axs[1, 0]
    ax.add_patch(Rectangle((-1.0, -0.12), 2.0, 0.24, fc=fs.LIGHT, ec='none'))
    ax.add_patch(Ellipse((0, -0.12), 2.0, 0.6, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((-1.0, -0.12), 2.0, 0.24, fc=fs.LIGHT, ec='none'))
    ax.add_patch(Ellipse((0, 0.12), 2.0, 0.6, fc='#dde6f0', ec=fs.BLACK, lw=1.0))
    ax.plot([-1, -1], [-0.12, 0.12], color=fs.BLACK, lw=1.0); ax.plot([1, 1], [-0.12, 0.12], color=fs.BLACK, lw=1.0)
    ax.plot([0, 0], [-0.8, 0.95], **AX)
    ax.text(0, -1.0, '원판·원기둥', fontsize=8.5, ha='center'); ax.text(0, -1.4, r'$\frac{1}{2}MR^2$', fontsize=10, ha='center')
    ax = axs[1, 1]
    ax.add_patch(Circle((0, 0), 0.8, fc='none', ec=fs.BLACK, lw=2.0))
    fs.ellipse3d(ax, (0, 0), 0.8, 0.22, color=fs.GRAY, lw=0.8)
    ax.plot([0, 0], [-1.0, 1.05], **AX)
    ax.text(0, -1.15, '얇은 구 껍질', fontsize=8.5, ha='center'); ax.text(0, -1.5, r'$\frac{2}{3}MR^2$', fontsize=10, ha='center')
    ax = axs[1, 2]
    ax.add_patch(Circle((0, 0), 0.8, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2))
    ax.add_patch(Circle((-0.25, 0.25), 0.3, fc='white', ec='none', alpha=0.5))
    ax.plot([0, 0], [-1.0, 1.05], **AX)
    ax.text(0, -1.15, '속이 찬 공', fontsize=8.5, ha='center'); ax.text(0, -1.5, r'$\frac{2}{5}MR^2$', fontsize=10, ha='center')
    fig.subplots_adjust(wspace=0.05, hspace=0.05)
    fs.save(fig, F, 'fig10_12')


# ---------------------------------------------------------------- 그림 10.13 예제 10.6 막대와 공
def fig13():
    s = 3.0     # m → 그림 단위
    fig, ax = fs.canvas(3.0, 3.2, xlim=(-1.4, 1.6), ylim=(-3.35, 0.4))
    fs.dot_out(ax, (0, 0), r=0.1)
    ax.text(0.2, 0.15, '회전축(⊙)', fontsize=8.5, color=fs.GRAY, ha='left')
    ax.add_patch(Rectangle((-0.05, -0.8 * s), 0.1, 0.8 * s - 0.1, fc=fs.LIGHT, ec=fs.BLACK, lw=1.0))
    ax.add_patch(Circle((0, -0.9 * s), 0.1 * s, fc='#cfd8e3', ec=fs.BLACK, lw=1.1))
    fs.dot(ax, (0, -0.9 * s), r=0.035)
    dimline(ax, (-0.55, 0), (-0.55, -0.8 * s), r'$0.80\ \mathrm{m}$', off=(-0.38, 0), fontsize=9)
    ax.plot([-0.65, -0.05], [-0.8 * s, -0.8 * s], color=fs.GRAY, lw=0.5, ls=':')
    dimline(ax, (0.6, 0), (0.6, -0.9 * s), r'$0.90\ \mathrm{m}$', off=(0.38, 0), fontsize=9)
    ax.plot([0, 0.7], [-0.9 * s, -0.9 * s], color=fs.GRAY, lw=0.5, ls=':')
    ax.plot([0, 0.7], [0, 0], color=fs.GRAY, lw=0.5, ls=':')
    ax.plot([0, 0.3 * np.cos(-0.5) * 1], [-0.9 * s, -0.9 * s + 0.3 * np.sin(-0.5)], color=fs.BLACK, lw=0.8)
    ax.text(0.05, -0.9 * s - 0.42, r'$0.10\ \mathrm{m}$', fontsize=8, ha='left')
    ax.text(0.12, -0.35 * s, r'막대 $1.0\ \mathrm{kg}$', fontsize=8.5, ha='left')
    ax.text(-0.38, -0.9 * s - 0.15, r'공 $2.0\ \mathrm{kg}$', fontsize=8.5, ha='right')
    fs.save(fig, F, 'fig10_13')


# ---------------------------------------------------------------- 그림 10.14 연습문제 4 정사각형의 네 질량
def fig14():
    a = 2.0
    fig, ax = fs.canvas(3.2, 2.7, xlim=(-1.7, 2.3), ylim=(-1.6, 1.75))
    c = [(-a / 2, -a / 2), (a / 2, -a / 2), (a / 2, a / 2), (-a / 2, a / 2)]
    ax.add_patch(Polygon(c, closed=True, fc='none', ec=fs.GRAY, lw=1.6))
    ax.plot([-1.6, 1.6], [-a / 2, -a / 2], color=fs.ACC, lw=1.0, ls='-.')
    ax.plot([-1.45, 1.45], [-1.45, 1.45], color=fs.FORCE, lw=1.0, ls='-.')
    for p in c:
        ax.add_patch(Circle(p, 0.14, fc=fs.VEL, ec=fs.BLACK, lw=0.8, zorder=5))
    fs.dot_out(ax, (0, 0), r=0.09)
    ax.text(0.15, -0.25, '(가)', fontsize=9)
    ax.text(1.65, -a / 2, '(나)', fontsize=9, color=fs.ACC, va='center')
    ax.text(1.5, 1.5, '(다)', fontsize=9, color=fs.FORCE, va='center')
    dimline(ax, (-a / 2, a / 2 + 0.3), (a / 2, a / 2 + 0.3), r'$0.40\ \mathrm{m}$', off=(0, 0.17), fontsize=9)
    fs.save(fig, F, 'fig10_14')


for f_ in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
    f_()
