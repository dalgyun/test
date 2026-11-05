"""부록 A 물리 상수와 단위 — 그림 생성 스크립트.

    python3 figures/appA/make_figs.py
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')); import figstyle as fs
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle

S = __file__


# ---------- 그림 A.1 일곱 정의 상수와 기본 단위의 관계 ----------
def figA01():
    fig, ax = fs.canvas(5.4, 2.7, xlim=(-0.2, 14.2), ylim=(-0.9, 6.3))
    consts = [r'$\Delta\nu_{\mathrm{Cs}}$', '$c$', '$h$', '$e$', '$k_B$', '$N_A$', r'$K_{\mathrm{cd}}$']
    units = ['s', 'm', 'kg', 'A', 'K', 'mol', 'cd']
    cols = [fs.FORCE, fs.VEL, fs.ACC, fs.ORANGE, fs.FIELD, fs.GRAY, '#8e6c3a']
    deps = {'s': [0], 'm': [0, 1], 'kg': [0, 1, 2], 'A': [0, 3], 'K': [0, 2, 4], 'mol': [5], 'cd': [0, 2, 6]}
    xs = np.linspace(1.0, 13.0, 7)
    yc, yu = 5.0, 0.6
    for j, u in enumerate(units):
        for i in deps[u]:
            ax.plot([xs[i], xs[j]], [yc - 0.45, yu + 0.45], color=cols[i], lw=1.3 if i else 1.0,
                    alpha=0.9, zorder=1)
    for i, (c, col) in enumerate(zip(consts, cols)):
        ax.add_patch(Circle((xs[i], yc), 0.6, fc='white', ec=col, lw=1.6, zorder=3))
        ax.text(xs[i], yc, c, fontsize=10.5, ha='center', va='center', zorder=4)
    for j, u in enumerate(units):
        ax.add_patch(FancyBboxPatch((xs[j] - 0.62, yu - 0.42), 1.24, 0.84, boxstyle='round,pad=0.02,rounding_size=0.12',
                                    fc=fs.LIGHT, ec=fs.BLACK, lw=1.0, zorder=3))
        ax.text(xs[j], yu, u, fontsize=10.5, ha='center', va='center', zorder=4)
    ax.text(0.0, yc + 0.95, '정의 상수(정확한 값)', fontsize=9, ha='left', va='center')
    ax.text(0.0, yu - 0.85, '기본 단위', fontsize=9, ha='left', va='center')
    fs.save(fig, S, 'figA_01')


if __name__ == '__main__':
    figA01()
