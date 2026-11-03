# -*- coding: utf-8 -*-
"""2학년 2학기 수학 수행평가2 대비 연습문제 PDF 생성기.

python3 make_pdf.py  ->  practice.html 생성 후 render.js 로 PDF 변환
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

INK = "#1b1f2a"
SOL = "#d6336c"      # 정답 도형
AUX = "#1c7ed6"      # 보조선
GIV = "#2b8a3e"      # 주어진 도형(피타고라스)
GRID = "#c9ced6"

LABEL_POS = {
    "n": (0, -9, "middle"), "s": (0, 17, "middle"),
    "e": (8, 5, "start"), "w": (-8, 5, "end"),
    "ne": (6, -6, "start"), "nw": (-6, -6, "end"),
    "se": (6, 15, "start"), "sw": (-6, 15, "end"),
}


class Fig:
    def __init__(self, W, H, cell=17, grid=True, pad=16, scale=None):
        self.W, self.H, self.c, self.grid, self.pad = W, H, cell, grid, pad
        self.items = []

    def X(self, x):
        return self.pad + x * self.c

    def Y(self, y):
        return self.pad + (self.H - y) * self.c

    # ---- primitives -------------------------------------------------
    def seg(self, p, q, color=INK, w=1.6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(
            f'<line x1="{self.X(p[0]):.1f}" y1="{self.Y(p[1]):.1f}" x2="{self.X(q[0]):.1f}" '
            f'y2="{self.Y(q[1]):.1f}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="round"/>')
        return self

    def poly(self, pts, color=INK, w=1.8, fill="none", dash=None, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self.items.append(
            f'<polygon points="{s}" stroke="{color}" stroke-width="{w}" fill="{fill}" '
            f'fill-opacity="{opacity}"{d} stroke-linejoin="round"/>')
        return self

    def pt(self, p, label=None, pos="ne", color=INK, r=3.3, hollow=False, size=15):
        fill = "#fff" if hollow else color
        self.items.append(
            f'<circle cx="{self.X(p[0]):.1f}" cy="{self.Y(p[1]):.1f}" r="{r}" fill="{fill}" '
            f'stroke="{color}" stroke-width="1.4"/>')
        if label:
            dx, dy, anc = LABEL_POS[pos]
            self.items.append(
                f'<text x="{self.X(p[0]) + dx:.1f}" y="{self.Y(p[1]) + dy:.1f}" text-anchor="{anc}" '
                f'class="lbl" font-size="{size}" fill="{color}">{label}</text>')
        return self

    def text(self, p, s, dx=0, dy=0, size=12, color=INK, anchor="middle", cls="t"):
        self.items.append(
            f'<text x="{self.X(p[0]) + dx:.1f}" y="{self.Y(p[1]) + dy:.1f}" text-anchor="{anchor}" '
            f'class="{cls}" font-size="{size}" fill="{color}">{s}</text>')
        return self

    def ticks(self, p, q, n=1, color=INK):
        mx, my = (self.X(p[0]) + self.X(q[0])) / 2, (self.Y(p[1]) + self.Y(q[1])) / 2
        vx, vy = self.X(q[0]) - self.X(p[0]), self.Y(q[1]) - self.Y(p[1])
        L = math.hypot(vx, vy) or 1
        ux, uy = vx / L, vy / L
        nx, ny = -uy, ux
        for i in range(n):
            off = (i - (n - 1) / 2) * 4
            cx, cy = mx + ux * off, my + uy * off
            self.items.append(
                f'<line x1="{cx + nx * 5:.1f}" y1="{cy + ny * 5:.1f}" x2="{cx - nx * 5:.1f}" '
                f'y2="{cy - ny * 5:.1f}" stroke="{color}" stroke-width="1.4"/>')
        return self

    def right(self, at, p, q, color=INK, s=9):
        ax, ay = self.X(at[0]), self.Y(at[1])
        def unit(t):
            vx, vy = self.X(t[0]) - ax, self.Y(t[1]) - ay
            L = math.hypot(vx, vy)
            return vx / L, vy / L
        u, v = unit(p), unit(q)
        pts = [(ax + u[0] * s, ay + u[1] * s), (ax + (u[0] + v[0]) * s, ay + (u[1] + v[1]) * s),
               (ax + v[0] * s, ay + v[1] * s)]
        self.items.append(
            '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
            f'" fill="none" stroke="{color}" stroke-width="1.2"/>')
        return self

    def arc(self, center, r, a0, a1, color=AUX, w=1.1):
        cx, cy, R = self.X(center[0]), self.Y(center[1]), r * self.c
        pts = []
        for i in range(25):
            a = math.radians(a0 + (a1 - a0) * i / 24)
            pts.append((cx + R * math.cos(a), cy - R * math.sin(a)))
        self.items.append(
            '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
            f'" fill="none" stroke="{color}" stroke-width="{w}"/>')
        return self

    def svg(self, width=None):
        Wpx = self.W * self.c + 2 * self.pad
        Hpx = self.H * self.c + 2 * self.pad
        out = [f'<svg viewBox="0 0 {Wpx} {Hpx}" width="{width or Wpx}" '
               f'xmlns="http://www.w3.org/2000/svg" class="fig">']
        if self.grid:
            for i in range(self.W + 1):
                out.append(f'<line x1="{self.X(i)}" y1="{self.Y(0)}" x2="{self.X(i)}" y2="{self.Y(self.H)}" '
                           f'stroke="{GRID}" stroke-width="0.8"/>')
            for j in range(self.H + 1):
                out.append(f'<line x1="{self.X(0)}" y1="{self.Y(j)}" x2="{self.X(self.W)}" y2="{self.Y(j)}" '
                           f'stroke="{GRID}" stroke-width="0.8"/>')
        else:
            out.append(f'<rect x="{self.pad / 2}" y="{self.pad / 2}" width="{Wpx - self.pad}" '
                       f'height="{Hpx - self.pad}" fill="none" stroke="{GRID}" stroke-width="1" rx="6"/>')
        out += self.items
        out.append("</svg>")
        return "\n".join(out)


def add(a, b, k=1):
    return (a[0] + k * b[0], a[1] + k * b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def centroid(a, b, c):
    return ((a[0] + b[0] + c[0]) / 3, (a[1] + b[1] + c[1]) / 3)


def tilted_square(base, p, q):
    """모눈 위 벡터 (p, q)를 한 변으로 하는 정사각형. base = 외접 정사각형의 왼쪽 아래."""
    bx, by = base
    return [(bx + q, by), (bx + q + p, by + q), (bx + p, by + q + p), (bx, by + p)]


def ov(s):
    return f'<span class="ov">{s}</span>'


def it(s):
    return f'<i class="m">{s}</i>'


# =====================================================================
# 문제 정의: 각 문제는 (번호, 제목, 본문 html, 문제그림, 해설 html, 해설그림)
# =====================================================================
P1, P2, P3 = [], [], []

# ---------------- PART 1 -------------------------------------------
# 1-1
A, B, G = (1, 2), (7, 2), (5, 5)
C = (3 * G[0] - A[0] - B[0], 3 * G[1] - A[1] - B[1])
assert centroid(A, B, C) == G
f = Fig(10, 12).pt(A, "A", "sw").pt(B, "B", "se").pt(G, "G", "e", color=AUX).seg(A, B)
M = mid(A, B)
s = Fig(10, 12, cell=15).seg(A, B).poly([A, B, C], SOL, 2.2)
s.seg(M, C, AUX, 1.3, "5 3").ticks(A, M, 1).ticks(M, B, 1)
s.pt(A, "A", "sw").pt(B, "B", "se").pt(M, "M", "s", AUX).pt(G, "G", "w", AUX).pt(C, "C", "n", SOL).right(B, A, C)
P1.append(dict(
    no="1-1", tag="기본",
    title="두 꼭짓점과 무게중심으로 나머지 꼭짓점 찾기",
    body=f"모눈종이 위에 두 꼭짓점 {it('A')}, {it('B')}와 △{it('ABC')}의 무게중심 {it('G')}가 있습니다."
         f"<ol class='sub'><li>나머지 꼭짓점 {it('C')}를 찾아 △{it('ABC')}를 그리고, 찾는 과정을 쓰시오.</li>"
         f"<li>△{it('ABC')}는 어떤 삼각형인지 추측하고, △{it('ABC')}와 △{it('GAB')}의 넓이를 각각 구하시오. (모눈 한 칸 = 1)</li></ol>",
    fig=f.svg(),
    sol=f"① {ov('AB')}의 중점 {it('M')}을 찾습니다(A에서 오른쪽 3칸).<br>"
        f"② {it('M')}→{it('G')}: 오른쪽 1칸, 위로 3칸. 무게중심은 중선을 2:1로 나누므로 {ov('GC')} = 2{ov('MG')}<br>"
        f"&nbsp;&nbsp;&nbsp;→ {it('G')}에서 오른쪽 2칸, 위로 6칸 간 곳이 {it('C')}입니다.<br>"
        f"③ {ov('AB')}는 가로, {ov('BC')}는 세로 → <b>∠B = 90°인 직각삼각형</b><br>"
        f"&nbsp;&nbsp;&nbsp;△ABC = 6×9÷2 = <b>27</b>, △GAB = 27÷3 = <b>9</b> (확인: 6×3÷2 = 9)",
    solfig=s.svg(),
))

# 1-2
A, G = (3, 10), (5, 6)
M = add(G, ((G[0] - A[0]) / 2, (G[1] - A[1]) / 2))
B, C = (M[0] - 4, M[1]), (M[0] + 4, M[1])
assert centroid(A, B, C) == G
f = Fig(12, 12).pt(A, "A", "n").pt(G, "G", "e", AUX)
s = Fig(12, 12, cell=15).poly([A, B, C], SOL, 2.2).seg(A, M, AUX, 1.3, "5 3")
s.ticks(B, M, 2).ticks(M, C, 2).pt(A, "A", "n").pt(G, "G", "e", AUX).pt(M, "M", "s", AUX)
s.pt(B, "B", "sw", SOL).pt(C, "C", "se", SOL)
P1.append(dict(
    no="1-2", tag="기본",
    title="한 꼭짓점과 무게중심 + 변의 조건",
    body=f"꼭짓점 {it('A')}와 △{it('ABC')}의 무게중심 {it('G')}가 있습니다. "
         f"변 {ov('BC')}가 <b>모눈의 가로선 위에 놓이고 길이가 8칸</b>일 때 △{it('ABC')}를 그리시오. "
         f"(단, 점 {it('B')}가 {it('C')}보다 왼쪽)",
    fig=f.svg(),
    sol=f"① {it('A')}→{it('G')}: 오른쪽 2칸, 아래로 4칸.<br>"
        f"② {ov('AG')} : {ov('GM')} = 2 : 1 이므로 {it('G')}에서 그 절반(오른쪽 1칸, 아래로 2칸)만큼 더 가면 "
        f"{ov('BC')}의 중점 {it('M')}입니다.<br>"
        f"③ {it('M')}을 지나는 가로선 위에서 {it('M')}의 왼쪽·오른쪽으로 4칸씩 → {it('B')}, {it('C')}",
    solfig=s.svg(),
))

# 1-3
B, M, G = (2, 2), (6, 3), (5, 5)
C = sub(add(M, M), B)
A = add(M, sub(G, M), 3)
assert centroid(A, B, C) == G
f = Fig(12, 11).pt(B, "B", "sw").pt(M, "M", "se").pt(G, "G", "e", AUX)
s = Fig(12, 11, cell=15).poly([A, B, C], SOL, 2.2).seg(A, M, AUX, 1.3, "5 3").ticks(B, M, 1).ticks(M, C, 1)
s.pt(B, "B", "sw").pt(M, "M", "se").pt(G, "G", "e", AUX).pt(A, "A", "n", SOL).pt(C, "C", "e", SOL)
P1.append(dict(
    no="1-3", tag="기본",
    title="한 꼭짓점, 변의 중점, 무게중심",
    body=f"꼭짓점 {it('B')}, 변 {ov('BC')}의 중점 {it('M')}, △{it('ABC')}의 무게중심 {it('G')}가 주어졌습니다. "
         f"나머지 두 꼭짓점 {it('A')}, {it('C')}를 찾아 △{it('ABC')}를 그리시오.",
    fig=f.svg(),
    sol=f"① {it('M')}은 {ov('BC')}의 중점 → {it('B')}→{it('M')}(오른쪽 4, 위 1)만큼 한 번 더 가면 {it('C')}<br>"
        f"② {ov('AG')} = 2{ov('GM')} → {it('M')}→{it('G')}(왼쪽 1, 위 2)의 2배만큼 {it('G')}에서 더 가면 "
        f"{it('A')} (왼쪽 2, 위 4)",
    solfig=s.svg(),
))

# 1-4
A0, B0, C0 = (1, 9), (5, 1), (9, 5)
G = centroid(A0, B0, C0)
M, N = mid(B0, C0), mid(C0, A0)
f = Fig(10, 10).pt(M, "M", "se").pt(N, "N", "ne").pt(G, "G", "w", AUX)
s = Fig(10, 10, cell=15).poly([A0, B0, C0], SOL, 2.2).seg(A0, M, AUX, 1.3, "5 3").seg(B0, N, AUX, 1.3, "5 3")
s.ticks(B0, M, 1).ticks(M, C0, 1).ticks(C0, N, 2).ticks(N, A0, 2)
s.pt(M, "M", "se").pt(N, "N", "ne").pt(G, "G", "w", AUX).pt(A0, "A", "nw", SOL).pt(B0, "B", "s", SOL).pt(C0, "C", "e", SOL)
P1.append(dict(
    no="1-4", tag="응용",
    title="두 변의 중점과 무게중심만으로 삼각형 추측하기",
    body=f"△{it('ABC')}에서 {it('M')}은 {ov('BC')}의 중점, {it('N')}은 {ov('CA')}의 중점, {it('G')}는 무게중심입니다. "
         f"세 꼭짓점 {it('A')}, {it('B')}, {it('C')}를 모두 찾아 △{it('ABC')}를 그리시오.",
    fig=f.svg(),
    sol=f"① 중선 {ov('AM')}: {it('M')}→{it('G')}(왼 2, 위 2)의 2배를 {it('G')}에서 더 가면 {it('A')}<br>"
        f"② 중선 {ov('BN')}: {it('N')}→{it('G')}(아래 2)의 2배를 {it('G')}에서 더 가면 {it('B')}<br>"
        f"③ {it('M')}은 {ov('BC')}의 중점 → {it('B')}→{it('M')}만큼 한 번 더 가면 {it('C')}<br>"
        f"④ <b>검산</b>: {it('N')}이 {ov('CA')}의 중점인지 확인 (A→N과 N→C가 같은 이동인지)",
    solfig=s.svg(),
))

# 1-5
A0, B0, C0 = (1, 1), (11, 3), (3, 11)
L, M, N = mid(A0, B0), mid(B0, C0), mid(C0, A0)
G = centroid(A0, B0, C0)
assert centroid(L, M, N) == G
f = Fig(12, 12).pt(L, "L", "s").pt(M, "M", "e").pt(N, "N", "w")
s = Fig(12, 12, cell=15).poly([A0, B0, C0], SOL, 2.2).poly([L, M, N], AUX, 1.2, dash="4 3")
s.seg(A0, M, INK, 0.9, "2 3").seg(B0, N, INK, 0.9, "2 3").seg(C0, L, INK, 0.9, "2 3")
s.pt(L, "L", "s").pt(M, "M", "e").pt(N, "N", "w").pt(G, "G", "se", AUX)
s.pt(A0, "A", "sw", SOL).pt(B0, "B", "e", SOL).pt(C0, "C", "n", SOL)
P1.append(dict(
    no="1-5", tag="응용",
    title="세 변의 중점으로 원래 삼각형 되살리기",
    body=f"어떤 △{it('ABC')}의 세 변 {ov('AB')}, {ov('BC')}, {ov('CA')}의 중점 {it('L')}, {it('M')}, {it('N')}만 남아 있습니다."
         f"<ol class='sub'><li>원래의 △{it('ABC')}를 그리시오.</li>"
         f"<li>△{it('ABC')}의 무게중심 {it('G')}를 찾고, △{it('LMN')}의 무게중심과 비교하여 알 수 있는 점을 쓰시오.</li></ol>",
    fig=f.svg(),
    sol=f"① 삼각형의 두 변의 중점을 연결한 선분은 나머지 변과 평행하고 길이는 절반입니다.<br>"
        f"&nbsp;&nbsp;&nbsp;→ □{it('ALMN')}, □{it('LBMN')}, □{it('LMCN')}은 모두 평행사변형<br>"
        f"&nbsp;&nbsp;&nbsp;→ {it('A')} = {it('N')}에서 (M→L 이동)만큼, {it('B')} = {it('M')}에서 (N→L 이동)만큼, "
        f"{it('C')} = {it('M')}에서 (L→N 이동)만큼<br>"
        f"② 중선 {ov('AM')}, {ov('BN')}, {ov('CL')}의 교점이 {it('G')}. "
        f"<b>△LMN의 무게중심도 같은 점 G</b>입니다.",
    solfig=s.svg(),
))

# 1-6
B, C = (2, 1), (8, 1)
G = (6, 3)
A = (3 * G[0] - B[0] - C[0], 3 * G[1] - B[1] - C[1])
M = mid(B, C)
f = Fig(10, 9).seg(B, C).pt(B, "B", "sw").pt(C, "C", "se").seg((6, 0), (6, 9), AUX, 1.2, "6 4").text((6, 9), "ℓ", 8, 12, 14, AUX, cls="lbl")
s = Fig(10, 9, cell=15).seg((6, 0), (6, 9), AUX, 1, "6 4").poly([A, B, C], SOL, 2.2).poly([G, B, C], AUX, 1, "#a5d8ff", opacity=0.5)
s.seg(A, M, AUX, 1.2, "5 3").pt(B, "B", "sw").pt(C, "C", "se").pt(M, "M", "s", AUX).pt(G, "G", "w", AUX).pt(A, "A", "n", SOL).right(C, B, A)
P1.append(dict(
    no="1-6", tag="응용",
    title="넓이 조건으로 무게중심의 위치 추측하기",
    body=f"선분 {ov('BC')}와 세로 직선 ℓ이 있습니다. △{it('ABC')}의 무게중심 {it('G')}는 직선 ℓ 위에 있고, "
         f"△{it('GBC')}의 넓이는 6입니다. (모눈 한 칸 = 1)"
         f"<ol class='sub'><li>점 {it('G')}와 꼭짓점 {it('A')}를 찾아 △{it('ABC')}를 그리시오.</li>"
         f"<li>△{it('ABC')}의 넓이를 구하고, 어떤 삼각형인지 쓰시오.</li></ol>",
    fig=f.svg(),
    sol=f"① {ov('BC')} = 6, △GBC = 6 → {it('G')}의 높이 = 6×2÷6 = 2 → ℓ 위에서 {ov('BC')}보다 2칸 위가 {it('G')}<br>"
        f"② {ov('BC')}의 중점 {it('M')}→{it('G')}(오른 1, 위 2)의 2배를 {it('G')}에서 더 가면 {it('A')}<br>"
        f"③ △ABC = 3 × △GBC = <b>18</b> (확인: 6×6÷2) / {ov('AC')}가 세로 → <b>∠C = 90°인 직각삼각형</b>",
    solfig=s.svg(),
))

# 1-7
A, G = (1, 1), (5, 3)
M = add(G, ((G[0] - A[0]) / 2, (G[1] - A[1]) / 2))
B, C = (M[0], A[1]), (M[0], 2 * M[1] - A[1])
assert centroid(A, B, C) == G
f = Fig(9, 9).pt(A, "A", "sw").pt(G, "G", "n", AUX)
s = Fig(9, 9, cell=15).poly([A, B, C], SOL, 2.2).seg(A, M, AUX, 1.2, "5 3").ticks(B, M, 1).ticks(M, C, 1)
s.pt(A, "A", "sw").pt(G, "G", "n", AUX).pt(M, "M", "e", AUX).pt(B, "B", "se", SOL).pt(C, "C", "n", SOL).right(B, A, C)
P1.append(dict(
    no="1-7", tag="도전",
    title="직각삼각형 조건이 붙은 경우",
    body=f"꼭짓점 {it('A')}와 무게중심 {it('G')}가 있습니다. △{it('ABC')}가 <b>∠B = 90°</b>이고 "
         f"변 {ov('AB')}가 모눈의 가로선 위에 있을 때, △{it('ABC')}를 그리시오. 또 이 삼각형은 어떤 삼각형인지 쓰시오.",
    fig=f.svg(),
    sol=f"① {it('A')}→{it('G')}(오른 4, 위 2)의 절반만큼 더 가면 {ov('BC')}의 중점 {it('M')}<br>"
        f"② {ov('AB')}가 가로이고 ∠B = 90° → {ov('BC')}는 세로. 따라서 {it('B')}는 "
        f"<b>{it('A')}의 가로줄</b>과 <b>{it('M')}의 세로줄</b>이 만나는 점<br>"
        f"③ {it('C')}는 {it('M')}에 대하여 {it('B')}와 대칭인 점 → AB = BC = 6, <b>직각이등변삼각형</b>",
    solfig=s.svg(),
))

# ---------------- PART 2 -------------------------------------------
# 2-1
A, B, G = (2, 1), (10, 3), (6, 5)
C = (3 * G[0] - A[0] - B[0], 3 * G[1] - A[1] - B[1])
M1 = mid(A, B)
N = mid(A, C)
D = sub(add(G, G), A)
M2 = mid(G, D)
assert M2 == mid(B, C)
f = Fig(12, 12).pt(A, "A", "sw").pt(B, "B", "se").pt(G, "G", "w", AUX)
s1 = Fig(12, 12, cell=11, pad=12).poly([A, B, C], SOL, 2).seg(M1, C, AUX, 1.2, "4 3").pt(A, "A", "sw", size=12).pt(B, "B", "se", size=12).pt(M1, "M", "s", AUX, size=12).pt(G, "G", "w", AUX, size=12).pt(C, "C", "n", SOL, size=12)
s2 = Fig(12, 12, cell=11, pad=12).poly([A, B, C], SOL, 2).seg(B, N, AUX, 1.2, "4 3").ticks(A, N, 1).ticks(N, C, 1).pt(A, "A", "sw", size=12).pt(B, "B", "se", size=12).pt(N, "N", "w", AUX, size=12).pt(G, "G", "s", AUX, size=12).pt(C, "C", "n", SOL, size=12)
s3 = Fig(12, 12, cell=11, pad=12).poly([A, B, C], SOL, 2).seg(A, D, AUX, 1.2, "4 3").poly([G, B, D, C], AUX, 1, "#a5d8ff", opacity=0.45).ticks(A, G, 2).ticks(G, D, 2).pt(A, "A", "sw", size=12).pt(B, "B", "se", size=12).pt(G, "G", "w", AUX, size=12).pt(D, "D", "e", AUX, size=12).pt(C, "C", "n", SOL, size=12)
P2.append(dict(
    no="2-1", tag="기본",
    title="같은 꼭짓점을 세 가지 방법으로 찾기",
    body=f"두 꼭짓점 {it('A')}, {it('B')}와 무게중심 {it('G')}가 주어졌습니다. 꼭짓점 {it('C')}를 "
         f"<b>[방법 A] {ov('AB')}의 중점 이용</b>, <b>[방법 C] 다른 중선({it('B')}에서 그은 중선) 이용</b>, "
         f"<b>[방법 D] 평행사변형 이용</b>의 세 가지 방법으로 각각 찾고, 모두 같은 점이 나오는지 확인하시오. "
         f"각 방법에서 이용한 성질도 한 줄씩 쓰시오.",
    fig=f.svg(),
    sol=f"[방법 A] {ov('AB')}의 중점 {it('M')}에서 {it('G')}까지 위로 3칸 → {it('G')}에서 위로 6칸 더 = {it('C')} "
        f"<span class='why'>(무게중심은 중선을 2:1로 나눈다)</span><br>"
        f"[방법 C] {it('B')}→{it('G')}(왼 4, 위 2)의 절반만큼 {it('G')}에서 더 가면 {ov('AC')}의 중점 {it('N')} → "
        f"{it('A')}→{it('N')}만큼 한 번 더 = {it('C')} <span class='why'>(중점의 뜻)</span><br>"
        f"[방법 D] {it('A')}를 {it('G')}에 대하여 대칭이동한 점 {it('D')}를 찍고, □{it('GBDC')}가 평행사변형이 되도록 "
        f"{it('C')}를 잡습니다 <span class='why'>(평행사변형의 두 대각선은 서로를 이등분)</span><br>"
        f"→ 세 방법 모두 같은 점 {it('C')}가 나옵니다.",
    solfig=f"<div class='trio'><div>{s1.svg()}<p>방법 A</p></div><div>{s2.svg()}<p>방법 C</p></div><div>{s3.svg()}<p>방법 D</p></div></div>",
    wide=True,
))

# 2-2
A, G = (3, 9), (5, 5)
M = add(G, ((G[0] - A[0]) / 2, (G[1] - A[1]) / 2))
ex = [((2, 3), (10, 3)), ((4, 1), (8, 5)), ((6, 0), (6, 6))]
for b, c in ex:
    assert centroid(A, b, c) == G
f = Fig(12, 11).pt(A, "A", "n").pt(G, "G", "e", AUX)
s = Fig(12, 11, cell=15)
cols = ["#d6336c", "#f08c00", "#7048e8"]
for (b, c), col, nm in zip(ex, cols, ["가", "나", "다"]):
    s.poly([A, b, c], col, 1.8)
s.pt(A, "A", "n").pt(G, "G", "w", AUX).pt(M, "M", "se", AUX)
s.text((10, 3), "(가)", 10, -4, 11, cols[0], "start").text((8, 5), "(나)", 8, 0, 11, cols[1], "start").text((6, 0), "(다)", 8, -2, 11, cols[2], "start")
s2 = Fig(12, 11, cell=11, pad=12).poly([A, (3, 3), (9, 3)], SOL, 2).right((3, 3), A, (9, 3)).pt(A, "A", "n", size=12).pt(G, "G", "e", AUX, size=12).pt((3, 3), "B", "sw", SOL, size=12).pt((9, 3), "C", "se", SOL, size=12).pt(M, "M", "s", AUX, size=12)
P2.append(dict(
    no="2-2", tag="기본",
    title="조건을 만족하는 서로 다른 삼각형 그리기",
    body=f"꼭짓점 {it('A')}와 무게중심 {it('G')}만 주어졌습니다. (꼭짓점은 모두 모눈의 꼭짓점에 오도록)"
         f"<ol class='sub'><li>조건을 만족하는 △{it('ABC')}를 <b>서로 다른 모양으로 2개</b> 그리시오.</li>"
         f"<li>이런 삼각형이 여러 개 존재하는 이유를 설명하시오.</li>"
         f"<li>(도전) 그중 ∠{it('B')} = 90°인 삼각형을 찾으시오.</li></ol>",
    fig=f.svg(),
    sol=f"① 먼저 {it('A')}→{it('G')}(오른 2, 아래 4)의 절반만큼 더 가서 {ov('BC')}의 중점 {it('M')}을 찾습니다.<br>"
        f"② {it('M')}에 대하여 서로 대칭인 두 점을 {it('B')}, {it('C')}로 잡으면 모두 정답 → 예: (가), (나), (다)<br>"
        f"③ 이유: {it('A')}, {it('G')}로 정해지는 것은 <b>{ov('BC')}의 중점 {it('M')}뿐</b>이고, {ov('BC')}의 방향과 길이는 "
        f"자유롭기 때문입니다.<br>④ ∠B = 90°: {it('B')}(A의 아래 6칸), {it('C')}(B의 오른쪽 6칸)",
    solfig=f"<div class='duo'><div>{s.svg()}<p>(1) 예시 3가지</p></div><div>{s2.svg()}<p>(3) ∠B = 90°</p></div></div>",
    wide=True,
))

# 2-3
A, B, G = (1, 7), (4, 1), (5, 5)
D = sub(add(G, G), A)
M = mid(G, D)
C = sub(add(M, M), B)
assert centroid(A, B, C) == G
f = Fig(11, 9).pt(A, "A", "nw").pt(B, "B", "s").pt(G, "G", "n", AUX)
s = Fig(11, 9, cell=15).poly([G, B, D, C], AUX, 1, "#a5d8ff", opacity=0.45).seg(A, D, AUX, 1.2, "5 3").poly([A, B, C], SOL, 2.2)
s.ticks(A, G, 2).ticks(G, D, 2).ticks(B, M, 1).ticks(M, C, 1)
s.pt(A, "A", "nw").pt(B, "B", "s").pt(G, "G", "n", AUX).pt(D, "D", "se", AUX).pt(M, "M", "s", AUX).pt(C, "C", "ne", SOL)
P2.append(dict(
    no="2-3", tag="응용",
    title="평행사변형(점대칭)을 이용하는 방법",
    body=f"두 꼭짓점 {it('A')}, {it('B')}와 무게중심 {it('G')}가 있습니다."
         f"<ol class='sub'><li>{it('A')}를 {it('G')}에 대하여 대칭이동한 점 {it('D')}를 찍으시오.</li>"
         f"<li>□{it('GBDC')}가 평행사변형이 되도록 점 {it('C')}를 찾아 △{it('ABC')}를 그리시오.</li>"
         f"<li>이렇게 그리면 {it('G')}가 △{it('ABC')}의 무게중심이 되는 이유를 설명하시오.</li></ol>",
    fig=f.svg(),
    sol=f"① {it('A')}→{it('G')}(오른 4, 아래 2)만큼 {it('G')}에서 한 번 더 → {it('D')}<br>"
        f"② {ov('GD')}의 중점 {it('M')}을 찾고, {it('B')}→{it('M')}만큼 한 번 더 → {it('C')}<br>"
        f"③ 이유: 평행사변형의 두 대각선은 서로를 이등분하므로 {it('M')}은 {ov('BC')}의 중점이고 "
        f"{ov('GM')} = ½{ov('GD')} = ½{ov('AG')}.<br>&nbsp;&nbsp;&nbsp;즉 {it('G')}는 중선 {ov('AM')}을 2:1로 나누는 점 → 무게중심",
    solfig=s.svg(),
))

# 2-4 (작도)
A, B, G = (1.2, 6.6), (2.0, 1.0), (4.6, 3.4)
C = (3 * G[0] - A[0] - B[0], 3 * G[1] - A[1] - B[1])
f = Fig(12, 8, grid=False).pt(A, "A", "n").pt(B, "B", "s").pt(G, "G", "n", AUX)
M = mid(A, B)
P_ = add(M, sub(G, M), 2)
s1 = Fig(12, 8, grid=False, cell=13, pad=12).poly([A, B, C], SOL, 2).seg(M, C, AUX, 1.1, "4 3")
s1.ticks(A, M, 2).ticks(M, B, 2).ticks(M, G, 1).ticks(G, P_, 1).ticks(P_, C, 1)
gm = math.hypot(*sub(G, M))
ang = math.degrees(math.atan2(*reversed(sub(C, M))))
s1.arc(G, gm, ang - 12, ang + 12).arc(P_, gm, ang - 12, ang + 12)
s1.pt(A, "A", "n", size=12).pt(B, "B", "s", size=12).pt(M, "M", "w", AUX, size=12).pt(G, "G", "n", AUX, size=12).pt(C, "C", "e", SOL, size=12)
D = sub(add(G, G), A)
M2 = mid(G, D)
s2 = Fig(12, 8, grid=False, cell=13, pad=12).poly([A, B, C], SOL, 2).seg(A, D, AUX, 1.1, "4 3").seg(B, C, AUX, 1.1, "4 3")
s2.ticks(A, G, 2).ticks(G, D, 2).ticks(B, M2, 1).ticks(M2, C, 1)
ag = math.hypot(*sub(G, A))
ang2 = math.degrees(math.atan2(*reversed(sub(D, A))))
s2.arc(G, ag, ang2 - 10, ang2 + 10)
s2.pt(A, "A", "n", size=12).pt(B, "B", "s", size=12).pt(G, "G", "n", AUX, size=12).pt(D, "D", "e", AUX, size=12).pt(M2, "M", "s", AUX, size=12).pt(C, "C", "e", SOL, size=12)
P2.append(dict(
    no="2-4", tag="응용",
    title="모눈 없이 자와 컴퍼스로 두 가지 방법",
    body=f"모눈이 없는 종이에 두 꼭짓점 {it('A')}, {it('B')}와 무게중심 {it('G')}가 있습니다. "
         f"자와 컴퍼스를 사용하여 꼭짓점 {it('C')}를 <b>서로 다른 두 가지 방법</b>으로 찾고, 작도 순서를 쓰시오. "
         f"(모눈이 없으므로 칸 세기를 쓸 수 없습니다!)",
    fig=f.svg(),
    sol=f"<b>방법 1</b> ① {ov('AB')}의 수직이등분선을 작도해 중점 {it('M')}을 찾는다. ② 반직선 {it('MG')}를 긋고, "
        f"컴퍼스로 {ov('MG')}의 길이를 {it('G')}에서부터 두 번 옮긴다. ③ 그 끝점이 {it('C')} ({ov('MC')} = 3{ov('MG')})<br>"
        f"<b>방법 2</b> ① 반직선 {it('AG')} 위에 {ov('GD')} = {ov('AG')}인 점 {it('D')}를 컴퍼스로 잡는다. "
        f"② {ov('GD')}의 수직이등분선으로 중점 {it('M')}을 찾는다. ③ 반직선 {it('BM')} 위에 {ov('MC')} = {ov('BM')}인 점이 {it('C')}",
    solfig=f"<div class='duo'><div>{s1.svg()}<p>방법 1</p></div><div>{s2.svg()}<p>방법 2</p></div></div>",
    wide=True,
))

# 2-5
B, C = (2, 2), (8, 2)
As = [(2, 8), (5, 8), (8, 8), (11, 8)]
f = Fig(12, 10).seg(B, C).pt(B, "B", "sw").pt(C, "C", "se")
s = Fig(12, 10, cell=15).seg((0, 4), (12, 4), AUX, 1, "6 4").seg((0, 8), (12, 8), INK, 0.8, "2 3")
cols = ["#d6336c", "#f08c00", "#2b8a3e", "#7048e8"]
for a, col in zip(As, cols):
    g = centroid(a, B, C)
    assert g[1] == 4 and g[0] == int(g[0])
    s.poly([a, B, C], col, 1.6).pt(g, None, color=col, r=3.6)
s.pt(B, "B", "sw").pt(C, "C", "s")
P2.append(dict(
    no="2-5", tag="도전",
    title="넓이가 같은 삼각형들의 무게중심 추측하기",
    body=f"선분 {ov('BC')}가 있습니다. (모눈 한 칸 = 1)"
         f"<ol class='sub'><li>넓이가 18이고 무게중심이 모눈의 꼭짓점에 오는 △{it('ABC')}를 <b>서로 다른 방법(모양)으로 2개 이상</b> 그리시오.</li>"
         f"<li>그린 삼각형들의 무게중심은 어떤 위치에 놓이는지 추측하고, 그 이유를 쓰시오.</li></ol>",
    fig=f.svg(),
    sol=f"① 넓이 18, 밑변 6 → 높이 6 → {it('A')}는 {ov('BC')}보다 6칸 위의 가로줄 위<br>"
        f"② {it('G')}가 모눈의 꼭짓점이 되는 {it('A')}: 4가지 (직각삼각형 2개, 이등변삼각형 1개, 둔각삼각형 1개)<br>"
        f"③ 추측: 무게중심은 모두 <b>{ov('BC')}보다 2칸 위의 가로줄 위</b>에 있다.<br>"
        f"&nbsp;&nbsp;&nbsp;이유: △GBC = ⅓△ABC = 6으로 항상 같으므로 {it('G')}의 높이는 6×2÷6 = 2로 일정",
    solfig=s.svg() + "<p class='small' style='margin:0'>파란 점선: 무게중심들이 모두 놓이는 직선</p>",
))

# ---------------- PART 3 -------------------------------------------
# 3-1
f = Fig(16, 6)
s = Fig(16, 6, cell=13, pad=12)
for base, (p, q), area in [((1, 1), (1, 2), 5), ((5, 1), (1, 3), 10), ((10, 0), (2, 3), 13)]:
    sq = tilted_square(base, p, q)
    s.poly(sq, SOL, 2, "#ffc9de", 0.6)
    s.poly([base, (base[0] + p + q, base[1]), (base[0] + p + q, base[1] + p + q), (base[0], base[1] + p + q)], AUX, 1, dash="4 3")
    cx = base[0] + (p + q) / 2
    s.text((cx, base[1] + (p + q) / 2), str(area), 0, 5, 13, SOL)
P3.append(dict(
    no="3-1", tag="기본",
    title="넓이가 5, 10, 13인 정사각형",
    body="모눈종이 위에 넓이가 각각 <b>5, 10, 13</b>인 정사각형을 그리시오. "
         "(단, 정사각형의 꼭짓점은 모두 모눈의 꼭짓점이고, 모눈 한 칸의 넓이는 1)",
    fig=f.svg(),
    sol="가로 a칸, 세로 b칸 이동한 선분을 한 변으로 하면 정사각형의 넓이 = a² + b²<br>"
        "· 5 = 1² + 2² &nbsp; · 10 = 1² + 3² &nbsp; · 13 = 2² + 3²<br>"
        "확인(큰 정사각형 − 직각삼각형 4개): 9 − 4×1 = 5, &nbsp;16 − 4×1.5 = 10, &nbsp;25 − 4×3 = 13",
    solfig=s.svg(),
    wide=True,
))

# 3-2
f = Fig(19, 8)
s = Fig(19, 8, cell=12, pad=12)
for base, (p, q), area in [((1, 1), (2, 2), 8), ((5, 1), (3, 3), 18), ((12, 0), (3, 4), 25)]:
    sq = tilted_square(base, p, q)
    s.poly(sq, SOL, 2, "#ffc9de", 0.6)
    s.poly([base, (base[0] + p + q, base[1]), (base[0] + p + q, base[1] + p + q), (base[0], base[1] + p + q)], AUX, 1, dash="4 3")
    s.text((base[0] + (p + q) / 2, base[1] + (p + q) / 2), str(area), 0, 5, 13, SOL)
P3.append(dict(
    no="3-2", tag="기본",
    title="넓이 8, 18인 정사각형과 '기울어진' 넓이 25인 정사각형",
    body="모눈종이 위에 넓이가 <b>8, 18</b>인 정사각형을 그리시오. 또 넓이가 <b>25</b>이면서 "
         "<b>변이 모눈선과 평행하지 않은</b> 정사각형을 그리시오. (꼭짓점은 모눈의 꼭짓점)",
    fig=f.svg(),
    sol="· 8 = 2² + 2² (16 − 4×2) &nbsp; · 18 = 3² + 3² (36 − 4×4.5)<br>"
        "· 25 = 3² + 4² → 가로 4칸·세로 3칸 이동한 선분을 한 변으로! (49 − 4×6 = 25)<br>"
        "※ 5×5 정사각형도 넓이는 25이지만 '모눈선과 평행하지 않은' 조건에 맞지 않습니다.",
    solfig=s.svg(),
    wide=True,
))

# 3-3
Pq = [(1, 1), (3, 1), (3, 3), (1, 3)]
Qq = [(4, 1), (7, 1), (7, 4), (4, 4)]
f = Fig(17, 7).poly(Pq, GIV, 1.8, "#b2f2bb", 0.5).poly(Qq, GIV, 1.8, "#b2f2bb", 0.5)
f.text((2, 2), "P", 0, 5, 14, GIV, cls="lbl").text((5.5, 2.5), "Q", 0, 5, 14, GIV, cls="lbl")
s = Fig(17, 7, cell=13, pad=12).poly(Pq, GIV, 1.6, "#b2f2bb", 0.5).poly(Qq, GIV, 1.6, "#b2f2bb", 0.5)
s.text((2, 2), "4", 0, 5, 12, GIV).text((5.5, 2.5), "9", 0, 5, 12, GIV)
sq13 = tilted_square((8, 1), 2, 3)
s.poly(sq13, SOL, 2, "#ffc9de", 0.6).text((10.5, 3.5), "13", 0, 5, 13, SOL)
s.poly([(8, 1), (11, 1), (8, 3)], AUX, 1.2, "#a5d8ff", 0.5).right((8, 1), (11, 1), (8, 3), AUX)
sq5 = tilted_square((14, 1), 1, 2)
s.poly(sq5, SOL, 2, "#ffc9de", 0.6).text((15.5, 2.5), "5", 0, 5, 13, SOL)
P3.append(dict(
    no="3-3", tag="응용",
    title="두 정사각형의 넓이의 합·차와 같은 정사각형",
    body=f"모눈종이 위에 정사각형 {it('P')}(넓이 4)와 {it('Q')}(넓이 9)가 있습니다. "
         f"피타고라스 정리를 이용하여 <ol class='sub'><li>{it('P')}와 {it('Q')}의 넓이의 <b>합</b>과 같은 넓이의 정사각형</li>"
         f"<li>{it('Q')}의 넓이에서 {it('P')}의 넓이를 <b>뺀</b> 것과 같은 넓이의 정사각형</li></ol>을 각각 그리시오.",
    fig=f.svg(),
    sol=f"(1) 두 변이 2, 3인 직각삼각형을 그리면 빗변 위의 정사각형 넓이 = 2² + 3² = <b>13</b><br>"
        f"(2) 9 − 4 = <b>5</b> = 1² + 2² → 가로 1칸·세로 2칸 이동한 선분을 한 변으로 하는 정사각형<br>"
        f"&nbsp;&nbsp;&nbsp;(빗변 위 정사각형 넓이 9, 한 변 위 정사각형 넓이 4인 직각삼각형의 나머지 변 위 정사각형이라고 생각해도 됩니다.)",
    solfig=s.svg(),
    wide=True,
))

# 3-4
R = [(1, 1), (6, 1), (6, 3), (1, 3)]
PG = [(1, 1), (5, 1), (6, 6), (2, 6)]
f1 = Fig(12, 5).poly(R, GIV, 1.8, "#b2f2bb", 0.5)
f2 = Fig(14, 7).poly(PG, GIV, 1.8, "#b2f2bb", 0.5)
s1 = Fig(12, 5, cell=11, pad=12).poly(R, GIV, 1.6, "#b2f2bb", 0.5).poly(tilted_square((7, 0), 1, 3), SOL, 2, "#ffc9de", 0.6).text((9, 2), "10", 0, 5, 12, SOL)
s2 = Fig(14, 7, cell=11, pad=12).poly(PG, GIV, 1.6, "#b2f2bb", 0.5).poly(tilted_square((7, 0), 2, 4), SOL, 2, "#ffc9de", 0.6).text((10, 3), "20", 0, 5, 12, SOL)
P3.append(dict(
    no="3-4", tag="응용",
    title="주어진 도형과 넓이가 같은 정사각형",
    body="(1) 직사각형과 넓이가 같은 정사각형, (2) 평행사변형과 넓이가 같은 정사각형을 각각 모눈종이 위에 그리시오. "
         "(꼭짓점은 모눈의 꼭짓점)",
    fig=f"<div class='duo'><div>{f1.svg()}<p>(1)</p></div><div>{f2.svg()}<p>(2)</p></div></div>",
    sol="(1) 직사각형 넓이 = 5×2 = 10 = 1² + 3² → 가로 1·세로 3 (또는 가로 3·세로 1) 이동한 선분을 한 변으로<br>"
        "(2) 평행사변형 넓이 = 밑변 4 × 높이 5 = 20 = 2² + 4² → 가로 2·세로 4 이동한 선분을 한 변으로<br>"
        "※ 먼저 <b>주어진 도형의 넓이</b>를 구하고, 그 수를 <b>두 제곱수의 합</b>으로 나타내는 것이 핵심!",
    solfig=f"<div class='duo'><div>{s1.svg()}<p>(1)</p></div><div>{s2.svg()}<p>(2)</p></div></div>",
    wide=True,
))

# 3-5
f = Fig(12, 6)
t1 = [(1, 1), (2, 4), (5, 3)]          # 다리 (1,3),(3,-1) → 넓이 5
t2 = [(7, 3), (9, 5), (11, 3)]         # 다리 (2,2),(2,-2) → 넓이 4
s = Fig(12, 6, cell=14).poly(t1, SOL, 2, "#ffc9de", 0.6).right((2, 4), (1, 1), (5, 3), SOL).text((2.7, 2.8), "5", 0, 5, 13, SOL)
s.poly(t2, SOL, 2, "#ffc9de", 0.6).right((9, 5), (7, 3), (11, 3), SOL).text((9, 3.7), "4", 0, 5, 13, SOL)
s.ticks((1, 1), (2, 4), 1, SOL).ticks((2, 4), (5, 3), 1, SOL).ticks((7, 3), (9, 5), 2, SOL).ticks((9, 5), (11, 3), 2, SOL)
P3.append(dict(
    no="3-5", tag="응용",
    title="넓이가 주어진 직각이등변삼각형",
    body="모눈종이 위에 다음 조건에 맞는 직각이등변삼각형을 그리시오. (꼭짓점은 모눈의 꼭짓점)"
         "<ol class='sub'><li>넓이가 5이고, 길이가 같은 두 변이 모눈선과 평행하지 않은 것</li>"
         "<li>넓이가 4이고, 길이가 같은 두 변이 모눈선과 평행하지 않은 것</li></ol>",
    fig=f.svg(),
    sol="직각이등변삼각형의 넓이 = (같은 변 위의 정사각형 넓이) ÷ 2<br>"
        "(1) 정사각형 넓이가 10 = 1² + 3² → 가로 1·세로 3 이동한 두 변을 직각으로<br>"
        "(2) 정사각형 넓이가 8 = 2² + 2² → 가로 2·세로 2 이동한 두 변을 직각으로 (빗변은 가로 4칸)",
    solfig=s.svg(),
))

# 3-6 (작도)
a, b, r = 2.4, 3.2, 4.5
f = Fig(14, 6, grid=False, cell=22)
f.poly([(0.8, 0.8), (0.8 + a, 0.8), (0.8 + a, 0.8 + a), (0.8, 0.8 + a)], GIV, 1.8, "#b2f2bb", 0.5).text((0.8 + a / 2, 0.8 + a / 2), "P", 0, 5, 14, GIV, cls="lbl")
f.poly([(4.2, 0.8), (4.2 + b, 0.8), (4.2 + b, 0.8 + b), (4.2, 0.8 + b)], GIV, 1.8, "#b2f2bb", 0.5).text((4.2 + b / 2, 0.8 + b / 2), "Q", 0, 5, 14, GIV, cls="lbl")
f.poly([(8.6, 0.6), (8.6 + r, 0.6), (8.6 + r, 0.6 + r), (8.6, 0.6 + r)], GIV, 1.8, "#b2f2bb", 0.5).text((8.6 + r / 2, 0.6 + r / 2), "R", 0, 5, 14, GIV, cls="lbl")
# 해설 (1)
O = (1.5, 1.0)
Pp, Qp = (O[0], O[1] + a), (O[0] + b, O[1])
v = sub(Pp, Qp)  # 빗변 Q->P
nrm = (v[1], -v[0])  # 바깥쪽 (오른쪽 위)
nrm = (-nrm[0], -nrm[1]) if nrm[0] < 0 else nrm
s1 = Fig(10, 8, grid=False, cell=15, pad=12)
s1.seg((O[0], 0.3), (O[0], 7.5), AUX, 1, "4 3").seg((0.5, O[1]), (9.5, O[1]), AUX, 1, "4 3")
s1.poly([O, Qp, Pp], INK, 1.6).right(O, Qp, Pp)
sqc = [Qp, Pp, add(Pp, (-v[1], v[0]) if False else (v[1] * -1, v[0]) if False else (0, 0)), Qp]
c1 = add(Pp, (a, b))
c2 = add(Qp, (a, b))
s1.poly([Qp, Pp, c1, c2], SOL, 2, "#ffc9de", 0.5)
s1.text(mid(O, Pp), "a", -9, 4, 13, INK, cls="lbl").text(mid(O, Qp), "b", 0, 15, 13, INK, cls="lbl")
s1.text(mid(Pp, c2), "a²+b²", 0, 5, 12, SOL)
# 해설 (2)
O2 = (1.2, 1.0)
P2p = (O2[0] + a, O2[1])
h = math.sqrt(r * r - a * a)
Q2p = (O2[0], O2[1] + h)
s2 = Fig(10, 8, grid=False, cell=15, pad=12)
s2.seg((O2[0], 0.3), (O2[0], 7.5), AUX, 1, "4 3").seg((0.4, O2[1]), (9.5, O2[1]), AUX, 1, "4 3")
ang = math.degrees(math.atan2(Q2p[1] - P2p[1], Q2p[0] - P2p[0]))
s2.arc(P2p, r, ang - 8, ang + 8)
s2.poly([O2, P2p, Q2p], INK, 1.6).right(O2, P2p, Q2p)
s2.poly([O2, Q2p, (O2[0] + h, O2[1] + h), (O2[0] + h, O2[1])], SOL, 2, "#ffc9de", 0.35)
s2.text(mid(O2, P2p), "a", 0, 15, 13, INK, cls="lbl").text(mid(P2p, Q2p), "r", 8, 0, 13, INK, cls="lbl")
s2.text((O2[0] + h / 2 + 0.5, O2[1] + h / 2 + 0.6), "r²−a²", 0, 5, 12, SOL)
P3.append(dict(
    no="3-6", tag="도전",
    title="모눈 없이 작도로 넓이의 합·차 만들기",
    body=f"모눈이 없는 종이에 정사각형 {it('P')}, {it('Q')}, {it('R')}가 있습니다. 자와 컴퍼스(또는 삼각자)를 이용하여"
         f"<ol class='sub'><li>{it('P')}와 {it('Q')}의 넓이의 합과 같은 넓이의 정사각형</li>"
         f"<li>{it('R')}의 넓이에서 {it('P')}의 넓이를 뺀 것과 같은 넓이의 정사각형</li></ol>을 그리고, 그리는 순서를 쓰시오.",
    fig=f.svg(),
    sol=f"(1) 직각을 이루는 두 직선을 긋고, 한 변 위에 {it('P')}의 한 변 길이 {it('a')}, 다른 변 위에 {it('Q')}의 한 변 길이 {it('b')}를 "
        f"컴퍼스로 옮긴다 → 빗변을 한 변으로 하는 정사각형의 넓이 = {it('a')}² + {it('b')}²<br>"
        f"(2) 직각을 이루는 두 직선의 한 변 위에 길이 {it('a')}를 옮기고, 그 끝점을 중심으로 반지름 {it('r')}({it('R')}의 한 변)인 원을 그려 "
        f"다른 직선과 만나는 점을 찾는다 → 그 변 위의 정사각형 넓이 = {it('r')}² − {it('a')}²",
    solfig=f"<div class='duo'><div>{s1.svg()}<p>(1) 합</p></div><div>{s2.svg()}<p>(2) 차</p></div></div>",
    wide=True,
))

# 3-7
SQ = [(1, 1), (5, 1), (5, 5), (1, 5)]
f = Fig(16, 9).poly(SQ, GIV, 1.8, "#b2f2bb", 0.5)
s = Fig(16, 9, cell=13, pad=12).poly(SQ, GIV, 1.6, "#b2f2bb", 0.5)
s.poly([(3, 1), (5, 3), (3, 5), (1, 3)], SOL, 2, "#ffc9de", 0.6).text((3, 3), "8", 0, 5, 13, SOL)
s.poly(tilted_square((7, 0), 4, 4), SOL, 2, "#ffc9de", 0.6).text((11, 4), "32", 0, 5, 13, SOL)
s.seg((1, 1), (5, 5), AUX, 1, "4 3")
P3.append(dict(
    no="3-7", tag="도전",
    title="넓이가 2배, 절반인 정사각형",
    body="모눈종이 위의 정사각형(넓이 16)을 보고, 넓이가 이 정사각형의 <b>절반</b>인 정사각형과 "
         "<b>2배</b>인 정사각형을 각각 그리시오. 또 그렇게 되는 이유를 피타고라스 정리로 설명하시오.",
    fig=f.svg(),
    sol="· 절반(8): 각 변의 중점을 차례로 이으면 한 변이 가로 2·세로 2 이동 → 2² + 2² = 8<br>"
        "· 2배(32): 대각선(가로 4·세로 4 이동)을 한 변으로 하는 정사각형 → 4² + 4² = 32<br>"
        "※ 대각선 위의 정사각형 넓이 = 두 변 위의 정사각형 넓이의 합 = 16 + 16",
    solfig=s.svg(),
    wide=True,
))

# ---------------- 실전 모의 --------------------------------------------
A, G = (2, 2), (6, 4)
M = add(G, ((G[0] - A[0]) / 2, (G[1] - A[1]) / 2))
B1, C1 = (M[0], M[1] - 4), (M[0], M[1] + 4)
B2, C2 = (8, 2), (8, 8)
assert centroid(A, B1, C1) == G and centroid(A, B2, C2) == G
mf1 = Fig(10, 10, cell=19).pt(A, "A", "sw").pt(G, "G", "n", AUX)
mf2 = Fig(10, 10, cell=19).pt(A, "A", "sw").pt(G, "G", "n", AUX)
R0 = (4, 4)
legH, legV = (8, 4), (4, 7)
mf3 = Fig(12, 12, cell=16).poly([R0, legH, legV], INK, 1.8).right(R0, legH, legV)
mf3.poly([(4, 0), (8, 0), (8, 4), (4, 4)], GIV, 1.6, "#b2f2bb", 0.5).poly([(1, 4), (4, 4), (4, 7), (1, 7)], GIV, 1.6, "#b2f2bb", 0.5)
mf3.text((6, 2), "16", 0, 5, 12, GIV).text((2.5, 5.5), "9", 0, 5, 12, GIV)
ms1 = Fig(10, 10, cell=13, pad=12).poly([A, B1, C1], SOL, 2).seg(A, M, AUX, 1.1, "4 3").ticks(B1, M, 1).ticks(M, C1, 1)
ms1.pt(A, "A", "sw", size=12).pt(G, "G", "n", AUX, size=12).pt(M, "M", "e", AUX, size=12).pt(B1, "B", "s", SOL, size=12).pt(C1, "C", "n", SOL, size=12)
D = sub(add(G, G), A)
ms2 = Fig(10, 10, cell=13, pad=12).poly([G, B2, D, C2], AUX, 1, "#a5d8ff", 0.45).seg(A, D, AUX, 1.1, "4 3").poly([A, B2, C2], SOL, 2).right(B2, A, C2)
ms2.pt(A, "A", "sw", size=12).pt(G, "G", "n", AUX, size=12).pt(D, "D", "e", AUX, size=12).pt(B2, "B", "se", SOL, size=12).pt(C2, "C", "n", SOL, size=12)
hyp = [(8, 4), (4, 7), (7, 11), (11, 8)]
ms3 = Fig(12, 12, cell=11, pad=12).poly([R0, legH, legV], INK, 1.6).right(R0, legH, legV)
ms3.poly([(4, 0), (8, 0), (8, 4), (4, 4)], GIV, 1.4, "#b2f2bb", 0.5).poly([(1, 4), (4, 4), (4, 7), (1, 7)], GIV, 1.4, "#b2f2bb", 0.5)
ms3.poly(hyp, SOL, 2, "#ffc9de", 0.6).poly([(4, 4), (11, 4), (11, 11), (4, 11)], AUX, 1, dash="4 3").text((7.5, 7.5), "25", 0, 5, 12, SOL)

# =====================================================================
# 개념 그림
# =====================================================================
cA, cB, cC = (3, 9), (0.5, 1), (11.5, 2)
cG = centroid(cA, cB, cC)
cMa, cMb, cMc = mid(cB, cC), mid(cC, cA), mid(cA, cB)
cf = Fig(12, 10, grid=False, cell=17, pad=14)
shades = ["#ffe3e3", "#fff3bf", "#d3f9d8", "#d0ebff", "#e5dbff", "#ffe8cc"]
for i, (p, q) in enumerate([(cA, cMc), (cMc, cB), (cB, cMa), (cMa, cC), (cC, cMb), (cMb, cA)]):
    cf.poly([cG, p, q], "none", 0, shades[i], 1)
cf.poly([cA, cB, cC], INK, 1.8)
for v_, m_ in [(cA, cMa), (cB, cMb), (cC, cMc)]:
    cf.seg(v_, m_, AUX, 1.2, "5 3")
cf.ticks(cB, cMa, 1).ticks(cMa, cC, 1).ticks(cC, cMb, 2).ticks(cMb, cA, 2).ticks(cA, cMc, 3).ticks(cMc, cB, 3)
cf.pt(cA, "A", "n").pt(cB, "B", "sw").pt(cC, "C", "se").pt(cG, "G", "e", AUX).pt(cMa, "M", "s", AUX)
cf.text(mid(cA, cG), "2", 9, 2, 13, SOL).text(mid(cG, cMa), "1", 9, 4, 13, SOL)

pf = Fig(5, 5, cell=24, pad=14)
pf.poly([(1, 1), (4, 1), (4, 4), (1, 4)], AUX, 1, dash="4 3")
sq = tilted_square((1, 1), 1, 2)
for tri in [[(1, 1), sq[0], sq[3]], [sq[0], (4, 1), sq[1]], [sq[1], (4, 4), sq[2]], [sq[2], (1, 4), sq[3]]]:
    pf.poly(tri, AUX, 0.8, "#a5d8ff", 0.5)
pf.poly(sq, SOL, 2, "#ffc9de", 0.55).text((2.5, 2.5), "5", 0, 6, 15, SOL)

df = Fig(10, 8, grid=False, cell=15, pad=12)
dA, dB, dG = (1, 6.5), (2.5, 1), (4.5, 3.6)
dC = (3 * dG[0] - dA[0] - dB[0], 3 * dG[1] - dA[1] - dB[1])
dD = sub(add(dG, dG), dA)
df.poly([dG, dB, dD, dC], AUX, 1, "#a5d8ff", 0.45).seg(dA, dD, AUX, 1.1, "4 3").poly([dA, dB, dC], SOL, 1.8)
df.ticks(dA, dG, 2).ticks(dG, dD, 2)
df.pt(dA, "A", "n", size=12).pt(dB, "B", "s", size=12).pt(dC, "C", "e", size=12).pt(dG, "G", "n", AUX, size=12).pt(dD, "D", "s", AUX, size=12)


# =====================================================================
# HTML 조립
# =====================================================================
def problem_html(p, show_answer_space=True):
    cls = "prob wide" if p.get("wide") else "prob"
    return (f'<div class="{cls}"><div class="ph"><span class="no">{p["no"]}</span>'
            f'<span class="tag t-{p["tag"]}">{p["tag"]}</span><span class="ti">{p["title"]}</span></div>'
            f'<div class="pb">{p["body"]}</div><div class="pf">{p["fig"]}</div>'
            f'<div class="write">풀이 과정 / 이용한 성질 :</div></div>')


def sol_html(p):
    cls = "sol wide" if p.get("wide") else "sol"
    return (f'<div class="{cls}"><div class="sh"><span class="no">{p["no"]}</span>{p["title"]}</div>'
            f'<div class="sf">{p["solfig"]}</div><div class="st">{p["sol"]}</div></div>')


def flow(problems, fn):
    """넓은 문제는 한 줄 전체, 일반 문제는 두 개씩 나란히."""
    out, buf = [], []
    for p in problems:
        if p.get("wide"):
            if buf:
                out.append('<div class="row">' + "".join(buf) + "</div>")
                buf = []
            out.append(fn(p))
        else:
            buf.append(fn(p))
            if len(buf) == 2:
                out.append('<div class="row">' + "".join(buf) + "</div>")
                buf = []
    if buf:
        out.append('<div class="row">' + "".join(buf) + "</div>")
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 13mm 12mm 15mm 12mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Sans KR', 'WenQuanYi Zen Hei', sans-serif; color: #1b1f2a; font-size: 9.6pt;
       line-height: 1.55; margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.lbl, i.m { font-family: 'Times New Roman', 'DejaVu Serif', serif; font-style: italic; }
i.m { font-size: 1.08em; }
.ov { text-decoration: overline; font-family: 'Times New Roman', 'DejaVu Serif', serif; font-style: italic; }
.t { font-family: 'Noto Sans KR', 'WenQuanYi Zen Hei', sans-serif; font-weight: 700; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 19pt; margin: 0 0 2mm; letter-spacing: -0.5px; }
h2 { font-size: 13.5pt; margin: 0 0 3mm; padding: 2mm 3mm; color: #fff; background: #1b1f2a; border-radius: 2mm; }
h2 small { font-weight: 400; font-size: 9.5pt; opacity: .85; margin-left: 2mm; }
h3 { font-size: 11.5pt; margin: 4mm 0 2mm; border-left: 4px solid #d6336c; padding-left: 2.5mm; }
.cover { border: 2px solid #1b1f2a; border-radius: 3mm; padding: 5mm 6mm; margin-bottom: 4mm; }
.cover .kick { color: #d6336c; font-weight: 700; font-size: 10pt; }
.cover .sub { font-size: 12pt; font-weight: 700; color: #495057; }
.name { display: flex; gap: 6mm; margin-top: 3mm; font-size: 10pt; }
.name span { border-bottom: 1px solid #868e96; min-width: 22mm; padding-right: 10mm; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; }
th, td { border: 1px solid #adb5bd; padding: 1.6mm 2mm; vertical-align: middle; }
th { background: #f1f3f5; }
.box { border: 1px solid #ced4da; border-radius: 2mm; padding: 2.5mm 3.5mm; margin: 2mm 0; background: #fbfcfd; }
.box.warn { border-color: #ffa8a8; background: #fff5f5; }
.box.tip { border-color: #91a7ff; background: #f3f6ff; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; align-items: start; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-bottom: 3.5mm; break-inside: avoid; }
.prob, .sol { border: 1px solid #ced4da; border-radius: 2mm; padding: 2.5mm 3mm; break-inside: avoid; background: #fff; }
.prob.wide, .sol.wide { margin-bottom: 3.5mm; }
.ph, .sh { display: flex; align-items: center; gap: 2mm; margin-bottom: 1.5mm; font-weight: 700; }
.no { white-space: nowrap; background: #1b1f2a; color: #fff; border-radius: 1.2mm; padding: 0 2mm; font-size: 9.5pt; }
.tag { white-space: nowrap; font-size: 8pt; border-radius: 3mm; padding: 0 2mm; font-weight: 700; }
.t-기본 { background: #d3f9d8; color: #2b8a3e; } .t-응용 { background: #fff3bf; color: #e67700; }
.t-도전 { background: #ffe3e3; color: #c92a2a; }
.ti { font-size: 10pt; }
.pb ol.sub { margin: 1mm 0 0; padding-left: 5mm; }
.pf { text-align: center; margin-top: 1.5mm; }
.pf svg.fig { max-width: 100%; height: auto; }
.write { margin-top: 2mm; border-top: 1px dashed #adb5bd; padding-top: 1mm; min-height: 11mm; color: #868e96; font-size: 8.5pt; }
.duo, .trio { display: flex; justify-content: center; gap: 4mm; }
.duo p, .trio p { margin: 0; text-align: center; font-size: 8.5pt; font-weight: 700; color: #495057; }
.sol .sf { text-align: center; }
.sol .sf svg.fig { max-width: 100%; height: auto; }
.sol .st { font-size: 9pt; margin-top: 1mm; }
.why { color: #1c7ed6; font-size: 8.6pt; }
.legend { font-size: 8.5pt; color: #495057; }
.legend b.s { color: #d6336c; } .legend b.a { color: #1c7ed6; } .legend b.g { color: #2b8a3e; }
.check td.c { width: 12mm; text-align: center; font-size: 12pt; }
.method { display: grid; grid-template-columns: 22mm 1fr; gap: 1mm 3mm; font-size: 9.2pt; }
.method .k { font-weight: 900; color: #d6336c; }
.mock .prob { margin-bottom: 3mm; }
.small { font-size: 8.5pt; color: #495057; }
"""

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" '
             'rel="stylesheet">')

