# 특집 A 양자정보와 양자컴퓨터

> 2025 "세계 양자 과학기술의 해" 기념 특집 · 관련 장: 29장(LC 진동), 36장(광자와 물질파), 37장(양자역학 입문), 38장(원자와 스핀)
> 국제연합(UN)은 하이젠베르크의 행렬역학(1925) 이후 100년이 되는 2025년을 "세계 양자 과학기술의 해"로 정했다. 36~38장을 먼저 훑어보기를 권하지만, 행렬 곱을 안다면 이 특집만 따로 읽어도 된다.

## 학습 목표
- 큐비트 상태를 복소 계수로 쓰고, 블로흐 구면 위의 점으로 나타낼 수 있다.
- 보른 규칙으로 측정 확률을 계산하고, 중첩과 "단순히 모르는 상태"의 차이를 설명할 수 있다.
- 텐서곱으로 여러 큐비트의 상태를 만들고, 곱 상태와 얽힌 상태를 구별할 수 있다.
- CHSH 부등식을 유도하고, 고전 한계 2와 양자역학의 값 $2\sqrt2$를 계산할 수 있다.
- H, X, CNOT 게이트로 벨 상태를 만드는 회로를 행렬로 계산하고 파이썬으로 시뮬레이션할 수 있다.
- 조지프슨 접합이 LC 회로를 비조화 진동자로 바꾸는 원리를 설명하고, 양자컴퓨터의 가능성과 한계를 과장 없이 말할 수 있다.

## 들어가며
고등학교에서 양자역학은 "에너지가 띄엄띄엄하다" 같은 문장으로 끝났다. 대학에서는 양자 상태를 **복소수 성분을 가진 벡터**로, 물리적 변화를 **행렬**로 다룬다. 큐비트는 이 수학이 가장 깨끗하게 드러나는 계이다. 2×2 행렬만으로 중첩, 측정, 얽힘, 간섭을 모두 계산할 수 있다. 1장의 오일러 공식 $e^{i\theta} = \cos\theta + i\sin\theta$가 여기서는 계산 편의가 아니라 물리 그 자체가 된다.

---

## A.1 큐비트

### 비트와 큐비트
고전적인 **비트**(bit)는 0 또는 1 가운데 하나의 값을 가진다. **큐비트**(qubit)는 구별되는 두 양자 상태 $|0\rangle$, $|1\rangle$을 가진 양자계이며, 일반적인 상태는 두 상태의 **중첩**(superposition)이다.

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle = \begin{pmatrix}\alpha\\ \beta\end{pmatrix}, \qquad \alpha, \beta \in \mathbb{C}, \quad |\alpha|^2 + |\beta|^2 = 1
$$

$\alpha$, $\beta$를 **확률 진폭**(probability amplitude)이라 한다. $|\psi\rangle$은 디랙의 **켓(ket)** 표기로, 지금은 열벡터의 다른 이름으로 보면 된다. 켤레 전치한 행벡터를 **브라(bra)** $\langle\psi| = (\alpha^*, \beta^*)$라 하고, 내적을 $\langle\phi|\psi\rangle = \phi_0^*\psi_0 + \phi_1^*\psi_1$로 쓴다.

큐비트는 전자나 원자핵의 **스핀 1/2**(38장), **광자의 편광** H/V(34장, 36장), 원자나 전기회로의 **가장 낮은 두 에너지 준위**(37장, A.6절) 등으로 만든다.

### 전역 위상과 블로흐 구면
복소수 두 개는 실수 4개이다. 정규화 조건으로 1개가 줄고, 상태 전체에 곱한 위상 인자 $e^{i\gamma}$(**전역 위상**, global phase)는 어떤 측정 확률도 바꾸지 않으므로 또 1개가 줄어든다. 따라서 모든 큐비트 상태는

$$
|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\varphi}\sin\frac{\theta}{2}|1\rangle, \qquad 0 \le \theta \le \pi,\quad 0 \le \varphi < 2\pi
$$

로 쓸 수 있다. $(\theta, \varphi)$를 구면좌표의 극각과 방위각으로 보면 상태는 단위 구면 위의 점 $\vec{r} = (\sin\theta\cos\varphi,\ \sin\theta\sin\varphi,\ \cos\theta)$에 대응한다. 이 구를 **블로흐 구면(Bloch sphere)**, $\vec{r}$을 **블로흐 벡터**라 한다. $|0\rangle$은 북극, $|1\rangle$은 남극이고, 적도 위에는

$$
|\pm\rangle = \frac{|0\rangle \pm |1\rangle}{\sqrt2}\ (\pm x\text{ 방향}), \qquad |\pm i\rangle = \frac{|0\rangle \pm i|1\rangle}{\sqrt2}\ (\pm y\text{ 방향})
$$

가 있다. $|+\rangle$과 $|-\rangle$은 $|0\rangle$, $|1\rangle$의 비율이 같지만 **상대 위상**(relative phase)이 $\pi$ 다르고, 구면에서 정반대 쪽에 있다. 상대 위상은 측정 기저를 바꾸면 확률 차이로 드러나는 진짜 물리량이다.

> **💡 개념 확인: 왜 $\theta$가 아니라 $\theta/2$인가**
> 직교하는 상태 $|0\rangle$과 $|1\rangle$은 블로흐 구면에서 $180°$ 떨어져 있다. 상태 공간에서 "직교"는 $90°$이므로 구면의 각은 상태 공간 각의 2배이고, 계수에는 $\theta/2$가 나온다.

### 파울리 행렬과 블로흐 벡터
**파울리 행렬(Pauli matrices)**

$$
X = \begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad Y = \begin{pmatrix}0&-i\\ i&0\end{pmatrix},\qquad Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

을 쓰면 블로흐 벡터는 기댓값으로 $\vec{r} = (\langle X\rangle, \langle Y\rangle, \langle Z\rangle)$이다($\langle X\rangle = \langle\psi|X|\psi\rangle$). 스핀 1/2에서는 $\vec{S} = \frac{\hbar}{2}(X, Y, Z)$이므로 블로흐 벡터는 **스핀 기댓값의 방향**이다(38장). 상태를 확률적으로만 아는 **혼합 상태**(mixed state)는 구의 내부($|\vec r| < 1$)에 대응한다. 예를 들어 50% $|0\rangle$, 50% $|1\rangle$인 혼합은 구의 중심이다.

### 예제 A.1 블로흐 구면 위의 위치
$|\psi\rangle = \frac{1}{\sqrt2}(|0\rangle + i|1\rangle)$은 블로흐 구면의 어디에 있는가? $\langle Y\rangle$을 계산해 확인하라.

**풀이** $\cos(\theta/2) = 1/\sqrt2$에서 $\theta = \pi/2$, $e^{i\varphi} = i$에서 $\varphi = \pi/2$이므로 $\vec{r} = (0, 1, 0)$, 곧 $+y$ 방향이다. 실제로 $Y|\psi\rangle = \frac{1}{\sqrt2}(-i\cdot i,\ i\cdot1)^T = |\psi\rangle$이므로 $\langle Y\rangle = 1$이다.

---

## A.2 중첩과 측정

### 보른 규칙
37장에서 $|\psi(x)|^2$이 확률밀도라고 배웠다. 큐비트에서는 더 단순하다. $\alpha|0\rangle + \beta|1\rangle$을 $\{|0\rangle, |1\rangle\}$ 기저(**계산 기저**, computational basis)로 측정하면 $P(0) = |\alpha|^2$, $P(1) = |\beta|^2$이고, 측정 직후 상태는 얻은 결과의 상태로 바뀐다(**상태 붕괴**). 일반적으로 정규직교 기저 $\{|\phi_k\rangle\}$로 측정하면

