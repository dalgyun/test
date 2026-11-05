"""5장 뉴턴의 운동 법칙 그림. 실행: python3 figures/ch05/make_figs.py"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

g = 9.8


def style(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def force(ax, c, d, label=None, color=fs.FORCE, start=0.0, lw=1.8, fontsize=10, loff=(0, 0), ha='center', ms=11):
    """점 c에서 방향 d로 힘 화살표. start>0이면 c에서 그만큼 떨어진 곳(상자 가장자리)에서 시작."""
    c = np.asarray(c, float); d = np.asarray(d, float)
    L = np.hypot(*d)
    if L < 1e-9:
        return
    u = d / L
    p = c + u * start
    fs.arrow(ax, tuple(p), tuple(p + d), color=color, lw=lw, ms=ms)
    if label:
        q = p + d + u * 0.22 + np.array(loff)
        ax.text(q[0], q[1], label, color=color, fontsize=fontsize, ha=ha, va='center')


def push(ax, face, d, label=None, color=fs.FORCE, lw=1.8, fontsize=10, loff=(0, 0.25)):
    """미는 힘: 화살표 끝이 물체 면(face)에 닿도록 그린다. d는 힘의 방향·길이."""
    face = np.asarray(face, float); d = np.asarray(d, float)
    p = face - d
    fs.arrow(ax, tuple(p), tuple(face), color=color, lw=lw, ms=11)
    if label:
        m = (p + face) / 2 + np.array(loff)
        ax.text(m[0], m[1], label, color=color, fontsize=fontsize, ha='center', va='center')


def rope(ax, p, q, lw=1.1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=fs.BLACK, lw=lw, zorder=2)


# ---------- 그림 5.1 갈릴레이의 빗면 사고 실험 ----------
def fig01():
    fig, ax = fs.canvas(5.0, 1.8, xlim=(-0.2, 11.2), ylim=(-0.5, 2.5))
    h = 1.8
    ax.plot([0, 2.0], [h, 0], color=fs.BLACK, lw=1.3)
    for xe, ls, col in ((4.0, '-', fs.BLACK), (6.0, '-', fs.GRAY), (9.0, '-', '#aaaaaa')):
        ax.plot([2.0, xe], [0, h], color=col, lw=1.1, ls=ls)
        fs.dot(ax, (xe, h), r=0.09, color=col)
    ax.plot([2.0, 11.0], [0, 0], color=fs.BLACK, lw=1.0)
    fs.arrow(ax, (9.6, 0.25), (11.0, 0.25), color=fs.VEL, lw=1.2, ms=9, ls='--')
    ax.text(10.3, 0.45, '영원히?', fontsize=8, color=fs.VEL, ha='center')
    ax.plot([0, 9.5], [h, h], color=fs.GRAY, lw=0.6, ls=':')
    ax.text(7.2, h + 0.18, '처음과 같은 높이', fontsize=8, color=fs.GRAY, ha='center')
    ax.add_patch(Circle((0.2, h + 0.0 + 0.12), 0.12, fc=fs.VEL, ec=fs.BLACK, lw=0.6, zorder=5))
    ax.text(0.0, h + 0.45, '공을 놓는다', fontsize=8)
    ax.text(2.0, -0.35, '빗면을 점점 눕힌다 →', fontsize=8, ha='left')
    fs.save(fig, __file__, 'fig05_01')


# ---------- 그림 5.2 예제 5.1 ----------
def fig02():
    fig, ax = fs.canvas(3.6, 2.9, xlim=(-2.6, 3.0), ylim=(-1.2, 2.4))
    s = 0.2
    fs.arrow(ax, (-2.4, 0), (2.8, 0), lw=0.7, ms=8, color=fs.GRAY)
    fs.arrow(ax, (0, -1.1), (0, 2.25), lw=0.7, ms=8, color=fs.GRAY)
    ax.text(2.85, -0.15, '동($+x$)', fontsize=8, color=fs.GRAY, ha='right', va='top')
    ax.text(0.08, 2.25, '북($+y$)', fontsize=8, color=fs.GRAY, va='top')
    F1 = np.array([10, 0]); F2 = 8 * np.array([np.cos(np.radians(120)), np.sin(np.radians(120))]); F3 = np.array([0, -3])
    Fn = F1 + F2 + F3
    force(ax, (0, 0), s * F1, r'$\vec F_1$ (10 N)', loff=(0.1, 0.2))
    force(ax, (0, 0), s * F2, r'$\vec F_2$ (8.0 N)', loff=(-0.1, 0.05))
    force(ax, (0, 0), s * F3, r'$\vec F_3$ (3.0 N)', loff=(0.6, 0.05))
    fs.arrow(ax, (0, 0), tuple(s * Fn), color=fs.FORCE, lw=2.4, ms=13)
    ax.text(s * Fn[0] + 0.1, s * Fn[1] + 0.15, r'$\vec F_{\mathrm{net}}$', color=fs.FORCE, fontsize=11)
    fs.vec(ax, (0, 0), 0.32 * np.array([3.0, 1.96]), color=fs.ACC, lw=2.2, ms=10)
    ax.text(0.85, 0.2, r'$\vec a$', color=fs.ACC, fontsize=10)
    fs.angle_arc(ax, (0, 0), 0.55, 120, 180, r'$60^\circ$', fontsize=8, tr=0.8)
    fs.angle_arc(ax, (0, 0), 1.6, 0, np.degrees(np.arctan2(Fn[1], Fn[0])), r'$33^\circ$', fontsize=8, tr=1.85)
    fs.dot(ax, (0, 0), r=0.07)
    fs.save(fig, __file__, 'fig05_02')


# ---------- 그림 5.3 말과 수레 ----------
def fig03():
    fig, ax = fs.canvas(5.2, 2.0, xlim=(-0.3, 11.6), ylim=(-0.75, 3.0))
    fs.ground(ax, -0.2, 11.4, 0, depth=0.18, n=60)
    # 수레(왼쪽)와 말(오른쪽), 실제 배치보다 띄워 그린다
    fs.block(ax, (2.2, 0.55), 1.8, 0.9, text='수레', fontsize=10)
    fs.block(ax, (8.0, 0.55), 1.6, 0.9, text='말', fontsize=10)
    force(ax, (3.1, 0.75), (1.7, 0), None)
    ax.text(3.9, 1.25, '말이 수레를\n끄는 힘', color=fs.FORCE, fontsize=8, ha='center')
    force(ax, (1.3, 0.25), (-0.7, 0), None, lw=1.5)
    ax.text(0.95, -0.45, '땅의 마찰력', color=fs.FORCE, fontsize=8, ha='center')
    force(ax, (7.2, 0.75), (-1.7, 0), None)
    ax.text(6.4, 1.25, '수레가 말을\n끄는 힘', color=fs.FORCE, fontsize=8, ha='center')
    force(ax, (8.8, 0.22), (1.6, 0), None, lw=1.5)
    ax.text(9.6, -0.45, '땅이 발굽을 미는 힘', color=fs.FORCE, fontsize=8, ha='center')
    ax.annotate('', xy=(4.3, 2.0), xytext=(6.0, 2.0),
                arrowprops=dict(arrowstyle='<->', color=fs.GRAY, lw=0.8, ls='--'))
    ax.text(5.15, 2.15, '작용·반작용 쌍(크기 같음)', fontsize=8, color=fs.GRAY, ha='center', va='bottom')
    ax.text(2.2, 2.75, '수레의 자유물체도', fontsize=8.5, ha='center')
    ax.text(8.0, 2.75, '말의 자유물체도', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig05_03')


# ---------- 그림 5.4 책·책상·지구 ----------
def fig04():
    fig, ax = fs.canvas(4.6, 2.8, xlim=(-0.2, 8.6), ylim=(-1.5, 3.8))
    # 책상
    ax.add_patch(Rectangle((0.5, 1.0), 4.0, 0.25, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    for x in (0.8, 4.2):
        ax.add_patch(Rectangle((x - 0.1, 0.0), 0.2, 1.0, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    fs.block(ax, (2.5, 1.55), 1.4, 0.6, text='책', fontsize=9, fc='#cfe0f3')
    # 지구
    ax.add_patch(Rectangle((-0.2, -1.4), 5.2, 1.4, fc='#e8e2d0', ec='none', zorder=0))
    ax.plot([-0.2, 5.0], [0, 0], color=fs.BLACK, lw=1.0)
    ax.text(0.3, -1.1, '지구', fontsize=9)
    c1, c2 = fs.FORCE, fs.ORANGE
    # 쌍 1: 수직항력과 책이 책상을 누르는 힘 (접촉면)
    force(ax, (2.05, 1.85), (0, 1.1), r'$\vec N$', color=c1, loff=(0, 0.05))
    force(ax, (2.05, 1.25), (0, -0.85), None, color=c1, lw=1.5)
    # 쌍 2: 중력
    force(ax, (2.95, 1.55), (0, -1.0), r'$m\vec g$', color=c2, loff=(0.35, 0.3))
    force(ax, (2.95, -0.9), (0, 0.6), None, color=c2, lw=1.5)
    # 설명
    tx = 5.3
    ax.text(tx, 3.2, '쌍 1 (접촉력)', fontsize=8.5, color=c1, fontweight='bold')
    ax.text(tx, 2.75, '책상이 책을 미는 힘 $\\vec N$', fontsize=8, color=c1)
    ax.text(tx, 2.35, '책이 책상을 누르는 힘', fontsize=8, color=c1)
    ax.text(tx, 1.5, '쌍 2 (중력)', fontsize=8.5, color=c2, fontweight='bold')
    ax.text(tx, 1.05, '지구가 책을 당기는 힘 $m\\vec g$', fontsize=8, color=c2)
    ax.text(tx, 0.65, '책이 지구를 당기는 힘', fontsize=8, color=c2)
    ax.text(tx, -0.4, '책에 작용하는 힘: $\\vec N$, $m\\vec g$\n(서로 쌍이 아님)', fontsize=8)
    fs.save(fig, __file__, 'fig05_04')


# ---------- 그림 5.5 예제 5.2 엘리베이터 ----------
def fig05():
    fig, axs = plt.subplots(1, 3, figsize=(5.0, 2.6))
    m = 60.0
    cases = [('(가) 위로 2.0 m/s²', 2.0), ('(나) 아래로 2.0 m/s²', -2.0), ('(다) 아래로 $g$', -g)]
    s = 1.3 / 600
    for ax, (title, ay) in zip(axs, cases):
        ax.axis('off'); ax.set_aspect('equal'); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-2.1, 2.5)
        ax.add_patch(Rectangle((-1.15, -1.95), 2.3, 4.35, fc='none', ec=fs.GRAY, lw=1.0, ls='-'))
        fs.block(ax, (0, -0.2), 0.55, 0.7, text='사람', fontsize=7)
        N = m * (g + ay)
        force(ax, (-0.12, 0.15), (0, N * s), f'$N$ = {N:.0f} N' if N > 0 else None, fontsize=8, loff=(0, 0.05))
        force(ax, (0.12, -0.55), (0, -m * g * s), None)
        ax.text(0.2, -1.75, r'$mg$ = 588 N', color=fs.FORCE, fontsize=8, ha='left', va='center')
        if N <= 0:
            ax.text(-0.1, 0.75, '$N = 0$', color=fs.FORCE, fontsize=8, ha='center')
        fs.vec(ax, (0.85, -0.2 - np.sign(ay) * 0.45), (0, np.sign(ay) * 0.9), color=fs.ACC, lw=1.6, ms=9)
        ax.text(0.85, -0.2 + np.sign(ay) * 0.75, r'$\vec a$', color=fs.ACC, fontsize=10, ha='center')
        ax.set_title(title, fontsize=8)
    fig.tight_layout(w_pad=0.2)
    fs.save(fig, __file__, 'fig05_05')


# ---------- 그림 5.6 예제 5.3 질량이 있는 밧줄 ----------
def fig06():
    fig = plt.figure(figsize=(5.0, 3.0))
    ax = fig.add_axes([0.0, 0.52, 1.0, 0.46]); ax.axis('off'); ax.set_aspect('equal')
    ax.set_xlim(-0.3, 10.3); ax.set_ylim(-0.4, 2.0)
    fs.ground(ax, -0.2, 10.2, 0, depth=0.15, n=60)
    fs.block(ax, (0.8, 0.45), 1.2, 0.9, text='$M$', fontsize=10)
    ax.plot([1.4, 8.4], [0.45, 0.45], color='#8b6b3e', lw=3.0, solid_capstyle='butt')
    force(ax, (8.4, 0.45), (1.2, 0), r'$F$', loff=(0.15, 0))
    xc = 4.6
    ax.plot([xc, xc], [0.15, 0.8], color=fs.GRAY, lw=0.9, ls='--')
    ax.add_patch(Rectangle((-0.05, -0.05), xc + 0.05, 1.15, fc='none', ec=fs.VEL, lw=1.0, ls=':'))
    force(ax, (xc, 0.45), (0.9, 0), r'$T(x)$', loff=(0.35, 0.25), fontsize=9)
    fs.dim(ax, (1.4, 0.45), (xc, 0.45), r'$x$', off=0.35, fontsize=9)
    fs.dim(ax, (1.4, 0.45), (8.4, 0.45), r'$L$', off=0.9, fontsize=9)
    ax.text(0.0, 1.2, '고른 계', fontsize=8, color=fs.VEL, va='bottom')
    ax2 = fig.add_axes([0.2, 0.08, 0.6, 0.36]); style(ax2)
    xx = np.linspace(0, 1, 50)
    ax2.plot(xx, (2.0 + 0.5 * xx) * 4.0, color=fs.FORCE, lw=1.6)
    ax2.set_xlim(0, 1); ax2.set_ylim(7, 10.5)
    ax2.set_xlabel(r'$x/L$', labelpad=1); ax2.set_ylabel(r'$T$ (N)')
    ax2.set_xticks([0, 0.5, 1]); ax2.set_yticks([8, 9, 10])
    ax2.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig05_06')


# ---------- 그림 5.7 훅 법칙 ----------
def fig07():
    fig, ax = fs.canvas(4.2, 2.6, xlim=(-0.4, 7.6), ylim=(-0.4, 4.6))
    for row, (dx, lab) in enumerate(((-0.9, r'$x<0$: $F_x = -kx > 0$'), (0.0, r'$x=0$: $F_x = 0$'),
                                      (1.1, r'$x>0$: $F_x = -kx < 0$'))):
        y = 3.6 - row * 1.5
        fs.wall(ax, y - 0.45, y + 0.5, x=0, side='left')
        ax.plot([0, 7.2], [y - 0.4, y - 0.4], color=fs.BLACK, lw=0.8)
        xb = 3.3 + dx
        fs.spring(ax, (0, y), (xb - 0.35, y), coils=8, width=0.14)
        fs.block(ax, (xb, y - 0.1), 0.7, 0.6)
        if dx != 0:
            force(ax, (xb, y - 0.1), (-np.sign(dx) * 1.0, 0), r'$\vec F$', start=0.35, loff=(0.1, 0.35))
        ax.text(5.0 if dx <= 0 else 5.4, y + 0.35, lab, fontsize=8.5, ha='left')
    ax.plot([3.3, 3.3], [-0.2, 4.3], color=fs.GRAY, lw=0.7, ls='--')
    ax.text(3.3, -0.35, r'$x = 0$ (자연 길이)', fontsize=8, ha='center', color=fs.GRAY)
    fs.save(fig, __file__, 'fig05_07')


# ---------- 빗면 위 상자 그리기 ----------
def incline_block(ax, origin, length, th_deg, s_pos, bw=0.9, bh=0.6, label=None):
    th = np.radians(th_deg)
    u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    top = fs.incline(ax, origin=origin, length=length, angle=th_deg)
    c = np.array(origin) + u * s_pos + n * (bh / 2)
    fs.block(ax, tuple(c), bw, bh, angle=th_deg, text=label, fontsize=9)
    return c, u, n, top


# ---------- 그림 5.8 빗면 위 상자의 자유물체도 ----------
def fig08():
    fig, ax = fs.canvas(4.4, 2.9, xlim=(-0.2, 6.6), ylim=(-0.5, 4.1))
    th = 30
    c, u, n, top = incline_block(ax, (0, 0), 6.0, th, 3.4, bw=1.0, bh=0.7)
    sc = 1.7
    W = np.array([0, -sc])
    force(ax, c, W, r'$m\vec g$', loff=(0.25, 0.1))
    force(ax, c, n * sc * np.cos(np.radians(th)), r'$\vec N$', start=0.35, loff=(-0.1, 0.0))
    # 성분
    Wx = -u * sc * np.sin(np.radians(th)); Wy = -n * sc * np.cos(np.radians(th))
    fs.vec(ax, tuple(c), Wx, color=fs.FORCE, lw=1.0, ls='--', ms=8)
    fs.vec(ax, tuple(c), Wy, color=fs.FORCE, lw=1.0, ls='--', ms=8)
    ax.plot([c[0] + Wx[0], c[0] + W[0]], [c[1] + Wx[1], c[1] + W[1]], color=fs.FORCE, lw=0.5, ls=':')
    ax.plot([c[0] + Wy[0], c[0] + W[0]], [c[1] + Wy[1], c[1] + W[1]], color=fs.FORCE, lw=0.5, ls=':')
    q = c + Wx
    ax.text(q[0] - 0.1, q[1] + 0.05, r'$mg\sin\theta$', color=fs.FORCE, fontsize=9, ha='right', va='bottom')
    q = c + Wy
    ax.text(q[0] + 0.12, q[1] - 0.12, r'$mg\cos\theta$', color=fs.FORCE, fontsize=9, ha='left', va='top')
    fs.angle_arc(ax, tuple(c), 0.85, -90 - th, -90, r'$\theta$', fontsize=9, tr=1.1)
    # 좌표축(빗면 아래쪽 +x, 수직 바깥 +y)
    o = np.array([4.7, 1.35])
    fs.arrow(ax, tuple(o), tuple(o - u * 0.8), lw=0.9, ms=8)
    fs.arrow(ax, tuple(o), tuple(o + n * 0.8), lw=0.9, ms=8)
    q = o - u * 0.95; ax.text(q[0], q[1] - 0.12, r'$+x$', fontsize=9, ha='center')
    q = o + n * 0.95; ax.text(q[0] + 0.05, q[1] + 0.05, r'$+y$', fontsize=9, ha='center')
    fs.save(fig, __file__, 'fig05_08')


# ---------- 그림 5.9 예제 5.5 접촉한 두 상자 ----------
def fig09():
    fig, ax = fs.canvas(5.0, 2.7, xlim=(-0.3, 10.3), ylim=(-0.6, 5.0))
    y0 = 3.4
    fs.ground(ax, 0.3, 6.5, y0, depth=0.15, n=35)
    fs.block(ax, (2.6, y0 + 0.55), 1.3, 1.1, text='$m_1$')
    fs.block(ax, (3.9, y0 + 0.5), 1.3, 1.0, text='$m_2$')
    push(ax, (1.95, y0 + 0.55), (1.3, 0), r'$F$')
    fs.vec(ax, (5.0, y0 + 1.4), (1.0, 0), color=fs.ACC, lw=1.5, ms=9)
    ax.text(6.1, y0 + 1.4, r'$\vec a$', color=fs.ACC, fontsize=10, va='center')
    # 자유물체도
    c1 = np.array([2.0, 1.1]); c2 = np.array([7.4, 1.1])
    fs.block(ax, tuple(c1), 1.0, 0.9, text='$m_1$')
    fs.block(ax, tuple(c2), 1.0, 0.9, text='$m_2$')
    push(ax, c1 - (0.5, 0), (1.3, 0), r'$F = 20$ N', fontsize=8.5, loff=(0, 0.3))
    push(ax, c1 + (0.5, 0), (-0.75, 0), r'$P$', loff=(0, 0.25))
    force(ax, c1, (0, 1.0), r'$N_1$', start=0.45, loff=(0.25, -0.1))
    force(ax, c1, (0, -1.0), r'$m_1g$', start=0.45, loff=(0.35, 0.15))
    push(ax, c2 - (0.5, 0), (0.75, 0), r'$P = 8.0$ N', fontsize=8.5, loff=(-0.2, 0.3))
    force(ax, c2, (0, 1.0), r'$N_2$', start=0.45, loff=(0.25, -0.1))
    force(ax, c2, (0, -1.0), r'$m_2g$', start=0.45, loff=(0.35, 0.15))
    fs.save(fig, __file__, 'fig05_09')


# ---------- 그림 5.10 예제 5.6 애트우드 기계 ----------
def fig10():
    fig, ax = fs.canvas(4.6, 3.0, xlim=(-0.3, 8.4), ylim=(-0.4, 5.4))
    fs.ceiling(ax, 0.4, 3.2, 5.2)
    P = np.array([1.8, 4.3]); r = 0.45
    ax.plot([P[0], P[0]], [P[1], 5.2], color=fs.BLACK, lw=1.2)
    fs.pulley(ax, tuple(P), r=r)
    y1, y2 = 2.6, 1.3
    rope(ax, (P[0] - r, P[1]), (P[0] - r, y1 + 0.35)); rope(ax, (P[0] + r, P[1]), (P[0] + r, y2 + 0.4))
    fs.block(ax, (P[0] - r, y1), 0.65, 0.7, text='$m_1$', fontsize=9)
    fs.block(ax, (P[0] + r, y2), 0.75, 0.8, text='$m_2$', fontsize=9)
    fs.vec(ax, (P[0] - r - 0.65, y1 - 0.35), (0, 0.7), color=fs.ACC, lw=1.4, ms=8)
    ax.text(P[0] - r - 0.8, y1, r'$a$', color=fs.ACC, fontsize=9, ha='right', va='center')
    fs.vec(ax, (P[0] + r + 0.7, y2 + 0.35), (0, -0.7), color=fs.ACC, lw=1.4, ms=8)
    ax.text(P[0] + r + 0.85, y2, r'$a$', color=fs.ACC, fontsize=9, ha='left', va='center')
    # 자유물체도
    c1 = np.array([5.0, 2.6]); c2 = np.array([7.3, 2.6])
    fs.block(ax, tuple(c1), 0.6, 0.6, text='$m_1$', fontsize=9)
    fs.block(ax, tuple(c2), 0.6, 0.6, text='$m_2$', fontsize=9)
    sc = 1.4 / 29.4
    T = 2 * 2.0 * 3.0 * g / 5.0
    force(ax, c1, (0, T * sc), r'$T$', start=0.3, loff=(0.25, -0.1))
    force(ax, c1, (0, -2.0 * g * sc), r'$m_1g$', start=0.3, loff=(0.4, 0.15))
    force(ax, c2, (0, T * sc), r'$T$', start=0.3, loff=(0.25, -0.1))
    force(ax, c2, (0, -3.0 * g * sc), r'$m_2g$', start=0.3, loff=(0.4, 0.2))
    ax.text(6.15, 4.85, '자유물체도', fontsize=8.5, ha='center')
    fs.save(fig, __file__, 'fig05_10')


# ---------- 그림 5.11 예제 5.7 탁자 위 상자와 매달린 추 ----------
def fig11():
    fig, ax = fs.canvas(5.0, 2.7, xlim=(-0.3, 10.0), ylim=(-0.3, 5.0))
    ty = 3.2
    ax.add_patch(Rectangle((0.0, ty - 0.25), 4.2, 0.25, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((0.3, 0), 0.2, ty - 0.25, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((3.6, 0), 0.2, ty - 0.25, fc='#d9c3a0', ec=fs.BLACK, lw=1.0))
    fs.ground(ax, -0.2, 5.0, 0, depth=0.15, n=28)
    P = np.array([4.45, ty + 0.1]); r = 0.25
    ax.plot([4.2, P[0]], [ty - 0.1, P[1]], color=fs.BLACK, lw=1.2)
    fs.block(ax, (1.7, ty + 0.35), 1.1, 0.7, text='$m_1$', fontsize=9)
    rope(ax, (2.25, ty + 0.35), (P[0], P[1] + r))
    rope(ax, (P[0] + r, P[1]), (P[0] + r, 1.6))
    fs.pulley(ax, tuple(P), r=r)
    fs.block(ax, (P[0] + r, 1.25), 0.6, 0.7, text='$m_2$', fontsize=9)
    fs.vec(ax, (1.3, ty + 1.05), (0.8, 0), color=fs.ACC, lw=1.4, ms=8)
    ax.text(2.25, ty + 1.05, r'$a$', color=fs.ACC, fontsize=9, va='center')
    fs.vec(ax, (P[0] + r + 0.6, 1.6), (0, -0.7), color=fs.ACC, lw=1.4, ms=8)
    ax.text(P[0] + r + 0.75, 1.25, r'$a$', color=fs.ACC, fontsize=9, va='center')
    # 자유물체도
    c1 = np.array([6.6, 2.6]); c2 = np.array([8.9, 2.4])
    fs.block(ax, tuple(c1), 0.8, 0.55, text='$m_1$', fontsize=9)
    fs.block(ax, tuple(c2), 0.55, 0.6, text='$m_2$', fontsize=9)
    s1 = 0.035   # m1의 힘 축척(N당 길이)
    force(ax, c1, (7.8 * s1, 0), r'$T$', start=0.4, loff=(0.15, 0.25), ms=8)
    force(ax, c1, (0, 39.2 * s1), r'$N$', start=0.28, loff=(0.25, -0.1))
    force(ax, c1, (0, -39.2 * s1), r'$m_1g$', start=0.28, loff=(0.4, 0.2))
    sc = 0.1
    force(ax, c2, (0, 7.8 * sc), r'$T$', start=0.3, loff=(0.25, -0.1))
    force(ax, c2, (0, -9.8 * sc), r'$m_2g$', start=0.3, loff=(0.4, 0.15))
    fs.save(fig, __file__, 'fig05_11')


# ---------- 그림 5.12 용수철에 매단 물체(🐍 실습) ----------
def fig12():
    fig, ax = fs.plot_axes(4.6, 2.3)
    m, k = 0.50, 20.0
    w = np.sqrt(k / m); T = 2 * np.pi / w
    t = np.linspace(0, 3 * T, 600)
    y = m * g / k * (1 - np.cos(w * t))
    ax.plot(t, y, color=fs.VEL)
    ax.axhline(m * g / k, color=fs.BLACK, ls='--', lw=0.9)
    ax.text(3 * T * 1.03, m * g / k, '평형\n$mg/k$\n$= 0.245$ m', fontsize=8, ha='left', va='center')
    ax.invert_yaxis()
    ax.set_xlabel(r'$t$ (s)'); ax.set_ylabel(r'늘어난 길이 $y$ (m)')
    ax.set_ylim(0.52, -0.03)
    fs.save(fig, __file__, 'fig05_12')


# ---------- 그림 5.13 연습문제 4: 두 줄에 매달린 전등 ----------
def fig13():
    fig, ax = fs.canvas(3.6, 1.9, xlim=(-0.2, 5.5), ylim=(-0.8, 2.4))
    L = np.array([3.7, 0.0]); h = 2.0
    A = L + np.array([-h / np.tan(np.radians(30)), h])
    B = L + np.array([h / np.tan(np.radians(60)), h])
    fs.ceiling(ax, -0.1, 5.4, h)
    rope(ax, L, A); rope(ax, L, B)
    ax.add_patch(Circle(tuple(L + (0, -0.3)), 0.28, fc='#f6e27a', ec=fs.BLACK, lw=1.0, zorder=4))
    ax.plot([L[0] - 1.3, L[0] + 1.3], [0, 0], color=fs.GRAY, lw=0.6, ls=':')
    fs.angle_arc(ax, tuple(L), 0.8, 150, 180, r'$30^\circ$', fontsize=8, tr=1.2)
    fs.angle_arc(ax, tuple(L), 0.6, 0, 60, r'$60^\circ$', fontsize=8, tr=0.9)
    ax.text(L[0] + 0.4, L[1] - 0.4, '2.0 kg', fontsize=8, va='center')
    m = (L + A) / 2; ax.text(m[0], m[1] + 0.2, r'$T_1$', fontsize=9, ha='center', color=fs.FORCE)
    m = (L + B) / 2; ax.text(m[0] + 0.15, m[1], r'$T_2$', fontsize=9, color=fs.FORCE)
    fs.save(fig, __file__, 'fig05_13')


# ---------- 그림 5.14 연습문제 9: 빗면과 매달린 추 ----------
def fig14():
    fig, ax = fs.canvas(4.2, 2.4, xlim=(-0.2, 6.6), ylim=(-0.3, 3.9))
    th = 30; L = 5.6; bh = 0.55
    thr = np.radians(th)
    u = np.array([np.cos(thr), np.sin(thr)]); n = np.array([-np.sin(thr), np.cos(thr)])
    top = np.array(fs.incline(ax, origin=(0, 0), length=L, angle=th, angle_label=r'$30^\circ$'))
    c = u * 2.6 + n * (bh / 2)
    fs.block(ax, tuple(c), 0.8, bh, angle=th, text='$m_1$', fontsize=9)
    r = 0.25
    P = top + n * (bh / 2 + r) + u * 0.25
    ax.plot([top[0], P[0]], [top[1], P[1]], color=fs.BLACK, lw=1.2)
    rope(ax, c + u * 0.4, P - n * r)
    rope(ax, (P[0] + r, P[1]), (P[0] + r, 1.25))
    fs.pulley(ax, tuple(P), r=r)
    fs.block(ax, (P[0] + r, 0.9), 0.55, 0.7, text='$m_2$', fontsize=9)
    ax.text(1.1, -0.25, '마찰 없음', fontsize=7.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig05_14')


# ---------- 그림 5.15 연습문제 13: 움직이는 쐐기 ----------
def fig15():
    fig, ax = fs.canvas(4.2, 2.3, xlim=(-1.6, 6.0), ylim=(-0.4, 3.4))
    fs.ground(ax, -1.5, 5.9, 0, depth=0.15, n=40)
    th = np.radians(30); W = 4.5; H = W * np.tan(th)
    ax.add_patch(Polygon([(0, 0), (W, 0), (0, H)], fc='#f2f2f2', ec=fs.BLACK, lw=1.2, zorder=1))
    ax.text(0.6, 0.45, '$M$', fontsize=11)
    fs.angle_arc(ax, (W, 0), 0.7, 180 - 30, 180, r'$\theta$', fontsize=10, tr=0.95)
    s = 1.6
    u = np.array([np.cos(th), -np.sin(th)]); n = np.array([np.sin(th), np.cos(th)])
    c = np.array([0, H]) + u * s + n * 0.3
    fs.block(ax, tuple(c), 0.8, 0.6, angle=-30, text='$m$', fontsize=10)
    fs.vec(ax, (-0.2, 1.0), (-1.1, 0), color=fs.ACC, lw=1.6, ms=9)
    ax.text(-0.75, 1.25, r'$A$', color=fs.ACC, fontsize=10, ha='center')
    fs.vec(ax, tuple(c + n * 0.55 + u * 0.1), tuple(u * 0.9), color=fs.ACC, lw=1.0, ms=8, ls='--')
    ax.text(c[0] + 1.6, c[1] + 0.55, '쐐기에 대해\n빗면을 따라', fontsize=7.5, color=fs.ACC)
    ax.text(2.5, -0.33, '마찰 없음', fontsize=7.5, color=fs.GRAY, va='top')
    fs.save(fig, __file__, 'fig05_15')


# ---------- 그림 5.16 연습문제 14: 이중 애트우드 기계 ----------
def fig16():
    fig, ax = fs.canvas(2.6, 3.2, xlim=(-0.2, 3.6), ylim=(-0.3, 4.6))
    fs.ceiling(ax, 0.2, 2.8, 4.4)
    P = np.array([1.5, 3.7]); r = 0.4
    ax.plot([P[0], P[0]], [P[1], 4.4], color=fs.BLACK, lw=1.2)
    fs.pulley(ax, tuple(P), r=r)
    rope(ax, (P[0] - r, P[1]), (P[0] - r, 2.3))
    fs.block(ax, (P[0] - r, 2.0), 0.6, 0.6, text='$m_1$', fontsize=9)
    Q = np.array([P[0] + r, 2.4]); r2 = 0.3
    rope(ax, (P[0] + r, P[1]), (Q[0], Q[1] + r2))
    rope(ax, (Q[0] - r2, Q[1]), (Q[0] - r2, 1.0))
    rope(ax, (Q[0] + r2, Q[1]), (Q[0] + r2, 0.65))
    fs.pulley(ax, tuple(Q), r=r2)
    fs.block(ax, (Q[0] - r2, 0.75), 0.45, 0.5, text='$m_2$', fontsize=8)
    fs.block(ax, (Q[0] + r2 + 0.05, 0.35), 0.55, 0.6, text='$m_3$', fontsize=8)
    ax.text(Q[0] + r2 + 0.15, Q[1] + 0.05, '움직도르래', fontsize=7.5, va='center')
    fs.save(fig, __file__, 'fig05_16')


# ---------- 그림 5.17 연습문제 16: 스스로 끌어올리기 ----------
def fig17():
    fig, ax = fs.canvas(2.4, 3.0, xlim=(-0.3, 3.0), ylim=(-0.2, 4.4))
    fs.ceiling(ax, 0.0, 2.8, 4.2)
    P = np.array([1.4, 3.6]); r = 0.45
    ax.plot([P[0], P[0]], [P[1], 4.2], color=fs.BLACK, lw=1.2)
    fs.pulley(ax, tuple(P), r=r)
    seat_y = 0.8
    ax.add_patch(Rectangle((0.2, seat_y - 0.15), 1.2, 0.15, fc='#b9a27a', ec=fs.BLACK, lw=1.0, zorder=3))
    rope(ax, (P[0] - r, P[1]), (P[0] - r, seat_y))
    fs.block(ax, (0.55, seat_y + 0.45), 0.6, 0.9, text='사람', fontsize=7.5)
    hand_y = seat_y + 0.7
    ax.plot([0.85, P[0] + r], [hand_y, hand_y], color=fs.BLACK, lw=2.0, zorder=4)
    rope(ax, (P[0] + r, P[1]), (P[0] + r, hand_y))
    ax.text(0.8, seat_y - 0.4, '의자', fontsize=8, ha='center')
    ax.text(P[0] + r + 0.12, 2.6, '사람이\n당기는 줄', fontsize=7.5, va='center')
    ax.text(P[0] - r - 0.08, 2.6, '의자에\n맨 줄', fontsize=7.5, va='center', ha='right')
    fs.save(fig, __file__, 'fig05_17')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13,
              fig14, fig15, fig16, fig17):
        f()