page1 = f"""
<section class="page">
<div class="cover">
  <div class="kick">2학년 2학기 수학 수행평가 ② 대비</div>
  <h1>삼각형의 성질을 이용하여 도형 추측하기<br>— 실전 연습문제집</h1>
  <div class="sub">무게중심으로 삼각형 그리기 · 다른 방법으로 그리기 · 피타고라스 정리로 넓이가 같은 도형 그리기</div>
  <div class="name"><span>2학년 &nbsp;&nbsp;&nbsp;반</span><span>번호</span><span>이름</span></div>
</div>

<h3>평가 기준 분석 → 이 문제집의 구성</h3>
<table>
<tr><th style="width:18%">평가 항목</th><th>세부 평가 내용 (배점)</th><th style="width:30%">이 문제집에서 연습할 곳</th></tr>
<tr><td rowspan="2" style="text-align:center"><b>삼각형의<br>무게중심</b></td>
    <td>무게중심의 성질을 이용하여 주어진 조건에 맞게 삼각형을 그렸는가? <b>(8점)</b></td>
    <td><b>PART 1</b> (1-1 ~ 1-7)</td></tr>
<tr><td>무게중심의 성질을 이용하여 주어진 조건에 맞게 <u>다른 방법으로</u> 삼각형을 그렸는가? <b>(8점)</b></td>
    <td><b>PART 2</b> (2-1 ~ 2-5)<br><span class="small">같은 점을 다른 방법으로 / 다른 삼각형을</span></td></tr>
<tr><td style="text-align:center"><b>피타고라스의<br>정리</b></td>
    <td>주어진 넓이와 같은 도형을 조건에 맞게 그렸는가? <b>(4점)</b></td>
    <td><b>PART 3</b> (3-1 ~ 3-7)</td></tr>
<tr><td colspan="2" style="text-align:right"><b>실전 모의 수행평가 (20점) + 자기 채점표</b></td><td><b>PART 4</b></td></tr>
</table>

<div class="box warn"><b>⚠ 감점·0점 주의 (공지 내용)</b><br>
· 평가일: <b>11/12(목) ~ 11/13(금)</b> — 반별 시간표 꼭 확인! 결석 시 수학 선생님께 빨리 연락해 재응시 날짜 정하기<br>
· <b>백지 제출(백지에 준하는 경우 포함) = 1점</b> → 모르더라도 아는 성질·시도한 과정을 꼭 쓰기<br>
· <b>표절 등 부정행위 = 0점</b></div>

<div class="box tip"><b>✔ 만점 답안을 위한 6가지 습관</b><br>
① 모든 점에 이름(A, B, C, G, M …)을 쓴다 &nbsp; ② 중점은 같은 길이 표시(＝, ‖)를 한다<br>
③ 보조선은 점선, 답이 되는 삼각형은 진하게 &nbsp; ④ <b>"무게중심은 중선을 꼭짓점으로부터 2:1로 나누므로"</b>처럼 이용한 성질을 문장으로 쓴다<br>
⑤ 다 그린 뒤 <b>검산</b>(다른 중선도 G를 지나는지, 넓이가 맞는지) &nbsp; ⑥ 자와 컴퍼스를 꼭 챙긴다</div>

<h3>핵심 개념 ① 삼각형의 무게중심</h3>
<div class="cols">
<div style="text-align:center">{cf.svg(240)}</div>
<div>
<b>중선</b>: 꼭짓점과 마주 보는 변의 중점을 이은 선분<br>
<b>무게중심 G</b>: 세 중선이 만나는 한 점<br><br>
<b>성질 1</b> &nbsp;무게중심은 각 중선을 꼭짓점으로부터 <b>2 : 1</b>로 나눈다.<br>
&nbsp;&nbsp;&nbsp;{ov('AG')} : {ov('GM')} = 2 : 1, &nbsp;즉 {ov('AG')} = 2{ov('GM')}, {ov('AM')} = 3{ov('GM')}<br>
<b>성질 2</b> &nbsp;세 중선으로 나뉜 <b>6개의 삼각형의 넓이는 모두 같다.</b><br>
&nbsp;&nbsp;&nbsp;△GAB = △GBC = △GCA = ⅓ △ABC<br>
<b>성질 3</b> &nbsp;(모눈 검산법) 세 꼭짓점의 가로 칸 위치의 합 = G의 가로 칸 위치 × 3 (세로도 같음)
</div></div>
</section>
"""