$$
P(k) = |\langle\phi_k|\psi\rangle|^2
$$

이다. 이것이 **보른 규칙**(Born rule)이다. 한 번 측정하면 결과 하나만 얻으므로, $\alpha$, $\beta$는 같은 상태를 **여러 번 준비해 측정한 통계**로만 알 수 있다. 측정 직후 같은 기저로 다시 재면 같은 결과가 나오지만, 다른 기저로 재면 상태가 바뀐다. 38장의 슈테른–게를라흐 장치를 $z$, $x$, $z$ 방향으로 연달아 통과시키면 마지막 $z$ 측정이 다시 50:50이 되는 것이 그 예이다.

### 예제 A.2 다른 기저에서의 측정
블로흐 각이 $(\theta, \varphi)$인 상태를 $\{|+\rangle, |-\rangle\}$ 기저($X$ 기저)로 측정할 때 $+$가 나올 확률을 구하라.

**풀이** $\langle +|\psi\rangle = \frac{1}{\sqrt2}\left(\cos\frac{\theta}{2} + e^{i\varphi}\sin\frac{\theta}{2}\right)$이므로
$$
P(+) = \frac{1}{2}\left(1 + 2\cos\varphi\cos\frac{\theta}{2}\sin\frac{\theta}{2}\right) = \frac{1 + \sin\theta\cos\varphi}{2} = \frac{1 + r_x}{2}
$$
일반적으로 블로흐 구면의 단위벡터 $\hat{n}$ 방향 상태를 "예"로 하는 측정의 확률은 $P = (1 + \vec{r}\cdot\hat{n})/2$이다. 예를 들어 $\theta = \pi/3$, $\varphi = \pi/4$이면 $\vec r = (0.612, 0.612, 0.5)$이므로 $P(+) = 0.806$, $P(0) = (1 + r_z)/2 = 0.75$이다.

> **💡 개념 확인: 중첩은 "둘 중 하나인데 모를 뿐"이 아니다**
> $|+\rangle$을 $Z$ 기저로 측정하면 0과 1이 반반 나온다. 그렇다면 $|+\rangle$은 동전 던지기 같은 50:50 혼합과 같을까? 아니다. $X$ 기저로 측정하면 $|+\rangle$은 **언제나** $+$가 나오지만, 50:50 혼합은 $X$ 기저에서도 반반이다. 차이는 상대 위상이 만드는 **간섭**(interference)이다. 36장 이중 슬릿에서 "어느 슬릿을 지났는지 확인하면 간섭무늬가 사라진다"는 것과 같은 이야기이다.

---

## A.3 여러 큐비트와 텐서곱

큐비트 두 개의 계산 기저는 $|00\rangle, |01\rangle, |10\rangle, |11\rangle$이고, 일반 상태는 $|\psi\rangle = \sum_{ij} c_{ij}|ij\rangle$, $\sum|c_{ij}|^2 = 1$이다. 이 책에서는 왼쪽 숫자를 첫째 큐비트(A), 오른쪽을 둘째 큐비트(B)로 쓴다. 소프트웨어마다 순서 관례가 다를 수 있으니 주의한다.

$n$큐비트에는 $2^n$개의 복소 진폭이 필요하다. 복소수 하나에 16바이트를 쓰면 30큐비트는 약 17 GB, 50큐비트는 약 18 PB가 필요하다. 저장 자체가 지수적으로 어려워진다는 점이 양자컴퓨터 아이디어의 출발점이다.

따로 준비된 두 큐비트 $|a\rangle$, $|b\rangle$를 합친 상태는 **텐서곱**(tensor product)이다.

$$
|a\rangle\otimes|b\rangle = (a_0 b_0,\ a_0 b_1,\ a_1 b_0,\ a_1 b_1)^T
$$

첫째 큐비트에만 $U$를 작용시키는 연산은 $U\otimes I$이다. numpy에서는 `np.kron`이 이 계산을 한다. 둘 중 첫째만 측정하면 0이 나올 확률은 $P_A(0) = |c_{00}|^2 + |c_{01}|^2$이고, 측정 뒤 상태는 해당 성분만 남겨 다시 정규화한 것이다.

### 예제 A.3 텐서곱과 부분 측정
$|+\rangle\otimes|0\rangle$을 계산 기저로 전개하고, 첫째 큐비트에서 1을 얻었을 때 둘째 큐비트의 상태를 구하라.

**풀이** $\frac{1}{\sqrt2}(1, 1)^T\otimes(1, 0)^T = \frac{1}{\sqrt2}(1, 0, 1, 0)^T = \frac{1}{\sqrt2}(|00\rangle + |10\rangle)$. 첫째가 1이면 $|10\rangle$만 남으므로 둘째는 $|0\rangle$이다. 결과가 0이어도 마찬가지이다. 곱 상태에서는 한쪽의 측정이 다른 쪽에 아무 영향도 주지 않는다.

---

## A.4 얽힘과 벨 부등식

### 곱 상태와 얽힌 상태
$|a\rangle\otimes|b\rangle$ 꼴로 쓰이면 **곱 상태(product state)**, 그렇게 쓸 수 없으면 **얽힌 상태**(entangled state)이다. 곱 상태는 $c_{ij} = a_ib_j$이므로 반드시 $c_{00}c_{11} - c_{01}c_{10} = 0$이고, 역도 성립한다(연습문제 8). 즉 계수 행렬 $(c_{ij})$의 **행렬식이 0이 아니면 얽힌 상태**이다. 대표적인 얽힌 상태는 네 개의 **벨 상태**(Bell states)이다.

$$
|\Phi^\pm\rangle = \frac{|00\rangle \pm |11\rangle}{\sqrt2}, \qquad |\Psi^\pm\rangle = \frac{|01\rangle \pm |10\rangle}{\sqrt2}
$$

### 예제 A.4 얽힘 판별
(가) $|\Phi^+\rangle$, (나) $\frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$은 얽힌 상태인가?

**풀이** (가) $\frac{1}{2} - 0 \neq 0$이므로 얽힌 상태. (나) $\frac{1}{4} - \frac{1}{4} = 0$이므로 곱 상태이고, 실제로 $|+\rangle\otimes|+\rangle$이다.

### 얽힘이 만드는 상관
$|\Phi^+\rangle$의 두 큐비트를 모두 $Z$ 기저로 측정하면 00 또는 11이 반반 나오고, 두 결과는 항상 같다. 이것은 "둘 다 0" 또는 "둘 다 1"이라고 적은 쪽지를 미리 나눠 가져도 흉내 낼 수 있다. 그런데 $|\Phi^+\rangle = \frac{1}{\sqrt2}(|{+}{+}\rangle + |{-}{-}\rangle)$이기도 하므로 $X$ 기저로 측정해도 결과가 항상 같다. 쪽지에 모든 측정 방향의 답을 미리 적어 두는 방식으로 이런 상관을 흉내 낼 수 있을까? 이 질문에 정량적인 답을 준 것이 벨 부등식이다.

