"""0장 대학 물리를 공부하는 법 — 그림 생성 스크립트.

    python3 figures/ch00/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

S = __file__


# ---------- 그림 0.1 문제 풀이의 4단계 ----------
def fig01():
    fig, ax = fs.canvas(5.4, 1.9, xlim=(0, 10.8), ylim=(-0.75, 2.85))
    steps = [('파악', 'Identify', '무엇을 구하나?\n어떤 원리?'),
             ('설정', 'Set up', '그림·좌표축\n자유물체도'),
             ('실행', 'Execute', '기호로 풀고\n마지막에 대입'),
             ('검증', 'Evaluate', '차원·극한·크기\n검사')]
    w, h, gap = 2.2, 1.95, 0.6
    xs = [0.1 + i * (w + gap) for i in range(4)]
    for i, (x, (k, e, d)) in enumerate(zip(xs, steps)):
        ax.add_patch(FancyBboxPatch((x, 0.45), w, h, boxstyle='round,pad=0.02,rounding_size=0.15',
                                    fc=fs.LIGHT, ec=fs.VEL, lw=1.2))
        ax.text(x + w / 2, 0.45 + h - 0.3, f'{i + 1}. {k}', fontsize=9.5, ha='center', va='center',
                fontweight='bold', color=fs.VEL)
        ax.text(x + w / 2, 0.45 + h - 0.68, e, fontsize=8, ha='center', va='center', color=fs.VEL)
        ax.text(x + w / 2, 0.45 + 0.5, d, fontsize=8.5, ha='center', va='center', linespacing=1.3)
        if i < 3:
            fs.arrow(ax, (x + w + 0.05, 0.45 + h / 2), (x + w + gap - 0.05, 0.45 + h / 2), color=fs.BLACK, lw=1.3, ms=10)
    # 되돌아가는 화살표
    x0 = xs[3] + w / 2; x1 = xs[1] + w / 2
    ax.add_patch(FancyArrowPatch((x0, 0.4), (x1, 0.4), connectionstyle='bar,fraction=-0.12',
                                 arrowstyle='-|>', mutation_scale=10, color=fs.FORCE, lw=1.1))
    ax.text((x0 + x1) / 2, -0.55, '검사에서 어긋나면 설정으로 돌아간다', fontsize=8.5, color=fs.FORCE,
            ha='center', va='center')
    fs.save(fig, S, 'fig00_01')


# ---------- 그림 0.2 예제 0.1 빗면 ----------
def fig02():
    fig, ax = fs.canvas(4.3, 2.6, xlim=(-0.5, 5.7), ylim=(-0.45, 3.0))
    th_deg = 30; th = np.radians(th_deg)
    Ls = 5.0
    fs.incline(ax, origin=(0, 0), length=Ls, angle=th_deg, angle_label=r'$\theta$')
    u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    bw, bh = 0.7, 0.45
    s1, s0 = 4.1, 1.3
    c1 = s1 * u + n * bh / 2; c0 = s0 * u + n * bh / 2
    fs.block(ax, c1, w=bw, h=bh, angle=th_deg)
    fs.block(ax, c0, w=bw, h=bh, angle=th_deg, fc='none', ec=fs.GRAY)
    # 미끄러진 거리 L
    fs.dim(ax, s0 * u, s1 * u, '$L$', off=-0.3, color=fs.BLACK, fontsize=11)
    # 높이 차 L sinθ
    p_top = s1 * u; p_bot = s0 * u
    xa = Ls * np.cos(th) + 0.3
    ax.plot([p_bot[0], xa + 0.1], [p_bot[1], p_bot[1]], color=fs.GRAY, lw=0.6, ls=':')
    ax.plot([p_top[0], xa + 0.1], [p_top[1], p_top[1]], color=fs.GRAY, lw=0.6, ls=':')
    ax.add_patch(FancyArrowPatch((xa, p_bot[1]), (xa, p_top[1]), arrowstyle='<|-|>', mutation_scale=8, color=fs.GRAY, lw=0.8))
    ax.text(xa + 0.08, (p_bot[1] + p_top[1]) / 2, r'$L\sin\theta$', fontsize=10, color=fs.GRAY, ha='left', va='center')
    # 자유물체도(위쪽 물체)
    fs.arrow(ax, c1, c1 + np.array([0, -1.0]), color=fs.FORCE, lw=1.6)
    ax.text(c1[0] + 0.08, c1[1] - 0.95, r'$m\vec{g}$', color=fs.FORCE, fontsize=10, ha='left', va='center')
    fs.arrow(ax, c1, c1 + n * 0.95, color=fs.FORCE, lw=1.6)
    q = c1 + n * 0.95
    ax.text(q[0] - 0.05, q[1] + 0.05, r'$\vec{F}_N$', color=fs.FORCE, fontsize=10, ha='right', va='bottom')
    ax.text(c1[0] + 0.05, c1[1] + 0.55, '정지에서 출발', fontsize=8.5, ha='left', va='bottom')
    # 아래쪽 위치의 속도
    fs.arrow(ax, c0 + n * 0.45, c0 + n * 0.45 - u * 0.9, color=fs.VEL, lw=1.6)
    r = c0 + n * 0.45 - u * 0.9
    ax.text(r[0] - 0.05, r[1] + 0.12, r'$v = ?$', color=fs.VEL, fontsize=10, ha='right', va='bottom')
    fs.ground(ax, -0.4, Ls * np.cos(th) + 0.3, 0.0)
    fs.save(fig, S, 'fig00_02')


if __name__ == '__main__':
    for f in (fig01, fig02):
        f()