page2 = f"""
<section class="page">
<h3>핵심 개념 ② 무게중심으로 삼각형을 그리는 5가지 방법 카드</h3>
<div class="cols">
<div class="method">
<div class="k">방법 A<br>중점→3배</div><div>알고 있는 두 꼭짓점의 중점 {it('M')}을 찾고, {it('M')}→{it('G')} 이동의 <b>2배</b>를 {it('G')}에서 더 가면 세 번째 꼭짓점. ({ov('MC')} = 3{ov('MG')})</div>
<div class="k">방법 B<br>꼭짓점→½</div><div>꼭짓점 {it('A')}→{it('G')} 이동의 <b>절반</b>만큼 {it('G')}에서 더 가면 마주 보는 변의 중점 {it('M')}. 그다음 {it('M')}에 대하여 대칭인 두 점을 {it('B')}, {it('C')}로.</div>
<div class="k">방법 C<br>다른 중선</div><div>꼭짓점 {it('A')} 말고 {it('B')}에서 그은 중선으로 {ov('AC')}의 중점 {it('N')}을 찾고, {it('A')}→{it('N')}만큼 한 번 더 가서 {it('C')}.</div>
<div class="k">방법 D<br>평행사변형</div><div>{it('A')}를 {it('G')}에 대해 대칭이동한 점 {it('D')}를 잡으면 □{it('GBDC')}는 평행사변형. ({ov('GD')}의 중점 = {ov('BC')}의 중점)</div>
<div class="k">방법 E<br>칸 수 계산</div><div>(검산용) {it('C')}의 위치 = 3×{it('G')} − {it('A')} − {it('B')} (가로·세로 따로 계산)</div>
</div>
<div style="text-align:center">{df.svg(200)}<div class="small">방법 D: {ov('AG')} = {ov('GD')}, □GBDC는 평행사변형</div></div>
</div>

<div class="box tip"><b>"다른 방법으로 그리기"(8점)는 두 가지로 출제될 수 있어요.</b><br>
(가) <b>같은 삼각형</b>을 다른 성질(다른 중선, 평행사변형, 작도 등)로 다시 그리기 → PART 2의 2-1, 2-3, 2-4<br>
(나) 같은 조건을 만족하는 <b>다른 모양의 삼각형</b> 그리기 → PART 2의 2-2, 2-5 &nbsp; ※ 어느 쪽이든 <b>무엇이 다른지</b>를 꼭 문장으로 쓰세요.</div>

<h3>핵심 개념 ③ 피타고라스 정리와 넓이</h3>
<div class="cols">
<div>
직각삼각형에서 직각을 낀 두 변의 길이를 {it('a')}, {it('b')}, 빗변의 길이를 {it('c')}라 하면<br>
<div style="text-align:center;font-size:13pt;margin:1.5mm 0"><b>{it('a')}² + {it('b')}² = {it('c')}²</b></div>
= <b>빗변 위의 정사각형 넓이 = 나머지 두 변 위의 정사각형 넓이의 합</b><br><br>
<b>모눈종이 공식</b>: 가로로 {it('p')}칸, 세로로 {it('q')}칸 이동한 선분을 한 변으로 하는 정사각형의 넓이 = <b>{it('p')}² + {it('q')}²</b><br>
<span class="small">확인 방법: (바깥 큰 정사각형) − (모서리 직각삼각형 4개). 오른쪽 그림: 9 − 4×1 = 5</span>
</div>
<div style="text-align:center">{pf.svg(150)}</div>
</div>
<table style="margin-top:2mm">
<tr><th>넓이</th><td>2</td><td>5</td><td>8</td><td>10</td><td>13</td><td>17</td><td>18</td><td>20</td><td>25</td><td>26</td><td>29</td><td>32</td></tr>
<tr><th>가로·세로 칸</th><td>1,1</td><td>1,2</td><td>2,2</td><td>1,3</td><td>2,3</td><td>1,4</td><td>3,3</td><td>2,4</td><td>3,4</td><td>1,5</td><td>2,5</td><td>4,4</td></tr>
</table>
<p class="small">※ 3, 6, 7, 11, 12 … 처럼 두 제곱수의 합으로 나타낼 수 없는 넓이의 정사각형은 꼭짓점이 모눈의 꼭짓점에 오도록 그릴 수 없습니다.
이때는 '넓이가 같은 도형'(예: 직사각형, 직각삼각형)을 이용하거나 작도로 해결합니다.</p>

<div class="box"><b>"주어진 넓이와 같은 도형" 문제 해결 순서</b><br>
① 주어진 도형(또는 조건)의 <b>넓이를 계산</b> → ② 그 수를 <b>두 제곱수의 합</b>으로 쪼개기 (예: 20 = 4 + 16) →
③ 가로·세로 이동으로 한 변을 그리고, 직각으로 돌려 나머지 변 완성 → ④ <b>큰 정사각형 − 삼각형 4개</b>로 넓이 검산</div>
<p class="legend">해설 그림 색: <b class="s">빨강 = 정답 도형</b> · <b class="a">파랑 = 보조선/무게중심</b> · <b class="g">초록 = 주어진 도형</b></p>
</section>
"""