1935년 아인슈타인·포돌스키·로젠(EPR)은 이런 상관을 근거로 숨은 변수가 있어야 한다고 주장했다. 1964년 벨(J. S. Bell)은 **국소적 숨은 변수 이론(local hidden variable theory)**, 곧 ① 측정 결과는 측정 전에 정해져 있고 ② 한쪽의 측정 설정이 멀리 떨어진 다른 쪽 결과에 영향을 주지 않는다는 가정이 실험으로 검증 가능한 부등식을 만족함을 보였다.

### CHSH 부등식: 고전 한계 2
1969년 클라우저·혼·시모니·홀트(CHSH)가 다듬은 형태를 유도하자. 앨리스는 설정 $a$나 $a'$를, 밥은 $b$나 $b'$를 골라 측정하고, 결과는 $\pm1$이다. 국소적 숨은 변수 이론에서는 각 쌍이 네 답 $A, A', B, B' \in \{\pm1\}$을 미리 가지고 출발한다. 그러면

$$
s = AB + AB' + A'B - A'B' = A(B + B') + A'(B - B')
$$

에서 $B + B'$와 $B - B'$ 중 하나는 0, 다른 하나는 $\pm2$이므로 모든 쌍에서 $s = \pm2$이다. 평균을 취하면 상관함수 $E(a, b) = \langle AB\rangle$에 대해

$$
\boxed{\,|S| = |E(a,b) + E(a,b') + E(a',b) - E(a',b')| \le 2\,}
$$

이다. 이것이 **CHSH 부등식**이다. 가능한 결정론적 답의 조합은 16가지뿐이고 확률적 전략은 이들을 섞은 것이므로, 숨은 변수가 확률적으로 분포해도 결론은 같다.

### 양자역학의 예측: $2\sqrt2$
블로흐 구면의 $x$-$z$ 평면에서 $z$축과 각 $\theta$를 이루는 방향의 측정은 관측가능량 $\sigma_\theta = \cos\theta\,Z + \sin\theta\,X$(고윳값 $\pm1$)에 해당한다. $|\Phi^+\rangle$에서 $\langle Z\otimes Z\rangle = \langle X\otimes X\rangle = 1$, $\langle Z\otimes X\rangle = \langle X\otimes Z\rangle = 0$이므로

$$
E(a, b) = \langle\Phi^+|\sigma_a\otimes\sigma_b|\Phi^+\rangle = \cos a\cos b + \sin a\sin b = \cos(a - b)
$$

이다. $a = 0$, $a' = \pi/2$, $b = \pi/4$, $b' = -\pi/4$로 고르면

$$
S = \cos\frac{\pi}{4} + \cos\frac{\pi}{4} + \cos\frac{\pi}{4} - \cos\frac{3\pi}{4} = 2\sqrt2 \approx 2.83
$$

으로 고전 한계 2를 넘는다. 1980년 치렐손(B. Tsirelson)은 양자역학이 허용하는 최댓값이 정확히 $2\sqrt2$임을 증명했다(**치렐손 한계**, 연습문제 13). 실험에서 $|S| > 2$가 나오면 두 가정 가운데 적어도 하나는 틀린 것이다. 광자 편광 실험에서는 편광판을 $\alpha$ 돌리면 블로흐 구면에서 $2\alpha$ 돌기 때문에 편광판 각도 $0°, 45°$와 $\pm22.5°$를 쓴다.

> **💡 개념 확인: 얽힘으로 빛보다 빠른 통신을 할 수 있는가**
> 없다. 앨리스가 어떤 설정을 고르든 밥이 자기 큐비트만 보고 얻는 확률은 언제나 반반이다(연습문제 7). 상관은 나중에 고전 통신으로 결과를 비교할 때에만 드러난다(**신호 불가 정리**, no-signaling).

> **🔬 최신 연구 노트: 2022 노벨 물리학상 — 얽힌 광자와 벨 부등식 위배**
> 2022년 노벨 물리학상은 아스펙트(Alain Aspect), 클라우저(John F. Clauser), 차일링거(Anton Zeilinger)에게 "얽힌 광자 실험으로 벨 부등식의 위배를 확립하고 양자정보과학을 개척한 공로"로 주어졌다. 클라우저는 1972년 프리드먼(S. Freedman)과 함께 원자에서 나온 광자 쌍으로 벨 부등식 위배를 처음 관측했다. 아스펙트는 1980년대 초 광자가 날아가는 동안 측정 설정을 바꾸어 국소성의 허점을 줄였다. 차일링거는 양자 순간이동(1997) 같은 양자정보 실험을 이끌었다. 2015년에는 여러 연구진이 검출 효율과 국소성의 허점을 동시에 막은 벨 실험을 보고했다. 결과는 모두 양자역학의 예측과 맞고 국소적 숨은 변수 이론과는 맞지 않는다.

---

## A.5 양자 게이트와 회로

### 게이트는 유니터리 행렬이다
고립된 양자계는 슈뢰딩거 방정식 $i\hbar\,\partial_t|\psi\rangle = \hat{H}|\psi\rangle$을 따르고(37장), $\hat H$가 일정하면 $|\psi(t)\rangle = e^{-i\hat{H}t/\hbar}|\psi(0)\rangle$이다. $U = e^{-i\hat{H}t/\hbar}$는 **유니터리(unitary)**, 곧 $U^\dagger U = I$이므로 정규화를 보존하고 언제나 되돌릴 수 있다. **양자 게이트**(quantum gate)는 해밀토니안을 정해진 시간 동안 조절해 원하는 $U$를 만드는 일이다. 예를 들어 전이 진동수에 맞춘 마이크로파나 레이저 펄스를 쪼이면 블로흐 벡터가 회전한다(라비 진동).

| 게이트 | 행렬 | 작용 | 블로흐 구면에서 |
|---|---|---|---|
| X (NOT) | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | $\lvert 0\rangle\leftrightarrow\lvert 1\rangle$ | $x$축 둘레 $180°$ 회전 |
| Z | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | $\lvert 1\rangle\to-\lvert 1\rangle$ | $z$축 둘레 $180°$ 회전 |
| H (아다마르) | $\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ | $\lvert 0\rangle\to\lvert +\rangle$, $\lvert 1\rangle\to\lvert -\rangle$ | $(\hat{x}+\hat{z})/\sqrt2$ 축 둘레 $180°$ 회전 |
| 위상 $R_\phi$ | $\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix}$ | $\lvert 1\rangle$에 $e^{i\phi}$를 곱함 | $z$축 둘레 $\phi$ 회전 |

**아다마르 게이트(Hadamard gate)** H는 계산 기저와 $X$ 기저를 서로 바꾼다($H^2 = I$, $HZH = X$). 그래서 "$X$ 기저 측정"은 실제로는 "H를 건 뒤 $Z$ 기저 측정"으로 구현한다.

두 큐비트 게이트의 대표는 **제어 NOT**(CNOT)이다. 제어 큐비트가 $|1\rangle$일 때만 표적 큐비트를 뒤집는다: $|c, t\rangle \to |c, t\oplus c\rangle$($\oplus$는 XOR). 첫째 큐비트가 제어이면

$$
\text{CNOT} = \begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}
$$

이다. 1큐비트 게이트들과 CNOT을 조합하면 임의의 다중 큐비트 유니터리를 원하는 정밀도로 근사할 수 있다(**보편 게이트 집합**).

### 벨 상태 만들기
가장 단순하고 중요한 회로는 H 다음 CNOT이다. 시간은 왼쪽에서 오른쪽으로 흐르고, ●은 제어, ⊕는 표적이다.

