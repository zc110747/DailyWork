# -*- coding: utf-8 -*-
"""逐题核算 浙教版七年级(上) 温州风格期末模拟卷"""
from fractions import Fraction as F
import math

ok = []
def chk(name, got, exp):
    good = (got == exp)
    ok.append(good)
    print(("PASS " if good else "FAIL ") + f"{name}: got={got} exp={exp}")

# --- 选择题 ---
chk("Q1 相反数(-2026)", 2026, 2026)
chk("Q2 无理数", "sqrt7", "sqrt7")

# Q3 3046000 精确到万位 -> 305万 = 3.05e6
v = 3046000
q_wan = round(v / 10000) * 10000
chk("Q3 精确到万位", q_wan, 3050000)
chk("Q3 科学记数法", f"{q_wan/1e6:.2f}e6", "3.05e6")

# Q4 合并同类项 4a^2b - 3ba^2 = a^2b
a, b = 2, -3
chk("Q4 4a2b-3ba2", 4*a*a*b - 3*b*a*a, 1*a*a*b)

# Q5 3x-1=5 -> x=2 ; 2x+a=3 -> a=-1
x = F(6, 3); chk("Q5 x", x, F(2))
chk("Q5 a", 3 - 2*x, F(-1))

# Q6 ∠DOE = (∠AOC+∠BOC)/2 = 90
chk("Q6 ∠DOE", (70 + 110) / 2, 90)

# Q7 a^2+2a=3 -> 2a^2+4a-1 = 2*3-1 = 5
chk("Q7 整体代入", 2*3 - 1, 5)

# Q8 成本x, 标价1.4x, 8折=1.12x=224 -> x=200
chk("Q8 x", F(224) / (F(14, 10) * F(8, 10)), F(200))

# Q9 中点 (-3+2)/2
chk("Q9 中点", F(-3 + 2, 2), F(-1, 2))

# Q10 n^2
chk("Q10 n=4", 4**2, 16)

# --- 填空题 ---
chk("T11 |−5|", abs(-5), 5)
chk("T11 −3^2", -(3**2), -9)
chk("T12 √16", math.isqrt(16), 4)
chk("T12 √16的平方根", sorted([2, -2]), [-2, 2])
# T13 2x^m y^2 与 -3x^3 y^n 同类项 -> m=3,n=2
chk("T13 m+n", 3 + 2, 5)
# T14 余角25°18' -> 角=64°42' -> 补角=115°18'
ang = 90*60 - (25*60 + 18)
chk("T14 角", ang, 64*60 + 42)
bu = 180*60 - ang
chk("T14 补角", f"{bu//60}°{bu%60}′", "115°18′")
# T15 AB=10,C中点(5), BD=2 -> D=8 或 D=12 ; CD
C = F(10, 2)
cd = sorted([abs(F(8) - C), abs(F(12) - C)])
chk("T15 CD", cd, [F(3), F(7)])
# T16 x=3 -> 12 -> 156
def prog(x):
    n = 0
    while True:
        x = x * (x + 1); n += 1
        if x >= 20: return x
chk("T16 输出", prog(3), 156)

# --- 解答题 ---
chk("Q17(1)", -(3**2) + abs(-2) - (-4), -3)
chk("Q17(2)", 5 - (-2) + 1, 8)

x1 = sp = None
# Q18(1) 5x-2=3x+6 -> x=4
chk("Q18(1)", F(8, 2), 4)
# Q18(2) (2x-1)/3-(x+2)/2=1 -> x=14 校验
xv = F(14)
lhs = (2*xv - 1)/3 - (xv + 2)/2
chk("Q18(2) 代回", lhs, F(1))

# Q19 3(2a^2-ab)-2(3a^2-2ab) = ab ; a=-1,b=2 -> -2
aa, bb = -1, 2
chk("Q19", 3*(2*aa**2 - aa*bb) - 2*(3*aa**2 - 2*aa*bb), aa*bb)
chk("Q19 值", aa*bb, -2)

# Q20 AB=8 AC=3
AB, AC = F(8), F(3)
BC = AB - AC
chk("Q20 BC", BC, 5)
AM, AN = AB/2, AC/2
chk("Q20 MN", AM - AN, F(5, 2))

# Q21 x+y=30, 6x+10y=216
for xx in range(31):
    yy = 30 - xx
    if 6*xx + 10*yy == 216:
        chk("Q21 笔记/钢笔", (xx, yy), (21, 9))

# Q22
BOC = 180 - 50
chk("Q22 BOC", BOC, 130)
COD = BOC / 2
chk("Q22 COD", COD, 65)
chk("Q22 AOD", 50 + COD, 115)
DOB = COD
chk("Q22 BOE 同侧", 90 - DOB, 25)
chk("Q22 BOE 异侧", 90 + DOB, 155)

# Q23
chk("Q23(1)a", abs(2 - 5), 3)
chk("Q23(1)b", abs(-3 - 1), 4)
chk("Q23(2)", sorted([2 + 3, 2 - 3]), [-1, 5])
chk("Q23(3) a,b", (-2, 4), (-2, 4))
chk("Q23(3) AB", abs(4 - (-2)), 6)
mn = min(abs(t + 1) + abs(t - 3) for t in [i/10 for i in range(-30, 50)])
chk("Q23(4) 最小值", mn, 4)

# Q24 阶梯水价 20吨内3元, 超20吨部分5元
def fee(t):
    return 3*t if t <= 20 else 60 + 5*(t - 20)
chk("Q24(1)", fee(18), 54)
t26 = (90 - 60)/5 + 20
chk("Q24(2) 吨", t26, 26)
chk("Q24(2) 校验", fee(26), 90)
sol = []
for a7 in range(0, 41):
    a8 = 40 - a7
    if fee(a7) + fee(a8) == 132 and a8 > a7:
        sol.append((a7, a8))
chk("Q24(3) 唯一解", sol, [(14, 26)])
chk("Q24(3) 校验", fee(14) + fee(26), 132)

# --- 分值 ---
choice = 10*3
fill = 6*4
ans = 6 + 8 + 6 + 8 + 8 + 10 + 10 + 10
print(f"\n分值：选择{choice} + 填空{fill} + 解答{ans} = {choice+fill+ans}")
chk("总分", choice + fill + ans, 120)

print("\nRESULT:", "ALL PASS" if all(ok) else "HAS FAIL")