part1 = f"""
<section class="page">
<h2>PART 1 <small>무게중심의 성질로 조건에 맞는 삼각형 그리기 (평가 ① 8점 대비)</small></h2>
{flow(P1, problem_html)}
</section>
"""
part2 = f"""
<section class="page">
<h2>PART 2 <small>무게중심의 성질로 '다른 방법으로' 삼각형 그리기 (평가 ② 8점 대비)</small></h2>
{flow(P2, problem_html)}
</section>
"""
part3 = f"""
<section class="page">
<h2>PART 3 <small>피타고라스 정리로 주어진 넓이와 같은 도형 그리기 (평가 ③ 4점 대비)</small></h2>
{flow(P3, problem_html)}
</section>
"""

mock = f"""
<section class="page mock">
<h2>PART 4 <small>실전 모의 수행평가 (20점) — 제한 시간 30분, 자와 컴퍼스 사용</small></h2>
<div class="row">
<div class="prob"><div class="ph"><span class="no">문항 1</span><span class="tag t-응용">8점</span></div>
<div class="pb">꼭짓점 {it('A')}와 △{it('ABC')}의 무게중심 {it('G')}가 있다. 변 {ov('BC')}가 <b>모눈의 세로선 위</b>에 있고 길이가 <b>8칸</b>인 △{it('ABC')}를 그리고, 무게중심의 성질을 이용하여 그리는 과정을 설명하시오.</div>
<div class="pf">{mf1.svg()}</div><div class="write" style="min-height:24mm">설명 :</div></div>
<div class="prob"><div class="ph"><span class="no">문항 2</span><span class="tag t-응용">8점</span></div>
<div class="pb">문항 1과 같은 점 {it('A')}, {it('G')}를 이용하여, <b>문항 1과 다른 방법으로</b> △{it('ABC')}를 그리되 이번에는 <b>∠B = 90°</b>가 되도록 하시오. 어떤 방법(성질)을 썼는지 설명하시오.</div>
<div class="pf">{mf2.svg()}</div><div class="write" style="min-height:24mm">설명 :</div></div>
</div>
<div class="row">
<div class="prob"><div class="ph"><span class="no">문항 3</span><span class="tag t-기본">4점</span></div>
<div class="pb">직각삼각형의 두 변 위에 넓이가 16, 9인 정사각형이 있다. <b>빗변을 한 변으로 하는 정사각형</b>을 그리고, 그 넓이가 두 정사각형 넓이의 합과 같음을 모눈의 칸 수를 이용하여 확인하시오.</div>
<div class="pf">{mf3.svg()}</div><div class="write">확인 :</div></div>
<div>
<h3 style="margin-top:0">자기 채점표</h3>
<table class="check">
<tr><th>평가 항목</th><th>체크 포인트</th><th>✔</th></tr>
<tr><td rowspan="3">문항 1<br>(8점)</td><td>{ov('BC')}의 중점 M을 2:1 성질로 정확히 찾았다</td><td class="c">□</td></tr>
<tr><td>{ov('BC')}가 세로선 위, 길이 8, M이 중점</td><td class="c">□</td></tr>
<tr><td>이용한 성질을 문장으로 썼다</td><td class="c">□</td></tr>
<tr><td rowspan="3">문항 2<br>(8점)</td><td>문항 1과 <b>다른 방법</b>을 썼다 (예: 평행사변형, 다른 중선)</td><td class="c">□</td></tr>
<tr><td>∠B = 90°, G가 무게중심인지 검산했다</td><td class="c">□</td></tr>
<tr><td>방법의 차이를 설명했다</td><td class="c">□</td></tr>
<tr><td rowspan="2">문항 3<br>(4점)</td><td>빗변 위에 정사각형을 정확히 그렸다</td><td class="c">□</td></tr>
<tr><td>49 − 4×6 = 25 = 16 + 9 확인</td><td class="c">□</td></tr>
<tr><th colspan="2" style="text-align:right">나의 예상 점수</th><td class="c" style="font-size:9pt">/20</td></tr>
</table>
</div>
</div>
</section>
"""