```
A: |0> ──[H]──●──
              │
B: |0> ───────⊕──
```

$$
|00\rangle \xrightarrow{H\otimes I} \frac{|00\rangle + |10\rangle}{\sqrt2} \xrightarrow{\text{CNOT}} \frac{|00\rangle + |11\rangle}{\sqrt2} = |\Phi^+\rangle
$$

H가 중첩을 만들고 CNOT이 그 중첩을 둘째 큐비트와 상관시켜 얽힘을 만든다. 입력이 $|01\rangle$, $|10\rangle$, $|11\rangle$이면 각각 $|\Psi^+\rangle$, $|\Phi^-\rangle$, $|\Psi^-\rangle$가 나온다(연습문제 5).

### 예제 A.5 회로를 거꾸로 돌리기
$|\Phi^-\rangle$에 CNOT을 걸고 이어서 첫째 큐비트에 H를 걸면 무엇이 되는가?

**풀이** CNOT은 $|11\rangle\to|10\rangle$이므로 $|\Phi^-\rangle \to (|00\rangle - |10\rangle)/\sqrt2 = |-\rangle|0\rangle$이고, H가 $|-\rangle\to|1\rangle$이므로 결과는 $|10\rangle$이다. 생성 회로를 거꾸로 돌리면 네 벨 상태가 네 계산 기저 상태로 하나씩 대응된다. 이것이 **벨 측정**(Bell measurement)이며 양자 순간이동(A.8절)에 쓰인다.

> **★ 심화: 복제 불가 정리**
> 임의의 미지 상태를 복사하는 유니터리 $U|\psi\rangle|0\rangle = |\psi\rangle|\psi\rangle$은 존재하지 않는다(**복제 불가 정리**, no-cloning theorem, 1982). $U$가 $|0\rangle$과 $|1\rangle$을 복사한다면 선형성 때문에 $U|+\rangle|0\rangle = \frac{1}{\sqrt2}(|00\rangle + |11\rangle)$이지만, 복사되었다면 $|+\rangle|+\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$이어야 하므로 모순이다. CNOT이 바로 이 예이다. 이 정리는 양자 암호(A.8절)와 오류 정정(A.7절)으로 이어진다.

> **🐍 파이썬 실습: numpy만으로 만드는 2큐비트 상태 벡터 시뮬레이터**
> $|00\rangle$에서 출발해 H와 CNOT으로 벨 상태를 만들고, 보른 규칙으로 측정 확률을 계산하고, 측정 1000회를 흉내 낸 뒤, CHSH 값을 계산한다.
> ```python
> import numpy as np
>
> # 1큐비트 기본 상태와 게이트
> ket0 = np.array([1, 0], dtype=complex)
> I = np.eye(2)
> X = np.array([[0, 1], [1, 0]])
> Z = np.array([[1, 0], [0, -1]])
> H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
> CNOT = np.array([[1, 0, 0, 0],      # 제어: 첫째(왼쪽) 큐비트
>                  [0, 1, 0, 0],
>                  [0, 0, 0, 1],
>                  [0, 0, 1, 0]])
>
> psi = np.kron(ket0, ket0)           # |00>
> psi = np.kron(H, I) @ psi           # 첫째 큐비트에 H
> psi = CNOT @ psi                    # CNOT -> 벨 상태
> print("상태 벡터:", np.round(psi.real, 4))
>
> probs = np.abs(psi)**2              # 보른 규칙
> for label, p in zip(["00", "01", "10", "11"], probs):
>     print(f"P({label}) = {p:.3f}")
>
> rng = np.random.default_rng(seed=1) # 측정 1000회 흉내
> shots = rng.choice(4, size=1000, p=probs)
> print("1000회 측정 횟수 [00,01,10,11]:", np.bincount(shots, minlength=4))
>
> def A(theta):                       # x-z 평면에서 각 theta 방향의 측정
>     return np.cos(theta)*Z + np.sin(theta)*X
>
> def E(a, b):                        # 상관함수 <A(a) ⊗ A(b)>
>     return np.vdot(psi, np.kron(A(a), A(b)) @ psi).real
>
> a, a2, b, b2 = 0, np.pi/2, np.pi/4, -np.pi/4
> S = E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2)
> print(f"E(a,b) = {E(a, b):.4f}")
> print(f"CHSH S = {S:.4f},  2*sqrt(2) = {2*np.sqrt(2):.4f}")
> ```
> 실행 결과: 상태 벡터 `[0.7071 0. 0. 0.7071]`, $P(00) = P(11) = 0.500$, $P(01) = P(10) = 0.000$. 1000회 측정에서 00이 507회, 11이 493회 나오고 01과 10은 한 번도 나오지 않는다(`seed=1` 기준). $E(a,b) = 0.7071 = \cos(\pi/4)$이고 $S = 2.8284 = 2\sqrt2$이다. 각도 `b, b2`를 바꾸어 보라. 어떤 각도에서도 $2\sqrt2$를 넘지 못한다.

---

## A.6 초전도 큐비트와 여러 가지 플랫폼

### LC 회로는 왜 큐비트가 아닌가
29장의 LC 회로 에너지 $\mathcal{E} = \frac{Q^2}{2C} + \frac{\Phi^2}{2L}$($\Phi = LI$)은 질량–용수철의 $\frac{p^2}{2m} + \frac{1}{2}kx^2$과 같은 꼴이다. 회로 전체를 양자역학으로 다루면 37장의 **양자 조화 진동자**가 되어 $E_n = \hbar\omega_0(n + \frac{1}{2})$, $\omega_0 = 1/\sqrt{LC}$로 준위가 **등간격**이다. 그러면 진동수 $\omega_0$의 마이크로파가 $0\to1$뿐 아니라 $1\to2$, $2\to3$ 전이도 똑같이 일으키므로 두 준위만 떼어 쓸 수 없다. 필요한 것은 간격이 서로 다른 준위, 곧 **비조화성**(anharmonicity)이다.

### 조지프슨 접합: 손실 없는 비선형 인덕터
초전도체에서는 전자가 **쿠퍼 쌍**(Cooper pair, 전하 $2e$)을 이루어 위상을 가진 거시적 파동함수처럼 행동한다. 두 초전도체 사이에 얇은 절연막을 끼운 **조지프슨 접합**(Josephson junction)에서는 쿠퍼 쌍이 막을 터널링하고(37장), 양쪽의 위상차 $\varphi$에 대해

$$
I = I_c\sin\varphi, \qquad V = \frac{\hbar}{2e}\frac{d\varphi}{dt}
$$

가 성립한다($I_c$는 임계 전류). 첫째 식을 미분하고 둘째 식을 넣으면

$$
\frac{dI}{dt} = I_c\cos\varphi\cdot\frac{2e}{\hbar}V \quad\Rightarrow\quad V = L_J\frac{dI}{dt},\qquad L_J = \frac{\hbar}{2eI_c\cos\varphi}
$$

이다. 조지프슨 접합은 **인덕턴스가 위상에 따라 변하는 비선형 인덕터**이고, 저항이 없어 에너지를 잃지 않는다. 저장 에너지는 $\int IV\,dt = -E_J\cos\varphi$($E_J = \hbar I_c/2e$)로, 포물선 대신 코사인 모양이다.

$$
-E_J\cos\varphi = -E_J + \frac{E_J}{2}\varphi^2 - \frac{E_J}{24}\varphi^4 + \cdots
$$

