"""부록 B 수학 공식 — 그림 생성 스크립트.

    python3 figures/appB/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse

S = __file__

# 비스듬한 투영(3차원 → 종이): x는 왼쪽 아래(앞쪽), y는 오른쪽, z는 위
EX = np.array([-0.55, -0.42]); EY = np.array([1.0, 0.0]); EZ = np.array([0.0, 1.0])


def P(x, y, z):
    return x * EX + y * EY + z * EZ


def P3(v):
    return P(*v)


def axes3d(ax, L=(2.0, 2.3, 2.1)):
    o = P(0, 0, 0)
    for v, lab, off in ((P(L[0], 0, 0), '$x$', (-0.12, -0.05)), (P(0, L[1], 0), '$y$', (0.12, 0.0)),
                        (P(0, 0, L[2]), '$z$', (0.0, 0.12))):
        fs.arrow(ax, o, v, color=fs.GRAY, lw=0.9, ms=9, zorder=1)
        ax.text(v[0] + off[0], v[1] + off[1], lab, fontsize=11, color=fs.GRAY, ha='center', va='center')


def curve3d(ax, pts, **kw):
    q = np.array([P3(p) for p in pts])
    ax.plot(q[:, 0], q[:, 1], **kw)


# ---------- 그림 B.1 단위원 ----------
def figB01():
    fig, ax = fs.canvas(3.0, 2.8, xlim=(-1.35, 1.75), ylim=(-1.3, 1.55))
    fs.arrow(ax, (-1.3, 0), (1.7, 0), color=fs.GRAY, lw=0.9, ms=9)
    fs.arrow(ax, (0, -1.25), (0, 1.5), color=fs.GRAY, lw=0.9, ms=9)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(th), np.sin(th), color=fs.BLACK, lw=1.0)
    t = np.radians(38)
    p = np.array([np.cos(t), np.sin(t)])
    ax.plot([0, 1], [0, np.tan(t)], color=fs.BLACK, lw=1.0)
    ax.plot([1, 1], [-0.3, 1.2], color=fs.GRAY, lw=0.7, ls='--')
    ax.plot([p[0], p[0]], [0, p[1]], color=fs.FORCE, lw=2.0)
    ax.plot([0, p[0]], [0, 0], color=fs.VEL, lw=2.6)
    ax.plot([1, 1], [0, np.tan(t)], color=fs.ACC, lw=2.0)
    fs.dot(ax, p, r=0.035)
    ax.text(p[0] - 0.05, p[1] + 0.06, r'$(\cos\theta, \sin\theta)$', fontsize=9, ha='right', va='bottom')
    ax.text(p[0] / 2, -0.06, r'$\cos\theta$', color=fs.VEL, fontsize=10, ha='center', va='top')
    ax.text(p[0] - 0.04, p[1] * 0.42, r'$\sin\theta$', color=fs.FORCE, fontsize=9.5, ha='right', va='center')
    ax.text(1.06, np.tan(t) / 2, r'$\tan\theta$', color=fs.ACC, fontsize=10, ha='left', va='center')
    fs.angle_arc(ax, (0, 0), 0.18, 0, 38, r'$\theta$', tr=0.29, fontsize=9.5)
    ax.text(0.33, 0.4, '$1$', fontsize=10, ha='center', va='center')
    ax.text(-0.75, -0.95, '반지름 1', fontsize=8.5, color=fs.GRAY, ha='center')
    fs.save(fig, S, 'figB_01')


# ---------- 그림 B.2 삼각형의 변과 각 ----------
def figB02():
    fig, ax = fs.canvas(3.0, 1.9, xlim=(-0.4, 4.6), ylim=(-0.45, 2.6))
    A = np.array([0.0, 0.0]); B = np.array([4.2, 0.0]); C = np.array([1.4, 2.2])
    ax.add_patch(Polygon([A, B, C], closed=True, fc=fs.LIGHT, ec=fs.BLACK, lw=1.2))
    def ang(p, q, r):
        a1 = np.degrees(np.arctan2(*(q - p)[::-1])); a2 = np.degrees(np.arctan2(*(r - p)[::-1]))
        return a1, a2
    for p, q, r, lab in ((A, B, C, r'$\alpha$'), (B, C, A, r'$\beta$'), (C, A, B, r'$\gamma$')):
        a1, a2 = ang(p, q, r)
        lo, hi = sorted((a1 % 360, a2 % 360))
        if hi - lo > 180:
            lo, hi = hi, lo + 360
        fs.angle_arc(ax, p, 0.38, lo, hi, lab, fontsize=10, tr=0.62)
    ax.text(*(0.5 * (B + C) + np.array([0.18, 0.12])), '$a$', fontsize=12, ha='center', va='center')
    ax.text(*(0.5 * (A + C) + np.array([-0.2, 0.1])), '$b$', fontsize=12, ha='center', va='center')
    ax.text(*(0.5 * (A + B) + np.array([0, -0.2])), '$c$', fontsize=12, ha='center', va='center')
    fs.save(fig, S, 'figB_02')


# ---------- 그림 B.3 작은 각 근사 ----------
def figB03():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.3, 2.3))
    deg = np.linspace(0.01, 60, 400); x = np.radians(deg)
    a1.plot(deg, np.tan(x), color=fs.ACC, lw=1.5, label=r'$\tan\theta$')
    a1.plot(deg, x, color=fs.BLACK, lw=1.5, ls='--', label=r'$\theta$ (rad)')
    a1.plot(deg, np.sin(x), color=fs.FORCE, lw=1.5, label=r'$\sin\theta$')
    a1.set_xlim(0, 60); a1.set_ylim(0, 1.8)
    a1.set_xlabel(r'$\theta$ (도)')
    a1.legend(fontsize=8, frameon=False, loc='upper left')
    a1.set_title('(가) 세 함수의 비교', fontsize=9)
    e_sin = (x - np.sin(x)) / np.sin(x) * 100
    e_tan = (np.tan(x) - x) / np.tan(x) * 100
    e_cos = ((1 - x ** 2 / 2) - np.cos(x)) / np.cos(x) * 100
    a2.plot(deg, e_sin, color=fs.FORCE, lw=1.5, label=r'$\sin\theta \approx \theta$')
    a2.plot(deg, e_tan, color=fs.ACC, lw=1.5, label=r'$\tan\theta \approx \theta$')
    a2.plot(deg, abs(e_cos), color=fs.VEL, lw=1.5, label=r'$\cos\theta \approx 1 - \theta^2/2$')
    a2.axhline(1, color=fs.GRAY, lw=0.8, ls=':')
    a2.set_xlim(0, 40); a2.set_ylim(0, 6)
    a2.set_xlabel(r'$\theta$ (도)'); a2.set_ylabel('상대 오차 (%)')
    a2.legend(fontsize=7.5, frameon=False, loc='upper left')
    a2.set_title('(나) 근사의 상대 오차', fontsize=9)
    for a in (a1, a2):
        a.grid(True, lw=0.4, color='#d0d0d0')
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    fig.tight_layout(w_pad=1.5)
    fs.save(fig, S, 'figB_03')


# ---------- 그림 B.4 평면 극좌표 ----------
def figB04():
    fig, ax = fs.canvas(3.3, 2.9, xlim=(-0.3, 3.4), ylim=(-0.35, 3.0))
    fs.arrow(ax, (-0.2, 0), (3.3, 0), color=fs.GRAY, lw=0.9, ms=9)
    fs.arrow(ax, (0, -0.2), (0, 2.9), color=fs.GRAY, lw=0.9, ms=9)
    ax.text(3.3, -0.08, '$x$', fontsize=11, color=fs.GRAY, ha='right', va='top')
    ax.text(-0.08, 2.9, '$y$', fontsize=11, color=fs.GRAY, ha='right', va='top')
    r, t, dr, dt = 2.2, np.radians(35), 0.35, np.radians(11)
    # 미소 넓이 요소
    tt = np.linspace(t, t + dt, 30)
    pts = np.concatenate([np.c_[r * np.cos(tt), r * np.sin(tt)], np.c_[(r + dr) * np.cos(tt[::-1]), (r + dr) * np.sin(tt[::-1])]])
    ax.add_patch(Polygon(pts, closed=True, fc=fs.SURF, ec=fs.BLACK, lw=0.8, alpha=0.9))
    p = np.array([r * np.cos(t), r * np.sin(t)])
    ax.plot([0, p[0]], [0, p[1]], color=fs.BLACK, lw=1.2)
    ax.plot([0, (r + dr + 0.2) * np.cos(t + dt)], [0, (r + dr + 0.2) * np.sin(t + dt)], color=fs.GRAY, lw=0.6, ls='--')
    fs.dot(ax, p, r=0.04)
    ax.text(p[0] / 2 + 0.05, p[1] / 2 - 0.12, '$r$', fontsize=11, ha='left', va='top')
    fs.angle_arc(ax, (0, 0), 0.5, 0, 35, r'$\theta$', tr=0.7, fontsize=10)
    fs.angle_arc(ax, (0, 0), 1.3, 35, 46, r'$d\theta$', tr=1.55, fontsize=9)
    ur = np.array([np.cos(t), np.sin(t)]); ut = np.array([-np.sin(t), np.cos(t)])
    fs.arrow(ax, p, p + 0.6 * ur, color=fs.FORCE, lw=1.5, ms=10)
    fs.arrow(ax, p, p + 0.6 * ut, color=fs.FORCE, lw=1.5, ms=10)
    q = p + 0.6 * ur; ax.text(q[0] + 0.05, q[1] - 0.05, r'$\hat{r}$', color=fs.FORCE, fontsize=11, ha='left', va='top')
    q = p + 0.6 * ut; ax.text(q[0] - 0.05, q[1] + 0.02, r'$\hat{\theta}$', color=fs.FORCE, fontsize=11, ha='right', va='bottom')
    m = (r + dr / 2) * np.array([np.cos(t + dt / 2), np.sin(t + dt / 2)])
    ax.annotate(r'$dA = r\,dr\,d\theta$', xy=m, xytext=(2.1, 2.55), fontsize=9.5, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', lw=0.6))
    fs.save(fig, S, 'figB_04')


def unit_vectors(ax, p3, vecs, L=0.55):
    for v, lab, off in vecs:
        a = P3(p3); b = P3(np.asarray(p3) + L * np.asarray(v))
        fs.arrow(ax, a, b, color=fs.FORCE, lw=1.5, ms=10, zorder=6)
        ax.text(b[0] + off[0], b[1] + off[1], lab, color=fs.FORCE, fontsize=11, ha='center', va='center')


# ---------- 그림 B.5 원통 좌표 ----------
def figB05():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-1.3, 2.6), ylim=(-1.1, 2.6))
    axes3d(ax)
    r, ph, z = 1.4, np.radians(62), 1.4
    Q = np.array([r * np.cos(ph), r * np.sin(ph), 0]); Pp = Q + np.array([0, 0, z])
    # 반지름 r인 원통 일부(점의 양옆 호)
    th = np.linspace(ph - 0.5, ph + 0.5, 60)
    for zz in (0, z):
        curve3d(ax, np.c_[r * np.cos(th), r * np.sin(th), np.full_like(th, zz)], color=fs.GRAY, lw=0.7, ls=':')
    curve3d(ax, [(0, 0, 0), Q], color=fs.BLACK, lw=1.2)
    curve3d(ax, [Q, Pp], color=fs.BLACK, lw=1.0, ls='--')
    curve3d(ax, [(0, 0, z), Pp], color=fs.GRAY, lw=0.7, ls='--')
    a = np.linspace(0, ph, 30)
    curve3d(ax, np.c_[0.5 * np.cos(a), 0.5 * np.sin(a), 0 * a], color=fs.BLACK, lw=0.9)
    m = P(0.72 * np.cos(ph / 2), 0.72 * np.sin(ph / 2), 0)
    ax.text(m[0], m[1], r'$\phi$', fontsize=11, ha='center', va='center')
    m = P3(Q / 2); ax.text(m[0] + 0.02, m[1] - 0.1, '$r$', fontsize=11, ha='center', va='top')
    m = P3(Q + np.array([0, 0, z / 2])); ax.text(m[0] + 0.08, m[1], '$z$', fontsize=11, ha='left', va='center')
    fs.dot(ax, P3(Pp), r=0.045)
    ax.text(*(P3(Pp) + np.array([-0.2, 0.32])), '$(r, \\phi, z)$', fontsize=9.5, ha='right', va='bottom')
    unit_vectors(ax, Pp, [((np.cos(ph), np.sin(ph), 0), r'$\hat{r}$', (0.12, -0.1)),
                          ((-np.sin(ph), np.cos(ph), 0), r'$\hat{\phi}$', (0.15, 0.05)),
                          ((0, 0, 1), r'$\hat{z}$', (0.12, 0.1))])
    fs.save(fig, S, 'figB_05')


# ---------- 그림 B.6 구면 좌표 ----------
def figB06():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-1.3, 2.6), ylim=(-1.1, 2.6))
    axes3d(ax)
    R, th, ph = 1.9, np.radians(42), np.radians(62)
    Pp = R * np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    Q = np.array([Pp[0], Pp[1], 0])
    curve3d(ax, [(0, 0, 0), Pp], color=fs.BLACK, lw=1.3)
    curve3d(ax, [(0, 0, 0), Q], color=fs.GRAY, lw=0.8, ls='--')
    curve3d(ax, [Q, Pp], color=fs.GRAY, lw=0.8, ls='--')
    a = np.linspace(0, th, 30)
    rr = 0.6
    curve3d(ax, np.c_[rr * np.sin(a) * np.cos(ph), rr * np.sin(a) * np.sin(ph), rr * np.cos(a)], color=fs.BLACK, lw=0.9)
    m = P(0.85 * np.sin(th / 2) * np.cos(ph), 0.85 * np.sin(th / 2) * np.sin(ph), 0.85 * np.cos(th / 2))
    ax.text(m[0], m[1], r'$\theta$', fontsize=11, ha='center', va='center')
    a = np.linspace(0, ph, 30)
    curve3d(ax, np.c_[0.5 * np.cos(a), 0.5 * np.sin(a), 0 * a], color=fs.BLACK, lw=0.9)
    m = P(0.72 * np.cos(ph / 2), 0.72 * np.sin(ph / 2), 0)
    ax.text(m[0], m[1], r'$\phi$', fontsize=11, ha='center', va='center')
    m = P3(Pp * 0.55); ax.text(m[0] + 0.1, m[1], '$r$', fontsize=11, ha='left', va='center')
    fs.dot(ax, P3(Pp), r=0.045)
    ax.text(*(P3(Pp) + np.array([-0.12, 0.1])), r'$(r, \theta, \phi)$', fontsize=9.5, ha='right', va='bottom')
    rh = Pp / R
    thh = np.array([np.cos(th) * np.cos(ph), np.cos(th) * np.sin(ph), -np.sin(th)])
    phh = np.array([-np.sin(ph), np.cos(ph), 0])
    unit_vectors(ax, Pp, [(rh, r'$\hat{r}$', (0.1, 0.12)), (thh, r'$\hat{\theta}$', (0.14, -0.08)),
                          (phh, r'$\hat{\phi}$', (0.15, 0.05))])
    fs.save(fig, S, 'figB_06')


# ---------- 그림 B.7 평행축 정리 ----------
def figB07():
    fig, ax = fs.canvas(3.2, 2.4, xlim=(-1.9, 2.4), ylim=(-1.4, 1.9))
    # 비스듬히 본 납작한 물체(원판)
    ax.add_patch(Ellipse((0, -0.12), 2.8, 0.9, fc='#cfd8e3', ec=fs.BLACK, lw=1.0, zorder=2))
    ax.add_patch(Ellipse((0, 0), 2.8, 0.9, fc=fs.LIGHT, ec=fs.BLACK, lw=1.1, zorder=3))
    ax.add_patch(Polygon([(-1.4, 0), (-1.4, -0.12), (1.4, -0.12), (1.4, 0)], closed=True, fc='#cfd8e3', ec='none', zorder=2))
    d = 1.15
    for x0, lab, c in ((0, '질량중심 축', fs.BLACK), (d, '평행한 축', fs.FORCE)):
        ax.plot([x0, x0], [-1.15, 1.45], color=c, lw=1.1, ls='-.', zorder=4)
        ax.text(x0, 1.55, lab, fontsize=8.5, color=c, ha='center', va='bottom')
    fs.dot(ax, (0, 0), r=0.05, color=fs.BLACK)
    ax.text(-0.1, 0.07, 'cm', fontsize=8.5, ha='right', va='bottom', zorder=6)
    fs.dim(ax, (0, -1.0), (d, -1.0), '$d$', off=0.0, color=fs.BLACK, fontsize=11)
    ax.text(-1.85, -1.3, r'$I = I_{\mathrm{cm}} + Md^2$', fontsize=10, ha='left', va='center')
    fs.save(fig, S, 'figB_07')


if __name__ == '__main__':
    for f in (figB01, figB02, figB03, figB04, figB05, figB06, figB07):
        f()
