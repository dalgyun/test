"""29장 전자기 진동과 교류 회로 — 그림 생성 스크립트.
python3 figures/ch29/make_figs.py  (FIG_PREVIEW=<폴더> 를 주면 PNG 미리보기도 저장)
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon, Arc

sd, elm = fs.schem()
F = fs.FIELD
CR, CL, CC = fs.BLACK, fs.VEL, fs.FORCE   # 저항·인덕터·축전기 전압 색
CI = fs.ORANGE                             # 전류


def tip(ax, p, d, color=CI, ms=10, zorder=6):
    p = np.asarray(p, float); d = np.asarray(d, float); d = d / (np.hypot(*d) + 1e-12)
    ax.add_patch(FancyArrowPatch(p - d * 0.02, p + d * 0.02, arrowstyle='-|>', mutation_scale=ms,
                                 color=color, lw=0, zorder=zorder))


def graph_ax(ax):
    ax.grid(True, lw=0.4, color='#d0d0d0')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def finish(ax, d, padx=0.4, pady=0.4):
    d.draw(show=False)
    ax.axis('off'); ax.set_aspect('equal')
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - padx, x1 + padx); ax.set_ylim(y0 - pady, y1 + pady)


def phasor(ax, p, q, color, lw=2.0, label=None, loff=(0, 0), ls='-', fontsize=11, ha='center', va='center'):
    fs.arrow(ax, p, q, color=color, lw=lw, ms=12, ls=ls)
    if label:
        ax.text(q[0] + loff[0], q[1] + loff[1], label, color=color, fontsize=fontsize, ha=ha, va=va)


# ---------- 그림 29.1 LC 회로 ----------
def fig01():
    fig, ax = plt.subplots(figsize=(2.8, 2.2))
    d = sd.Drawing(canvas=ax)
    d += (cap := elm.Capacitor().down())
    d += elm.Line().right(3)
    d += (ind := elm.Inductor2(loops=4).up())
    d += elm.Line().left(3)
    finish(ax, d)
    c = (np.array(cap.start) + np.array(cap.end)) / 2
    ax.text(c[0] + 0.45, c[1] + 0.3, r'$+q$', fontsize=10, color=fs.POS, va='center')
    ax.text(c[0] + 0.45, c[1] - 0.3, r'$-q$', fontsize=10, color=fs.NEG, va='center')
    ax.text(c[0] - 0.45, c[1], r'$C$', fontsize=11, ha='right', va='center')
    m = (np.array(ind.start) + np.array(ind.end)) / 2
    ax.text(m[0] + 0.5, m[1], r'$L$', fontsize=11, va='center')
    y = cap.start[1]
    fs.arrow(ax, (1.9, y + 0.3), (0.9, y + 0.3), color=CI, lw=1.4, ms=10)
    ax.text(1.4, y + 0.45, r'$i = dq/dt$', fontsize=9.5, color=CI, ha='center', va='bottom')
    fs.save(fig, __file__, 'fig29_01')


# ---------- 그림 29.2 LC 회로의 에너지 교환 ----------
def lc_panel(ax, q, i, title):
    """q, i: 처음 값으로 나눈 값(−1..1). 축전기 왼쪽, 인덕터 오른쪽."""
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(-1.75, 2.45); ax.set_aspect('equal'); ax.axis('off')
    # 도선
    ax.plot([0, 0, 2.6, 2.6, 0, 0], [1.2, 2.0, 2.0, 0.0, 0.0, 0.7], color=fs.BLACK, lw=1.2)
    ax.plot([2.6, 2.6], [0.0, 2.0], color='white', lw=3)
    ax.plot([2.6, 2.6], [0.0, 0.35], color=fs.BLACK, lw=1.2); ax.plot([2.6, 2.6], [1.65, 2.0], color=fs.BLACK, lw=1.2)
    # 축전기 판
    ax.plot([-0.4, 0.4], [1.2, 1.2], color=fs.BLACK, lw=2.2); ax.plot([-0.4, 0.4], [0.7, 0.7], color=fs.BLACK, lw=2.2)
    if abs(q) > 0.05:
        top, bot = ('+', '−') if q > 0 else ('−', '+')
        ax.text(-0.5, 1.3, top, fontsize=10, color=fs.POS if top == '+' else fs.NEG, ha='center', va='center')
        ax.text(-0.5, 0.6, bot, fontsize=10, color=fs.POS if bot == '+' else fs.NEG, ha='center', va='center')
        for x in (-0.22, 0.0, 0.22):
            fs.arrow(ax, (x, 1.16 if q > 0 else 0.74), (x, 0.74 if q > 0 else 1.16), color=F, lw=0.9, ms=6)
        ax.text(0.5, 0.95, r'$\vec{E}$', fontsize=9, color=F, va='center')
    # 인덕터 코일
    th = np.linspace(0, 2 * np.pi * 4, 400)
    ax.plot(2.6 + 0.2 * np.sin(th), 0.45 + 1.1 * th / th[-1] - 0.1 * np.cos(th) + 0.1, color=fs.BLACK, lw=1.2)
    if abs(i) > 0.05:
        sgn = -1 if i > 0 else 1
        fs.arrow(ax, (3.05, 1.0 - 0.35 * sgn), (3.05, 1.0 + 0.35 * sgn), color=F, lw=1.4, ms=8)
        ax.text(3.2, 1.0, r'$\vec{B}$', fontsize=9, color=F, va='center')
        # 전류: i>0이면 위 판으로 들어감 → 위 도선에서 왼쪽으로(반시계)
        d = (-1, 0) if i > 0 else (1, 0)
        tip(ax, (1.3, 2.0), d, color=CI, ms=12)
        ax.text(1.3, 2.13, r'$i$', fontsize=10, color=CI, ha='center', va='bottom')
    # 에너지 막대
    UE, UB = q ** 2, i ** 2
    ax.add_patch(Rectangle((0.3, -1.3), 0.6, 0.02 + 0.9 * UE, fc=fs.FORCE, ec='none'))
    ax.add_patch(Rectangle((1.9, -1.3), 0.6, 0.02 + 0.9 * UB, fc=fs.VEL, ec='none'))
    ax.plot([0.1, 2.7], [-1.3, -1.3], color=fs.BLACK, lw=0.8)
    ax.text(0.6, -1.42, r'$U_E$', fontsize=9, ha='center', va='top')
    ax.text(2.2, -1.42, r'$U_B$', fontsize=9, ha='center', va='top')
    ax.text(1.3, 2.38, title, fontsize=9, ha='center', va='bottom')


def fig02():
    fig, axs = plt.subplots(1, 4, figsize=(5.6, 2.5))
    for ax, ph, title in zip(axs, [0, 0.25, 0.5, 0.75], [r'$t = 0$', r'$t = T/4$', r'$t = T/2$', r'$t = 3T/4$']):
        w = 2 * np.pi * ph
        q, i = np.cos(w), -np.sin(w)
        q = 0 if abs(q) < 1e-9 else q; i = 0 if abs(i) < 1e-9 else i
        lc_panel(ax, q, i, title)
    fig.subplots_adjust(wspace=0.05)
    fs.save(fig, __file__, 'fig29_02')


# ---------- 그림 29.3 LC 진동: 전하·전류와 에너지 (예제 29.1) ----------
def fig03():
    L, C, V = 10e-3, 1e-6, 10.0
    w = 1 / np.sqrt(L * C); T = 2 * np.pi / w; Q0 = C * V
    t = np.linspace(0, 1.5 * T, 600); tm = t * 1e3
    fig, axs = plt.subplots(2, 1, figsize=(4.4, 3.4), sharex=True)
    for a in axs: graph_ax(a)
    ax = axs[0]
    ax.plot(tm, Q0 * np.cos(w * t) * 1e6, color=fs.FORCE, lw=1.7, label=r'$q$ ($\mu$C)')
    ax.plot(tm, -w * Q0 * np.sin(w * t) * 100, color=CI, lw=1.7, ls='--', label=r'$i$ (×0.01 A)')
    ax.set_ylim(-12, 17); ax.set_yticks([-10, 0, 10])
    ax.legend(fontsize=8.5, loc='upper center', frameon=False, ncol=2, borderaxespad=0.1)
    ax.set_ylabel('전하·전류')
    ax = axs[1]
    UE = Q0 ** 2 / (2 * C) * np.cos(w * t) ** 2 * 1e6; UB = Q0 ** 2 / (2 * C) * np.sin(w * t) ** 2 * 1e6
    ax.plot(tm, UE, color=fs.FORCE, lw=1.7, label=r'$U_E$')
    ax.plot(tm, UB, color=fs.VEL, lw=1.7, ls='--', label=r'$U_B$')
    ax.plot(tm, UE + UB, color=fs.BLACK, lw=1.0, label='합')
    ax.plot(T / 8 * 1e3, 25, 'o', color=fs.BLACK, ms=4)
    ax.annotate(r'$t = T/8 = 79\ \mu$s', xy=(T / 8 * 1e3, 25), xytext=(0.17, 28),
                fontsize=8.5, arrowprops=dict(arrowstyle='->', lw=0.7),
                bbox=dict(fc='white', ec='none', pad=1))
    ax.set_ylim(0, 72); ax.set_ylabel(r'에너지 ($\mu$J)')
    ax.set_xlabel(r'$t$ (ms)'); ax.set_xlim(0, 1.5 * T * 1e3)
    ax.legend(fontsize=8.5, loc='upper center', frameon=False, ncol=3, borderaxespad=0.1)
    fig.subplots_adjust(hspace=0.12)
    fs.save(fig, __file__, 'fig29_03')


# ---------- 그림 29.4 RLC 감쇠의 세 영역 ----------
def fig04():
    L, C = 10e-3, 1e-6
    w0 = 1 / np.sqrt(L * C)
    t = np.linspace(0, 3e-3, 1500)
    def q(R):
        b = R / (2 * L)
        if b < w0:
            wd = np.sqrt(w0 ** 2 - b ** 2)
            return np.exp(-b * t) * (np.cos(wd * t) + b / wd * np.sin(wd * t))
        if np.isclose(b, w0):
            return (1 + b * t) * np.exp(-b * t)
        s = np.sqrt(b ** 2 - w0 ** 2); r1, r2 = -b + s, -b - s
        return (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1)
    fig, ax = fs.plot_axes(4.4, 2.6)
    tm = t * 1e3
    ax.plot(tm, q(20), color=fs.VEL, lw=1.4, label=r'약한 감쇠 $R = 20\ \Omega$')
    ax.plot(tm, np.exp(-20 / (2 * L) * t), color=fs.VEL, lw=0.8, ls=':')
    ax.plot(tm, -np.exp(-20 / (2 * L) * t), color=fs.VEL, lw=0.8, ls=':')
    ax.plot(tm, q(200), color=fs.FORCE, lw=1.8, label=r'임계 감쇠 $R = 200\ \Omega$')
    ax.plot(tm, q(600), color=fs.ACC, lw=1.6, ls='--', label=r'과감쇠 $R = 600\ \Omega$')
    ax.axhline(0, color=fs.BLACK, lw=0.6)
    ax.set_xlabel(r'$t$ (ms)'); ax.set_ylabel(r'$q/Q_0$'); ax.set_xlim(0, 3); ax.set_ylim(-1.05, 1.15)
    ax.legend(fontsize=8, loc='upper right', frameon=True, framealpha=0.9, edgecolor='none')
    fs.save(fig, __file__, 'fig29_04')


# ---------- 그림 29.5 세 소자의 위상 관계 ----------
def fig05():
    fig = plt.figure(figsize=(5.6, 3.3))
    x = np.linspace(0, 4 * np.pi, 400)
    items = [('저항', 0, CR, r'$v_R$'), ('인덕터', 90, CL, r'$v_L$'), ('축전기', -90, CC, r'$v_C$')]
    for k, (name, ph, col, vl) in enumerate(items):
        ax = fig.add_axes([0.04 + k * 0.33, 0.52, 0.28, 0.38])
        ax.plot(x, np.sin(x), color=CI, lw=1.4)
        ax.plot(x, 1.2 * np.sin(x + np.radians(ph)), color=col, lw=1.8)
        ax.axhline(0, color=fs.GRAY, lw=0.6)
        ax.set_xlim(0, 4 * np.pi); ax.set_ylim(-1.45, 1.6); ax.axis('off')
        ax.text(4 * np.pi, -1.4, r'$t$', fontsize=9, ha='right', color=fs.GRAY)
        ax.set_title(name, fontsize=10)
        lab = {0: '같은 위상', 90: '전압이 90° 앞섬', -90: '전압이 90° 뒤짐'}[ph]
        ax.text(2 * np.pi, -1.75, lab, fontsize=8.5, ha='center', va='top')
        # 범례 대신 글자
        ax.text(0.4, 1.5, vl, color=col, fontsize=10, va='center')
        ax.text(1.6, 1.5, r'$i$', color=CI, fontsize=10, va='center')
        bx = fig.add_axes([0.06 + k * 0.33, 0.02, 0.24, 0.32])
        bx.set_xlim(-1.4, 1.4); bx.set_ylim(-1.3, 1.3); bx.set_aspect('equal'); bx.axis('off')
        th = np.radians(35)
        phasor(bx, (0, 0), (0.9 * np.cos(th), 0.9 * np.sin(th)), CI, lw=1.6, label=r'$\tilde{I}$',
               loff=(0.25, -0.15) if ph == 0 else (0.15, 0.1), fontsize=10)
        a = th + np.radians(ph)
        phasor(bx, (0, 0), (1.15 * np.cos(a), 1.15 * np.sin(a)), col, lw=2.0,
               label=r'$\tilde{V}$', loff={0: (-0.1, 0.22), 90: (-0.22, 0.05), -90: (0.2, -0.12)}[ph], fontsize=10)
        if ph:
            fs.angle_arc(bx, (0, 0), 0.35, np.degrees(min(th, a)), np.degrees(max(th, a)), None)
    fs.save(fig, __file__, 'fig29_05')


# ---------- 그림 29.6 리액턴스와 진동수 ----------
def fig06():
    L, C = 0.50, 10e-6
    f = np.linspace(5, 200, 500)
    XL = 2 * np.pi * f * L; XC = 1 / (2 * np.pi * f * C)
    fig, ax = fs.plot_axes(4.0, 2.6)
    ax.plot(f, XL, color=CL, lw=1.8, label=r'$X_L = \omega_d L$')
    ax.plot(f, XC, color=CC, lw=1.8, ls='--', label=r'$X_C = 1/\omega_d C$')
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    ax.axvline(f0, color=fs.GRAY, lw=0.7, ls=':')
    ax.text(f0 + 2, 560, r'$f_0 = 71$ Hz', fontsize=8.5, color=fs.GRAY)
    ax.axvline(60, color=fs.GRAY, lw=0.7, ls='-.')
    for v, c in [(2 * np.pi * 60 * L, CL), (1 / (2 * np.pi * 60 * C), CC)]:
        ax.plot(60, v, 'o', color=c, ms=4)
        ax.text(57, v, f'{v:.0f} Ω', fontsize=8.5, color=c, ha='right', va='center')
    ax.set_xlabel(r'진동수 $f$ (Hz)'); ax.set_ylabel(r'리액턴스 ($\Omega$)')
    ax.set_xlim(0, 200); ax.set_ylim(0, 700)
    ax.legend(fontsize=8.5, loc='upper right', frameon=False)
    fs.save(fig, __file__, 'fig29_06')


# ---------- 그림 29.7 직렬 RLC 회로 ----------
def fig07():
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    d = sd.Drawing(canvas=ax)
    d += (src := elm.SourceSin().up().label(r'$\mathcal{E}_m\sin\omega_d t$', loc='bottom', ofst=0.3))
    d += (r := elm.Resistor().right().label(r'$R$', loc='top'))
    d += (l := elm.Inductor2(loops=4).right().label(r'$L$', loc='top'))
    d += (c := elm.Capacitor().down().label(r'$C$', loc='bottom', ofst=0.3))
    d += elm.Line().left().tox(src.start)
    finish(ax, d)
    fs.save(fig, __file__, 'fig29_07')


# ---------- 그림 29.8 직렬 RLC 회로의 페이저 그림 ----------
def fig08():
    fig, ax = fs.canvas(3.6, 3.0, xlim=(-0.6, 3.4), ylim=(-1.6, 2.4))
    VR, VL, VC = 2.2, 2.1, 0.9
    phasor(ax, (0, 0), (VR, 0), CR, label=r'$V_R$', loff=(0.05, -0.22))
    phasor(ax, (0, 0), (0, VL), CL, label=r'$V_L$', loff=(-0.3, 0))
    phasor(ax, (0, 0), (0, -VC), CC, label=r'$V_C$', loff=(-0.3, 0))
    phasor(ax, (0, 0), (VR * 0.55, 0), CI, lw=1.4, label=None)
    ax.text(VR * 0.45, -0.22, r'$I$', color=CI, fontsize=11, ha='center')
    fs.arrow(ax, (VR, 0), (VR, VL - VC), color=fs.GRAY, lw=1.2, ls='--', ms=10)
    ax.text(VR + 0.08, (VL - VC) / 2, r'$V_L - V_C$', fontsize=9.5, color=fs.GRAY, va='center')
    ax.plot([0, VR], [VL - VC, VL - VC], color=fs.GRAY, lw=0.6, ls=':')
    phasor(ax, (0, 0), (VR, VL - VC), F, lw=2.4, label=r'$\mathcal{E}_m$', loff=(0.12, 0.2))
    fs.angle_arc(ax, (0, 0), 0.7, 0, np.degrees(np.arctan2(VL - VC, VR)), r'$\phi$', fontsize=11, tr=0.9)
    ax.add_patch(Circle((0, 0), 0.05, color=fs.BLACK, zorder=8))
    ax.add_patch(Arc((0, 0), 5.4, 5.4, theta1=35, theta2=55, color=fs.GRAY, lw=0.9))
    tip(ax, (2.7 * np.cos(np.radians(55)), 2.7 * np.sin(np.radians(55))), (-np.sin(np.radians(55)), np.cos(np.radians(55))),
        color=fs.GRAY, ms=9)
    ax.text(2.05, 2.25, r'$\omega_d$로 회전', fontsize=8.5, color=fs.GRAY)
    fs.save(fig, __file__, 'fig29_08')


# ---------- 그림 29.9 예제 29.4의 페이저 (실제 비율) ----------
def fig09():
    VR, VL, VC = 175, 329, 463
    s = 1 / 120
    fig, ax = fs.canvas(3.3, 3.4, xlim=(-1.0, 3.2), ylim=(-4.2, 3.2))
    phasor(ax, (0, 0), (VR * s, 0), CR, label=r'$V_R = 175$', loff=(0.05, 0.25), fontsize=9)
    phasor(ax, (0, 0), (0, VL * s), CL, label=r'$V_L = 329$', loff=(0.12, -0.1), fontsize=9, ha='left')
    phasor(ax, (0, 0), (0, -VC * s), CC, label=r'$V_C = 463$', loff=(0.12, 0.1), fontsize=9, ha='left')
    fs.arrow(ax, (VR * s, 0), (VR * s, (VL - VC) * s), color=fs.GRAY, lw=1.1, ls='--', ms=9)
    ax.text(VR * s + 0.1, (VL - VC) * s / 2, r'$V_L - V_C$' + '\n' + r'$= -134$', fontsize=8.5, color=fs.GRAY, va='center')
    phasor(ax, (0, 0), (VR * s, (VL - VC) * s), F, lw=2.4, label=r'$\mathcal{E}_{\rm rms} = 220$', loff=(-0.1, -0.35), fontsize=9)
    fs.angle_arc(ax, (0, 0), 0.6, np.degrees(np.arctan2(VL - VC, VR)), 0, None)
    ax.text(-0.15, -0.35, r'$\phi = -37.5$°', fontsize=8.5, ha='right', va='center')
    ax.add_patch(Circle((0, 0), 0.05, color=fs.BLACK, zorder=8))
    ax.text(3.15, 3.1, '단위: V (rms)', fontsize=8.5, color=fs.GRAY, va='top', ha='right')
    fs.save(fig, __file__, 'fig29_09')


# ---------- 그림 29.10 공명 곡선 ----------
def fig10():
    L, C, Vrms = 0.50, 10e-6, 220.0
    f = np.linspace(40, 110, 3000); w = 2 * np.pi * f
    fig, ax = fs.plot_axes(4.4, 2.8)
    for R, col, ls in [(10, fs.VEL, '-'), (30, fs.FORCE, '--'), (100, fs.ACC, '-.')]:
        I = Vrms / np.abs(R + 1j * (w * L - 1 / (w * C)))
        ax.plot(f, I, color=col, ls=ls, lw=1.6, label=rf'$R = {R}\ \Omega$')
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    ax.axvline(f0, color=fs.GRAY, lw=0.7, ls=':')
    # R=30 반치폭 표시 (전력 절반 ↔ 전류 1/√2)
    R = 30; Imax = Vrms / R; df = R / (2 * np.pi * L)
    fl = np.sqrt((R / (4 * np.pi * L)) ** 2 + f0 ** 2) - R / (4 * np.pi * L); fh = fl + df
    ax.annotate('', xy=(fh, Imax / np.sqrt(2)), xytext=(fl, Imax / np.sqrt(2)),
                arrowprops=dict(arrowstyle='<->', color=fs.FORCE, lw=0.9))
    ax.text(fh + 6, Imax / np.sqrt(2) + 2.5, r'$\Delta f = R/2\pi L = 9.55$ Hz' + '\n' + r'($R = 30\ \Omega$)', fontsize=8.5,
            color=fs.FORCE, va='center', bbox=dict(fc='white', ec='none', pad=1))
    ax.text(f0 + 1.2, 17, r'$f_0 = 71.2$ Hz', fontsize=8.5, color=fs.GRAY)
    ax.set_xlabel(r'구동 진동수 $f$ (Hz)'); ax.set_ylabel(r'$I_{\rm rms}$ (A)')
    ax.set_xlim(40, 110); ax.set_ylim(0, 23.5)
    ax.legend(fontsize=8.5, loc='upper left', frameon=False)
    fs.save(fig, __file__, 'fig29_10')


# ---------- 그림 29.11 RC 저역 통과 필터 ----------
def fig11():
    fig = plt.figure(figsize=(5.6, 2.4))
    ax = fig.add_axes([0.0, 0.1, 0.38, 0.8])
    d = sd.Drawing(canvas=ax)
    d += elm.Dot(open=True).label(r'$\tilde{V}_{\rm in}$', loc='left')
    d += elm.Resistor().right().label(r'$R$', loc='top')
    d += elm.Dot()
    d.push()
    d += elm.Line().right(1.2)
    d += elm.Dot(open=True).label(r'$\tilde{V}_{\rm out}$', loc='right')
    d.pop()
    d += (c := elm.Capacitor().down().label(r'$C$', loc='bottom', ofst=0.2))
    d += elm.Dot()
    d.push(); d += elm.Line().right(1.2); d += elm.Dot(open=True); d.pop()
    d += elm.Line().left(3)
    d += elm.Dot(open=True)
    finish(ax, d, padx=0.9, pady=0.3)
    bx = fig.add_axes([0.5, 0.2, 0.47, 0.72]); graph_ax(bx)
    x = np.logspace(-2, 2, 400)
    H = 1 / np.sqrt(1 + x ** 2)
    bx.loglog(x, H, color=fs.VEL, lw=1.8, label=r'$|H|$')
    bx.loglog(x[x > 1], 1 / x[x > 1], color=fs.GRAY, lw=0.8, ls='--')
    bx.axvline(1, color=fs.GRAY, lw=0.7, ls=':')
    bx.plot(1, 1 / np.sqrt(2), 'o', color=fs.FORCE, ms=4)
    bx.text(1.3, 0.75, r'$1/\sqrt{2}$ ($-3$ dB)', fontsize=8.5, color=fs.FORCE)
    bx.text(14, 0.13, r'$\approx \omega_c/\omega$', fontsize=8.5, color=fs.GRAY)
    bx.set_xlabel(r'$\omega/\omega_c$'); bx.set_ylabel(r'$|H|$')
    bx.set_ylim(5e-3, 1.6)
    fs.save(fig, __file__, 'fig29_11')


# ---------- 그림 29.12 순간 전력 (예제 29.4) ----------
def fig12():
    Em = 220 * np.sqrt(2); I = 1.745 * np.sqrt(2); phi = np.radians(-37.5)
    w = 2 * np.pi * 60
    t = np.linspace(0, 2 / 60, 600); tm = t * 1e3
    e = Em * np.sin(w * t); i = I * np.sin(w * t - phi); p = e * i
    fig, axs = plt.subplots(2, 1, figsize=(4.4, 3.3), sharex=True)
    for a in axs: graph_ax(a)
    a = axs[0]
    a.plot(tm, e, color=F, lw=1.6, label=r'$\mathcal{E}$ (V)')
    a.plot(tm, i * 100, color=CI, lw=1.6, ls='--', label=r'$i$ (×0.01 A)')
    a.axhline(0, color=fs.BLACK, lw=0.6)
    a.set_ylim(-380, 380); a.legend(fontsize=8.5, loc='lower left', frameon=False, ncol=2)
    a = axs[1]
    a.plot(tm, p, color=fs.BLACK, lw=1.6, label=r'$p = \mathcal{E}i$')
    a.fill_between(tm, p, 0, where=p < 0, color=fs.FORCE, alpha=0.3, lw=0)
    a.axhline(305, color=fs.ACC, lw=1.2, ls='--')
    a.text(33.0, 720, r'$P_{\rm avg} = 305$ W', fontsize=8.5, color=fs.ACC, ha='right', va='bottom',
           bbox=dict(fc='white', ec='none', pad=1))
    a.axhline(0, color=fs.BLACK, lw=0.6)
    a.set_ylabel('전력 (W)'); a.set_xlabel(r'$t$ (ms)'); a.set_xlim(0, 2000 / 60)
    a.set_ylim(-350, 950)
    a.text(1.0, -300, '음수: 에너지가 전원으로 되돌아감', fontsize=8, color=fs.FORCE)
    fig.subplots_adjust(hspace=0.1)
    fs.save(fig, __file__, 'fig29_12')


# ---------- 그림 29.13 역률 개선 (예제 29.6) ----------
def fig13():
    fig, ax = fs.canvas(3.4, 3.0, xlim=(-0.9, 3.6), ylim=(-2.25, 1.6))
    s = 0.3
    phasor(ax, (0, 0), (3.0, 0), F, lw=1.4, label=r'$\tilde{V}$', loff=(0.05, 0.18), fontsize=11)
    phasor(ax, (0, 0), (8 * s, -6 * s), CL, lw=2.2, label=r'전동기 $I = 10$ A', loff=(-0.1, -0.22), fontsize=9)
    ax.plot([8 * s, 8 * s], [0, -6 * s], color=fs.GRAY, lw=0.7, ls=':')
    phasor(ax, (0, 0), (8 * s, 0), fs.ACC, lw=2.6, label=None)
    ax.text(4 * s, 0.12, r'$I\cos\phi = 8.0$ A', fontsize=8.5, color=fs.ACC, ha='center', va='bottom')
    phasor(ax, (8 * s, -6 * s), (8 * s, 0), CC, lw=1.8, ls='--', label=None)
    ax.text(8 * s + 0.1, -3 * s, r'$I_C = 6.0$ A' + '\n(축전기)', fontsize=8.5, color=CC, va='center')
    phasor(ax, (0, 0), (0, 6 * s), CC, lw=1.8, label=r'$I_C$', loff=(-0.25, 0), fontsize=10)
    fs.angle_arc(ax, (0, 0), 0.6, np.degrees(np.arctan2(-6, 8)), 0, r'$\phi$', fontsize=10, tr=0.8)
    ax.add_patch(Circle((0, 0), 0.04, color=fs.BLACK, zorder=8))
    ax.text(3.5, 1.5, r'$\cos\phi = 0.80$ (뒤짐)', fontsize=8.5, va='top', ha='right')
    fs.save(fig, __file__, 'fig29_13')


# ---------- 그림 29.14 변압기 ----------
def fig14():
    fig, ax = fs.canvas(4.4, 2.6, xlim=(-2.4, 2.6), ylim=(-1.5, 1.5))
    # 철심
    ax.add_patch(Rectangle((-1.3, -1.2), 2.6, 2.4, fc='#c9ced6', ec=fs.BLACK, lw=1.0))
    ax.add_patch(Rectangle((-0.8, -0.7), 1.6, 1.4, fc='white', ec=fs.BLACK, lw=1.0))
    # 선속 고리
    xs = [-1.05, 1.05, 1.05, -1.05, -1.05]; ys = [0.95, 0.95, -0.95, -0.95, 0.95]
    ax.plot(xs, ys, color=F, lw=1.2, ls='--')
    for p, d in [((0, 0.95), (1, 0)), ((1.05, 0), (0, -1)), ((0, -0.95), (-1, 0)), ((-1.05, 0.3), (0, 1))]:
        tip(ax, p, d, color=F, ms=10)
    ax.text(0, 1.02, r'$\Phi_B$', fontsize=10, color=F, ha='center', va='bottom')
    # 코일
    def coil(xc, n, label):
        ys_ = np.linspace(-0.5, 0.5, n)
        for y in ys_:
            ax.add_patch(Arc((xc, y), 0.75, 0.16, theta1=180, theta2=360, color=fs.ORANGE, lw=1.6, zorder=5))
        return ys_
    yp = coil(-1.05, 6, 'p'); ys_ = coil(1.05, 3, 's')
    for x0, x1, yy in [(-1.42, -2.0, yp), (1.42, 2.0, ys_)]:
        ax.plot([x0, x1], [yy[-1], yy[-1]], color=fs.ORANGE, lw=1.4)
        ax.plot([x0, x1], [yy[0], yy[0]], color=fs.ORANGE, lw=1.4)
    # 1차 교류 전원, 2차 부하
    ax.add_patch(Circle((-2.0, 0), 0.25, fc='white', ec=fs.BLACK, lw=1.1, zorder=6))
    xx = np.linspace(-0.15, 0.15, 50); ax.plot(-2.0 + xx, 0.08 * np.sin(xx / 0.15 * np.pi), color=fs.BLACK, lw=1.0, zorder=7)
    ax.plot([-2.0, -2.0], [yp[-1], 0.25], color=fs.ORANGE, lw=1.4); ax.plot([-2.0, -2.0], [yp[0], -0.25], color=fs.ORANGE, lw=1.4)
    fs.spring(ax, (2.0, ys_[-1]), (2.0, ys_[0]), coils=3, width=0.1, color=fs.BLACK, lw=1.2, lead=0.15)
    ax.text(2.15, 0, r'$R$', fontsize=11, va='center')
    ax.text(-2.3, 0, r'$V_p$', fontsize=10, ha='right', va='center')
    ax.text(-1.05, -1.38, r'1차 $N_p$', fontsize=9, ha='center')
    ax.text(1.05, -1.38, r'2차 $N_s$', fontsize=9, ha='center')
    ax.text(1.55, 0.75, r'$V_s$', fontsize=10)
    ax.text(0, 0, '철심', fontsize=9, ha='center', va='center', color=fs.GRAY)
    fs.save(fig, __file__, 'fig29_14')


if __name__ == '__main__':
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14]:
        f()