$-\varphi^4$ 항은 우물을 위쪽에서 포물선보다 넓게 만든다. 넓은 우물일수록 준위 간격이 좁으므로(37장 상자 속 입자) 위로 갈수록 간격이 줄어드는 **비등간격 준위**가 생긴다.

### 트랜스몬
조지프슨 접합에 축전기를 병렬로 단 회로(널리 쓰이는 **트랜스몬**, transmon 큐비트의 기본 구조)의 해밀토니안은

$$
\hat{H} = 4E_C(\hat{n} - n_g)^2 - E_J\cos\hat{\varphi}, \qquad E_C = \frac{e^2}{2C}
$$

이다. $\hat{n}$은 통과한 쿠퍼 쌍의 수, $n_g$는 바깥 전압이 정하는 오프셋이고, $\hat{n}$과 $\hat{\varphi}$는 위치와 운동량처럼 짝을 이룬다. $E_J \gg E_C$이면 근사적으로

$$
E_{01} \approx \sqrt{8E_JE_C} - E_C, \qquad E_{12} - E_{01} \approx -E_C
$$

이다. $\sqrt{8E_JE_C}$는 $L_J$(작은 위상)와 $C$로 만든 LC 회로의 $\hbar\omega_0$이다(연습문제 12).

> **🐍 파이썬 실습: 트랜스몬의 에너지 준위**
> 전하 기저 $|n\rangle$에서 $\cos\hat{\varphi} = \frac{1}{2}\sum_n(|n\rangle\langle n+1| + |n+1\rangle\langle n|)$이므로, 해밀토니안은 대각선에 $4E_C(n - n_g)^2$, 바로 옆 대각선에 $-E_J/2$가 놓인 행렬이다.
> ```python
> import numpy as np
>
> def transmon_levels(EJ_over_EC, ng=0.0, N=30, k=4):
>     """전하 기저에서 H = 4E_C(n-ng)^2 - E_J cos(phi)를 대각화 (E_C = 1 단위)"""
>     n = np.arange(-N, N + 1)
>     Hm = np.diag(4.0*(n - ng)**2)
>     Hm -= EJ_over_EC/2 * (np.eye(2*N + 1, k=1) + np.eye(2*N + 1, k=-1))
>     E = np.linalg.eigvalsh(Hm)[:k]
>     return E - E[0]
>
> for r in [1, 10, 50]:
>     E = transmon_levels(r)
>     E01, E12 = E[1] - E[0], E[2] - E[1]
>     print(f"E_J/E_C = {r:3d}: E01 = {E01:7.3f}, E12 = {E12:7.3f}, "
>           f"비조화성 E12-E01 = {E12 - E01:6.3f}  (단위 E_C)")
> print("근사식 sqrt(8*50) - 1 =", np.sqrt(8*50) - 1)
> ```
> 결과($E_C$ 단위): $E_J/E_C = 50$에서 $E_{01} = 18.942$, $E_{12} = 17.793$, 비조화성 $-1.149$로 근사식($19.0$, $-1$)에 가깝다. $E_J/E_C = 10$이면 비조화성 $-2.550$, $1$이면 $-3.979$이다. $E_J/E_C$가 작으면 비조화성은 크지만 준위가 $n_g$(주변 전하의 요동)에 민감해진다(`ng=0.25`로 비교해 보라). 트랜스몬은 $E_J/E_C$를 크게 하여 전하 잡음 민감도를 줄이고 비조화성 $\approx -E_C$는 남기는 절충안이다.

### 예제 A.6 트랜스몬 숫자 감각
예시로 $E_J/h = 15\ \text{GHz}$, $E_C/h = 0.3\ \text{GHz}$($E_J/E_C = 50$)인 회로를 생각하자. (가) $I_c$와 $C$, (나) $0\to1$ 전이 진동수, (다) 열적 들뜸을 피하려면 온도가 얼마보다 충분히 낮아야 하는지 구하라.

**풀이**
(가) $I_c = 2eE_J/\hbar = 4\pi e\,(E_J/h) \approx 30\ \text{nA}$, $C = e^2/(2E_C) \approx 65\ \text{fF}$. 검산: $L_J = \hbar/2eI_c \approx 11\ \text{nH}$, $1/(2\pi\sqrt{L_JC}) = 6.0\ \text{GHz} = \sqrt{8E_JE_C}/h$.
(나) 파이썬 결과 $E_{01} = 18.94E_C$에서 $f_{01} \approx 5.68\ \text{GHz}$. $1\to2$ 전이는 이보다 약 $0.34\ \text{GHz}$ 낮다.
(다) $hf_{01}/k_B \approx 0.27\ \text{K}$. 볼츠만 인자 $e^{-hf/k_BT}$가 충분히 작으려면 $T$가 이보다 훨씬 낮아야 한다. $T = 20\ \text{mK}$이면 $e^{-13.6} \approx 1\times10^{-6}$이다. 그래서 초전도 큐비트는 **희석 냉동기**(dilution refrigerator)로 수십 mK 수준까지 냉각해 운용한다.

> **🔬 최신 연구 노트: 2025 노벨 물리학상 — 전기회로 속의 양자역학**
> 2025년 노벨 물리학상은 클라크(John Clarke), 드보레(Michel H. Devoret), 마티니스(John M. Martinis)에게 "for the discovery of macroscopic quantum mechanical tunnelling and energy quantisation in an electric circuit(전기회로에서 거시적 양자 터널링과 에너지 양자화를 발견한 공로)"로 주어졌다. 세 사람은 1984~85년 캘리포니아 대학교 버클리에서 전류를 흘린 조지프슨 접합을 극저온에서 실험했다. 위상차 $\varphi$는 기울어진 빨래판 모양 퍼텐셜 $U(\varphi) = -E_J\cos\varphi - (\hbar I/2e)\varphi$의 한 우물에 갇혀 있고(접합 전압 0), 우물을 벗어나면 전압이 나타난다. 온도를 낮추자 탈출률이 온도와 무관한 값에 머물렀다. 열적으로 장벽을 넘는 것이 아니라 **수많은 쿠퍼 쌍의 집단 변수인 $\varphi$가 장벽을 터널링**한다는 뜻이다. 또 특정 진동수의 마이크로파를 쪼이면 탈출이 공명적으로 늘어나, 우물 속 에너지가 **띄엄띄엄한 준위로 양자화**되어 있음을 보였다. 손에 쥘 수 있는 회로가 원자처럼 양자역학을 따른다는 이 결과는 초전도 큐비트의 기반이 되었다(29장, 37장).

### 여러 가지 큐비트 플랫폼
성능 수치는 빠르게 바뀌므로 원리만 비교한다.

| 플랫폼 | 큐비트와 게이트 | 장점 | 어려운 점 |
|---|---|---|---|
| 초전도 회로 | 조지프슨 회로, 마이크로파 펄스 | 반도체 공정으로 제작, 빠른 게이트 | 극저온, 짧은 결맞음 시간 |
| 포획 이온 | 가둔 이온의 내부 준위, 레이저 | 모든 이온이 똑같음, 긴 결맞음 시간 | 느린 게이트, 많은 이온 제어 |
| 광자 | 편광·경로, 빔 분할기 | 상온 전송, 통신에 적합 | 광자끼리 상호작용이 약함, 손실 |
| 중성 원자 | 광집게 속 원자, 뤼드베리 상태 | 많은 원자 배열이 쉬움 | 원자 손실, 레이저 정밀도 |

