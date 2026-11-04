"""교재 그림 공통 스타일과 도우미 함수.

모든 그림은 figures/chNN/make_figs.py 가 이 모듈을 써서 만든다.
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
    import figstyle as fs
    fig, ax = fs.canvas(4.2, 2.8, xlim=(0, 6), ylim=(0, 4))
    ...
    fs.save(fig, __file__, 'fig05_01')     # figures/ch05/fig05_01.svg

원칙
- 글자는 SVG 안에서 곡선(path)으로 바뀌므로 어느 환경에서도 같은 모양으로 보인다.
- 색은 아래 팔레트만 쓴다. 힘=빨강, 속도=파랑, 가속도=초록, 변위·위치=검정, 장(場)=보라.
- 크기는 실제 인쇄 크기(인치)로 정한다. 본문 폭은 약 7인치, 보통 그림은 폭 3~5인치.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Polygon, Arc, Ellipse

# ---------- 기본 설정 ----------
plt.rcParams.update({
    'font.family': 'Noto Sans CJK KR',
    'mathtext.fontset': 'cm',          # 수식 기호는 본문 MathJax와 비슷한 Computer Modern
    'axes.unicode_minus': False,
    'svg.fonttype': 'path',
    'font.size': 10,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.4,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.04,
    'figure.dpi': 100,
})

# ---------- 팔레트 ----------
FORCE = '#c0392b'     # 힘
VEL = '#1f5fa8'       # 속도
ACC = '#2e8b57'       # 가속도
FIELD = '#7b3fa0'     # 전기장·자기장·중력장
POS = '#c0392b'       # 양전하
NEG = '#1f5fa8'       # 음전하
GRAY = '#7f8c8d'
LIGHT = '#e8eef5'     # 물체 채움
SURF = '#f5d76e'      # 가우스 면·폐곡면 강조
BLACK = '#222222'
ORANGE = '#e67e22'
CYCLE = [VEL, FORCE, ACC, ORANGE, FIELD, GRAY]   # 그래프 여러 선
plt.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=CYCLE)


# ---------- 캔버스 ----------
def canvas(w, h, xlim=None, ylim=None, axis=False):
    """도식용 캔버스. xlim/ylim을 주면 축 비율을 1:1로 고정한다."""
    fig, ax = plt.subplots(figsize=(w, h))
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    if xlim is not None and ylim is not None:
        ax.set_aspect('equal')
    if not axis:
        ax.axis('off')
    return fig, ax


def plot_axes(w=4.0, h=2.8):
    """그래프용 캔버스(눈금·격자 있음)."""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    return fig, ax


def save(fig, script_file, name):
    """figures/chNN/<name>.svg 로 저장. FIG_PREVIEW 환경변수가 있으면 그 폴더에 PNG 미리보기도 저장."""
    d = os.path.dirname(os.path.abspath(script_file))
    fig.savefig(os.path.join(d, name + '.svg'))
    pv = os.environ.get('FIG_PREVIEW')
    if pv:
        os.makedirs(pv, exist_ok=True)
        fig.savefig(os.path.join(pv, os.path.basename(d) + '_' + name + '.png'), dpi=130)
    plt.close(fig)


# ---------- 기본 도형 ----------
def arrow(ax, p, q, color=BLACK, lw=1.6, label=None, lpos=1.0, loff=(0.12, 0.12),
          fontsize=11, style='-|>', ms=12, ls='-', zorder=5, ha='center', va='center'):
    """p→q 화살표. label은 화살표 위의 lpos(0~1) 지점에서 loff만큼 떨어진 곳에 쓴다."""
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                        linestyle=ls, shrinkA=0, shrinkB=0, zorder=zorder)
    ax.add_patch(a)
    if label:
        x = p[0] + (q[0] - p[0]) * lpos + loff[0]
        y = p[1] + (q[1] - p[1]) * lpos + loff[1]
        ax.text(x, y, label, color=color, fontsize=fontsize, ha=ha, va=va, zorder=zorder + 1)
    return a


def vec(ax, origin, d, **kw):
    """origin에서 d=(dx,dy)만큼 가는 벡터."""
    return arrow(ax, origin, (origin[0] + d[0], origin[1] + d[1]), **kw)


def dot(ax, p, r=0.05, color=BLACK, zorder=6):
    ax.add_patch(Circle(p, r, color=color, zorder=zorder))


def label(ax, p, s, fontsize=11, color=BLACK, **kw):
    kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    ax.text(p[0], p[1], s, fontsize=fontsize, color=color, **kw)


def block(ax, center, w=1.0, h=0.7, angle=0.0, text=None, fc=LIGHT, ec=BLACK, fontsize=11, zorder=3):
    """중심이 center, 각도 angle(도)인 상자. 꼭짓점 배열을 돌려준다."""
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    R = np.array([[c, -s], [s, c]])
    pts = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]]) @ R.T + center
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.2, zorder=zorder))
    if text:
        ax.text(center[0], center[1], text, ha='center', va='center', fontsize=fontsize, zorder=zorder + 1)
    return pts


def ground(ax, x0, x1, y=0.0, depth=0.15, n=None, color=BLACK):
    """수평 바닥선과 아래쪽 빗금."""
    ax.plot([x0, x1], [y, y], color=color, lw=1.3, zorder=2)
    n = n or max(int((x1 - x0) / 0.18), 3)
    for x in np.linspace(x0, x1 - depth, n):
        ax.plot([x, x + depth], [y, y - depth], color=color, lw=0.7, zorder=2)


def wall(ax, y0, y1, x=0.0, depth=0.15, side='left', n=None, color=BLACK):
    """수직 벽과 빗금. side='left'면 빗금이 벽 왼쪽."""
    ax.plot([x, x], [y0, y1], color=color, lw=1.3, zorder=2)
    n = n or max(int((y1 - y0) / 0.18), 3)
    sgn = -1 if side == 'left' else 1
    for y in np.linspace(y0, y1 - depth, n):
        ax.plot([x, x + sgn * depth], [y, y + depth], color=color, lw=0.7, zorder=2)


def ceiling(ax, x0, x1, y, depth=0.15, n=None, color=BLACK):
    ax.plot([x0, x1], [y, y], color=color, lw=1.3, zorder=2)
    n = n or max(int((x1 - x0) / 0.18), 3)
    for x in np.linspace(x0, x1 - depth, n):
        ax.plot([x, x + depth], [y, y + depth], color=color, lw=0.7, zorder=2)


def incline(ax, origin=(0, 0), length=4.0, angle=30.0, fc='#f2f2f2', show_angle=True, angle_label=r'$\theta$'):
    """origin(아래 왼쪽 꼭짓점)에서 오른쪽 위로 올라가는 빗면 삼각형. 빗면 위쪽 끝 좌표를 돌려준다."""
    th = np.radians(angle)
    x0, y0 = origin
    base = length * np.cos(th)
    top = (x0 + base, y0 + length * np.sin(th))
    ax.add_patch(Polygon([origin, (x0 + base, y0), top], closed=True, fc=fc, ec=BLACK, lw=1.2, zorder=1))
    if show_angle:
        angle_arc(ax, origin, 0.6, 0, angle, angle_label)
    return top


def angle_arc(ax, center, r, th1, th2, text=None, color=BLACK, fontsize=10, tr=None):
    """center에서 각 th1→th2(도) 호와 글자."""
    ax.add_patch(Arc(center, 2 * r, 2 * r, theta1=min(th1, th2), theta2=max(th1, th2), color=color, lw=0.9))
    if text:
        tm = np.radians((th1 + th2) / 2)
        tr = tr or r * 1.35
        ax.text(center[0] + tr * np.cos(tm), center[1] + tr * np.sin(tm), text,
                ha='center', va='center', fontsize=fontsize, color=color)


def spring(ax, p, q, coils=8, width=0.18, color=BLACK, lw=1.1, lead=0.15):
    """p와 q 사이의 지그재그 용수철."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    L = np.linalg.norm(d)
    u = d / L
    nrm = np.array([-u[1], u[0]])
    pts = [p, p + u * lead]
    m = 2 * coils
    for i in range(1, m + 1):
        t = lead + (L - 2 * lead) * (i - 0.5) / m
        pts.append(p + u * t + nrm * width * (1 if i % 2 else -1))
    pts += [q - u * lead, q]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=3)