mock_sol = [
    dict(no="모의 1", title="문항 1 해설", solfig=ms1.svg(),
         sol=f"{it('A')}→{it('G')}(오른 4, 위 2)의 절반(오른 2, 위 1)만큼 {it('G')}에서 더 가면 {ov('BC')}의 중점 {it('M')}. "
             f"({ov('AG')} : {ov('GM')} = 2 : 1) → {it('M')}의 세로선 위에서 위·아래로 4칸씩 → {it('C')}, {it('B')}"),
    dict(no="모의 2", title="문항 2 해설", solfig=ms2.svg(),
         sol=f"[평행사변형 방법] {it('A')}를 {it('G')}에 대해 대칭이동한 {it('D')}를 잡으면 {ov('GD')}의 중점이 {ov('BC')}의 중점 {it('M')}. "
             f"∠B = 90°가 되려면 {it('B')}는 {it('A')}와 같은 가로줄, {it('M')}과 같은 세로줄 → {it('B')}, "
             f"□GBDC가 평행사변형이 되도록 {it('C')}. (검산: 가로 2+8+8 = 18 = 6×3, 세로 2+2+8 = 12 = 4×3)"),
    dict(no="모의 3", title="문항 3 해설", solfig=ms3.svg(),
         sol="빗변은 가로 4칸·세로 3칸 이동 → 그 변을 직각으로 돌려(가로 3·세로 4) 정사각형 완성. "
             "점선 큰 정사각형 7×7 = 49에서 직각삼각형 4개(각 6)를 빼면 49 − 24 = <b>25 = 16 + 9</b>"),
]

answers = f"""
<section class="page">
<h2>정답 및 해설 <small>PART 1</small></h2>
<p class="legend">그림 색: <b class="s">빨강 = 정답 도형</b> · <b class="a">파랑 = 보조선/무게중심</b> · <b class="g">초록 = 주어진 도형</b> · 같은 표시(｜, ‖)는 같은 길이</p>
{flow(P1, sol_html)}
</section>
<section class="page">
<h2>정답 및 해설 <small>PART 2</small></h2>
{flow(P2, sol_html)}
</section>
<section class="page">
<h2>정답 및 해설 <small>PART 3 · PART 4</small></h2>
{flow(P3, sol_html)}
<div class="trio" style="align-items:stretch">{''.join(sol_html(m) for m in mock_sol)}</div>
</section>
"""

html_doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>수행평가2 연습문제</title>{FONT_LINK}<style>{CSS}</style></head>
<body>{page1}{page2}{part1}{part2}{part3}{mock}{answers}</body></html>"""

with open(os.path.join(HERE, "practice.html"), "w", encoding="utf-8") as fh:
    fh.write(html_doc)
print("practice.html written")