이 밖에 반도체 양자점 속 전자 스핀을 쓰는 방식도 연구된다.

---

## A.7 양자컴퓨터가 할 수 있는 일과 한계

> **💡 개념 확인: "모든 경우를 동시에 계산한다"는 설명의 함정**
> $n$큐비트가 $2^n$개 기저 상태의 중첩에 있을 수 있는 것은 맞다. 그러나 측정하면 그중 **하나**만 얻고, $n$큐비트에서 읽어 낼 수 있는 고전 정보는 최대 $n$비트이다(홀레보 한계). 양자 알고리즘의 핵심은 **간섭을 설계해 틀린 답의 진폭은 상쇄시키고 원하는 답의 진폭은 키우는 것**이다. 그런 구조를 가진 문제에서만 이득이 있으며, 양자컴퓨터가 일반적인 계산에서 고전 컴퓨터를 대체하는 것은 아니다.

**양자 시뮬레이션.** 1980년대 초 파인만(R. Feynman)은 양자계를 고전 컴퓨터로 흉내 내려면 지수적 자원이 필요하므로(A.3절) 양자 장치로 흉내 내자고 제안했다. 분자의 전자 구조나 고체 속 강하게 상호작용하는 전자계는 가장 자연스러운 응용 후보이며, 실용적 이득이 언제 어떤 문제에서 나타날지는 아직 연구 중이다.

**쇼어 알고리즘.** 1994년 쇼어(P. Shor)는 정수의 소인수분해를 자릿수에 대해 **다항 시간**에 하는 양자 알고리즘을 발표했다. 알려진 최선의 고전 알고리즘은 자릿수가 늘 때 어떤 다항식보다도 빠르게 시간이 늘어난다. RSA 공개키 암호는 소인수분해의 어려움에 기대므로, 충분히 큰 오류 정정 양자컴퓨터가 생기면 위협이 된다. 그래서 **양자 내성 암호**(post-quantum cryptography)로 바꾸는 작업이 진행되고 있다. 알고리즘의 구조는 "소인수분해를 **주기 찾기**로 바꾸고, 주기는 양자 푸리에 변환으로 찾는다"이다. $a^r \equiv 1 \pmod N$인 가장 작은 $r$을 알면 $\gcd(a^{r/2} \pm 1, N)$이 인수가 되는 경우가 많다. 예: $N = 15$, $a = 7$이면 $7^k \bmod 15$가 $7, 4, 13, 1$로 $r = 4$이고, $7^2 \equiv 4$에서 $\gcd(3, 15) = 3$, $\gcd(5, 15) = 5$이다. 양자컴퓨터가 빠르게 하는 부분은 주기 찾기뿐이다.

**그로버 알고리즘.** 구조 없는 $N$개 항목 중 하나를 찾을 때 고전적으로는 평균 $N/2$번 확인해야 한다. 1996년 그로버(L. Grover)는 약 $\frac{\pi}{4}\sqrt N$번으로 찾는 알고리즘을 발표했다. ① **오라클**이 답의 진폭 부호를 뒤집고 ② **확산**이 모든 진폭을 평균에 대해 뒤집는다($2|s\rangle\langle s| - I$, $|s\rangle$는 균일 중첩). 두 반사를 합치면 상태가 매번 각 $2\theta$($\sin\theta = 1/\sqrt N$)만큼 답 쪽으로 회전한다. 이득은 **제곱근 수준**이고, 구조 없는 탐색에서는 이보다 빠를 수 없음이 증명되어 있다.

> **🐍 파이썬 실습: 그로버 탐색**
> ```python
> import numpy as np
>
> def grover(n, marked, iters):
>     N = 2**n
>     s = np.ones(N) / np.sqrt(N)              # 균일 중첩 (H를 n개 적용한 결과)
>     psi = s.copy()
>     for _ in range(iters):
>         psi[marked] *= -1                    # 오라클: 표시된 항목의 부호 반전
>         psi = 2*s*(s @ psi) - psi            # 확산: 평균에 대한 반전 2|s><s| - I
>     return np.abs(psi[marked])**2
>
> for n in [2, 4, 8, 10]:
>     N = 2**n
>     k = int(np.floor(np.pi/4*np.sqrt(N)))    # 최적 반복 횟수
>     print(f"n = {n:2d}, N = {N:5d}: 반복 {k:3d}회 후 성공 확률 {grover(n, 3, k):.4f}")
> ```
> 결과: $N = 4$는 1회 반복으로 성공 확률 1.0000, $N = 16$은 3회에 0.9613, $N = 256$은 12회에 0.9999, $N = 1024$는 25회에 0.9995이다. 반복을 너무 많이 하면 회전이 지나쳐 확률이 다시 줄어든다. `k`를 바꾸어 확인해 보라.

### 결어긋남과 오류 정정
큐비트가 주변 환경(열, 잡음, 재료 결함)과 얽히면 중첩의 위상 정보가 사라져 혼합 상태가 된다. 이를 **결어긋남**(decoherence)이라 하며, 두 시간 척도로 나타낸다. $T_1$(**에너지 이완 시간**)은 $|1\rangle$이 $|0\rangle$으로 떨어지는 시간, $T_2$(**위상 결맞음 시간**)는 상대 위상이 무작위해지는 시간이다. 게이트와 측정의 부정확성도 더해지고, 오류는 계산이 길수록 쌓인다.

양자에서는 복사해 다수결을 할 수 없고 측정하면 상태가 망가지는데도 오류 정정이 가능하다는 것이 1990년대 중반의 중요한 발견이다. 가장 간단한 **3큐비트 비트 반전 부호**는 논리 큐비트를 $\alpha|0\rangle + \beta|1\rangle \to \alpha|000\rangle + \beta|111\rangle$로 **얽힘을 이용해 퍼뜨린다**(세 번 복사한 상태와는 다르다). 둘째 큐비트가 뒤집혀 $\alpha|010\rangle + \beta|101\rangle$이 되면, "1번과 2번이 같은가", "2번과 3번이 같은가"($Z_1Z_2$, $Z_2Z_3$)만 측정해 $\alpha$, $\beta$에 대한 정보 없이 오류 위치를 알 수 있다(**신드롬 측정**). 그 큐비트에 X를 걸면 복구된다. 위상 오류까지 막으려면 쇼어의 9큐비트 부호, 표면 부호 같은 더 큰 부호가 필요하다.

**문턱 정리**(threshold theorem)에 따르면 물리적 오류율이 어떤 문턱값보다 낮으면 물리 큐비트를 더 써서 논리 큐비트의 오류율을 원하는 만큼 낮출 수 있다. 대가로 논리 큐비트 하나에 많은 물리 큐비트가 필요하다. 오류 정정이 충분하지 않은 현재의 장치를 프레스킬(J. Preskill)은 NISQ(잡음이 있는 중간 규모 양자) 장치라고 불렀다. 쇼어 알고리즘처럼 긴 계산을 할 오류 정정 양자컴퓨터는 아직 연구·개발 단계이다.

---

## A.8 양자 센싱과 양자 통신

