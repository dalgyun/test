"""40장 원자핵, 입자, 우주 그림. python3 figures/ch40/make_figs.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools'))
import figstyle as fs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Wedge, FancyArrowPatch

# ---------------------------------------------------------------- 반경험적 질량 공식(본문 🐍 코드와 같은 계수)
av, as_, ac, aa, ap = 15.8, 18.3, 0.714, 23.2, 12.0


def B(Z, A):
    N = A - Z
    pair = ap / np.sqrt(A) * ((Z % 2 == 0) & (N % 2 == 0)) - ap / np.sqrt(A) * ((Z % 2 == 1) & (N % 2 == 1))
    return av * A - as_ * A ** (2 / 3) - ac * Z * (Z - 1) / A ** (1 / 3) - aa * (A - 2 * Z) ** 2 / A + pair


A_all = np.arange(4, 251)
best = np.array([max(range(1, a), key=lambda z: B(z, a)) for a in A_all])
BA = np.array([B(z, a) / a for z, a in zip(best, A_all)])

# 실측 핵자당 결합 에너지(MeV, 원자 질량 평가 자료의 값)
DATA = {'$^{2}$H': (2, 1.112), '$^{3}$He': (3, 2.573), '$^{4}$He': (4, 7.074), '$^{6}$Li': (6, 5.332),
        '$^{7}$Li': (7, 5.606), '$^{9}$Be': (9, 6.463), '$^{12}$C': (12, 7.680), '$^{14}$N': (14, 7.476),
        '$^{16}$O': (16, 7.976), '$^{20}$Ne': (20, 8.032), '$^{24}$Mg': (24, 8.261), '$^{28}$Si': (28, 8.448),
        '$^{40}$Ca': (40, 8.551), '$^{56}$Fe': (56, 8.790), '$^{62}$Ni': (62, 8.795), '$^{90}$Zr': (90, 8.710),
        '$^{120}$Sn': (120, 8.505), '$^{208}$Pb': (208, 7.868), '$^{235}$U': (235, 7.591), '$^{238}$U': (238, 7.570)}


def style(a):
    a.grid(True, lw=0.4, color='#d0d0d0'); a.tick_params(labelsize=8)
    for s in ('top', 'right'):
        a.spines[s].set_visible(False)


# ---------------------------------------------------------------- 그림 40.1 결합 에너지 곡선
def fig01():
    fig, ax = fs.plot_axes(5.0, 3.0)
    ax.plot(A_all, BA, color=fs.VEL, lw=1.3, label='반경험적 질량 공식')
    xs = [v[0] for v in DATA.values()]; ys = [v[1] for v in DATA.values()]
    ax.plot(xs, ys, 'o', color=fs.FORCE, ms=3.5, label='실측값', zorder=5)
    lab = {'$^{2}$H': (2, 1.112, 9, 0.9), '$^{4}$He': (4, 7.074, 22, 6.6), '$^{6}$Li': (6, 5.332, 13, 4.9),
           '$^{56}$Fe': (56, 8.790, 50, 9.15), '$^{238}$U': (238, 7.570, 222, 8.0)}
    for k, (x, y, tx, ty) in lab.items():
        ax.annotate(k, xy=(x, y), xytext=(tx, ty), fontsize=8, color=fs.FORCE,
                    arrowprops=dict(arrowstyle='-', lw=0.5, color=fs.FORCE) if k in ('$^{4}$He', '$^{6}$Li') else None)
    ax.annotate('', xy=(42, 6.0), xytext=(18, 2.0), arrowprops=dict(arrowstyle='-|>', color=fs.ACC, lw=1.4))
    ax.text(33, 2.9, '핵융합', color=fs.ACC, fontsize=9)
    ax.annotate('', xy=(125, 8.2), xytext=(232, 7.35), arrowprops=dict(arrowstyle='-|>', color=fs.ORANGE, lw=1.4))
    ax.text(170, 6.85, '핵분열', color=fs.ORANGE, fontsize=9)
    ax.set_xlim(0, 250); ax.set_ylim(0, 9.6)
    ax.set_xlabel('질량수 $A$', fontsize=9); ax.set_ylabel('$B/A$ (MeV)', fontsize=9)
    ax.legend(fontsize=8, loc='lower right', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig40_01')


# ---------------------------------------------------------------- 그림 40.2 N-Z 안정선
def fig02():
    fig, ax = fs.plot_axes(4.0, 3.3)
    Z = best; N = A_all - best
    ax.plot([0, 100], [0, 100], '--', color=fs.GRAY, lw=0.9)
    ax.text(70, 64, '$N = Z$', fontsize=9, color=fs.GRAY, rotation=40)
    ax.plot(Z, N, '.', color=fs.VEL, ms=2.5, label='각 $A$에서 $B$가 가장 큰 핵(공식)')
    for name, z, n in (('$^{56}$Fe', 26, 30), ('$^{208}$Pb', 82, 126), ('$^{238}$U', 92, 146), ('$^{16}$O', 8, 8)):
        ax.plot(z, n, 'o', color=fs.FORCE, ms=4, zorder=5)
        if z < 10:
            ax.text(z + 3, n - 4, name, fontsize=8, color=fs.FORCE, ha='left')
        else:
            ax.text(z - 3, n + 5, name, fontsize=8, color=fs.FORCE, ha='right')
    # 붕괴 방향 화살표(범례)
    o = np.array([27, 120]); s = 7
    for d, lab, c in (((-2, -2), r'$\alpha$', fs.FORCE), ((1, -1), r'$\beta^-$', fs.VEL), ((-1, 1), r'$\beta^+$, EC', fs.ACC)):
        q = o + s * np.array(d)
        ax.annotate('', xy=q, xytext=o, arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3))
        ax.text(q[0] + (1.5 if d[0] > 0 else -1.5), q[1] + (-3 if d[1] < 0 else 3), lab, color=c, fontsize=8.5,
                ha='left' if d[0] > 0 else 'right', va='center')
    ax.text(o[0], o[1] + 16, '붕괴의 방향', fontsize=8, ha='center')
    ax.plot(*o, 'o', color=fs.BLACK, ms=3)
    ax.text(60, 25, '중성자 부족:\n$\\beta^+$, 전자 포획', fontsize=8, color=fs.ACC, ha='center')
    ax.text(28, 80, '중성자 과다:\n$\\beta^-$', fontsize=8, color=fs.VEL, ha='center')
    ax.set_xlim(0, 100); ax.set_ylim(0, 155)
    ax.set_xlabel('양성자 수 $Z$', fontsize=9); ax.set_ylabel('중성자 수 $N$', fontsize=9)
    ax.legend(fontsize=7.5, loc='lower right', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig40_02')


# ---------------------------------------------------------------- 그림 40.3 알파 붕괴의 쿨롱 장벽
def fig03():
    fig, ax = fs.plot_axes(4.4, 2.8)
    ax.grid(False)
    ke2 = 1.44  # MeV fm
    R = 9.3; Q = 4.27
    b = 2 * 90 * ke2 / Q
    r = np.linspace(R, 80, 600)
    U = 2 * 90 * ke2 / r
    ax.plot(r, U, color=fs.BLACK, lw=1.4)
    ax.plot([0, R, R], [-15, -15, 2 * 90 * ke2 / R], color=fs.BLACK, lw=1.4)
    ax.axhline(0, color=fs.GRAY, lw=0.6)
    ax.plot([0, R], [Q, Q], color=fs.FORCE, lw=1.4)
    ax.plot([b, 80], [Q, Q], color=fs.FORCE, lw=1.4)
    rr = np.linspace(R, b, 200)
    ax.fill_between(rr, Q, 2 * 90 * ke2 / rr, color=fs.SURF, alpha=0.5, lw=0)
    ax.text(18, 12, '장벽\n(고전적 금지 영역)', fontsize=8, ha='left')
    ax.text(70, Q + 2.0, r'$Q = 4.27$ MeV', color=fs.FORCE, fontsize=8.5, ha='center')
    ax.annotate('', xy=(b + 8, Q), xytext=(R, Q),
                arrowprops=dict(arrowstyle='-|>', color=fs.FORCE, lw=1.0, ls='--'))
    ax.text((R + b) / 2 - 4, Q + 1.0, '터널링', color=fs.FORCE, fontsize=8.5, ha='center')
    ax.text(R + 0.8, 2 * 90 * ke2 / R, f'≈ {2*90*ke2/R:.0f} MeV', fontsize=8, va='center')
    ax.plot([b, b], [-15, Q], color=fs.GRAY, lw=0.6, ls='--')
    ax.set_xticks([0, R, b]); ax.set_xticklabels(['0', r'$R$' '\n9.3', r'$b$' '\n61'], fontsize=8)
    ax.text(4.6, -10, '핵\n안쪽', fontsize=8, ha='center')
    ax.set_xlim(0, 80); ax.set_ylim(-16, 32)
    ax.set_xlabel('중심에서의 거리 $r$ (fm)', fontsize=9); ax.set_ylabel('알파 입자의 퍼텐셜 에너지 (MeV)', fontsize=8)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig40_03')


# ---------------------------------------------------------------- 그림 40.4 탄소-14 붕괴 곡선
def fig04():
    th = 5730.0
    t = np.linspace(0, 30000, 600)
    fig, ax = fs.plot_axes(4.4, 2.7)
    ax.plot(t, np.exp(-np.log(2) * t / th), color=fs.VEL)
    for n in range(1, 5):
        tn = n * th; yn = 0.5 ** n
        ax.plot([tn, tn, 0], [0, yn, yn], color=fs.GRAY, lw=0.6, ls=':')
        ax.text(tn, yn + 0.03, f'$1/{2**n}$', fontsize=7.5, ha='left', color=fs.GRAY)
    tx = th / np.log(2) * np.log(1 / 0.30)
    ax.plot([0, tx, tx], [0.30, 0.30, 0], color=fs.FORCE, lw=0.9, ls='--')
    ax.plot(tx, 0.30, 'o', color=fs.FORCE, ms=4)
    ax.text(tx + 600, 0.38, f'예제 40.4: 30% → {tx:.0f}년', fontsize=8, color=fs.FORCE)
    ax.set_xticks([0, th, 2 * th, 3 * th, 4 * th, 5 * th])
    ax.set_xticklabels(['0', '5730', '11460', '17190', '22920', '28650'], fontsize=7.5)
    ax.set_xlim(0, 30000); ax.set_ylim(0, 1.05)
    ax.set_xlabel('죽은 뒤 지난 시간 $t$ (년)', fontsize=9); ax.set_ylabel(r'$\mathcal{A}/\mathcal{A}_0 = N/N_0$', fontsize=9)
    ax.tick_params(axis='y', labelsize=8)
    fs.save(fig, __file__, 'fig40_04')


# ---------------------------------------------------------------- 핵 그림 도우미
def nucleus(ax, c, A, label, color='#e8c39e', fontsize=8, scale=0.11):
    r = scale * A ** (1 / 3)
    ax.add_patch(Circle(c, r, fc=color, ec=fs.BLACK, lw=0.8, zorder=4))
    ax.text(c[0], c[1], label, ha='center', va='center', fontsize=fontsize, zorder=5)
    return r


def neutron(ax, c, r=0.09):
    ax.add_patch(Circle(c, r, fc='#bfc7cf', ec=fs.BLACK, lw=0.6, zorder=6))


# ---------------------------------------------------------------- 그림 40.5 핵분열과 연쇄 반응
def fig05():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.4, 3.4), gridspec_kw={'height_ratios': [1, 1.05]})
    for a in (a1, a2):
        a.set_aspect('equal'); a.axis('off')
    a1.set_xlim(-0.3, 8.6); a1.set_ylim(-1.2, 1.15)
    neutron(a1, (0.1, 0)); a1.text(0.1, -0.3, '느린\n중성자', fontsize=7, ha='center', va='top')
    fs.arrow(a1, (0.25, 0), (0.95, 0), lw=1.0, ms=8)
    nucleus(a1, (1.65, 0), 235, '$^{235}$U')
    fs.arrow(a1, (2.45, 0), (3.0, 0), lw=1.0, ms=8)
    a1.add_patch(matplotlib_ellipse((3.85, 0), 1.45, 1.05))
    a1.text(3.85, 0, '$^{236}$U*', ha='center', va='center', fontsize=8, zorder=5)
    a1.text(3.85, -0.72, '들뜬 상태', fontsize=7, ha='center')
    fs.arrow(a1, (4.7, 0), (5.25, 0), lw=1.0, ms=8)
    nucleus(a1, (5.95, 0.52), 141, '$^{141}$Ba', color='#f2d7a6')
    nucleus(a1, (6.1, -0.62), 92, '$^{92}$Kr', color='#f2d7a6')
    for i, y in enumerate((0.55, 0.0, -0.55)):
        neutron(a1, (7.2 + 0.3 * (i == 1), y))
        fs.arrow(a1, (7.35 + 0.3 * (i == 1), y), (7.75 + 0.3 * (i == 1), y * 1.25), lw=0.8, ms=6)
    a1.text(7.45, -0.95, '중성자 3개', fontsize=7, ha='center')
    a1.text(6.9, 0.8, r'$\sim 200$ MeV', fontsize=8, color=fs.FORCE, ha='center')
    a1.set_title('(가) $n + {}^{235}$U → $^{141}$Ba + $^{92}$Kr + $3n$', fontsize=9)
    # (나) k = 1 연쇄 반응
    a2.set_xlim(-0.3, 8.6); a2.set_ylim(-1.1, 1.0)
    xs = [0.6, 3.1, 5.6]
    neutron(a2, (-0.1, 0)); fs.arrow(a2, (0.03, 0), (0.33, 0), lw=0.9, ms=6)
    for i, x in enumerate(xs):
        nucleus(a2, (x, 0), 235, 'U', fontsize=7, scale=0.07)
        # 다음 분열로 가는 중성자
        neutron(a2, (x + 0.65, 0)); fs.arrow(a2, (x + 0.78, 0), (x + 2.1, 0), lw=0.9, ms=6, color=fs.ACC)
        # 흡수되는 중성자
        neutron(a2, (x + 0.55, 0.45)); fs.arrow(a2, (x + 0.65, 0.5), (x + 1.25, 0.72), lw=0.8, ms=6)
        a2.add_patch(Rectangle((x + 1.3, 0.6), 0.5, 0.22, fc='#555555', ec='none'))
        # 새어 나가는 중성자
        neutron(a2, (x + 0.55, -0.45)); fs.arrow(a2, (x + 0.65, -0.5), (x + 1.35, -0.85), lw=0.8, ms=6, ls='--')
    a2.text(1.95 + 0.0, 0.92, '제어봉 등에 흡수', fontsize=7, ha='center')
    a2.text(1.95, -1.08, '밖으로 새어 나감', fontsize=7, ha='center')
    a2.text(8.25, 0.05, '…', fontsize=12, ha='center', va='center')
    a2.text(7.75, -0.35, '다음 세대로\n1개씩', fontsize=7, color=fs.ACC, ha='center', va='top')
    a2.set_title('(나) 임계 상태($k = 1$)의 연쇄 반응', fontsize=9)
    fig.tight_layout(h_pad=0.2)
    fs.save(fig, __file__, 'fig40_05')


def matplotlib_ellipse(c, w, h):
    from matplotlib.patches import Ellipse
    return Ellipse(c, w, h, fc='#e8c39e', ec=fs.BLACK, lw=0.8, zorder=4)


# ---------------------------------------------------------------- 그림 40.6 D-T 융합과 가모프 봉우리
def fig06():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.6), gridspec_kw={'width_ratios': [1, 1.25]})
    a1.set_aspect('equal'); a1.axis('off'); a1.set_xlim(-0.2, 4.2); a1.set_ylim(-1.4, 1.6)
    nucleus(a1, (0.35, 0.55), 2, 'D', color='#cfe0f3', scale=0.25)
    nucleus(a1, (0.35, -0.55), 3, 'T', color='#cfe0f3', scale=0.25)
    fs.arrow(a1, (0.75, 0.4), (1.45, 0.08), lw=0.9, ms=7); fs.arrow(a1, (0.75, -0.4), (1.45, -0.08), lw=0.9, ms=7)
    a1.add_patch(Circle((1.85, 0), 0.38, fc=fs.SURF, ec=fs.BLACK, lw=0.8, alpha=0.8))
    a1.text(1.85, 0, '$^5$He*', ha='center', va='center', fontsize=7.5)
    nucleus(a1, (2.9, 0.75), 4, r'$\alpha$', color='#e8c39e', scale=0.25)
    neutron(a1, (2.9, -0.75), r=0.15)
    a1.text(2.9, -0.75, 'n', ha='center', va='center', fontsize=7.5, zorder=7)
    fs.arrow(a1, (2.25, 0.2), (2.6, 0.55), lw=0.9, ms=7); fs.arrow(a1, (2.25, -0.2), (2.65, -0.6), lw=0.9, ms=7)
    fs.arrow(a1, (3.25, 0.95), (3.85, 1.25), color=fs.VEL, lw=1.2, ms=8)
    fs.arrow(a1, (3.1, -0.95), (4.0, -1.35), color=fs.VEL, lw=1.2, ms=8)
    a1.text(2.9, 1.3, '3.5 MeV', fontsize=8, ha='center', color=fs.VEL)
    a1.text(2.6, -1.35, '14.1 MeV', fontsize=8, ha='center', color=fs.VEL)
    a1.set_title('(가) D–T 반응, $Q = 17.6$ MeV', fontsize=9)
    # (나) 가모프 봉우리
    style(a2)
    kT = 10.0                       # keV
    mu = 2.014102 * 3.016049 / (2.014102 + 3.016049) * 931494.0   # keV
    EG = 2 * mu * (np.pi / 137.036) ** 2                            # keV
    E = np.linspace(0.5, 120, 1200)
    mb = np.exp(-E / kT)
    tun = np.exp(-np.sqrt(EG / E))
    prod = mb * tun
    a2.semilogy(E, mb, color=fs.VEL, label=r'$e^{-E/k_BT}$ (분포 꼬리)')
    a2.semilogy(E, tun, color=fs.ACC, label=r'$e^{-\sqrt{E_G/E}}$ (터널링)')
    a2.semilogy(E, prod, color=fs.FORCE, lw=1.8, label='곱(반응에 기여)')
    E0 = (EG * kT ** 2 / 4) ** (1 / 3)
    a2.axvline(E0, color=fs.FORCE, lw=0.6, ls=':')
    a2.text(E0 + 2, 3e-9, f'≈ {E0:.0f} keV', color=fs.FORCE, fontsize=7.5)
    a2.axvline(kT, color=fs.GRAY, lw=0.6, ls=':')
    a2.text(kT + 1.5, 2e-11, r'$k_BT$', fontsize=8, color=fs.GRAY)
    a2.set_ylim(1e-12, 2); a2.set_xlim(0, 120)
    a2.set_xlabel('충돌 에너지 $E$ (keV)', fontsize=9)
    a2.legend(fontsize=6.8, loc='lower right', frameon=False)
    a2.set_title(r'(나) $k_BT = 10$ keV 플라스마', fontsize=9)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig40_06')


# ---------------------------------------------------------------- 그림 40.9 Mo-Tc 발생기 (본문 코드)
def fig07():
    T_Mo, T_Tc = 65.94, 6.007
    lM, lT = np.log(2) / T_Mo, np.log(2) / T_Tc
    f = 0.88
    t = np.linspace(0, 72, 7201)
    A_Mo = np.exp(-lM * t)
    A_Tc = f * lT / (lT - lM) * (np.exp(-lM * t) - np.exp(-lT * t))
    i = np.argmax(A_Tc)
    fig, ax = fs.plot_axes(4.2, 2.6)
    ax.plot(t, A_Mo, color=fs.VEL, label=r'$^{99}$Mo')
    ax.plot(t, A_Tc, color=fs.FORCE, label=r'$^{99\mathrm{m}}$Tc')
    ax.plot(t, 0.968 * A_Mo, color=fs.GRAY, ls=':', lw=1.0, label=r'과도 평형 $0.968\,\mathcal{A}_{\mathrm{Mo}}$')
    ax.plot(t[i], A_Tc[i], 'o', color=fs.FORCE, ms=4)
    ax.annotate(f'최대 {t[i]:.1f} h', xy=(t[i], A_Tc[i]), xytext=(30, 0.5), fontsize=8,
                arrowprops=dict(arrowstyle='->', lw=0.6))
    ax.set_xlim(0, 72); ax.set_ylim(0, 1.05); ax.set_xticks(range(0, 73, 12))
    ax.set_xlabel('Tc를 뽑아낸 뒤 시간 $t$ (h)', fontsize=9); ax.set_ylabel('방사능 (처음 Mo = 1)', fontsize=9)
    ax.legend(fontsize=7.5, loc='lower right', frameon=False)
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig40_09')


# ---------------------------------------------------------------- 그림 40.7 투과력과 반가층
def fig08():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.5), gridspec_kw={'width_ratios': [1.25, 1]})
    a1.set_xlim(-0.3, 5.2); a1.set_ylim(-0.3, 3.0); a1.set_aspect('equal'); a1.axis('off')
    a1.add_patch(Rectangle((0, 0.2), 0.45, 2.3, fc='#f0e6a0', ec=fs.BLACK, lw=0.8))
    a1.text(0.22, 1.35, '선원', rotation=90, ha='center', va='center', fontsize=8)
    for x0, w, fc, lab in ((1.6, 0.06, '#ffffff', '종이'), (2.7, 0.3, '#c9d6e3', '플라스틱\n수 mm'),
                           (3.9, 0.55, '#8c8c8c', '납·\n콘크리트')):
        a1.add_patch(Rectangle((x0, 0.0), w, 2.7, fc=fc, ec=fs.BLACK, lw=0.8))
        a1.text(x0 + w / 2, -0.08, lab, ha='center', va='top', fontsize=7.5)
    ys = (2.15, 1.35, 0.55)
    fs.arrow(a1, (0.5, ys[0]), (1.58, ys[0]), color=fs.FORCE, lw=1.6, ms=9)
    a1.text(0.95, ys[0] + 0.15, r'$\alpha$', color=fs.FORCE, fontsize=10)
    fs.arrow(a1, (0.5, ys[1]), (2.68, ys[1]), color=fs.VEL, lw=1.6, ms=9)
    a1.text(0.95, ys[1] + 0.15, r'$\beta$', color=fs.VEL, fontsize=10)
    a1.plot([0.5, 3.9], [ys[2], ys[2]], color=fs.ACC, lw=1.6)
    fs.arrow(a1, (4.45, ys[2]), (5.1, ys[2]), color=fs.ACC, lw=0.7, ms=6)
    a1.text(0.95, ys[2] + 0.15, r'$\gamma$', color=fs.ACC, fontsize=10)
    a1.text(4.75, ys[2] + 0.15, '약해짐', color=fs.ACC, fontsize=7, ha='center')
    a1.set_title('(가) 방사선의 투과력', fontsize=9)
    # (나) 반가층
    style(a2)
    x = np.linspace(0, 2.4, 300)
    hvl = 0.3
    a2.semilogy(x, 0.5 ** (x / hvl), color=fs.ACC)
    for n in range(1, 8):
        a2.plot(n * hvl, 0.5 ** n, 'o', color=fs.ACC, ms=2.5)
    a2.axhline(0.01, color=fs.FORCE, lw=0.8, ls='--')
    a2.text(0.05, 0.0125, '1/100', color=fs.FORCE, fontsize=7.5)
    a2.plot([7 * hvl] * 2, [1e-3, 0.5 ** 7], color=fs.FORCE, lw=0.8, ls=':')
    a2.text(7 * hvl - 0.03, 2e-3, '반가층 7개\n= 2.1 mm', fontsize=7.5, color=fs.FORCE, ha='right')
    a2.set_xlim(0, 2.4); a2.set_ylim(1e-3, 1.2)
    a2.set_xlabel('납 두께 $x$ (mm)', fontsize=9); a2.set_ylabel('$I/I_0$', fontsize=9)
    a2.set_title('(나) $x_{1/2} = 0.3$ mm (140 keV)', fontsize=9)
    fig.tight_layout(w_pad=0.6)
    fs.save(fig, __file__, 'fig40_07')


# ---------------------------------------------------------------- 그림 40.8 PET
def fig09():
    fig, ax = fs.canvas(3.2, 3.0, xlim=(-1.75, 1.75), ylim=(-1.6, 1.65))
    n = 36
    for k in range(n):
        th = 2 * np.pi * k / n
        c, s = np.cos(th), np.sin(th)
        w, h = 0.13, 0.26
        pts = np.array([[-h / 2, -w / 2], [h / 2, -w / 2], [h / 2, w / 2], [-h / 2, w / 2]])
        R = np.array([[c, -s], [s, c]])
        pts = pts @ R.T + 1.35 * np.array([c, s])
        ax.add_patch(plt.Polygon(pts, fc='#dfe6ee', ec=fs.BLACK, lw=0.5))
    ax.add_patch(plt.matplotlib.patches.Ellipse((0, -0.05), 1.3, 1.05, fc='#f6e0d6', ec=fs.GRAY, lw=0.8))
    p = np.array([0.25, 0.15]); ang = np.radians(28)
    u = np.array([np.cos(ang), np.sin(ang)])
    # 직선과 원의 교점
    bq = p @ u; cq = p @ p - 1.22 ** 2
    t1 = -bq + np.sqrt(bq ** 2 - cq); t2 = -bq - np.sqrt(bq ** 2 - cq)
    q1, q2 = p + t1 * u, p + t2 * u
    ax.plot([q2[0], q1[0]], [q2[1], q1[1]], color=fs.ORANGE, lw=0.6, ls=':')
    for q in (q1, q2):
        d = q - p; L = np.linalg.norm(d); v = d / L; nrm = np.array([-v[1], v[0]])
        tt = np.linspace(0.12, L - 0.08, 200)
        pts = p + np.outer(tt, v) + np.outer(0.04 * np.sin(2 * np.pi * tt / 0.12), nrm)
        ax.plot(pts[:, 0], pts[:, 1], color=fs.ORANGE, lw=1.1)
        ax.add_patch(FancyArrowPatch(p + (L - 0.12) * v, q, arrowstyle='-|>', mutation_scale=9, color=fs.ORANGE, lw=0))
    for q in (q1, q2):
        k = int(round((np.arctan2(q[1], q[0]) % (2 * np.pi)) / (2 * np.pi) * n)) % n
        th = 2 * np.pi * k / n
        ax.add_patch(Circle(1.35 * np.array([np.cos(th), np.sin(th)]), 0.1, fc=fs.FORCE, ec='none', alpha=0.6, zorder=7))
    ax.add_patch(Circle(p, 0.06, fc=fs.FORCE, ec='none', zorder=8))
    ax.text(p[0] - 0.05, p[1] - 0.17, '소멸', fontsize=8, ha='center', va='top')
    ax.text(0.5, 0.58, '511 keV', fontsize=8, color=fs.ORANGE, ha='center')
    ax.text(-0.62, -0.62, '511 keV', fontsize=8, color=fs.ORANGE, ha='center')
    ax.text(0, 1.55, '검출기 고리', fontsize=8, ha='center')
    ax.text(-0.25, 0.2, r'$e^+ + e^-$', fontsize=8, ha='center')
    fs.save(fig, __file__, 'fig40_08')


# ---------------------------------------------------------------- 그림 40.10 표준모형 입자
def fig10():
    fig, ax = fs.canvas(5.5, 3.3, xlim=(-0.65, 5.75), ylim=(-0.35, 4.55))
    QC, LC, GC, HC = '#e3ecf8', '#e5f3e8', '#fbe5dc', '#fbf1cc'
    cells = [
        # (열, 행, 기호, 이름, 질량, 전하, 색)
        (0, 3, 'u', '위', '2.2 MeV', r'$+\frac{2}{3}$', QC), (1, 3, 'c', '맵시', '1.27 GeV', r'$+\frac{2}{3}$', QC),
        (2, 3, 't', '꼭대기', '173 GeV', r'$+\frac{2}{3}$', QC),
        (0, 2, 'd', '아래', '4.7 MeV', r'$-\frac{1}{3}$', QC), (1, 2, 's', '기묘', '93 MeV', r'$-\frac{1}{3}$', QC),
        (2, 2, 'b', '바닥', '4.18 GeV', r'$-\frac{1}{3}$', QC),
        (0, 1, 'e', '전자', '0.511 MeV', '$-1$', LC), (1, 1, r'\mu', '뮤온', '105.7 MeV', '$-1$', LC),
        (2, 1, r'\tau', '타우', '1.777 GeV', '$-1$', LC),
        (0, 0, r'\nu_e', '전자 중성미자', '< 1 eV', '0', LC), (1, 0, r'\nu_\mu', '뮤온 중성미자', '< 1 eV', '0', LC),
        (2, 0, r'\nu_\tau', '타우 중성미자', '< 1 eV', '0', LC),
        (3.25, 3, 'g', '글루온', '0', '0', GC), (3.25, 2, r'\gamma', '광자', '0', '0', GC),
        (3.25, 1, 'Z^0', 'Z 보손', '91.2 GeV', '0', GC), (3.25, 0, r'W^\pm', 'W 보손', '80.4 GeV', r'$\pm1$', GC),
        (4.5, 3, 'H', '힉스', '125 GeV', '0', HC),
    ]
    for (c, r, sym, name, m, q, col) in cells:
        ax.add_patch(FancyBboxPatch((c + 0.05, r + 0.05), 0.9, 0.9, boxstyle='round,pad=0,rounding_size=0.08',
                                    fc=col, ec=fs.GRAY, lw=0.6))
        ax.text(c + 0.5, r + 0.55, f'${sym}$', ha='center', va='center', fontsize=14)
        ax.text(c + 0.5, r + 0.18, name, ha='center', va='center', fontsize=5.6 if len(name) > 4 else 7)
        ax.text(c + 0.5, r + 0.84, m, ha='center', va='center', fontsize=5.8, color='#444444')
        ax.text(c + 0.13, r + 0.55, q, ha='left', va='center', fontsize=6.3, color='#444444')
    for c, t in ((0, '1세대'), (1, '2세대'), (2, '3세대')):
        ax.text(c + 0.5, 4.12, t, ha='center', fontsize=8)
    ax.text(-0.12, 2.5, '쿼크', rotation=90, ha='center', va='center', fontsize=9, color=fs.VEL)
    ax.text(-0.12, 0.5 + 0.5, '렙톤', rotation=90, ha='center', va='center', fontsize=9, color=fs.ACC)
    ax.plot([-0.38, -0.38], [2.08, 3.92], color=fs.VEL, lw=1.2); ax.plot([-0.38, -0.38], [0.08, 1.92], color=fs.ACC, lw=1.2)
    ax.text(3.75, 4.12, '게이지 보손\n(스핀 1)', ha='center', fontsize=7.5, color=fs.FORCE)
    ax.text(5.0, 4.12, '스칼라 보손\n(스핀 0)', ha='center', fontsize=7.5, color=fs.ORANGE)
    ax.text(1.5, 4.42, '페르미온 (스핀 1/2)', ha='center', fontsize=8)
    ax.text(5.0, 1.95, '칸 안의 표시\n위: 질량\n왼쪽: 전하($e$ 단위)', ha='center', va='center', fontsize=6.8,
            color='#444444')
    ax.text(2.6, -0.22, '질량은 $mc^2$ 값(근삿값). 각 페르미온에는 반입자가 있다.', ha='center', fontsize=7, color='#444444')
    fs.save(fig, __file__, 'fig40_10')


# ---------------------------------------------------------------- 그림 40.11 베타 붕괴의 파인만 그림
def fermion(ax, p, q, label=None, lpos=0.5, loff=(0, 0.15), reverse=False, color=fs.BLACK, fontsize=10):
    p, q = np.asarray(p, float), np.asarray(q, float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=1.3)
    a, b = (q, p) if reverse else (p, q)
    m = (p + q) / 2
    d = (b - a) / np.linalg.norm(b - a) * 0.12
    ax.add_patch(FancyArrowPatch(m - d, m + d, arrowstyle='-|>', mutation_scale=10, color=color, lw=0))
    if label:
        x = p + (q - p) * lpos
        ax.text(x[0] + loff[0], x[1] + loff[1], label, fontsize=fontsize, ha='center', va='center', color=color)


def fig11():
    fig, ax = fs.canvas(4.4, 2.9, xlim=(-0.6, 5.4), ylim=(-2.3, 1.75))
    y = [1.2, 0.75, 0.3]
    for yy, (ql, qr) in zip(y, (('u', 'u'), ('d', 'd'), ('d', 'u'))):
        if yy != 0.3:
            fermion(ax, (0, yy), (4.2, yy))
            ax.text(-0.15, yy, ql, ha='right', va='center', fontsize=10); ax.text(4.35, yy, qr, ha='left', va='center', fontsize=10)
    v1 = np.array([2.0, 0.3])
    fermion(ax, (0, 0.3), v1)
    fermion(ax, v1, (4.2, 0.3))
    ax.text(-0.15, 0.3, 'd', ha='right', va='center', fontsize=10); ax.text(4.35, 0.3, 'u', ha='left', va='center', fontsize=10)
    v2 = np.array([3.0, -1.0])
    tt = np.linspace(0, 1, 300)
    d = v2 - v1; L = np.linalg.norm(d); nrm = np.array([-d[1], d[0]]) / L
    pts = v1 + np.outer(tt, d) + np.outer(0.07 * np.sin(2 * np.pi * tt * 7), nrm)
    ax.plot(pts[:, 0], pts[:, 1], color=fs.FIELD, lw=1.3)
    ax.text(2.25, -0.45, r'$W^-$', color=fs.FIELD, fontsize=11, ha='right')
    fermion(ax, v2, (4.6, -0.35), label=r'$e^-$', lpos=1.0, loff=(0.2, 0.05), color=fs.VEL)
    fermion(ax, v2, (4.6, -1.75), label=r'$\bar\nu_e$', lpos=1.0, loff=(0.22, -0.05), color=fs.VEL, reverse=True)
    for v in (v1, v2):
        ax.add_patch(Circle(v, 0.06, color=fs.BLACK, zorder=6))
    ax.add_patch(FancyBboxPatch((-0.5, 0.1), 0.25, 1.3, boxstyle='round,pad=0.02', fc='none', ec=fs.GRAY, lw=0.6))
    ax.text(-0.37, -0.1, '$n$', ha='center', va='top', fontsize=10, color=fs.GRAY)
    ax.add_patch(FancyBboxPatch((4.25, 0.1), 0.25, 1.3, boxstyle='round,pad=0.02', fc='none', ec=fs.GRAY, lw=0.6))
    ax.text(4.75, 0.75, '$p$', ha='left', va='center', fontsize=10, color=fs.GRAY)
    fs.arrow(ax, (0, -2.05), (1.6, -2.05), lw=0.9, ms=8)
    ax.text(0.8, -1.9, '시간', fontsize=8, ha='center', va='bottom')
    fs.save(fig, __file__, 'fig40_11')


# ---------------------------------------------------------------- 그림 40.12 팽창과 허블-르메트르 법칙
def fig12():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.5, 2.6), gridspec_kw={'width_ratios': [1, 1.15]})
    a1.set_aspect('equal'); a1.axis('off'); a1.set_xlim(-2.4, 2.4); a1.set_ylim(-2.9, 2.4)
    gal = 0.8 * np.array([[0, 0], [0.55, 0.1], [1.3, 0.3], [-0.45, 0.45], [-1.25, -0.3], [0.2, -0.6], [0.3, 1.25],
                          [-0.6, -1.2], [1.0, -0.95], [-0.95, 1.0]])
    s = 1.6
    for g in gal:
        a1.plot(*g, 'o', color=fs.GRAY, ms=3.5)
        a1.plot(*(g * s), 'o', color=fs.VEL, ms=4.5)
    ref = gal[0]
    for g in gal[1:]:
        fs.arrow(a1, tuple(g * s), tuple(g * s + 0.45 * (g - ref)), color=fs.FORCE, lw=0.9, ms=7)
    a1.plot(0, 0, '*', color=fs.ORANGE, ms=10, zorder=6)
    a1.text(0.0, -0.42, '우리 은하', fontsize=7, color=fs.ORANGE, ha='center')
    a1.text(0, -2.75, '회색: 이전, 파랑: 나중(모든 거리 1.6배)\n빨강: 후퇴 속도 ∝ 거리', fontsize=6.8, ha='center')
    a1.set_title('(가) 공간의 팽창', fontsize=9)
    style(a2)
    d = np.linspace(0, 250, 100)
    a2.fill_between(d, 67 * d / 1e3, 73 * d / 1e3, color=fs.VEL, alpha=0.15, lw=0, label='$H_0 = 67$–$73$')
    a2.plot(d, 70 * d / 1e3, color=fs.VEL, label='$H_0 = 70$ km/(s·Mpc)')
    for dd, lab in ((100, '예제 40.8'), (200, '연습문제 7')):
        a2.plot(dd, 70 * dd / 1e3, 'o', color=fs.FORCE, ms=4, zorder=5)
        a2.text(dd + 6, 70 * dd / 1e3 - 1.3, lab, fontsize=7.5, color=fs.FORCE)
    a2.set_xlim(0, 250); a2.set_ylim(0, 18)
    a2.set_xlabel('거리 $d$ (Mpc)', fontsize=9); a2.set_ylabel('후퇴 속도 $v$ ($10^3$ km/s)', fontsize=9)
    a2.legend(fontsize=7, loc='upper left', frameon=False)
    a2.set_title('(나) $v = H_0d$', fontsize=9)
    fig.tight_layout(w_pad=0.5)
    fs.save(fig, __file__, 'fig40_12')


# ---------------------------------------------------------------- 그림 40.13 우주 배경 복사의 흑체 스펙트럼
def fig13():
    h, c, k = 6.62607015e-34, 299792458.0, 1.380649e-23
    lam = np.logspace(-7, -1.5, 2000)
    fig, ax = fs.plot_axes(4.6, 2.6)
    for T, col, lab in ((3000, fs.FORCE, '3000 K (빛이 풀려난 때)'), (2.725, fs.VEL, '2.725 K (오늘의 CMB)')):
        with np.errstate(over='ignore'):
            Bl = 1 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1)
        ax.semilogx(lam * 1e3, Bl / Bl.max(), color=col, label=lab)
        lm = 2.897771955e-3 / T
        ax.axvline(lm * 1e3, color=col, lw=0.6, ls=':')
    ax.text(2.8977e-3 / 2.725 * 1e3 * 1.15, 1.02, r'$\lambda_{\max} = 1.06$ mm', fontsize=8, color=fs.VEL)
    ax.text(2.8977e-3 / 3000 * 1e3 * 1.15, 1.02, r'$0.97\ \mu$m', fontsize=8, color=fs.FORCE)
    ax.annotate('', xy=(1.06 * 0.9, 0.5), xytext=(0.97e-3 * 1.4, 0.5),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, color=fs.GRAY))
    ax.text(0.03, 0.55, '파장 약 1100배', fontsize=8, color=fs.GRAY, ha='center')
    ax.set_xlim(1e-4, 30); ax.set_ylim(0, 1.15)
    ax.set_xlabel(r'파장 $\lambda$ (mm)', fontsize=9); ax.set_ylabel(r'$B_\lambda$ (최댓값 = 1)', fontsize=9)
    ax.legend(fontsize=7.5, loc='center', frameon=False, bbox_to_anchor=(0.45, 0.25))
    ax.tick_params(labelsize=8)
    fs.save(fig, __file__, 'fig40_13')


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13):
        f()
