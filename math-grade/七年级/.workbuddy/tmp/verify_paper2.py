# -*- coding: utf-8 -*-
"""0002 杭州风格卷 逐题核算（100 分制）"""
from fractions import Fraction as F
import math

ok = []
def chk(name, got, exp):
    good = (got == exp)
    ok.append(good)
    print(("PASS " if good else "FAIL ") + f"{name}: got={got} exp={exp}")

# ---------- 选择题 10×3 ----------
chk("Q1 倒数(-2026)", F(-1, 2026), F(-1, 2026))
vals = [abs(-3) * -1, -(-2), 0, (-1) ** 2]
chk("Q2 四数", vals, [-3, 2, 0, 1])
chk("Q2 最小值", min(vals), -3)

# Q3 余角 90° - 32°18'
m = 90 * 60 - (32 * 60 + 18)
chk("Q3 余角", f"{m//60}°{m%60}′", "57°42′")

# Q5 (10b+a)+(10a+b) = 11(a+b)
a, b = 7, 3
chk("Q5 对调和", (10 * b + a) + (10 * a + b), 11 * (a + b))

# Q7 |a|=3,|b|=2, a<b -> a+b
sols = sorted({x + y for x in (3, -3) for y in (2, -2) if x < y})
chk("Q7 a+b", sols, [-5, -1])

# Q8 ∠BOD：OC 在 OA 与 OE 之间，∠COE=28 -> ∠AOC=62 -> 对顶角相等
aoc = 90 - 28
chk("Q8 ∠AOC", aoc, 62)
chk("Q8 ∠BOD", aoc, 62)

# Q9 5x+3 = 6x-4 -> x=7, 学生 38
x = None
for g in range(1, 20):
    if 5 * g + 3 == 6 * g - 4:
        x = g
chk("Q9 组数", x, 7)
chk("Q9 人数", 5 * x + 3, 38)

# Q10 n^2+2n = (n+1)^2-1
for n in (1, 2, 3, 4):
    chk(f"Q10 n={n}", n * n + 2 * n, (n + 1) ** 2 - 1)

# ---------- 填空题 6×4 ----------
chk("T11", (-1) ** 2026 - (-2) ** 3, 9)
chk("T12 平方为16", sorted([4, -4]), [-4, 4])
# T13 系数 -3/5, 次数 3
coef = F(-3, 5); deg = 2 + 1
chk("T13 系数", coef, F(-3, 5))
chk("T13 次数", deg, 3)
# T14 a^2+a=2 -> 3-2(a^2+a)
chk("T14", 3 - 2 * 2, -1)
# T15 8:30 钟面角
hour = 8 * 30 + 30 * 0.5
minute = 6 * 30
d = abs(hour - minute)
chk("T15 钟面角", min(d, 360 - d), 75)
# T16 1/2,2/5,3/10,4/17 -> 5/26
seq = [F(n, n * n + 1) for n in range(1, 6)]
chk("T16 前四项", seq[:4], [F(1, 2), F(2, 5), F(3, 10), F(4, 17)])
chk("T16 第五项", seq[4], F(5, 26))

# ---------- 解答题 ----------
chk("Q17(1)", -6 / -3 + (-2) ** 3 * F(1, 4), 0)
chk("Q17(2)", math.isqrt(49) - abs(-3) + (-1) ** 2025, 3)

# Q18(1) 4x+3 = 2(x-1)+7 -> x=1
lx, rx = 4 * 1 + 3, 2 * (1 - 1) + 7
chk("Q18(1) 代回", lx, rx)
# Q18(2) (x-1)/2-(2x+1)/3=1 -> x=-11
xv = F(-11)
chk("Q18(2) 代回", (xv - 1) / 2 - (2 * xv + 1) / 3, F(1))

# Q19 2(x^2-2xy)-3(x^2-xy)+x^2 = -xy ; x=-2,y=1/2
X, Y = -2, F(1, 2)
expr = 2 * (X ** 2 - 2 * X * Y) - 3 * (X ** 2 - X * Y) + X ** 2
chk("Q19", expr, -X * Y)
chk("Q19 值", expr, 1)

# Q20 AC=BD, AB=10, CD=4 -> AC=3 ; MN=(a+b)/2
AB, CD = 10, 4
chk("Q20 AC", (AB - CD) / 2, 3)
chk("Q20 MN (10,4)", (AB + CD) / 2, 7)
# 几何验算：A=0, AC=3 -> C=3, D=7, B=10, M=1.5, N=8.5
M, N = (0 + 3) / 2, (7 + 10) / 2
chk("Q20 MN 坐标验算", N - M, 7)
chk("Q20 公式验算", (10 + 4) / 2, 7)

# Q21
sol = [(i, 20 - i) for i in range(21) if 8 * i + 12 * (20 - i) == 196]
chk("Q21(1)", sol, [(11, 9)])
chk("Q21(2)", (15 * 8 + 20 * 12) * 0.9, 324)
chk("Q21(3) 29本", 29 * 8, 232)
chk("Q21(3) 30本9折", 30 * 8 * 0.9, 216)
chk("Q21(3) 更省", 232 - 216, 16)

# Q22 数轴动点：A=-6, B=2, vP=3 向右, vQ=1 向左
def P(t): return -6 + 3 * t
def Q(t): return 2 - t
chk("Q22(2) 相遇", [t for t in [F(i, 100) for i in range(0, 1000)] if P(t) == Q(t)][0], F(2))
sols = [t for t in [F(i, 100) for i in range(0, 1000)] if abs(P(t) - Q(t)) == 4]
chk("Q22(3)", sols, [F(1), F(3)])
chk("Q22(3) 检验 t=1", (P(1), Q(1), abs(P(1) - Q(1))), (-3, 1, 4))
chk("Q22(3) 检验 t=3", (P(3), Q(3), abs(P(3) - Q(3))), (3, -1, 4))

# ---------- 分值 ----------
choice, fill, essay = 10 * 3, 6 * 4, 6 + 6 + 6 + 8 + 10 + 10
print(f"\n分值：选择{choice} + 填空{fill} + 解答{essay} = {choice + fill + essay}")
chk("总分", choice + fill + essay, 100)

print("\nRESULT:", "ALL PASS" if all(ok) else "HAS FAIL")