### 양자 센싱
환경에 민감하다는 약점은 거꾸로 **아주 작은 신호를 재는 장점**이 된다. 양자 상태의 위상은 자기장, 시간, 중력에 따라 변하고 간섭으로 읽어 낼 수 있다.
- **원자시계**: SI의 초는 세슘-133 원자의 바닥상태 초미세 전이 진동수를 $9\,192\,631\,770\ \text{Hz}$로 정의한다(2장). 원자의 두 준위가 곧 큐비트이다(38장).
- **SQUID**: 조지프슨 접합을 고리에 넣은 초전도 양자 간섭 소자로, 선속 양자 $\Phi_0 = h/2e \approx 2.07\times10^{-15}\ \text{Wb}$보다 훨씬 작은 선속 변화를 잰다. 뇌의 미약한 자기장을 재는 뇌자도(MEG)에 쓰인다.
- **NV 센터와 간섭계**: 다이아몬드 속 질소–빈자리 결함의 전자 스핀은 나노미터 규모의 자기장을 재고, LIGO 같은 중력파 검출기는 빛의 양자 잡음을 줄이려고 **압축광**(squeezed light)을 쓴다(33장).

독립된 입자 $N$개로 위상을 재면 불확도가 $1/\sqrt N$로 줄어든다(표준 양자 한계. 특집 B 몬테카를로 오차와 같은 통계이다). 얽힌 입자를 쓰면 원리적으로 $1/N$(하이젠베르크 한계)까지 줄일 수 있다.

> **🔗 전공 연결: NMR과 큐비트는 같은 언어를 쓴다**
> 약학의 NMR 분광 분석과 수의학의 MRI는 원자핵 스핀(큐비트!)을 라디오파 펄스로 돌리고 세차운동이 내는 신호를 잰다(30장, 38장). $T_1$, $T_2$라는 이름 자체가 NMR에서 왔고, 위상 결맞음을 되살리는 **스핀 메아리**(spin echo)는 양자컴퓨터에서 잡음을 줄이는 펄스 기법의 원형이다. 블로흐 구면이라는 이름도 NMR의 선구자 블로흐(F. Bloch)에게서 왔다.

### 양자 키 분배(QKD)
**양자 키 분배**(quantum key distribution)는 두 사람이 비밀 키(무작위 비트열)를 공유하되 도청이 있으면 반드시 드러나게 하는 방법이다. 1984년 베넷과 브라사르의 **BB84**에서 앨리스는 무작위 비트와 무작위 기저($Z$ 또는 $X$)를 골라 광자를 $|0\rangle, |1\rangle$ 또는 $|+\rangle, |-\rangle$로 보내고, 밥은 무작위 기저로 측정한다. 둘은 공개 채널로 **기저만** 비교해 같았던 비트(평균 절반)만 남기고, 그 일부를 공개 비교해 오류율을 잰다. 오류율이 높으면 키를 버린다.

도청자 이브가 광자를 가로채 측정하면, 기저를 모르므로 절반은 틀린 기저로 측정해 상태를 바꾼다. 복제 불가 정리 때문에 몰래 복사할 수도 없다. 이브가 모든 광자를 가로채 측정한 뒤 다시 보내면 남은 비트의 오류율은 $\frac{1}{2}\times\frac{1}{2} = 25\%$가 된다(틀린 기저일 확률 1/2, 그때 밥이 틀릴 확률 1/2, 연습문제 14). 1991년 에커트(A. Ekert)는 얽힌 쌍과 벨 부등식 검사를 쓰는 E91을 제안했다. 안전성의 근거가 계산의 어려움이 아니라 물리 법칙이라는 점이 특징이지만, 실제 장치의 불완전성이 허점이 될 수 있고, 복제 불가 정리 때문에 신호를 증폭할 수 없어 광섬유 손실이 거리를 제한한다.

### 양자 순간이동
앨리스와 밥이 벨 쌍을 나눠 가지고 있으면, 앨리스는 미지의 상태 $|\psi\rangle$과 자기 쪽 큐비트에 벨 측정(예제 A.5)을 하고 결과 2비트를 고전 통신으로 보낸다. 밥은 그 2비트에 따라 X, Z 게이트를 걸어 $|\psi\rangle$을 얻는다. 원래 상태는 측정으로 사라지므로 복제 불가 정리에 어긋나지 않고, 고전 통신이 필요하므로 빛보다 빠르지도 않다. **양자 순간이동**(quantum teleportation)은 1993년 이론으로 제안되었고 1997년 광자로 처음 실험되었다.

---

## 핵심 정리

| 개념 | 핵심 식 | 관련 장 |
|---|---|---|
| 큐비트 | $\lvert\psi\rangle = \alpha\lvert 0\rangle + \beta\lvert 1\rangle$, $\lvert\alpha\rvert^2 + \lvert\beta\rvert^2 = 1$ | 37 |
| 블로흐 구면 | $\cos\frac{\theta}{2}\lvert 0\rangle + e^{i\varphi}\sin\frac{\theta}{2}\lvert 1\rangle$, $\vec{r} = (\langle X\rangle, \langle Y\rangle, \langle Z\rangle)$ | 38 |
| 보른 규칙 | $P(k) = \lvert\langle\phi_k\vert\psi\rangle\rvert^2$, 측정 후 붕괴 | 36, 37 |
| 텐서곱 | $n$큐비트 → $2^n$개 진폭, `np.kron` | — |
| 얽힘 판별 | $c_{00}c_{11} - c_{01}c_{10} \ne 0$ (2큐비트 순수 상태) | — |
| CHSH | 국소적 숨은 변수 $\lvert S\rvert \le 2$, 양자 최대 $2\sqrt2$ | 34 |
| 게이트 | 유니터리 $U^\dagger U = I$; H, X, Z, CNOT | 37 |
| 조지프슨 접합 | $I = I_c\sin\varphi$, $V = \frac{\hbar}{2e}\dot\varphi$, $L_J = \frac{\hbar}{2eI_c\cos\varphi}$ | 29 |
| 트랜스몬 | $E_{01} \approx \sqrt{8E_JE_C} - E_C$, 비조화성 $\approx -E_C$ | 29, 37 |
| 알고리즘 | 쇼어: 주기 찾기로 소인수분해; 그로버: $\sim\frac{\pi}{4}\sqrt N$ 질의 | — |
| 한계 | 결어긋남($T_1$, $T_2$), 복제 불가, 오류 정정 필요 | — |

---

## 연습문제

**기본**
1. $|\psi\rangle = \frac{1}{\sqrt5}(|0\rangle + 2i|1\rangle)$이 정규화되어 있음을 확인하고, $Z$ 기저와 $X$ 기저로 측정할 때 각 결과의 확률을 구하라.
2. $|-\rangle$, $|{-i}\rangle$, $\cos\frac{\pi}{8}|0\rangle + \sin\frac{\pi}{8}|1\rangle$의 블로흐 벡터를 구하라.
3. $H$가 유니터리이며 $H^2 = I$임을 확인하고, $HZH = X$를 보여라.
4. $|0\rangle\otimes|-\rangle$을 4성분 열벡터로 쓰고 얽힌 상태인지 판별하라.
5. 벨 상태 회로(H 다음 CNOT)에 $|01\rangle$, $|10\rangle$, $|11\rangle$을 넣으면 각각 어떤 벨 상태가 나오는가?
6. 진동수 $5\ \text{GHz}$인 큐비트의 에너지 $hf$는 몇 J, 몇 μeV인가? $hf = k_BT$인 온도는?