def dim(ax, p, q, text, off=0.25, color=GRAY, fontsize=10):
    """치수선: p-q 사이 양쪽 화살표, 선분에 수직으로 off만큼 띄워 그린다."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    u = (q - p) / np.linalg.norm(q - p)
    n = np.array([-u[1], u[0]]) * off
    a, b = p + n, q + n
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='<|-|>', mutation_scale=8, color=color, lw=0.8))
    for e, f in ((p, a), (q, b)):
        ax.plot([e[0], f[0] + n[0] * 0.3], [e[1], f[1] + n[1] * 0.3], color=color, lw=0.5)
    m = (a + b) / 2 + n * 0.6
    ax.text(m[0], m[1], text, ha='center', va='center', fontsize=fontsize, color=color)


def charge(ax, p, q=+1, r=0.18, fontsize=12):
    """점전하. q>0이면 빨간 +, q<0이면 파란 −."""
    c = POS if q > 0 else NEG
    ax.add_patch(Circle(p, r, fc=c, ec='none', zorder=7))
    ax.text(p[0], p[1] - 0.01, '+' if q > 0 else '−', color='white', ha='center', va='center',
            fontsize=fontsize, fontweight='bold', zorder=8)


def _efield(charges, p):
    E = np.zeros(2)
    for (cx, cy, q) in charges:
        d = p - np.array([cx, cy]); r = np.hypot(*d) + 1e-12
        E += q * d / r ** 3
    return E


def field_lines(ax, charges, xlim, ylim, per_unit=8, color=FIELD, lw=0.9, r0=0.2, step=0.02,
                arrows=True, max_steps=4000, start_angle=0.0):
    """교과서식 전기력선. [(x, y, q), ...]의 양전하에서 |q|·per_unit 개씩 출발해 음전하나 그림 밖에서 끝난다.
    양전하가 없거나 음전하가 더 크면 음전하에서 거꾸로도 그린다."""
    qpos = sum(q for *_, q in charges if q > 0); qneg = -sum(q for *_, q in charges if q < 0)
    def trace(start, sgn):
        pts = [start]; p = np.array(start, float)
        for _ in range(max_steps):
            def f(x):
                E = _efield(charges, x); n = np.hypot(*E) + 1e-12; return sgn * E / n
            k1 = f(p); k2 = f(p + step / 2 * k1); k3 = f(p + step / 2 * k2); k4 = f(p + step * k3)
            p = p + step / 6 * (k1 + 2 * k2 + 2 * k3 + k4); pts.append(p.copy())
            if not (xlim[0] - 0.5 < p[0] < xlim[1] + 0.5 and ylim[0] - 0.5 < p[1] < ylim[1] + 0.5):
                break
            if any(np.hypot(p[0] - cx, p[1] - cy) < r0 * 0.9 for (cx, cy, q) in charges if q * sgn < 0):
                break
        return np.array(pts)
    lines = []
    src_sign = 1 if qpos >= qneg else -1
    for (cx, cy, q) in charges:
        if q * src_sign <= 0:
            continue
        n = max(int(round(abs(q) * per_unit)), 2)
        for k in range(n):
            a = 2 * np.pi * k / n + np.radians(start_angle)
            pts = trace((cx + r0 * np.cos(a), cy + r0 * np.sin(a)), src_sign)
            if src_sign < 0:
                pts = pts[::-1]
            lines.append(pts)
    # 반대 부호 전하 쪽에서도 거꾸로 추적해, 그림 밖에서 들어오는 선을 채운다(원천 전하에서 끝나는 선은 중복이므로 버린다).
    for (cx, cy, q) in charges:
        if q * src_sign >= 0:
            continue
        n = max(int(round(abs(q) * per_unit)), 2)
        for k in range(n):
            a = 2 * np.pi * k / n + np.radians(start_angle) + np.pi / n
            pts = trace((cx + r0 * np.cos(a), cy + r0 * np.sin(a)), -src_sign)
            end = pts[-1]
            if any(np.hypot(end[0] - sx, end[1] - sy) < r0 for (sx, sy, sq) in charges if sq * src_sign > 0):
                continue
            lines.append(pts if src_sign < 0 else pts[::-1])
    for pts in lines:
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=1)
        if arrows and len(pts) > 20:
            inside = [i for i, p in enumerate(pts) if xlim[0] < p[0] < xlim[1] and ylim[0] < p[1] < ylim[1]]
            if inside:
                i = inside[len(inside) // 2]
                j = min(i + 3, len(pts) - 1)
                ax.add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle='-|>', mutation_scale=9,
                                             color=color, lw=0, zorder=2))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)


def dot_out(ax, p, r=0.09, color=BLACK):
    """지면에서 나오는 방향(⊙)."""
    ax.add_patch(Circle(p, r, fc='white', ec=color, lw=1.0, zorder=6))
    ax.add_patch(Circle(p, r * 0.28, color=color, zorder=7))


def cross_in(ax, p, r=0.09, color=BLACK):
    """지면으로 들어가는 방향(⊗)."""
    ax.add_patch(Circle(p, r, fc='white', ec=color, lw=1.0, zorder=6))
    k = r * 0.65
    ax.plot([p[0] - k, p[0] + k], [p[1] - k, p[1] + k], color=color, lw=1.0, zorder=7)
    ax.plot([p[0] - k, p[0] + k], [p[1] + k, p[1] - k], color=color, lw=1.0, zorder=7)


def field_grid(ax, xlim, ylim, kind='in', step=0.5, color=FIELD, r=0.06):
    """균일 자기장을 ⊙/⊗ 격자로 표시."""
    for x in np.arange(xlim[0] + step / 2, xlim[1], step):
        for y in np.arange(ylim[0] + step / 2, ylim[1], step):
            (cross_in if kind == 'in' else dot_out)(ax, (x, y), r=r, color=color)


def ellipse3d(ax, center, rx, ry, color=BLACK, lw=1.0, back_dashed=True, fc='none', zorder=3):
    """비스듬히 본 원(원통·구의 단면). 뒤쪽 절반은 점선."""
    th = np.linspace(0, np.pi, 100)
    x = center[0] + rx * np.cos(th); y = center[1] + ry * np.sin(th)
    ax.plot(x, y, color=color, lw=lw, ls='--' if back_dashed else '-', zorder=zorder)
    th = np.linspace(np.pi, 2 * np.pi, 100)
    x = center[0] + rx * np.cos(th); y = center[1] + ry * np.sin(th)
    ax.plot(x, y, color=color, lw=lw, zorder=zorder)
    if fc != 'none':
        ax.add_patch(Ellipse(center, 2 * rx, 2 * ry, fc=fc, ec='none', zorder=zorder - 1))


def sphere(ax, center, r, fc=SURF, alpha=0.35, ec=BLACK, equator=True):
    """반투명 구(가우스 면 등). 적도는 비스듬한 타원."""
    ax.add_patch(Circle(center, r, fc=fc, alpha=alpha, ec='none', zorder=1))
    ax.add_patch(Circle(center, r, fc='none', ec=ec, lw=1.1, zorder=3))
    if equator:
        ellipse3d(ax, center, r, r * 0.3, color=ec, lw=0.8)


def cylinder(ax, center, r, h, fc=SURF, alpha=0.35, ec=BLACK, ry=None, vertical=True):
    """비스듬히 본 원통. vertical=True면 축이 세로, 아니면 가로."""
    ry = ry or r * 0.3
    cx, cy = center
    if vertical:
        ax.add_patch(Rectangle((cx - r, cy - h / 2), 2 * r, h, fc=fc, alpha=alpha, ec='none', zorder=1))
        ax.plot([cx - r, cx - r], [cy - h / 2, cy + h / 2], color=ec, lw=1.1, zorder=3)
        ax.plot([cx + r, cx + r], [cy - h / 2, cy + h / 2], color=ec, lw=1.1, zorder=3)
        ax.add_patch(Ellipse((cx, cy + h / 2), 2 * r, 2 * ry, fc=fc, alpha=alpha, ec=ec, lw=1.1, zorder=2))
        ellipse3d(ax, (cx, cy - h / 2), r, ry, color=ec, lw=1.1)
    else:
        ax.add_patch(Rectangle((cx - h / 2, cy - r), h, 2 * r, fc=fc, alpha=alpha, ec='none', zorder=1))
        ax.plot([cx - h / 2, cx + h / 2], [cy - r, cy - r], color=ec, lw=1.1, zorder=3)
        ax.plot([cx - h / 2, cx + h / 2], [cy + r, cy + r], color=ec, lw=1.1, zorder=3)
        ax.add_patch(Ellipse((cx + h / 2, cy), 2 * ry, 2 * r, fc=fc, alpha=alpha, ec=ec, lw=1.1, zorder=2))
        th = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
        ax.plot(cx - h / 2 + ry * np.cos(th), cy + r * np.sin(th), color=ec, lw=1.1, zorder=3)
        th = np.linspace(-np.pi / 2, np.pi / 2, 100)
        ax.plot(cx - h / 2 + ry * np.cos(th), cy + r * np.sin(th), color=ec, lw=1.1, ls='--', zorder=3)


def pulley(ax, center, r=0.3, fc='#dfe6ee'):
    ax.add_patch(Circle(center, r, fc=fc, ec=BLACK, lw=1.2, zorder=4))
    ax.add_patch(Circle(center, r * 0.15, fc=BLACK, zorder=5))


def lens(ax, x, h=1.2, kind='convex', color=VEL, bulge=0.15):
    """세로 축 위치 x의 얇은 렌즈. kind='convex' 또는 'concave'."""
    y = np.linspace(-h, h, 100)
    if kind == 'convex':
        xs = bulge * (1 - (y / h) ** 2)
        ax.fill_betweenx(y, x - xs, x + xs, color=color, alpha=0.25, lw=0)
        ax.plot(x - xs, y, color=color, lw=1.1); ax.plot(x + xs, y, color=color, lw=1.1)
    else:
        xs = bulge * (y / h) ** 2 + 0.03
        ax.fill_betweenx(y, x - xs, x + xs, color=color, alpha=0.25, lw=0)
        ax.plot(x - xs, y, color=color, lw=1.1); ax.plot(x + xs, y, color=color, lw=1.1)
        ax.plot([x - xs[0], x + xs[0]], [-h, -h], color=color, lw=1.1)
        ax.plot([x - xs[-1], x + xs[-1]], [h, h], color=color, lw=1.1)


def ray(ax, pts, color=ORANGE, lw=1.2, arrows=True, ls='-'):
    """꺾인 광선. 각 구간 중간에 진행 방향 화살촉."""
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=ls, zorder=4)
    if arrows:
        for a, b in zip(pts[:-1], pts[1:]):
            m = a + (b - a) * 0.55
            ax.add_patch(FancyArrowPatch(a + (b - a) * 0.45, m, arrowstyle='-|>', mutation_scale=9,
                                         color=color, lw=0, zorder=4))


def wave(ax, x0, x1, y0=0.0, amp=0.3, wavelength=1.0, color=VEL, lw=1.4, phase=0.0, n=400):
    x = np.linspace(x0, x1, n)
    ax.plot(x, y0 + amp * np.sin(2 * np.pi * (x - x0) / wavelength + phase), color=color, lw=lw)


# ---------- 회로도(schemdraw) ----------
def schem():
    """schemdraw 기본 설정을 맞추고 모듈을 돌려준다.
        sd, elm = fs.schem()
        with sd.Drawing(show=False) as d:
            d += elm.Battery().up().label(r'$\\mathcal{E}$')
            ...
        fs.save_schem(d, __file__, 'fig25_03')
    """
    import schemdraw, schemdraw.elements as elm
    schemdraw.config(fontsize=11, font='Noto Sans CJK KR', lw=1.4)
    schemdraw.use('matplotlib')  # matplotlib 백엔드: 글자를 path로 저장(rcParams 공유)
    return schemdraw, elm


def save_schem(d, script_file, name):
    d_ = os.path.dirname(os.path.abspath(script_file))
    d.save(os.path.join(d_, name + '.svg'))
    pv = os.environ.get('FIG_PREVIEW')
    if pv:
        os.makedirs(pv, exist_ok=True)
        d.save(os.path.join(pv, os.path.basename(d_) + '_' + name + '.png'), dpi=130)