**응용**
7. (신호 불가) $|\Phi^+\rangle$에서 앨리스가 첫째 큐비트를 $X$ 기저로 측정하든 $Z$ 기저로 측정하든, 결과를 모르는 밥이 둘째 큐비트를 $Z$ 기저로 측정해 0을 얻을 확률은 1/2임을 보여라.
8. $c_{00}c_{11} - c_{01}c_{10} = 0$이면 곱 상태로 쓸 수 있음을 보여라. (힌트: 계수 행렬의 행렬식이 0이면 두 행이 평행하다.)
9. $|\Psi^-\rangle$에 대해 $E(a, b) = -\cos(a - b)$임을 보이고($x$-$z$ 평면 측정), $|S| = 2\sqrt2$가 되는 각도를 하나 찾아라.
10. 그로버 알고리즘에서 $k$번 반복 뒤 성공 확률은 $\sin^2((2k+1)\theta)$, $\sin\theta = 1/\sqrt N$이다. $N = 4$, $k = 1$에서 확률이 정확히 1임을 보이고, $N = 16$, $k = 3$의 확률을 본문 파이썬 결과와 비교하라.
11. 3큐비트 비트 반전 부호에서 오류가 없을 때와 각 큐비트가 뒤집혔을 때의 신드롬 $(Z_1Z_2, Z_2Z_3)$를 표로 정리하라.
12. $L_J$(작은 위상)와 $C$로 만든 LC 회로에서 $\hbar/\sqrt{L_JC} = \sqrt{8E_JE_C}$임을 보여라.

**도전**
13. (치렐손 한계) $\hat{S} = A\otimes(B + B') + A'\otimes(B - B')$이고 $A^2 = A'^2 = B^2 = B'^2 = I$일 때 $\hat{S}^2 = 4I - [A, A']\otimes[B, B']$임을 보이고, $|\langle\hat S\rangle| \le 2\sqrt2$를 유도하라. (힌트: 교환자의 노름은 2 이하.)
14. (파이썬) BB84를 numpy로 시뮬레이션하라. 광자 10만 개에 대해 무작위 비트·기저를 만들고, "틀린 기저로 측정하면 결과는 50:50"이라는 보른 규칙으로 밥의 결과를 정한 뒤, 기저가 같은 비트의 오류율을 도청이 없을 때와 이브가 모든 광자를 가로채 측정할 때 비교하라.

## 연습문제 답과 힌트
1. $\frac{1}{5}(1 + 4) = 1$. $P(0) = 1/5$, $P(1) = 4/5$. $\langle\pm|\psi\rangle = \frac{1}{\sqrt{10}}(1 \pm 2i)$이므로 $P(\pm) = 1/2$. 블로흐 벡터가 $y$-$z$ 평면에 있어 $r_x = 0$이기 때문이다.
2. $(-1, 0, 0)$, $(0, -1, 0)$, $(\frac{1}{\sqrt2}, 0, \frac{1}{\sqrt2})$ (마지막은 $\theta = \pi/4$, $\varphi = 0$).
3. $H$는 실수 대칭이므로 $H^\dagger = H$이고 $H^2 = I$. $ZH = \frac{1}{\sqrt2}\begin{pmatrix}1&1\\-1&1\end{pmatrix}$, $H(ZH) = \begin{pmatrix}0&1\\1&0\end{pmatrix} = X$.
4. $\frac{1}{\sqrt2}(1, -1, 0, 0)^T$. 행렬식 $0$이므로 곱 상태.
5. $|\Psi^+\rangle$, $|\Phi^-\rangle$, $|\Psi^-\rangle$. 예: $|10\rangle \to (|00\rangle - |10\rangle)/\sqrt2 \to (|00\rangle - |11\rangle)/\sqrt2$.
6. $3.31\times10^{-24}\ \text{J} = 20.7\ \mu\text{eV}$, $T = 0.24\ \text{K}$.
7. $Z$ 기저: 앨리스 결과에 따라 밥은 1/2 확률로 $|0\rangle$ 또는 $|1\rangle$, $P(0) = 1/2$. $X$ 기저: $|\Phi^+\rangle = (|{+}{+}\rangle + |{-}{-}\rangle)/\sqrt2$이므로 밥은 $|+\rangle$ 또는 $|-\rangle$이 되고 어느 쪽이든 $P(0) = 1/2$.
8. $(c_{10}, c_{11}) = \lambda(c_{00}, c_{01})$이면 $|\psi\rangle = (|0\rangle + \lambda|1\rangle)\otimes(c_{00}|0\rangle + c_{01}|1\rangle)$이다(첫 행이 0이면 $|1\rangle\otimes(\cdots)$).
9. $\langle Z\otimes Z\rangle = \langle X\otimes X\rangle = -1$, 교차항 0이므로 $E = -\cos(a - b)$. 본문과 같은 각도에서 $S = -2\sqrt2$.
10. $N = 4$: $\theta = 30°$, $\sin^2 90° = 1$. $N = 16$: $\theta = 14.48°$, $\sin^2(101.4°) = 0.9613$으로 일치한다.
11. 오류 없음 $(+1, +1)$, 1번 $(-1, +1)$, 2번 $(-1, -1)$, 3번 $(+1, -1)$. 네 경우가 모두 달라 위치를 정할 수 있고, $\alpha$, $\beta$와 무관하다.
12. $L_J = \hbar/2eI_c = \hbar^2/(4e^2E_J)$, $C = e^2/2E_C$이므로 $L_JC = \hbar^2/(8E_JE_C)$.
13. $(B \pm B')^2 = 2I \pm \{B, B'\}$, $(B + B')(B - B') = -[B, B']$ 등을 쓰면 $\hat{S}^2 = 4I - [A, A']\otimes[B, B']$. $\lVert\hat S^2\rVert \le 4 + 2\cdot2 = 8$이므로 $|\langle\hat S\rangle| \le 2\sqrt2$. 고전적으로는 교환자가 0이어서 $|S| \le 2$이다.
14. 도청이 없으면 오류율 0, 있으면 약 0.25. 힌트: `wrong = b_basis != basis`, `b_bits = np.where(wrong, rng.integers(0, 2, n), bits)`. 이브가 있으면 같은 처리를 한 번 먼저 하고 광자의 기저를 이브의 기저로 바꾼다.

## 영어 용어 정리
| 한글 | English |
|---|---|
| 큐비트 / 중첩 | qubit / superposition |
| 전역 위상 / 상대 위상 | global phase / relative phase |
| 블로흐 구면 | Bloch sphere |
| 파울리 행렬 | Pauli matrices |
| 보른 규칙 / 계산 기저 | Born rule / computational basis |
| 혼합 상태 | mixed state |
| 텐서곱 | tensor product |
| 곱 상태 / 얽힌 상태 | product state / entangled state |
| 벨 상태 / 벨 부등식 | Bell state / Bell inequality |
| 국소적 숨은 변수 이론 | local hidden variable theory |
| 양자 게이트 | quantum gate |
| 아다마르 게이트 | Hadamard gate |
| 복제 불가 정리 | no-cloning theorem |
| 조지프슨 접합 / 쿠퍼 쌍 | Josephson junction / Cooper pair |
| 비조화성 | anharmonicity |
| 거시적 양자 터널링 | macroscopic quantum tunnelling |
| 포획 이온 / 중성 원자 | trapped ion / neutral atom |
| 결어긋남 | decoherence |
| 양자 오류 정정 / 문턱 정리 | quantum error correction / threshold theorem |
| 양자 내성 암호 | post-quantum cryptography |
| 양자 키 분배 | quantum key distribution (QKD) |
| 양자 순간이동 | quantum teleportation |
